import sys
import glob
import re
import argparse
from archive import exit_code, complain

bracket_pat = re.compile(r'\[((?:\d+\s*,\s*)*\d+)\](?!\()')
superscript_pat = re.compile(r'<sup>\s*((?:\d+\s*,\s*)*\d+)\s*</sup>')
end_section_pat = re.compile(r'^(#+\s*(References|Works Cited|Endnotes)\s*$)', re.MULTILINE | re.IGNORECASE)
end_num_pat = re.compile(r'^\s*\[(?:<a id="[^"]+">)?(\d+)(?:</a>)?\](.*?)$', re.MULTILINE)
ref_point_pat = re.compile(bracket_pat.pattern + '|' + superscript_pat.pattern)

def split_body_and_end(content):
    end_section = end_section_pat.search(content)
    if end_section:
        return content[:end_section.start()], content[end_section.start():]
    else:
        return content, ''
    
def parse_comma_separated(txt):
    return [n.strip() for n in txt.split(',')]

def flatten_groups(groups):
    nums = []
    for group in groups:
        nums.extend(parse_comma_separated(group))
    return nums

def parse_ref_nums(text):
    brackets = flatten_groups(bracket_pat.findall(text))
    superscripts = flatten_groups(superscript_pat.findall(text))
    if brackets and superscripts:
        style = "mixed"
    elif brackets:
        style = "brackets"
    elif superscripts:
        style = "superscripts"
    else:
        style = "none"
    return brackets, superscripts, style

def check(filename, check_only):
    with open(filename, encoding='utf-8') as f:
        content = f.read()
    body, end = split_body_and_end(content)
    b_brackets, b_super, b_style = parse_ref_nums(body)
    e_brackets, e_super, e_style = parse_ref_nums(end)

    # Check for no-op and stuff the script can't fix.
    if e_style == "none":
        if b_style == "none":
            print(f"NOTE: {filename} has no ref nums. Nothing to do.")
        else:
            complain(f"No section at the end expands inline ref nums in {filename}. Need human fix.")
        return
    if b_style == "mixed" or e_style == "mixed":
        complain(f"Body ref style = {b_style}, end ref style = {e_style} in {filename}. Need human fix.")
        return
    if e_style == "superscripts":
        complain(f"Expanded refs at end use superscripts in {filename}. Need human fix.")
        return
    
    inline_nums = [int(n) for n in b_brackets] if b_brackets else [int(n) for n in b_super]
    end_nums = [int(n) for n in e_brackets] if e_brackets else [int(n) for n in e_super]
    issues = False

    # Check for orphans in either direction
    inline_set, expanded_set = set(inline_nums), set(end_nums)
    if inline_set != expanded_set:
        missing = expanded_set - inline_set
        extra = inline_set - expanded_set
        if missing:
            complain(f"Expanded refs at end not cited in inline text in {filename}: {sorted(missing)}. Need human fix.")
        if extra:
            complain(f"Inline refs have no expanded ref at end in {filename}: {sorted(extra)}. Need human fix.")
        if missing or extra:
            return

    # Check for gaps/out-of-order in inline refs and expanded forms
    gaps = False
    for category, nums in (("inline ref num", inline_nums), ("expanded ref", end_nums)):
        max_seen = 0
        for n in nums:
            if n > max_seen + 1:
                complain(f"Gap or out-of-order {category} [{n}] in {filename}.", not check_only)
                gaps = True
            max_seen = max(max_seen, n)

    if not gaps:
        print(f"No ref num issues found in {filename}.")

    return gaps

def extract_expanded_entries(end_section_text):
    prefix = None
    suffix = None
    entries = {}
    start = 0
    while True:
        m = end_num_pat.search(end_section_text, start)
        if m:
            entries[int(m.group(1))] = m.group(2).strip()
            if prefix is None:
                prefix = end_section_text[:m.start()]
            start = m.end()
        else:
            suffix = end_section_text[start:].rstrip() + '\n'
            break
    return entries, prefix, suffix

class RefPoint:
    def __init__(self, m, nums):
        self.m = m
        self.nums = nums
    def __str__(self):
        return f"RefPoint at {self.m.start()}: nums={self.nums}"

def find_ref_points(body):
    points = []
    for m in ref_point_pat.finditer(body):
        group = m.group(1) if m.group(1) else m.group(2)
        nums = parse_comma_separated(group)
        points.append(RefPoint(m, [int(n) for n in nums]))
    return points

def fix_gaps(filename, new):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    body, end_section = split_body_and_end(content)
    expanded_entries, prefix, suffix = extract_expanded_entries(end_section)
    remapped = {}
    fixed_body = ''
    body_offset = 0
    ref_points = find_ref_points(body)
    i = 1
    for point in ref_points:
        fixed_body += body[body_offset:point.m.start()]
        nums_at_this_point = []
        for old_num in point.nums:
            entry = expanded_entries[old_num]
            if remapped.get(entry) is None:
                remapped[entry] = i
                new_num = i
                i += 1
            else:
                new_num = remapped[entry]
            if (new_num != old_num):
                print(f"Remapped {old_num} to {new_num} in {filename}.")
            nums_at_this_point.append(new_num)
        fixed_body += f"[{', '.join(str(n) for n in nums_at_this_point)}]"
        body_offset = point.m.end()
    fixed_body += body[body_offset:]
    outfile = filename + '.new' if new else filename
    with open(outfile, 'w', encoding='utf-8') as f:
        f.write(fixed_body)
        f.write(prefix)
        tuples = sorted(remapped.items(), key=lambda x: x[1])
        f.write('\n\n'.join(f"[{item[1]}] {item[0]}" for item in tuples))
        f.write(suffix)
        print(f"Fixed ref numbering in {outfile}.")

def main():
    parser = argparse.ArgumentParser(description="Check/fix reference numbers in markdown files.")
    parser.add_argument('--check-only', action='store_true', help='Only check for problems, do not fix them')
    parser.add_argument('--except', dest='except_file', help='File containing filenames to exclude, one per line')
    parser.add_argument('--new', action='store_true', help='Save result in *.new instead of modifying files in place.')
    parser.add_argument('files', nargs='+', help='Markdown files or glob patterns to process')
    args = parser.parse_args()
    all_files = []
    for arg in args.files:
        all_files.extend(glob.glob(arg) or [arg])
    all_files = set(all_files)
    exclude = set()
    if args.except_file:
        with open(args.except_file, encoding='utf-8') as f:
            exclude = set([x for x in [x.strip() for x in f.readlines() if x.strip()] if not x.startswith('#')])
    unique_files = all_files - exclude
    for filename in unique_files:
        gaps = check(filename, args.check_only)
        if gaps and not args.check_only:
            fix_gaps(filename, args.new)
    sys.exit(exit_code)

if __name__ == '__main__':
    main()