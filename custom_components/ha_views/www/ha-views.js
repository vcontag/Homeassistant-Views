// Gemeinsam für alle Seiten (wird früh im <head> geladen).
//
// 1. Design: Wahl je Gerät/Browser (Diagnoseseite) – "auto", "light" oder "dark".
//    Bei "auto" gilt innerhalb von Home Assistant (Seitenleiste, Companion-App, Webseiten-Karte) das Design von
//    Home Assistant, sonst das Systemdesign. Die Seiten färben sich über :root[data-theme="light"|"dark"].
//
// 2. Mobilansicht: Manche Apps (eingebauter Browser/WebView) ignorieren die Viewport-Angabe, bauen die Seite mit
//    Desktop-Breite (z. B. 1082 px) auf und verkleinern sie dann aufs Display. Erkennt die Seite das (Touch-Gerät,
//    Seite deutlich breiter als das Display), vergrößert sie sich passend (CSS-Zoom) und schaltet die
//    Breiten-Regeln (@media min/max-width) so, als wäre das Fenster so breit wie das Display.
(function () {
  var THEME = 'hav:theme', FIT = 'hav:fit';
  function get(k, d) { try { return localStorage.getItem(k) || d; } catch (e) { return d; } }
  function put(k, v, d) { try { v === d ? localStorage.removeItem(k) : localStorage.setItem(k, v); } catch (e) {} }
  var root = document.documentElement;

  /* ---------- Design ---------- */
  function haDark() {
    try {
      if (window.parent === window) return null;
      var el = window.parent.document.querySelector('home-assistant');
      var d = el && el.hass && el.hass.themes && el.hass.themes.darkMode;
      return typeof d === 'boolean' ? d : null;
    } catch (e) { return null; }
  }
  function applyTheme() {
    var c = get(THEME, 'auto'), dark = c === 'light' ? false : c === 'dark' ? true : haDark();
    if (dark === null) root.removeAttribute('data-theme');
    else root.setAttribute('data-theme', dark ? 'dark' : 'light');
    root.style.colorScheme = dark === null ? '' : (dark ? 'dark' : 'light');
  }

  /* ---------- Mobilansicht ---------- */
  var fitZoom = 1;
  function coarse() { try { return matchMedia('(pointer:coarse)').matches || navigator.maxTouchPoints > 0; } catch (e) { return false; } }
  // Breite, mit der die Seite rechnen sollte (CSS px)
  function wanted() {
    var sw = screen.width, sh = screen.height;
    // Ausrichtung: Querformat, wenn das Fenster breiter als hoch ist
    var land = innerWidth > innerHeight;
    return land ? Math.max(sw, sh) : Math.min(sw, sh);
  }
  function needFit() {
    if (get(FIT, 'auto') === 'off' || !coarse()) return 1;
    var w = wanted(), real = innerWidth; // innerWidth hängt nicht vom CSS-Zoom ab
    // nur bei deutlich zu breiter Rechnung auf kleinen Displays (normale Handys und PCs bleiben unberührt)
    return w > 0 && w <= 1024 && real > w * 1.3 ? real / w : 1;
  }
  // Breitenabfragen der Seite für die gewünschte Breite auswerten (Original bleibt gemerkt)
  function evalWidth(text, w) {
    var parts = text.split(/\s+and\s+/i), ok = true, any = false;
    for (var i = 0; i < parts.length; i++) {
      var m = parts[i].match(/^\(\s*(min|max)-width\s*:\s*([\d.]+)px\s*\)$/i);
      if (!m) return null; // andere Merkmale: unverändert lassen
      any = true;
      var v = parseFloat(m[2]);
      if (m[1].toLowerCase() === 'max' ? w > v : w < v) ok = false;
    }
    return any ? ok : null;
  }
  function rewriteMedia(w) {
    for (var s = 0; s < document.styleSheets.length; s++) {
      var rules;
      try { rules = document.styleSheets[s].cssRules; } catch (e) { continue; } // fremde Stylesheets (Schriften)
      for (var r = 0; r < rules.length; r++) {
        var rule = rules[r];
        if (!rule.media || rule.type !== 4) continue;
        if (rule.__hav === undefined) rule.__hav = rule.media.mediaText;
        var orig = rule.__hav, res = w ? evalWidth(orig, w) : null;
        var text = res === null ? orig : res ? 'all' : 'not all';
        if (rule.media.mediaText !== text) rule.media.mediaText = text;
      }
    }
  }
  function applyFit() {
    // erst ohne Zoom messen, dann ggf. neu setzen
    var z = needFit();
    if (Math.abs(z - fitZoom) < 0.02) return;
    fitZoom = z;
    if (z > 1) {
      root.style.zoom = z;
      root.setAttribute('data-fit', '');
      rewriteMedia(wanted());
    } else {
      root.style.zoom = '';
      root.removeAttribute('data-fit');
      rewriteMedia(0);
    }
  }

  window.HAV = {
    THEME: THEME, FIT: FIT,
    choice: function () { return get(THEME, 'auto'); },
    fitChoice: function () { return get(FIT, 'auto'); },
    haDark: haDark,
    setTheme: function (v) { put(THEME, v, 'auto'); applyTheme(); },
    setFit: function (v) { put(FIT, v, 'auto'); fitZoom = 0; applyFit(); },
    // Zoom und Breite, mit der die Seite effektiv rechnet
    zoom: function () { return fitZoom; },
    width: function () { return Math.round(innerWidth / (fitZoom || 1)); },
    apply: function () { applyTheme(); applyFit(); }
  };
  applyTheme();
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', applyFit);
  else applyFit();
  addEventListener('load', applyFit);
  addEventListener('resize', function () { clearTimeout(window.__havT); window.__havT = setTimeout(applyFit, 150); });
  // HA-Design kann sich ändern (Profil, Sonnenauf-/untergang): beim Zurückkehren und regelmäßig prüfen
  document.addEventListener('visibilitychange', function () { if (!document.hidden) applyTheme(); });
  setInterval(applyTheme, 10000);
})();
