// 🔍 Simple recipe search
const recipes = ["Chicken Biryani", "Chicken Burger", "Italian Pizza", "Alfredo Pasta"];
document.getElementById("searchBar").addEventListener("keyup", function() {
  const input = this.value.toLowerCase();
  const results = recipes.filter(r => r.toLowerCase().includes(input));
  const resultDiv = document.getElementById("searchResults");
  resultDiv.innerHTML = results.map(r => `<p>${r}</p>`).join("");
});

// 📩 Contact form
document.getElementById("contactForm").addEventListener("submit", function(e) {
  e.preventDefault();
  document.getElementById("responseMessage").textContent = "✅ Data Saved!";
});

const recipe = document.querySelectorAll('.recipe');
const popupBox = document.getElementById('popup-box');
const popupTitle = document.getElementById('popup-title');
const popupText = document.getElementById('popup-text');
const closeBtn = document.querySelector('.close-btn');

// Open popup with details
recipes.forEach(recipe => {
  recipe.addEventListener('click', () => {
    popupTitle.textContent = recipe.getAttribute('data-title');
    popupText.textContent = recipe.getAttribute('data-desc');
    popupBox.style.display = 'flex';
  });
});

// Close popup
closeBtn.addEventListener('click', () => {
  popupBox.style.display = 'none';
});

// Close popup when clicking outside
window.addEventListener('click', (e) => {
  if (e.target === popupBox) {
    popupBox.style.display = 'none';
  }
});
// ✅ Prevent page reload on PDF download
const downloadBtn = document.querySelector('.download-btn');
downloadBtn.addEventListener('click', function(e) {
    e.preventDefault(); // stop any default action (like reload)
    window.location.href = this.href; // trigger the download
});
// Automatically hide notifications after 60 seconds
setTimeout(function() {
  const notificationSection = document.getElementById('notifications');
  if (notificationSection) {
    notificationSection.style.transition = "opacity 1s ease";
    notificationSection.style.opacity = "0";
    setTimeout(() => {
      notificationSection.style.display = "none";
    }, 1000); // hide fully after fade out
  }
}, 60000);