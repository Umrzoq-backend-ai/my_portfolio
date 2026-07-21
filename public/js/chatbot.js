/* =========================================================================
   chatbot.js — AI yordamchi widget
   ========================================================================= */
(function () {
  const fab = document.getElementById("chatFab");
  const panel = document.getElementById("chatPanel");
  const form = document.getElementById("chatForm");
  const input = document.getElementById("chatText");
  const messagesEl = document.getElementById("chatMessages");
  const openBtn = document.getElementById("aiOpenBtn");
  if (!fab || !panel) return;

  const history = []; // {role, content}
  let greeted = false;

  const greetings = {
    uz: "Assalomu alaykum! 👋 Men Umrzoqning AI yordamchisiman. Uning ko'nikmalari, loyihalari yoki tajribasi haqida so'rashingiz mumkin.",
    en: "Hello! 👋 I'm Umrzoq's AI assistant. Ask me about his skills, projects, or experience.",
  };
  const suggestions = {
    uz: ["Qanday texnologiyalarni biladi?", "Loyihalari haqida ayt", "U ishga tayyormi?"],
    en: ["What technologies does he know?", "Tell me about his projects", "Is he open to work?"],
  };

  const lang = () => localStorage.getItem("lang") || "uz";

  function addMessage(role, text) {
    const div = document.createElement("div");
    div.className = "msg msg-" + role;
    div.innerHTML = `<div class="msg-bubble"></div>`;
    div.querySelector(".msg-bubble").textContent = text;
    messagesEl.appendChild(div);
    messagesEl.scrollTop = messagesEl.scrollHeight;
    return div;
  }

  function addSuggestions() {
    const wrap = document.createElement("div");
    wrap.className = "chat-suggestions";
    suggestions[lang()].forEach((s) => {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "chat-chip";
      b.textContent = s;
      b.addEventListener("click", () => { input.value = s; form.requestSubmit(); });
      wrap.appendChild(b);
    });
    messagesEl.appendChild(wrap);
  }

  function typingIndicator(show) {
    let el = document.getElementById("typing");
    if (show) {
      if (el) return;
      el = document.createElement("div");
      el.id = "typing";
      el.className = "msg msg-assistant";
      el.innerHTML = `<div class="msg-bubble typing"><span></span><span></span><span></span></div>`;
      messagesEl.appendChild(el);
      messagesEl.scrollTop = messagesEl.scrollHeight;
    } else if (el) {
      el.remove();
    }
  }

  function openPanel() {
    panel.classList.add("open");
    fab.classList.add("active");
    if (!greeted) {
      greeted = true;
      addMessage("assistant", greetings[lang()]);
      addSuggestions();
    }
    setTimeout(() => input.focus(), 200);
  }
  function closePanel() {
    panel.classList.remove("open");
    fab.classList.remove("active");
  }

  fab.addEventListener("click", () => {
    panel.classList.contains("open") ? closePanel() : openPanel();
  });
  if (openBtn) openBtn.addEventListener("click", () => {
    openPanel();
    panel.scrollIntoView({ behavior: "smooth" });
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;
    // suggestion chiplarni tozalash
    const sug = messagesEl.querySelector(".chat-suggestions");
    if (sug) sug.remove();

    addMessage("user", text);
    history.push({ role: "user", content: text });
    input.value = "";
    typingIndicator(true);

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: history }),
      });
      const data = await res.json();
      typingIndicator(false);
      const reply = data.reply || "…";
      addMessage("assistant", reply);
      history.push({ role: "assistant", content: reply });
    } catch (err) {
      typingIndicator(false);
      addMessage("assistant", lang() === "uz"
        ? "Uzr, xatolik yuz berdi. Qayta urinib ko'ring."
        : "Sorry, an error occurred. Please try again.");
    }
  });

  // Esc bilan yopish
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && panel.classList.contains("open")) closePanel();
  });
})();
