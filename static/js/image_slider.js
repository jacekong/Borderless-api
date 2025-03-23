// image slider
let slideIndex = 1;
showSlides(slideIndex);

function plusSlides(n) {
  showSlides(slideIndex += n);
}

function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  let dots = document.getElementsByClassName("bar");
  if (n > slides.length) {slideIndex = 1}    
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";  
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = " block";  
  dots[slideIndex-1].className += " active";
}

var slideshowContainer = document.querySelector('.slideshow-container');
// Add event listeners for keyboard navigation
document.addEventListener('keydown', function(event) {
  if (event.key === 'ArrowLeft') {
    plusSlides(-1);
    console.log("hi");
  } else if (event.key === 'ArrowRight') {
    plusSlides(1);
  }
});

// Enable touch swipe gesture
var hammer = new Hammer(slideshowContainer);
hammer.on('swipeleft', function () {
  plusSlides(1);
});

hammer.on('swiperight', function () {
  plusSlides(-1);
});