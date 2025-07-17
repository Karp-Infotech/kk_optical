import frappe

def assign_warehouse(doc, method):


    # Get the logged-in user
    current_user = frappe.session.user
    user_doc = frappe.get_doc("User", current_user)
    retailer_doc = frappe.get_doc("Retailer", user_doc.retailer)
    
    items_not_available = []
    for item in doc.items:
        print(item.item_group)

        if item.item_group == "Eyeglasses" and not is_stock_in_warehosue(item,retailer_doc.store_warehouse):
            item.warehouse = retailer_doc.store_warehouse
            items_not_available.append(item.item_code)

    if items_not_available:
        item_list = ", ".join(items_not_available)
        frappe.msgprint(
            f"The following items are last piece. Please keep them ready for pickup </b>: {item_list}"
        )
    # Assign Source Store to SO
    doc.custom_source_store = retailer_doc.store_warehouse


def is_stock_in_warehosue(item, warehouse):
    # Fetch the actual quantity available in the warehouse
    actual_qty = frappe.db.get_value(
        "Bin",
        {"item_code": item.item_code, "warehouse": warehouse},
        "actual_qty"
    )

    # Default actual_qty to 0 if no Bin entry exists
    actual_qty = actual_qty or 0

    # Check if available stock is less than required quantity
    if actual_qty < item.qty:
        return False
    else:
         return True


def update_cust_store_association(doc, method):

    # Get the customer linked to the sales order
    customer = frappe.get_doc("Customer", doc.customer)
    current_user = frappe.session.user
    user_doc = frappe.get_doc("User", current_user)
    retailer_doc = frappe.get_doc("Retailer", user_doc.retailer)

    if customer.custom_customer_relationship == "Indirect":
        # Set the warehouse field in the Customer doctype based on the Sales Order warehouse
        customer.custom_store_association = retailer_doc.store_warehouse
        # Bypass permission check for write
        customer.flags.ignore_permissions = True
        customer.save()

    
def calculate_sales_dist(doc, method):
    
    # Get the customer linked to the sales order
    customer = frappe.get_doc("Customer", doc.customer)
    kk_sales_portion = 0
    sales_dist_plan = get_sale_dist_plan()
    for item in doc.items:
        item_doc = frappe.get_doc("Item", item.item_code)
        for sd_item in sales_dist_plan.sales_distribution_items:
                if(sd_item.brand == item_doc.brand and sd_item.item_group == item_doc.item_group
                    and sd_item.sales_channel == doc.custom_sales_channel 
                    and sd_item.customer_relationship == customer.custom_customer_relationship) :
                    kk_sales_portion += item.net_amount * sd_item.kk_share_ / 100
                    break
        doc.custom_klear_kut_payment_amount = kk_sales_portion
        doc.save
        frappe.db.commit()
    
    




def get_sale_dist_plan():
	
    current_user = frappe.session.user
    user_doc = frappe.get_doc("User", current_user)
    retailer_doc = frappe.get_doc("Retailer", user_doc.retailer)
    sdp = retailer_doc = frappe.get_doc("Sales Distribution Plan", retailer_doc.custom_sdp)
    return sdp
