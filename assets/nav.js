// Shared header nav behavior for index.html and certificates.html.
// Load this AFTER each page's inline script (it reads which sections are
// visible — e.g. the certificates page hides an empty Courses section first).
(function () {
  const headerInner = document.querySelector('.header-inner');
  const siteNav = document.querySelector('.site-nav');
  const navToggle = document.querySelector('.nav-toggle');
  if (!siteNav) return;

  const allLinks = Array.prototype.slice.call(siteNav.querySelectorAll('.nav-link'));

  // Disable sticky :hover on touch devices (CSS gates hover on html:not(.touch)).
  window.addEventListener('touchstart', () => {
    document.documentElement.classList.add('touch');
  }, { once: true, passive: true });

  // Hamburger → animated dropdown (mobile).
  if (navToggle) {
    navToggle.addEventListener('click', () => {
      const open = siteNav.classList.toggle('nav-open');
      navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Native smooth scroll — starts immediately, no JS ramp-up. 72px matches the
  // sections' scroll-margin-top (clears the sticky header).
  function smoothScrollTo(targetEl) {
    const top = Math.max(0, targetEl.getBoundingClientRect().top + window.scrollY - 72);
    window.scrollTo({ top, behavior: 'smooth' });
  }

  // Hide any nav link whose target section is hidden (e.g. an empty Courses).
  allLinks.forEach(l => {
    const href = l.getAttribute('href') || '';
    if (href.charAt(0) === '#') {
      const sec = document.getElementById(href.slice(1));
      if (sec && getComputedStyle(sec).display === 'none') l.style.display = 'none';
    }
  });
  const links = allLinks.filter(l => l.style.display !== 'none');

  // The sections this nav controls, in document order (derived from the links).
  const sections = links
    .map(l => document.getElementById((l.getAttribute('href') || '').slice(1)))
    .filter(Boolean);
  const lastSectionId = sections.length ? sections[sections.length - 1].id : null;

  let navIntentId = null;

  function closeNav() {
    siteNav.classList.remove('nav-open');
    if (navToggle) navToggle.setAttribute('aria-expanded', 'false');
  }

  // Intercept in-page links (smooth scroll, no hash added to the URL). Links to
  // another page (e.g. the certificates logo → index.html) navigate normally.
  links.forEach(l => l.addEventListener('click', e => {
    const href = l.getAttribute('href') || '';
    if (href.charAt(0) !== '#') return;
    const target = document.getElementById(href.slice(1));
    if (!target) return;
    e.preventDefault();
    closeNav();
    navIntentId = target.id;
    smoothScrollTo(target);
    requestActiveUpdate();
  }));

  // Logo: smooth-scroll when it's an in-page anchor (home); otherwise let it
  // navigate (the certificates logo points at index.html).
  const brandLogo = document.querySelector('.brand-logo');
  if (brandLogo) {
    const href = brandLogo.getAttribute('href') || '';
    if (href.charAt(0) === '#') {
      const target = document.getElementById(href.slice(1));
      if (target) brandLogo.addEventListener('click', e => { e.preventDefault(); smoothScrollTo(target); });
    }
  }

  // ── Scrollspy ──────────────────────────────────────────────────────────
  const OFFSET = 100;                 // reference line just below the sticky header
  let activeId = null;
  function setActive(id) {
    if (id === activeId) return;
    activeId = id;
    links.forEach(l => l.classList.toggle('active', l.getAttribute('href') === '#' + id));
    // iOS Safari leaves a "ghost" underline on the backdrop-filter header when a
    // class changes; a one-frame transform nudge forces a clean recomposite.
    if (headerInner) {
      headerInner.style.transform = 'translateZ(0)';
      requestAnimationFrame(() => { headerInner.style.transform = ''; });
    }
  }

  // True only when the page actually scrolls AND we're at the bottom — so a page
  // short enough to fit the viewport doesn't wrongly pin the last section active.
  function atPageBottom() {
    const docH = document.documentElement.scrollHeight;
    return docH > window.innerHeight &&
      window.innerHeight + Math.ceil(window.scrollY) >= docH - 2;
  }

  let ticking = false;
  function updateActive() {
    ticking = false;
    if (!sections.length) return;
    // Trailing sections can share the bottom scroll position and never reach the
    // reference line — honor the link the user clicked (or fall back to the last).
    if (atPageBottom()) { setActive(navIntentId || lastSectionId); return; }
    let current = sections[0].id;
    sections.forEach(s => { if (s.getBoundingClientRect().top <= OFFSET) current = s.id; });
    setActive(current);
  }
  function requestActiveUpdate() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(updateActive);
  }

  window.addEventListener('scroll', requestActiveUpdate, { passive: true });
  window.addEventListener('resize', requestActiveUpdate);
  // A real user scroll cancels the click intent (programmatic smooth scroll
  // does not fire these), so manual scrolling resolves normally.
  ['wheel', 'touchmove', 'keydown'].forEach(ev =>
    window.addEventListener(ev, () => { navIntentId = null; }, { passive: true }));

  updateActive();
})();
