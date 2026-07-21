/* =========================================================================
   admin.js — Admin panel mantiqi
   Barcha kod DOMContentLoaded ichida — DOM tayyor bo'lgandan keyin ishlaydi
   ========================================================================= */

document.addEventListener("DOMContentLoaded", function () {

const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];

/* ---- API ---- */
async function api(path, opts = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...opts,
  });
  if (res.status === 401) { showLogin(); throw new Error("unauthorized"); }
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || "Xatolik");
  return data;
}

/* ---- Toast ---- */
let toastTimer;
function toast(msg, type = "ok") {
  const el = $("#toast");
  if (!el) return;
  el.textContent = msg;
  el.className = "toast show " + type;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => (el.className = "toast"), 2800);
}

/* ---- Sxemalar ---- */
const CATEGORIES = ["Backend", "Data Engineering", "Tools & DevOps", "Frontend"];
const SCHEMAS = {
  skills: {
    title: "Ko'nikma",
    fields: [
      { k: "category", label: "Kategoriya", type: "select", options: CATEGORIES },
      { k: "name",     label: "Nomi",        type: "text" },
      { k: "level",    label: "Daraja (%)",  type: "number" },
      { k: "sort",     label: "Tartib",      type: "number" },
    ],
  },
  projects: {
    title: "Loyiha",
    fields: [
      { k: "title_uz", label: "Sarlavha (UZ)", type: "text" },
      { k: "title_en", label: "Sarlavha (EN)", type: "text" },
      { k: "desc_uz",  label: "Tavsif (UZ)", type: "textarea", full: true },
      { k: "desc_en",  label: "Tavsif (EN)", type: "textarea", full: true },
      { k: "tags",     label: "Teglar (vergul bilan)", type: "text", full: true },
      { k: "github",   label: "GitHub havola", type: "text" },
      { k: "demo",     label: "Demo havola",   type: "text" },
      { k: "featured", label: "Featured (tanlangan)", type: "checkbox" },
      { k: "sort",     label: "Tartib", type: "number" },
    ],
  },
  certificates: {
    title: "Sertifikat",
    fields: [
      { k: "title",  label: "Nomi",      type: "text", full: true },
      { k: "issuer", label: "Kim bergan", type: "text" },
      { k: "date",   label: "Sana",      type: "text" },
      { k: "url",    label: "Havola",    type: "text", full: true },
      { k: "sort",   label: "Tartib",    type: "number" },
    ],
  },
  experience: {
    title: "Tajriba",
    fields: [
      { k: "date_label_uz", label: "Sana (UZ)",     type: "text" },
      { k: "date_label_en", label: "Sana (EN)",     type: "text" },
      { k: "role_uz",       label: "Lavozim (UZ)",  type: "text" },
      { k: "role_en",       label: "Lavozim (EN)",  type: "text" },
      { k: "org",           label: "Tashkilot",     type: "text", full: true },
      { k: "points_uz",     label: "Tafsilotlar UZ (; bilan ajrating)", type: "textarea", full: true },
      { k: "points_en",     label: "Tafsilotlar EN (; bilan ajrating)", type: "textarea", full: true },
      { k: "sort",          label: "Tartib",        type: "number" },
    ],
  },
  blog: {
    title: "Blog post",
    fields: [
      { k: "title_uz",   label: "Sarlavha (UZ)",  type: "text" },
      { k: "title_en",   label: "Sarlavha (EN)",  type: "text" },
      { k: "slug",       label: "Slug",           type: "text", full: true },
      { k: "excerpt_uz", label: "Qisqacha (UZ)",  type: "textarea", full: true },
      { k: "excerpt_en", label: "Qisqacha (EN)",  type: "textarea", full: true },
      { k: "body_uz",    label: "Matn (UZ)",      type: "textarea", full: true },
      { k: "body_en",    label: "Matn (EN)",      type: "textarea", full: true },
      { k: "published",  label: "E'lon qilingan", type: "checkbox" },
      { k: "sort",       label: "Tartib",         type: "number" },
    ],
  },
};

