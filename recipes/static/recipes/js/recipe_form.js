var category_count = 0;
function createCategoryInIngredientsForm(loop)
{
	for (i=0; i<loop; i++) {
		$("#ingredients-form").append('\
			<div class="rounded recipe-category">\
			  <!-- Category Title -->\
			  <div class="form-group">\
			    <label>Tytuł kategorii</label>\
			    <input type="text" name="category" maxlength="100" class="form-control" required>\
			  </div>\
			  <br/>\
			  <!-- Category Ingredients -->\
			  <div class="form-group">\
			    <label>Wprowadź listę składników do następującej kategorii</label>\
			    <textarea name="ingredients" maxlength="500" class="form-control" rows="10" required></textarea>\
			  </div>\
			  <button type="button" class="btn btn-outline-danger w-100" onclick="category_count--;updateCategoryButtonInIngredientsForm(); $(this).closest(\'div\').remove();">Usuń kategorie</button>\
			</div>\
		');
		category_count++
	}
	return "Category has been successfully generated."
}



function importCategories(c, i)
{
	// c = categories list
	// i = ingredients list

	if (c==null||i==null) { return }

	else if (c.length!=i.length) {
		console.log("ERROR - Categories length must equal to ingredients domain")
	}

	else {
		$("input[name=category]").each(function(index) {
			$(this).val(c[index])
		});
		$("textarea[name=ingredients]").each(function(index){
			$(this).val(i[index])
		})
	}
}



/* Determine if #create-category-btn should be disabled */
function updateCategoryButtonInIngredientsForm()
{
	var btn = $("#create-category-btn");

	if (category_count>8) {
		btn.prop('disabled', true)
	} else { 
		btn.prop('disabled', false)
	}
}



function forLicenseInclude(year, fullname)
{
	$('#id_license')
	.val(
		$('#id_license')
			.val()
			.replace(/\[rok\]/g, year)
			.replace(/\[pełne imię i nazwisko\]/g, fullname)
	)
}



window.onload = function() 
{
	createCategoryInIngredientsForm(category_creation_count);
	importCategories(categories, ingredients);
	forLicenseInclude(new Date().getFullYear(), user_fullname);
	$('textarea').addClass('custom-scroll empty-h-scroll')
}