const tabs = Array.from(document.querySelectorAll('[role="tab"]'));

function selectTab(selected) {
  tabs.forEach((tab) => {
    const active = tab === selected;
    tab.setAttribute('aria-selected', String(active));
    tab.tabIndex = active ? 0 : -1;
    document.getElementById(tab.getAttribute('aria-controls')).hidden = !active;
  });
}

tabs.forEach((tab) => {
  tab.addEventListener('click', () => selectTab(tab));
  tab.addEventListener('keydown', (event) => {
    if (!['ArrowLeft', 'ArrowRight'].includes(event.key)) return;
    event.preventDefault();
    const nextIndex = (tabs.indexOf(tab) + (event.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length;
    selectTab(tabs[nextIndex]);
    tabs[nextIndex].focus();
  });
});

document.querySelectorAll('[data-copy]').forEach((button) => {
  button.addEventListener('click', async () => {
    const label = button.textContent;
    try {
      await navigator.clipboard.writeText(button.dataset.copy);
      button.textContent = 'Copied';
    } catch {
      button.textContent = 'Select command';
      button.previousElementSibling.focus?.();
    }
    window.setTimeout(() => {
      button.textContent = label;
    }, 1800);
  });
});

const agent = navigator.userAgent.toLowerCase();
let recommended;

if (agent.includes('windows')) {
  recommended = document.querySelector('[data-platform="windows"]');
} else if (agent.includes('mac')) {
  recommended = document.querySelector('[data-platform="mac-arm"]');
}

if (recommended) {
  recommended.classList.add('is-recommended');
  recommended.querySelector('.recommended').hidden = false;
}
