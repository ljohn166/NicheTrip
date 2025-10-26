document.addEventListener("DOMContentLoaded", () => {
  const mapContainer = document.getElementById("map");
  const recommendationList = document.getElementById("recommendationList");
  const pageShell = document.querySelector(".results-shell");

  if (!mapContainer || !recommendationList || !pageShell || typeof L === "undefined") {
    return;
  }

  const defaultCenter = [40.7128, -74.0060];
  const map = L.map(mapContainer, {
    center: defaultCenter,
    zoom: 12,
    minZoom: 11,
    maxZoom: 18,
    zoomControl: true,
    scrollWheelZoom: false,
    attributionControl: false,
  });

  map.on("mouseover", function () {
    map.scrollWheelZoom.enable();
  });

  map.on("mouseout", function () {
    map.scrollWheelZoom.disable();
  });


  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
  }).addTo(map);

  const iconRetinaUrl = "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png";
  const iconUrl = "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png";
  const shadowUrl = "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png";

  L.Icon.Default.mergeOptions({
    iconRetinaUrl,
    iconUrl,
    shadowUrl,
  });

  const markers = new Map();
  let hasAtLeastOneCoordinate = false;

  recommendationList.querySelectorAll(".recommendation-card").forEach((card) => {
    const name = card.getAttribute("data-name") ?? "Unknown";
    const description = card.getAttribute("data-description") ?? "";
    const lat = parseFloat(card.getAttribute("data-latitude") ?? "");
    const lng = parseFloat(card.getAttribute("data-longitude") ?? "");

    if (!Number.isFinite(lat) || !Number.isFinite(lng)) {
      return;
    }

    hasAtLeastOneCoordinate = true;

    const marker = L.marker([lat, lng]).addTo(map);
    marker.bindPopup(
      `<strong>${name}</strong><div style="margin-top:0.35rem;font-size:0.9rem;color:#475569;">${description}</div>`
    );

    markers.set(card, marker);

    card.addEventListener("click", () => {
      map.flyTo([lat, lng], 15, { animate: true, duration: 1.4 });
      marker.openPopup();
    });
  });

  if (!hasAtLeastOneCoordinate) {
    mapContainer.innerHTML =
      '<div class="map-empty-state">Map preview unavailable — coordinates missing for current itinerary.</div>';
    map.remove();
  }

  window.addEventListener("resize", () => {
    map.invalidateSize();
  });
});