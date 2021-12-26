/**
* Template Name: NiceAdmin - v2.1.0
* Template URL: https://bootstrapmade.com/nice-admin-bootstrap-admin-html-template/
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
   * Sidebar toggle
   */
  if (select('.toggle-sidebar-btn')) {
    on('click', '.toggle-sidebar-btn', function(e) {
      select('body').classList.toggle('toggle-sidebar')
    })
  }

  /**
   * Search bar toggle
   */
  if (select('.search-bar-toggle')) {
    on('click', '.search-bar-toggle', function(e) {
      select('.search-bar').classList.toggle('search-bar-show')
    })
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
   * Initiate tooltips
   */
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  })

  /**
   * Initiate quill editors
   */
  if (select('.quill-editor-default')) {
    new Quill('.quill-editor-default', {
      theme: 'snow'
    });
  }

  if (select('.quill-editor-bubble')) {
    new Quill('.quill-editor-bubble', {
      theme: 'bubble'
    });
  }

  if (select('.quill-editor-full')) {
    new Quill(".quill-editor-full", {
      modules: {
        toolbar: [
          [{
            font: []
          }, {
            size: []
          }],
          ["bold", "italic", "underline", "strike"],
          [{
              color: []
            },
            {
              background: []
            }
          ],
          [{
              script: "super"
            },
            {
              script: "sub"
            }
          ],
          [{
              list: "ordered"
            },
            {
              list: "bullet"
            },
            {
              indent: "-1"
            },
            {
              indent: "+1"
            }
          ],
          ["direction", {
            align: []
          }],
          ["link", "image", "video"],
          ["clean"]
        ]
      },
      theme: "snow"
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

  /**
   * Initiate Bootstrap validation check
   */
  var needsValidation = document.querySelectorAll('.needs-validation')

  Array.prototype.slice.call(needsValidation)
    .forEach(function(form) {
      form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      }, false)
    })

  /**
   * Initiate Datatables
   */
  const datatables = select('.datatable', true)
  datatables.forEach(datatable => {
    new simpleDatatables.DataTable(datatable);
  })

  /**
   * Autoresize echart charts
   */
  const mainContainer = select('#main');
  if (mainContainer) {
    setTimeout(() => {
      new ResizeObserver(function() {
        select('.echart', true).forEach(getEchart => {
          echarts.getInstanceByDom(getEchart).resize();
        })
      }).observe(mainContainer);
    }, 200);
  }

})();

//vendor submit form js
//Vendor Form
$(document).ready(function (e) {
	$("#add_vendor").on('submit',(function(e) {
	 e.preventDefault();
	 $.ajax({
	 url: '/vendor/add_vendor/',
	  type: "POST",
	  data:  new FormData(this),
	  contentType: false,
			cache: false,
	  processData:false,
	  
	  success: function(data)
		 {
	   if(data == "error")
        {
        // invalid file format.
        $(".alert-danger").show();
        }
	   else
        {
            // view uploaded file.
            $(".alert-success").show();
            $("#add_vendor")[0].reset(); 
            // location.reload();
            }
		 },
		          
	   });
	}));
});

//update email vendor
$(function() {

	$('.vendor_edit_form').on('click',function(){
	  
	  var email = $(this).data('email');    
	  var id = $(this).data('id');   
	  // AJAX request  
	  $(".pop_id").val(id); 
	  $("#email").val(email);  
	});
});

$(document).ready(function () {
	$("#my-form").submit(function (e) {  
    e.preventDefault(); // Cancel the default action  
   let id = $('#id').val();
   $.ajax({
    url: "/vendor/update_vendor_email/" + id + "/",
    type: "POST",
    data:  new FormData(this),
    contentType: false,
      cache: false,
    processData:false,
    beforeSend : function()
    {
     //$("#preview").fadeOut();
     $("#err").fadeOut();
    },
    success: function(data)
       {
       if(data == "error")
       {
        $(".alert-danger").show();
       }
       else
       {
        // view uploaded file.
        $(".alert-primary").show(); 
        location.reload();
       }
       },
          
     });
  });
});


