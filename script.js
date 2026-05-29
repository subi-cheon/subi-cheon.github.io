(function () {
  'use strict';

  var root = document.documentElement;

  /* ===== Theme toggle (light / dark) ===== */
  var toggle = document.getElementById('themeToggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var current = root.getAttribute('data-theme');
      var next = current === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      localStorage.setItem('theme', next);
    });
  }

  /* Follow OS theme changes only when the user hasn't chosen explicitly */
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function (e) {
    if (!localStorage.getItem('theme')) {
      root.setAttribute('data-theme', e.matches ? 'dark' : 'light');
    }
  });

  /* ===== Mobile menu ===== */
  var menuBtn = document.getElementById('menuBtn');
  var navList = document.getElementById('navList');

  function closeMenu() {
    if (!navList) return;
    navList.classList.remove('open');
    if (menuBtn) menuBtn.setAttribute('aria-expanded', 'false');
  }

  if (menuBtn && navList) {
    menuBtn.addEventListener('click', function () {
      var isOpen = navList.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', String(isOpen));
    });

    /* Close on nav link click */
    navList.addEventListener('click', function (e) {
      if (e.target.closest('a')) closeMenu();
    });

    /* Close on Escape */
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeMenu();
    });

    /* Reset menu state when leaving mobile breakpoint */
    window.matchMedia('(max-width: 720px)').addEventListener('change', function (e) {
      if (!e.matches) closeMenu();
    });
  }
})();
