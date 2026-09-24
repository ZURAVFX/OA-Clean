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
