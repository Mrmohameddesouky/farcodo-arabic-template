#!/usr/bin/env python3
"""Local checks only. Passing these does NOT prove Blogger compatibility."""
import re, sys, subprocess, tempfile, pathlib
from lxml import etree
root = pathlib.Path(__file__).resolve().parent.parent
p = root/'dist/farcodo-arabic-template.xml'
raw = p.read_bytes()
fails = 0
def ok(c, m):
    global fails
    print(('PASS ' if c else 'FAIL ') + m)
    if not c: fails += 1
# 1. XML well-formed
try:
    tree = etree.fromstring(raw, etree.XMLParser(resolve_entities=False)); ok(True, 'XML is well-formed')
except Exception as e:
    ok(False, f'XML parse: {e}'); sys.exit(1)
B='http://www.google.com/2005/gml/b'
ns={'b':B,'x':'http://www.w3.org/1999/xhtml'}
# 2. structure
ok(len(tree.xpath('//b:skin',namespaces=ns))==1, 'exactly one b:skin')
ok(len(tree.xpath('//b:widget[@type="Blog"]',namespaces=ns))==1, 'exactly one Blog widget')
ids=[e.get('id') for e in tree.xpath('//b:section|//b:widget',namespaces=ns)]
ok(len(ids)==len(set(ids)), f'unique section/widget ids ({len(ids)})')
for e in tree.xpath('//b:widget',namespaces=ns):
    inc=[i.get('id') for i in e.xpath('./b:includable',namespaces=ns)]
    ok(inc.count('main')==1, f'{e.get("id")}: single main includable')
    for call in e.xpath('.//b:include[@name]',namespaces=ns):
        n=call.get('name')
        if n in inc: continue
        if n in ('comments','all-head-content'): print(f'NOTE {e.get("id")}: relies on Blogger default includable "{n}"'); continue
        ok(False, f'{e.get("id")}: include "{n}" has no includable')
# 3. JS syntax
js='\n'.join(re.findall(r'<script>//<!\[CDATA\[\n(.*?)//\]\]></script>',raw.decode(),re.S))
with tempfile.NamedTemporaryFile('w',suffix='.js',delete=False) as f: f.write(js)
r=subprocess.run(['node','--check',f.name],capture_output=True,text=True); ok(r.returncode==0,'JavaScript syntax (node --check)'+r.stderr[:200])
# 4. CSS brace balance + no ]]>
css=re.search(r'<b:skin><!\[CDATA\[(.*?)\]\]></b:skin>',raw.decode(),re.S).group(1)
body=re.sub(r'/\*.*?\*/','',css,flags=re.S); body=re.sub(r'url\("data:[^"]*"\)','url()',body)
ok(body.count('{')==body.count('}'),f'CSS braces balanced ({body.count("{")})')
ok('<Variable' in css,'skin variables declared')
# 5. Arabic-only interface scan (visible text + a11y attrs)
allowed=re.compile(r'^(Farcodo|arcodo|404|IBM Plex Sans Arabic)$')
latin=re.compile(r'[A-Za-z]{2,}')
bad=[]
def scan(s,where):
    s=s.strip()
    if not s or s.startswith('/') or s.startswith('[]') or s=='NONE': return
    for w in latin.findall(s):
        if not allowed.match(w) and w not in ('Farcodo','arcodo'): bad.append((where,s[:70]))
for el in tree.iter():
    if not isinstance(el.tag,str): continue
    tag=etree.QName(el).localname
    if tag in ('script','skin','style'): continue
    if tag=='widget-setting':
        if (el.get('name') or '').startswith('text-') or el.get('name')=='content': scan(el.text or '','setting')
    elif el.text and etree.QName(el).namespace!=B: scan(el.text,tag)
    if el.tail: scan(el.tail,'tail')
    for a in ('aria-label','placeholder','alt','title'):
        if el.get(a): scan(el.get(a),a)
# JS strings
for m in re.findall(r"'([^']*[\u0600-\u06FF][^']*)'",js): scan(m,'js')
ok(not bad,'no English UI text in markup/JS strings'+('' if not bad else ' -> '+str(bad[:8])))
print('\nSize: %.1f KB'%(len(raw)/1024))
sys.exit(1 if fails else 0)
