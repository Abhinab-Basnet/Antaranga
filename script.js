document.addEventListener("DOMContentLoaded", function() {
    const steps = document.querySelectorAll(".step");
    const nextBtns = document.querySelectorAll(".btn-next");
    const prevBtns = document.querySelectorAll(".btn-prev");
    const progressBar = document.getElementById("progress");
    let currentStep = 1;

    nextBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            if (currentStep < 4) {
                document.querySelector(`.step[data-step="${currentStep}"]`).classList.remove("active");
                currentStep++;
                document.querySelector(`.step[data-step="${currentStep}"]`).classList.add("active");
                updateProgress();
            }
        });
    });

    prevBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            if (currentStep > 1) {
                document.querySelector(`.step[data-step="${currentStep}"]`).classList.remove("active");
                currentStep--;
                document.querySelector(`.step[data-step="${currentStep}"]`).classList.add("active");
                updateProgress();
            }
        });
    });

    function updateProgress() {
        const percentage = (currentStep / 4) * 100;
        progressBar.style.width = percentage + "%";
    }
});