$(document).ready(function () {
	$("#my-form-edit-email").submit(function (e) {  
    e.preventDefault(); // Cancel the default action  
   let id = $('#id').val();
   $.ajax({
    url: "/vendor/add_vendor_email/" + id + "/",
    type: "POST",
    data:  new FormData(this),
    contentType: false,
      cache: false,
    processData:false,
    beforeSend : function()
    {
     //$("#preview").fadeOut();
     $("#err").fadeOut();
    },
    success: function(data)
       {
       if(data == "error")
       {
        $(".alert-danger").show();
       }
       else
       {
        // view uploaded file.
        $(".alert-primary").show(); 
        location.reload();
       }
       },
          
     });
  });
});

//update Category vendor
$(function() {

	$('.vendor_edit_category').on('click',function(){
	  
	  var category = $(this).data('category');    
	  var id = $(this).data('id');   
	  // AJAX request  
	  $(".pop_id").val(id); 
	  $("#category").val(category);  
	});
});

$(document).ready(function () {
	$("#my-form-category").submit(function (e) {  
    e.preventDefault(); // Cancel the default action 
   let id = $('#id').val();
   $.ajax({
    url: "/vendor/update_vendor_category/" + id + "/",
    type: "POST",
    data:  new FormData(this),
    contentType: false,
      cache: false,
    processData:false,
    beforeSend : function()
    {
     //$("#preview").fadeOut();
     $("#err").fadeOut();
    },
    success: function(data)
       {
       if(data == "error")
       {
        $(".alert-danger").show();
       }
       else
       {
        // view uploaded file.
        $(".alert-primary").show(); 
        location.reload();
       }
       },
          
     });
  });
});

$(document).ready(function () {
	$("#my-form-add-category").submit(function (e) {  
    e.preventDefault(); // Cancel the default action 
   let id = $('#id').val();
   $.ajax({
    url: "/vendor/add_vendor_category/" + id + "/",
    type: "POST",
    data:  new FormData(this),
    contentType: false,
      cache: false,
    processData:false,
    beforeSend : function()
    {
     //$("#preview").fadeOut();
     $("#err").fadeOut();
    },
    success: function(data)
       {
       if(data == "error")
       {
        $(".alert-danger").show();
       }
       else
       {
        // view uploaded file.
        $(".alert-primary").show(); 
        location.reload();
       }
       },
          
     });
  });
});
 
//update Menufacture vendor
$(function() {

	$('.vendor_edit_menufacture').on('click',function(){
	  
	  var menufacture = $(this).data('menufacture');    
	  var id = $(this).data('id');   
	  // AJAX request  
	  $(".pop_id").val(id); 
	  $("#menufacture").val(menufacture);  
	});
});

$(document).ready(function () {
	$("#my-form-menufacture").submit(function (e) {  
    e.preventDefault(); // Cancel the default action 
   let id = $('#id').val();
   $.ajax({
    url: "/vendor/update_vendor_menufacture/" + id + "/",
    type: "POST",
    data:  new FormData(this),
    contentType: false,
      cache: false,
    processData:false,
    beforeSend : function()
    {
     //$("#preview").fadeOut();
     $("#err").fadeOut();
    },
    success: function(data)
       {
       if(data == "error")
       {
        $(".alert-danger").show();
       }
       else
       {
        // view uploaded file.
        $(".alert-primary").show(); 
        location.reload();
       }
       },
          
     });
  });
});

$(document).ready(function () {
	$("#my-form-add-menufacture").submit(function (e) {  
    e.preventDefault(); // Cancel the default action 
   let id = $('#id').val();
   $.ajax({
    url: "/vendor/add_vendor_menufacture/" + id + "/",
    type: "POST",
    data:  new FormData(this),
    contentType: false,
      cache: false,
    processData:false,
    beforeSend : function()
    {
     //$("#preview").fadeOut();
     $("#err").fadeOut();
    },
    success: function(data)
       {
       if(data == "error")
       {
        $(".alert-danger").show();
       }
       else
       {
        // view uploaded file.
        $(".alert-primary").show(); 
        location.reload();
       }
       },
          
     });
  });
});

//update Model vendor
$(function() {

	$('.vendor_edit_model').on('click',function(){
	  
	  var model = $(this).data('model');    
	  var id = $(this).data('id');   
	  // AJAX request  
	  $(".pop_id").val(id); 
	  $("#model").val(model);  
	});
});

