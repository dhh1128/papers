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
    # Match single or comma-separated numbers in brackets
    acm_refs = re.findall(r'\[((?:\d+\s*,\s*)*\d+)\]', content)
    # Flatten comma-separated lists
    acm_refs_flat = []
    for group in acm_refs:
        acm_refs_flat.extend([n.strip() for n in group.split(',')])
    superscripts = re.findall(r'<sup>(\d+)</sup>', content)
    endnote_section = re.search(r'^(#+\s*Endnotes\s*$)', content, re.MULTILINE | re.IGNORECASE)
    style = None
    if acm_refs_flat and superscripts:
        style = "mixed"
    elif acm_refs_flat:
        style = "ACM bracketed inline refs"
    elif superscripts:
        style = "superscript inline refs"
    elif endnote_section:
        style = "endnotes"
    else:
        style = "none"
    return acm_refs_flat, superscripts, endnote_section, style

def find_refs_section(content):
    return re.search(r'^(#+\s*(References|Works Cited|Endnotes)\s*$)', content, re.MULTILINE | re.IGNORECASE)

def extract_ref_lines(refs_text):
    # Returns a list of (original_num, line, content) for each reference line
    ref_entry_pat = re.compile(r'^(\s*)\[(?:<a id="[^"]+">)?([0-9]+)(?:</a>)?\](.*)$')
    ref_lines = refs_text.splitlines(keepends=True)
    entries = []
    for line in ref_lines:
        m = ref_entry_pat.match(line)
        if m:
            old_num = int(m.group(2))
            content = m.group(3).strip()
            entries.append((old_num, line, content))
    return entries, ref_lines

def analyze(filename):
    with open(filename, encoding='utf-8') as f:
        content = f.read()
    acm_refs, superscripts, endnote_section, style = parse_citations_and_refs(content)
    if style == "mixed":
        complain(f"Inconsistent footnote formats in {filename}")
    if style == "none":
        print(f"NOTE: {filename} has no footnotes or references. Nothing to do.")
        return
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
        ref_entries, _ = extract_ref_lines(refs_text)
        ref_nums = [num for num, _, _ in ref_entries]
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
    # 1. Parse references section to build mapping from original number to reference content
    ref_section = find_refs_section(content)
    if not ref_section:
        complain(f"No References, Works Cited, or Endnotes section found in {filename}")
        return
    ref_start = ref_section.end()
    refs_text = content[ref_start:]
    ref_entries, ref_lines = extract_ref_lines(refs_text)
    ref_dict = {num: (line, ref_content) for num, line, ref_content in ref_entries}
    # 2. Scan inline citations in order, assign new numbers to unique sources by reference content
    inline_pat = re.compile(r'\[((?:\d+\s*,\s*)*\d+)\]')
    inline_nums = []
    for m in inline_pat.finditer(content[:ref_start]):
        nums = [int(n.strip()) for n in m.group(1).split(',')]
        inline_nums.extend(nums)
    content_to_newnum = {}
    num_to_content = {num: ref_content for num, _, ref_content in ref_entries}
    mapping = {}
    new_order = []
    next_num = 1
    for n in inline_nums:
        ref_content = num_to_content.get(n)
        if ref_content is None:
            complain(f"Inline citation [{n}] has no matching reference entry in {filename}")
            continue
        if ref_content not in content_to_newnum:
            content_to_newnum[ref_content] = next_num
            mapping[n] = next_num
            new_order.append(ref_content)
            next_num += 1
        else:
            mapping[n] = content_to_newnum[ref_content]
    # 3. Replace all inline citations with new numbers (including lists)
    def repl(match):
        nums = [int(n.strip()) for n in match.group(1).split(',')]
        newnums = [str(mapping.get(n, n)) for n in nums]
        return f"[{', '.join(newnums)}]"
    content = inline_pat.sub(repl, content[:ref_start]) + content[ref_start:]
    # 4. Rebuild references section in new order, one entry per unique source
    new_ref_lines = []
    for i, ref_content in enumerate(new_order, 1):
        # Find the original line for this content
        for num, line, c in ref_entries:
            if c == ref_content:
                # Replace the number in the line with the new number
                new_line = re.sub(r'\[(?:<a id="[^"]+">)?([0-9]+)(?:</a>)?\]', f'[{i}]', line, count=1)
                new_ref_lines.append(new_line)
                break
    # Add any non-reference lines after the last reference
    last_ref_idx = 0
    for i, line in enumerate(ref_lines):
        if any(line == entry[1] for entry in ref_entries):
            last_ref_idx = i
    new_refs_text = ''.join(new_ref_lines) + ''.join(ref_lines[last_ref_idx+1:])
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