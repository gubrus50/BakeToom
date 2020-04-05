function setCookie(cname,cvalue,exdays) {
  var d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  var expires = "expires=" + d.toGMTString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}


/* Cookies toggle animation */
$(document).ready(function(){
	if (!getCookie('allow_cookies')) {   
		setTimeout(function () {
        	$("#cookieConsent").fadeIn(200)
    	}, 1000)
    }
    $("ignorecookies, .acceptcookies").click(function() {
    	setCookie('allow_cookies',true,7)
        $("#cookieConsent").fadeOut(200)
    })
})

