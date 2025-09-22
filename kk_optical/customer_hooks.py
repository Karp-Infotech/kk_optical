import frappe

def add_kk_data(doc, method):

    # Set a store association on first save
    if not doc.custom_store_association:
        # Example: Set retailer based on current user
        current_user = frappe.session.user
        user_doc = frappe.get_doc("User", current_user)
        print ("User Type : " + user_doc.user_type)
        if(user_doc.user_type == "Website User") :
            doc.custom_customer_relationship = "Direct"
            if(not doc.customer_name) : 
                copy_username_to_custmer (user_doc, doc)
            assign_loyalty_program(doc)
            doc.save()


def copy_username_to_custmer (user, customer) :
    if (user.first_name and user.last_name):
        customer.customer_name = user.first_name + user.last_name
    else : 
        customer.customer_name = user.first_name

def assign_loyalty_program(customer): 
    k_ws_settings = frappe.get_single("Karp Webshop Settings") 
    customer.loyalty_program = k_ws_settings.b2c_loyalty_program