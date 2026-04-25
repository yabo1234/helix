(function () {
  const closeAll = () => {
    document.querySelectorAll('.dropdown[data-open="true"]').forEach((dd) => {
      dd.setAttribute('data-open', 'false');
      const btn = dd.querySelector('button');
      if (btn) btn.setAttribute('aria-expanded', 'false');
    });
  };

  document.addEventListener('click', (e) => {
    const dropdown = e.target.closest('.dropdown');
    if (!dropdown) {
      closeAll();
      return;
    }

    const button = e.target.closest('button');
    if (!button) return;

    const isOpen = dropdown.getAttribute('data-open') === 'true';
    closeAll();
    dropdown.setAttribute('data-open', String(!isOpen));
    button.setAttribute('aria-expanded', String(!isOpen));
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeAll();
  });
})();
