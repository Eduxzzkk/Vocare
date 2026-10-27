(() => {
  const modal = document.querySelector('#login-modal');
  const openButton = document.querySelector('#open-login');
  const card = modal?.querySelector('.modal__card');
  const form = modal?.querySelector('#login-form');
  const emailInput = modal?.querySelector('#email');
  const passwordInput = modal?.querySelector('#password');
  const toggleButton = modal?.querySelector('#toggle-password');
  const eyeIcon = modal?.querySelector('#icon-eye');
  const eyeOffIcon = modal?.querySelector('#icon-eye-off');

  if (!modal || !openButton || !card || !form) return;

  let lastFocused = null;

  function openModal() {
    lastFocused = document.activeElement;
    modal.dataset.open = 'true';
    modal.setAttribute('aria-hidden', 'false');
    document.documentElement.classList.add('no-scroll');
    window.setTimeout(() => emailInput?.focus({ preventScroll: true }), 60);
  }

  function closeModal() {
    modal.dataset.open = 'false';
    modal.setAttribute('aria-hidden', 'true');
    document.documentElement.classList.remove('no-scroll');
    lastFocused?.focus({ preventScroll: true });
  }

  const isOpen = () => modal.dataset.open === 'true';

  openButton.addEventListener('click', openModal);

  modal.addEventListener('click', (event) => {
    const closeTarget = event.target.closest('[data-close]');
    if (!closeTarget) return;
    if (closeTarget.classList.contains('modal__center') && event.target.closest('.modal__card')) return;
    closeModal();
  });

  document.addEventListener('keydown', (event) => {
    if (!isOpen()) return;
    if (event.key === 'Escape') {
      closeModal();
      return;
    }
    if (event.key !== 'Tab') return;

    const focusable = [...card.querySelectorAll('a[href], button, input')]
      .filter((element) => !element.disabled && element.offsetParent !== null);
    if (!focusable.length) return;

    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });

  toggleButton?.addEventListener('click', () => {
    const showPassword = passwordInput.type === 'password';
    passwordInput.type = showPassword ? 'text' : 'password';
    eyeIcon?.classList.toggle('is-hidden', showPassword);
    eyeOffIcon?.classList.toggle('is-hidden', !showPassword);
    toggleButton.setAttribute('aria-label', showPassword ? 'Ocultar senha' : 'Mostrar senha');
  });

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    window.location.assign('pagina-em-branco.html');
  });

  window.LoginModal = { open: openModal, close: closeModal };

  if (window.location.hash === '#login') openModal();
})();
