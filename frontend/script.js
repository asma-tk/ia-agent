// constants
const CHAT_STORAGE_KEY = "chat_messages_html";

// utility Functions
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

// chat Bubble Functions
function appendUserBubble(text) {
  const messages = getMessagesContainer();
  const div = document.createElement("div");
  div.className = "bubble-right";
  div.innerHTML = `<p>${escapeHtml(text)}</p>`;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
  saveChatState();
}

function appendBotBubble(text) {
  const messages = getMessagesContainer();
  const div = document.createElement("div");
  div.className = "bubble-left";
  div.innerHTML = `
    <img src="bot.png" class="bot-avatar" alt="bot">
    <div class="bubble-text"><p>${escapeHtml(text)}</p></div>
  `;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
  saveChatState();
}

function appendBotHtmlBubble(html) {
  const messages = getMessagesContainer();
  const div = document.createElement("div");
  div.className = "bubble-left";
  div.innerHTML = `
    <img src="bot.png" class="bot-avatar" alt="bot">
    <div class="bubble-text">${html}</div>
  `;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
  saveChatState();
}

function appendBotDownloadBubble(fileUrl, displayText) {
  const messages = getMessagesContainer();
  const div = document.createElement("div");
  div.className = "bubble-left";
  div.innerHTML = `
    <img src="bot.png" class="bot-avatar" alt="bot">
    <div class="bubble-text">
      <a href="#" class="download-link" data-filename="${fileUrl.replace('/files/', '')}">${displayText || "Download file"}</a>
    </div>
  `;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
  saveChatState();
}

function showAgentDownloadBubble(filename, displayText) {
  appendBotDownloadBubble(`/files/${filename}`, displayText || `Télécharger le fichier '${filename}'`);
}

function appendThinkingBubble() {
  const messages = getMessagesContainer();
  const div = document.createElement("div");
  div.className = "bubble-left bubble-thinking";
  div.innerHTML = `
    <img src="bot.png" class="bot-avatar" alt="bot">
    <div class="bubble-text thinking-text">
      <div class="thinking-row">
        <span class="thinking-spinner"></span>
        <p>Wait seconds, I'm thinking...</p>
      </div>
    </div>
  `;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
  return div;
}

// Main chat logic
function buildBotResultHtml(data) {
  const botMessage = data.response || data.message || "Action done.";
  const action = normalizeAction(data.action);

  let html = `<p>${escapeHtml(botMessage)}</p>`;

  if (action && action.action) {
    html += `<p><strong>Action:</strong> ${escapeHtml(action.action)}</p>`;
  }

  const fileActions = ["create_file", "writein_file", "deletein_file", "execute_regex"];
  if (action && fileActions.includes(action.action) && Array.isArray(action.params) && action.params[0]) {
    const fileName = String(action.params[0]);
    html += `
      <p><strong>File ${action.action === "create_file" ? "created" : "modified"}:</strong> ${escapeHtml(fileName)}</p>
      <p><a href="#" class="download-link" data-filename="${escapeHtml(fileName)}">Download ${escapeHtml(fileName)}</a></p>
    `;
  }

  return html;
}

// Make sendText available globally for the button onclick
// window.sendText = sendText;

// event Listeners
document.addEventListener("DOMContentLoaded", () => {
  restoreChatState();

  document.getElementById("txt").addEventListener("keydown", (e) => {
    if (e.key === "Enter") window.sendText();
  });

  const btn = document.getElementById("delete-chat-btn");
  if (btn) {
    btn.onclick = function () {
      const messages = getMessagesContainer();
      if (messages) {
        messages.innerHTML = `<div class="bubble-left"><img src="bot.png" class="bot-avatar" alt="bot"><div class="bubble-text"><p>Hi! What can I do for you?</p></div></div>`;
        localStorage.removeItem(CHAT_STORAGE_KEY);
      }
    };
  }
});

// Download link handler
document.addEventListener("click", function (e) {
  if (e.target && e.target.classList.contains("download-link")) {
    e.preventDefault();
    const filename = e.target.getAttribute("data-filename");
    if (filename) {
      triggerDownload(filename);
    }
  }
});