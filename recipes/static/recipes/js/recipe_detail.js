/* Applies scrolls if category ingredients
   content is on word-break             */
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


/* Expands/shrinks method list by applying/removing break tags */
function updateMethodListBreaks(checkbox) {
	var rml = $('#recipe-method-list').children().eq(2);

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


/* Includes chebox bulletpoint for each list
   element from categories ingredients    */
function replaceIngredientsList() {
	var ingredients_list = []

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
	return ingredients_list
}


/* Removes null/spaced objects from the method list */
function replaceMethodList() {
	// Get list
	var new_method_list = []
	var method_data = $('#recipe-method-list > p').html();
	var method_list = method_data.split('<br>');

	for (var i=0; i<method_list.length; i++) {
		// Remove linenumbers
		method_list[i]=method_list[i].replace(/^.+?\./g,'')
		// Populate new_method_list with existing data
	    if (!method_list[i] 
	    || 	method_list[i]===''
	    || 	/^\s+$/g.test(method_list[i]))
	    {} else {
	    	new_method_list.push(method_list[i])
	    }
	}

	// Apply linenumbers for each element from method_list
	var linenumbers = new_method_list.length.toString().replace(/\d/g,'0')
	for (var i=0; i<new_method_list.length; i++) {
		x = linenumbers
		x = x.slice((i+1).toString().length)
		new_method_list[i]= x + (i+1) + '.' + new_method_list[i]+'<br>'
	}

	$('#recipe-method-list > p').html(new_method_list)
}


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
	replaceIngredientsList()
	replaceMethodList()

	/* Fancy checkbox button functionality */
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
	            };

	        // Event Handlers
	        $button.on('click', function () {
	            $checkbox.prop('checked', !$checkbox.is(':checked'));
	            $checkbox.triggerHandler('change');
	            updateDisplay();
	        });
	        $checkbox.on('change', function () {
	            updateDisplay();
	        });

	        // Actions
	        function updateDisplay() {
	            var isChecked = $checkbox.is(':checked');

	            // Set the button's state
	            $button.data('state', (isChecked) ? "on" : "off");

	            // Set the button's icon
	            $button.find('.state-icon')
	                .removeClass()
	                .addClass('state-icon ' + settings[$button.data('state')].icon);

	            // Update the button's color
	            if (isChecked) {
	                $button
	                    .removeClass('btn-default')
	                    .addClass('btn-' + color + ' active');
	            }
	            else {
	                $button
	                    .removeClass('btn-' + color + ' active')
	                    .addClass('btn-default');
	            }
	        }
	    });
	});
}

window.onresize = function(event) {
    applyApropiateScrolls()
}