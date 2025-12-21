import sys
import glob
import re
import argparse

complaints_found = False

def complain(msg):
    global complaints_found
    print(f"Error: {msg}", file=sys.stderr)
    complaints_found = True

def parse_citations_and_refs(content):
    acm_refs = re.findall(r'\[(\d+)\]', content)
    superscripts = re.findall(r'<sup>(\d+)</sup>', content)
    endnote_section = re.search(r'^(#+\s*Endnotes\s*$)', content, re.MULTILINE | re.IGNORECASE)
    style = None
    if acm_refs and superscripts:
        style = "mixed"
    elif acm_refs:
        style = "ACM bracketed inline refs"
    elif superscripts:
        style = "superscript inline refs"
    elif endnote_section:
        style = "endnotes"
    else:
        style = "none"
    return acm_refs, superscripts, endnote_section, style

def find_refs_section(content):
    return re.search(r'^(#+\s*(References|Works Cited|Endnotes)\s*$)', content, re.MULTILINE | re.IGNORECASE)

def extract_ref_nums(refs_text):
    endnote_entries = re.findall(r'^\s*\[(?:<a id="[^"]+">)?([0-9]+)(?:</a>)?\]', refs_text, re.MULTILINE)
    ref_entries = re.findall(r'^\s*\[([0-9]+)\]', refs_text, re.MULTILINE)
    return [int(n) for n in endnote_entries] if endnote_entries else [int(n) for n in ref_entries]

def analyze(filename):
    with open(filename, encoding='utf-8') as f:
        content = f.read()
    acm_refs, superscripts, endnote_section, style = parse_citations_and_refs(content)
    if style == "mixed":
        complain(f"Inconsistent footnote formats in {filename}")
    if style == "none":
        complain(f"No footnotes found in {filename}")
    print(f"{filename}: Detected style: {style}")
    refs = [int(n) for n in acm_refs] if acm_refs else [int(n) for n in superscripts]
    max_seen = 0
    seen = set()
    for n in refs:
        if n > max_seen + 1:
            complain(f"Gap or out-of-order citation [{n}] in {filename}")
        max_seen = max(max_seen, n)
        seen.add(n)
    ref_section = find_refs_section(content)
    if not ref_section:
        complain(f"No References, Works Cited, or Endnotes section found in {filename}")
    else:
        ref_start = ref_section.end()
        refs_text = content[ref_start:]
        ref_nums = extract_ref_nums(refs_text)
        max_ref = 0
        for n in ref_nums:
            if n > max_ref + 1:
                complain(f"Gap or out-of-order reference [{n}] in {filename}")
            max_ref = max(max_ref, n)
        inline_set = set(refs)
        ref_set = set(ref_nums)
        if inline_set != ref_set:
            missing = ref_set - inline_set
            extra = inline_set - ref_set
            if missing:
                complain(f"References/Endnotes not cited inline in {filename}: {sorted(missing)}")
            if extra:
                complain(f"Inline citations without reference/endnote entries in {filename}: {sorted(extra)}")

def fix_citations_and_refs(filename):
    with open(filename, encoding='utf-8') as f:
        content = f.read()
    acm_refs, superscripts, endnote_section, style = parse_citations_and_refs(content)
    if style == "mixed" or style == "none":
        complain(f"Cannot fix: {filename} has style '{style}'")
        return
    print(f"{filename}: Detected style: {style} (fixing)")
    refs = [int(n) for n in acm_refs] if acm_refs else [int(n) for n in superscripts]
    # Build mapping from old to new numbers based on first appearance
    mapping = {}
    new_refs = []
    next_num = 1
    for n in refs:
        if n not in mapping:
            mapping[n] = next_num
            next_num += 1
        new_refs.append(mapping[n])
    # Replace inline citations
    if acm_refs:
        def repl(match):
            old = int(match.group(1))
            return f"[{mapping[old]}]"
        content = re.sub(r'\[(\d+)\]', repl, content)
    elif superscripts:
        def repl(match):
            old = int(match.group(1))
            return f"<sup>{mapping[old]}</sup>"
        content = re.sub(r'<sup>(\d+)</sup>', repl, content)
    # Fix references/endnotes section
    ref_section = find_refs_section(content)
    if not ref_section:
        complain(f"No References, Works Cited, or Endnotes section found in {filename}")
        return
    ref_start = ref_section.end()
    refs_text = content[ref_start:]
    ref_lines = refs_text.splitlines(keepends=True)
    # Parse and remap reference lines
    ref_entry_pat = re.compile(r'^(\s*)\[(?:<a id="[^"]+">)?([0-9]+)(?:</a>)?\](.*)$')
    ref_entries = []
    for line in ref_lines:
        m = ref_entry_pat.match(line)
        if m:
            old_num = int(m.group(2))
            ref_entries.append((old_num, line))
    # Resort and renumber
    ref_entries_sorted = sorted(ref_entries, key=lambda x: refs.index(x[0]) if x[0] in refs else float('inf'))
    new_ref_lines = []
    for i, (old_num, line) in enumerate(ref_entries_sorted, 1):
        new_line = re.sub(r'\[(?:<a id="[^"]+">)?([0-9]+)(?:</a>)?\]', f'[{i}]', line, count=1)
        new_ref_lines.append(new_line)
    # Replace old reference section with new one
    new_refs_text = ''.join(new_ref_lines) + ''.join(ref_lines[len(ref_entries):])
    content = content[:ref_start] + new_refs_text
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed numbering in {filename}")

def all_footnoted_files(filenames):
    for filename in filenames:
        try:
            with open(filename, encoding='utf-8') as f:
                content = f.read()
                # ACM inline bracketed numbers: [1], [2], etc.
                acm_refs = re.findall(r'\[\d+\]', content)
                # Superscripted numbers: <sup>1</sup>, <sup>2</sup>, ...
                superscripts = re.findall(r'<sup>\d+</sup>', content)
                has_acm = bool(acm_refs)
                has_supers = len([n for n in superscripts if n.startswith('<sup>1')]) >= 1 and len(superscripts) >= 3
                if has_acm or has_supers:
                    yield filename
        except Exception as e:
            print(f"Error reading {filename}: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Check/fix footnotes in markdown files.")
    parser.add_argument('--no-fix', action='store_true', help='Only report problems, do not fix them')
    parser.add_argument('files', nargs='+', help='Markdown files or glob patterns to process')
    args = parser.parse_args()

    # Expand globs if needed
    all_files = []
    for arg in args.files:
        expanded = glob.glob(arg)
        if expanded:
            all_files.extend(expanded)
        else:
            all_files.append(arg)

    seen = set()
    unique_files = [f for f in all_files if not (f in seen or seen.add(f))]

    if args.no_fix:
        for filename in all_footnoted_files(unique_files):
            analyze(filename)
        if complaints_found:
            sys.exit(1)
        else:
            sys.exit(0)
    else:
        for filename in all_footnoted_files(unique_files):
            fix_citations_and_refs(filename)
        if complaints_found:
            sys.exit(1)
        else:
            sys.exit(0)

if __name__ == '__main__':
    main()