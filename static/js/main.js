/**
* Template Name: FlexStart - v1.9.0
* Template URL: https://bootstrapmade.com/flexstart-bootstrap-startup-template/
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/
(function() {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    if (all) {
      select(el, all).forEach(e => e.addEventListener(type, listener))
    } else {
      select(el, all).addEventListener(type, listener)
    }
  }

  /**
   * Easy on scroll event listener 
   */
  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
  }

  /**
   * Navbar links active state on scroll
   */
  let navbarlinks = select('#navbar .scrollto', true)
  const navbarlinksActive = () => {
    let position = window.scrollY + 200
    navbarlinks.forEach(navbarlink => {
      if (!navbarlink.hash) return
      let section = select(navbarlink.hash)
      if (!section) return
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        navbarlink.classList.add('active')
      } else {
        navbarlink.classList.remove('active')
      }
    })
  }
  window.addEventListener('load', navbarlinksActive)
  onscroll(document, navbarlinksActive)

  /**
   * Scrolls to an element with header offset
   */
  const scrollto = (el) => {
    let header = select('#header')
    let offset = header.offsetHeight

    if (!header.classList.contains('header-scrolled')) {
      offset -= 10
    }

    let elementPos = select(el).offsetTop
    window.scrollTo({
      top: elementPos - offset,
      behavior: 'smooth'
    })
  }

  /**
   * Toggle .header-scrolled class to #header when page is scrolled
   */
  let selectHeader = select('#header')
  if (selectHeader) {
    const headerScrolled = () => {
      if (window.scrollY > 100) {
        selectHeader.classList.add('header-scrolled')
      } else {
        selectHeader.classList.remove('header-scrolled')
      }
    }
    window.addEventListener('load', headerScrolled)
    onscroll(document, headerScrolled)
  }

  /**
   * Back to top button
   */
  let backtotop = select('.back-to-top')
  if (backtotop) {
    const toggleBacktotop = () => {
      if (window.scrollY > 100) {
        backtotop.classList.add('active')
      } else {
        backtotop.classList.remove('active')
      }
    }
    window.addEventListener('load', toggleBacktotop)
    onscroll(document, toggleBacktotop)
  }

  /**
   * Mobile nav toggle
   */
  on('click', '.mobile-nav-toggle', function(e) {
    select('#navbar').classList.toggle('navbar-mobile')
    this.classList.toggle('bi-list')
    this.classList.toggle('bi-x')
  })

  /**
   * Mobile nav dropdowns activate
   */
  on('click', '.navbar .dropdown > a', function(e) {
    if (select('#navbar').classList.contains('navbar-mobile')) {
      e.preventDefault()
      this.nextElementSibling.classList.toggle('dropdown-active')
    }
  }, true)

  /**
   * Scrool with ofset on links with a class name .scrollto
   */
  on('click', '.scrollto', function(e) {
    if (select(this.hash)) {
      e.preventDefault()

      let navbar = select('#navbar')
      if (navbar.classList.contains('navbar-mobile')) {
        navbar.classList.remove('navbar-mobile')
        let navbarToggle = select('.mobile-nav-toggle')
        navbarToggle.classList.toggle('bi-list')
        navbarToggle.classList.toggle('bi-x')
      }
      scrollto(this.hash)
    }
  }, true)

  /**
   * Scroll with ofset on page load with hash links in the url
   */
  window.addEventListener('load', () => {
    if (window.location.hash) {
      if (select(window.location.hash)) {
        scrollto(window.location.hash)
      }
    }
  });

  /**
   * Clients Slider
   */
  new Swiper('.clients-slider', {
    speed: 400,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false
    },
    slidesPerView: 'auto',
    pagination: {
      el: '.swiper-pagination',
      type: 'bullets',
      clickable: true
    },
    breakpoints: {
      320: {
        slidesPerView: 2,
        spaceBetween: 40
      },
      480: {
        slidesPerView: 3,
        spaceBetween: 60
      },
      640: {
        slidesPerView: 4,
        spaceBetween: 80
      },
      992: {
        slidesPerView: 6,
        spaceBetween: 120
      }
    }
  });

  /**
   * Porfolio isotope and filter
   */
  window.addEventListener('load', () => {
    let portfolioContainer = select('.portfolio-container');
    if (portfolioContainer) {
      let portfolioIsotope = new Isotope(portfolioContainer, {
        itemSelector: '.portfolio-item',
        layoutMode: 'fitRows'
      });

      let portfolioFilters = select('#portfolio-flters li', true);

      on('click', '#portfolio-flters li', function(e) {
        e.preventDefault();
        portfolioFilters.forEach(function(el) {
          el.classList.remove('filter-active');
        });
        this.classList.add('filter-active');

        portfolioIsotope.arrange({
          filter: this.getAttribute('data-filter')
        });
        aos_init();
      }, true);
    }

  });

  /**
   * Initiate portfolio lightbox 
   */
  const portfolioLightbox = GLightbox({
    selector: '.portfokio-lightbox'
  });

  /**
   * Portfolio details slider
   */
  new Swiper('.portfolio-details-slider', {
    speed: 400,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false
    },
    pagination: {
      el: '.swiper-pagination',
      type: 'bullets',
      clickable: true
    }
  });

  /**
   * Testimonials slider
   */
  new Swiper('.testimonials-slider', {
    speed: 600,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false
    },
    slidesPerView: 'auto',
    pagination: {
      el: '.swiper-pagination',
      type: 'bullets',
      clickable: true
    },
    breakpoints: {
      320: {
        slidesPerView: 1,
        spaceBetween: 40
      },

      1200: {
        slidesPerView: 3,
      }
    }
  });

  /**
   * Animation on scroll
   */
  function aos_init() {
    AOS.init({
      duration: 1000,
      easing: "ease-in-out",
      once: true,
      mirror: false
    });
  }
  window.addEventListener('load', () => {
    aos_init();
  });

})();

