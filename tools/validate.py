#!/usr/bin/env python3
"""Local checks only. Passing these does NOT prove Blogger compatibility."""
import re, sys, subprocess, tempfile, pathlib
from lxml import etree
root = pathlib.Path(__file__).resolve().parent.parent
raw = (root/'farcodo-arabic-template.xml').read_bytes(); txt = raw.decode()
fails = 0
def ok(c, m):
    global fails; print(('PASS ' if c else 'FAIL ') + m); fails += (not c)
tree = etree.fromstring(raw); ok(True, 'XML well-formed')
ns = {'b': 'http://www.google.com/2005/gml/b'}
ok(len(tree.xpath('//b:skin', namespaces=ns)) == 1, 'one b:skin')
ok(len(tree.xpath('//b:widget[@type="Blog"]', namespaces=ns)) == 1, 'one Blog widget')
ids = [e.get('id') for e in tree.xpath('//b:section|//b:widget', namespaces=ns)]
dup = {i for i in ids if ids.count(i) > 1}; ok(not dup, f'unique section/widget ids ({len(ids)}) {dup or ""}')
for w in tree.xpath('//b:widget', namespaces=ns):
    inc = [i.get('id') for i in w.xpath('./b:includable', namespaces=ns)]
    ok(inc.count('main') == 1, f'{w.get("id")}: one main includable')
    for c in w.xpath('.//b:include[@name]', namespaces=ns):
        n = c.get('name')
        if n not in inc and n not in ('comments', 'all-head-content'): ok(False, f'{w.get("id")}: include {n} missing')
sk = re.search(r'<b:skin><!\[CDATA\[(.*?)\]\]></b:skin>', txt, re.S).group(1)
for v in re.findall(r'\$\(([\w.]+)\)', sk): ok(f'name="{v}"' in sk, f'skin variable declared: {v}')
js = re.findall(r'<script>//<!\[CDATA\[\n(.*?)//\]\]></script>', txt, re.S)[-1]
f = tempfile.NamedTemporaryFile('w', suffix='.js', delete=False); f.write(js); f.close()
ok(subprocess.run(['node', '--check', f.name]).returncode == 0, 'JS syntax')
body = re.sub(r'/\*.*?\*/', '', sk, flags=re.S); body = re.sub(r'url\("data:[^"]*"\)', 'url()', body)
ok(body.count('{') == body.count('}'), 'CSS braces balanced')
# Arabic-only UI scan (config key lines like "heading=" are admin syntax, not UI)
latin = re.compile(r'[A-Za-z]{2,}'); bad = []
def scan(s, w):
    for line in s.splitlines():
        line = line.strip()
        if not line or line.startswith('/') or re.match(r'^[a-z_0-9-]+\s*[=:]', line) or line.startswith('#') or line in ('NONE','[]'): continue
        if any(x not in ('Farcodo', 'arcodo') for x in latin.findall(line)): bad.append((w, line[:60]))
for e in tree.iter():
    if not isinstance(e.tag, str): continue
    t = etree.QName(e).localname
    if t in ('script', 'skin', 'style'): continue
    if t == 'widget-setting':
        if e.get('name') in ('content',) or (e.get('name') or '').startswith('text-'): scan(e.text or '', 'setting')
    elif e.text and etree.QName(e).namespace != ns['b']: scan(e.text, t)
    if e.tail: scan(e.tail, 'tail')
    for a in ('aria-label', 'placeholder', 'alt', 'title'):
        if e.get(a): scan(e.get(a), a)
for m in re.findall(r"'([^'\n(]*[\u0600-\u06FF][^'\n(]*)'", js): scan(m, 'js')
ok(not bad, 'no English UI text' + (str(bad[:6]) if bad else ''))
print('size %.1f KB' % (len(raw) / 1024)); sys.exit(1 if fails else 0)
