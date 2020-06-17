function isEmpty(element) {
	if (!element
	|| element===''
	|| /^\s+$/g.test(element))
	{ return true }
	return false
}




function showSection(section_id) {
	$('#recipe-detail-content > div').addClass('d-none');
	$('#'+section_id).removeClass('d-none');
}




function replaceIngredientsListBulletPointToCheckbox() {
	$('.ingredients').each(function(){
		$(this).html(
			$(this).html().replace(new RegExp('<li>','g'),'<li><label class="checkbox-container">')
		)
	});
	$('.ingredients').each(function(){
		$(this).html(
			$(this).html().replace(new RegExp('</label>','g'),'<input type="checkbox"><span class="checkmark"></span></label>')
		)
	});
}




function RemoveEmptyMethodListElements() {
	// Get list
	var new_method_list = []
	var method_data = $('#recipe-method-list > p').html();
	var method_list = method_data.split('<br>');

	for (var i=0; i<method_list.length; i++) {
		// Remove |linenumbers
		method_list[i]=method_list[i].replace(/^.+?\./g,'')

		if (!isEmpty(method_list[i])) {
			new_method_list.push(method_list[i])
		}
	}

	// Apply |linenumbers for each element from method_list
	var linenumbers = new_method_list.length.toString().replace(/\d/g,'0')
	for (var i=0; i<new_method_list.length; i++) {
		x = linenumbers
		x = x.slice((i+1).toString().length)
		new_method_list[i]= x + (i+1) + '.' + new_method_list[i]+'<br>'
	}

	$('#recipe-method-list > p').html(new_method_list.join("<br>"));
}




function printExternalPage(url) {
	var printWindow = window.open( url, 'Print', 'left=200, top=200, width=950, height=500, toolbar=0, resizable=0');
	printWindow.addEventListener('load', function() {
		setTimeout(function() { printWindow.print()
		}, 500);
	}, true);
}




/* Fancy checkbox button functionality */
function applyCheckboxFunctionality()
{
	$(function () {
		$('.button-checkbox').each(function () {

			// Settings
			var $widget = $(this),
				$button = $widget.find('button'),
				$checkbox = $widget.find('input:checkbox'),
				color = $button.data('color'),
				settings = {
					on: {
						icon: 'glyphicon glyphicon-check'
					},
					off: {
						icon: 'glyphicon glyphicon-unchecked'
					}
				}

			// Event Handlers
			$button.on('click', function () {
				$checkbox.prop('checked', !$checkbox.is(':checked'));
				$checkbox.triggerHandler('change');
				updateDisplay()
			})
			$checkbox.on('change', function () {
				updateDisplay()
			})

			// Actions
			function updateDisplay() {
				var isChecked = $checkbox.is(':checked');

				// Set the button's state
				$button.data('state', (isChecked) ? "on" : "off");

				// Set the button's icon
				$button.find('.state-icon')
					.removeClass()
					.addClass('state-icon ' + settings[$button.data('state')].icon)

				// Update the button's color
				if (isChecked) {
					$button
						.removeClass('btn-default')
						.addClass('btn-' + color + ' active')
					$button
						.children('i').eq(0).addClass('d-none')
					$button
						.children('i').eq(1).removeClass('d-none')
				} else {
					$button
						.removeClass('btn-' + color + ' active')
						.addClass('btn-default')
					$button
						.children('i').eq(0).removeClass('d-none')
					$button
						.children('i').eq(1).addClass('d-none')
				}
			}
		})
	})
}




window.onload = function()
{
	var	tools     = $('div[aria-labelledby="navbarDropdown"]');
	edit_recipe   = $(tools).find('a[name="edit_recipe"]');
	update_recipe = $(tools).find('a[name="update_recipe"]');
	delete_recipe = $(tools).find('a[name="delete_recipe"]');
	report_tool   = $(tools).find('a[name="report"]');
	download_tool = $(tools).find('a[name="download"]');
	print_tool    = $(tools).find('a[name="print"]');

	// Enable print tool (Wydrukuj)
	$(print_tool).attr('onclick', "printExternalPage(recipe_plain)");
	$(print_tool).removeClass('disabled');

	// Enable download tool (Pobierz)
	$(download_tool).attr('href', recipe_plain);
	$(download_tool).attr('download', recipe_title+'.html');
	$(download_tool).removeClass('disabled');

	if (editing_tools) {
		// The following script enables editing_tools for the owner of the recipe
		$(edit_recipe).attr('href', window.location.pathname+"update");
		$(edit_recipe).removeClass('disabled');
		$(delete_recipe).attr('href', window.location.pathname+"delete");
		$(delete_recipe).removeClass('disabled')
	} else {
		$(report_tool).removeClass('disabled')
	}



	/* Share container -> icons Functionality */

	var share_url = window.location;
	var share_title = recipe_title;
	var share_via = 'BakeToom';
	var share_related = 'BakeToom,BakeToomTeam,BTChefs';

	// Facebook
	$('li[name="facebook-icon"]').find('a').attr({
		href: 'http://www.facebook.com/sharer.php?u='+share_url,
		target: '_blank'
	});

	// Reddit
	$('li[name="reddit-icon"]').find('a').attr({
		href: 'http://reddit.com/submit?url='+share_url+
			  '&title='+share_title,

		target: '_blank'
	});

	// Twitter
	$('li[name="twitter-icon"]').find('a').attr({
		href: 'https://twitter.com/intent/tweet'+
			  '?url='+share_url+ 
			  '&text='+share_title+
			  '&via='+share_via +
			  '&related='+share_related,

		target: '_blank'
	});

	// Mail
	$('li[name="mail-icon"]').find('a').attr({
		href: 'mailto:?Subject='+share_title+
			  '&body='+share_url
	});

	/* END of Share container -> icons Functionality */



	replaceIngredientsListBulletPointToCheckbox();
	RemoveEmptyMethodListElements();
	applyCheckboxFunctionality();
}