const TAB_TITLES = {
  dashboard: "Dashboard", profile: "Profil", skills: "Ko'nikmalar",
  projects: "Loyihalar", certificates: "Sertifikatlar", experience: "Tajriba",
  blog: "Blog", messages: "Xabarlar", settings: "Sozlamalar",
};

/* ---- Login / Auth ko'rinish ---- */
function showLogin() {
  $("#loginView").removeAttribute("hidden");
  $("#appView").setAttribute("hidden", "");
}
function showApp() {
  $("#loginView").setAttribute("hidden", "");
  $("#appView").removeAttribute("hidden");
}

async function checkSession() {
  try {
    const d = await api("/api/admin/session");
    if (d.authenticated) { showApp(); initApp(); }
    else showLogin();
  } catch { showLogin(); }
}

/* ---- Login formasi ---- */
$("#loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  $("#loginError").textContent = "";
  const btn = e.target.querySelector("button[type=submit]");
  btn.disabled = true;
  btn.textContent = "Tekshirilmoqda...";
  try {
    await api("/api/admin/login", {
      method: "POST",
      body: JSON.stringify({
        username: $("#loginUser").value.trim(),
        password: $("#loginPass").value,
      }),
    });
    showApp();
    initApp();
  } catch (err) {
    $("#loginError").textContent = err.message || "Login yoki parol xato";
    btn.disabled = false;
    btn.textContent = "Kirish";
  }
});

/* ---- Logout ---- */
$("#logoutBtn").addEventListener("click", async () => {
  await api("/api/admin/logout", { method: "POST" }).catch(() => {});
  showLogin();
});

/* ---- Tab navigatsiya ---- */
let currentTab = "dashboard";

function initApp() {
  $$("#sideNav button").forEach((b) => {
    b.addEventListener("click", () => switchTab(b.dataset.tab));
  });
  $("#menuBtn").addEventListener("click", () => {
    $("#sidebar").classList.toggle("open");
  });
  loadAiStatus();
  loadMsgCount();
  switchTab("dashboard");
}

function switchTab(tab) {
  currentTab = tab;
  $$("#sideNav button").forEach((b) => b.classList.toggle("active", b.dataset.tab === tab));
  $("#pageTitle").textContent = TAB_TITLES[tab] || tab;
  $("#sidebar").classList.remove("open");
  renderTab(tab);
}

function loadAiStatus() {
  const el = $("#aiStatus");
  if (el) el.textContent = "⚡ Server ishlayapti";
}

async function loadMsgCount() {
  try {
    const msgs = await api("/api/admin/messages");
    const unread = msgs.filter((m) => !m.is_read).length;
    const el = $("#msgCount");
    if (el) el.textContent = unread || "";
  } catch {}
}

/* ---- Tab render ---- */
async function renderTab(tab) {
  const c = $("#content");
  c.innerHTML = `<div class="empty">Yuklanmoqda...</div>`;
  try {
    if (tab === "dashboard")   return await renderDashboard(c);
    if (tab === "profile")     return await renderProfile(c);
    if (tab === "messages")    return await renderMessages(c);
    if (tab === "settings")    return renderSettings(c);
    return await renderCrud(c, tab);
  } catch (e) {
    c.innerHTML = `<div class="empty">Xatolik: ${esc(e.message)}</div>`;
  }
}

/* ---- Dashboard ---- */
async function renderDashboard(c) {
  const [skills, projects, certs, exp, blog, msgs] = await Promise.all([
    api("/api/admin/skills"), api("/api/admin/projects"),
    api("/api/admin/certificates"), api("/api/admin/experience"),
    api("/api/admin/blog"), api("/api/admin/messages"),
  ]);
  const unread = msgs.filter((m) => !m.is_read).length;
  c.innerHTML = `
    <div class="welcome-card">
      <h3>Xush kelibsiz, Umrzoq! 👋</h3>
      <p>Portfolio saytingizning barcha ma'lumotlarini shu yerdan boshqarasiz.</p>
    </div>
    <div class="stat-grid">
      ${sb(projects.length,  "Loyihalar",       "projects")}
      ${sb(skills.length,    "Ko'nikmalar",     "skills")}
      ${sb(certs.length,     "Sertifikatlar",   "certificates")}
      ${sb(exp.length,       "Tajriba",         "experience")}
      ${sb(blog.length,      "Blog postlar",    "blog")}
      ${sb(unread,           "O'qilmagan xabar","messages")}
    </div>`;
  $$("[data-goto]", c).forEach((b) => (b.onclick = () => switchTab(b.dataset.goto)));
}
function sb(v, l, goto) {
  return `<div class="stat-box" data-goto="${goto}" style="cursor:pointer">
    <div class="sv">${v}</div><div class="sl">${l}</div></div>`;
}

