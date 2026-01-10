import sys
import glob
import re
import argparse
from archive import exit_code, complain

def parse_footnotes(content):
    acm_refs = re.findall(r'\[((?:\d+\s*,\s*)*\d+)\](?!\()', content)
    acm_refs_flat = []
    for group in acm_refs:
        acm_refs_flat.extend([n.strip() for n in group.split(',')])
    superscripts = re.findall(r'<sup>(\d+)</sup>', content)
    ref_section = re.search(r'^(#+\s*(References|Works Cited|Endnotes)\s*$)', content, re.MULTILINE | re.IGNORECASE)
    style = None
    if acm_refs_flat and superscripts:
        style = "mixed"
    elif acm_refs_flat:
        style = "acm"
    elif superscripts:
        style = "superscript"
    elif ref_section:
        style = "endnotes"
    else:
        style = "none"
    return acm_refs_flat, superscripts, ref_section, style

def extract_ref_entries(refs_text):
    pat = re.compile(r'^\s*\[(?:<a id="[^"]+">)?(\d+)(?:</a>)?\](.*)$', re.MULTILINE)
    return [(int(m.group(1)), m.group(2).strip()) for m in pat.finditer(refs_text)]

def check_and_fix(filename, check_only):
    with open(filename, encoding='utf-8') as f:
        content = f.read()
    acm_refs, superscripts, ref_section, style = parse_footnotes(content)
    if style == "mixed":
        complain(f"Inconsistent footnote formats in {filename}")
        return
    if style == "none":
        print(f"NOTE: {filename} has no footnotes or references. Nothing to do.")
        return
    refs = [int(n) for n in acm_refs] if acm_refs else [int(n) for n in superscripts]
    if not ref_section:
        complain(f"No References, Works Cited, or Endnotes section found in {filename}")
        return
    ref_start = ref_section.end()
    refs_text = content[ref_start:]
    ref_entries = extract_ref_entries(refs_text)
    ref_nums = [num for num, _ in ref_entries]
    issues = False
    # Check for gaps/out-of-order in citations and references
    for seq, nums in (("citation", refs), ("reference", ref_nums)):
        max_seen = 0
        for n in nums:
            if n > max_seen + 1:
                complain(f"Gap or out-of-order {seq} [{n}] in {filename}")
                issues = True
            max_seen = max(max_seen, n)
    # Check for mismatches
    inline_set, ref_set = set(refs), set(ref_nums)
    if inline_set != ref_set:
        missing = ref_set - inline_set
        extra = inline_set - ref_set
        if missing:
            complain(f"References/Endnotes not cited inline in {filename}: {sorted(missing)}")
            issues = True
        if extra:
            complain(f"Inline citations without reference/endnote entries in {filename}: {sorted(extra)}")
            issues = True
    if not issues:
        print(f"No reference numbering issues found in {filename}.")
        return
    if check_only or not issues:
        return
    # Fixing logic
    pat = re.compile(r'\[((?:\d+\s*,\s*)*\d+)\]')
    inline_nums = []
    for m in pat.finditer(content[:ref_start]):
        nums = [int(n.strip()) for n in m.group(1).split(',')]
        inline_nums.extend(nums)
    num_to_content = {num: ref_content for num, ref_content in ref_entries}
    content_to_newnum, mapping, new_order = {}, {}, []
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
    def repl(match):
        nums = [int(n.strip()) for n in match.group(1).split(',')]
        newnums = [str(mapping.get(n, n)) for n in nums]
        return f"[{', '.join(newnums)}]"
    new_content = pat.sub(repl, content[:ref_start]) + content[ref_start:]
    # Rebuild references
    new_ref_lines = [f"[{i}] {ref_content}\n" for i, ref_content in enumerate(new_order, 1)]
    # Add any non-reference lines after the last reference
    ref_lines = refs_text.splitlines(keepends=True)
    last_ref_idx = 0
    for i, line in enumerate(ref_lines):
        if any(str(num) in line for num, _ in ref_entries):
            last_ref_idx = i
    new_refs_text = ''.join(new_ref_lines) + ''.join(ref_lines[last_ref_idx+1:])
    new_content = new_content[:ref_start] + new_refs_text
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Fixed numbering in {filename}")

def main():
    parser = argparse.ArgumentParser(description="Check/fix footnotes in markdown files.")
    parser.add_argument('--check-only', action='store_true', help='Only check for problems, do not fix them')
    parser.add_argument('--except', dest='except_file', help='File containing filenames to exclude, one per line')
    parser.add_argument('files', nargs='+', help='Markdown files or glob patterns to process')
    args = parser.parse_args()
    all_files = []
    for arg in args.files:
        all_files.extend(glob.glob(arg) or [arg])
    exclude = set()
    if args.except_file:
        with open(args.except_file, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    exclude.update(glob.glob(line) or [line])
    seen = set()
    unique_files = [f for f in all_files if not (f in seen or seen.add(f)) and f not in exclude]
    for filename in unique_files:
        check_and_fix(filename, args.check_only)
    sys.exit(exit_code)

if __name__ == '__main__':
    main()