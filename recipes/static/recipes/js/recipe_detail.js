window.onload = function() {
	var	tools = $('div[aria-labelledby="navbarDropdown"]');
	var edit_recipe = $(tools).children().eq(3);
		
	$(edit_recipe).attr('href', window.location.pathname+"update");
	$(edit_recipe).removeClass('disabled')
}
