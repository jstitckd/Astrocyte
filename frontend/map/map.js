/* Labels and descriptions come from models/areas.py. Artwork lives in index.html. */
(() => {
  "use strict";
  const buildings = [...document.querySelectorAll(".building[data-area]")];
  const touch = window.matchMedia("(hover: none)").matches;
  let areas = new Map();
  let selected = null;
  let disabled = false;

  function renderTasks(tasks) {
    const layer = document.getElementById("task-markers");
    layer.replaceChildren();
    document.getElementById("task-count").textContent = `${tasks.length} task${tasks.length === 1 ? "" : "s"} due`;
    buildings.forEach(building => building.classList.toggle("has-task", tasks.some(task => task.area === building.dataset.area)));
    tasks.forEach(task => {
      if (!areas.has(task.area)) return;
      const marker = document.createElement("button");
      marker.className = "task-marker task-" + task.area + (task.urgent ? " urgent" : "");
      marker.disabled = disabled;
      marker.setAttribute("aria-label", `${task.crew}: ${task.title}, due ${task.due}. View assigned tasks`);
      for (const [tag, text] of [["strong", `${task.crew} · ${task.title}`], ["span", task.detail], ["small", `Due ${task.due}`]]) {
        const line = document.createElement(tag);
        line.textContent = text;
        marker.append(line);
      }
      marker.addEventListener("click", () => {
        if (disabled) return;
        send("streamlit:setComponentValue", {value: {area: task.area, task: task.id, event_id: Date.now().toString(36) + "-" + Math.random().toString(36).slice(2)}, dataType: "json"});
      });
      layer.append(marker);
    });
  }

  // The map is an iframe. These messages are the bridge back to Streamlit.
  const send = (type, payload = {}) => window.parent.postMessage({isStreamlitMessage: true, type, ...payload}, "*");
  const resize = () => send("streamlit:setFrameHeight", {height: Math.ceil(document.querySelector(".map-shell").getBoundingClientRect().height) + 4});

  function selectArea(id) {
    const area = areas.get(id);
    if (!area) return;
    selected = id;
    buildings.forEach(building => building.classList.toggle("selected", building.dataset.area === id));
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

  window.addEventListener("message", event => {
    if (event.source !== window.parent || event.data?.type !== "streamlit:render") return;
    const args = event.data.args || {};
    areas = new Map((args.areas || []).map(area => [area.id, area]));
    disabled = Boolean(event.data.disabled);
    if (typeof args.background === "string" && /^#[0-9a-f]{6}$/i.test(args.background)) {
      document.documentElement.style.background = args.background;
    }
    if (typeof args.accent === "string" && /^#[0-9a-f]{6}$/i.test(args.accent)) {
      document.documentElement.style.setProperty("--accent", args.accent);
      document.documentElement.style.setProperty("--accent-soft", args.accent + "1f");
    }
    buildings.forEach(building => {
      const area = areas.get(building.dataset.area);
      building.setAttribute("aria-disabled", String(disabled || !area));
      if (!area) return;
      building.setAttribute("aria-label", "Open " + area.name + " page");
      building.setAttribute("aria-description", area.description);
      building.querySelector(".label-name").textContent = area.label;
      building.querySelector(".label-code").textContent = area.code;
    });
    const initial = selected && areas.has(selected) ? selected : (areas.has("living") ? "living" : areas.keys().next().value);
    renderTasks(Array.isArray(args.tasks) ? args.tasks : []);
    if (initial) selectArea(initial);
    requestAnimationFrame(resize);
  });

  if (touch) document.getElementById("map-instructions").textContent = "Tap a building to open its page";
  new ResizeObserver(() => requestAnimationFrame(resize)).observe(document.querySelector(".map-shell"));
  document.fonts.ready.then(resize);
  send("streamlit:componentReady", {apiVersion: 1});
})();