$(document).ready(function () {
	$("#my-form-model").submit(function (e) {  
    e.preventDefault(); // Cancel the default action 
   let id = $('#id').val();
   $.ajax({
    url: "/vendor/update_vendor_model/" + id + "/",
    type: "POST",
    data:  new FormData(this),
    contentType: false,
      cache: false,
    processData:false,
    beforeSend : function()
    {
     //$("#preview").fadeOut();
     $("#err").fadeOut();
    },
    success: function(data)
       {
       if(data == "error")
       {
        $(".alert-danger").show();
       }
       else
       {
        // view uploaded file.
        $(".alert-primary").show(); 
        location.reload();
       }
       },
          
     });
  });
});


$(document).ready(function () {
	$("#my-add-form-model").submit(function (e) {  
    e.preventDefault(); // Cancel the default action 
   let id = $('#id').val();
   $.ajax({
    url: "/vendor/add_vendor_model/" + id + "/",
    type: "POST",
    data:  new FormData(this),
    contentType: false,
      cache: false,
    processData:false,
    beforeSend : function()
    {
     //$("#preview").fadeOut();
     $("#err").fadeOut();
    },
    success: function(data)
       {
       if(data == "error")
       {
        $(".alert-danger").show();
       }
       else
       {
        // view uploaded file.
        $(".alert-primary").show(); 
        location.reload();
       }
       },
          
     });
  });
});

//update Image Buyer
$(function() {

	$('.buyer_update_image_model').on('click',function(){
	      
	  var id = $(this).data('id');   
	  // AJAX request  
	  $(".pop_id").val(id);  
	});
});

$(document).ready(function () {
	$("#my-form-update-buyer-attachment").submit(function (e) {  
    e.preventDefault(); // Cancel the default action 
   let id = $('#id').val();
   $.ajax({
    url: "/buyer/update_buyer_attachment/" + id + "/",
    type: "POST",
    data:  new FormData(this),
    contentType: false,
      cache: false,
    processData:false,
    beforeSend : function()
    {
     //$("#preview").fadeOut();
     $("#err").fadeOut();
    },
    success: function(data)
       {
       if(data == "error")
       {
        $(".alert-danger").show();
       }
       else
       {
        // view uploaded file.
        $(".alert-primary").show(); 
        location.reload();
       }
       },
          
     });
  });
});

  //update vendor

  $(document).ready(function () {
    $("#update_vendor").submit(function(e){ 
     let vendor_id = $('#vendor_id').val();
     $.ajax({
      url: "/vendor/edit_vendor/" + vendor_id + "/",
      type: "POST",
      data:  new FormData(this),
      contentType: false,
        cache: false,
      processData:false,
       
      success: function(data)
       {
       if(data == "error")
       {
        $(".alert-danger").show();
       }
       else
       {
        // view uploaded file.
        $(".alert-success").show(); 
        // location.reload();
       }
       },
                
       });
    });
});

//Buyer submit form js
//Buyer Form
$(document).ready(function (e) {
	$("#add_buyer").on('submit',(function(e) {
	 e.preventDefault();
	 $.ajax({
	 url: '/buyer/add_buyer/',
	  type: "POST",
	  data:  new FormData(this),
	  contentType: false,
			cache: false,
	  processData:false,
	  
	  success: function(data)
		 {
	   if(data == "error")
        {
        // invalid file format.
        $(".alert-danger").show();
        }
	   else
        {
            // view uploaded file.
            $(".alert-success").show();
            $("#add_buyer")[0].reset(); 
            // location.reload();
        }
		 },
		          
	   });
	}));
});

//buyer-email-form
$(document).ready(function () {
	$("#my-form-email").submit(function (e) {  
    e.preventDefault(); // Cancel the default action 
   let id = $('#id').val();
   $.ajax({
    url: "/buyer/update_buyer_email/" + id + "/",
    type: "POST",
    data:  new FormData(this),
    contentType: false,
      cache: false,
    processData:false, 
    success: function(data)
       {
       if(data == "error")
       {
        $(".alert-danger").show();
       }
       else
       {
        // view uploaded file.
        $(".alert-primary").show(); 
        location.reload();
       }
       },
          
     });
  });
});

