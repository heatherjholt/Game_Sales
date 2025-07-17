$(document).ready(function () {
  $('#search-input').on('input', function () {
    let query = $(this).val();
    if (query.length > 1) {
      $.get('/autocomplete', { q: query }, function (data) {
        let suggestions = $('#suggestions');
        suggestions.empty();
        data.forEach(function (item) {
          suggestions.append(`<li>${item}</li>`);
        });
        $('ul#suggestions li').click(function () {
          $('#search-input').val($(this).text());
          $('#suggestions').empty();
        });
      });
    } else {
      $('#suggestions').empty();
    }
  });
});


