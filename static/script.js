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
        const selectedTitle = $(this).text();
        $('#search-input').val(selectedTitle);
        $('#suggestions').empty();
        window.location.href = '/search?title=' + encodeURIComponent(selectedTitle);  //redirect to /search
        });
      });
    } else {
      $('#suggestions').empty();
    }
  });
});

