var category_count = 1;
function createCategoryInIngredientsForm() {
	$("#ingredientsForm").append('\
		<div class="p-3 mb-2 rounded recipe-category">\
  	  	  <!-- Category Title -->\
		  <div class="form-group">\
		    <label>Tytuł kategorii</label>\
		    <input type="text" name="category" maxlength="100" class="form-control" required>\
		  </div>\
		  <br/><br/>\
		  <!-- Category Ingredients -->\
		  <div class="form-group empty-scroll">\
		    <label>Wprowadź listę składników do następującej kategorii</label>\
		    <textarea name="ingredients" maxlength="240" class="form-control" rows="3" required></textarea>\
		  </div>\
		  <button type="button" class="btn btn-outline-danger" onclick="category_count--;updateCategoryButtonInIngredientsForm(); $(this).closest(\'div\').remove();">Usuń kategorie</button>\
	  </div>\
	');

	category_count++;
	return "Category has been successfully generated."
}

function updateCategoryButtonInIngredientsForm() {
	var btn = $("#create-category-btn");
	// Determine if #create-category-btn should be disabled
	// (This function occurs only in new_recipe.html template)
	if (category_count>8) {
		btn.prop('disabled', true)
	} else { btn.prop('disabled', false) }
}