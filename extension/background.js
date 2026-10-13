"use strict";

// Per-Window Undo Close Tab
// Reopens the most recently closed tab that belonged to the window the command was used in.
// sessions.restore() puts a tab back into the window it was closed from.
//
// Two commands run the same code. The second one asks for Firefox's own keys (Cmd+Shift+T on a Mac,
// Ctrl+Shift+T elsewhere). Firefox handles its own keys first, so that command only becomes active after
// the user has removed Firefox's shortcut in about:keyboard.
const COMMANDS = new Set(["undo-close-tab-in-this-window", "undo-close-tab-in-this-window-cmd"]);

async function reopenInWindow(windowId) {
  try {
    const closed = await browser.sessions.getRecentlyClosed(); // newest first, tabs and windows
    const candidates = closed.filter((s) => s.tab && s.tab.windowId === windowId);
    for (const candidate of candidates) {
      try {
        await browser.sessions.restore(candidate.tab.sessionId);
        return;
      } catch (error) {
        // This one could not be restored (for example it was forgotten in the meantime); try the next one.
        console.warn("Per-Window Undo Close Tab: could not restore", candidate.tab.sessionId, error);
      }
    }
  } catch (error) {
    console.error("Per-Window Undo Close Tab: could not read the closed tabs", error);
  }
}

browser.commands.onCommand.addListener(async (name, tab) => {
  if (!COMMANDS.has(name)) {
    return;
  }
  const windowId = tab ? tab.windowId : (await browser.windows.getLastFocused()).id;
  await reopenInWindow(windowId);
});
