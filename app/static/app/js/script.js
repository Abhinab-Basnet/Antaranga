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

       
        const cardBg = window.getComputedStyle(card).backgroundImage;
        heroSection.style.backgroundImage = `linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), ${cardBg}`;

        
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
                console.log("Audio play prevented. Ensure user has interacted with the page first.");
            });
        }
    });
});



const intelObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const counters = entry.target.querySelectorAll('.counter');
            counters.forEach(counter => {
                const updateCount = () => {
                    const target = +counter.getAttribute('data-target');
                    const count = +counter.innerText;
                    
                 
                    const speed = target > 100 ? 150 : 250; 
                    const inc = Math.ceil(target / speed);

                    if (count < target) {
                       
                        counter.innerText = count + inc > target ? target : count + inc;
                        setTimeout(updateCount, 15);
                    } else {
                        counter.innerText = target;
                    }
                };
                updateCount();
            });
           
            intelObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.4 });


document.addEventListener("DOMContentLoaded", () => {
    const section = document.getElementById('intel-section');
    if (section) intelObserver.observe(section);
});


