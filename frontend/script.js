const CHAT_STORAGE_KEY = "chat_messages_html";

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

function appendUserBubble(text) {
  const messages = getMessagesContainer();
  const div = document.createElement("div");
  div.className = "bubble-right";
  div.innerHTML = `<p>${text}</p>`;
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
    <div class="bubble-text"><p>${text}</p></div>
  `;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
  saveChatState();
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\"/g, "&quot;")
    .replace(/'/g, "&#39;");
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

function createBlobDownloadLink(fileName) {
  const safeName = fileName || "created_file.txt";
  const blob = new Blob([""], { type: "text/plain" });
  const blobUrl = URL.createObjectURL(blob);
  return { url: blobUrl, fileName: safeName };
}

function buildBotResultHtml(data) {
  const botMessage = data.response || data.message || "Action done.";
  const action = normalizeAction(data.action);

  let html = `<p>${escapeHtml(botMessage)}</p>`;

  if (action && action.action) {
    html += `<p><strong>Action:</strong> ${escapeHtml(action.action)}</p>`;
  }

  if (action && action.action === "create_file" && Array.isArray(action.params) && action.params[0]) {
    const fileName = String(action.params[0]);
    const download = createBlobDownloadLink(fileName);
    html += `
      <p><strong>File created:</strong> ${escapeHtml(fileName)}</p>
      <p><a href="${download.url}" download="${escapeHtml(download.fileName)}">Download ${escapeHtml(fileName)}</a></p>
    `;
  }

  return html;
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

async function sendText() {
  const input = document.getElementById("txt");
  const button = document.querySelector("#answer-wrap button");
  const text = input.value.trim();
  if (text === "") return;

  appendUserBubble(text);
  input.value = "";
  input.disabled = true;
  button.disabled = true;
  const thinkingBubble = appendThinkingBubble();

  try {
    const data = await sendMessageToBackend(text);
    thinkingBubble.remove();
    const resultHtml = buildBotResultHtml(data);
    appendBotHtmlBubble(resultHtml);
  } catch (error) {
    thinkingBubble.remove();
    appendBotBubble(`Error: ${error.message}`);
  } finally {
    input.disabled = false;
    button.disabled = false;
    input.focus();
  }
}

document.addEventListener("DOMContentLoaded", () => {
  restoreChatState();
  document.getElementById("txt").addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendText();
  });
});

