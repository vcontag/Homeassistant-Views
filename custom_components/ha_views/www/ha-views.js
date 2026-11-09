// Gemeinsam für alle Seiten (wird früh im <head> geladen).
// Design: Wahl je Gerät/Browser (Diagnoseseite) – "auto", "light" oder "dark".
// Bei "auto" gilt innerhalb von Home Assistant (Seitenleiste, Companion-App) das Design von Home Assistant,
// sonst das Systemdesign. Die Seiten färben sich über :root[data-theme="light"|"dark"].
(function () {
  var KEY = 'hav:theme';
  function choice() { try { return localStorage.getItem(KEY) || 'auto'; } catch (e) { return 'auto'; } }
  // Dunkelmodus von Home Assistant, wenn die Seite in der HA-Oberfläche eingebettet ist (null = unbekannt)
  function haDark() {
    try {
      if (window.parent === window) return null;
      var hass = window.parent.document.querySelector('home-assistant');
      hass = hass && hass.hass;
      var d = hass && hass.themes && hass.themes.darkMode;
      return typeof d === 'boolean' ? d : null;
    } catch (e) { return null; }
  }
  function apply() {
    var c = choice(), root = document.documentElement, dark = null;
    if (c === 'light') dark = false;
    else if (c === 'dark') dark = true;
    else dark = haDark();
    if (dark === null) root.removeAttribute('data-theme');
    else root.setAttribute('data-theme', dark ? 'dark' : 'light');
    root.style.colorScheme = dark === null ? '' : (dark ? 'dark' : 'light');
  }
  window.HAV = {
    KEY: KEY, choice: choice, haDark: haDark, apply: apply,
    setTheme: function (v) { try { v === 'auto' ? localStorage.removeItem(KEY) : localStorage.setItem(KEY, v); } catch (e) {} apply(); }
  };
  apply();
  // HA-Design kann sich ändern (Profil, Sonnenauf-/untergang): beim Zurückkehren und regelmäßig prüfen
  document.addEventListener('visibilitychange', function () { if (!document.hidden) apply(); });
  setInterval(apply, 10000);
})();
