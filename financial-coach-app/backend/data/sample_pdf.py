# data/create_sample_pdf.py
from fpdf import FPDF
import os

def create_sample_pdf(save_path="data/sample_document.pdf"):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", size=12)
    
    text_lines = [
        "STANDARD BANK PERSONAL LOAN AGREEMENT",
        "",
        "Loan Amount: R50,000",
        "Interest Rate: 12% per annum",
        "",
        "Terms and Conditions apply.",
        "Please contact info@standardbank.co.za for more information.",
        "",
        "This is a legitimate loan offer for South African residents.",
        "",
        "Do not miss out on this opportunity!"
    ]
    
    for line in text_lines:
        pdf.multi_cell(0, 10, line)
    
    pdf.output(save_path)
    print(f"✅ Sample PDF created at {save_path}")

if __name__ == "__main__":
    create_sample_pdf()
