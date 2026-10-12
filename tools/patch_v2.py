#!/usr/bin/env python3
"""One-shot upgrade: v1 (user-edited XML) -> v2. Kept for audit; the XML itself is the source of truth."""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
p = root/'farcodo-arabic-template.xml'
s = (root/'backup/farcodo-arabic-template.v1-backup.xml').read_text(encoding='utf-8')

def rep(old, new, n=1):
    global s
    assert s.count(old) == n, (s.count(old), old[:80])
    s = s.replace(old, new)

# ---------- head / skin ----------
rep('wght@400;500;600;700', 'wght@400;500;700')
rep('Version: 1.0.0', 'Version: 2.0.0')
rep('<Variable name="brand.cyan" description="السماوي" type="color" default="#00c8ff" value="#00c8ff"/>',
    '<Variable name="brand.cyan" description="السماوي" type="color" default="#00c8ff" value="#00c8ff"/>\n'
    '<Variable name="footer.bg" description="خلفية التذييل" type="color" default="#07122e" value="#07122e"/>\n'
    '<Variable name="layout.width" description="أقصى عرض للمحتوى" type="length" default="1240px" min="960px" max="1500px" value="1240px"/>\n'
    '<Variable name="card.radius" description="استدارة البطاقات" type="length" default="16px" min="0px" max="28px" value="16px"/>')
rep('--r:16px;--max:1240px;', '--r:$(card.radius);--max:$(layout.width);')
rep('.fc-footer{background:#07122e;', '.fc-footer{background:$(footer.bg);')

