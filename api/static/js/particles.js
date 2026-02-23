// js/particles.js - Partículas mágicas para el fondo de la web

(function () {
    const canvas = document.getElementById('particles-canvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let particles = [];
    let animationId;
    const PARTICLE_COUNT = 50;

    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    class Particle {
        constructor() {
            this.reset();
        }

        reset() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.size = Math.random() * 2.5 + 0.5;
            this.speedY = -(Math.random() * 0.3 + 0.1);
            this.speedX = (Math.random() - 0.5) * 0.2;
            this.opacity = Math.random() * 0.5 + 0.1;
            this.fadeSpeed = Math.random() * 0.003 + 0.001;
            this.growing = Math.random() > 0.5;
 
            const colorRoll = Math.random();
            if (colorRoll > 0.82) {
                this.color = `rgba(74, 142, 230, `; // magic blue
            } else if (colorRoll > 0.64) {
                this.color = `rgba(155, 89, 182, `; // purple
            } else if (colorRoll > 0.46) {
                this.color = `rgba(232, 67, 147, `; // pink
            } else if (colorRoll > 0.30) {
                this.color = `rgba(240, 192, 64, `; // yellow
            } else {
                const r = 140 + Math.floor(Math.random() * 60);
                const g = 60 + Math.floor(Math.random() * 50);
                const b = 180 + Math.floor(Math.random() * 75);
                this.color = `rgba(${r}, ${g}, ${b}, `;
            }
        }

        update() {
            this.y += this.speedY;
            this.x += this.speedX;

            this.speedX += (Math.random() - 0.5) * 0.01;
            this.speedX = Math.max(-0.3, Math.min(0.3, this.speedX));

            if (this.growing) {
                this.opacity += this.fadeSpeed;
                if (this.opacity >= 0.6) this.growing = false;
            } else {
                this.opacity -= this.fadeSpeed;
                if (this.opacity <= 0.05) this.growing = true;
            }

            if (this.y < -10 || this.x < -10 || this.x > canvas.width + 10) {
                this.reset();
                this.y = canvas.height + 10;
            }
        }

        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = this.color + this.opacity + ')';
            ctx.fill();

            if (this.size > 1.5) {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size * 3, 0, Math.PI * 2);
                ctx.fillStyle = this.color + (this.opacity * 0.15) + ')';
                ctx.fill();
            }
        }
    }

    function init() {
        resize();
        particles = [];
        const count = getParticleCount();
        for (let i = 0; i < count; i++) {
            particles.push(new Particle());
        }
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        particles.forEach(p => {
            p.update();
            p.draw();
        });

        animationId = requestAnimationFrame(animate);
    }

    function getParticleCount() {
        return window.innerWidth < 768 ? 25 : PARTICLE_COUNT;
    }

    window.addEventListener('resize', () => {
        resize();
    });

    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            cancelAnimationFrame(animationId);
        } else {
            animate();
        }
    });

    init();
    animate();
})();
