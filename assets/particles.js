// Reusable particle-network background, shared by index.html (hero + intro)
// and certificates.html (page background). Returns { start, stop }.
function createParticleField(canvas, opts) {
  opts = opts || {};
  const ctx = canvas.getContext('2d');
  const COUNT = opts.count || 48;
  const MAX_DIST = opts.maxDist || 140;
  const particles = [];

  function resize() {
    canvas.width  = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  for (let i = 0; i < COUNT; i++) {
    particles.push({
      x:  Math.random() * canvas.width,
      y:  Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 0.35,
      vy: (Math.random() - 0.5) * 0.35,
      r:  Math.random() * 1.4 + 0.7,
    });
  }

  let rafId = null;
  function frame() {
    rafId = requestAnimationFrame(frame);
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let i = 0; i < particles.length; i++) {
      const p = particles[i];
      p.x += p.vx;
      p.y += p.vy;
      if (p.x < 0 || p.x > canvas.width)  p.vx *= -1;
      if (p.y < 0 || p.y > canvas.height) p.vy *= -1;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(140,110,220,0.45)';
      ctx.fill();

      for (let j = i + 1; j < particles.length; j++) {
        const q = particles[j];
        const dx = p.x - q.x;
        const dy = p.y - q.y;
        const d  = Math.sqrt(dx * dx + dy * dy);
        if (d < MAX_DIST) {
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(q.x, q.y);
          ctx.strokeStyle = `rgba(140,110,220,${(1 - d / MAX_DIST) * 0.13})`;
          ctx.lineWidth = 0.7;
          ctx.stroke();
        }
      }
    }
  }

  return {
    start() { if (rafId === null) frame(); },
    stop()  { if (rafId !== null) { cancelAnimationFrame(rafId); rafId = null; } }
  };
}
