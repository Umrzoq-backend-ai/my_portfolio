/* =========================================================================
   main.js — Portfolio public sayt mantiqi
   ========================================================================= */

// ---- i18n lug'at (statik matnlar) ----
const I18N = {
  uz: {
    brandRole: "Backend Engineer",
    navHome: "Bosh sahifa", navProjects: "Loyihalar", navCerts: "Sertifikatlar",
    navResume: "Tajriba", navAI: "AI", navBlog: "Blog", navAbout: "Bog'lanish",
    navContact: "Bog'lanish",
    heroOpen: "Ishga tayyor",
    heroCta1: "Loyihalarni ko'rish", heroCta2: "Bog'lanish", heroCv: "Bog'lanish",
    statProjects: "Loyihalar", statExp: "Yil tajriba", statStack: "Tech Stack",
    skillsTag: "01 — Ko'nikmalar", skillsTitle: "Ko'nikmalar & Texnologiyalar", skillsSub: "Texnologiyalar bo'yicha darajam",
    projectsTag: "02 — Loyihalar", projectsTitle: "Loyihalar", projectsSub: "Men qurgan loyihalar",
    certsTag: "03 — Sertifikatlar", certsTitle: "Sertifikatlar",
    expTag: "04 — Tajriba", expTitle: "Tajriba & Ta'lim",
    aiTag: "AI", aiTitle: "Umrzoq AI ga so'rang", aiSub: "Ko'nikmalar, loyihalar va tajriba haqida so'rang.", aiOpen: "AI bilan suhbat",
    blogTag: "05 — Blog", blogTitle: "Blog",
    contactTag: "06 — Bog'lanish", contactTitle: "Bog'lanish", contactSub: "Savollaringiz bormi? Bog'laning!",
    formName: "Ismingiz", formEmail: "Email", formMessage: "Xabaringiz", formSend: "Yuborish",
    footerMade: "Python & ❤️ bilan qurilgan",
    chatOnline: "Onlayn — savol bering", chatPlaceholder: "Savolingizni yozing...",
    available: "Ishga tayyor", notAvailable: "Hozircha band",
    readMore: "Batafsil", sending: "Yuborilmoqda...", sent: "Xabaringiz yuborildi. Rahmat!", sendErr: "Xatolik. Qayta urinib ko'ring.",
    emailLabel: "Email", phoneLabel: "Telefon", githubLabel: "GitHub", linkedinLabel: "LinkedIn",
  },
  en: {
    brandRole: "Backend Engineer",
    navHome: "Home", navProjects: "Projects", navCerts: "Certificates",
    navResume: "Experience", navAI: "AI", navBlog: "Blog", navAbout: "Contact",
    navContact: "Contact",
    heroOpen: "Open to work",
    heroCta1: "View Projects", heroCta2: "Contact Me", heroCv: "Contact Me",
    statProjects: "Projects", statExp: "Years Exp.", statStack: "Tech Stack",
    skillsTag: "01 — Skills", skillsTitle: "Skills & Expertise", skillsSub: "My proficiency across technologies",
    projectsTag: "02 — Projects", projectsTitle: "Projects", projectsSub: "Projects I've built",
    certsTag: "03 — Certificates", certsTitle: "Certificates",
    expTag: "04 — Experience", expTitle: "Experience & Education",
    aiTag: "AI", aiTitle: "Ask Umrzoq AI", aiSub: "Ask about skills, projects and experience.", aiOpen: "Chat with AI",
    blogTag: "05 — Blog", blogTitle: "Blog",
    contactTag: "06 — Contact", contactTitle: "Contact Me", contactSub: "Got a question? Reach out!",
    formName: "Your name", formEmail: "Email", formMessage: "Your message", formSend: "Send",
    footerMade: "Built with Python & ❤️",
    chatOnline: "Online — ask me", chatPlaceholder: "Type your question...",
    available: "Open to work", notAvailable: "Currently busy",
    readMore: "Read more", sending: "Sending...", sent: "Your message was sent. Thanks!", sendErr: "Error. Please try again.",
    emailLabel: "Email", phoneLabel: "Phone", githubLabel: "GitHub", linkedinLabel: "LinkedIn",
  },
};

