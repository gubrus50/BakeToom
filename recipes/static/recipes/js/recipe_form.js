var category_count = 0;
function createCategoryInIngredientsForm(loop)
{
	for (i=0; i<loop; i++) {
		$("#ingredientsForm").append('\
			<div class="p-3 mb-2 rounded recipe-category">\
			  <!-- Category Title -->\
			  <div class="form-group">\
			    <label>Tytuł kategorii</label>\
			    <input type="text" name="category" maxlength="100" class="form-control" required>\
			  </div>\
			  <br/><br/>\
			  <!-- Category Ingredients -->\
			  <div class="form-group custom-scroll empty-h-scroll">\
			    <label>Wprowadź listę składników do następującej kategorii</label>\
			    <textarea name="ingredients" maxlength="500" class="form-control" rows="3" required></textarea>\
			  </div>\
			  <button type="button" class="btn btn-outline-danger" onclick="category_count--;updateCategoryButtonInIngredientsForm(); $(this).closest(\'div\').remove();">Usuń kategorie</button>\
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



window.onload = function() 
{
	createCategoryInIngredientsForm(category_creation_count)
	importCategories(categories, ingredients)
	$('textarea').addClass('custom-scroll empty-h-scroll')
}