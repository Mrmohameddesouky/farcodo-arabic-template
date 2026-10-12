/* Farcodo Arabic — original script. No third-party libraries, no tracking. */
(function () {
  'use strict';
  var d = document;
  function $(s, c) { return (c || d).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); }
  function el(t, c, x) { var e = d.createElement(t); if (c) e.className = c; if (x != null) e.textContent = x; return e; }

  var T = {
    copied: 'تم نسخ الرابط', copyFail: 'تعذّر نسخ الرابط',
    loading: 'جارٍ تحميل المقالات…', err: 'تعذّر تحميل المقالات حاليًا. حاول مرة أخرى لاحقًا.',
    empty: 'لا توجد مقالات في هذا القسم بعد.', noRel: 'لا توجد مقالات ذات صلة حاليًا.',
    all: 'عرض كل المقالات', read: 'وقت القراءة', upd: 'آخر تحديث',
    dark: 'التبديل إلى الوضع الفاتح', light: 'التبديل إلى الوضع الداكن',
    open: 'فتح القائمة', close: 'إغلاق القائمة'
  };

  function mins(n) {
    n = Math.max(1, Math.round(n));
    if (n === 1) return 'دقيقة واحدة';
    if (n === 2) return 'دقيقتان';
    if (n <= 10) return n + ' دقائق';
    return n + ' دقيقة';
  }
  function fmt(iso) {
    try { return new Date(iso).toLocaleDateString('ar-u-nu-latn', { year: 'numeric', month: 'long', day: 'numeric' }); }
    catch (e) { return ''; }
  }
  function strip(h) {
    try { return (new DOMParser().parseFromString(h || '', 'text/html').body.textContent || '').replace(/\s+/g, ' ').trim(); }
    catch (e) { return ''; }
  }
  function bigImg(u) {
    return u ? u.replace(/\/s\d+(-[a-z]+)*\//, '/w640-h360-c/').replace(/=s\d+(-[a-z]+)*$/, '=w640-h360-c') : '';
  }
  function pathKey(u) { return String(u || '').replace(/^https?:\/\/[^\/]+/, '').split(/[?#]/)[0]; }

  var tt;
  function toast(m) {
    var t = $('#fc-toast'); if (!t) return;
    t.textContent = m; t.classList.add('show');
    clearTimeout(tt); tt = setTimeout(function () { t.classList.remove('show'); }, 2200);
  }

  /* ---------- Theme ---------- */
  function syncTheme() {
    var t = d.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
    var b = $('#fc-theme');
    if (b) { b.setAttribute('aria-pressed', t === 'dark' ? 'true' : 'false'); b.setAttribute('aria-label', t === 'dark' ? T.dark : T.light); }
  }
  function initTheme() {
    var b = $('#fc-theme'); syncTheme();
    if (!b) return;
    b.addEventListener('click', function () {
      var n = d.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      d.documentElement.setAttribute('data-theme', n);
      try { localStorage.setItem('fc-theme', n); } catch (e) {}
      syncTheme();
    });
  }

  /* ---------- Mobile drawer ---------- */
  function initDrawer() {
    var btn = $('#fc-menu'), dr = $('#fc-drawer'); if (!btn || !dr) return;
    var nav = $('.fc-nav ul'), box = $('.fc-drawer-nav', dr);
    if (nav && box) box.appendChild(nav.cloneNode(true));
    function tg(o) {
      dr.hidden = !o;
      btn.setAttribute('aria-expanded', o ? 'true' : 'false');
      btn.setAttribute('aria-label', o ? T.close : T.open);
      d.body.classList.toggle('fc-lock', o);
    }
    btn.addEventListener('click', function () { tg(dr.hidden); });
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !dr.hidden) { tg(false); btn.focus(); } });
    dr.addEventListener('click', function (e) { if (e.target.closest && e.target.closest('a')) tg(false); });
    if (window.matchMedia) {
      var mq = window.matchMedia('(min-width:901px)');
      var f = function (e) { if (e.matches && !dr.hidden) tg(false); };
      if (mq.addEventListener) mq.addEventListener('change', f); else if (mq.addListener) mq.addListener(f);
    }
  }

  /* ---------- Feeds & cards ---------- */
  function feed(path, n) {
    return fetch(path + (path.indexOf('?') > -1 ? '&' : '?') + 'alt=json&max-results=' + n, { credentials: 'same-origin' })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); });
  }
  function norm(e) {
    var url = '';
    (e.link || []).forEach(function (l) { if (l.rel === 'alternate') url = l.href; });
    var raw = (e.summary && e.summary.$t) || (e.content && e.content.$t) || '';
    var s = strip(raw); if (s.length > 130) s = s.slice(0, 130).replace(/\s+\S*$/, '') + '…';
    return { title: (e.title && e.title.$t) || '', url: url, img: e.media$thumbnail ? bigImg(e.media$thumbnail.url) : '',
      date: (e.published && e.published.$t) || '', snip: s };
  }
  function card(p) {
    var a = el('article', 'fc-card'), th = el('a', 'fc-thumb');
    th.href = p.url; th.tabIndex = -1; th.setAttribute('aria-hidden', 'true');
    if (p.img) { var im = new Image(); im.alt = ''; im.width = 640; im.height = 360; im.loading = 'lazy'; im.decoding = 'async'; im.src = p.img; th.appendChild(im); }
    else th.appendChild(el('span', 'fc-ph'));
    a.appendChild(th);
    var b = el('div', 'fc-body'), h = el('h3', 'fc-t'), l = el('a', null, p.title);
    l.href = p.url; h.appendChild(l); b.appendChild(h);
    if (p.snip) b.appendChild(el('p', 'fc-snip', p.snip));
    if (p.date) { var m = el('div', 'fc-meta'), t = el('time', null, fmt(p.date)); t.setAttribute('datetime', p.date); m.appendChild(t); b.appendChild(m); }
    a.appendChild(b); return a;
  }
  function fill(grid, state, entries, emptyMsg) {
    grid.textContent = '';
    if (!entries.length) { state.textContent = emptyMsg; state.hidden = false; return; }
    state.hidden = true;
    entries.forEach(function (e) { grid.appendChild(card(norm(e))); });
  }

  /* ---------- Home: configurable category sections ---------- */
  function parseCat(a) {
    var parts = a.textContent.split('|'), href = a.getAttribute('href') || '', label = '';
    var m = href.match(/\/search\/label\/([^?#\/]+)/);
    if (m) { try { label = decodeURIComponent(m[1]); } catch (e) { label = m[1]; } }
    return { title: parts[0].trim(), sub: (parts[1] || '').trim(), href: href, label: label };
  }
  function cats() {
    var src = $('#fc-cats-src'), out = $('#fc-cats'); if (!src || !out) return;
    var io = ('IntersectionObserver' in window) ? new IntersectionObserver(function (es) {
      es.forEach(function (x) { if (x.isIntersecting) { io.unobserve(x.target); x.target.__load(); } });
    }, { rootMargin: '300px' }) : null;
    $$('a', src).forEach(function (a, i) {
      var c = parseCat(a); if (!c.label || !c.title) return;
      var s = el('section', 'fc-sec'), hd = el('header', 'fc-sec-head'), tw = el('div'), hid = 'fc-cat-' + i;
      var h = el('h2', 'fc-sec-t', c.title); h.id = hid; tw.appendChild(h);
      if (c.sub) tw.appendChild(el('p', 'fc-sec-sub', c.sub));
      hd.appendChild(tw);
      var more = el('a', 'fc-more', T.all); more.href = c.href; more.setAttribute('aria-label', T.all + ': ' + c.title); hd.appendChild(more);
      s.setAttribute('aria-labelledby', hid); s.appendChild(hd);
      var st = el('p', 'fc-state', T.loading); st.setAttribute('role', 'status');
      var g = el('div', 'fc-grid fc-grid4'); s.appendChild(st); s.appendChild(g); out.appendChild(s);
      s.__load = function () {
        feed('/feeds/posts/default/-/' + encodeURIComponent(c.label), 4)
          .then(function (j) { fill(g, st, (j.feed && j.feed.entry) || [], T.empty); })
          .catch(function () { st.textContent = T.err; });
      };
      if (io) io.observe(s); else s.__load();
    });
  }

  /* ---------- Post enhancements ---------- */
  function post() {
    var art = $('.fc-article'); if (!art) return;
    var body = $('.post-body', art);
    var url = (($('link[rel=canonical]') || {}).href) || location.href.split('#')[0];
    var title = ($('.fc-title', art) || {}).textContent || d.title;

    if (body) {
      var n = (body.textContent || '').trim().split(/\s+/).filter(Boolean).length;
      var rt = $('.fc-rt', art); if (rt) rt.textContent = T.read + ': ' + mins(n / 190);
      $$('img', body).forEach(function (i, k) { if (k > 0 && !i.hasAttribute('loading')) i.setAttribute('loading', 'lazy'); i.setAttribute('decoding', 'async'); });
    }

    var u = encodeURIComponent(url), t = encodeURIComponent(title);
    var map = {
      x: 'https://twitter.com/intent/tweet?text=' + t + '&url=' + u,
      facebook: 'https://www.facebook.com/sharer/sharer.php?u=' + u,
      whatsapp: 'https://wa.me/?text=' + t + '%20' + u,
      telegram: 'https://t.me/share/url?url=' + u + '&text=' + t,
      linkedin: 'https://www.linkedin.com/sharing/share-offsite/?url=' + u
    };
    $$('[data-share]', art).forEach(function (a) { var k = a.getAttribute('data-share'); if (map[k]) { a.href = map[k]; a.target = '_blank'; a.rel = 'noopener noreferrer'; } });
    var cp = $('[data-copy]', art);
    if (cp) cp.addEventListener('click', function () {
      function ok() { toast(T.copied); } function ko() { toast(T.copyFail); }
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(url).then(ok, ko);
      else { try { var x = el('textarea'); x.value = url; x.setAttribute('readonly', ''); x.style.position = 'fixed'; x.style.opacity = '0'; d.body.appendChild(x); x.select(); var r = d.execCommand('copy'); d.body.removeChild(x); r ? ok() : ko(); } catch (e) { ko(); } }
    });
    var nb = $('[data-native]', art);
    if (nb && navigator.share) { nb.hidden = false; nb.addEventListener('click', function () { navigator.share({ title: title, url: url }).catch(function () {}); }); }

    // Dates + structured data
    var id = art.getAttribute('data-id'), pub = '', mod = '';
    var done = function () { articleLD(art, title, url, pub, mod); };
    if (id) {
      feed('/feeds/posts/default/' + encodeURIComponent(id), 1).then(function (j) {
        var e = j.entry || {}; pub = (e.published && e.published.$t) || ''; mod = (e.updated && e.updated.$t) || '';
        var up = $('.fc-upd', art);
        if (up && mod && pub && fmt(mod) !== fmt(pub)) { up.textContent = T.upd + ': ' + fmt(mod); up.hidden = false; }
      }).catch(function () {}).then(done);
    } else done();

    // Related
    var first = $('.fc-chips a, .fc-labels a', art), box = $('#fc-related'), grid = $('#fc-rel-grid'), st = $('#fc-rel-state');
    if (!box || !grid || !st) return;
    var lbl = '';
    if (first) { var m = (first.getAttribute('href') || '').match(/\/search\/label\/([^?#\/]+)/); if (m) { try { lbl = decodeURIComponent(m[1]); } catch (e) { lbl = m[1]; } } }
    var path = lbl ? '/feeds/posts/default/-/' + encodeURIComponent(lbl) : '/feeds/posts/default';
    var run = function () {
      feed(path, 8).then(function (j) {
        var cur = pathKey(url), list = ((j.feed && j.feed.entry) || []).filter(function (e) { return pathKey(norm(e).url) !== cur; }).slice(0, 3);
        fill(grid, st, list, T.noRel);
      }).catch(function () { st.textContent = T.err; });
    };
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { io.disconnect(); run(); } }, { rootMargin: '400px' }); io.observe(box);
    } else run();
  }

  /* ---------- Structured data (single source, no duplication) ---------- */
  function ld(o) { var s = d.createElement('script'); s.type = 'application/ld+json'; s.text = JSON.stringify(o); d.head.appendChild(s); }
  function meta(n, a) { var m = $('meta[' + (a || 'property') + '="' + n + '"]'); return m ? m.getAttribute('content') : ''; }
  function crumbs() {
    var li = $$('.fc-bc li'); if (!li.length) return null;
    return { '@context': 'https://schema.org', '@type': 'BreadcrumbList', itemListElement: li.map(function (x, i) {
      var a = $('a', x), o = { '@type': 'ListItem', position: i + 1, name: x.textContent.trim() };
      if (a && i < li.length - 1) o.item = a.href; return o; }) };
  }
  function orgObj() { return { '@type': 'Organization', name: 'Farcodo', url: location.origin + '/' }; }
  function articleLD(art, title, url, pub, mod) {
    var o = { '@context': 'https://schema.org', '@type': 'BlogPosting', headline: title.slice(0, 110), mainEntityOfPage: { '@type': 'WebPage', '@id': url },
      url: url, inLanguage: 'ar', publisher: orgObj() };
    var img = meta('og:image'); if (img) o.image = [img];
    var ds = meta('description', 'name') || meta('og:description'); if (ds) o.description = ds;
    if (pub) o.datePublished = pub; if (mod) o.dateModified = mod;
    var an = $('.au-name', art); if (an && an.textContent.trim()) o.author = { '@type': 'Person', name: an.textContent.trim() };
    ld(o); var c = crumbs(); if (c) ld(c);
  }
  function otherLD() {
    if ($('.fc-article')) return;
    var url = (($('link[rel=canonical]') || {}).href) || location.href.split('#')[0];
    if ($('.fc-hero')) {
      ld({ '@context': 'https://schema.org', '@type': 'WebSite', name: 'Farcodo', url: location.origin + '/', inLanguage: 'ar',
        potentialAction: { '@type': 'SearchAction', target: location.origin + '/search?q={search_term_string}', 'query-input': 'required name=search_term_string' } });
      ld(Object.assign({ '@context': 'https://schema.org' }, orgObj()));
      return;
    }
    if ($('.fc-pagebox')) { ld({ '@context': 'https://schema.org', '@type': 'WebPage', name: ($('.fc-title') || {}).textContent || d.title, url: url, inLanguage: 'ar' }); var c = crumbs(); if (c) ld(c); return; }
    if ($('[data-kind=label]')) { ld({ '@context': 'https://schema.org', '@type': 'CollectionPage', name: ($('.fc-listhead h1') || {}).textContent || d.title, url: url, inLanguage: 'ar' }); var c2 = crumbs(); if (c2) ld(c2); }
  }

  function init() {
    initTheme(); initDrawer(); cats(); post(); otherLD();
    var y = $('#fc-year'); if (y) y.textContent = new Date().getFullYear();
  }
  if (d.readyState === 'loading') d.addEventListener('DOMContentLoaded', init); else init();
})();