// SVG ikonlar
const ICONS = {
  server: '<svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="7" rx="2"/><rect x="3" y="13" width="18" height="7" rx="2"/><path d="M7 7.5h.01M7 16.5h.01"/></svg>',
  database: '<svg viewBox="0 0 24 24"><ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v6c0 1.7 3.6 3 8 3s8-1.3 8-3V5M4 11v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/></svg>',
  wrench: '<svg viewBox="0 0 24 24"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.4l-6 6 2.7 2.7 6-6a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.7-2.7 2.5-2.5z"/></svg>',
  code: '<svg viewBox="0 0 24 24"><path d="M16 18l6-6-6-6M8 6l-6 6 6 6"/></svg>',
  folder: '<svg viewBox="0 0 24 24"><path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg>',
  award: '<svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="6"/><path d="M8.2 13.9L7 22l5-3 5 3-1.2-8.1"/></svg>',
  github: '<svg viewBox="0 0 24 24"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.9a3.4 3.4 0 0 0-.9-2.6c3-.3 6.2-1.5 6.2-6.7A5.2 5.2 0 0 0 20 4.8a4.9 4.9 0 0 0-.1-3.6s-1.2-.3-3.9 1.5a13.4 13.4 0 0 0-7 0C6.3.9 5.1 1.2 5.1 1.2A4.9 4.9 0 0 0 5 4.8a5.2 5.2 0 0 0-1.4 3.6c0 5.2 3.2 6.4 6.2 6.7a3.4 3.4 0 0 0-.9 2.6V22"/></svg>',
  linkedin: '<svg viewBox="0 0 24 24"><path d="M16 8a6 6 0 0 1 6 6v6h-4v-6a2 2 0 0 0-4 0v6h-4v-6a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg>',
  telegram: '<svg viewBox="0 0 24 24"><path d="M22 2L2 10l6 2 2 7 3-4 5 4z"/></svg>',
  instagram: '<svg viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>',
  external: '<svg viewBox="0 0 24 24"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14L21 3"/></svg>',
  mail: '<svg viewBox="0 0 24 24"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 6l-10 7L2 6"/></svg>',
  phone: '<svg viewBox="0 0 24 24"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3.1-8.6A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>',
};
const CAT_ICON = { "Backend": "server", "Data Engineering": "database", "Tools & DevOps": "wrench", "Frontend": "code" };

let LANG = localStorage.getItem("lang") || "en";
let DATA = null;

const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];

// ---- API ----
async function loadData() {
  const res = await fetch("/api/portfolio");
  if (!res.ok) throw new Error("API xato");
  return res.json();
}

// ---- i18n qo'llash ----
function applyStaticI18n() {
  const dict = I18N[LANG];
  $$("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    if (dict[key] != null) {
      // ikonli buttonlarda faqat matn tugunini yangilash
      const iconChild = el.querySelector("svg");
      if (iconChild) {
        el.childNodes.forEach((n) => { if (n.nodeType === 3) n.textContent = ""; });
        el.insertBefore(document.createTextNode(dict[key] + " "), el.firstChild);
      } else {
        el.textContent = dict[key];
      }
    }
  });
  $$("[data-i18n-ph]").forEach((el) => {
    const key = el.getAttribute("data-i18n-ph");
    if (dict[key] != null) el.placeholder = dict[key];
  });
  document.documentElement.lang = LANG;
  $(".lang-current").textContent = LANG.toUpperCase();
}

const t = (key) => I18N[LANG][key] || key;
const L = (obj, base) => obj[base + "_" + LANG] || obj[base + "_uz"] || obj[base + "_en"] || "";

// ---- Render ----
function renderAll() {
  if (!DATA) return;
  applyStaticI18n();
  renderHero();
  renderSkills();
  renderProjects();
  renderCerts();
  renderExperience();
  renderBlog();
  renderContact();
  initAiInline();
  initReveal();
}