$(document).ready(function () {
	$("#my-buyer-form-email").submit(function (e) {  
    e.preventDefault(); // Cancel the default action 
   let id = $('#id').val();
   $.ajax({
    url: "/buyer/add_buyer_email/" + id + "/",
    type: "POST",
    data:  new FormData(this),
    contentType: false,
      cache: false,
    processData:false, 
    success: function(data)
       {
       if(data == "error")
       {
        $(".alert-danger").show();
       }
       else
       {
        // view uploaded file.
        $(".alert-primary").show(); 
        location.reload();
       }
       },
          
     });
  });
});

//Buyer Category
$(document).ready(function () {
	$("#my-form-buyer-cat").submit(function (e) {  
    e.preventDefault(); // Cancel the default action 
   let id = $('#id').val();
   $.ajax({
    url: "/buyer/update_buyer_category/" + id + "/",
    type: "POST",
    data:  new FormData(this),
    contentType: false,
      cache: false,
    processData:false, 
    success: function(data)
       {
       if(data == "error")
       {
        $(".alert-danger").show();
       }
       else
       {
        // view uploaded file.
        $(".alert-primary").show(); 
        location.reload();
       }
       },
          
     });
  });
});

$(document).ready(function () {
	$("#my-form-add-buyer-cat").submit(function (e) {  
    e.preventDefault(); // Cancel the default action 
   let id = $('#id').val();
   $.ajax({
    url: "/buyer/add_buyer_category/" + id + "/",
    type: "POST",
    data:  new FormData(this),
    contentType: false,
      cache: false,
    processData:false, 
    success: function(data)
       {
       if(data == "error")
       {
        $(".alert-danger").show();
       }
       else
       {
        // view uploaded file.
        $(".alert-primary").show(); 
        location.reload();
       }
       },
          
     });
  });
});

//Menufcture
$(document).ready(function () {
	$("#my-form-buyer-menufacture").submit(function (e) {  
    e.preventDefault(); // Cancel the default action 
   let id = $('#id').val();
   $.ajax({
    url: "/buyer/update_buyer_menufacture/" + id + "/",
    type: "POST",
    data:  new FormData(this),
    contentType: false,
      cache: false,
    processData:false,
    beforeSend : function()
    {
     //$("#preview").fadeOut();
     $("#err").fadeOut();
    },
    success: function(data)
       {
       if(data == "error")
       {
        $(".alert-danger").show();
       }
       else
       {
        // view uploaded file.
        $(".alert-primary").show(); 
        location.reload();
       }
       },
          
     });
  });
});

$(document).ready(function () {
	$("#my-form-add-buyer-menufacture").submit(function (e) {  
    e.preventDefault(); // Cancel the default action 
   let id = $('#id').val();
   $.ajax({
    url: "/buyer/add_buyer_menufacture/" + id + "/",
    type: "POST",
    data:  new FormData(this),
    contentType: false,
      cache: false,
    processData:false,
    beforeSend : function()
    {
     //$("#preview").fadeOut();
     $("#err").fadeOut();
    },
    success: function(data)
       {
       if(data == "error")
       {
        $(".alert-danger").show();
       }
       else
       {
        // view uploaded file.
        $(".alert-primary").show(); 
        location.reload();
       }
       },
          
     });
  });
});

//model popup 
$(document).ready(function () {
	$("#my-form-buyer-model").submit(function (e) {  
    e.preventDefault(); // Cancel the default action 
   let id = $('#id').val();
   $.ajax({
    url: "/buyer/update_buyer_model/" + id + "/",
    type: "POST",
    data:  new FormData(this),
    contentType: false,
      cache: false,
    processData:false,
    beforeSend : function()
    {
     //$("#preview").fadeOut();
     $("#err").fadeOut();
    },
    success: function(data)
       {
       if(data == "error")
       {
        $(".alert-danger").show();
       }
       else
       {
        // view uploaded file.
        $(".alert-primary").show(); 
        location.reload();
       }
       },
          
     });
  });
});

