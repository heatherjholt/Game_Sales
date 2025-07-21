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

// toggle list/grid
function setView(view) {
  const grid = document.querySelector('.card-grid');
  const list = document.querySelector('.card-list');

  if (view === 'grid') {
    grid.style.display = 'flex';
    list.style.display = 'none';
  } else {
    grid.style.display = 'none';
    list.style.display = 'flex';
  }
}

