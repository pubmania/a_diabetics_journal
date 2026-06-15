// Script to create slider for nutrition cards.
document.addEventListener('DOMContentLoaded', function() {
	const customContainer = document.querySelector('.custom--container'); // Fixed variable name
	const slides = document.querySelectorAll('.custom-slide');
	const leftArrow = document.querySelector('.left-arrow');
	const rightArrow = document.querySelector('.right-arrow');
	let currentIndex = 0; // Track the current slide index
	// Function to update the scroll position
	function updateScroll() {
		const slideWidth = slides[currentIndex].offsetWidth; // Get the width of the current slide
		customContainer.scrollTo({
			left: slideWidth * currentIndex, // Scroll to the current slide
			behavior: 'smooth' // Smooth scrolling
		});
	}
	// Event listener for the left arrow
	leftArrow.addEventListener('click', function() {
		if (currentIndex > 0) {
			currentIndex--; // Decrease index
			updateScroll(); // Update scroll position
		}
	});
	// Event listener for the right arrow
	rightArrow.addEventListener('click', function() {
		if (currentIndex < slides.length - 1) {
			currentIndex++; // Increase index
			updateScroll(); // Update scroll position
		}
	});
});
