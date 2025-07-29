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

  
    //check if view is set in URL and default to grid if not
function setView(view) {
  const grid         = document.getElementById('gridWrapper');
  const list         = document.getElementById('listWrapper');
  const sortControls = document.getElementById('sortControlsGrid');

  //update the URL so `?view=grid` or list stays in the address bar
  const url = new URL(window.location);
  url.searchParams.set('view', view);
  window.history.replaceState(null, '', url);
    //update the view in the gui
  const viewInput = document.querySelector('#sortControlsGrid input[name="view"]');
  if (viewInput) viewInput.value = view;
    //show/hide the grid or list based on the view
  if (view === 'grid') {
    grid.style.display         = 'block';
    list.style.display         = 'none';
    sortControls.style.display = 'block';
  } else {
    grid.style.display         = 'none';
    list.style.display         = 'block';
    sortControls.style.display = 'none';
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