(function ($) {

  /* Global Function */
  $(document).on('blur', 'input', function() {
    if ($(this).val().length > 0)
      $(this).removeClass('btn-danger');
  });

  /* Login Page */
  $('#login').find('form').on('submit', function(event) {
    var self = $(this),
        input_1 = self.find('input').first(),
        input_2 = self.find('input').last();

    if (input_1.val().length === 0) {
      input_1.addClass('btn-danger');
      return false;
    } else if (input_2.val().length === 0) {
      input_2.addClass('btn-danger');
      return false;
    } else {
      return true;
    }

  });// end login function

  $('#category-add-toggle').on('click', function () {
    func.toggle_cat_add($(this));
  });

  $('#category-add-submit').on('click', function () {
    var cat_input = $(this).parent().find('input'),
        cat_name = cat_input.val();

    func.add_new_cat(cat_name);
    cat_input.val('');
  });


})(jQuery);

var func = {
  debug : true,

  toggle_cat_add: function($target) {
    $target.parent().next('#category-add').toggleClass('hide');
  },

  add_new_cat: function (cat_name) {
    var self = this;

    $.ajax({
      type: 'POST',
      url: "/admin/category/add",
      dataType: 'JSON',
      data: {
        cat_name: cat_name
      },
      success: function(data) {
        if (self.debug) console.log(data);
        self.build_cat_check_box(data.cat_id, data.cat_name);
        $('#category-add-toggle').trigger('click');
      }
    });
  },

  build_cat_check_box: function (cat_id, cat_name) {
    var html = "<div class='checkbox anim-checkbox'>" +
               "<input type='checkbox' id='" + cat_id + "' class='primary'>" +
               "<label for='" + cat_id + "'>" + cat_name + "</label>" +
               "</div>";

    $(html).prependTo('#category_list');
  }
}