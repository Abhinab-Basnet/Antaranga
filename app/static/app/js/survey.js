document.addEventListener("DOMContentLoaded", function() {
    const steps = document.querySelectorAll(".step");
    const nextBtns = document.querySelectorAll(".btn-next");
    const prevBtns = document.querySelectorAll(".btn-prev");
    const progressBar = document.getElementById("progress");
    const stepTitle = document.getElementById("step-title");
    const navItems = document.querySelectorAll(".nav-item");
    const sliders = document.querySelectorAll('input[type="range"]');
    
    let currentStep = 1;

   
    sliders.forEach(slider => {
        slider.addEventListener("input", (e) => {
            e.target.nextElementSibling.innerText = e.target.value;
        });
    });

    nextBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            if (currentStep < 5) changeStep(currentStep + 1);
        });
    });

    prevBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            if (currentStep > 1) changeStep(currentStep - 1);
        });
    });

    function changeStep(newStep) {
        document.querySelector(`.step[data-step="${currentStep}"]`).classList.remove("active");
        currentStep = newStep;
        const activeStep = document.querySelector(`.step[data-step="${currentStep}"]`);
        activeStep.classList.add("active");
        
        stepTitle.innerText = activeStep.getAttribute("data-title");
        updateUI();
    }

    function updateUI() {
        progressBar.style.width = (currentStep / 5) * 100 + "%";
        navItems.forEach(item => {
            const itemStep = parseInt(item.getAttribute("data-for"));
            item.classList.toggle("active", itemStep <= currentStep);
        });
    }
});