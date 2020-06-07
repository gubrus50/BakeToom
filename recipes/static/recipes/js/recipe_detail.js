function getCurrentDate()
{
	var today = new Date();
	var dd = today.getDate();
	var mm = today.getMonth()+1;
	var yyyy = today.getFullYear();

	if(dd<10) {
		dd = '0'+dd
	} 

	if(mm<10) {
		mm = '0'+mm
	} 

	return dd + '/' + mm + '/' + yyyy
}


function showSection(section_id) {
	$('#recipe-detail-content > div').addClass('d-none');
	$('#'+section_id).removeClass('d-none');
}


function getBase64(url, callback)
{
	var xhr = new XMLHttpRequest();
	xhr.onload = function() {

	var reader = new FileReader();
	reader.onloadend = function() {
		callback(reader.result)
	}
	reader.readAsDataURL(xhr.response)
	}

	xhr.open('GET', url);
	xhr.responseType = 'blob';
	xhr.send()
}



function isEmpty(element)
{
	if (!element
	|| element===''
	|| /^\s+$/g.test(element))
	{ 
		return true
	}
	return false
}




/* Expands/shrinks the list from method
   container by applying/removing break tags */
function updateMethodListBreaks(checkbox)
{
	var rml = $('#recipe-method-list').children();

	if (checkbox.checked) {
		$(rml).html(
			$(rml).html().replace(new RegExp('<br>','g'),'<br><br>')
		)
	} else {
		$(rml).html(
			$(rml).html().replace(new RegExp('<br><br>','g'),'<br>')
		)
	}
}


function replaceIngredientsListBulletPointToCheckbox()
{
	$('.ingredients').each(function(){
		$(this).html(
			$(this).html().replace(new RegExp('<li>','g'),'<li><label class="checkbox-container">')
		)
	})
	$('.ingredients').each(function(){
		$(this).html(
			$(this).html().replace(new RegExp('</label>','g'),'<input type="checkbox"><span class="checkmark"></span></label>')
		)
	})
}




function RemoveEmptyMethodListElements()
{
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

	$('#recipe-method-list > p').html(new_method_list)
}



function returnPageToNormal(originalContents)
{
	// Return page to normal state / old document
	document.body.innerHTML = originalContents;
	applyCheckboxFunctionality();

	// Uncheck Expand List checkbox (Rozszerz Litę)
	// to avoid additional expantion bug.
	var rml = $('#recipe-method-list').children().eq(2);
	$(rml).html(
		$(rml).html().replace(new RegExp('<br><br>','g'),'<br>')
	)
	$('#expand-list')
		.removeClass('active btn-primary')
		.addClass('btn-default')
}



function renderDocumentAndCommitAction(mode, content_id)
{
	// Get content and old document
	var printContents = document.getElementById(content_id).outerHTML;
	var originalContents = document.body.innerHTML;

	// Validate the provided parameters
	// Regex: select print or download from first position where no data follows after 
	if (!content_id || !/^(print|download)(?!(.|\n))/g.test(mode)) { return false }

	else {
		/* Following scripts render new document */

		// include current date and url with content_id content.
		document.body.innerHTML = 'EU-Data: ' + getCurrentDate() + ', URL: ' + window.location.href + printContents;

		// Replace nationality image with country name instead
		$('small > li.flag').replaceWith($('<span>' + recipe_nationality + '</span>'));

		// Float image to the right
		$('#recipe-image').attr('style', 'float: right; border-radius: 5px 5px 5px 75px');

		// Remove background from #recipes container
		$('#recipes').attr('style', 'background-size: 15px 15px');

		// Align text to left side
		$('#recipes > center').attr('style', 'text-align: left');

		// Remove bottom margin of #recipes
		$('#recipes').removeClass('mb-5');

		// Set container of all categories to default style
		$('.recipe-ingredients > section')
			.attr('style', 'height: auto; border-radius: 10px; min-height: 250px; margin: 14px');
		// Remove scrollbars from all categories
		$('.recipe-ingredients > section')
			.addClass('empty-v-scroll', 'empty-h-scroll');

		// Remove Expand list (Rozszerz Listę) button	
		$('.button-checkbox').remove();

		// Replace custom checkbox with default circle bulletpoint
		// for all categories list
		$('section > ul').attr('style', 'list-style-type: circle');
		// Filter section ul, remove lists with no data
		$('section > ul').each(function(){
			$(this).children('li').each(function(index){
				// if list is empty
				if (isEmpty($(this).text())) {
					$(this).remove()
				}
			})
		})
	}

	if (mode=='print') {
		window.print();
		returnPageToNormal(originalContents)

	} else { return originalContents }
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
	var	tools = $('div[aria-labelledby="navbarDropdown"]');
	edit_recipe = $(tools).find('a[name="edit_recipe"]');
	update_recipe = $(tools).find('a[name="update_recipe"]');
	delete_recipe = $(tools).find('a[name="delete_recipe"]');
	report_tool = $(tools).find('a[name="report"]');
	/*download_tool = $(tools).find('a[name="download"]');
	print_tool = $(tools).find('a[name="print"]');

	// Enable print tool (Wydrukuj)
	$(print_tool).attr('onclick', "renderDocumentAndCommitAction('print','recipes')");
	$(print_tool).removeClass('disabled');
	// Enable download tool (Pobierz)
	$(download_tool).attr('onclick',
		"var originalContents = renderDocumentAndCommitAction('download', 'recipes'); " +
		"this.href = 'data:text/html;charset=UTF-8,' + encodeURIComponent(document.documentElement.outerHTML); " +
		"returnPageToNormal(originalContents)"
	);
	$(download_tool).attr('download', recipe_title+'.html');
	$(download_tool).removeClass('disabled'); */

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



	// Change recipe image to base64 url
	getBase64($('#recipe-image').attr('src'), function(dataUrl) {
		$('#recipe-image').attr('src' , dataUrl)
	});


	replaceIngredientsListBulletPointToCheckbox();
	RemoveEmptyMethodListElements();
	applyCheckboxFunctionality()
}