import os
import sys

from archive import *

paper_cat = cat_index('Papers')
paper_required_fields = ['title', 'author', 'date', 'pdf_url']

def check_meta(item, meta):
    """
    Checks metadata for required fields if item is of category 'Papers'.
    Complains if any required field is missing.
    """
    if item.cat_index == paper_cat:
        missing = [field for field in required_fields if not meta.get(field)]
        if missing:
            complain(f"{item.url}: missing required metadata fields for Papers: {', '.join(missing)}")

def main():
    for item in indexed_items():
        if not item.is_external:
            if not os.path.isfile(item.path):
                complain(f"Missing file: {item.url}")
                continue
        if not item.meta:
            complain(f"Could not load metadata for: {item.url}")
        else:
            check_meta(item, item.meta)
    if not exit_code:
        print("All requirements met.")
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