NEWCSS = r'''
/* ===== v2: layout-driven gadgets, banner, social, sections ===== */
.fc-cfgwrap,#hero-banner .widget,#home-sections .widget,#brand-settings .widget{display:none}
.fc-brand [hidden]{display:none}
.fc-brand.is-custom{direction:rtl;gap:10px}
.fc-brand.is-custom img{height:40px;width:auto;margin:0}
.fc-hero[hidden]{display:none}
.fc-banner{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);align-items:center;gap:28px;padding:clamp(24px,5vw,56px);border-radius:calc(var(--r) + 8px);background:linear-gradient(135deg,var(--navy) 0%,#0a3b9c 62%,var(--blue) 100%);color:#fff;margin-bottom:28px;position:relative;overflow:hidden}
.fc-banner:not(.has-img){grid-template-columns:minmax(0,1fr)}
.fc-banner.is-center{text-align:center;justify-items:center}
.fc-banner .fc-chip{background:var(--grad);color:#fff}
.fc-banner-t{margin:12px 0 10px;font-size:clamp(28px,4.2vw,46px);line-height:1.4;font-weight:700}
.fc-banner-d{margin:0 0 24px;color:#d6e0f7;font-size:18px;max-width:60ch}
.fc-banner.is-center .fc-banner-d{margin-inline:auto}
.fc-banner-btns{display:flex;gap:12px;flex-wrap:wrap}
.fc-banner.is-center .fc-banner-btns{justify-content:center}
.fc-banner .btn:not(.btn-p){background:rgba(255,255,255,.1);color:#fff;border-color:rgba(255,255,255,.35)}
.fc-banner .btn:not(.btn-p):hover{background:rgba(255,255,255,.2)}
.fc-banner-img img{width:100%;height:auto;border-radius:16px;display:block}
.fc-sec:first-child{margin-top:0}
.fc-hero+.fc-sec,.fc-sec{margin-top:48px}
.fc-grid[data-n="1"]{grid-template-columns:minmax(0,1fr)}
.fc-grid[data-n="2"]{grid-template-columns:repeat(2,minmax(0,1fr))}
.fc-grid[data-n="3"]{grid-template-columns:repeat(3,minmax(0,1fr))}
.fc-grid[data-n="4"]{grid-template-columns:repeat(4,minmax(0,1fr))}
.fc-list{grid-template-columns:repeat(2,minmax(0,1fr))}
.fc-list .fc-card{flex-direction:row}
.fc-list .fc-thumb{width:38%;aspect-ratio:auto;min-height:150px;flex:none}
.fc-list .fc-snip{-webkit-line-clamp:2}
.fc-clist{list-style:none;margin:0;padding:0;background:var(--surface);border:1px solid var(--line);border-radius:var(--r)}
.fc-clist li{display:flex;justify-content:space-between;gap:16px;align-items:baseline;padding:14px 18px;border-bottom:1px solid var(--line)}
.fc-clist li:last-child{border-bottom:0}
.fc-clist a{color:var(--ink);font-weight:600}.fc-clist time{color:var(--muted);font-size:13.5px;white-space:nowrap}
.fc-state .btn{margin-inline-start:10px;padding:6px 14px}
.fc-social{list-style:none;margin:0;padding:0;display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.fc-social:empty{display:none}
.fc-social a{display:inline-flex;align-items:center;justify-content:center;min-width:38px;min-height:38px;border-radius:999px;border:1px solid var(--line);color:var(--ink);padding:0 10px;font-size:14px}
.fc-social a.is-icon{width:38px;padding:0}
.fc-social a:hover{border-color:var(--blue);color:var(--link);text-decoration:none}
.fc-hdrsoc{display:flex}.fc-hdrsoc .fc-social a{border-color:transparent;width:36px;min-width:36px;min-height:36px;height:36px}
.fc-footer .fc-social{margin-top:16px}
.fc-footer .fc-social a{color:#c9d5f0;border-color:#22305a}.fc-footer .fc-social a:hover{color:#fff;border-color:var(--cyan)}
.fc-drawer>.fc-social{margin-top:18px;padding-top:18px;border-top:1px solid var(--line)}
.fc-tw{overflow-x:auto;margin:1.4em 0;border:1px solid var(--line);border-radius:12px;-webkit-overflow-scrolling:touch}
.fc-tw table,.post-body .fc-tw table{display:table;width:100%;min-width:520px;margin:0;border:0;font-size:.92em;line-height:1.7}
.post-body th{background:color-mix(in srgb,var(--blue) 10%,transparent);text-align:start;font-weight:700}
.post-body tbody tr:nth-child(even){background:color-mix(in srgb,var(--blue) 4%,transparent)}
.fc-tw th,.fc-tw td{border-width:0 0 1px 0}.fc-tw tr:last-child td{border-bottom:0}
.fc-pre{position:relative;margin:1.4em 0}.fc-pre pre{margin:0;padding-top:42px}
.fc-copy{position:absolute;top:8px;inset-inline-end:8px;border:1px solid rgba(255,255,255,.25);background:rgba(255,255,255,.08);color:#e6edff;border-radius:8px;padding:4px 12px;font:500 13px var(--font);cursor:pointer}
.fc-copy:hover{background:rgba(255,255,255,.18)}
@media (max-width:1100px){.fc-grid[data-n="4"]{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:900px){.fc-grid[data-n="3"]{grid-template-columns:repeat(2,minmax(0,1fr))}.fc-banner{grid-template-columns:minmax(0,1fr)}.fc-hdrsoc{display:none}.fc-list{grid-template-columns:minmax(0,1fr)}}
@media (max-width:600px){.fc-grid[data-n]{grid-template-columns:minmax(0,1fr)}.fc-banner-btns .btn{flex:1;justify-content:center}.fc-list .fc-thumb{width:34%}.fc-clist li{flex-direction:column;gap:2px}}
'''
rep(']]></b:skin>', NEWCSS + ']]></b:skin>')

# ---------- header ----------
SOCIAL_INC = ("<b:includable id='main' var='this'>\n"
 "<ul class='fc-social'><b:loop values='data:links' var='link'><li><a expr:href='data:link.target' rel='me noopener' target='_blank'><data:link.name/></a></li></b:loop></ul>\n"
 "</b:includable>")
