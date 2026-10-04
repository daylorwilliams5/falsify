import { useEffect, useState } from 'react';

// Minimal hash router: "#/experiments/exp001_pilot" → ["experiments", "exp001_pilot"]
export function useRoute(): string[] {
  const read = () => window.location.hash.replace(/^#\/?/, '').split('/').filter(Boolean);
  // "#now"-style in-page anchors scroll within the current page instead of routing.
  const isAnchor = () => window.location.hash.length > 1 && !window.location.hash.startsWith('#/');
  const [route, setRoute] = useState(() => (isAnchor() ? [] : read()));
  useEffect(() => {
    const on = () => {
      if (isAnchor()) { document.getElementById(window.location.hash.slice(1))?.scrollIntoView({ behavior: 'smooth' }); return; }
      setRoute(read());
      window.scrollTo(0, 0);
    };
    window.addEventListener('hashchange', on);
    return () => window.removeEventListener('hashchange', on);
  }, []);
  return route;
}
