function setCookie(cname,cvalue,exdays)
{
	var d = new Date();
	d.setTime(d.getTime() + (exdays*24*60*60*1000));
	var expires = "expires=" + d.toGMTString();
	document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/"
}



function getCookie(cname)
{
	var name = cname + "=";
	var decodedCookie = decodeURIComponent(document.cookie);
	var ca = decodedCookie.split(';');

	for(var i = 0; i <ca.length; i++) {
		var c = ca[i];
		while (c.charAt(0) == ' ') {
			c = c.substring(1);
		}
		if (c.indexOf(name) == 0) {
			return c.substring(name.length, c.length)
		}
	}

	return ""
}



/* shows scroll-to-top button if we scroll 
beyond the height of the initial window. */
const scrollFunc = () => {

	let scroll_vertical_axis = window.scrollY;

	if (scroll_vertical_axis > 0) {
		$('#scroll-to-top-button').fadeIn()
	} else {
		$('#scroll-to-top-button').fadeOut()
	}
}
window.addEventListener('scroll', scrollFunc);



$(document).ready(function()
{
	$('#scroll-to-top-button').hide();

	/* Cookies toggle animation */
	if (!getCookie('hide_cookies_popup')) { 
		setTimeout(function () {
			$("#cookieConsent").css('visibility', 'visible').hide().fadeIn(500) 
		}, 250)
	}
	else {
		$("#cookieConsent").css('display', 'none')
	}
	$("ignorecookies, .acceptcookies").click(function() {
		setCookie('hide_cookies_popup',true,1)
		$("#cookieConsent").fadeOut(200)
	});

	/* Search filter container toggle animation */
	var fc = $('div[name="filter-container"]');
	$('#search-filter-btn').on('click', function() {
		if ($(fc).is(':hidden')) {
			$(fc).slideDown('slow')
		}
		else {
			$('div[name="filter-container"]').slideUp('slow')
		}
	})

	/* Search filter dynamic functions */
	var elm = document.querySelectorAll('[name="SD"]');
	var publish_date = elm[0];
	var edit_date = elm[1];
	var nationality_mode_radios = $('input[name="NM"]');
	var specific = nationality_mode_radios[2];
	
	// Disable upload date checkbox if publish/edit date is checked
	function disableOrEnableUploadDateFilter() {
		if (publish_date.checked || edit_date.checked) {
			// disable upload date radio buttons from search filter-container
			$('ul[name="upload-date-children"]').children('li').each(function(index) {
				$(this).children('input[type="radio"]').prop('disabled', true)
			})
		} else {
			// enable upload date radio buttons from search filter-container
			$('ul[name="upload-date-children"]').children('li').each(function(index) {
				$(this).children('input[type="radio"]').prop('disabled', false)
			})
		}
	}


	if (publish_date && edit_date && specific) {	
		publish_date.onclick = function() { disableOrEnableUploadDateFilter() }
		edit_date.onclick = function() { disableOrEnableUploadDateFilter() }

		// Disable or enable countrypicker in nationality filter
		$(nationality_mode_radios).on('change', function() {
			if (specific.checked) {
				if ($('.countrypicker').hasClass('d-none')) {
					$('.countrypicker').removeClass('d-none')
				}
				else { $('.countrypicker').show() }
			} else { $('.countrypicker').hide() }	
		})
	}
	/* END of Search filter dynamic functions */

})