#!/usr/bin/env python3
"""
email_thread_splitter.py

Splits multi-message PDFs into single-message files,
appends metadata to Email_Exhibit_Master_List.csv.
"""
import os, PyPDF2, csv

def split_pdf(input_path, output_dir):
    reader = PyPDF2.PdfReader(input_path)
    base = os.path.splitext(os.path.basename(input_path))[0]
    for i, page in enumerate(reader.pages, start=1):
        writer = PyPDF2.PdfWriter()
        writer.add_page(page)
        out_path = os.path.join(output_dir, f"{base}_page{i}.pdf")
        with open(out_path, "wb") as f:
            writer.write(f)
        yield out_path

def main():
    out_csv = "09 Master Indexes/Email_Exhibit_Master_List.csv"
    with open(out_csv, 'a', newline='') as csvfile:
        w = csv.writer(csvfile)
        for root, _, files in os.walk("08 Photographic Evidence"):
            for f in files:
                if f.lower().endswith('.pdf'):
                    full = os.path.join(root, f)
                    for piece in split_pdf(full, root):
                        w.writerow([root.strip('./'), os.path.basename(piece)])
if __name__ == "__main__":
    main()
