const teamCards = document.querySelectorAll('.team-card-reveal');
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (reduceMotion || !('IntersectionObserver' in window)) {
  teamCards.forEach((card) => card.classList.add('is-visible'));
} else {
  const teamObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.15 });

  teamCards.forEach((card, index) => {
    card.style.transitionDelay = `${index * 80}ms`;
    teamObserver.observe(card);
  });
}

document.documentElement.classList.add('js');
