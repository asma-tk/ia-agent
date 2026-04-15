const BACKEND_CHAT_URL = "http://127.0.0.1:8001/chat";


async function sendMessageToBackend(userInput) {
   const response = await fetch(BACKEND_CHAT_URL, {
      method: "POST",
      headers: {
         "Content-Type": "application/json",
      },
      body: JSON.stringify({ user_input: userInput }),
   });

   const data = await response.json();

   if (!response.ok) {
      throw new Error(data.message || `HTTP ${response.status}`);
   }

   if (data.status === "error") {
      throw new Error(data.message || "Backend error");
   }

   return data;
}