function renderHero() {
  const p = DATA.profile;

  // Subtitle
  const sub = document.getElementById("heroSub");
  if (sub) sub.textContent = L(p, "tagline") ||
    "Junior developer focused on Backend & Data Engineering";

  // Socials
  const socialsEl = document.getElementById("heroSocials");
  if (socialsEl) {
    const socials = [];
    if (p.github) socials.push(["github", p.github]);
    if (p.linkedin) socials.push(["linkedin", p.linkedin]);
    if (p.telegram && p.telegram !== "https://t.me/") socials.push(["telegram", p.telegram]);
    if (p.instagram) socials.push(["instagram", p.instagram]);
    if (p.email) socials.push(["mail", "mailto:" + p.email]);
    socialsEl.innerHTML = socials
      .map(([ic, url]) => `<a href="${url}" target="_blank" rel="noopener" aria-label="${ic}">${ICONS[ic]}</a>`)
      .join("");
  }

  // Profile section
  const codeRole = document.getElementById("profileCodeRole");
  if (codeRole) {
    const role = (p.role_en || "JUNIOR BACKEND & DATA ENGINEER").toUpperCase().replace(/ /g,"_");
    codeRole.textContent = `[${role}]`;
  }
  const bioEl = document.getElementById("profileBio");
  if (bioEl) bioEl.textContent = L(p, "bio") ||
    "I specialize in backend architecture and data engineering pipelines. Building reliable systems with clean code and clear architecture.";

  // Profile stats
  const statsEl = document.getElementById("profileStats");
  if (statsEl) {
    const svgs = {
      folder:    '<svg viewBox="0 0 24 24"><path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg>',
      briefcase: '<svg viewBox="0 0 24 24"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-4 0v2M8 7V5a2 2 0 0 0-4 0v2"/></svg>',
      code:      '<svg viewBox="0 0 24 24"><path d="M16 18l6-6-6-6M8 6l-6 6 6 6"/></svg>',
    };
    const stats = [
      { icon: "folder",    v: DATA.projects.length + "+", l: { uz: "Loyihalar", en: "Projects" } },
      { icon: "briefcase", v: DATA.experience.length + "+", l: { uz: "Tajriba yil", en: "Years Exp." } },
      { icon: "code",      v: DATA.skills.filter(s=>s.level>=60).length + "+", l: { uz: "Tech Stack", en: "Tech Stack" } },
    ];
    statsEl.innerHTML = stats.map(s => `
      <div class="pstat">
        ${svgs[s.icon]}
        <span class="pstat-v">${s.v}</span>
        <span class="pstat-l">${s.l[LANG]}</span>
      </div>`).join("");
  }

  // Terminal location
  const termLoc = document.getElementById("heroTerminalLoc");
  if (termLoc) {
    const loc = (p.location_en || "JIZZAKH, UZ").toUpperCase();
    termLoc.textContent = `LOC: ${loc}`;
  }

  // Rasm
  const frame = document.getElementById("heroPhotoFrame");
  const placeholder = document.getElementById("heroPhotoPlaceholder");
  if (frame && p.avatar) {
    const img = document.createElement("img");
    img.src = p.avatar;
    img.alt = p.name || "Umrzoq";
    img.onerror = () => {};
    if (placeholder) placeholder.style.display = "none";
    frame.insertBefore(img, frame.firstChild);
  }
}

function renderAbout() {
  const p = DATA.profile;
  const card = $("#aboutCard");
  if (!card) return;

  const stats = [
    { v: DATA.projects.length + "+", l: { uz: "Loyihalar", en: "Projects"}, icon: "📁" },
    { v: DATA.experience.length + "+", l: { uz: "Tajriba", en: "Experience"}, icon: "💼" },
    { v: (DATA.skills.filter(s=>s.level>=70).length) + "+", l: { uz: "Texnologiyalar", en: "Tech Stack"}, icon: "⚡" },
  ];

  const availHtml = p.available
    ? `<span class="badge-available"><span class="dot"></span>${t("available")}</span>`
    : "";

  card.innerHTML = `
    <div class="about-avatar-wrap">
      <div class="about-avatar">🧑‍💻</div>
      <div class="about-avatar-status"></div>
    </div>
    <div class="about-body">
      <div class="about-name">${p.name || "Umrzoq Yulchiyev"}</div>
      <div class="about-tagline">${L(p,"tagline")} ${availHtml}</div>
      <div class="about-stat-row">
        ${stats.map(s=>`
          <div class="about-stat-item">
            <div class="sv">${s.icon} ${s.v}</div>
            <div class="sl">${s.l[LANG]}</div>
          </div>`).join("")}
      </div>
      <div class="about-bio">${L(p,"bio")}</div>
    </div>`;
}

function renderSkills() {
  const cats = {};
  DATA.skills.forEach((s) => { (cats[s.category] = cats[s.category] || []).push(s); });
  $("#skillsGrid").innerHTML = Object.entries(cats)
    .map(([cat, items]) => `
      <div class="skill-cat">
        <div class="skill-cat-head">
          <div class="skill-cat-icon">${ICONS[CAT_ICON[cat] || "code"]}</div>
          <h3>${cat}</h3>
        </div>
        ${items.map((s) => `
          <div class="skill-item">
            <div class="skill-item-top"><span>${s.name}</span><span>${s.level}%</span></div>
            <div class="skill-bar"><div class="skill-fill" data-level="${s.level}"></div></div>
          </div>`).join("")}
      </div>`).join("");
}