def social_widget(wid, title):
    return (f"<b:widget id='{wid}' locked='false' title='{title}' type='LinkList' version='2' visible='true'>\n"
            "<b:widget-settings>\n<b:widget-setting name='sorting'>NONE</b:widget-setting>\n</b:widget-settings>\n"
            + SOCIAL_INC + "\n</b:widget>")
rep("<div class='fc-acts'>\n<form action='/search' class='fc-search' method='get' role='search'>\n<input aria-label='ابحث في الموقع' autocomplete='off'",
    "<div class='fc-acts'>\n<b:section class='fc-hdrsoc' id='header-social' maxwidgets='1' showaddelement='yes'>\n"
    + social_widget('LinkList3', 'روابط التواصل في الرأس') + "\n</b:section>\n"
    "<form action='/search' class='fc-search' method='get' role='search'>\n<input aria-label='ابحث في الموقع' autocomplete='off'")

CFG_INC = ("<b:includable id='main'>\n<div class='widget HTML fc-cfg'><b:if cond='data:title != \"\"'><h3 class='title'><data:title/></h3></b:if>"
           "<div class='widget-content'><data:content/></div></div>\n</b:includable>")
def cfg_widget(wid, title, content):
    return (f"<b:widget id='{wid}' locked='false' title='{title}' type='HTML' version='2' visible='true'>\n"
            f"<b:widget-settings>\n<b:widget-setting name='content'>{content}</b:widget-setting>\n</b:widget-settings>\n"
            + CFG_INC + "\n</b:widget>")

BRAND = ("# اترك القيم فارغة لاستخدام شعار فاركودو الأصلي (الرمز + arcodo).\n"
         "# logo = رابط صورة شعارك (https://...)  |  name = اسم الموقع كنص بجانب الشعار\n"
         "logo=\nname=\nalt=")
rep("</header>\n\n<div class='fc-wrap fc-main-wrap'>",
    "</header>\n<div class='fc-cfgwrap' hidden='hidden'>\n<b:section class='fc-brandsec' id='brand-settings' maxwidgets='1' showaddelement='no'>\n"
    + cfg_widget('HTML3', 'الشعار واسم الموقع', BRAND) + "\n</b:section>\n</div>\n\n<div class='fc-wrap fc-main-wrap'>")

# ---------- hero banner section (before Blog1) ----------
HERO = ("# اللافتة الرئيسية للصفحة الأولى. لإخفائها: hidden=yes  أو احذف الأداة من التخطيط.\n"
        "badge=تقنية بالعربية\n"
        "heading=كل ما يهمك في التقنية والذكاء الاصطناعي\n"
        "description=شروحات ومراجعات وأدوات مختارة بعناية، مكتوبة بلغة واضحة لتفهمها وتستفيد منها مباشرة.\n"
        "button1=ابدأ من هنا | /search/label/الذكاء الاصطناعي\n"
        "button2=استكشف الأقسام | #fc-sections\n"
        "image=\nalt=\nalign=right\nposts=show")
rep("<b:section class='fc-mainsec' id='main' showaddelement='no'>",
    "<b:section class='fc-herosec' id='hero-banner' maxwidgets='1' showaddelement='yes'>\n"
    + cfg_widget('HTML2', 'اللافتة الرئيسية', HERO) + "\n</b:section>\n"
    "<b:section class='fc-mainsec' id='main' showaddelement='no'>")

# ---------- home sections (replaces LinkList1) ----------
def sec(wid, title, label, sub, extra=''):
    return cfg_widget(wid, title, "# قسم في الصفحة الرئيسية. عنوان القسم هو عنوان هذه الأداة.\n"
                      f"label={label}\nsubtitle={sub}\ncount=4\nlayout=grid{extra}")
