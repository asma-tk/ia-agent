// =====================
// Main Chat Logic
// =====================

function buildBotResultHtml(data) {
  const botMessage = data.response || data.message || "Action done.";
  const action = normalizeAction(data.action);

  let html = `<p>${escapeHtml(botMessage)}</p>`;

  if (action && action.action) {
    html += `<p><strong>Action:</strong> ${escapeHtml(action.action)}</p>`;
  }

  if (action && action.action === "create_file" && Array.isArray(action.params) && action.params[0]) {
    const fileName = String(action.params[0]);
    html += `
      <p><strong>File created:</strong> ${escapeHtml(fileName)}</p>
      <p><a href="#" class="download-link" data-filename="${escapeHtml(fileName)}">Download ${escapeHtml(fileName)}</a></p>
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
