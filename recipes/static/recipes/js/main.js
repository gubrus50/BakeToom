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

	/* Search filter -> Disable upload date checkbox is publish/edit date is checked */
	// jquery :checked feature was bugged at 18/04/2020, thats why I use selector by class
	var elm = document.getElementsByClassName('filter-search-by-date');
	var pd = elm[0];
	var ed = elm[1];
	
	function disableOrEnableUploadDateFilter() {
		if (pd.checked || ed.checked) {
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
	
	pd.onclick = function() { disableOrEnableUploadDateFilter() }
	ed.onclick = function() { disableOrEnableUploadDateFilter() }
})