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



/* Prevent Header and Footer from interfering the Body */
function adjustHeaderAndFooter()
{
	$('body').css({
		'padding-top': $('header > nav').outerHeight()+'px',
		'padding-bottom': $('footer').outerHeight()+'px'
	})
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
	adjustHeaderAndFooter();
	$(window).resize((function() {
		var timeout = null;
		return function() {
			if (timeout) clearTimeout(timeout);
			timeout = setTimeout(adjustHeaderAndFooter(), 250)
		}
	})());


	$('#scroll-to-top-button').hide();
	$('a.disabled').click( function()
	{
		if ($(this).hasClass('disabled')) {
			return false
		}
		else {
			$(this).trigger('click')
		}
	});


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
	})
})