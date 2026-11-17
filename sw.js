const CACHE_NAME = 'toolbox-v5';
const STATIC_ASSETS = [
  './',
  './index.html',
  './manifest.json'
];

// Install: cache static assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(STATIC_ASSETS))
  );
  self.skipWaiting();
});

// Activate: clean old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// Fetch: network-first for HTML/manifest (so edits/new tools show immediately),
// cache-first for other static assets (fonts, icons, etc.)
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // Encrypted private files are never cached
  if (url.pathname.includes('/vault/')) return;

  const isHTMLOrDynamic =
    event.request.mode === 'navigate' ||
    url.pathname.endsWith('.html') ||
    url.pathname.endsWith('/') ||
    url.pathname.endsWith('manifest.json') ||
    url.pathname.endsWith('library.json') ||
    url.pathname.includes('/tools/');

  if (isHTMLOrDynamic) {
    // Network-first: always try fresh content, fall back to cache when offline
    event.respondWith(
      fetch(event.request)
        .then(response => {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
          return response;
        })
        .catch(() => caches.match(event.request))
    );
    return;
  }

  // Everything else (fonts, images, etc.): cache-first
  event.respondWith(
    caches.match(event.request).then(cached => cached || fetch(event.request))
  );
});