/* ---- Generic CRUD ---- */
async function renderCrud(c, tab) {
  const schema = SCHEMAS[tab];
  const items = await api("/api/admin/" + tab);
  let listHtml;
  if (tab === "skills") {
    const groups = {};
    items.forEach((it) => { (groups[it.category] = groups[it.category] || []).push(it); });
    listHtml = Object.entries(groups).map(([cat, arr]) =>
      `<div class="cat-label">${esc(cat)}</div>
       <div class="card-list">${arr.map((it) => skillRow(it)).join("")}</div>`
    ).join("") || `<div class="empty">Hozircha yo'q</div>`;
  } else {
    listHtml = items.length
      ? `<div class="card-list">${items.map((it) => itemRow(tab, it)).join("")}</div>`
      : `<div class="empty">Hozircha yo'q. "Qo'shish" tugmasini bosing.</div>`;
  }
  c.innerHTML = `
    <div class="section-bar">
      <div><h3>${esc(schema.title)}lar</h3><p>Jami: ${items.length}</p></div>
      <button class="btn btn-primary" id="addBtn">+ Qo'shish</button>
    </div>
    ${listHtml}`;
  $("#addBtn", c).addEventListener("click", () => openModal(tab, null));
  bindRowActions(tab, c);
}

function skillRow(it) {
  return `<div class="item-card" data-id="${it.id}">
    <div class="item-main"><h4>${esc(it.name)}</h4><p>${esc(it.category)}</p></div>
    <div class="skill-level-bar"><span style="width:${it.level}%"></span></div>
    <span class="item-tag">${it.level}%</span>
    <div class="item-actions">
      <button class="icon-btn edit" data-id="${it.id}">✎</button>
      <button class="icon-btn del" data-id="${it.id}">🗑</button>
    </div></div>`;
}

function itemRow(tab, it) {
  let title = "", sub = "", tags = "";
  if (tab === "projects") {
    title = it.title_uz || it.title_en; sub = (it.desc_uz || "").slice(0, 80);
    if (it.featured) tags += `<span class="item-tag feat">★</span>`;
  } else if (tab === "certificates") {
    title = it.title; sub = (it.issuer || "") + (it.date ? " · " + it.date : "");
  } else if (tab === "experience") {
    title = it.role_uz || it.role_en; sub = (it.org || "") + " · " + (it.date_label_uz || "");
  } else if (tab === "blog") {
    title = it.title_uz || it.title_en; sub = it.excerpt_uz || "";
    tags += it.published ? `<span class="item-tag">E'lon</span>` : `<span class="item-tag unpub">Qoralama</span>`;
  }
  return `<div class="item-card" data-id="${it.id}">
    <div class="item-main"><h4>${esc(title)} ${tags}</h4><p>${esc(sub)}</p></div>
    <div class="item-actions">
      <button class="icon-btn edit" data-id="${it.id}">✎</button>
      <button class="icon-btn del" data-id="${it.id}">🗑</button>
    </div></div>`;
}

function bindRowActions(tab, c) {
  $$(".icon-btn.edit", c).forEach((b) => {
    b.addEventListener("click", async () => {
      try {
        const items = await api("/api/admin/" + tab);
        const item = items.find((x) => x.id == b.dataset.id);
        if (item) openModal(tab, item);
      } catch (e) { toast(e.message, "err"); }
    });
  });
  $$(".icon-btn.del", c).forEach((b) => {
    b.addEventListener("click", async () => {
      if (!confirm("O'chirilsinmi?")) return;
      try {
        await api(`/api/admin/${tab}/${b.dataset.id}`, { method: "DELETE" });
        toast("O'chirildi");
        renderTab(tab);
      } catch (e) { toast(e.message, "err"); }
    });
  });
}

