// testimonials
$(document).ready(function () {
	const testimonials = [
		{
			text: "Absolutely amazing experience selling the car through KeySavvy. They are an A+ team. I cannot think of any better service.",
			author: "Mash, Nissan Leaf",
			link: "https://google.com",
		},
		{
			text: "KeySavvy made the process smooth and easy. Highly recommend their services!",
			author: "John, Tesla Model 3",
			link: "https://google.com",
		},
		{
			text: "Selling my car was hassle-free and convenient. Great service!",
			author: "Anna, Ford Focus",
			link: "https://google.com",
		},
		{
			text: "Professional, efficient, and trustworthy. Highly recommended!",
			author: "Mark, BMW X5",
			link: "https://google.com",
		},
		{
			text: "Great team and fantastic service!",
			author: "Lucy, Audi A4",
			link: "https://google.com",
		},
		{
			text: "Effortless and transparent experience. Would use again!",
			author: "James, Honda Civic",
			link: "https://google.com",
		},
	];

	const itemsPerPage = 1;
	let currentPage = 1;

	function renderTestimonials(page) {
		const start = (page - 1) * itemsPerPage;
		const end = start + itemsPerPage;
		const currentTestimonials = testimonials.slice(start, end);

		$("#testimonial-container").empty();
		currentTestimonials.forEach((testimonial) => {
			$("#testimonial-container").append(`
      <div class="card shadow-sm p-3 col-md-6">
        <p>"${testimonial.text}"</p>
        <p><strong>${testimonial.author}</strong></p>
        <a href="${testimonial.link}" target="_blank">Read on Google</a>
      </div>
    `);
		});
	}

	function renderPagination() {
		const totalPages = Math.ceil(testimonials.length / itemsPerPage);
		$("#testimonial-pagination").empty();

		for (let i = 1; i <= totalPages; i++) {
			$("#testimonial-pagination").append(`
      <li class="page-item ${i === currentPage ? "active" : ""}">
        <a class="page-link" href="#">${i}</a>
      </li>
    `);
		}
	}

	function handlePagination() {
		$(document).on("click", ".page-link", function (e) {
			e.preventDefault();
			const page = parseInt($(this).text());
			if (page !== currentPage) {
				currentPage = page;
				renderTestimonials(currentPage);
				renderPagination();
			}
		});
	}

	function autoNextPage() {
		const totalPages = Math.ceil(testimonials.length / itemsPerPage);
		setInterval(() => {
			currentPage = currentPage < totalPages ? currentPage + 1 : 1;
			renderTestimonials(currentPage);
			renderPagination();
		}, 4000);
	}
	renderTestimonials(currentPage);
	renderPagination();
	handlePagination();
	autoNextPage();
});

// heading texts
$(document).ready(function () {
	const texts = [
		"Cars & Birds",
		"Hemmings",
		"Offer UP",
		"Cars.com",
		"Autotrader",
		"Hagerty",
		"Bring a Trailer",
		"Car Gurus",
		"Hagerty",
		"any marketplace",
		"Craigslist",
	];
	let index = 0;

	function animateText() {
		$(".heading-animated-text").fadeOut(500, function () {
			index = (index + 1) % texts.length;
			$(this).text(`${texts[index]}`).fadeIn(500);
		});
	}

	setInterval(animateText, 1500);

	// Tab click event
	$(".tab-button").click(function () {
		$(".tab-button").removeClass("active");
		$(this).addClass("active");
		$(".tab-content").addClass("d-none");
		const target = $(this).data("target");
		$(`#${target}`).removeClass("d-none");
	});
});
