// Open modal for single image
function openSingleImageModal(imageUrl) {
  
  const modal = document.getElementById('imageModal');
  const modalImage = document.getElementById('modalImage');
  const prevArrow = document.querySelector('.prevBtn');
  const nextArrow = document.querySelector('.nextBtn');

  modalImage.src = imageUrl;
  modal.classList.remove('hidden');
  prevArrow.classList.add('hidden');
  nextArrow.classList.add('hidden');
}

let slideIndex = 0;
let slides;
let currentPostId = null;
let filteredImageContainers = [];
let hammerModal;

// Initialize on DOM load
document.addEventListener("DOMContentLoaded", function() {
    slides = document.getElementsByClassName("mySlides");
});

// Open modal for a specific post
function openModal(postId) {
    currentPostId = postId;
    const modal = document.getElementById("imageModal");
    modal.classList.remove("hidden");

    const currentSlides = Array.from(slides).find(
        slide => slide.getAttribute("data-post-id") === postId
    );

    filteredImageContainers = currentSlides
        ? Array.from(currentSlides.getElementsByClassName("image-container"))
        : [];

    const prevBtn = document.querySelector(".prevBtn");
    const nextBtn = document.querySelector(".nextBtn");
    if (filteredImageContainers.length > 1) {
        prevBtn.classList.remove("hidden");
        nextBtn.classList.remove("hidden");

        const modalContent = document.querySelector(".image-modal-content");
        hammerModal = new Hammer(modalContent);
        hammerModal.on("swipeleft", () => plusSlides(1));
        hammerModal.on("swiperight", () => plusSlides(-1));
    } else {
        prevBtn.classList.add("hidden");
        nextBtn.classList.add("hidden");
    }

    if (slideIndex >= filteredImageContainers.length) {
        slideIndex = 0;
    }
    showSlides(slideIndex);
}

// Close modal
function closeModal(event) {
    if (event && event.target.id !== "imageModal") return;
    document.getElementById("imageModal").classList.add("hidden");
    currentPostId = null;
    filteredImageContainers = [];
    if (hammerModal) {
        hammerModal.off("swipeleft swiperight");
    }
}

// Navigation functions
function plusSlides(n) {
    if (filteredImageContainers.length <= 1) return;
    showSlides(slideIndex += n);
}

function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    if (filteredImageContainers.length === 0) return;

    if (n >= filteredImageContainers.length) { slideIndex = 0; }
    if (n < 0) { slideIndex = filteredImageContainers.length - 1; }

    const modalImage = document.getElementById("modalImage");
    const currentImage = filteredImageContainers[slideIndex].querySelector("img");
    modalImage.src = currentImage.src;

}

// Keyboard navigation
document.addEventListener("keydown", function(event) {
    const modal = document.getElementById("imageModal");
    if (modal && !modal.classList.contains("hidden") && filteredImageContainers.length > 1) {
        if (event.key === "ArrowLeft") {
            plusSlides(-1);
        } else if (event.key === "ArrowRight") {
            plusSlides(1);
        } else if (event.key === "Escape") {
            closeModal();
        }
    }
});
