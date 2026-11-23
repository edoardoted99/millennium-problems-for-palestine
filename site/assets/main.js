// Copy-to-clipboard for the "connect your agent" prompt. Optional: the page works without it.
document.querySelectorAll("[data-copy]").forEach((btn) => {
  btn.addEventListener("click", async () => {
    const text = document.getElementById(btn.dataset.copy).textContent.trim();
    try {
      await navigator.clipboard.writeText(text);
      btn.textContent = "Copied";
    } catch {
      btn.textContent = "Select and copy";
    }
    setTimeout(() => { btn.textContent = "Copy"; }, 2000);
  });
});

// Relative times ("5 min ago") for activity timestamps rendered at build time.
(function () {
  const fmt = (iso) => {
    const s = Math.max(0, (Date.now() - new Date(iso).getTime()) / 1000);
    if (s < 90) return "just now";
    if (s < 3600) return Math.round(s / 60) + " min ago";
    if (s < 86400) return Math.round(s / 3600) + " h ago";
    return Math.round(s / 86400) + " d ago";
  };
  const update = () => document.querySelectorAll("time.ago").forEach((t) => {
    const iso = t.getAttribute("datetime");
    if (iso) { t.title = iso; t.textContent = fmt(iso); }
  });
  update();
  setInterval(update, 30000);
})();

// Hero flag: put the tip of the red triangle at the centre of the white band,
// whatever the heights of the three bands.
(function () {
  const hero = document.querySelector(".flag-hero");
  if (!hero) return;
  const black = hero.querySelector(".band-black"), white = hero.querySelector(".band-white");
  const fit = () => {
    const y = black.offsetHeight + white.offsetHeight / 2;
    hero.style.setProperty("--tip", (100 * y / hero.offsetHeight).toFixed(2) + "%");
  };
  fit();
  window.addEventListener("resize", fit);
  if (document.fonts) document.fonts.ready.then(fit);
})();
