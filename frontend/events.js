// 
// event Listeners

//quand on clique sur entrer ou sur le bouton envoyer, on envoie le message au backend et on affiche la reponse du bot
document.addEventListener("DOMContentLoaded", () => {
  restoreChatState();
  document.getElementById("txt").addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendText();
  });
  const btn = document.getElementById("delete-chat-btn");
  if (btn) {
    btn.onclick = function() {
      const messages = getMessagesContainer();
      if (messages) {
        messages.innerHTML = `<div class=\"bubble-left\"><img src=\"bot.png\" class=\"bot-avatar\" alt=\"bot\"><div class=\"bubble-text\"><p>Hi! What can I do for you?</p></div></div>`;
        localStorage.removeItem(CHAT_STORAGE_KEY);
      }
    };
  }
});

// Listen for clicks on download links in chat bubbles and trigger download.js logic
document.addEventListener("click", function(e) {
  if (e.target && e.target.classList.contains("download-link")) {
    e.preventDefault();
    const filename = e.target.getAttribute("data-filename");
    if (filename) {
      triggerDownload(filename);
    }
  }
});
