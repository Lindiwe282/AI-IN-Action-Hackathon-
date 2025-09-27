# data/create_sample_pdfs.py
import os
from fpdf import FPDF

def ensure_dir(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def create_pdf(lines, save_path, title=None):
    """
    Create a PDF file using fpdf2 (UTF-8 safe).
    lines: list of strings
    save_path: where to write the pdf
    title: optional title to show in output message
    """
    ensure_dir(save_path)
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    # Use a default font that supports basic UTF-8 characters.
    # fpdf2 will encode text as UTF-8 when possible.
    pdf.set_font("Arial", size=12)

    for line in lines:
        # Ensure we have a string and strip trailing newlines:
        text = str(line).rstrip("\n")
        # Write the line with multi_cell so it wraps automatically
        pdf.multi_cell(0, 8, txt=text)

    pdf.output(save_path)
    if title:
        print(f"✅ {title} created at: {save_path}")
    else:
        print(f"✅ PDF created at: {save_path}")


def create_legitimate_sample(save_path="data/sample_document.pdf"):
    lines = [
        "STANDARD BANK PERSONAL LOAN AGREEMENT",
        "",
        "Loan Amount: R10,000",
        "Interest Rate: 12% per annum",
        "",
        "Terms and Conditions apply.",
        "Please contact info@standardbank.co.za for more information.",
        "",
        "This is a legitimate loan offer for South African residents.",
        "",
        "For inquiries, please visit your nearest branch or contact our official email."
    ]
    create_pdf(lines, save_path, title="Legitimate sample PDF")



def create_fraudulent_sample(save_path="data/fraudulent_document.pdf"):
    lines = [
        "GUARANTEED 100% RETURNS ON YOUR INVESTMENT!",
        "",
        "Limited time offer - ACT NOW!",
        "Invest R11,000 and double your money in 7 days!",
        "",
        "No risk guaranteed profit. Send upfront payment of R5,000 for registration.",
        "Bitcoin investment opportunity - exclusive offer!",
        "",
        "Contact us immediately: scammer@example.com",
        "Don't miss out on this once-in-a-lifetime chance!",
        "",
        "This is a high-reward investment opportunity. No experience needed!",
        "Call now: +27 82 555 1234"
    ]
    create_pdf(lines, save_path, title="Fraudulent sample PDF")


if __name__ == "__main__":
    create_legitimate_sample()
    create_fraudulent_sample()
    print("All sample PDFs generated.")
