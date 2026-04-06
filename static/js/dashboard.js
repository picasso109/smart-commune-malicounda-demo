document.addEventListener("DOMContentLoaded", function () {
    // =========================
    // 📊 EXECUTIVE REVENUE CHART
    // =========================
    const chartCanvas = document.getElementById("financeChart");

    if (chartCanvas && typeof Chart !== "undefined") {
        const ctx = chartCanvas.getContext("2d");

        if (window.financeChartInstance) {
            window.financeChartInstance.destroy();
        }

        const gradient = ctx.createLinearGradient(0, 0, 0, 320);
        gradient.addColorStop(0, "rgba(13,110,253,0.30)");
        gradient.addColorStop(1, "rgba(13,110,253,0)");

        fetch("/dashboard/api/kpis")
            .then((response) => response.json())
            .then((data) => {
                const revenueData = [
                    8,
                    10,
                    12,
                    15,
                    17,
                    Math.round((data.recettes_value || 87500000) / 10000000)
                ];

                window.financeChartInstance = new Chart(ctx, {
                    type: "line",
                    data: {
                        labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
                        datasets: [{
                            label: "Revenue Intelligence (M FCFA)",
                            data: revenueData,
                            fill: true,
                            backgroundColor: gradient,
                            borderColor: "#0d6efd",
                            borderWidth: 3,
                            tension: 0.42,
                            pointRadius: 4,
                            pointHoverRadius: 7,
                            pointBorderWidth: 2
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        interaction: {
                            intersect: false,
                            mode: "index"
                        },
                        animation: {
                            duration: 1800,
                            easing: "easeOutQuart"
                        },
                        plugins: {
                            legend: {
                                labels: {
                                    font: {
                                        size: 13,
                                        weight: "600"
                                    }
                                }
                            },
                            tooltip: {
                                backgroundColor: "#ffffff",
                                titleColor: "#111827",
                                bodyColor: "#374151",
                                borderColor: "#e5e7eb",
                                borderWidth: 1,
                                padding: 12,
                                displayColors: false
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                ticks: {
                                    padding: 8
                                },
                                grid: {
                                    color: "rgba(0,0,0,0.05)",
                                    drawBorder: false
                                }
                            },
                            x: {
                                grid: {
                                    display: false
                                }
                            }
                        }
                    }
                });
            })
            .catch((error) => {
                console.error("Erreur chargement KPI:", error);
            });
    }

    // =========================
    // 🗺️ EXECUTIVE GEO INTELLIGENCE MAP PRO
    // =========================
    const mapDiv = document.getElementById("map");

    if (mapDiv && typeof L !== "undefined") {
        if (window.smartCommuneMap) {
            window.smartCommuneMap.remove();
        }

        const map = L.map("map", {
            zoomControl: true,
            scrollWheelZoom: true
        });

        window.smartCommuneMap = map;

        // 🌍 fond premium
        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            attribution: "© OpenStreetMap • Smart Commune GIS",
            maxZoom: 20
        }).addTo(map);

        // 📍 couches points de risques
        const zones = [
            {
                coords: [14.410, -16.980],
                title: "Pointe Sarène",
                type: "Litige foncier",
                score: 92,
                level: "Critique",
                capex: "1.2 Md FCFA",
                owner: "Service Foncier",
                color: "#dc3545"
            },
            {
                coords: [14.460, -16.930],
                title: "Falokh",
                type: "Zone sécurisée",
                score: 18,
                level: "Faible",
                capex: "450 M FCFA",
                owner: "Cadastre",
                color: "#198754"
            },
            {
                coords: [14.430, -16.950],
                title: "Madinatou Salam",
                type: "Projet voirie",
                score: 56,
                level: "Moyen",
                capex: "800 M FCFA",
                owner: "PMO",
                color: "#fd7e14"
            }
        ];

        zones.forEach((zone) => {
            const marker = L.circleMarker(zone.coords, {
                radius: 12,
                fillColor: zone.color,
                color: "#ffffff",
                weight: 3,
                fillOpacity: 0.95
            }).addTo(map);

            marker.bindPopup(`
                <div style="min-width:260px">
                    <h6 style="font-weight:700">${zone.title}</h6>
                    <hr style="margin:6px 0">
                    <p><strong>📌 Type:</strong> ${zone.type}</p>
                    <p><strong>⚠️ Niveau:</strong> ${zone.level}</p>
                    <p><strong>📊 Risk Score:</strong> ${zone.score}/100</p>
                    <p><strong>💰 Exposition:</strong> ${zone.capex}</p>
                    <p><strong>🏢 Responsable:</strong> ${zone.owner}</p>
                </div>
            `);

            L.circle(zone.coords, {
                radius: zone.score * 18,
                color: zone.color,
                fillColor: zone.color,
                fillOpacity: 0.08,
                weight: 1
            }).addTo(map);
        });

        // 🎯 zoom initial sur points
        const bounds = L.latLngBounds(zones.map((z) => z.coords));
        map.fitBounds(bounds, {
            padding: [50, 50]
        });

        // 🧭 légende pro
        const legend = L.control({ position: "bottomright" });

        legend.onAdd = function () {
            const div = L.DomUtil.create("div", "info legend");
            div.style.background = "white";
            div.style.padding = "12px";
            div.style.borderRadius = "12px";
            div.style.boxShadow = "0 8px 20px rgba(0,0,0,.12)";
            div.innerHTML = `
                <h6 style="margin-bottom:8px;font-weight:700">🧭 Risk Legend</h6>
                <div><span style="color:#dc3545">⬤</span> Critique</div>
                <div><span style="color:#fd7e14">⬤</span> Moyen</div>
                <div><span style="color:#198754">⬤</span> Faible</div>
            `;
            return div;
        };

        legend.addTo(map);

        // =========================
        // 🌍 GEOJSON POLYGON LAYER
        // =========================
        fetch("/static/data/malicounda_zones.geojson")
            .then((response) => response.json())
            .then((geojsonData) => {
                const polygonLayer = L.geoJSON(geojsonData, {
                    style: function (feature) {
                        const risk = feature.properties.risk;

                        let color = "#198754";
                        if (risk === "Critique") color = "#dc3545";
                        else if (risk === "Moyen") color = "#fd7e14";

                        return {
                            color: color,
                            fillColor: color,
                            fillOpacity: 0.22,
                            weight: 2
                        };
                    },
                    onEachFeature: function (feature, layer) {
                        const props = feature.properties;

                        layer.bindPopup(`
                            <div style="min-width:260px">
                                <h6 style="font-weight:700">${props.name}</h6>
                                <hr style="margin:6px 0">
                                <p><strong>⚠️ Risque:</strong> ${props.risk}</p>
                                <p><strong>📊 Score:</strong> ${props.score}/100</p>
                                <p><strong>💰 CAPEX:</strong> ${props.capex}</p>
                                <p><strong>🏢 Service:</strong> ${props.service}</p>
                            </div>
                        `);
                    }
                }).addTo(map);

                // 🎯 zoom intelligent final sur polygones
                map.fitBounds(polygonLayer.getBounds(), {
                    padding: [40, 40]
                });
            })
            .catch((error) => {
                console.error("Erreur GeoJSON:", error);
            });

        // 📱 responsive fix
        setTimeout(() => {
            map.invalidateSize();
        }, 500);

        window.addEventListener("resize", () => {
            map.invalidateSize();
        });
    }
});