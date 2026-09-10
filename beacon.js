/* A page-view counter for sanelabs.org, kept as small as the thing it measures.
 *
 * No cookie, no localStorage, no visitor id, no IP and no user agent: one row
 * saying which page was opened, which host sent the reader, and how wide the
 * window was. That is enough to answer the only question worth asking after a
 * post goes up — did anyone arrive, and from where — and not enough to follow
 * anybody around. Do Not Track is honoured.
 *
 * The key below is the project's publishable key, the same one the run log
 * already reads with. Row-level security lets it INSERT into `hit` and nothing
 * else; the table has no SELECT policy, so the log cannot be read back from a
 * browser. Failures are swallowed on purpose — a counter must never be able to
 * break a page.
 */
(function () {
  try {
    if (navigator.doNotTrack === "1" || window.doNotTrack === "1" ||
        navigator.globalPrivacyControl) return;

    var URL_ = "https://lqswldfiqgpqwwhetrlw.supabase.co";
    var KEY = "sb_publishable_kuNsZM28zvADNuCrt6pmxQ_XdMUu2Wv";

    var path = (location.pathname || "/").replace(/index\.html$/, "") || "/";

    var refHost = null, internal = false;
    if (document.referrer) {
      try {
        var h = new URL(document.referrer).host;
        if (h === location.host) internal = true; else refHost = h;
      } catch (e) { /* an unparseable referrer is simply no referrer */ }
    }

    var q = new URLSearchParams(location.search);
    var src = q.get("src") || q.get("utm_source");

    var cut = function (s, n) { return s ? String(s).slice(0, n) : null; };

    fetch(URL_ + "/rest/v1/hit", {
      method: "POST",
      headers: {
        apikey: KEY,
        Authorization: "Bearer " + KEY,
        "Content-Type": "application/json",
        Prefer: "return=minimal"
      },
      body: JSON.stringify({
        path: cut(path, 128),
        ref_host: cut(refHost, 128),
        src: cut(src, 64),
        width: Math.min(window.innerWidth || 0, 10000),
        entry: !internal
      }),
      keepalive: true
    }).catch(function () {});
  } catch (e) { /* never let the counter matter */ }
})();
