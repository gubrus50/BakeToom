function createCategoryInIngredientsForm() {
	$("#ingredientsForm").append('\
		<div class="p-3 mb-2 rounded" style="background-color: #e8e8e8">\
  	  	  <!-- Category Title -->\
		  <div class="form-group">\
		    <label>Tytuł kategorii</label>\
		    <input type="text" class="form-control">\
		  </div>\
		  <!-- Category Ingredients -->\
		  <div class="form-group">\
		    <label>Wprowadź listę składników do następującej kategorii</label>\
		    <textarea class="form-control" rows="3"></textarea>\
		  </div>\
		  <button type="button" class="btn btn-outline-danger" onclick="$(this).closest(\'div\').remove();">Usuń następującą kategorie</button>\
	  </div>\
	');
	return "Category has been successfully generated."
}