// main.js - JS for 3D Animations, AI Effects, Quiz
document.addEventListener('DOMContentLoaded', () => {
    // 3D Globe Animation (Three.js on home page)
    if (document.getElementById('three-canvas')) {
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('three-canvas'), alpha: true });
        renderer.setSize(window.innerWidth, window.innerHeight);

        const geometry = new THREE.SphereGeometry(5, 32, 32);
        const material = new THREE.MeshBasicMaterial({ color: 0x4ecdc4, wireframe: true });
        const sphere = new THREE.Mesh(geometry, material);
        scene.add(sphere);

        camera.position.z = 15;

        function animate() {
            requestAnimationFrame(animate);
            sphere.rotation.y += 0.005;  // Rotate
            renderer.render(scene, camera);
        }
        animate();

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
    }

    // AI Particle Effect (on home and loader)
    if (document.getElementById('particles-js')) {
        particlesJS('particles-js', {
            particles: { number: { value: 80 }, color: { value: '#ff6b6b' }, shape: { type: 'circle' }, opacity: { value: 0.5 }, size: { value: 3 }, move: { speed: 2 } },
            interactivity: { events: { onhover: { enable: true, mode: 'repulse' } } },
            retina_detect: true
        });
    }

    // Quiz Submission
    const quizForm = document.getElementById('quiz-form');
    if (quizForm) {
        quizForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const responses = [];  // Collect all select values (0/1 as 'wrong'/'correct' for sim)
            quizForm.querySelectorAll('select').forEach(select => responses.push(select.value));
            
            const loader = document.getElementById('ai-loader');
            loader.classList.remove('hidden');
            
            const res = await fetch('/submit_quiz', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ responses })
            });
            const data = await res.json();
            loader.classList.add('hidden');
            if (data.success) {
                window.location.href = '/dashboard';
            } else {
                alert('Error: ' + data.error);
            }
        });
    }
});