/* ---- Modal ---- */
let modalTab = null, modalId = null;

function openModal(tab, item) {
  modalTab = tab;
  modalId = item ? item.id : null;
  const schema = SCHEMAS[tab];
  $("#modalTitle").textContent = (item ? "Tahrirlash — " : "Yangi — ") + schema.title;
  const form = $("#modalForm");
  form.innerHTML = schema.fields.map((f) => fieldHtml(f, item)).join("");
  $("#modalOverlay").removeAttribute("hidden");
}

function fieldHtml(f, item) {
  const val = item ? (item[f.k] != null ? item[f.k] : "") : (f.type === "number" ? (f.k === "level" ? 50 : 0) : "");
  const full = f.full ? "full" : "";
  if (f.type === "textarea") {
    return `<div class="field float ${full}">
      <textarea data-k="${f.k}" placeholder=" ">${esc(String(val))}</textarea>
      <label>${f.label}</label>
    </div>`;
  }
  if (f.type === "checkbox") {
    return `<div class="check-row ${full}">
      <input type="checkbox" data-k="${f.k}" id="cb_${f.k}" ${val ? "checked" : ""} />
      <label for="cb_${f.k}">${f.label}</label>
    </div>`;
  }
  if (f.type === "select") {
    const opts = f.options.map((o) => `<option ${o === String(val) ? "selected" : ""}>${esc(o)}</option>`).join("");
    return `<div class="field float ${full}">
      <select data-k="${f.k}">${opts}</select>
      <label>${f.label}</label>
    </div>`;
  }
  return `<div class="field float ${full}">
    <input type="${f.type}" data-k="${f.k}" value="${esc(String(val))}" placeholder=" " />
    <label>${f.label}</label>
  </div>`;
}

function closeModal() {
  $("#modalOverlay").setAttribute("hidden", "");
}

$("#modalClose").addEventListener("click", closeModal);
$("#modalCancel").addEventListener("click", closeModal);
$("#modalOverlay").addEventListener("click", (e) => {
  if (e.target === $("#modalOverlay")) closeModal();
});

$("#modalSave").addEventListener("click", async () => {
  const form = $("#modalForm");
  const data = {};
  $$("[data-k]", form).forEach((el) => {
    const k = el.dataset.k;
    if (el.type === "checkbox") data[k] = el.checked ? 1 : 0;
    else if (el.type === "number") data[k] = parseInt(el.value || "0", 10);
    else data[k] = el.value;
  });
  const btn = $("#modalSave");
  btn.disabled = true;
  btn.textContent = "Saqlanmoqda...";
  try {
    if (modalId) {
      await api(`/api/admin/${modalTab}/${modalId}`, { method: "PUT", body: JSON.stringify(data) });
    } else {
      await api(`/api/admin/${modalTab}`, { method: "POST", body: JSON.stringify(data) });
    }
    toast("Saqlandi ✓");
    closeModal();
    renderTab(modalTab);
  } catch (e) {
    toast(e.message, "err");
  } finally {
    btn.disabled = false;
    btn.textContent = "Saqlash";
  }
});

