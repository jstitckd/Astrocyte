/* Interaction only. Draw/move buildings in index.html; recolour them in map.css. */
(() => {
  "use strict";
  const buildings = [...document.querySelectorAll("[data-area]")];
  const mobileButtons = document.getElementById("mobile-buildings");
  const openButton = document.getElementById("open-page");
  const touch = window.matchMedia("(hover: none)").matches;
  let areas = new Map();
  let selected = null;
  let disabled = false;

  // Streamlit's component bridge: HTML runs in an iframe, separate from Python.
  const send = (type, payload = {}) => window.parent.postMessage({isStreamlitMessage: true, type, ...payload}, "*");
  const resize = () => send("streamlit:setFrameHeight", {height: Math.ceil(document.querySelector(".map-shell").getBoundingClientRect().height)});

  function selectArea(id) {
    if (!areas.has(id)) return;
    selected = id;
    buildings.forEach(building => building.classList.toggle("selected", building.dataset.area === id));
    mobileButtons.querySelectorAll("button").forEach(button => button.setAttribute("aria-pressed", String(button.dataset.area === id)));
    document.getElementById("selected-name").textContent = areas.get(id).name;
    openButton.disabled = disabled;
    openButton.setAttribute("aria-label", "Open " + areas.get(id).name + " page");
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
    areas = new Map((event.data.args.areas || []).map(area => [area.id, area]));
    const accent = event.data.args.accent;
    if (typeof accent === "string" && /^#[0-9a-f]{6}$/i.test(accent)) {
      document.documentElement.style.setProperty("--accent", accent);
    }
    disabled = Boolean(event.data.disabled);
    buildings.forEach(building => {
      const area = areas.get(building.dataset.area);
      if (!area) return;
      building.setAttribute("aria-label", "Open " + area.name + " page");
      building.querySelector("text").textContent = area.name;
    });
    mobileButtons.replaceChildren();
    areas.forEach(area => {
      const button = document.createElement("button");
      button.type = "button";
      button.dataset.area = area.id;
      button.textContent = area.name;
      button.disabled = disabled;
      button.addEventListener("click", () => selectArea(area.id));
      mobileButtons.appendChild(button);
    });
    if (selected) selectArea(selected);
    requestAnimationFrame(resize);
  });

  new ResizeObserver(resize).observe(document.querySelector(".map-shell"));
  send("streamlit:componentReady", {apiVersion: 1});
})();
