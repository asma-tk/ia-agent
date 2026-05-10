// main chat logic

function buildBotResultHtml(data) {
  // Get the human-friendly message from the bot
  const botMessage = data.agent_response || data.response || data.message || "Done!";
  
  // Normalize the action
  const action = normalizeAction(data.action);
  
  // Build HTML with just the message (no technical details)
  let html = `<p>${escapeHtml(botMessage)}</p>`;

  // Show download link for created or modified files
  const fileActions = ["create_file", "writein_file", "deletein_file", "img_create"];
  if (action && fileActions.includes(action.action) && Array.isArray(action.params) && action.params[0]) {
    const fileName = String(action.params[0]);
    html += `
      <p><a href="#" class="download-link" data-filename="${escapeHtml(fileName)}">📥 Download ${escapeHtml(fileName)}</a></p>
    `;
  }

  return html;
}

function appendThinkingBubble() {    // Append a "thinking" bubble to the chat to indicate that the bot is processing
  const messages = getMessagesContainer(); //
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
