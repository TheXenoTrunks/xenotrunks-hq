(function () {
  var TZ = "Australia/Perth";

  var menu = document.getElementById("menu");
  var nav = document.getElementById("navigation");
  if (menu && nav) {
    function setOpen(open) {
      nav.classList.toggle("open", open);
      menu.setAttribute("aria-expanded", String(open));
      menu.textContent = open ? "Close" : "Menu";
    }
    menu.addEventListener("click", function () { setOpen(!nav.classList.contains("open")); });
    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () { setOpen(false); });
    });
  }

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }
  // Only allow http(s) links and site-relative paths (blocks javascript: and data: URLs typed into the CMS).
  function safeUrl(u) {
    if (u == null) return "";
    u = String(u).trim();
    if (!u) return "";
    if (/^https?:\/\//i.test(u)) return u;
    if (/^[a-z][a-z0-9+.-]*:/i.test(u) || u.indexOf("//") === 0) return "";
    return u;
  }
  function mediaPath(p) {
    if (!p) return "";
    p = String(p).trim();
    if (/^https?:\/\//i.test(p)) return p;
    if (/^[a-z][a-z0-9+.-]*:/i.test(p) || p.indexOf("//") === 0) return "";
    return p.replace(/^\//, "");
  }
  function parseWhen(s, endOfDay) {
    if (s == null) return null;
    s = String(s).trim();
    if (!s) return null;
    if (/^\d{4}-\d{2}-\d{2}$/.test(s)) {
      return new Date(s + (endOfDay ? "T23:59:59+08:00" : "T00:00:00+08:00"));
    }
    var d = new Date(s);
    return isNaN(d.getTime()) ? null : d;
  }
  function windowState(start, end, now) {
    var a = parseWhen(start, false);
    var b = parseWhen(end, true);
    if (a && now < a) return "upcoming";
    if (b && now > b) return "recent";
    if (a && now >= a && b && now <= b) return "live";
    if (!a && b && now <= b) return "live";
    if (!a && b && now > b) return "recent";
    if (a && !b && now >= a) return "open";
    return "open";
  }
  function itemState(item, now) {
    if (item.hidden) return "hidden";
    if (item.windows && item.windows.length) {
      var states = item.windows.map(function (w) { return windowState(w.starts_at, w.ends_at, now); });
      if (states.indexOf("live") >= 0) return "live";
      if (states.every(function (s) { return s === "upcoming"; })) return "upcoming";
      if (states.every(function (s) { return s === "recent"; })) return "recent";
      if (states.indexOf("upcoming") >= 0) return "upcoming";
      return "recent";
    }
    var st = windowState(item.starts_at, item.ends_at, now);
    if (st === "open") return item.kind === "announcement" ? "announcement" : "live";
    return st;
  }
  function perthDate(iso) {
    if (!iso) return "";
    var d = new Date(iso);
    if (isNaN(d)) return iso;
    return new Intl.DateTimeFormat("en-GB", { timeZone: TZ, day: "numeric", month: "short", year: "numeric" }).format(d);
  }
  function extLink(href, label) {
    href = safeUrl(href);
    if (!href) return "";
    return '<a href="' + esc(href) + '" target="_blank" rel="noopener noreferrer">' + esc(label || "Source") + " ↗</a>";
  }
  function setText(id, value, html) {
    var el = document.getElementById(id);
    if (!el || value == null || value === "") return el;
    if (html) el.innerHTML = value;
    else el.textContent = value;
    return el;
  }
  function setImg(id, src, alt) {
    var el = document.getElementById(id);
    if (!el) return;
    if (src) el.src = mediaPath(src);
    if (alt) el.alt = alt;
  }

  function applySettings(s) {
    if (!s) return;
    var site = s.site || {};
    var hero = s.hero || {};
    if (site.title) document.title = site.title;
    var desc = document.querySelector('meta[name="description"]');
    if (desc && site.description) desc.setAttribute("content", site.description);
    setImg("brand-logo", site.logo);
    setImg("footer-logo", site.logo);
    if (site.name || site.tagline) {
      var name = esc((site.name || "Xeno Trunks").toUpperCase());
      var tag = esc((site.tagline || "Time Patrol").toUpperCase());
      setText("brand-name", name + "<small>" + tag + "</small>", true);
      setText("footer-name", (site.name || "Xeno Trunks").toUpperCase());
    }
    if (s.nav_cta && s.nav_cta.url) {
      var cta = document.getElementById("nav-cta");
      if (cta) { cta.href = s.nav_cta.url; cta.textContent = s.nav_cta.label || "Join Discord"; }
    }
    setImg("hero-image", hero.image, hero.image_alt);
    setText("hero-kicker", hero.kicker);
    if (hero.headline) {
      setText("hero-title", esc(hero.headline) + (hero.headline_accent ? " <span>" + esc(hero.headline_accent) + "</span>" : ""), true);
    }
    setText("hero-lead", hero.intro);
    if (hero.buttons && hero.buttons.length) {
      var actions = document.getElementById("hero-actions");
      if (actions) {
        actions.innerHTML = hero.buttons.map(function (b) {
          var cls = b.style === "outline" ? "btn outline" : "btn";
          return '<a class="' + cls + '" href="' + esc(safeUrl(b.url)) + '" target="_blank" rel="noopener noreferrer">' + esc(b.label) + "</a>";
        }).join("");
      }
    }
    if (s.ticker && s.ticker.length) {
      var ticker = document.getElementById("ticker");
      if (ticker) {
        ticker.innerHTML = s.ticker.map(function (item) {
          return "<span><b>" + esc(item.number) + "</b> &nbsp; " + esc(item.label) + "</span>";
        }).join("");
      }
    }
    if (s.patreon) {
      var p = s.patreon;
      setImg("patreon-image", p.image, p.image_alt);
      var copy = document.getElementById("patreon-copy");
      if (copy) {
        var btn = "";
        if (p.enabled && p.url) {
          btn = '<a class="btn" href="' + esc(safeUrl(p.url)) + '" target="_blank" rel="noopener noreferrer">' + esc(p.button_label || "Join the Patreon") + "</a>";
        }
        copy.innerHTML = '<p class="kicker">' + esc(p.kicker || "") + "</p><h2>" + esc(p.title || "Patreon.") + "</h2><p>" + esc(p.text || "") + "</p>" + btn;
      }
    }
    if (s.paypal) {
      var pay = s.paypal;
      var box = document.getElementById("paypal");
      if (box) {
        var payBtn;
        // PayPal is a plain link only. No PayPal script or SDK is ever loaded.
        // It renders only when enabled is true AND the URL is an official https://www.paypal.com/ or https://paypal.me/ link.
        var payUrl = safeUrl(pay.url);
        var payOk = pay.enabled === true && /^https:\/\/(www\.)?(paypal\.com|paypal\.me)\//i.test(payUrl);
        var title = pay.title || "", text = pay.text || "";
        if (payOk) {
          title = pay.live_title || title;
          text = pay.live_text || text;
          payBtn = '<a class="btn" href="' + esc(payUrl) + '" target="_blank" rel="noopener noreferrer">' + esc(pay.live_button_label || "Support Xeno Trunks on PayPal") + "</a>";
        } else {
          payBtn = '<span class="btn outline" aria-disabled="true">' + esc(pay.button_label || "Coming soon") + "</span>";
        }
        box.innerHTML = '<p class="kicker">' + esc(pay.kicker || "PayPal") + "</p><h3>" + esc(title) + "</h3><p>" + esc(text) + "</p>" + payBtn;
      }
    }
    if (s.community) {
      var ch = document.getElementById("community-heading");
      if (ch) {
        ch.innerHTML = '<p class="kicker">' + esc(s.community.kicker || "Community") + "</p><h2>" + esc(s.community.title || "") + "</h2><p>" + esc(s.community.intro || "") + "</p>";
      }
      function fillPanel(id, card) {
        var el = document.getElementById(id);
        if (!el || !card) return;
        if (safeUrl(card.url)) el.href = safeUrl(card.url);
        var img = el.querySelector("img");
        if (img) {
          if (card.image) img.src = mediaPath(card.image);
          if (card.image_alt) img.alt = card.image_alt;
        }
        var copyEl = el.querySelector(".panel-copy");
        if (copyEl) {
          copyEl.innerHTML = '<p class="kicker">' + esc(card.kicker || "") + "</p><h3>" + esc(card.title || "") + "</h3><p>" + esc(card.text || "") + '</p><span class="go">' + esc(card.button_label || "Open") + " ↗</span>";
        }
      }
      fillPanel("community-discord", s.community.discord);
      fillPanel("community-group", s.community.facebook_group);
    }
    if (s.connect) {
      var conn = document.getElementById("connect-heading");
      if (conn) {
        conn.innerHTML = '<p class="kicker">' + esc(s.connect.kicker || "") + "</p><h2>" + esc(s.connect.title || "") + "</h2><p>" + esc(s.connect.intro || "") + "</p>";
      }
    }
    if (s.socials && s.socials.length) {
      var root = document.getElementById("socials-root");
      if (root) {
        root.innerHTML = s.socials.map(function (item) {
          return '<a class="social" href="' + esc(safeUrl(item.url)) + '" target="_blank" rel="noopener noreferrer"><span>' + esc(item.name) + "<small>" + esc(item.handle || "") + '</small></span><span class="arr" aria-hidden="true">↗</span></a>';
        }).join("");
      }
    }
    if (s.footer) {
      setText("footer-tagline", s.footer.tagline);
      setText("footer-disclaimer", s.footer.disclaimer);
    }
  }

  function displayTitle(item, state, now) {
    if (item.weeks && item.weeks.length && (item.title_prefix || item.title)) {
      var liveWeek = null;
      item.weeks.forEach(function (w) {
        if (windowState(w.starts_at, w.ends_at, now) === "live") liveWeek = w;
      });
      if (liveWeek) {
        return (item.title_prefix || "Final Festival") + " — " + liveWeek.id + ": " + liveWeek.mode;
      }
    }
    return item.title || "";
  }

  function renderNews(data) {
    var root = document.getElementById("news-root");
    if (!root || !data || !data.items) return;
    var now = new Date();
    var groups = { live: [], upcoming: [], recent: [], announcement: [] };
    var labels = { live: "Live now", upcoming: "Upcoming", recent: "Past events", announcement: "Announcements" };
    var badgeText = { live: "Live now", upcoming: "Upcoming", recent: "Ended", announcement: "Announcement" };
    var badgeClass = { live: "current", upcoming: "upcoming", recent: "recent", announcement: "" };
    data.items.forEach(function (item) {
      var state = itemState(item, now);
      if (state === "hidden") return;
      if (!groups[state]) groups[state] = [];
      groups[state].push({ item: item, state: state });
    });
    function card(entry) {
      var item = entry.item;
      var state = entry.state;
      var weeks = "";
      if (item.weeks) {
        weeks = '<div class="weeks">' + item.weeks.map(function (w) {
          var ws = windowState(w.starts_at, w.ends_at, now);
          var cls = ws === "live" ? "current" : ws === "recent" ? "ended" : ws;
          return '<div class="week ' + cls + '"><b>' + esc(w.id) + " · " + esc(w.mode) + "</b><span>" + esc(w.dates || "") + "</span></div>";
        }).join("") + "</div>";
        if (item.weeks_note) weeks += '<p style="margin-top:8px;font-size:0.88rem">' + esc(item.weeks_note) + "</p>";
      }
      var src = extLink(item.source_url, item.source_label || "Source");
      var img = mediaPath(item.image);
      var media = "";
      if (img) {
        media = '<figure class="news-media"><img src="' + esc(img) + '" alt="' + esc(item.image_alt || "") + '" width="1280" height="720" loading="lazy" decoding="async">' +
          (item.image_credit ? "<figcaption>" + esc(item.image_credit) + "</figcaption>" : "") + "</figure>";
      }
      return '<article class="news-card' + (media ? " has-media" : "") + '">' + media + '<div class="news-body"><div class="news-meta"><span class="badge ' + badgeClass[state] + '">' + badgeText[state] + "</span><span>" + esc(item.kicker || "") + "</span><span>" + esc(item.date_label || "") + "</span></div><h3>" + esc(displayTitle(item, state, now)) + "</h3><p>" + esc(item.summary) + "</p>" + (media ? "</div><div class=\"news-extra\">" : "") + weeks + src + "</div></article>";
    }
    function endTime(e) {
      var it = e.item, ends = [];
      if (it.windows) it.windows.forEach(function (w) { var d = parseWhen(w.ends_at, true); if (d) ends.push(d.getTime()); });
      var d0 = parseWhen(it.ends_at, true); if (d0) ends.push(d0.getTime());
      return ends.length ? Math.max.apply(null, ends) : 0;
    }
    function startTime(e) { var d = parseWhen(e.item.starts_at, false); return d ? d.getTime() : 0; }
    groups.upcoming.sort(function (a, b) { return startTime(a) - startTime(b); });
    groups.recent.sort(function (a, b) { return endTime(b) - endTime(a); });
    var html = "";
    ["live", "upcoming", "announcement"].forEach(function (key) {
      if (!groups[key].length) return;
      html += '<div class="news-group"><h3>' + labels[key] + "</h3><div class=\"news-list\">" + groups[key].map(card).join("") + "</div></div>";
    });
    // Ended raids/events move here automatically once their end time passes (collapsed by default).
    if (groups.recent.length) {
      html += '<details class="news-archive" id="past-events"><summary>' + labels.recent + " (" + groups.recent.length + ")</summary><div class=\"news-list\">" + groups.recent.map(card).join("") + "</div></details>";
    }
    root.innerHTML = html || "<p>No news items to show.</p>";
  }

  function bindPlayers(root) {
    root.querySelectorAll("[data-yt]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var id = btn.getAttribute("data-yt");
        var iframe = document.createElement("iframe");
        iframe.src = "https://www.youtube-nocookie.com/embed/" + encodeURIComponent(id) + "?autoplay=1";
        iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
        iframe.allowFullscreen = true;
        iframe.title = btn.getAttribute("data-title") || "YouTube video";
        btn.innerHTML = "";
        btn.appendChild(iframe);
        btn.style.cursor = "default";
      });
    });
  }

  function videoCard(v) {
    var cdn = "https://i.ytimg.com/vi/" + encodeURIComponent(v.id) + "/hqdefault.jpg";
    var thumb = mediaPath(v.thumb || v.thumb_cdn || cdn) || cdn;
    var watch = safeUrl(v.url) || ("https://www.youtube.com/watch?v=" + encodeURIComponent(v.id));
    return '<article class="yt-card"><button class="yt-thumb" type="button" data-yt="' + esc(v.id) + '" data-title="' + esc(v.title) + '" aria-label="Play ' + esc(v.title) + '"><img src="' + esc(thumb) + '" data-cdn="' + esc(cdn) + '" alt="" width="480" height="360" loading="lazy" decoding="async"><span class="play"><span aria-hidden="true">▶</span></span></button><h3><a href="' + esc(watch) + '" target="_blank" rel="noopener noreferrer">' + esc(v.title) + "</a></h3><time datetime=\"" + esc(v.published || "") + "\">" + (v.published ? perthDate(v.published) : "") + "</time></article>";
  }

  function renderVideos(manual, auto) {
    var root = document.getElementById("yt-root");
    if (!root) return;
    manual = manual || {};
    auto = auto || {};
    if (manual.kicker || manual.title || manual.intro) {
      var heading = document.getElementById("yt-heading");
      if (heading) {
        heading.innerHTML = '<p class="kicker">' + esc(manual.kicker || "Xeno Trunks YouTube") + "</p><h2>" + esc(manual.title || "Latest videos & Shorts.") + "</h2><p>" + esc(manual.intro || "") + "</p>";
      }
    }
    var seen = {};
    var autoItems = (auto.items || []).filter(function (v) {
      if (!v || !v.id || seen[v.id]) return false;
      seen[v.id] = true;
      return true;
    });
    var autoMap = {};
    autoItems.forEach(function (v) { autoMap[v.id] = v; });
    var featured = (manual.featured || []).map(function (f) {
      var full = autoMap[f.id] ? Object.assign({}, autoMap[f.id], f) : f;
      if (!full.thumb && !full.thumb_cdn && full.id) {
        full.thumb_cdn = "https://i.ytimg.com/vi/" + full.id + "/hqdefault.jpg";
      }
      return full;
    }).filter(function (v) { return v.id; });
    var featuredIds = {};
    featured.forEach(function (v) { featuredIds[v.id] = true; });
    var rest = autoItems.filter(function (v) { return !featuredIds[v.id]; });
    // If featured videos are already in the auto list, keep a single grid of unique items (featured first).
    var list = featured.concat(rest).slice(0, 10);
    root.innerHTML = list.map(videoCard).join("");
    // If a saved thumbnail file is missing, fall back to YouTube's own thumbnail.
    root.querySelectorAll("img[data-cdn]").forEach(function (img) {
      img.addEventListener("error", function () {
        var cdn = img.getAttribute("data-cdn");
        if (cdn && img.src !== cdn) img.src = cdn;
      }, { once: true });
    });
    bindPlayers(root);
    var channel = document.querySelector('#youtube .wrap > p:last-of-type a, #yt-channel');
    var chUrl = manual.channel_url || "https://www.youtube.com/@Xeno_Trunks";
    var chBtn = document.getElementById("yt-channel");
    if (!chBtn) {
      var wrap = document.querySelector("#youtube .wrap");
      if (wrap) {
        var links = wrap.querySelectorAll('a[href*="youtube.com"]');
        links.forEach(function (a) {
          if (/open the channel/i.test(a.textContent)) {
            a.id = "yt-channel";
            a.href = chUrl;
          }
        });
      }
    } else {
      chBtn.href = chUrl;
    }
  }

  function renderMods(data) {
    if (!data) return;
    setImg("workshop-image", data.image, data.image_alt);
    setText("workshop-kicker", data.kicker);
    setText("workshop-title", data.title);
    setText("workshop-intro", data.intro);
    var list = document.getElementById("workshop-list");
    if (list && data.items) {
      list.innerHTML = data.items.filter(function (m) { return m && !m.hidden; }).map(function (m) {
        var bits = "<li><strong>" + esc(m.title) + "</strong>";
        if (m.status && m.status !== "available") bits += " — " + esc(m.status.replace(/-/g, " "));
        if (m.description) bits += " — " + esc(m.description);
        var links = [];
        if (m.tutorial_url) links.push(extLink(m.tutorial_url, "Tutorial"));
        if (m.video_url) links.push(extLink(m.video_url, "Video"));
        if (m.download_url) links.push(extLink(m.download_url, "Download"));
        if (links.length) bits += '<div class="mod-links">' + links.join(" ") + "</div>";
        return bits + "</li>";
      }).join("");
    }
    var cta = document.getElementById("workshop-cta");
    if (cta) {
      if (data.button_url) {
        cta.innerHTML = '<a class="btn" href="' + esc(safeUrl(data.button_url)) + '" target="_blank" rel="noopener noreferrer">' + esc(data.button_label || "Visit the Patreon") + "</a>";
      } else {
        cta.innerHTML = "";
      }
    }
  }

  function renderFn(data) {
    if (!data) return;
    setImg("fn-image", data.image, data.image_alt);
    setText("fn-badge", data.badge);
    setText("fn-kicker", data.kicker);
    setText("fn-title", data.title);
    setText("fn-intro", data.intro);
    setText("fn-note", data.note);
    var list = document.getElementById("fn-list");
    if (list && data.progress) {
      list.innerHTML = data.progress.filter(function (row) { return row && !row.hidden; }).map(function (row) {
        var html = "<li>" + esc(row.item || "");
        if (row.note) html += " — " + esc(row.note);
        if (row.percent != null && row.percent !== "") {
          var pct = Math.max(0, Math.min(100, Number(row.percent)));
          if (!isNaN(pct)) html += ' <span>(' + pct + '%)</span><div class="fn-bar" aria-hidden="true"><span style="width:' + pct + '%"></span></div>';
        }
        return html + "</li>";
      }).join("");
    }
    var actions = document.getElementById("fn-actions");
    if (actions) {
      function actionBtn(url, label) {
        url = safeUrl(url);
        if (url) return '<a class="btn" href="' + esc(url) + '" target="_blank" rel="noopener noreferrer">' + esc(label) + "</a>";
        return '<span class="btn outline" aria-disabled="true">' + esc(label) + "</span>";
      }
      var extra = "";
      if (data.updates && data.updates.length) {
        extra = '<ul class="fn-updates">' + data.updates.map(function (u) {
          return "<li>" + (u.date ? "<b>" + esc(u.date) + "</b> — " : "") + esc(u.text || "") + "</li>";
        }).join("") + "</ul>";
      }
      actions.innerHTML = extra + actionBtn(data.trailer_url, data.trailer_label || "Trailer — coming when released") + actionBtn(data.download_url, data.download_label || "Download — coming when released");
    }
  }

  function loadJSON(path, fallback) {
    if (location.protocol === "file:") return Promise.resolve(fallback);
    return fetch(path).then(function (r) { return r.ok ? r.json() : fallback; }).catch(function () { return fallback; });
  }

  function start() {
  var fb = window.SITE_FALLBACK || {};
  Promise.all([
    loadJSON("content/settings.json", fb.settings || null),
    loadJSON("content/news.json", fb.news || window.NEWS_FALLBACK || null),
    loadJSON("content/videos.json", fb.videos || null),
    loadJSON("content/videos-auto.json", fb.videos_auto || window.YT_FALLBACK || null),
    loadJSON("content/mods.json", fb.mods || null),
    loadJSON("content/fn.json", fb.fn || null)
  ]).then(function (all) {
    applySettings(all[0]);
    renderNews(all[1]);
    renderVideos(all[2], all[3]);
    renderMods(all[4]);
    renderFn(all[5]);
  });
  }
  // Online, content comes from content/*.json. When the page is opened as a local file
  // (no web server), load the bundled copy in content/fallback.js first.
  if (location.protocol === "file:" && !window.SITE_FALLBACK) {
    var fs = document.createElement("script");
    fs.src = "content/fallback.js";
    fs.onload = start;
    fs.onerror = start;
    document.head.appendChild(fs);
  } else {
    start();
  }
})();