// Tags Input
// console.clear();

// $(function() {
//   $('input').on('change', function(event) {

//     var $element = $(event.target);
//     var $container = $element.closest('.example');

//     if (!$element.data('tagsinput'))
//       return;

//     var val = $element.val();
//     if (val === null)
//       val = "null";
//     var items = $element.tagsinput('items');
//     console.log(items[items.length - 1]);

//     $('code', $('pre.val', $container)).html(($.isArray(val) ? JSON.stringify(val) : "\"" + val.replace('"', '\\"') + "\""));
//     $('code', $('pre.items', $container)).html(JSON.stringify($element.tagsinput('items')));

//     console.log(val);
//     console.log(items);
//     console.log(JSON.stringify(val));
//     console.log(JSON.stringify(items));

//     console.log(items[items.length - 1]);

//   }).trigger('change');
// });


// var data =
// '[{ "value": 1, "text": "Task 1", "continent": "Task" }, { "value": 2, "text": "Task 2", "continent": "Task" }, { "value": 3, "text": "Task 3", "continent": "Task" }, { "value": 4, "text": "Task 4", "continent": "Task" }, { "value": 5, "text": "Task 5", "continent": "Task" }, { "value": 6, "text": "Task 6", "continent": "Task" } ]';

// //get data pass to json
// var task = new Bloodhound({
// datumTokenizer: Bloodhound.tokenizers.obj.whitespace("text"),
// queryTokenizer: Bloodhound.tokenizers.whitespace,
// local: jQuery.parseJSON(data) //your can use json type
// });

// task.initialize();

// var elt = $("#category");
// elt.tagsinput({
// itemValue: "value",
// itemText: "text",
// typeaheadjs: {
//   name: "task",
//   displayKey: "text",
//   source: task.ttAdapter()
// }
// });

$(function () {

  console.log($('#myTags').tagsValues())


})

function runSuggestions(element,query) {

  /*
  using ajax to populate suggestions
   */
  let sug_area=$(element).parents().eq(2).find('.autocomplete .autocomplete-items');
  $.getJSON("http://127.0.0.1:8000/buyer/buyer_category/", function( data ) {
      _tag_input_suggestions_data = data;
      $.each(data,function (key,value) {
          let template = $("<div>"+value.name+"</div>").hide()
          sug_area.append(template)
          template.show()

      })
  });

}

function runSuggestions_menufatcure(element,query) {

  /*
  using ajax to populate suggestions
   */
  let sug_area=$(element).parents().eq(2).find('.autocomplete .autocomplete-items');
  $.getJSON("http://127.0.0.1:8000/buyer/buyer_menufacture/", function( data ) {
      _tag_input_suggestions_data = data;
      $.each(data,function (key,value) {
          let template = $("<div>"+value.name+"</div>").hide()
          sug_area.append(template)
          template.show()

      })
  });

}

