import frappe

def add_kk_data(doc, method):
    current_user = frappe.session.user
    user_doc = frappe.get_doc("User", current_user)

    if(user_doc.user_type == "Website User") :
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