$(document).ready(function () {
	$("#my-form-add-buyer-model").submit(function (e) {  
    e.preventDefault(); // Cancel the default action 
   let id = $('#id').val();
   $.ajax({
    url: "/buyer/add_buyer_model/" + id + "/",
    type: "POST",
    data:  new FormData(this),
    contentType: false,
      cache: false,
    processData:false,
    beforeSend : function()
    {
     //$("#preview").fadeOut();
     $("#err").fadeOut();
    },
    success: function(data)
       {
       if(data == "error")
       {
        $(".alert-danger").show();
       }
       else
       {
        // view uploaded file.
        $(".alert-primary").show(); 
        location.reload();
       }
       },
          
     });
  });
});
 //buyer buyer

 $(document).ready(function (e) {
  $("#update_buyer").on('submit',(function(e) {
   e.preventDefault();
   let buyer_id = $('#buyer_id').val();
   $.ajax({
    url: "/buyer/edit_buyer/" + buyer_id + "/",
    type: "POST",
    data:  new FormData(this),
    contentType: false,
      cache: false,
    processData:false,
    beforeSend : function()
    {
     //$("#preview").fadeOut();
     $("#err").fadeOut();
    },
    success: function(data)
     {
     if(data == "error")
     {
      $(".alert-danger").show();
     }
     else
     {
      // view uploaded file.
      $(".alert-success").show(); 
      // location.reload();
     }
     },
              
     });
  }));
});

//admin side inquiry form edit js
$(document).ready(function (e) {
	$("#update_inquiry_form").on('submit',(function(e) {
	 e.preventDefault();
   let id = $('#inquiry_id').val();
	 $.ajax({
	 url: '/buyer/update_buyer_inquiry/'+ id+ "/",
	  type: "POST",
	  data:  new FormData(this),
	  contentType: false,
			cache: false,
	  processData:false,
	  
	  success: function(data)
		 {
      if(data == "error")
      {
       $(".alert-danger").show();
      }
      else
      {
       // view uploaded file.
       $(".alert-success").show(); 
       // location.reload();
      }
		 },
		          
	   });
	}));
});

//send mail

$(document).ready(function (e) {
	$("#send_buyer_email").on('submit',(function(e) {
	 e.preventDefault(); 
   $("body").addClass("loading");
	 $.ajax({
	 url: '/buyer/send_buyer_inquiry_to_vendor/',
	  type: "POST",
	  data:  new FormData(this),
	  contentType: false,
			cache: false,
	  processData:false,
	  
	  success: function(data)
		 {
      if(data == "error")
      {
       $(".alert-danger").show();
      }
      else
      {
       // view uploaded file.
       $("body").removeClass("loading"); 
       $(".alert-success").show(); 
       // location.reload();
      }
		 },
		          
	   });
	}));
});

//buyer delete

$(function() {

	$('.delete_buyer_email').on('click',function(){
	  
	  var id = $(this).data('id');     
    if(confirm("Are you sure you want to remove this  from database?"))
    {
    $.ajax({
      url:'/buyer/delete_buyer_email/'+ id + "/",
      method:"POST",
      data:{"req_id":id},
      success: function (response){ 
        $(".alert-success").show(); 
        location.reload();
      }
      })
      }
    else
    {
    return false;
    }
	});
});


$(function() {

	$('.delete_buyer_category').on('click',function(){
	  
	  var id = $(this).data('id');     
    if(confirm("Are you sure you want to remove this  from database?"))
    {
    $.ajax({
      url:'/buyer/delete_buyer_category/'+ id + "/",
      method:"POST",
      data:{"req_id":id},
      success: function (response){ 
        $(".alert-success").show(); 
        location.reload();
      }
      })
      }
    else
    {
    return false;
    }
	});
});


$(function() {

	$('.delete_buyer_menufacture').on('click',function(){
	  
	  var id = $(this).data('id');     
    if(confirm("Are you sure you want to remove this  from database?"))
    {
    $.ajax({
      url:'/buyer/delete_buyer_menufacture/'+ id + "/",
      method:"POST",
      data:{"req_id":id},
      success: function (response){ 
        $(".alert-success").show(); 
        location.reload();
      }
      })
      }
    else
    {
    return false;
    }
	});
});


