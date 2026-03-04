import sys
import os

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.invoice_service import generate_invoice
from app.email_service import send_invoice

invoice_data = {
    "invoice_number": "2026-005",
    "freelancer_name": "Teknology Solutions",
    "freelancer_email": "auribe@teknowsolutions.com",
    "client_name": "Acme Corp",
    "client_email": "auribem84@gmail.com",
    "items": [
        {"description": "Backend Development", "quantity": 20, "rate": 75},
        {"description": "Frontend Design", "quantity": 10, "rate": 50}
    ],
    "tax_rate": 0.2,
    "bank_details": "IBAN: XX00 0000 0000 0000"
}

pdf_path = generate_invoice(invoice_data)
send_invoice(invoice_data["client_email"], pdf_path, invoice_data["invoice_number"])

print("Invoice generated and sent successfully!")