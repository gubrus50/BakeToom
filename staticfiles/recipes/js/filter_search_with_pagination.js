function paginateToPage(index) {
	var url = window.location.href;

	if (/&page=\d+/g.test(url)) { window.location = url.replace(/&page=\d+/g,'&page='+index)
	} else { 
		window.location = url+'&page='+index
	}
}



window.onload = function()
{
	/* Search filter-container/(fc) toggle animation */
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
	var publish_date = $('input[name="search_by_date"]')[0];
	var recipe_id = $('input[name="id"]')[0];
	var nationality_mode = $('input[name="nationality_mode"]');
	var specific = nationality_mode[2];
	

	// Disable upload date checkbox if publish/edit date is checked
	function disableOrEnableUploadDateFilter()
	{
		if (publish_date.checked) {

			// disable upload date radio buttons from search filter-container
			$('ul[name="upload-date-children"]').children('li').each(function(index) {
				$(this).children('input[type="radio"]').prop('disabled', true)
			});
			$('ul[name="search-by-children"]').find('input[name="title"]').prop('disabled', true);
			$('ul[name="search-by-children"]').find('input[name="publisher"]').prop('disabled', true);
			$('ul[name="search-by-children"]').find('input[name="id"]').prop('disabled', true)
		
		} else {

			// enable upload date radio buttons from search filter-container
			$('ul[name="upload-date-children"]').children('li').each(function(index) {
				$(this).children('input[type="radio"]').prop('disabled', false)
			});
			$('ul[name="search-by-children"]').find('input[name="title"]').prop('disabled', false);
			$('ul[name="search-by-children"]').find('input[name="publisher"]').prop('disabled', false);
			$('ul[name="search-by-children"]').find('input[name="id"]').prop('disabled', false)
		}
	}


	function disableAllFilters()
	{
		if (recipe_id.checked) {

			$('ul[name="search-by-children"]').children('li').each(function(index) {
				$(this).children('input').prop('disabled', true)
			});
			$('ul[name="upload-date-children"]').children('li').each(function(index) {
				$(this).children('input').prop('disabled', true)
			});
			$('ul[name="categories-children"]').children('li').each(function(index) {
				$(this).children('input').prop('disabled', true)
			});
			$('ul[name="nationality-children"]').children('li').each(function(index) {
				$(this).children('input').prop('disabled', true)
			});
			$('ul[name="search-by-children"]').find('input[name="id"]').prop('disabled', false)
		
		} else {

			$('ul[name="search-by-children"]').children('li').each(function(index) {
				$(this).children('input').prop('disabled', false)
			});
			$('ul[name="upload-date-children"]').children('li').each(function(index) {
				$(this).children('input').prop('disabled', false)
			});
			$('ul[name="categories-children"]').children('li').each(function(index) {
				$(this).children('input').prop('disabled', false)
			});
			$('ul[name="nationality-children"]').children('li').each(function(index) {
				$(this).children('input').prop('disabled', false)
			});
		}
	}


	if (publish_date && specific && recipe_id)
	{	
		publish_date.onclick = function() { disableOrEnableUploadDateFilter() }
		recipe_id.onclick = function() { disableAllFilters() }

		// Disable or enable countrypicker in nationality filter
		$(nationality_mode).on('change', function() {
			if (specific.checked) {
				if ($('.countrypicker').hasClass('d-none')) {
					$('.countrypicker').removeClass('d-none')
				}
				else { $('.countrypicker').show() }
			} else { $('.countrypicker').hide() }	
		});
	}
}