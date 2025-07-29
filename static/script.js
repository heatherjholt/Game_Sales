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

//toggle list/grid
const gridWrapper = document.getElementById('gridWrapper');
const listWrapper = document.getElementById('listWrapper');

  

function setView(view) {
  const grid = document.getElementById('gridWrapper');
  const list = document.getElementById('listWrapper');
  const sortControls = document.getElementById('sortControlsGrid');

  if (view === 'grid') {
    grid.style.display        = 'block';
    list.style.display        = 'none';
    sortControls.style.display= 'block';
  } else {
    grid.style.display        = 'none';
    list.style.display        = 'block';
    sortControls.style.display= 'none';
  }
}

//when user picks a sort option, reload with ?sort=...
document.getElementById('sortSelect').addEventListener('change', function() {
  const val = this.value;
  const url = new URL(window.location);
  if (val) url.searchParams.set('sort', val);
  else     url.searchParams.delete('sort');
    const view = document.getElementById('gridWrapper').style.display === 'block'
        ? 'grid'
        : 'list';
    url.searchParams.set('view', view);
  window.location.href = url.toString();
});