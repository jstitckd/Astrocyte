/* Small, dependency-free Streamlit v1 component bridge. */
(() => {
  "use strict";
  let areas = new Map();
  let selected = null;
  let disabled = false;
  const regions = [...document.querySelectorAll("[data-area]")];
  const button = document.getElementById("open-dashboard");
  const mobileAreas = document.getElementById("mobile-areas");
  const touch = window.matchMedia("(hover: none)").matches;
  const send = (type, payload = {}) => window.parent.postMessage({isStreamlitMessage: true, type, ...payload}, "*");
  const resize = () => send("streamlit:setFrameHeight", {height: Math.ceil(document.documentElement.getBoundingClientRect().height)});

  function choose(id) {
    const area = areas.get(id);
    if (!area) return;
    selected = id;
    regions.forEach(region => {
      const active = region.dataset.area === id;
      region.classList.toggle("selected", active);
      region.setAttribute("aria-pressed", String(active));
    });
    mobileAreas.querySelectorAll("button").forEach(item => item.setAttribute("aria-pressed", String(item.dataset.id === id)));
    document.getElementById("preview-number").textContent = area.code;
    document.getElementById("preview-name").textContent = area.name;
    document.getElementById("preview-tasks").textContent = area.tasks.join(" · ");
    button.disabled = disabled;
    button.setAttribute("aria-label", "Open " + area.name + " dashboard");
    requestAnimationFrame(resize);
  }

  function open(id) {
    if (disabled || !areas.has(id)) return;
    send("streamlit:setComponentValue", {value: {area: id, event_id: Date.now().toString(36) + "-" + Math.random().toString(36).slice(2)}, dataType: "json"});
  }

  regions.forEach(region => {
    const id = region.dataset.area;
    region.addEventListener("mouseenter", () => { if (!touch) choose(id); });
    region.addEventListener("focus", () => { if (!touch) choose(id); });
    region.addEventListener("click", event => {
      // Touch previews before navigating; the prominent button is the next action.
      if (touch && event.detail !== 0) { choose(id); return; }
      open(id);
    });
    region.addEventListener("keydown", event => {
      if (event.key === "Enter" || event.key === " ") { event.preventDefault(); choose(id); open(id); }
    });
  });
  button.addEventListener("click", () => open(selected));
  window.addEventListener("message", event => {
    if (event.source !== window.parent || event.data?.type !== "streamlit:render") return;
    const args = event.data.args || {};
    areas = new Map((args.areas || []).map(area => [area.id, area]));
    disabled = Boolean(event.data.disabled);
    mobileAreas.replaceChildren();
    areas.forEach(area => {
      const item = document.createElement("button");
      item.type = "button";
      item.dataset.id = area.id;
      item.textContent = area.code + "  " + area.name;
      item.disabled = disabled;
      item.addEventListener("click", () => choose(area.id));
      mobileAreas.appendChild(item);
    });
    if (selected && areas.has(selected)) choose(selected);
    else if (args.selected && areas.has(args.selected)) choose(args.selected);
    requestAnimationFrame(resize);
  });
  if (touch) document.getElementById("hint").textContent = "Tap a building, then Open dashboard";
  new ResizeObserver(resize).observe(document.querySelector(".map-shell"));
  window.addEventListener("load", resize);
  send("streamlit:componentReady", {apiVersion: 1});
})();