function renderProjects() {
  $("#projectsGrid").innerHTML = DATA.projects
    .map((pr) => {
      const tags = (pr.tags || "").split(",").filter(Boolean)
        .map((tag) => `<span class="tag">${tag.trim()}</span>`).join("");
      const links = [];
      if (pr.github) links.push(`<a href="${pr.github}" target="_blank" rel="noopener" aria-label="github">${ICONS.github}</a>`);
      if (pr.demo) links.push(`<a href="${pr.demo}" target="_blank" rel="noopener" aria-label="demo">${ICONS.external}</a>`);
      return `
        <div class="project-card">
          ${pr.featured ? `<span class="featured-badge">★</span>` : ""}
          <div class="project-top">
            <div class="project-icon">${ICONS.folder}</div>
            <div class="project-links">${links.join("")}</div>
          </div>
          <h3>${L(pr, "title")}</h3>
          <p>${L(pr, "desc")}</p>
          <div class="project-tags">${tags}</div>
        </div>`;
    }).join("");
}

function renderCerts() {
  if (!DATA.certificates.length) { const s = $("#certificates"); if(s) s.style.display = "none"; return; }
  $("#certsGrid").innerHTML = DATA.certificates.map((c, i) => {
    const imgPart = c.image
      ? `<div class="cert-img-wrap">
           <img src="${c.image}" alt="${c.title}" loading="lazy" />
           <div class="cert-img-overlay"></div>
         </div>`
      : `<div class="cert-no-img">${["🏆","🎓","📜","⭐","🥇","🎯"][i%6]}</div>`;
    return `
      <div class="cert-card">
        ${imgPart}
        <div class="cert-body">
          <div class="cert-icon">${ICONS.award}</div>
          <div>
            <h3>${c.title}</h3>
            <div class="cert-issuer">${c.issuer || ""}</div>
            ${c.date ? `<div class="cert-date">${c.date}</div>` : ""}
            ${c.url ? `<a class="cert-link" href="${c.url}" target="_blank" rel="noopener">${t("readMore")}</a>` : ""}
          </div>
        </div>
      </div>`;
  }).join("");
}

function renderExperience() {
  $("#timeline").innerHTML = DATA.experience
    .map((e) => {
      const points = (L(e, "points") || "").split(";").filter(Boolean)
        .map((pt) => `<li>${pt.trim()}</li>`).join("");
      return `
        <div class="tl-item">
          <div class="tl-date">${L(e, "date_label")}</div>
          <h3>${L(e, "role")}</h3>
          <div class="tl-org">${e.org || ""}</div>
          <ul class="tl-points">${points}</ul>
        </div>`;
    }).join("");
}

function renderBlog() {
  if (!DATA.blog || !DATA.blog.length) {
    const sec = $("#blog");
    if (sec) sec.style.display = "none";
    return;
  }
  const grid = $("#blogGrid");
  if (!grid) return;
  grid.innerHTML = DATA.blog.map((b, i) => {
    const date = (b.created_at || "").split(" ")[0];
    const title = L(b, "title") || b.title_en || b.title_uz || "";
    const excerpt = L(b, "excerpt") || b.excerpt_en || b.excerpt_uz || "";
    const isTg = b.telegram_msg_id;
    const imgWrap = b.image
      ? `<div class="blog-img-wrap">
           <img src="${b.image}" alt="${title}" loading="lazy" />
           <div class="blog-img-overlay"></div>
           ${isTg ? `<span class="blog-tg-badge"><svg viewBox="0 0 24 24"><path d="M9.78 18.65l.28-4.23 7.68-6.92c.34-.31-.07-.46-.52-.19L7.74 13.3 3.64 12c-.88-.25-.89-.86.2-1.3l15.97-6.16c.73-.33 1.43.18 1.15 1.3l-2.72 12.81c-.19.91-.74 1.13-1.5.71L12.6 16.3l-1.99 1.93c-.23.23-.42.42-.83.42z"/></svg>Telegram</span>`:""}
         </div>`
      : `<div class="blog-no-img">
           ${isTg ? "📱" : ["📝","💡","🔧","🚀","📊","⚡"][i%6]}
           ${isTg ? `<span class="blog-tg-badge" style="top:8px;right:8px"><svg viewBox="0 0 24 24"><path d="M9.78 18.65l.28-4.23 7.68-6.92c.34-.31-.07-.46-.52-.19L7.74 13.3 3.64 12c-.88-.25-.89-.86.2-1.3l15.97-6.16c.73-.33 1.43.18 1.15 1.3l-2.72 12.81c-.19.91-.74 1.13-1.5.71L12.6 16.3l-1.99 1.93c-.23.23-.42.42-.83.42z"/></svg>Telegram</span>`:""}
         </div>`;
    return `
      <div class="blog-card reveal" data-blog-id="${b.id}" style="--i:${i}">
        ${imgWrap}
        <div class="blog-body">
          <div class="blog-meta">
            <span class="blog-date">${date}</span>
            ${isTg ? `<span class="blog-tag">Telegram</span>` : `<span class="blog-tag">Blog</span>`}
          </div>
          <h3>${title}</h3>
          <p>${excerpt}</p>
          <div class="blog-footer">
            <span class="blog-read">
              ${t("readMore")}
              <svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
            </span>
          </div>
        </div>
      </div>`;
  }).join("");

  // Click → modal ochish
  $$(".blog-card[data-blog-id]").forEach((card) => {
    card.addEventListener("click", () => {
      const id = parseInt(card.dataset.blogId);
      const b = DATA.blog.find((x) => x.id === id);
      if (b) openBlogModal(b);
    });
  });
}

