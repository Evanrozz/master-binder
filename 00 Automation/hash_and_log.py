
cat > "00 Automation/hash_and_log.py" << 'EOF'
#!/usr/bin/env python3
"""
hash_and_log.py

Walks the repo, computes SHA-256 for each file,
writes side-car .sha256.txt, and appends rows to Email_Exhibit_Master_List.csv
and RTB_Document_Master_List.csv.
"""
import os, hashlib, csv

def sha256sum(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def main():
    master_docs = "09 Master Indexes/RTB_Document_Master_List.csv"
    email_docs  = "09 Master Indexes/Email_Exhibit_Master_List.csv"
    with open(master_docs, 'a', newline='') as md, \
         open(email_docs,  'a', newline='') as ed:
        md_writer = csv.writer(md)
        ed_writer = csv.writer(ed)
        for root, _, files in os.walk('.'):
            if root.startswith('./00 Automation') or root.startswith('./.git'):
                continue
            for fname in files:
                fpath = os.path.join(root, fname)
                digest = sha256sum(fpath)
                with open(fpath + '.sha256.txt', 'w') as hf:
                    hf.write(digest)
                # Example: write to the appropriate CSV (customize as needed)
                if fname.lower().endswith('.pdf') and 'email' in root.lower():
                    ed_writer.writerow([root.strip('./'), fname, digest])
                else:
                    md_writer.writerow([root.strip('./'), fname, digest])

if __name__ == "__main__":
    main()
