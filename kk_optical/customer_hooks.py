import frappe

def assign_store_association(doc, method):

    # Set a store association on first save
    if not doc.custom_store_association:
        doc.custom_customer_relationship = "Indirect"
        # Example: Set retailer based on current user
        current_user = frappe.session.user
        user_doc = frappe.get_doc("User", current_user)
        if user_doc.retailer:
            retailer_doc = frappe.get_doc("Retailer", user_doc.retailer)
            doc.custom_store_association = retailer_doc.store_warehouse
            doc.db_update()  # save the change to DB
    