// ---- Blog modal ----
function openBlogModal(b) {
  let overlay = document.getElementById("blogModalOverlay");
  if (!overlay) {
    overlay = document.createElement("div");
    overlay.id = "blogModalOverlay";
    overlay.className = "blog-modal-overlay";
    overlay.innerHTML = `
      <div class="blog-modal" id="blogModal">
        <img id="blogModalImg" class="blog-modal-img" src="" alt="" style="display:none"/>
        <div class="blog-modal-content">
          <div class="blog-modal-head">
            <h2 id="blogModalTitle"></h2>
            <button class="blog-modal-close" id="blogModalClose">✕</button>
          </div>
          <div class="blog-modal-meta" id="blogModalMeta"></div>
          <div class="blog-modal-body" id="blogModalBody"></div>
          <div id="blogModalTgLink"></div>
        </div>
      </div>`;
    document.body.appendChild(overlay);
    overlay.addEventListener("click", (e) => { if (e.target === overlay) closeBlogModal(); });
    document.getElementById("blogModalClose").addEventListener("click", closeBlogModal);
    document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeBlogModal(); });
  }

  const title = L(b, "title") || "";
  const body  = L(b, "body")  || L(b, "excerpt") || "";
  const date  = (b.created_at || "").split(" ")[0];

  document.getElementById("blogModalTitle").textContent = title;
  document.getElementById("blogModalMeta").textContent = date + (b.telegram_msg_id ? " · Telegram" : " · Blog");
  document.getElementById("blogModalBody").textContent = body;

  const imgEl = document.getElementById("blogModalImg");
  if (b.image) { imgEl.src = b.image; imgEl.alt = title; imgEl.style.display = "block"; }
  else imgEl.style.display = "none";

  const tgDiv = document.getElementById("blogModalTgLink");
  if (b.telegram_msg_id) {
    tgDiv.innerHTML = `<a class="blog-modal-tg-link" href="https://t.me/Umrzoq_dev/${b.telegram_msg_id}" target="_blank" rel="noopener">
      <svg viewBox="0 0 24 24" width="18" height="18" fill="#29b6f6"><path d="M9.78 18.65l.28-4.23 7.68-6.92c.34-.31-.07-.46-.52-.19L7.74 13.3 3.64 12c-.88-.25-.89-.86.2-1.3l15.97-6.16c.73-.33 1.43.18 1.15 1.3l-2.72 12.81c-.19.91-.74 1.13-1.5.71L12.6 16.3l-1.99 1.93c-.23.23-.42.42-.83.42z"/></svg>
      Telegram'da ko'rish
    </a>`;
  } else { tgDiv.innerHTML = ""; }

  overlay.classList.add("open");
  document.body.style.overflow = "hidden";
}

function closeBlogModal() {
  const ov = document.getElementById("blogModalOverlay");
  if (ov) ov.classList.remove("open");
  document.body.style.overflow = "";
}

function renderContact() {
  const p = DATA.profile;
  const lines = [];
  if (p.email) lines.push(["mail", t("emailLabel"), p.email, "mailto:" + p.email]);
  if (p.phone && !p.phone.includes("00 000")) lines.push(["phone", t("phoneLabel"), p.phone, "tel:" + p.phone.replace(/\s/g, "")]);
  if (p.github) lines.push(["github", t("githubLabel"), p.github.replace("https://", ""), p.github]);
  if (p.linkedin) lines.push(["linkedin", t("linkedinLabel"), "LinkedIn", p.linkedin]);
  $("#contactInfo").innerHTML = lines
    .map(([ic, label, val, url]) => `
      <a class="contact-line" href="${url}" target="_blank" rel="noopener">
        <div class="ci-icon">${ICONS[ic]}</div>
        <div><small>${label}</small><strong>${val}</strong></div>
      </a>`).join("");
}

// ---- AI inline bo'lim — hero ichidagi mini chat ----
let aiInlineHistory = [];
let aiInlineGreeted = false;

