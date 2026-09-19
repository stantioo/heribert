// Heribert Service Worker
//
// Aufgabe: die App vom Home-Bildschirm startbar und offline benutzbar machen.
//
// Zwei Regeln, die wichtig sind:
//  1. Die App-Hülle (index.html) wird IMMER zuerst aus dem Netz geholt. Sonst
//     würde eine neue Version nie ankommen, weil der Cache gewinnt.
//  2. Aufrufe an Supabase werden nie zwischengespeichert. Karten und Freigaben
//     kämen sonst veraltet zurück, und Antworten mit Sitzungsbezug haben in
//     einem geteilten Cache ohnehin nichts verloren.
//
// CACHE_VERSION hochzählen, wenn sich Dateien in vendor/ oder icons/ ändern.
const CACHE_VERSION = "heribert-v2";

// Nur die Dateien, die für den ersten Start gebraucht werden. Die großen
// Import-Bibliotheken (pdf.js, mammoth, jszip) landen erst im Cache, wenn sie
// wirklich benutzt werden.
const PRECACHE = [
  "./",
  "index.html",
  "confirmed.html",
  "manifest.webmanifest",
  "vendor/react-18.3.1.min.js",
  "vendor/react-dom-18.3.1.min.js",
  "vendor/supabase-js-2.116.0.min.js",
  "vendor/babel-standalone-7.29.8.min.js",
  "vendor/dompurify-3.4.15.min.js",
  "icons/icon-192.png",
  "icons/icon-512.png",
  "icons/apple-touch-icon.png",
];

self.addEventListener("install", event => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE_VERSION);
    // Einzeln statt addAll: eine fehlende Datei soll nicht die ganze
    // Installation scheitern lassen.
    await Promise.all(PRECACHE.map(url =>
      cache.add(new Request(url, { cache: "reload" })).catch(() => {})
    ));
    await self.skipWaiting();
  })());
});

self.addEventListener("activate", event => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter(k => k !== CACHE_VERSION).map(k => caches.delete(k)));
    await self.clients.claim();
  })());
});

self.addEventListener("fetch", event => {
  const req = event.request;
  if (req.method !== "GET") return;

  const url = new URL(req.url);
  const sameOrigin = url.origin === self.location.origin;

  // Supabase und alles andere Fremde: unverändert ins Netz.
  if (!sameOrigin) return;

  // Seitenaufrufe: erst Netz, bei Funkloch die zuletzt gesehene Fassung.
  if (req.mode === "navigate") {
    event.respondWith((async () => {
      try {
        // cache:"reload" umgeht den HTTP-Cache des Browsers. Ohne das kann
        // GitHub Pages die alte index.html noch minutenlang aus dem Browser-
        // Cache liefern, obwohl der Service Worker extra ins Netz geht.
        const fresh = await fetch(req, { cache: "reload" });
        const cache = await caches.open(CACHE_VERSION);
        cache.put(req, fresh.clone());
        return fresh;
      } catch (e) {
        return (await caches.match(req))
            || (await caches.match("index.html"))
            || Response.error();
      }
    })());
    return;
  }

  // Eigene Dateien: aus dem Cache, sonst holen und merken. Die Namen in
  // vendor/ enthalten die Version, deshalb ist das gefahrlos.
  event.respondWith((async () => {
    const cached = await caches.match(req);
    if (cached) return cached;
    try {
      const fresh = await fetch(req);
      if (fresh.ok && fresh.type === "basic") {
        const cache = await caches.open(CACHE_VERSION);
        cache.put(req, fresh.clone());
      }
      return fresh;
    } catch (e) {
      return Response.error();
    }
  })());
});
