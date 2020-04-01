window.onload = function() {
	var	tools = $('div[aria-labelledby="navbarDropdown"]');
	var edit_recipe = $(tools).children().eq(3);
	var delete_recipe = $(tools).children().eq(4);

	if (editing_tools) {
		// This script enables editing_tools for the owner of the recipe
		$(edit_recipe).attr('href', window.location.pathname+"update");
		$(edit_recipe).removeClass('disabled');
		$(delete_recipe).attr('href', window.location.pathname+"delete");
		$(delete_recipe).removeClass('disabled')
	}

	applyApropiateScrolls()
}

window.onresize = function(event) {
    applyApropiateScrolls()
}

function applyApropiateScrolls() {
	$('.recipe-ingredients > section').each(function(){
		if (this.scrollHeight > this.clientHeight) {
			// If section from .recipe-ingredients has vertical scrollbar
			$(this).css('border-radius','10px 0px 0px 10px')
			$(this).removeClass('empty-v-scroll')
		} else {
			// If not, hide empty vertical scrollbar
			$(this).css('border-radius','10px')
			$(this).addClass('empty-v-scroll')
		}
	})	
}