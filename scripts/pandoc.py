import sys
from archive import *

def date_as_pdfdate(d):
    return f"D:{d:%Y%m%d}"

def main(item):
    os.chdir(repo_root)
    tmp = ".pdfmeta.tex"
    input_path = item.path
    output_path = item.path[:-3] + '.pdf'
    meta = item.meta
    author = meta['author']
    d = date_as_pdfdate(meta['date'])
    md = meta.get('revision_date', None)
    titl = meta['title']
    if len(titl) > 40:
        i = titl[:41].rfind(' ')
        if i > 10:
            titl = titl[:i] + '…'
        else:
            titl = titl[:39] + '…'
    if md:
        md = date_as_pdfdate(md)
    if isinstance(author, list):
        meta['author'] = ', '.join(author)
    keywords = meta.get('keywords', '')
    if isinstance(keywords, str) and keywords[0] == '"':
        keywords = keywords[1:-1]
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write(r'\AtBeginDocument{' + '\n')
        f.write(r'  \hypersetup{' + '\n')
        f.write(r'    pdftitle={' + meta['title'] + '},\n')
        f.write(r'    pdfauthor={' + meta['author'] + '},\n')
        f.write(r'    pdfcreationdate={' + d + '000000Z},\n')
        f.write(r'    pdfmoddate={' + md + '000000Z},\n')
        f.write(r'    pdfsubject={Codecraft Papers (item: ' + meta['item_id'] + ', version: ' + str(meta['version']) + ')},\n')
        f.write(r'    pdfkeywords={' + meta['keywords'] + '}\n')
        f.write('  }\n}\n')
        f.write(r'\newcommand{\ccitemid}{' + meta['item_id'] + '}\n')
        f.write(r'\newcommand{\ccversion}{' + str(meta['version']) + '}\n')
        f.write(r'\newcommand{\cctitle}{' + titl + '}\n')
    cmd = f'pandoc "{input_path}" -o "{output_path}" ' + \
        '--from=markdown+autolink_bare_uris+yaml_metadata_block+implicit_figures+link_attributes ' + \
        '--pdf-engine=xelatex ' + \
        '--resource-path=".:assets" ' + \
        '-V papersize=letter ' + \
        '-V fontsize=11pt ' + \
        '-V geometry:margin=2.7cm ' + \
        '-V mainfont="TeX Gyre Pagella" ' + \
        '-V monofont="Inconsolata" ' + \
        '-V microtypeoptions=protrusion=true ' + \
        '--include-in-header=scripts/pandoc/pkgs.tex ' + \
        '--include-in-header=.pdfmeta.tex ' + \
        '--include-in-header=scripts/pandoc/header.tex '
    print(cmd)
    ret = os.system(cmd)
    if not ret:
        os.remove(tmp)    
    sys.exit(ret)

if __name__ == '__main__':
    url = sys.argv[1]
    for item in internal_items():
        if item.url == url:
            main(item)
            break
    sys.stderr.write(f"Item {item} doesn't appear to exist in the archive.\n")
    sys.exit(1)