/* ---- Profil ---- */
async function renderProfile(c) {
  const p = await api("/api/admin/profile");

  function fld(k, label, type, full) {
    const val = p[k] != null ? String(p[k]) : "";
    const cls = full ? "full" : "";
    if (type === "textarea")
      return `<div class="field float ${cls}">
        <textarea data-k="${k}" placeholder=" ">${esc(val)}</textarea>
        <label>${label}</label>
      </div>`;
    return `<div class="field float ${cls}">
      <input type="${type || "text"}" data-k="${k}" value="${esc(val)}" placeholder=" " />
      <label>${label}</label>
    </div>`;
  }

  c.innerHTML = `
    <div class="section-bar">
      <div><h3>Profil</h3><p>Saytda ko'rinadigan asosiy ma'lumotlar</p></div>
      <button class="btn btn-primary" id="saveProfileBtn">Saqlash</button>
    </div>

    <!-- Rasm yuklash -->
    <div class="upload-card" id="uploadCard">
      <div class="upload-preview" id="uploadPreview">
        ${p.avatar
          ? `<img src="${esc(p.avatar)}" alt="avatar" />`
          : `<div class="upload-placeholder">📷</div>`}
      </div>
      <div class="upload-info">
        <strong>Profil rasmi</strong>
        <small>JPG, PNG, WEBP — max 10MB</small>
        <label class="btn btn-ghost btn-sm upload-label" style="cursor:pointer;margin-top:8px">
          📁 Rasm tanlash
          <input type="file" id="photoInput" accept="image/jpeg,image/png,image/webp,image/gif" style="display:none" />
        </label>
        <span id="uploadStatus" style="font-size:13px;margin-top:6px;display:block"></span>
      </div>
    </div>

    <form id="profileForm" class="form-grid">
      <div class="form-section-title">Asosiy</div>
      ${fld("name","Ism")}${fld("nickname","Nickname")}
      ${fld("role_uz","Lavozim (UZ)")}${fld("role_en","Lavozim (EN)")}
      ${fld("headline_uz","Bosh sarlavha (UZ)","text",true)}
      ${fld("headline_en","Bosh sarlavha (EN)","text",true)}
      ${fld("tagline_uz","Tagline (UZ)","text",true)}
      ${fld("tagline_en","Tagline (EN)","text",true)}
      ${fld("bio_uz","Bio (UZ)","textarea",true)}
      ${fld("bio_en","Bio (EN)","textarea",true)}
      <div class="form-section-title">Aloqa</div>
      ${fld("location_uz","Joylashuv (UZ)")}${fld("location_en","Joylashuv (EN)")}
      ${fld("email","Email")}${fld("phone","Telefon")}
      ${fld("github","GitHub","text",true)}
      ${fld("linkedin","LinkedIn","text",true)}
      ${fld("telegram","Telegram","text",true)}
      ${fld("resume_url","CV havola","text",true)}
      <div class="check-row full">
        <input type="checkbox" data-k="available" id="cb_available" ${p.available ? "checked" : ""} />
        <label for="cb_available">Open to work (Ishga tayyor)</label>
      </div>
    </form>`;

  // Rasm yuklash
  const photoInput = $("#photoInput", c);
  const uploadStatus = $("#uploadStatus", c);
  const uploadPreview = $("#uploadPreview", c);
  if (photoInput) {
    photoInput.addEventListener("change", async () => {
      const file = photoInput.files[0];
      if (!file) return;
      uploadStatus.textContent = "Yuklanmoqda...";
      uploadStatus.style.color = "var(--text-dim)";
      const form = new FormData();
      form.append("photo", file);
      try {
        const res = await fetch("/api/admin/upload", { method: "POST", body: form });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || "Xato");
        uploadStatus.textContent = "✓ Rasm saqlandi!";
        uploadStatus.style.color = "#4ade80";
        // Preview yangilash
        uploadPreview.innerHTML = `<img src="${data.url}?t=${Date.now()}" alt="avatar" />`;
        toast("Rasm yuklandi ✓");
      } catch (e) {
        uploadStatus.textContent = "✗ " + e.message;
        uploadStatus.style.color = "#f87171";
      }
    });
  }

  $("#saveProfileBtn", c).addEventListener("click", async () => {
    const data = {};
    $$("[data-k]", c).forEach((el) => {
      data[el.dataset.k] = el.type === "checkbox" ? (el.checked ? 1 : 0) : el.value;
    });
    try {
      await api("/api/admin/profile", { method: "PUT", body: JSON.stringify(data) });
      toast("Profil saqlandi ✓");
    } catch (e) { toast(e.message, "err"); }
  });
}

