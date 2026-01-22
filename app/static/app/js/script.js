const cards = document.querySelectorAll('.card');
const heroTitle = document.getElementById('hero-title');
const heroSection = document.querySelector('.hero');


const voiceMap = {
    "MOUNT EVEREST": "audio/namaskar.m4a",
    "SWAYAMBHUNATH": "audio/mounteverest.m4a",
    "ANNAPURNA": "audio/namaskar.m4a",
    "PASHUPATINATH": "audio/pashupati.m4a",
    "LUMBINI": "audio/lumbini.m4a"
};

let currentAudio = null;

cards.forEach(card => {
    card.addEventListener('click', () => {
        const title = card.getAttribute('data-title');

       
        cards.forEach(c => c.classList.remove('active'));
        card.classList.add('active');
        heroTitle.innerText = title;
        const newBg = card.style.backgroundImage;
        heroSection.style.backgroundImage = `linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), ${newBg}`;

      
        if (currentAudio) {
            currentAudio.pause();
            currentAudio.currentTime = 0;
        }

     
        if (voiceMap[title]) {
            currentAudio = new Audio(voiceMap[title]);
            
        
            const source = document.createElement('source');
            source.src = voiceMap[title];
            source.type = 'audio/mp4'; 
            currentAudio.appendChild(source);

            currentAudio.play().catch(error => {
                console.log("Audio play prevented. Ensure user has interacted with the page.");
            });
        }
    });
});

// aboutsection
window.addEventListener('scroll', () => {
    const cards = document.querySelectorAll('.info-card');
    const screenPos = window.innerHeight / 1.2;

    cards.forEach((card, index) => {
        const cardPos = card.getBoundingClientRect().top;

        if (cardPos < screenPos) {
            
            setTimeout(() => {
                card.style.opacity = "1";
                card.style.transform = "translateY(0)";
            }, index * 150);
        }
    });
});


//page 3

//page4

function goToStep(step) {
    const frames = document.querySelectorAll('.q-frame');
    const dots = document.querySelectorAll('.dot');
    const aura = document.getElementById('aura');
    const watermark = document.getElementById('cultural-watermark');

   
    frames.forEach(frame => {
        if(frame.classList.contains('active')) {
            frame.style.opacity = '0';
        }
    });

    setTimeout(() => {
        frames.forEach(frame => frame.classList.remove('active'));
        
        const nextFrame = document.getElementById('q' + step);
        nextFrame.classList.add('active');
        nextFrame.style.opacity = '1';

        
        const themeColor = nextFrame.getAttribute('data-color');
        const iconSymbol = nextFrame.getAttribute('data-icon');

        aura.style.background = `radial-gradient(circle at center, ${themeColor} 0%, transparent 70%)`;
        watermark.style.opacity = '0';
        
        setTimeout(() => {
            watermark.innerText = iconSymbol;
            watermark.style.opacity = '0.06';
        }, 300);

        
        dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === step - 1);
        });
    }, 400);
}