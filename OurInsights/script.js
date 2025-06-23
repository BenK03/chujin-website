function clearHighlights() {
  document.querySelectorAll('.highlight').forEach(el => {
    const parent = el.parentNode;
    parent.replaceChild(document.createTextNode(el.textContent), el);
    parent.normalize();
  });
}

function searchPage() {
  clearHighlights();

  const term = document.getElementById("searchInput").value.trim().toLowerCase();
  if (!term) return;

  const root = document.getElementById("mainContent");
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null, false);

  const nodesToHighlight = [];

  let node;
  while ((node = walker.nextNode())) {
    const content = node.textContent.toLowerCase();
    let index = content.indexOf(term);
    while (index !== -1) {
      nodesToHighlight.push({ node, index });
      index = content.indexOf(term, index + term.length);
    }
  }

  // Apply highlights in reverse order to avoid corrupting text nodes
  for (let i = nodesToHighlight.length - 1; i >= 0; i--) {
    const { node, index } = nodesToHighlight[i];
    const range = document.createRange();
    range.setStart(node, index);
    range.setEnd(node, index + term.length);

    const highlight = document.createElement("span");
    highlight.className = "highlight";
    highlight.textContent = range.toString();

    range.deleteContents();
    range.insertNode(highlight);
  }
  const firstHighlight = document.querySelector('.highlight');
  if (firstHighlight) firstHighlight.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("searchInput");
  input.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
      searchPage();
    }
  });
});

function toggleMenu() {
  const navLinks = document.querySelector('.nav-links');
  navLinks.classList.toggle('show');
}

// ─── Enable click-and-drag on the carousel ───
const carousel = document.querySelector('.slideshow-container');
let isDragging  = false;
let startX      = 0;
let scrollLeft = 0;

carousel.addEventListener('mousedown', (e) => {
  isDragging  = true;
  carousel.classList.add('dragging');
  startX      = e.pageX - carousel.offsetLeft;
  scrollLeft = carousel.scrollLeft;
});
carousel.addEventListener('mouseup', () => {
  isDragging  = false;
  carousel.classList.remove('dragging');
});
carousel.addEventListener('mouseleave', () => {
  isDragging  = false;
  carousel.classList.remove('dragging');
});
carousel.addEventListener('mousemove', (e) => {
  if (!isDragging) return;
  e.preventDefault();
  const x    = e.pageX - carousel.offsetLeft;
  const walk = (x - startX);  // adjust multiplier for faster scroll
  carousel.scrollLeft = scrollLeft - walk;
});
