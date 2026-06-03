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

  /* ===== Contact form → Slack ===== */
  /*
   * 두 가지 전송 방식을 지원합니다. 둘 중 하나만 채우면 됩니다.
   *
   * 1) ENDPOINT_URL (권장): 본인이 만든 서버리스 프록시 주소.
   *    웹훅 URL을 브라우저에 노출하지 않아 스팸/악용에 안전합니다.
   *    프록시가 { name, phone } JSON을 받아 Slack으로 다시 보내면 됩니다.
   *
   * 2) SLACK_WEBHOOK_URL: Slack Incoming Webhook URL을 직접 사용.
   *    설정이 가장 간단하지만 URL이 공개 소스에 노출되는 점에 유의하세요.
   */
  var CONTACT = {
    ENDPOINT_URL: 'https://subicheon--8cf6feb25f2311f182e01607ee4eb77e.web.val.run',
    SLACK_WEBHOOK_URL: ''      // 예: 'https://hooks.slack.com/services/XXX/YYY/ZZZ'
  };

  var form = document.getElementById('contactForm');
  if (form) {
    var statusEl = document.getElementById('contactStatus');
    var submitBtn = document.getElementById('contactSubmit');
    var nameEl = document.getElementById('contactName');
    var phoneEl = document.getElementById('contactPhone');
    var messageEl = document.getElementById('contactMessage');
    var consentEl = document.getElementById('contactConsent');

    function setStatus(msg, type) {
      statusEl.textContent = msg;
      statusEl.className = 'contact-status' + (type ? ' ' + type : '');
    }

    function isValidPhone(v) {
      return /[0-9]/.test(v) && v.replace(/[^0-9]/g, '').length >= 9;
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      var name = nameEl.value.trim();
      var phone = phoneEl.value.trim();
      var message = messageEl ? messageEl.value.trim() : '';

      if (!name) { setStatus('이름을 입력해 주세요.', 'error'); nameEl.focus(); return; }
      if (!isValidPhone(phone)) { setStatus('전화번호를 정확히 입력해 주세요.', 'error'); phoneEl.focus(); return; }
      if (!message) { setStatus('문의 내용을 입력해 주세요.', 'error'); messageEl.focus(); return; }
      if (consentEl && !consentEl.checked) { setStatus('개인정보 수집·이용에 동의해 주세요.', 'error'); consentEl.focus(); return; }

      submitBtn.disabled = true;
      setStatus('전송 중…', '');

      var sent;
      if (CONTACT.ENDPOINT_URL) {
        sent = fetch(CONTACT.ENDPOINT_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name: name, phone: phone, message: message })
        });
      } else if (CONTACT.SLACK_WEBHOOK_URL) {
        var text = '📨 *새 문의가 도착했어요*\n• 이름: ' + name + '\n• 전화번호: ' + phone + '\n• 내용: ' + message;
        // form-encoded payload + no-cors 로 Slack Webhook CORS 제약을 우회합니다.
        var body = 'payload=' + encodeURIComponent(JSON.stringify({ text: text }));
        sent = fetch(CONTACT.SLACK_WEBHOOK_URL, {
          method: 'POST',
          mode: 'no-cors',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: body
        });
      } else {
        submitBtn.disabled = false;
        setStatus('전송 채널이 아직 설정되지 않았어요. (script.js의 CONTACT 설정 확인)', 'error');
        return;
      }

      sent.then(function () {
        setStatus('문의가 정상적으로 전송됐어요. 곧 연락드릴게요!', 'success');
        form.reset();
      }).catch(function () {
        setStatus('전송에 실패했어요. 잠시 후 다시 시도해 주세요.', 'error');
      }).then(function () {
        submitBtn.disabled = false;
      });
    });
  }
})();