function initAiInline() {
  const form = document.getElementById("heroAiForm");
  const input = document.getElementById("heroAiInput");
  const msgsEl = document.getElementById("heroAiMsgs");
  if (!form || !msgsEl) return;

  // Birinchi marta greeting
  if (!aiInlineGreeted) {
    aiInlineGreeted = true;
    addHeroAiMsg("bot", LANG === "uz"
      ? "Salom! 👋 Ko'nikmalar, loyihalar yoki tajriba haqida so'rang."
      : "Hi! 👋 Ask me about skills, projects or experience.");
  }

  form.onsubmit = async (e) => {
    e.preventDefault();
    const text = (input.value || "").trim();
    if (!text) return;
    addHeroAiMsg("user", text);
    aiInlineHistory.push({ role: "user", content: text });
    input.value = "";
    const typingEl = addHeroAiTyping();
    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: aiInlineHistory }),
      });
      const data = await res.json();
      typingEl.remove();
      const reply = data.reply || "...";
      addHeroAiMsg("bot", reply);
      aiInlineHistory.push({ role: "assistant", content: reply });
    } catch {
      typingEl.remove();
      addHeroAiMsg("bot", LANG === "uz" ? "Xatolik yuz berdi." : "An error occurred.");
    }
  };

  function addHeroAiMsg(role, text) {
    const div = document.createElement("div");
    div.className = `hero-ai-msg hero-ai-msg-${role === "user" ? "user" : "bot"}`;
    div.innerHTML = `<div class="hero-ai-bubble">${text}</div>`;
    msgsEl.appendChild(div);
    msgsEl.scrollTop = msgsEl.scrollHeight;
    return div;
  }

  function addHeroAiTyping() {
    const div = document.createElement("div");
    div.className = "hero-ai-msg hero-ai-msg-bot";
    div.innerHTML = `<div class="hero-ai-bubble"><span style="opacity:.5">···</span></div>`;
    msgsEl.appendChild(div);
    msgsEl.scrollTop = msgsEl.scrollHeight;
    return div;
  }
}

// ---- Reveal on scroll — progressive disclosure ----
let revealObserver;
function initReveal() {
  if (revealObserver) revealObserver.disconnect();

  // Har bir kartaga --i CSS variable qo'yish (stagger uchun)
  [".project-card", ".cert-card", ".blog-card", ".skill-cat", ".stat-card"].forEach((sel) => {
    $$(sel).forEach((el, i) => {
      el.style.setProperty("--i", i);
      el.classList.add("reveal");
    });
  });

  revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("in");
        // skill barlarni to'ldirish
        $$(".skill-fill", entry.target).forEach((f) => {
          setTimeout(() => { f.style.width = f.dataset.level + "%"; }, 200);
        });
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08, rootMargin: "0px 0px -40px 0px" });

  $$(".reveal").forEach((el) => revealObserver.observe(el));
}

