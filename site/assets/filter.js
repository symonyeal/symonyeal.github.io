// Gallery filter: show the cards whose data-subject matches the pressed button ("" = all).
// An area tile (data-filter) applies its subject and then follows its link to the gallery.
const f = document.querySelector(".filter"), cards = [...document.querySelectorAll(".card")], n = document.querySelector(".count");
const show = s => {
  cards.forEach(c => c.hidden = s !== "" && c.dataset.subject !== s);
  f.querySelectorAll("button").forEach(b => b.setAttribute("aria-pressed", b.dataset.subject === s));
  n.textContent = `${cards.filter(c => !c.hidden).length} of ${cards.length} projects`;
};
f.hidden = false;
f.addEventListener("click", ev => { const b = ev.target.closest("button"); if (b) show(b.dataset.subject); });
document.querySelectorAll("[data-filter]").forEach(t => t.addEventListener("click", () => show(t.dataset.filter)));
show("");
