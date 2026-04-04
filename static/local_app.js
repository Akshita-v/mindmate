const chatList = document.getElementById("chatList");
const form = document.getElementById("chatForm");
const input = document.getElementById("messageInput");
const newSessionBtn = document.getElementById("newSessionBtn");
const sessionCards = document.querySelectorAll(".session-card[data-session-id]");

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function appendUserMessage(text) {
  chatList.insertAdjacentHTML(
    "beforeend",
    `<div class="message user"><div class="bubble">${escapeHtml(text)}</div></div>`
  );
}

function appendBotMessage(entry) {
  const result = entry.result || {};
  const meta = result.conversation_type === "emotional"
    ? `<div class="meta">Emotion: ${escapeHtml((result.emotion?.emotion || "neutral"))} | Stress: ${escapeHtml((result.stress?.level || "Low"))}</div>`
    : "";

  const response = escapeHtml(result.response || "I am here with you.").replaceAll("\n", "<br>");

  chatList.insertAdjacentHTML(
    "beforeend",
    `<div class="message bot"><div class="avatar">-</div><div class="bubble"><p>${response}</p>${meta}</div></div>`
  );
}

async function sendMessage(message) {
  const res = await fetch("/api/message", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message })
  });

  if (!res.ok) {
    throw new Error("Failed to send message");
  }

  return res.json();
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = input.value.trim();
  if (!message) return;

  appendUserMessage(message);
  input.value = "";
  input.focus();

  try {
    const entry = await sendMessage(message);
    appendBotMessage(entry);
    chatList.scrollTop = chatList.scrollHeight;
  } catch (error) {
    appendBotMessage({ result: { response: "Something went wrong. Please try again." } });
  }
});

newSessionBtn.addEventListener("click", async () => {
  await fetch("/api/new-session", { method: "POST" });
  window.location.reload();
});

sessionCards.forEach((card) => {
  card.addEventListener("click", async () => {
    if (card.classList.contains("active")) {
      return;
    }

    const sessionId = card.dataset.sessionId;
    if (!sessionId) {
      return;
    }

    await fetch("/api/switch-session", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId })
    });

    window.location.reload();
  });
});