/* ---- Xabarlar ---- */
async function renderMessages(c) {
  const msgs = await api("/api/admin/messages");
  if (!msgs.length) {
    c.innerHTML = `<div class="section-bar"><div><h3>Xabarlar</h3></div></div><div class="empty">Hozircha xabar yo'q</div>`;
    return;
  }
  c.innerHTML = `
    <div class="section-bar"><div><h3>Kelgan xabarlar</h3><p>Jami: ${msgs.length}</p></div></div>
    <div class="card-list">
      ${msgs.map((m) => `
        <div class="msg-card ${m.is_read ? "" : "unread"}" data-id="${m.id}">
          <div class="msg-card-top">
            <strong>${esc(m.name)}</strong>
            <span class="msg-date">${(m.created_at || "").replace("T", " ")}</span>
          </div>
          ${m.email ? `<div class="msg-email">${esc(m.email)}</div>` : ""}
          <div class="msg-body">${esc(m.message)}</div>
          <div class="item-actions" style="margin-top:12px">
            ${!m.is_read ? `<button class="btn btn-sm btn-ghost read-btn" data-id="${m.id}">O'qildi</button>` : ""}
            ${m.email ? `<a class="btn btn-sm btn-ghost" href="mailto:${esc(m.email)}">Javob ✉</a>` : ""}
            <button class="btn btn-sm btn-danger del-btn" data-id="${m.id}">O'chirish</button>
          </div>
        </div>`).join("")}
    </div>`;

  $$(".read-btn", c).forEach((b) => {
    b.addEventListener("click", async () => {
      await api("/api/admin/messages/read", { method: "POST", body: JSON.stringify({ id: +b.dataset.id }) });
      loadMsgCount();
      renderTab("messages");
    });
  });
  $$(".del-btn", c).forEach((b) => {
    b.addEventListener("click", async () => {
      if (!confirm("O'chirilsinmi?")) return;
      await api(`/api/admin/messages/${b.dataset.id}`, { method: "DELETE" });
      toast("O'chirildi");
      loadMsgCount();
      renderTab("messages");
    });
  });
}

/* ---- Sozlamalar ---- */
function renderSettings(c) {
  c.innerHTML = `
    <div class="section-bar"><div><h3>Sozlamalar</h3></div></div>
    <form id="pwForm" style="max-width:440px; display:flex; flex-direction:column; gap:16px;">
      <div class="field float">
        <input type="password" id="newPass" placeholder=" " autocomplete="new-password" />
        <label>Yangi parol (min 6 belgi)</label>
      </div>
      <div class="field float">
        <input type="password" id="newPass2" placeholder=" " autocomplete="new-password" />
        <label>Parolni tasdiqlang</label>
      </div>
      <button type="submit" class="btn btn-primary">Parolni saqlash</button>
    </form>
    <div class="welcome-card" style="margin-top:26px; max-width:500px">
      <h3 style="font-size:1.1rem; margin-bottom:8px">💡 AI chatbot</h3>
      <p>To'liq AI uchun serverni shunday ishga tushiring:</p>
      <pre style="background:rgba(0,0,0,.3);padding:12px;border-radius:8px;margin-top:10px;font-size:13px;color:#22d3ee">export GROQ_API_KEY="gsk_..."
python3 app.py</pre>
      <p style="margin-top:8px">Bepul kalit: <a href="https://console.groq.com" target="_blank" style="color:#22d3ee">console.groq.com</a></p>
    </div>`;

  $("#pwForm", c).addEventListener("submit", async (e) => {
    e.preventDefault();
    const p1 = $("#newPass", c).value;
    const p2 = $("#newPass2", c).value;
    if (p1.length < 6) return toast("Parol kamida 6 belgi bo'lishi kerak", "err");
    if (p1 !== p2) return toast("Parollar mos kelmadi", "err");
    try {
      await api("/api/admin/password", { method: "POST", body: JSON.stringify({ new_password: p1 }) });
      toast("Parol o'zgartirildi ✓");
      e.target.reset();
    } catch (e2) { toast(e2.message, "err"); }
  });
}

/* ---- Util ---- */
function esc(s) {
  return String(s || "").replace(/[&<>"']/g, (m) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[m])
  );
}

/* ---- Start ---- */
checkSession();

}); // DOMContentLoaded
