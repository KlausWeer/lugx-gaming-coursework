(function ($) {
	
	"use strict";

	// Page loading animation
	$(window).on('load', function() {

        $('#js-preloader').addClass('loaded');

    });


	$(window).scroll(function() {
	  var scroll = $(window).scrollTop();
	  var box = $('.header-text').height();
	  var header = $('header').height();

	  if (scroll >= box - header) {
	    $("header").addClass("background-header");
	  } else {
	    $("header").removeClass("background-header");
	  }
	})

	var width = $(window).width();
		$(window).resize(function() {
		if (width > 767 && $(window).width() < 767) {
			location.reload();
		}
		else if (width < 767 && $(window).width() > 767) {
			location.reload();
		}
	})

	const elem = document.querySelector('.trending-box');
	const filtersElem = document.querySelector('.trending-filter');
	if (elem) {
		const rdn_events_list = new Isotope(elem, {
			itemSelector: '.trending-items',
			layoutMode: 'masonry'
		});
		if (filtersElem) {
			filtersElem.addEventListener('click', function(event) {
				if (!matchesSelector(event.target, 'a')) {
					return;
				}
				const filterValue = event.target.getAttribute('data-filter');
				rdn_events_list.arrange({
					filter: filterValue
				});
				filtersElem.querySelector('.is_active').classList.remove('is_active');
				event.target.classList.add('is_active');
				event.preventDefault();
			});
		}
	}


	// Menu Dropdown Toggle
	if($('.menu-trigger').length){
		$(".menu-trigger").on('click', function() {	
			$(this).toggleClass('active');
			$('.header-area .nav').slideToggle(200);
		});
	}


	// Menu elevator animation
	$('.scroll-to-section a[href*=\\#]:not([href=\\#])').on('click', function() {
		if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
			var target = $(this.hash);
			target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
			if (target.length) {
				var width = $(window).width();
				if(width < 991) {
					$('.menu-trigger').removeClass('active');
					$('.header-area .nav').slideUp(200);	
				}				
				$('html,body').animate({
					scrollTop: (target.offset().top) - 80
				}, 700);
				return false;
			}
		}
	});


	// Page loading animation
	$(window).on('load', function() {
		if($('.cover').length){
			$('.cover').parallax({
				imageSrc: $('.cover').data('image'),
				zIndex: '1'
			});
		}

		$("#preloader").animate({
			'opacity': '0'
		}, 600, function(){
			setTimeout(function(){
				$("#preloader").css("visibility", "hidden").fadeOut();
			}, 300);
		});
	});
    

// Add this code at the end of custom.js

// --- Analytics Tracking Code ---

    // A reusable function to send analytics events
    function sendAnalyticsEvent(eventData) {
        // A simple way to get a unique user ID, or create one if it doesn't exist
        let userId = localStorage.getItem('lugx_user_id');
        if (!userId) {
            userId = 'user_' + Date.now() + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('lugx_user_id', userId);
        }

        // Add user_id and page_url to all events
        const dataToSend = {
            ...eventData,
            user_id: userId,
            page_url: window.location.pathname
        };

        // Send the data to our analytics endpoint
        fetch('/api/track', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dataToSend),
        })
        .then(response => response.json())
        .then(data => console.log('Analytics event sent:', data))
        .catch((error) => console.error('Error sending analytics event:', error));
    }

    // --- Event Listener 1: Page View ---
    document.addEventListener("DOMContentLoaded", function() {
        sendAnalyticsEvent({ event_type: 'page_view' });
    });

    // --- Event Listener 2: Click Tracking ---
    document.addEventListener('click', function(event) {
        // We only track clicks on links (<a>) and buttons (<button>)
        if (event.target.tagName.toLowerCase() === 'a' || event.target.tagName.toLowerCase() === 'button') {
            sendAnalyticsEvent({
                event_type: 'click',
                clicked_element_id: event.target.id || event.target.innerText.substring(0, 20) // Use ID or first 20 chars of text
            });
        }
    });

    // --- Event Listener 3: Scroll Depth Tracking ---
    let scrollDepthTracked = false; // A flag to ensure we only send this event once per page load
    window.addEventListener('scroll', function() {
        if (scrollDepthTracked) {
            return; // Don't do anything if we've already tracked it
        }

        let scrollPosition = window.scrollY;
        let windowSize = window.innerHeight;
        let bodyHeight = document.body.offsetHeight;

        // Calculate the percentage scrolled
        let percentageScrolled = (scrollPosition + windowSize) / bodyHeight * 100;

        // If the user has scrolled more than 75% of the way down the page, track it.
        if (percentageScrolled > 75) {
            sendAnalyticsEvent({
                event_type: 'scroll_depth_75_percent',
                scroll_depth: 75 // We can send the percentage as data
            });
            scrollDepthTracked = true; // Set the flag so we don't send it again
        }
    });

})(window.jQuery);