import frappe


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


def update_cust_retailer_association(doc, method):

    if(doc.custom_sales_channel == "Web"):
        return
    else:
        # Get the customer linked to the sales order
        customer_doc = frappe.get_doc("Customer", doc.customer)

        if(customer_doc.customer_type == "Company") :
            if(doc.custom_end_customer):
                end_customer_doc = frappe.get_doc("Customer", doc.custom_end_customer)
                if (end_customer_doc.custom_assigned_retailer):
                    end_customer_doc.custom_assigned_retailer = customer_doc.custom_assigned_retailer
                    end_customer_doc.flags.ignore_permissions = True
                    end_customer_doc.save()

    
def calculate_sales_dist(doc, method):
     
    if(doc.custom_sales_channel == "Web"):
        return
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
