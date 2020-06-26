function createEmptyCategoryObject() {
	var categories_count = $('.recipe-category').length;
	if (categories_count >= categories_max_num) {
		updateCreateCategoryBtn(); return;
	}

	var delete_label = "Usuń";
	if (recipe_id) { category_value = 'value="'+recipe_id+'"' }
	else { category_value = '' }

	$("#ingredients-form").append('\
		<div class="recipe-category">\
		  <div id="div_id_category_set-'+categories_count+'-name" class="form-group">\
		    <label for="id_category_set-'+categories_count+'-name" class="">'+categories_name_label+'</label>\
		    <div class="">\
		      <input type="text" name="category_set-'+categories_count+'-name" maxlength="100" class="textinput textInput form-control" id="id_category_set-'+categories_count+'-name">\
		    </div>\
		  </div>\
		  <div id="div_id_category_set-'+categories_count+'-ingredients" class="form-group">\
		    <label for="id_category_set-'+categories_count+'-ingredients" class=" requiredField">'+categories_ingredients_label+'</label>\
		    <div class="">\
		      <textarea name="category_set-'+categories_count+'-ingredients" cols="40" rows="10" maxlength="500" class="textarea form-control custom-scroll empty-h-scroll" id="id_category_set-'+categories_count+'-ingredients"></textarea>\
		    </div>\
		  </div>\
		  <input type="hidden" name="category_set-'+categories_count+'-id" id="id_category_set-'+categories_count+'-id">\
		  <div class="form-group">\
		    <div id="div_id_category_set-'+categories_count+'-DELETE" class="form-check">\
		      <input type="checkbox" name="category_set-'+categories_count+'-DELETE" class="checkboxinput form-check-input" id="id_category_set-'+categories_count+'-DELETE">\
		        <label for="id_category_set-'+categories_count+'-DELETE" class="form-check-label">'+delete_label+'</label>\
		      </div>\
		    </div>\
		    <input type="hidden" name="category_set-'+categories_count+'-recipe" '+recipe_id+' id="id_category_set-'+categories_count+'-recipe">\
		  </div>\
		</div>\
	')
}



/* Determine if #create-category-btn should be disabled */
function updateCreateCategoryBtn()
{
	var categories_count = $('.recipe-category').length;
	var btn = $("#create-category-btn");

	if (categories_count >= categories_max_num) {
		btn.prop('disabled', true)
	} else { 
		btn.prop('disabled', false)
	}
}



function setYearAndFullnameAtLicense(year, fullname)
{
	$('#id_license')
	.val(
		$('#id_license')
			.val()
			.replace(/\[year\]/g, year)
			.replace(/\[fullname\]/g, fullname)
	)
}



window.onload = function() 
{
	$('.recipe-category').each(function(index){
		var name = $('#id_category_set-'+index+'-name');
		var ingr = $('#id_category_set-'+index+'-ingredients');

		if (name.is(':empty') && ingr.is(':empty')) {
			$(this).remove();
		}
	});

	updateCreateCategoryBtn();
	setYearAndFullnameAtLicense(new Date().getFullYear(), user_fullname);
	$('textarea').addClass('custom-scroll empty-h-scroll');
}