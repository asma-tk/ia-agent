// =====================
// Chat Bubble Functions
// =====================

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