$(function() {

	$('.delete_buyer_model').on('click',function(){
	  
	  var id = $(this).data('id');     
    if(confirm("Are you sure you want to remove this  from database?"))
    {
    $.ajax({
      url:'/buyer/delete_buyer_model/'+ id + "/",
      method:"POST",
      data:{"req_id":id},
      success: function (response){ 
        $(".alert-success").show(); 
        location.reload();
      }
      })
      }
    else
    {
    return false;
    }
	});
});

$(function() {

	$('.delete_buyer_attachment').on('click',function(){
	  
	  var id = $(this).data('id');     
    if(confirm("Are you sure you want to remove this  from database?"))
    {
    $.ajax({
      url:'/buyer/delete_buyer_attachment/'+ id + "/",
      method:"POST",
      data:{"req_id":id},
      success: function (response){ 
        $(".alert-success").show(); 
        location.reload();
      }
      })
      }
    else
    {
    return false;
    }
	});
});

$(document).ready(function () {
	$("#form_add_image_model").submit(function (e) {  
    e.preventDefault(); // Cancel the default action 
   let id = $('#id').val();
   $.ajax({
    url: "/buyer/add_buyer_attachment/" + id + "/",
    type: "POST",
    data:  new FormData(this),
    contentType: false,
      cache: false,
    processData:false,
    beforeSend : function()
    {
     //$("#preview").fadeOut();
     $("#err").fadeOut();
    },
    success: function(data)
       {
       if(data == "error")
       {
        $(".alert-danger").show();
       }
       else
       {
        // view uploaded file.
        $(".alert-primary").show(); 
        location.reload();
       }
       },
          
     });
  });
});
//vendor delete
$(function() {

	$('.delete_vendor_email').on('click',function(){
	  
	  var id = $(this).data('id');     
    if(confirm("Are you sure you want to remove this  from database?"))
    {
    $.ajax({
      url:'/vendor/delete_vendor_email/'+ id + "/",
      method:"POST",
      data:{"req_id":id},
      success: function (response){ 
        $(".alert-success").show(); 
        location.reload();
      }
      })
      }
    else
    {
    return false;
    }
	});
});


$(function() {

	$('.delete_vendor_category').on('click',function(){
	  
	  var id = $(this).data('id');     
    if(confirm("Are you sure you want to remove this  from database?"))
    {
    $.ajax({
      url:'/vendor/delete_vendor_category/'+ id + "/",
      method:"POST",
      data:{"req_id":id},
      success: function (response){ 
        $(".alert-success").show(); 
        location.reload();
      }
      })
      }
    else
    {
    return false;
    }
	});
});


$(function() {

	$('.delete_vendor_menufacture').on('click',function(){
	  
	  var id = $(this).data('id');     
    if(confirm("Are you sure you want to remove this  from database?"))
    {
    $.ajax({
      url:'/vendor/delete_vendor_menufacture/'+ id + "/",
      method:"POST",
      data:{"req_id":id},
      success: function (response){ 
        $(".alert-success").show(); 
        location.reload();
      }
      })
      }
    else
    {
    return false;
    }
	});
});


