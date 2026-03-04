from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from datetime import datetime, timedelta
import os

def generate_invoice(data):

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("invoice.html")

    subtotal = sum(item["quantity"] * item["rate"] for item in data["items"])
    tax = subtotal * data["tax_rate"]
    total = subtotal + tax

    for item in data["items"]:
        item["total"] = item["quantity"] * item["rate"]

    html_out = template.render(
        freelancer_name=data["freelancer_name"],
        freelancer_email=data["freelancer_email"],
        client_name=data["client_name"],
        client_email=data["client_email"],
        invoice_number=data["invoice_number"],
        issue_date=datetime.now().strftime("%Y-%m-%d"),
        due_date=(datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"),
        items=data["items"],
        subtotal=f"{subtotal:.2f}",
        tax=f"{tax:.2f}",
        total=f"{total:.2f}",
        payment_terms="Net 14",
        bank_details=data["bank_details"]
    )

    os.makedirs("invoices", exist_ok=True)
    output_path = f"invoices/{data['invoice_number']}.pdf"

#    HTML(string=html_out).write_pdf(output_path)
    HTML(string=html_out, base_url=os.getcwd()).write_pdf(output_path)
    
    return output_path