function runSuggestions_model(element,query) {

  /*
  using ajax to populate suggestions
   */
  let sug_area=$(element).parents().eq(2).find('.autocomplete .autocomplete-items');
  $.getJSON("http://127.0.0.1:8000/buyer/buyer_model/", function( data ) {
      _tag_input_suggestions_data = data;
      $.each(data,function (key,value) {
          let template = $("<div>"+value.name+"</div>").hide()
          sug_area.append(template)
          template.show()

      })
  });

}
/**
   * Initiate TinyMCE Editor
   */

 var useDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;

 tinymce.init({
   selector: 'textarea.tinymce-editor',
   plugins: 'print preview paste importcss searchreplace autolink autosave save directionality code visualblocks visualchars fullscreen image link media template codesample table charmap hr pagebreak nonbreaking anchor toc insertdatetime advlist lists wordcount imagetools textpattern noneditable help charmap quickbars emoticons',
   imagetools_cors_hosts: ['picsum.photos'],
   menubar: 'file edit view insert format tools table help',
   toolbar: 'undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist | forecolor backcolor removeformat | pagebreak | charmap emoticons | fullscreen  preview save print | insertfile image media template link anchor codesample | ltr rtl',
   toolbar_sticky: true,
   autosave_ask_before_unload: true,
   autosave_interval: '30s',
   autosave_prefix: '{path}{query}-{id}-',
   autosave_restore_when_empty: false,
   autosave_retention: '2m',
   image_advtab: true,
   link_list: [{
       title: 'My page 1',
       value: 'https://www.tiny.cloud'
     },
     {
       title: 'My page 2',
       value: 'http://www.moxiecode.com'
     }
   ],
   image_list: [{
       title: 'My page 1',
       value: 'https://www.tiny.cloud'
     },
     {
       title: 'My page 2',
       value: 'http://www.moxiecode.com'
     }
   ],
   image_class_list: [{
       title: 'None',
       value: ''
     },
     {
       title: 'Some class',
       value: 'class-name'
     }
   ],
   importcss_append: true,
   file_picker_callback: function(callback, value, meta) {
     /* Provide file and text for the link dialog */
     if (meta.filetype === 'file') {
       callback('https://www.google.com/logos/google.jpg', {
         text: 'My text'
       });
     }

     /* Provide image and alt text for the image dialog */
     if (meta.filetype === 'image') {
       callback('https://www.google.com/logos/google.jpg', {
         alt: 'My alt text'
       });
     }

     /* Provide alternative source and posted for the media dialog */
     if (meta.filetype === 'media') {
       callback('movie.mp4', {
         source2: 'alt.ogg',
         poster: 'https://www.google.com/logos/google.jpg'
       });
     }
   },
   templates: [{
       title: 'New Table',
       description: 'creates a new table',
       content: '<div class="mceTmpl"><table width="98%%"  border="0" cellspacing="0" cellpadding="0"><tr><th scope="col"> </th><th scope="col"> </th></tr><tr><td> </td><td> </td></tr></table></div>'
     },
     {
       title: 'Starting my story',
       description: 'A cure for writers block',
       content: 'Once upon a time...'
     },
     {
       title: 'New list with dates',
       description: 'New List with dates',
       content: '<div class="mceTmpl"><span class="cdate">cdate</span><br /><span class="mdate">mdate</span><h2>My List</h2><ul><li></li><li></li></ul></div>'
     }
   ],
   template_cdate_format: '[Date Created (CDATE): %m/%d/%Y : %H:%M:%S]',
   template_mdate_format: '[Date Modified (MDATE): %m/%d/%Y : %H:%M:%S]',
   height: 600,
   image_caption: true,
   quickbars_selection_toolbar: 'bold italic | quicklink h2 h3 blockquote quickimage quicktable',
   noneditable_noneditable_class: 'mceNonEditable',
   toolbar_mode: 'sliding',
   contextmenu: 'link image imagetools table',
   skin: useDarkMode ? 'oxide-dark' : 'oxide',
   content_css: useDarkMode ? 'dark' : 'default',
   content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:14px }'
 });



//insert data to input in load page
// elt.tagsinput("add", {
//   value: 1,
//   text: "task 1",
//   continent: "task"
// });


// $('input[name="category"]').amsifySuggestags({
//   suggestions: ['Apple', 'Banana', 'Cherries', 'Dates', 'Guava'], 
//   whiteList: true,
//   afterAdd : function(value) {
//     console.info(value);
//   },
//   afterRemove : function(value) {
//     console.info(value);
//   },
// });
 
 
//buyer Form
$(document).ready(function (e) {
	$("#buyer_form").on('submit',(function(e) {
	 e.preventDefault();
	 $.ajax({
	 url: '/buyer/buyer_inquiry_form/',
	  type: "POST",
	  data:  new FormData(this),
	  contentType: false,
			cache: false,
	  processData:false,
	  
	  success: function(data)
		 {
	   if(data.error)
        {
        // invalid file format.
        $("error-message").show();
        }
	   else
        {
            // view uploaded file.
            $(".sent-message").show();
            $("#buyer_form")[0].reset(); 
            // location.reload();
            }
		 },
		          
	   });
	}));
});

//Vendor Form
$(document).ready(function (e) {
	$("#vendor_form").on('submit',(function(e) {
	 e.preventDefault();
	 $.ajax({
	 url: '/vendor/vendor_inquiry_form/',
	  type: "POST",
	  data:  new FormData(this),
	  contentType: false,
			cache: false,
	  processData:false,
	  
	  success: function(data)
		 {
	   if(data.error)
        {
        // invalid file format.
        $("error-message").show();
        }
	   else
        {
            // view uploaded file.
            $(".sent-message").show();
            //$("#vendor_form")[0].reset(); 
            // location.reload();
            }
		 },
		          
	   });
	}));
});


   //subtract logic
$(document).ready(function() {
    if($("#vendor_form").length){
        $( "#sub_total" ).keyup(function() {
            $.sum();          
        }); 
        $( "#discount" ).keyup(function() {
            $.sum();          
        }); 
     }   
        $.sum = function(){
            $("#total").val(parseInt($("#sub_total").val()) -     parseInt($("#discount").val()));
        } 
});



