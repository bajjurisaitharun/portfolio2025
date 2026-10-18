// 3D Car Animation using Three.js
let scene, camera, renderer, car;

function init3D() {
    const canvas = document.getElementById('carCanvas');
    if (!canvas) return;

    // Scene setup
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, canvas.offsetWidth / canvas.offsetHeight, 0.1, 1000);
    renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true });
    renderer.setSize(canvas.offsetWidth, canvas.offsetHeight);
    renderer.setClearColor(0x000000, 0);

    // Create a simple car shape
    const carGeometry = new THREE.BoxGeometry(4, 1, 2);
    const carMaterial = new THREE.MeshPhongMaterial({ color: 0x3b82f6 });
    car = new THREE.Mesh(carGeometry, carMaterial);
    scene.add(car);

    // Add wheels
    const wheelGeometry = new THREE.CylinderGeometry(0.4, 0.4, 0.2, 8);
    const wheelMaterial = new THREE.MeshPhongMaterial({ color: 0x1f2937 });
    
    const wheels = [];
    const wheelPositions = [
        [-1.5, -0.7, 1.2],
        [1.5, -0.7, 1.2],
        [-1.5, -0.7, -1.2],
        [1.5, -0.7, -1.2]
    ];

    wheelPositions.forEach(pos => {
        const wheel = new THREE.Mesh(wheelGeometry, wheelMaterial);
        wheel.position.set(pos[0], pos[1], pos[2]);
        wheel.rotation.z = Math.PI / 2;
        wheels.push(wheel);
        scene.add(wheel);
    });

    // Lighting
    const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(10, 10, 5);
    scene.add(directionalLight);

    camera.position.set(0, 2, 8);
    camera.lookAt(0, 0, 0);

    // Animation loop
    function animate() {
        requestAnimationFrame(animate);
        
        car.rotation.y += 0.005;
        wheels.forEach(wheel => {
            wheel.rotation.x += 0.05;
        });
        
        renderer.render(scene, camera);
    }
    animate();
}

// Navigation scroll effect
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 100) {
        navbar.style.background = 'rgba(255, 255, 255, 0.98)';
        navbar.style.boxShadow = '0 2px 20px rgba(0,0,0,0.1)';
    } else {
        navbar.style.background = 'rgba(255, 255, 255, 0.95)';
        navbar.style.boxShadow = 'none';
    }
});

// Contact form handling
document.getElementById('contactForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData);
    
    try {
        const response = await fetch('/api/contact', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('Thank you for contacting us! We will get back to you soon.');
            e.target.reset();
        } else {
            alert('Something went wrong. Please try again.');
        }
    } catch (error) {
        alert('Error sending message. Please try again.');
    }
});

// Book service function
function bookService(serviceName, price) {
    document.getElementById('service').value = serviceName.toLowerCase().replace(' ', '-');
    document.getElementById('contact').scrollIntoView({ behavior: 'smooth' });
}

// Open contact section
function openContact() {
    document.getElementById('contact').scrollIntoView({ behavior: 'smooth' });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    init3D();
    
    // Add scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    document.querySelectorAll('.service-card, .pricing-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s ease';
        observer.observe(el);
    });
});

// Responsive canvas resizing
window.addEventListener('resize', () => {
    const canvas = document.getElementById('carCanvas');
    if (canvas && renderer && camera) {
        camera.aspect = canvas.offsetWidth / canvas.offsetHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(canvas.offsetWidth, canvas.offsetHeight);
    }
});
