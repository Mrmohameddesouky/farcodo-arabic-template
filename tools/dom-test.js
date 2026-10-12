const {JSDOM}=require('jsdom');const fs=require('fs');
const js=fs.readFileSync(process.env.FCJS,'utf8');
const g=(id,title,txt)=>`<div class="widget HTML" id="${id}"><h3 class="title">${title}</h3><div class="widget-content">${txt}</div></div>`;
const html=`<!DOCTYPE html><html><head></head><body>
<header><a class="fc-brand" href="/"><img src="x" width="24" height="24"><span aria-hidden="true">arcodo</span></a><nav class="fc-nav"><ul><li><a href="/a">أ</a></li></ul></nav>
<div id="header-social"><ul class="fc-social"><li><a href="https://x.com/farcodo">إكس</a></li><li><a href="javascript:alert(1)">سيئ</a></li><li><a href="https://youtube.com/@f">يوتيوب</a></li></ul></div>
<button id="fc-menu"></button><div id="fc-drawer" hidden><nav class="fc-drawer-nav"></nav></div></header>
<div id="brand-settings">${g('H3','الشعار','# c\nlogo=https://e.com/l.png\nname=موقعي\nalt=')}</div>
<main><div id="hero-banner">${g('H2','اللافتة','heading=عنوان<br>description=وصف<br>button1=ابدأ | /search/label/x<br>button2=سيئ | javascript:1<br>posts=hide<br>image=https://e.com/i.jpg')}</div>
<section class="fc-hero"></section>
<div id="home-sections">${g('H4','الذكاء الاصطناعي','label=الذكاء الاصطناعي\nsubtitle=وصف\ncount=3\nlayout=grid')}
${g('H5','فارغ','label=none-here\ncount=4')}${g('H6','مخفي','label=a\nhidden=yes')}${g('H7','فشل','label=fail\nlayout=compact')}${g('H8','أحدث','count=2\nlayout=list\nmore=none')}</div></main>
<footer><ul class="fc-social"></ul></footer><span id="fc-year"></span>
<article class="fc-article" data-id="1"><div class="fc-chips"><a href="/search/label/x">ت</a></div><h1 class="fc-title">T</h1><div class="post-body"><table><tr><td>1</td></tr></table><pre>code</pre></div></article>
<div id="fc-toast"></div></body></html>`;
const dom=new JSDOM(html,{runScripts:'outside-only',url:'https://farcodo.com/',pretendToBeVisual:true});
const w=dom.window;const calls=[];
w.fetch=(u)=>{calls.push(u);if(/fail/.test(u))return Promise.reject(new Error('x'));
 if(/none-here/.test(u))return Promise.resolve({ok:true,json:()=>({feed:{entry:[]}})});
 if(/\/feeds\/posts\/default\/1/.test(u))return Promise.resolve({ok:true,json:()=>({entry:{published:{$t:'2026-01-01T00:00:00Z'},updated:{$t:'2026-02-01T00:00:00Z'}}})});
 const e=n=>({title:{$t:'مقال '+n},link:[{rel:'alternate',href:'https://farcodo.com/p'+n+'.html'}],published:{$t:'2026-03-0'+n+'T00:00:00Z'},summary:{$t:'ملخص'},media$thumbnail:{url:'https://blogger.googleusercontent.com/img/a/s72-c/x.jpg'}});
 return Promise.resolve({ok:true,json:()=>({feed:{entry:[e(1),e(2),e(3),e(4)]}})})};
w.eval(js);
setTimeout(()=>{const q=s=>w.document.querySelector(s),qa=s=>[...w.document.querySelectorAll(s)];
const r=[];const ck=(n,c)=>{r.push((c?'PASS ':'FAIL ')+n)};
ck('brand custom',q('.fc-brand').classList.contains('is-custom')&&q('.fc-brand span').textContent==='موقعي'&&q('.fc-brand img').src==='https://e.com/l.png');
ck('banner built',!!q('.fc-banner')&&q('.fc-banner-t').textContent==='عنوان');
ck('banner only safe button',qa('.fc-banner-btns a').length===1);
ck('banner image',!!q('.fc-banner-img img')&&q('.fc-banner.has-img'));
ck('posts hero hidden',q('.fc-hero').hidden===true);
const secs=qa('#home-sections .fc-sec');
ck('sections: AI, failed, latest (empty removed, hidden skipped) = 3',secs.length===3);
ck('first section id',secs[0].id==='fc-sections');
ck('AI grid data-n 3 with 3 cards',secs[0].querySelectorAll('.fc-card').length===3&&secs[0].querySelector('.fc-grid').dataset.n==='3');
ck('more link encoded',secs[0].querySelector('.fc-more').getAttribute('href')==='/search/label/'+encodeURIComponent('الذكاء الاصطناعي'));
ck('failed shows error+retry',secs[1].querySelector('.fc-state').textContent.includes('تعذّر')&&!!secs[1].querySelector('.fc-state button'));
ck('list layout 2 cards, no more link',secs[2].querySelectorAll('.fc-card').length===2&&!secs[2].querySelector('.fc-more'));
ck('latest uses /feeds/posts/default',calls.some(u=>/^\/feeds\/posts\/default\?/.test(u)));
ck('social: unsafe removed, icons added',qa('#header-social .fc-social a').length===2&&qa('#header-social svg').length===2);
ck('social drawer clone',qa('#fc-drawer .fc-social a').length===2);
ck('empty footer social hidden',qa('footer .fc-social')[0].hidden===true);
ck('table wrapped',!!q('.fc-tw table'));ck('pre copy btn',!!q('.fc-pre .fc-copy'));
const lds=qa('script[type="application/ld+json"]').map(s=>JSON.parse(s.text));
ck('no JSON-LD duplicates on post',lds.filter(l=>l['@type']==='BlogPosting').length===1);
ck('article LD has keywords+dates',lds[0].keywords==='ت'&&!!lds[0].datePublished);
ck('year',q('#fc-year').textContent==='2026'||q('#fc-year').textContent.length===4);
console.log(r.join('\n'));process.exit(r.some(x=>x.startsWith('FAIL'))?1:0)},400);
