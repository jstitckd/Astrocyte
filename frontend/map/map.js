/* Labels and descriptions come from models/areas.py. Artwork lives in index.html. */
(() => {
  "use strict";
  const buildings = [...document.querySelectorAll(".building[data-area]")];
  const spaceList = document.getElementById("space-list");
  const openButton = document.getElementById("open-page");
  const touch = window.matchMedia("(hover: none)").matches;
  let areas = new Map();
  let selected = null;
  let disabled = false;

  // The map is an iframe. These messages are the bridge back to Streamlit.
  const send = (type, payload = {}) => window.parent.postMessage({isStreamlitMessage: true, type, ...payload}, "*");
  const resize = () => send("streamlit:setFrameHeight", {height: Math.ceil(document.querySelector(".map-shell").getBoundingClientRect().height) + 4});

  function selectArea(id) {
    const area = areas.get(id);
    if (!area) return;
    selected = id;
    buildings.forEach(building => building.classList.toggle("selected", building.dataset.area === id));
    spaceList.querySelectorAll("button").forEach(button => button.setAttribute("aria-pressed", String(button.dataset.area === id)));
    document.getElementById("selected-category").textContent = area.category;
    document.getElementById("selected-name").textContent = area.name;
    document.getElementById("selected-description").textContent = area.description;
    const features = document.getElementById("selected-features");
    features.replaceChildren();
    (area.features || []).forEach(label => {
      const item = document.createElement("li");
      item.textContent = label;
      features.appendChild(item);
    });
    openButton.disabled = disabled;
    openButton.setAttribute("aria-label", "Open " + area.name + " page");
    requestAnimationFrame(resize);
  }

  function openArea(id) {
    if (disabled || !areas.has(id)) return;
    send("streamlit:setComponentValue", {
      value: {area: id, event_id: Date.now().toString(36) + "-" + Math.random().toString(36).slice(2)},
      dataType: "json",
    });
  }

  buildings.forEach(building => {
    const id = building.dataset.area;
    building.addEventListener("mouseenter", () => { if (!touch) selectArea(id); });
    building.addEventListener("focus", () => selectArea(id));
    building.addEventListener("click", () => { selectArea(id); openArea(id); });
    building.addEventListener("keydown", event => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        selectArea(id);
        openArea(id);
      }
    });
  });
  openButton.addEventListener("click", () => openArea(selected));

  window.addEventListener("message", event => {
    if (event.source !== window.parent || event.data?.type !== "streamlit:render") return;
    const args = event.data.args || {};
    areas = new Map((args.areas || []).map(area => [area.id, area]));
    disabled = Boolean(event.data.disabled);
    if (typeof args.accent === "string" && /^#[0-9a-f]{6}$/i.test(args.accent)) {
      document.documentElement.style.setProperty("--accent", args.accent);
      document.documentElement.style.setProperty("--accent-soft", args.accent + "1f");
    }
    document.getElementById("area-count").textContent = String(areas.size).padStart(2, "0");
    buildings.forEach(building => {
      const area = areas.get(building.dataset.area);
      building.setAttribute("aria-disabled", String(disabled || !area));
      if (!area) return;
      building.setAttribute("aria-label", "Open " + area.name + " page");
      building.querySelector(".label-name").textContent = area.label;
      building.querySelector(".label-code").textContent = area.code;
    });
    spaceList.replaceChildren();
    areas.forEach(area => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "area-link";
      button.dataset.area = area.id;
      button.disabled = disabled;
      button.setAttribute("aria-label", "Open " + area.name + " page");
      for (const [className, text] of [["area-number", area.code], ["area-title", area.label], ["area-arrow", "↗"]]) {
        const span = document.createElement("span");
        span.className = className;
        span.textContent = text;
        button.appendChild(span);
      }
      button.addEventListener("mouseenter", () => { if (!touch) selectArea(area.id); });
      button.addEventListener("focus", () => selectArea(area.id));
      button.addEventListener("click", event => {
        selectArea(area.id);
        // Touch previews first; the Open space button is the next action.
        // Keyboard activation still navigates directly on a touch device.
        if (!touch || event.detail === 0) openArea(area.id);
      });
      spaceList.appendChild(button);
    });
    const initial = selected && areas.has(selected) ? selected : (areas.has("living") ? "living" : areas.keys().next().value);
    if (initial) selectArea(initial);
    requestAnimationFrame(resize);
  });

  if (touch) document.getElementById("map-instructions").textContent = "Tap a building to open · Choose a space below to preview";
  new ResizeObserver(() => requestAnimationFrame(resize)).observe(document.querySelector(".map-shell"));
  document.fonts.ready.then(resize);
  send("streamlit:componentReady", {apiVersion: 1});
})();
