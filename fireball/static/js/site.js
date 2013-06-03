/**
 * Based on Wookmark's endless scroll.
 */
$(window).ready(function () {
    var apiURL = '/api/blobs/recent/'
    var page = 1;
    var handler = null;
    var isLoading = false;
    
    /**
     * When scrolled all the way to the bottom, add more tiles.
     */
    function onScroll(event) {
      if(!isLoading) {
          var closeToBottom = ($(window).scrollTop() + $(window).height() > $(document).height() - 100);
          if(closeToBottom) loadData();
      }
    };
    
    function applyLayout() {
      $('#blobs').imagesLoaded(function() {
          // Clear our previous layout handler.
          if(handler) handler.wookmarkClear();
          
          // Create a new layout handler.
          handler = $('#blobs .blob');
          handler.wookmark({
              autoResize: true,
              /** container: $('#content'), */
              offset: 12,
              itemWidth: 232,
          });
      });
    };
    
    /**
     * Loads data from the API.
     */
    function loadData() {
        isLoading = true;
        $('#loader').show();
        
        $.ajax({
            url: apiURL+page,
            success: onLoadData
        });
    };
    
    /**
     * Receives data from the API, creates HTML for images and updates the layout
     */
    function onLoadData(data) {
        isLoading = false;
        $('#loader').hide();
        
        page++;
        
        var html = '';
        var i=0, length=data.length, image;
        for(; i<length; i++) {
          image = data[i];
          html += '<div class="blob">';
              html += '<div class="blob-options">';
                  html += '<a href="/blobs/delete-blob/'+image.id+'">';
                      html += '<i class="icon-trash"></i>';
                  html += '</a>';
                  
                  html += '<a class="fancybox" rel="blobs" href="'+image.image+'">';
                      html += '<i class="icon-zoom-in"></i>';
                  html += '</a>';
                 
              html += '</div>';
              html += '<a class="fancybox" rel="blobs" href="'+image.image+'">';
                  html += '<div class="photo"><img src="'+image.thumbnail+'" width="200" ></div>';
              html += '</a>';
              html += '<div class="meta"><a href="#"class="description">'+image.description+'</a>';
              html += '<img id="avatar" width="16" height="16" src="https://secure.gravatar.com/avatar/'+image.email_hash+'?s=24" />';
              html += '<span class="username">by '+image.username+'</span></div>';
          html += '</div>';
        }
        
        $('div#blobs').append(html);
        
        applyLayout();
    };
  
    $(document).ready(new function() {
        $(document).bind('scroll', onScroll);
        loadData();
    });

    /**
     * On clicking an image show fancybox original.
     */
    $('.fancybox').fancybox({
        openEffect: 'none',
        closeEffect: 'none'
    });


	(function($){
		$.fn.fadeable = function(options){
	
			var settings = {
				target: this,
				duration: 'fast'
			};
			$.extend(settings, options)
	
			$(this).live('hover', function(event) {
				switch(event.type){
					case 'mouseenter':
						$(this).find(settings.target).stop().fadeTo(settings.duration, 1);
						break;
					case 'mouseleave':
						$(this).find(settings.target).stop().fadeTo(settings.duration, 0);
						break;
				}
			});
		}
	})(jQuery);
	
	// show screenblob info on hover
	$('div.photo').fadeable({target: 'a.description-over'});
	
});
