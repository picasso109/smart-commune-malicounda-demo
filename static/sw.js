const CACHE_NAME = "smart-commune-v3";
const APP_ROUTES = [
    "/",
    "/foncier/",
    "/finances/",
    "/projets/",
    "/incidents/",
    "/auth/login"
];

// =========================
// 📦 INSTALL
// =========================
self.addEventListener("install", (event) => {
    self.skipWaiting();

    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(APP_ROUTES);
        })
    );
});

// =========================
// ♻️ ACTIVATE
// =========================
self.addEventListener("activate", (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cache) => {
                    if (cache !== CACHE_NAME) {
                        return caches.delete(cache);
                    }
                })
            );
        })
    );

    self.clients.claim();
});

// =========================
// 🌐 FETCH → NETWORK FIRST
// =========================
self.addEventListener("fetch", (event) => {
    event.respondWith(
        fetch(event.request)
            .then((networkResponse) => {
                return caches.open(CACHE_NAME).then((cache) => {
                    cache.put(event.request, networkResponse.clone());
                    return networkResponse;
                });
            })
            .catch(() => {
                return caches.match(event.request);
            })
    );
});