SECTIONS = ("<b:section class='fc-homesec' id='home-sections' maxwidgets='12' showaddelement='yes'>\n"
  + sec('HTML4', 'الذكاء الاصطناعي', 'الذكاء الاصطناعي', 'أدوات وتطبيقات وأخبار تصنع مستقبل التقنية') + "\n"
  + sec('HTML5', 'التقنية', 'التقنية', 'أخبار وشروحات تبسّط عالم التقنية') + "\n"
  + sec('HTML6', 'صناعة المحتوى', 'صناعة المحتوى', 'أفكار وأساليب تساعدك على إنتاج محتوى أفضل') + "\n"
  + sec('HTML7', 'أدوات مفيدة', 'أدوات مفيدة', 'أدوات عملية توفّر وقتك وتزيد إنتاجيتك') + "\n"
  + "</b:section>")
m = re.search(r"<b:section class='fc-homecats'.*?</b:section>", s, re.S); assert m
s = s[:m.start()] + SECTIONS + s[m.end():]

# ---------- footer ----------
rep("<b:section class='fc-footsec' id='footer-about' maxwidgets='1' showaddelement='yes'>", "<b:section class='fc-footsec' id='footer-about' maxwidgets='3' showaddelement='yes'>")
rep("<b:section class='fc-footsec' id='footer-pages' maxwidgets='1' showaddelement='yes'>", "<b:section class='fc-footsec' id='footer-pages' maxwidgets='3' showaddelement='yes'>")
rep("<b:section class='fc-footsec' id='footer-labels' maxwidgets='1' showaddelement='yes'>", "<b:section class='fc-footsec' id='footer-labels' maxwidgets='3' showaddelement='yes'>")
i = s.index("id='footer-about'"); j = s.index("</b:section>", i)
s = s[:j] + social_widget('LinkList4', 'روابط التواصل في التذييل') + "\n" + s[j:]

# ---------- JS ----------
rep(r'[ \\u00a0]', r'[ \u00a0]', 2)
a = s.index('  /* ---------- Home: configurable category sections ---------- */')
b = s.index('  /* ---------- Post enhancements ---------- */')
NEWJS = (root/'tools/v2.js.txt').read_text(encoding='utf-8')
s = s[:a] + NEWJS + '\n' + s[b:]
rep("    initTheme(); initHeaderMenus(); initDrawer(); cats(); post(); otherLD();",
    "    initTheme(); brand(); initHeaderMenus(); social(); initDrawer(); banner(); homeSections(); content(); post(); otherLD();")
rep("    open: 'فتح القائمة', close: 'إغلاق القائمة'",
    "    open: 'فتح القائمة', close: 'إغلاق القائمة', retry: 'إعادة المحاولة',\n    copy: 'نسخ', copied2: 'تم النسخ', tbl: 'جدول قابل للتمرير'")
rep("function orgObj() { return { '@type': 'Organization', name: 'Farcodo', url: location.origin + '/' }; }",
    "function orgObj() {\n    var o = { '@type': 'Organization', name: 'Farcodo', url: location.origin + '/' };\n"
    "    var sa = $$('.fc-social a').map(function (a) { return a.href; }).filter(function (h, i, arr) { return /^https?:/.test(h) && arr.indexOf(h) === i; });\n"
    "    if (sa.length) o.sameAs = sa; return o;\n  }")
rep("var img = meta('og:image'); if (img) o.image = [img];",
    "var img = meta('og:image') || (($('.post-body img', art) || {}).src || ''); if (img) o.image = [img];\n"
    "    var kw = $$('.fc-chips a', art).map(function (a) { return a.textContent.trim(); }).filter(Boolean);\n"
    "    if (kw.length) { o.keywords = kw.join('، '); o.articleSection = kw[0]; }\n"
    "    var bd = $('.post-body', art); if (bd) o.wordCount = (bd.textContent || '').trim().split(/\\s+/).filter(Boolean).length;")
p.write_text(s, encoding='utf-8'); print('ok', len(s))
