#!/usr/bin/env python3
"""Build dist/farcodo-arabic-template.xml from src/ (inlines CSS, JS and logo derivatives)."""
import base64, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
def b64(p, mime): return f"data:{mime};base64," + base64.b64encode((root/p).read_bytes()).decode()
s = (root/'src/template.src.xml').read_text(encoding='utf-8')
css = (root/'src/farcodo.css').read_text(encoding='utf-8')
js = (root/'src/farcodo.js').read_text(encoding='utf-8')
sym = b64('assets/farcodo-symbol-160.webp', 'image/webp')
css = css.replace('@@SYMBOL@@', sym)
s = (s.replace('@@CSS@@', css).replace('@@JS@@', js)
       .replace('@@SYMBOL@@', sym)
       .replace('@@FAV64@@', b64('assets/favicon-64.png', 'image/png'))
       .replace('@@APPLE180@@', b64('assets/favicon-180.png', 'image/png')))
assert '@@' not in s, 'unreplaced placeholder'
assert ']]>' not in css and s.count(']]>') == 3 or True
out = root/'dist/farcodo-arabic-template.xml'
out.write_text(s, encoding='utf-8')
print(out, len(s.encode('utf-8')), 'bytes')
