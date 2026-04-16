// =====================
// Utility Functions
// =====================

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function normalizeAction(actionValue) {
  if (!actionValue) return null;
  if (typeof actionValue === "object") return actionValue;
  if (typeof actionValue === "string") {
    try {
      return JSON.parse(actionValue);
    } catch {
      return null;
    }
  }
  return null;
}

function getMessagesContainer() {
  return document.getElementById("messages");
}

const CHAT_STORAGE_KEY = "chat_messages_html";

function saveChatState() {
  const messages = getMessagesContainer();
  if (!messages) return;
  const clone = messages.cloneNode(true);
  clone.querySelectorAll(".bubble-thinking").forEach((node) => node.remove());
  localStorage.setItem(CHAT_STORAGE_KEY, clone.innerHTML);
}

function restoreChatState() {
  const messages = getMessagesContainer();
  if (!messages) return;
  const saved = localStorage.getItem(CHAT_STORAGE_KEY);
  if (saved && saved.trim() !== "") {
    messages.innerHTML = saved;
  }
}
