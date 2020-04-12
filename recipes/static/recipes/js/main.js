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



/* Cookies toggle animation */
$(document).ready(function()
{
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