// ---- Lightfall Canvas — streak + yulduzlar + glow (ReactBits Lightfall uslubi) ----
function initStars() {
  const canvas = $("#stars");
  const ctx = canvas.getContext("2d");
  let w, h, scrollY = 0, mouse = { x: -9999, y: -9999 };

  // Ranglar (Lightfall uslubi)
  const COLORS = ["#A6C8FF", "#8b7fff", "#c084fc", "#60a5fa", "#ffffff"];
  const BG_COLORS = ["rgba(99,102,241,0.12)", "rgba(168,85,247,0.10)", "rgba(96,165,250,0.08)"];

  window.addEventListener("scroll", () => { scrollY = window.scrollY; }, { passive: true });
  window.addEventListener("mousemove", (e) => { mouse.x = e.clientX; mouse.y = e.clientY; }, { passive: true });

  // ---- Streaklar (yog'du chiziqlar) ----
  function mkStreak() {
    const color = COLORS[Math.floor(Math.random() * COLORS.length)];
    const angle = (Math.random() * 30 + 75) * Math.PI / 180; // 75°–105° (pastga)
    const speed = Math.random() * 2.5 + 1.8;
    const len   = Math.random() * 180 + 80;
    const width = Math.random() * 2.5 + 0.8;
    const glow  = Math.random() * 20 + 8;
    return {
      x: Math.random() * w,
      y: Math.random() * h * -1.5,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed,
      len, width, color, glow,
      alpha: 0,
      fadeIn: Math.random() * 0.04 + 0.02,
      alive: true,
      twinkle: Math.random() * 0.06 + 0.01,
      twinklePhase: Math.random() * Math.PI * 2,
      layer: Math.random() * 0.3 + 0.1,
    };
  }

  // ---- Yulduzlar ----
  function mkStar() {
    const r = Math.random();
    let radius, baseAlpha, layer;
    if (r < 0.65)      { radius = Math.random() * 0.6 + 0.2; baseAlpha = Math.random() * 0.3 + 0.1; layer = 0.1; }
    else if (r < 0.90) { radius = Math.random() * 1.0 + 0.5; baseAlpha = Math.random() * 0.35 + 0.2; layer = 0.25; }
    else               { radius = Math.random() * 1.5 + 1.0; baseAlpha = Math.random() * 0.25 + 0.45; layer = 0.45; }
    const color = Math.random() > 0.7 ? COLORS[Math.floor(Math.random() * COLORS.length)] : "rgba(255,255,255,1)";
    return {
      x: Math.random() * (w || window.innerWidth),
      baseY: Math.random() * (h || window.innerHeight) * 3,
      r: radius, baseAlpha, layer, color,
      pulseSpeed: Math.random() * 0.005 + 0.002,
      pulsePhase: Math.random() * Math.PI * 2,
      drift: (Math.random() - 0.5) * 0.03,
    };
  }

  const MAX_STREAKS = 22;
  let streaks = [], stars = [];

  function resize() {
    w = canvas.width  = window.innerWidth;
    h = canvas.height = window.innerHeight;
    const starCount = Math.min(320, Math.max(160, Math.floor((w * h) / 5500)));
    stars = Array.from({ length: starCount }, mkStar);
    if (!streaks.length) {
      streaks = Array.from({ length: MAX_STREAKS }, () => { const s = mkStreak(); s.y = Math.random() * h; return s; });
    }
  }

  function drawStars() {
    stars.forEach((st) => {
      const parallaxY = st.baseY - scrollY * st.layer;
      const screenY = ((parallaxY % (h * 2)) + h * 2) % (h * 2) - h * 0.5;
      if (screenY < -10 || screenY > h + 10) return;

      st.pulsePhase += st.pulseSpeed;
      const pulse = Math.sin(st.pulsePhase);
      const alpha = Math.max(0.04, st.baseAlpha + pulse * st.baseAlpha * 0.5);

      // Mouse proximity glow
      const dx = st.x - mouse.x, dy = screenY - mouse.y;
      const dist = Math.sqrt(dx*dx + dy*dy);
      const boost = dist < 120 ? (1 - dist/120) * 0.6 : 0;

      if (st.r > 1.5) {
        ctx.save();
        ctx.globalAlpha = alpha * 0.18;
        ctx.shadowColor = st.color; ctx.shadowBlur = 10;
        ctx.strokeStyle = st.color; ctx.lineWidth = 0.4;
        const len = st.r * 3;
        ctx.beginPath();
        ctx.moveTo(st.x - len, screenY); ctx.lineTo(st.x + len, screenY);
        ctx.moveTo(st.x, screenY - len); ctx.lineTo(st.x, screenY + len);
        ctx.stroke();
        ctx.restore();
      }

      ctx.save();
      ctx.globalAlpha = Math.min(1, alpha + boost);
      ctx.shadowColor = st.color; ctx.shadowBlur = st.r > 1 ? 8 : 3;
      ctx.beginPath();
      ctx.arc(st.x, screenY, st.r, 0, Math.PI * 2);
      ctx.fillStyle = st.color;
      ctx.fill();
      ctx.restore();

      st.x += st.drift;
      if (st.x < -4) st.x = w + 2;
      if (st.x > w + 4) st.x = -2;
    });
  }

  function drawStreaks() {
    streaks.forEach((st, i) => {
      // Mouse interaction
      const dx = st.x - mouse.x, dy = st.y - mouse.y;
      const dist = Math.sqrt(dx*dx + dy*dy);
      const mBoost = dist < 150 ? (1 - dist/150) * 0.8 : 0;

      // Parallax
      const py = st.y - scrollY * st.layer * 0.3;

      // Twinkle
      st.twinklePhase += st.twinkle;
      const twinkle = 0.7 + Math.sin(st.twinklePhase) * 0.3;

      const finalAlpha = Math.min(1, st.alpha * twinkle + mBoost * 0.3);
      if (finalAlpha < 0.01) { st.x += st.vx; st.y += st.vy; st.alpha += st.fadeIn; return; }

      // Streak chizish
      const tx = st.x + Math.cos(Math.atan2(st.vy, st.vx) + Math.PI) * st.len;
      const ty = py  + Math.sin(Math.atan2(st.vy, st.vx) + Math.PI) * st.len;

      ctx.save();
      const grad = ctx.createLinearGradient(st.x, py, tx, ty);
      const g2 = ctx.createLinearGradient(st.x, py, tx, ty);
      g2.addColorStop(0, `${st.color}${Math.round(finalAlpha*255).toString(16).padStart(2,"0")}`);
      g2.addColorStop(1, `${st.color}00`);

      ctx.strokeStyle = g2;
      ctx.lineWidth = st.width;
      ctx.shadowColor = st.color;
      ctx.shadowBlur = st.glow;
      ctx.globalAlpha = finalAlpha;
      ctx.lineCap = "round";
      ctx.beginPath();
      ctx.moveTo(st.x, py);
      ctx.lineTo(tx, ty);
      ctx.stroke();

      // Bosh nuqtada yorqin nuqta
      ctx.globalAlpha = finalAlpha * 0.9;
      ctx.shadowBlur = st.glow * 1.8;
      ctx.fillStyle = st.color;
      ctx.beginPath();
      ctx.arc(st.x, py, st.width * 1.2, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();

      // Harakat
      st.x += st.vx;
      st.y += st.vy;
      st.alpha = Math.min(1, st.alpha + st.fadeIn);

      // Ekrandan chiqsa yangidan yaratish
      if (st.y > h + st.len + 100 || st.x < -st.len - 100 || st.x > w + st.len + 100) {
        const ns = mkStreak();
        ns.x = Math.random() * (w + 200) - 100;
        ns.y = -st.len - Math.random() * 200;
        streaks[i] = ns;
      }
    });
  }

  function draw() {
    ctx.clearRect(0, 0, w, h);
    drawStars();
    drawStreaks();
    requestAnimationFrame(draw);
  }

  resize();
  window.addEventListener("resize", resize);
  draw();
}

// ---- Navbar / interaktivlik ----
function initNav() {
  const navbar = $("#navbar");
  const burger = $("#burger");
  const navLinks = $("#navLinks");

  window.addEventListener("scroll", () => {
    navbar.classList.toggle("scrolled", window.scrollY > 30);
    // active link
    let current = "";
    $$("section[id]").forEach((sec) => {
      if (window.scrollY >= sec.offsetTop - 120) current = sec.id;
    });
    $$(".nav-links a").forEach((a) => {
      a.classList.toggle("active", a.getAttribute("href") === "#" + current);
    });
  });

  burger.addEventListener("click", () => {
    burger.classList.toggle("open");
    navLinks.classList.toggle("open");
  });
  $$(".nav-links a").forEach((a) => a.addEventListener("click", () => {
    burger.classList.remove("open");
    navLinks.classList.remove("open");
  }));
}

// ---- Til almashtirish ----
function initLangToggle() {
  $("#langToggle").addEventListener("click", () => {
    LANG = LANG === "uz" ? "en" : "uz";
    localStorage.setItem("lang", LANG);
    renderAll();
  });
}

// ---- Contact form ----
function initContactForm() {
  const form = $("#contactForm");
  if (!form) return;
  const status = $("#formStatus");
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const btn = $("#cSubmit");

    const nameVal    = (document.getElementById("cName")?.value    || "").trim();
    const emailVal   = (document.getElementById("cEmail")?.value   || "").trim();
    const messageVal = (document.getElementById("cMessage")?.value || "").trim();

    if (!nameVal) {
      status.className = "form-status err";
      status.textContent = LANG === "uz" ? "Ismingizni kiriting" : "Please enter your name";
      return;
    }
    if (!messageVal) {
      status.className = "form-status err";
      status.textContent = LANG === "uz" ? "Xabar kiriting" : "Please enter a message";
      return;
    }

    status.className = "form-status";
    status.textContent = t("sending");
    btn.disabled = true;

    try {
      const body = JSON.stringify({ name: nameVal, email: emailVal, message: messageVal });
      const res = await fetch("/api/contact", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Content-Length": new Blob([body]).size,
        },
        body: body,
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data.error || "Server xatosi");
      status.className = "form-status ok";
      status.textContent = t("sent");
      form.reset();
    } catch (err) {
      status.className = "form-status err";
      status.textContent = err.message || t("sendErr");
    } finally {
      btn.disabled = false;
    }
  });
}

// ---- Init ----
function hideLoader() {
  const loader = document.getElementById("loader");
  if (loader) loader.classList.add("hidden");
}

async function main() {
  $("#year").textContent = new Date().getFullYear();
  initStars();
  initNav();
  initLangToggle();
  initContactForm();
  // Loader'ni 2 sekunddan keyin har qanday holatda yashir
  const loaderTimer = setTimeout(hideLoader, 2000);
  try {
    DATA = await loadData();
    window.__PORTFOLIO = DATA;
    renderAll();
  } catch (e) {
    console.error("Portfolio yuklanmadi:", e);
  } finally {
    clearTimeout(loaderTimer);
    setTimeout(hideLoader, 200);
  }
}
document.addEventListener("DOMContentLoaded", main);
