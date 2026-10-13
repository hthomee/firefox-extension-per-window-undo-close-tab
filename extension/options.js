"use strict";

const DAY_MS = 24 * 60 * 60 * 1000;
const INT32_MAX = 2147483647;
const DEFAULTS = { windows: 5, tabs: 25, days: 14 };

const sliders = {
  windows: document.getElementById("windows"),
  tabs: document.getElementById("tabs"),
  days: document.getElementById("days"),
};

function storeGet(key) {
  try {
    return localStorage.getItem(key);
  } catch (e) {
    return null; // storage may be unavailable
  }
}

function storeSet(key, value) {
  try {
    localStorage.setItem(key, value);
  } catch (e) {
    // not critical
  }
}

function loadValues() {
  let saved = {};
  try {
    saved = JSON.parse(storeGet("limits") || "{}");
  } catch (e) {
    saved = {};
  }
  for (const key of Object.keys(DEFAULTS)) {
    const value = Number(saved[key]);
    const slider = sliders[key];
    slider.value = Number.isFinite(value) && value >= slider.min && value <= slider.max ? value : DEFAULTS[key];
  }
}

function render() {
  const windows = Number(sliders.windows.value);
  const tabs = Number(sliders.tabs.value);
  const days = Number(sliders.days.value);
  const ms = Math.min(days * DAY_MS, INT32_MAX);
  const dayText = days + (days === 1 ? " day" : " days");

  document.getElementById("windows-out").textContent = windows;
  document.getElementById("tabs-out").textContent = tabs;
  document.getElementById("days-out").textContent = dayText;
  document.getElementById("v-windows").textContent = windows;
  document.getElementById("v-tabs").textContent = tabs;
  document.getElementById("v-days").textContent = ms;
  document.getElementById("v-days-text").textContent = dayText;

  storeSet("limits", JSON.stringify({ windows, tabs, days }));
}

for (const slider of Object.values(sliders)) {
  slider.addEventListener("input", render);
}

let toastTimer = null;
function toast(text) {
  const el = document.getElementById("toast");
  el.textContent = text;
  el.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => el.classList.remove("show"), 6000);
}

// Copy text to the clipboard. Needs a real user click; falls back to the older selection-based copy.
async function copyText(text) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (e) {
    const area = document.createElement("textarea");
    area.value = text;
    area.setAttribute("readonly", "");
    area.style.position = "fixed";
    area.style.opacity = "0";
    document.body.appendChild(area);
    area.select();
    let ok = false;
    try {
      ok = document.execCommand("copy");
    } catch (err) {
      ok = false;
    }
    area.remove();
    return ok;
  }
}

async function copyFromElement(codeEl) {
  const text = codeEl.textContent.trim();
  if (await copyText(text)) {
    toast(codeEl.classList.contains("about")
      ? text + " copied. Firefox does not let add-ons open about: pages. Paste it into the address bar of a new tab."
      : "Copied: " + text);
  } else {
    toast("Copy failed. Select the text and copy it manually.");
  }
}

// Firefox blocks add-ons from opening about: pages, so these addresses are copied instead of linked.
document.addEventListener("click", (event) => {
  const el = event.target.closest && event.target.closest("code.copy");
  if (el) {
    copyFromElement(el);
  }
});
document.addEventListener("keydown", (event) => {
  const el = event.target.closest && event.target.closest("code.copy");
  if (el && (event.key === "Enter" || event.key === " ")) {
    event.preventDefault();
    copyFromElement(el);
  }
});

for (const el of document.querySelectorAll("code.copy")) {
  el.title = "Click to copy";
  el.tabIndex = 0;
  el.setAttribute("role", "button");
}

try {
  document.getElementById("version").textContent = "Version " + browser.runtime.getManifest().version;
} catch (e) {
  // not critical
}

loadValues();
render();
