#!/usr/bin/env python3
import re
import sys
from PyPDF2 import PdfReader, PdfWriter

def split_email_pdf(input_pdf_path):
    reader = PdfReader(input_pdf_path)
    boundaries = [0]
    header_regex = re.compile(r"^(Subject:|From:|Date:|To:)", re.IGNORECASE)

    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        # look at first 10 lines for headers or forwarded markers
        preview = "\n".join(text.splitlines()[:10])
        if i > 0 and (re.search(r"Forwarded message", preview, re.IGNORECASE)
                      or header_regex.search(preview)):
            boundaries.append(i)
    boundaries.append(len(reader.pages))

    for idx in range(len(boundaries) - 1):
        writer = PdfWriter()
        for p in range(boundaries[idx], boundaries[idx + 1]):
            writer.add_page(reader.pages[p])
        out_path = f"{input_pdf_path[:-4]}_part{idx+1}.pdf"
        with open(out_path, "wb") as out_f:
            writer.write(out_f)
        print(f"Created: {out_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 email_pdf_splitter.py <input_file.pdf>")
        sys.exit(1)
    split_email_pdf(sys.argv[1])

