/*!
 * Sumi theme runtime. Vanilla JavaScript, no dependencies.
 * Heavy runtimes (Mermaid, KaTeX) are loaded only on pages that use them.
 */
(function () {
  'use strict';

  var S = window.sumi || {};
  var T = S.t || {};
  var doc = document;
  var root = doc.documentElement;
  var $ = function (sel, el) { return (el || doc).querySelector(sel); };
  var $$ = function (sel, el) { return Array.prototype.slice.call((el || doc).querySelectorAll(sel)); };
  var isMac = /Mac|iPhone|iPad/.test(navigator.platform || navigator.userAgent);
  var store = {
    get: function (k) { try { return localStorage.getItem('sumi.' + k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem('sumi.' + k, v); } catch (e) {} }
  };
  function t(key, vars) {
    var s = T[key] || key;
    if (vars) Object.keys(vars).forEach(function (k) { s = s.replace('{' + k + '}', vars[k]); });
    return s;
  }
  function url(path) {
    if (/^(https?:)?\/\//.test(path) || path.charAt(0) === '/') return path;
    var base = S.base || '.';
    return (base === '.' ? '' : base + '/') + path;
  }
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function svg(name) {
    var paths = {
      file: '<path d="M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z"/><path d="M14 2v5a1 1 0 0 0 1 1h5"/>',
      hash: '<line x1="4" x2="20" y1="9" y2="9"/><line x1="4" x2="20" y1="15" y2="15"/><line x1="10" x2="8" y1="3" y2="21"/><line x1="16" x2="14" y1="3" y2="21"/>',
      cmd: '<path d="m9 18 6-6-6-6"/>',
      copy: '<rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>',
      check: '<path d="M20 6 9 17l-5-5"/>',
      link: '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>'
    };
    return '<svg class="sumi-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + (paths[name] || paths.cmd) + '</svg>';
  }
  var toastTimer;
  function toast(msg) {
    var el = $('.sumi-toast');
    if (!el) return;
    el.textContent = msg;
    el.classList.add('is-on');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { el.classList.remove('is-on'); }, 1600);
  }
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text);
    return new Promise(function (resolve, reject) {
      var ta = doc.createElement('textarea');
      ta.value = text; ta.setAttribute('readonly', ''); ta.style.position = 'fixed'; ta.style.opacity = '0';
      doc.body.appendChild(ta); ta.select();
      try { doc.execCommand('copy') ? resolve() : reject(); } catch (e) { reject(e); }
      doc.body.removeChild(ta);
    });
  }
  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var s = doc.createElement('script');
      s.src = src; s.async = true; s.onload = resolve; s.onerror = reject;
      doc.head.appendChild(s);
    });
  }
  function typing(e) {
    var el = e.target;
    return el && (el.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName)) || e.isComposing;
  }

  /* ── Theme ─────────────────────────────────────────────────────────── */
  var listeners = [];
  function setTheme(mode, persist) {
    root.dataset.theme = mode;
    if (persist) store.set('palette', mode);
    listeners.forEach(function (fn) { fn(mode); });
  }
  function toggleTheme() { setTheme(root.dataset.theme === 'dark' ? 'light' : 'dark', true); }
  $$('[data-sumi-theme]').forEach(function (b) { b.addEventListener('click', toggleTheme); });
  if (window.matchMedia) {
    matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function (e) {
      if (!store.get('palette') && (root.dataset.palette === 'auto' || !root.dataset.palette)) setTheme(e.matches ? 'dark' : 'light');
    });
  }

  /* ── Keyboard hints ────────────────────────────────────────────────── */
  $$('[data-mod]').forEach(function (k) { k.textContent = isMac ? '⌘ K' : 'Ctrl K'; });

  /* ── Announcement ──────────────────────────────────────────────────── */
  var ann = $('.sumi-announce');
  if (ann) {
    var key = 'announce.' + (ann.dataset.key || '');
    if (store.get(key)) ann.hidden = true;
    $('.sumi-announce-close', ann).addEventListener('click', function () { ann.hidden = true; store.set(key, '1'); });
  }

  /* ── Menus ─────────────────────────────────────────────────────────── */
  function closeMenus(except) {
    $$('.sumi-menu.is-open').forEach(function (m) {
      if (m !== except) { m.classList.remove('is-open'); $('button', m).setAttribute('aria-expanded', 'false'); }
    });
  }
  doc.addEventListener('click', function (e) {
    var btn = e.target.closest('.sumi-menu > button');
    if (btn) {
      var menu = btn.parentElement;
      var open = !menu.classList.contains('is-open');
      closeMenus(menu);
      menu.classList.toggle('is-open', open);
      btn.setAttribute('aria-expanded', String(open));
      return;
    }
    if (!e.target.closest('.sumi-menu-list')) closeMenus();
  });

  /* ── Mobile sidebar ────────────────────────────────────────────────── */
  var side = $('#sumi-sidebar');
  var menuBtn = $('.sumi-menu-btn');
  var scrim;
  function setDrawer(open) {
    if (!side) return;
    side.classList.toggle('is-open', open);
    doc.body.classList.toggle('sumi-locked', open);
    if (menuBtn) menuBtn.setAttribute('aria-expanded', String(open));
    if (open) {
      scrim = doc.createElement('div');
      scrim.className = 'sumi-scrim';
      scrim.addEventListener('click', function () { setDrawer(false); });
      doc.body.appendChild(scrim);
    } else if (scrim) { scrim.remove(); scrim = null; }
  }
  if (menuBtn) menuBtn.addEventListener('click', function () { setDrawer(!side.classList.contains('is-open')); });
  if (side) {
    var current = $('.is-current', side);
    if (current) {
      var box = $('.sumi-sidebar-inner', side);
      var r = current.getBoundingClientRect(), b = box.getBoundingClientRect();
      if (r.bottom > b.bottom - 40) box.scrollTop += r.top - b.top - b.height / 3;
    }
  }

  /* ── Code blocks: copy button and language label ───────────────────── */
  $$('.sumi-prose pre').forEach(function (pre) {
    if (pre.classList.contains('mermaid') || pre.closest('.linenos')) return;
    var host = pre.closest('.highlight, .codehilite') || pre;
    if (host.querySelector(':scope > .sumi-copy')) return;
    var code = $('code', pre) || pre;
    var btn = doc.createElement('button');
    btn.type = 'button'; btn.className = 'sumi-copy'; btn.setAttribute('aria-label', t('copy_code')); btn.title = t('copy_code');
    btn.innerHTML = svg('copy');
    btn.addEventListener('click', function () {
      var text = code.innerText.replace(/\n$/, '');
      var lines = text.split('\n');
      // Skip shell prompts and console output marked by Pygments.
      var prompts = $$('.gp', code).length;
      if (prompts) {
        text = $$('.gp', code).map(function (p) {
          var out = '', n = p.nextSibling;
          while (n && !(n.nodeType === 1 && (n.classList.contains('gp') || n.classList.contains('go')))) {
            out += n.textContent; n = n.nextSibling;
          }
          return out.replace(/\n$/, '');
        }).join('\n');
      } else { text = lines.join('\n'); }
      copyText(text).then(function () {
        btn.classList.add('is-done'); btn.innerHTML = svg('check');
        setTimeout(function () { btn.classList.remove('is-done'); btn.innerHTML = svg('copy'); }, 1400);
      });
    });
    host.appendChild(btn);
    var lang = (code.className.match(/language-([\w+#-]+)/) || host.className.match(/language-([\w+#-]+)/) || [])[1];
    if (lang && host !== pre && !host.closest('.sumi-code') && !host.closest('.sumi-tab')) {
      var label = doc.createElement('span');
      label.className = 'sumi-code-lang'; label.textContent = lang;
      host.appendChild(label);
    }
  });

  /* ── Tabs ──────────────────────────────────────────────────────────── */
  var tabSets = [];
  function selectTab(set, label, focus) {
    var tabs = $$(':scope > .sumi-tab', set);
    var idx = tabs.findIndex(function (tb) { return tb.dataset.label === label; });
    if (idx < 0) return false;
    tabs.forEach(function (tb, i) { tb.classList.toggle('is-active', i === idx); });
    $$('.sumi-tablist button', set).forEach(function (b, i) {
      b.setAttribute('aria-selected', String(i === idx)); b.tabIndex = i === idx ? 0 : -1;
      if (i === idx && focus) b.focus();
    });
    return true;
  }
  $$('.sumi-tabs').forEach(function (set, n) {
    var tabs = $$(':scope > .sumi-tab', set);
    var list = doc.createElement('div');
    list.className = 'sumi-tablist'; list.setAttribute('role', 'tablist');
    tabs.forEach(function (tb, i) {
      var b = doc.createElement('button');
      b.type = 'button'; b.setAttribute('role', 'tab'); b.textContent = tb.dataset.label;
      b.id = 'sumi-tabbtn-' + n + '-' + i; tb.setAttribute('role', 'tabpanel'); tb.setAttribute('aria-labelledby', b.id);
      b.addEventListener('click', function () {
        var y = b.getBoundingClientRect().top;
        tabSets.forEach(function (s) { selectTab(s, tb.dataset.label); });
        store.set('tab', tb.dataset.label);
        window.scrollBy(0, b.getBoundingClientRect().top - y);
      });
      b.addEventListener('keydown', function (e) {
        var d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (!d) return;
        var next = tabs[(i + d + tabs.length) % tabs.length];
        selectTab(set, next.dataset.label, true);
      });
      list.appendChild(b);
    });
    set.insertBefore(list, set.firstChild);
    set.dataset.ready = '';
    tabSets.push(set);
    if (!selectTab(set, store.get('tab'))) selectTab(set, tabs[0] && tabs[0].dataset.label);
  });

  /* ── Table of contents scroll spy ──────────────────────────────────── */
  var tocLinks = $$('.sumi-toc a');
  var headings = [];
  var seen = {};
  tocLinks.forEach(function (a) {
    var id = decodeURIComponent((a.getAttribute('href') || '').slice(1));
    var h = id && doc.getElementById(id);
    if (h && !seen[id]) { headings.push(h); seen[id] = true; }
  });
  function spy() {
    var y = (parseInt(getComputedStyle(root).getPropertyValue('--sumi-header-h'), 10) || 60) + 24;
    var active = null;
    for (var i = 0; i < headings.length; i++) {
      if (headings[i].getBoundingClientRect().top - y <= 1) active = headings[i]; else break;
    }
    if (!active && headings.length) active = null;
    if ((window.innerHeight + window.scrollY) >= doc.body.scrollHeight - 4 && headings.length) active = headings[headings.length - 1];
    tocLinks.forEach(function (a) {
      var on = !!active && a.getAttribute('href') === '#' + encodeURIComponent(active.id).replace(/%20/g, '%20');
      if (!on && active) on = decodeURIComponent(a.getAttribute('href').slice(1)) === active.id;
      a.classList.toggle('is-active', on);
    });
  }
  if (headings.length) {
    var ticking = false;
    window.addEventListener('scroll', function () {
      if (!ticking) { requestAnimationFrame(function () { spy(); ticking = false; }); ticking = true; }
    }, { passive: true });
    spy();
  }
  $$('.sumi-toc-inline .sumi-toc a').forEach(function (a) {
    a.addEventListener('click', function () { a.closest('details').open = false; });
  });
  var topLink = $('.sumi-rail-top');
  if (topLink) topLink.addEventListener('click', function (e) { e.preventDefault(); window.scrollTo({ top: 0, behavior: 'smooth' }); history.replaceState(null, '', location.pathname); });

  /* ── Page actions ──────────────────────────────────────────────────── */
  var mdCache = null;
  function getMarkdown() {
    if (!S.markdown) return Promise.reject();
    if (mdCache) return Promise.resolve(mdCache);
    return fetch(S.markdown).then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); })
      .then(function (txt) { mdCache = txt; return txt; });
  }
  function copyMarkdown(btn) {
    // Safari needs the clipboard write to start inside the click: hand it a promise.
    var done = function () {
      toast(t('copied'));
      if (btn) {
        btn.classList.add('is-done');
        setTimeout(function () { btn.classList.remove('is-done'); }, 1400);
      }
    };
    if (window.ClipboardItem && navigator.clipboard && navigator.clipboard.write && window.isSecureContext) {
      var item = new ClipboardItem({ 'text/plain': getMarkdown().then(function (s) { return new Blob([s], { type: 'text/plain' }); }) });
      return navigator.clipboard.write([item]).then(done, function () { getMarkdown().then(copyText).then(done); });
    }
    return getMarkdown().then(copyText).then(done);
  }
  $$('[data-sumi-copy-page]').forEach(function (b) { b.addEventListener('click', function () { copyMarkdown(b); }); });
  $$('[data-sumi-print]').forEach(function (b) { b.addEventListener('click', function () { closeMenus(); window.print(); }); });
  $$('[data-assistant]').forEach(function (a) {
    var md = S.markdown ? new URL(S.markdown, location.href).href : location.href;
    var prompt = 'Read ' + md + ' so I can ask questions about it.';
    a.href = a.dataset.assistant === 'claude'
      ? 'https://claude.ai/new?q=' + encodeURIComponent(prompt)
      : 'https://chatgpt.com/?hints=search&q=' + encodeURIComponent(prompt);
    a.target = '_blank';
  });
  window.addEventListener('beforeprint', function () {
    $$('.sumi-prose details').forEach(function (d) { if (!d.open) { d.dataset.wasClosed = ''; d.open = true; } });
  });
  window.addEventListener('afterprint', function () {
    $$('.sumi-prose details[data-was-closed]').forEach(function (d) { d.open = false; delete d.dataset.wasClosed; });
  });

  /* ── Image zoom ────────────────────────────────────────────────────── */
  var zoom = $('.sumi-zoom');
  if (zoom) {
    $$('.sumi-prose img').forEach(function (img) {
      if (img.closest('a') || img.closest('.sumi-cards') || img.classList.contains('no-zoom')) return;
      img.classList.add('sumi-zoomable');
      img.addEventListener('click', function () {
        var z = $('img', zoom);
        z.src = img.currentSrc || img.src; z.alt = img.alt;
        zoom.showModal();
      });
    });
    zoom.addEventListener('click', function () { zoom.close(); });
  }

  /* ── Mermaid (lazy) ────────────────────────────────────────────────── */
  var features = S.features || [];
  if (features.indexOf('mermaid') >= 0) {
    var diagrams = $$('pre.mermaid');
    diagrams.forEach(function (d) { d.dataset.source = d.textContent; });
    var render = function () {
      var dark = root.dataset.theme === 'dark';
      var css = getComputedStyle(root);
      window.mermaid.initialize({
        startOnLoad: false, securityLevel: 'strict', theme: 'base',
        fontFamily: css.getPropertyValue('--sumi-font'),
        themeVariables: {
          darkMode: dark, fontSize: '14px',
          background: css.getPropertyValue('--sumi-bg-elev').trim(),
          primaryColor: css.getPropertyValue('--sumi-bg-soft').trim(),
          primaryBorderColor: css.getPropertyValue('--sumi-line-2').trim(),
          primaryTextColor: css.getPropertyValue('--sumi-fg').trim(),
          lineColor: css.getPropertyValue('--sumi-fg-3').trim(),
          secondaryColor: css.getPropertyValue('--sumi-bg-sunken').trim(),
          tertiaryColor: css.getPropertyValue('--sumi-bg-elev').trim(),
          noteBkgColor: dark ? '#3a3220' : '#fbf3dc', noteTextColor: css.getPropertyValue('--sumi-fg').trim()
        }
      });
      diagrams.forEach(function (d) { d.removeAttribute('data-processed'); d.innerHTML = esc(d.dataset.source); });
      return window.mermaid.run({ nodes: diagrams });
    };
    loadScript(url('assets/sumi/vendor/mermaid/mermaid.min.js')).then(render).then(function () {
      listeners.push(function () { render(); });
    }).catch(function () {});
  }

  /* ── KaTeX (lazy) ──────────────────────────────────────────────────── */
  if (features.indexOf('math') >= 0) {
    loadScript(url('assets/sumi/vendor/katex/katex.min.js')).then(function () {
      $$('.sumi-math, .arithmatex').forEach(function (el) {
        var tex = el.textContent.trim();
        var display = el.classList.contains('math-display') || el.tagName === 'DIV';
        tex = tex.replace(/^\\\(|\\\)$/g, '').replace(/^\\\[|\\\]$/g, '').replace(/^\$\$?|\$\$?$/g, '');
        try {
          window.katex.render(tex, el, { displayMode: display, throwOnError: false, output: 'htmlAndMathml' });
          el.dataset.rendered = '';
        } catch (e) {}
      });
    }).catch(function () {});
  }

  /* ── Versions (mike) ───────────────────────────────────────────────── */
  if (S.versions === 'mike') {
    var vmenu = $('.sumi-version-menu');
    var siteRoot = new URL(url('../'), location.href);
    fetch(new URL('versions.json', siteRoot)).then(function (r) { return r.json(); }).then(function (versions) {
      var here = new URL(url('.'), location.href).pathname.replace(siteRoot.pathname, '').split('/')[0];
      var cur = versions.find(function (v) { return v.version === here || (v.aliases || []).indexOf(here) >= 0; });
      if (!cur || !vmenu) return;
      $('.sumi-version-current', vmenu).textContent = cur.title || cur.version;
      var list = $('.sumi-menu-list', vmenu);
      var rel = location.href.slice(new URL(url('.'), location.href).href.length);
      versions.forEach(function (v) {
        var li = doc.createElement('li');
        li.setAttribute('role', 'none');
        li.innerHTML = '<a role="menuitem" href="' + esc(new URL(v.version + '/' + rel, siteRoot).href) + '"' +
          (v === cur ? ' aria-current="true"' : '') + '>' + esc(v.title || v.version) + '</a>';
        list.appendChild(li);
      });
      vmenu.hidden = false;
      var latest = versions[0];
      if (cur !== latest && (latest.aliases || []).indexOf(here) < 0) {
        var banner = $('.sumi-version-banner');
        banner.innerHTML = esc(t('old_version')) + ' <a href="' + esc(new URL((latest.aliases && latest.aliases[0] || latest.version) + '/', siteRoot).href) + '">' + esc(t('go_latest')) + '</a>';
        banner.hidden = false;
      }
      S.versionList = versions;
    }).catch(function () {});
  }

  /* ── Command palette ───────────────────────────────────────────────── */
  var pal = $('.sumi-palette');
  var input = pal && $('input', pal);
  var results = pal && $('.sumi-palette-results', pal);
  var index = null, loading = null, items = [], sel = 0;
  var CJK = /[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uac00-\ud7af]/;

  function loadIndex() {
    if (index || loading) return loading;
    if (!S.search) { index = []; return Promise.resolve(index); }
    loading = fetch(S.search).then(function (r) { return r.json(); }).then(function (data) {
      var titles = {};
      (data.docs || []).forEach(function (d) { if (d.location.indexOf('#') < 0) titles[d.location] = d.title; });
      index = (data.docs || []).map(function (d) {
        var hash = d.location.indexOf('#');
        var pageLoc = hash < 0 ? d.location : d.location.slice(0, hash);
        var text = (d.text || '').replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
        return {
          title: d.title || '', page: titles[pageLoc] || '', loc: d.location, text: text,
          lt: (d.title || '').toLowerCase(), lx: text.toLowerCase(), section: hash >= 0
        };
      });
      return index;
    }).catch(function () { index = []; return index; });
    return loading;
  }
  function terms(q) {
    var out = [];
    q.toLowerCase().split(/\s+/).forEach(function (w) {
      if (!w) return;
      if (CJK.test(w)) {
        // Split mixed runs: CJK sequences are matched as substrings.
        (w.match(/[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uac00-\ud7af]+|[^\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uac00-\ud7af]+/g) || []).forEach(function (p) { out.push(p); });
      } else out.push(w);
    });
    return out;
  }
  function highlight(text, ts) {
    var h = esc(text);
    ts.forEach(function (w) {
      if (!w) return;
      var re = new RegExp('(' + w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&').replace(/&/g, '&amp;').replace(/</g, '&lt;') + ')', 'ig');
      h = h.replace(re, '<mark>$1</mark>');
    });
    return h;
  }
  function snippet(text, ts) {
    var lx = text.toLowerCase(), pos = -1;
    for (var i = 0; i < ts.length && pos < 0; i++) pos = lx.indexOf(ts[i]);
    if (pos < 0) return text.slice(0, 140);
    var start = Math.max(0, pos - 50);
    return (start ? '…' : '') + text.slice(start, start + 160) + (start + 160 < text.length ? '…' : '');
  }
  function searchDocs(q) {
    var ts = terms(q);
    if (!ts.length) return [];
    var scored = [];
    (index || []).forEach(function (d) {
      var score = 0;
      for (var i = 0; i < ts.length; i++) {
        var w = ts[i], inTitle = d.lt.indexOf(w), inText = d.lx.indexOf(w);
        if (inTitle < 0 && inText < 0 && d.page.toLowerCase().indexOf(w) < 0) return;
        if (inTitle === 0) score += 14; else if (inTitle > 0) score += 9;
        if (inText >= 0) score += 2 + Math.min(3, d.lx.split(w).length - 2) * 0.5;
      }
      if (d.lt === q.toLowerCase()) score += 10;
      if (!d.section) score += 1.5;
      scored.push({ d: d, s: score });
    });
    scored.sort(function (a, b) { return b.s - a.s; });
    return scored.slice(0, 40).map(function (x) {
      var d = x.d;
      return {
        kind: 'doc', icon: d.section ? 'hash' : 'file', href: url(d.loc),
        title: highlight(d.title || d.page, ts),
        path: d.section ? esc(d.page) : '',
        snippet: d.text ? highlight(snippet(d.text, ts), ts) : ''
      };
    });
  }
  function navMatches(q) {
    var ts = terms(q);
    return (S.nav || []).filter(function (n) {
      var hay = (n.t + ' ' + n.s).toLowerCase();
      return ts.every(function (w) { return hay.indexOf(w) >= 0; });
    }).slice(0, 30).map(function (n) {
      return { kind: 'doc', icon: n.x ? 'link' : 'file', href: n.x ? n.u : url(n.u), title: highlight(n.t, ts), path: esc(n.s) };
    });
  }
  function commands() {
    var list = [
      { title: t('cmd_toggle_theme'), run: toggleTheme, keys: 'theme dark light 主题 深色' }
    ];
    if (S.markdown) {
      list.push({ title: t('cmd_copy_markdown'), run: function () { copyMarkdown(); }, keys: 'copy markdown md 复制' });
      list.push({ title: t('cmd_view_markdown'), run: function () { window.open(S.markdown, '_blank'); }, keys: 'markdown source 源码' });
    }
    if (S.edit) list.push({ title: t('cmd_edit'), run: function () { location.href = S.edit; }, keys: 'edit github 编辑' });
    list.push({ title: t('cmd_print'), run: function () { window.print(); }, keys: 'print pdf 打印' });
    list.push({ title: t('cmd_top'), run: function () { window.scrollTo({ top: 0 }); }, keys: 'top 顶部' });
    list.push({ title: t('cmd_home'), run: function () { location.href = url('./'); }, keys: 'home 首页' });
    (S.alternate || []).forEach(function (a) {
      list.push({ title: t('cmd_language', { name: a.name }), run: function () { location.href = url(a.link.replace(/^\//, '')); }, keys: 'language lang 语言 ' + a.lang });
    });
    (S.versionList || []).forEach(function (v) {
      list.push({ title: t('cmd_version', { name: v.title || v.version }), run: function () { location.href = new URL('../' + v.version + '/', new URL(url('./'), location.href)).href; }, keys: 'version 版本' });
    });
    if (doc.querySelector('link[href$="llms.txt"]')) list.push({ title: t('cmd_llms'), run: function () { location.href = url('llms.txt'); }, keys: 'llms ai agent' });
    return list;
  }
  function render(q) {
    var cmdOnly = q.charAt(0) === '>';
    var query = cmdOnly ? q.slice(1).trim() : q.trim();
    var docs = [];
    if (!cmdOnly && query) docs = index && index.length ? searchDocs(query) : navMatches(query);
    if (!cmdOnly && !query) docs = (S.nav || []).slice(0, 8).map(function (n) {
      return { kind: 'doc', icon: n.x ? 'link' : 'file', href: n.x ? n.u : url(n.u), title: esc(n.t), path: esc(n.s) };
    });
    var lq = query.toLowerCase();
    var cmds = commands().filter(function (c) {
      return !lq || (c.title + ' ' + c.keys).toLowerCase().indexOf(lq) >= 0;
    }).map(function (c) { return { kind: 'cmd', icon: 'cmd', title: highlight(c.title, lq ? [lq] : []), run: c.run }; });
    if (!cmdOnly && query && docs.length) cmds = cmds.slice(0, 3);
    items = docs.concat(cmds);
    var html = '';
    if (docs.length) html += '<div class="sumi-palette-group">' + esc(t('pages')) + '</div>';
    items.forEach(function (it, i) {
      if (i === docs.length && cmds.length) html += '<div class="sumi-palette-group">' + esc(t('commands')) + '</div>';
      html += '<div class="sumi-palette-item" role="option" id="sumi-opt-' + i + '" data-i="' + i + '">' + svg(it.icon) +
        '<span class="sumi-palette-text"><span class="sumi-palette-title">' + it.title + '</span>' +
        (it.path ? '<span class="sumi-palette-path">' + it.path + '</span>' : '') +
        (it.snippet ? '<span class="sumi-palette-snippet">' + it.snippet + '</span>' : '') + '</span></div>';
    });
    if (!items.length) html = '<div class="sumi-palette-empty">' + esc(t('search_no_results')) + ' “' + esc(query) + '”</div>';
    results.innerHTML = html;
    sel = 0; mark();
  }
  function mark() {
    $$('.sumi-palette-item', results).forEach(function (el, i) {
      el.setAttribute('aria-selected', String(i === sel));
      if (i === sel) { el.scrollIntoView({ block: 'nearest' }); input.setAttribute('aria-activedescendant', el.id); }
    });
  }
  function choose(i, newTab) {
    var it = items[i];
    if (!it) return;
    if (it.kind === 'cmd') { pal.close(); it.run(); return; }
    if (newTab) window.open(it.href, '_blank'); else { pal.close(); location.href = it.href; }
  }
  function openPalette(prefix) {
    if (!pal || pal.open) return;
    closeMenus();
    pal.showModal();
    input.value = prefix || '';
    render(input.value);
    input.focus();
    var p = loadIndex();
    if (p) p.then(function () { if (pal.open) render(input.value); });
  }
  if (pal) {
    $$('[data-sumi-palette]').forEach(function (b) { b.addEventListener('click', function () { openPalette(); }); });
    input.addEventListener('input', function () { render(input.value); });
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { e.preventDefault(); pal.close(); return; }
      if (e.key === 'ArrowDown') { e.preventDefault(); sel = Math.min(items.length - 1, sel + 1); mark(); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); sel = Math.max(0, sel - 1); mark(); }
      else if (e.key === 'Enter') { e.preventDefault(); choose(sel, e.metaKey || e.ctrlKey); }
    });
    results.addEventListener('click', function (e) {
      var el = e.target.closest('.sumi-palette-item');
      if (el) choose(+el.dataset.i, e.metaKey || e.ctrlKey);
    });
    results.addEventListener('mousemove', function (e) {
      var el = e.target.closest('.sumi-palette-item');
      if (el && +el.dataset.i !== sel) { sel = +el.dataset.i; mark(); }
    });
    pal.addEventListener('click', function (e) { if (e.target === pal) pal.close(); });
  }

  /* ── Help dialog ───────────────────────────────────────────────────── */
  var help = $('.sumi-help');
  function openHelp() { if (help && !help.open) help.showModal(); }
  $$('[data-sumi-help]').forEach(function (b) { b.addEventListener('click', openHelp); });
  if (help) {
    $('[data-close]', help).addEventListener('click', function () { help.close(); });
    help.addEventListener('click', function (e) { if (e.target === help) help.close(); });
  }

  /* ── Keyboard ──────────────────────────────────────────────────────── */
  doc.addEventListener('keydown', function (e) {
    if ((e.metaKey || e.ctrlKey) && !e.altKey && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      if (pal && pal.open) pal.close(); else openPalette();
      return;
    }
    if (e.key === 'Escape') { closeMenus(); setDrawer(false); return; }
    if (S.keyboard === false || typing(e) || e.metaKey || e.ctrlKey || e.altKey) return;
    if ($('dialog[open]')) return;
    switch (e.key) {
      case '/': e.preventDefault(); openPalette(); break;
      case '>': e.preventDefault(); openPalette('>'); break;
      case 't': toggleTheme(); break;
      case '[': if (S.prev) location.href = S.prev; break;
      case ']': if (S.next) location.href = S.next; break;
      case '?': openHelp(); break;
      case 'j': case 'k': {
        if (!headings.length) break;
        var y = (parseInt(getComputedStyle(root).getPropertyValue('--sumi-header-h'), 10) || 60) + 30;
        var target = null;
        if (e.key === 'j') target = headings.find(function (h) { return h.getBoundingClientRect().top > y + 2; });
        else for (var i = headings.length - 1; i >= 0; i--) if (headings[i].getBoundingClientRect().top < y - 2) { target = headings[i]; break; }
        if (target) { target.scrollIntoView({ behavior: 'smooth' }); history.replaceState(null, '', '#' + target.id); }
        break;
      }
    }
  });
})();
