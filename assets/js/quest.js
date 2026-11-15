/* Quest page (quest.html?q=<slug>). Data: content/work.json, content/fn.json, content/install-guide.json, content/settings.json. */
(function () {
  var menu = document.getElementById("menu"), nav = document.getElementById("navigation");
  if (menu && nav) {
    menu.addEventListener("click", function () {
      var open = !nav.classList.contains("open");
      nav.classList.toggle("open", open);
      menu.setAttribute("aria-expanded", String(open));
      menu.textContent = open ? "Close" : "Menu";
    });
    nav.querySelectorAll("a").forEach(function (a) { a.addEventListener("click", function () { nav.classList.remove("open"); menu.setAttribute("aria-expanded", "false"); menu.textContent = "Menu"; }); });
  }

  function esc(s) { return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }
  function safeUrl(u) {
    if (u == null) return ""; u = String(u).trim(); if (!u) return "";
    if (/^https?:\/\//i.test(u)) return u;
    if (/^[a-z][a-z0-9+.-]*:/i.test(u) || u.indexOf("//") === 0) return "";
    return u.replace(/^\//, "");
  }
  function val(v) { v = v == null ? "" : String(v).trim(); return !v || /^tbc$/i.test(v) ? '<mark class="tbc">TBC</mark>' : esc(v).replace(/\bTBC\b/g, '<mark class="tbc">TBC</mark>'); }
  function $(id) { return document.getElementById(id); }
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fb = window.SITE_FALLBACK || {};
  function load(path, key) {
    if (location.protocol === "file:") return Promise.resolve(fb[key] || null);
    return fetch(path).then(function (r) { return r.ok ? r.json() : fb[key] || null; }).catch(function () { return fb[key] || null; });
  }

  function questList(work, fn) {
    var list = [];
    if (fn && fn.slug && fn.page) {
      var p = fn.page;
      list.push({ slug: fn.slug, title: "Frieza’s Nightmare", type: p.facts && p.facts.mode, status: "fn", tagline: p.tagline, hype: p.hype, facts: p.facts,
        download_url: p.download_url, download_host: p.download_host, download_label: p.download_label, youtube_id: p.youtube_id, trailer_label: p.trailer_label,
        gallery: p.gallery, changelog: p.changelog, nexus_url: p.nexus_url, nexus_label: p.nexus_label, facts_source: p.facts_source, clip_mp4: "assets/fn2-teaser.mp4", clip_webm: "assets/fn2-teaser.webm", clip_poster: "assets/fn2-teaser-poster.jpg",
        card: "assets/fn2-teaser-poster.jpg", note: fn.note, requirements: "", credit: "" });
    }
    ((work && work.items) || []).forEach(function (w) {
      if (!w || w.hidden || !w.slug) return;
      var p = w.page || {};
      list.push({ slug: w.slug, title: w.title, type: w.type, year: w.year, status: "released", tagline: p.tagline, hype: p.hype || [w.summary], facts: p.facts || {},
        download_url: w.show_download !== false ? w.download_url : "", download_host: w.download_host, youtube_id: p.youtube_id, gallery: p.gallery, changelog: p.changelog,
        clip_mp4: w.clip_mp4, clip_webm: w.clip_webm, clip_poster: w.clip_poster, card: w.clip_poster || w.image, requirements: w.requirements, credit: w.credit,
        summary: w.summary, install_note: p.install_note, commission: w.commission, nexus_url: w.nexus_url, facts_source: p.facts_source });
    });
    return list;
  }

  function render(q, all, guide, settings) {
    document.title = q.title + " | Xeno Trunks · Xenoverse 2 custom quest";
    var md = document.querySelector('meta[name="description"]');
    if (md) md.setAttribute("content", q.title + ": " + (q.tagline || "") + " Custom Parallel Quest for Dragon Ball Xenoverse 2 by Xeno Trunks, with trailer, facts and a step-by-step install guide.");
    $("q-crumb").textContent = q.title;
    $("q-title").textContent = q.title;
    $("q-tagline").textContent = q.tagline || "";

    // Hero loop
    var hm = $("q-hero-media"), clip = safeUrl(q.clip_mp4), poster = safeUrl(q.clip_poster || q.card);
    if (clip) {
      hm.innerHTML = '<video muted loop playsinline preload="metadata"' + (reduce ? "" : " autoplay") + ' poster="' + esc(poster) + '">' +
        (q.clip_webm ? '<source src="' + esc(safeUrl(q.clip_webm)) + '" type="video/webm">' : "") + '<source src="' + esc(clip) + '" type="video/mp4"></video>' +
        '<img class="q-still" src="' + esc(poster) + '" alt="">';
      var v = hm.querySelector("video");
      if (!reduce) { v.muted = true; var pr = v.play(); if (pr && pr.catch) pr.catch(function () {}); }
    } else if (poster) hm.innerHTML = '<img src="' + esc(poster) + '" alt="" style="display:block">';

    // Badges
    var b = [];
    if (q.status === "fn") { b.push('<span class="q-badge free">1.7 free now</span>', '<span class="q-badge dev">2.0 in development</span>'); }
    else {
      b.push('<span class="q-badge">Released</span>');
      if (safeUrl(q.download_url)) b.push('<span class="q-badge free">Free download</span>');
      if (q.commission) b.push('<span class="q-badge">Commission</span>');
    }
    if (q.type) b.push('<span class="q-badge">' + esc(q.type) + "</span>");
    $("q-badges").innerHTML = b.join("");

    // Actions + download box
    var dl = safeUrl(q.download_url);
    var dlLabel = q.download_label || (dl ? "Free download" : "");
    var host = q.download_host ? String(q.download_host) : "";
    var acts = [];
    if (dl) acts.push('<a class="btn" href="' + esc(dl) + '" target="_blank" rel="noopener noreferrer">' + esc(dlLabel) + " ↗</a>");
    if (q.youtube_id) acts.push('<a class="btn outline" href="#trailer">▶ Watch trailer</a>');
    acts.push('<a class="btn outline" href="#install">Install guide</a>');
    $("q-actions").innerHTML = acts.join("");
    var navdl = $("nav-dl");
    if (navdl) { if (dl) { navdl.href = dl; navdl.target = "_blank"; navdl.rel = "noopener noreferrer"; navdl.textContent = q.status === "fn" ? "Play 1.7 free" : "Download"; } else navdl.remove(); }
    $("download").innerHTML = dl
      ? '<a class="btn" href="' + esc(dl) + '" target="_blank" rel="noopener noreferrer">' + esc(dlLabel) + ' ↗</a><p class="host">Hosted on ' + esc(host.replace(/^VGM\b/, "Videogamemods (VGM)")) + "</p>"
      : '<span class="btn outline" aria-disabled="true">Download coming later</span>';
    var nx = safeUrl(q.nexus_url);
    if (nx) $("download").innerHTML += '<a class="btn outline" href="' + esc(nx) + '" target="_blank" rel="noopener noreferrer">' + esc(q.nexus_label || "Mirror: Nexus Mods") + ' ↗</a><p class="host">Nexus needs a free account to download. Some Nexus files come as a .zip: unzip it to get the .x2m.</p>';

    // Overview
    $("q-hype").innerHTML = (q.hype || []).map(function (p) { return "<p>" + esc(p) + "</p>"; }).join("");
    $("q-credit").textContent = q.credit || "";
    if (q.status === "fn") {
      var n = $("q-note"); n.hidden = false;
      n.textContent = q.note || "No release date yet. How 2.0 will be released is still being decided. Version 1.7 is free to play now.";
    }

    // Facts
    var f = q.facts || {};
    var rows = [
      ["Version", f.version], ["Last updated", f.updated], ["Released", f.released], ["Type", f.mode || q.type],
      ["Requires", f.game || q.requirements], ["Tested game version", f.tested_game], ["XV2 Patcher", f.patcher],
      ["Platform", "PC (Steam)"], ["File size", f.size], ["Download", host ? host.replace(/^VGM\b/, "Videogamemods (VGM)") : ""]
    ];
    var hasTbc = false;
    $("q-facts").innerHTML = rows.map(function (r) { var h = val(r[1]); if (h.indexOf("tbc") > -1) hasTbc = true; return "<dt>" + esc(r[0]) + "</dt><dd>" + h + "</dd>"; }).join("");
    $("q-tbc-note").hidden = !hasTbc;
    var srcs = (q.facts_source || []).filter(function (s) { return s && safeUrl(s.url); });
    var sn = $("q-src");
    if (sn && srcs.length) { sn.hidden = false; sn.innerHTML = "Info from listings, not yet confirmed: " + srcs.map(function (s) { return '<a href="' + esc(safeUrl(s.url)) + '" target="_blank" rel="noopener noreferrer">' + esc(s.label || "source") + "</a>"; }).join(" · "); }

    // Trailer: click-to-load (no YouTube request until the visitor asks)
    var tr = $("q-trailer");
    if (q.youtube_id && /^[\w-]{6,20}$/.test(q.youtube_id)) {
      if (q.trailer_label) $("q-trailer-title").textContent = q.trailer_label;
      tr.innerHTML = '<button type="button" aria-label="Play the ' + esc(q.title) + ' trailer"><img src="https://i.ytimg.com/vi/' + esc(q.youtube_id) + '/hqdefault.jpg" alt="" loading="lazy"><span class="play" aria-hidden="true">▶</span></button>';
      tr.querySelector("button").addEventListener("click", function () {
        tr.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + esc(q.youtube_id) + '?autoplay=1&rel=0" title="' + esc(q.title) + ' trailer" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>';
      });
    } else $("trailer").hidden = true;

    // Gallery
    var g = (q.gallery || []).map(safeUrl).filter(Boolean);
    if (g.length) $("q-gallery").innerHTML = g.map(function (src, i) { return '<a href="' + esc(src) + '" target="_blank" rel="noopener"><img src="' + esc(src) + '" alt="' + esc(q.title) + " trailer still " + (i + 1) + '" width="960" height="540" loading="lazy" decoding="async"></a>'; }).join("");
    else $("gallery").hidden = true;

    // Install guide
    if (guide) {
      $("g-title").textContent = guide.title || "How to install";
      $("g-intro").textContent = guide.intro || "";
      $("g-req").innerHTML = '<p class="kicker">Before you start</p><h3>Requirements</h3><ul>' + (guide.requirements || []).map(function (r) { return "<li>" + esc(r) + "</li>"; }).join("") +
        (f.game && !/^tbc$/i.test(String(f.game).trim()) ? "<li><b>This quest:</b> " + esc(f.game) + "</li>" : "") + "</ul>" +
        (guide.tools_url ? '<p style="margin:14px 0 0"><a class="btn outline" href="' + esc(safeUrl(guide.tools_url)) + '" target="_blank" rel="noopener noreferrer">Get Eternity Tools (VGM) ↗</a></p>' : "");
      if (q.install_note) $("g-quest-note").innerHTML = '<div class="q-note" style="margin:0 0 16px">' + esc(q.install_note) + "</div>";
      var patreon = /patreon/i.test(host);
      function steps(arr) {
        return (arr || []).map(function (s) {
          var img = safeUrl(patreon && s.image_patreon ? s.image_patreon : s.image);
          return "<li><div><h4>" + esc(s.title) + "</h4><p>" + esc(patreon && s.text_patreon ? s.text_patreon : s.text) + "</p></div>" + (img ? '<img src="' + esc(img) + '" alt="Screenshot: ' + esc(s.title) + '" loading="lazy" decoding="async">' : "") + "</li>";
        }).join("");
      }
      $("g-setup-steps").innerHTML = steps(guide.setup);
      $("g-install-steps").innerHTML = steps(guide.install);
      $("g-play-steps").innerHTML = steps(guide.play);
      $("g-uninstall-body").innerHTML = "<p>" + esc(guide.uninstall || "") + "</p>" + (guide.uninstall_image ? '<img src="' + esc(safeUrl(guide.uninstall_image)) + '" alt="Screenshot: uninstall in XV2INS" loading="lazy">' : "");
      function qa(arr) { return (arr || []).map(function (x) { return "<details><summary>" + esc(x.q) + "</summary><p>" + esc(x.a) + "</p></details>"; }).join(""); }
      $("g-trouble").innerHTML = qa(guide.troubleshooting);
      $("g-faq").innerHTML = qa(guide.faq);
    }

    // Changelog
    var cl = q.changelog || [];
    $("q-changelog").innerHTML = cl.length ? cl.map(function (c) { return "<li><b>" + esc(c.version) + "</b>" + esc(c.notes) + "</li>"; }).join("") : "<li><b>Coming soon</b>Patch notes for this quest will be added here.</li>";

    // Media buttons
    var want = { "Nexus Mods": ["m-nexus", "Mirror downloads"], Discord: ["m-discord", "Join the Time Patrol"], YouTube: ["m-youtube", "Trailers & reveals"], Patreon: ["m-patreon", "Support the next quest"], Facebook: ["m-facebook", "News & updates"], X: ["m-x", "Quick updates"] };
    var socials = (settings && (settings.socials || settings.social)) || [];
    var seen = {};
    var media = socials.filter(function (s) { return s && !s.hidden && want[s.name] && !seen[s.name] && (seen[s.name] = 1) && safeUrl(s.url); }).map(function (s) {
      return '<a class="' + want[s.name][0] + '" href="' + esc(safeUrl(s.url)) + '" target="_blank" rel="noopener noreferrer"><b>' + esc(s.name) + "</b><small>" + esc(want[s.name][1]) + "</small></a>";
    });
    $("q-media").innerHTML = media.join("");

    // More quests
    $("q-more").innerHTML = all.filter(function (o) { return o.slug !== q.slug; }).map(function (o) {
      return '<a href="quest.html?q=' + encodeURIComponent(o.slug) + '"><img src="' + esc(safeUrl(o.card)) + '" alt="" width="640" height="360" loading="lazy" decoding="async"><span>' + esc(o.title) + "</span></a>";
    }).join("");
  }

  function start() {
    Promise.all([load("content/work.json", "work"), load("content/fn.json", "fn"), load("content/install-guide.json", "install_guide"), load("content/settings.json", "settings")]).then(function (r) {
      var all = questList(r[0], r[1]);
      var slug = new URLSearchParams(location.search).get("q") || "";
      var q = all.filter(function (x) { return x.slug === slug; })[0];
      if (!q) {
        $("q-title").textContent = "Quest not found";
        $("q-tagline").innerHTML = 'That quest page doesn’t exist. <a href="index.html#work">See all quests</a>.';
        return;
      }
      render(q, all, r[2], r[3]);
      if (location.hash) { var t = document.querySelector(location.hash); if (t) t.scrollIntoView(); }
    });
  }
  if (location.protocol === "file:" && !window.SITE_FALLBACK) {
    var s = document.createElement("script"); s.src = "content/fallback.js"; s.onload = function () { fb = window.SITE_FALLBACK || {}; start(); }; s.onerror = start; document.head.appendChild(s);
  } else start();
})();