$(function() {

	$('.delete_vendor_model').on('click',function(){
	  
	  var id = $(this).data('id');     
    if(confirm("Are you sure you want to remove this  from database?"))
    {
    $.ajax({
      url:'/vendor/delete_vendor_model/'+ id + "/",
      method:"POST",
      data:{"req_id":id},
      success: function (response){ 
        $(".alert-success").show(); 
        location.reload();
      }
      })
      }
    else
    {
    return false;
    }
	});
});

 
 //subtract logic
 $(document).ready(function() {
  if($("#send_quotation").length){
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

$(document).ready(function() {
  if($("#send_buyer_quotation").length){
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


$(document).ready(function() {
  if($("#edit_buyer_quotation").length){
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
//Buyer Quotation from Vendor(procure)
$(document).ready(function (e) {
	$("#send_buyer_quotation").on('submit',(function(e) {
	 e.preventDefault(); 
   $("body").addClass("loading");
	 $.ajax({
	 url: '/vendor/send_quotation_to_buyer_email/',
	  type: "POST",
	  data:  new FormData(this),
	  contentType: false,
			cache: false,
	  processData:false,
	  
	  success: function(data)
		 {
      if(data == "error")
      {
       $(".alert-danger").show();
      }
      else
      {
       // view uploaded file.
       $("body").removeClass("loading"); 
       $(".alert-success").show(); 
       // location.reload();
      }
		 },
		          
	   });
	}));
});


$(document).ready(function (e) {
	$("#send_quotation").on('submit',(function(e) {
	 e.preventDefault(); 
   $("body").addClass("loading");
	 $.ajax({
	 url: '/vendor/send_quotation/',
	  type: "POST",
	  data:  new FormData(this),
	  contentType: false,
			cache: false,
	  processData:false,
	  
	  success: function(data)
		 {
      if(data == "error")
      {
       $(".alert-danger").show();
      }
      else
      {
       // view uploaded file.
       $("body").removeClass("loading"); 
       $(".alert-success").show(); 
       // location.reload();
      }
		 },
		          
	   });
	}));
});

$(document).ready(function (e) {
	$("#edit_buyer_quotation").on('submit',(function(e) {
	 e.preventDefault();  
	 $.ajax({
	 url: '/vendor/update_send_inquiry/',
	  type: "POST",
	  data:  new FormData(this),
	  contentType: false,
			cache: false,
	  processData:false,
	  
	  success: function(data)
		 {
      if(data == "error")
      {
       $(".alert-danger").show();
      }
      else
      {
       // view uploaded file. 
       $(".alert-success").show(); 
       // location.reload();
      }
		 },
		          
	   });
	}));
});

$(function(){
  $(".reference_no").bind('input',function() {
  var token = $('input[name="csrfmiddlewaretoken"]').prop('value');  
  var searchref = $(this).val(); 
  if(searchref!='') {
    $.ajax({ 
      type: "POST",
      url: "/vendor/get_buyer_email/",
      data: {'csrfmiddlewaretoken':token, 'searchref':searchref},
      cache: false,
      success: function(response) {
        var jsonData = JSON.parse(response);
        for (var i = 0; i < jsonData.length; i++) {
          var counter = jsonData[i];  
          var email = counter.fields.email_list;  
          $('#exampleid').append(`<tr><td>
          <div class="custom-control custom-checkbox">
          <input type="checkbox" class="custom-control-input" name="buyer_emails" value="${email}" id="customCheck${i}">
          <label class="custom-control-label" for="customCheck${i}">${i}</label>
          </div></td><td>${email}</td></tr>`); 
        }
      }
    });
  }
  return false;
});
});

 


$(function () {
  $(document).on('click', '.btn-add', function (e) {
      e.preventDefault();

      var controlForm = $('.controls:first'),
          currentEntry = $(this).parents('.entry:first'),
          newEntry = $(currentEntry.clone()).appendTo(controlForm);

      newEntry.find('input').val('');
      controlForm.find('.entry:not(:last) .btn-add')
          .removeClass('btn-add').addClass('btn-remove')
          .removeClass('btn-success').addClass('btn-danger')
          .html('<span class="bi bi-trash"></span>');
  }).on('click', '.btn-remove', function (e) {
      $(this).parents('.entry:first').remove();

      e.preventDefault();
      return false;
  });
});


$(document).ready(function (e) {
	$("#add_buyer_inquiry").on('submit',(function(e) {
	 e.preventDefault();
	 $.ajax({
	 url: '/buyer/add_buyer_inquiry/',
	  type: "POST",
	  data:  new FormData(this),
	  contentType: false,
			cache: false,
	  processData:false,
	  
	  success: function(data)
		 {
	   if(data == "error")
        {
        // invalid file format.
        $(".alert-danger").show();
        }
	   else
        {
            // view uploaded file.
            $(".alert-success").show();
            $("#add_buyer_inquiry")[0].reset(); 
            // location.reload();
        }
		 },
		          
	   });
	}));
});

// Buyer Email For PO
$(function(){
  $("#buyer_reference_no").bind('input', function(e) {
    e.preventDefault();
  var token = $('input[name="csrfmiddlewaretoken"]').prop('value');  
  var searchref = $(this).val(); 
  if(searchref!='') {
    $.ajax({ 
      type: "POST",
      url: "/buyer/get_buyer_email/",
      data: {'csrfmiddlewaretoken':token, 'searchref':searchref},
      dataType: 'json',
      success: function(response) {
        var jsonData = JSON.parse(response);
        for (var i = 0; i < jsonData.length; i++) {
          var counter = jsonData[i];  
          var email = counter.fields.email_list; 
          $('#exampleid').append(`<tr><td>
                                        <div class="custom-control custom-checkbox">
                                        <input type="checkbox" class="custom-control-input" name="buyer_emails" value="${email}" id="customCheck${i}">
                                        <label class="custom-control-label" for="customCheck${i}">${i}</label>
                                        </div></td><td>${email}</td></tr>`); 
        // $("#from_email").val(email); 
        } 
        $("#searchResult li").bind("click",function(){
          setText(this);
      });
      }
    });
  }
  return false;
});
});


$(document).ready(function (e) {
	$("#create_buyer_po").on('submit',(function(e) {
	 e.preventDefault();
   $("body").addClass("loading");
	 $.ajax({
	 url: '/buyer/create_buyer_po/',
	  type: "POST",
	  data:  new FormData(this),
	  contentType: false,
			cache: false,
	  processData:false,
	  
	  success: function(data)
		 {
	   if(data == "error")
        {
        // invalid file format.
        $(".alert-danger").show();
        }
	   else
        {
            // view uploaded file.
            $("body").removeClass("loading");
            $(".alert-success").show();
            $("#create_buyer_po")[0].reset(); 
            // location.reload();
        }
		 },
		          
	   });
	}));
}); 
 

$(document).ready(function() {
  if($("#create_buyer_po").length){
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


//vendor Po
$(document).ready(function() {
  if($("#create_vendor_po").length){
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

$(document).ready(function (e) {
	$("#create_vendor_po").on('submit',(function(e) {
	 e.preventDefault();
   $("body").addClass("loading");
	 $.ajax({
	 url: '/vendor/create_vendor_po/',
	  type: "POST",
	  data:  new FormData(this),
	  contentType: false,
			cache: false,
	  processData:false,
	  
	  success: function(data)
		 {
	   if(data == "error")
        {
        // invalid file format.
        $(".alert-danger").show();
        }
	   else
        {
            // view uploaded file.
            $("body").removeClass("loading");
            $(".alert-success").show();
            $("#create_vendor_po")[0].reset(); 
            // location.reload();
        }
		 },
		          
	   });
	}));
}); 

$(function(){
  $("#vendor_reference_no").bind('input',function(e) {
    e.preventDefault();
  var token = $('input[name="csrfmiddlewaretoken"]').prop('value');  
  var searchref = $(this).val(); 
  if(searchref!='') {
    $.ajax({ 
      type: "POST",
      url: "/vendor/get_vendor_email/",
      data: {'csrfmiddlewaretoken':token, 'searchref':searchref},
      dataType: 'json',
      success: function(response) {
        var jsonData = JSON.parse(response);
        for (var i = 0; i < jsonData.length; i++) {
          var counter = jsonData[i];  
          var email = counter.fields.email_list; 
          $('#exampleid').append(`<tr><td>
                                        <div class="custom-control custom-checkbox">
                                        <input type="checkbox" class="custom-control-input" name="buyer_emails" value="${email}" id="customCheck${i}">
                                        <label class="custom-control-label" for="customCheck${i}">${i}</label>
                                        </div></td><td>${email}</td></tr>`); 
        // $("#from_email").val(email); 
        } 
        $("#searchResult li").bind("click",function(){
          setText(this);
      });
      }
    });
  }
  return false;
});
});


//Order Page
 //subtract logic
 $(document).ready(function() {
  if($("#create_order").length){
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


//order js
$(document).ready(function (e) {
	$("#create_order").on('submit',(function(e) {
	 e.preventDefault(); 
   $("body").addClass("loading");
	 $.ajax({
	 url: '/order/create_order/',
	  type: "POST",
	  data:  new FormData(this),
	  contentType: false,
			cache: false,
	  processData:false,
	  
	  success: function(data)
		 {
      if(data == "error")
      {
       $(".alert-danger").show();
      }
      else
      {
       // view uploaded file.
       $("body").removeClass("loading");
       $(".alert-success").show(); 
       // location.reload();
      }
		 },
		          
	   });
	}));
});