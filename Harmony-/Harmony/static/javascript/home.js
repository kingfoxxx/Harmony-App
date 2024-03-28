document.addEventListener('DOMContentLoaded', function () {
    // Get the current page URL
    var currentPage = window.location.href;
    var menuItems = document.querySelectorAll('.menu-item');
    
    
    // Select the menu item based on the current page
    var menuItem = document.querySelector('a[href="' + currentPage + '"]');
    console.log(menuItem);
    // Add the "active" class if a matching menu item is found
    if (menuItem) {
        menuItem.classList.add('App__category-item--selected');
    }
});


$(document).ready(function () {
  $("#searchInput").on("input", function () {
      const searchTerm = $(this).val();
      $.ajax({
          url: "search", 
          method: "get", 
          data: { q: searchTerm },
          success: function (response) {
              // Update the artist and track sections in the template
              $(".artist_box").empty();
              $(".App__section-grid-container").empty();

              // Populate the artist section
              response.artists.items.forEach(function(artist) {
                  $(".artist_box").append(`
                    <a href='${artist.external_urls.spotify}'> 
                      <div class="App__section-grid-item">
                          <div class="featured-image" style="background-image: url('${artist.images[0].url}')"></div>
                          <h3>${artist.name}</h3>
                          <span>NPR</span>
                      </div>
                      </a>
                  `);
              });

              // Populate the track section
              response.tracks.items.forEach(function(track) {
                  $(".App__section-grid-container").append(`
                     <a href='${track.external_urls.spotify}'> 
                      <div class="App__section-grid-item">
                          <div class="featured-image" style="background-image: url('${track.album.images[0].url}')"></div>
                          <h3>${track.name}</h3>
                          <span>
                              ${track.artists.map(artist => artist.name).join(', ')}
                          </span>
                      </div>
                      </a>
                  `);
              });
          },
          error: function (error) {
              console.error("Error:", error);
          }
      });
  });

 //this navigates logout from home page of application 
});
$('#logout').on('click',(e)=>{
  e.preventDefault();
  $('#logoutform').submit();
});