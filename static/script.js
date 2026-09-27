async function scanUrl() {
    const inputEl = document.getElementById("url-input");
    const url = (inputEl && inputEl.value ? inputEl.value : "").trim();

    if (!url) {
        document.getElementById("risk-level").textContent = "Please enter a URL.";
        return;
    }

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url: url })
        });

        const data = await response.json();

        const score = data.risk_score;

        document.getElementById("score").textContent = score;

        const clamped = Math.max(0, Math.min(100, score));
        const fill = document.getElementById("meter-fill");
        fill.style.width = clamped + "%";

        let color;

        if (clamped < 40) {
            color = "limegreen";
        } else if (clamped < 70) {
            color = "gold";
        } else {
            color = "crimson";
        }

        fill.style.backgroundColor = color;
        fill.style.boxShadow = `0 0 20px ${color}`;

        document.getElementById("risk-level").textContent = data.verdict;

    } catch (error) {
        console.error(error);
        document.getElementById("risk-level").textContent = "Error scanning URL";
    }
}

// Risk meter scan button
document.getElementById("scan-btn").addEventListener("click", (e) => {
  e.preventDefault();
  scanUrl();
});

// Smooth fade‑out transition on navigation
document.querySelectorAll("nav a").forEach((link) => {
  link.addEventListener("click", (e) => {
    e.preventDefault();
    const href = link.getAttribute("href");
    document.body.classList.add("fade-out");
    setTimeout(() => {
      window.location.href = href;
    }, 500);
  });
});

// Toggle Sign Up Modal
const signupToggle = document.getElementById("signup-toggle");
const signupModal = document.getElementById("signup-modal");
const closeSignup = document.getElementById("close-signup");

signupToggle.addEventListener("click", () => {
  signupModal.style.display = "flex"; // show modal
});

closeSignup.addEventListener("click", () => {
  signupModal.style.display = "none"; // hide modal
});

// Close modal when clicking outside content
window.addEventListener("click", (e) => {
  if (e.target === signupModal) {
    signupModal.style.display = "none";
  }
});
