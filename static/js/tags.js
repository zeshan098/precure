let _tag_input_suggestions_data = null;

/*
create a chainnable method for the script to
*/
$.fn.tagsValues = function (method /*, args*/) {
    //loop through all tags getting the attribute value
    var data=[];
    $(this).find(".data .tag .text").each(function (key,value) {
        let v=$(value).attr('value');
        data.push(v);
    })

    return data;
};


/*
Handle click of the input area
 */
$('.tags-input').click(function () {
    $(this).find('input').focus();
});
 

$('.tags-input-menufacture').click(function () {
    $(this).find('input').focus();
});

$('.tags-input-model').click(function () {
    $(this).find('input').focus();
});
/*
handle the click of close button on the tags
 */

$(document).on("click", ".tags-input .data .tag .close", function() {
    // whatever you do to delete this row
    $(this).parent().remove()

})

$(document).on("click", ".tags-input-menufacture .data .tag .close", function() {
    // whatever you do to delete this row
    $(this).parent().remove()

})

$(document).on("click", ".tags-input-model .data .tag .close", function() {
    // whatever you do to delete this row
    $(this).parent().remove()

})
/*
Handle the click of one suggestion
*/

$(document).on("click", ".tags-input .autocomplete-items div", function() {
    let index=$(this).index()
    let data=_tag_input_suggestions_data[index];
    let data_holder = $(this).parents().eq(4).find('.data')
    _add_input_tag(data_holder,data.id,data.name)
    $('.tags-input .autocomplete-items').html('');

})

$(document).on("click", ".tags-input-menufacture .autocomplete-items div", function() {
    let index=$(this).index()
    let data=_tag_input_suggestions_data[index];
    let data_holder = $(this).parents().eq(4).find('.data_menufacture')
    _add_input_tag_menufacture(data_holder,data.id,data.name)
    $('.menufacture .autocomplete-items').html('');

})

$(document).on("click", ".tags-input-model .autocomplete-items div", function() {
    let index=$(this).index()
    let data=_tag_input_suggestions_data[index];
    let data_holder = $(this).parents().eq(4).find('.data_model')
    _add_input_tag_model(data_holder,data.id,data.name)
    $('.model .autocomplete-items').html('');

})

/*
detect enter on the input
 */
$(".tags-input input").on( "keydown", function(event) {
    if(event.which == 13){
        let data = $(this).val()
        if(data!="")_add_input_tag(this,data,data)
    }


});

$(".tags-input-menufacture input").on( "keydown", function(event) {
    if(event.which == 13){
        let data = $(this).val()
        if(data!="")_add_input_tag_menufacture(this,data,data)
    }


});

$(".tags-input-model input").on( "keydown", function(event) {
    if(event.which == 13){
        let data = $(this).val()
        if(data!="")_add_input_tag_model(this,data,data)
    }


});

$(".tags-input input").on( "focusout", function(event) {
    $(this).val("")
    var that = this;
    setTimeout(function(){ $(that).parents().eq(2).find('.autocomplete .autocomplete-items').html(""); }, 500);
});


$(".tags-input-menufacture input").on( "focusout", function(event) {
    $(this).val("")
    var that = this;
    setTimeout(function(){ $(that).parents().eq(2).find('.autocomplete .autocomplete-items').html(""); }, 500);
});

$(".tags-input-model input").on( "focusout", function(event) {
    $(this).val("")
    var that = this;
    setTimeout(function(){ $(that).parents().eq(2).find('.autocomplete .autocomplete-items').html(""); }, 500);
});

function _add_input_tag(el,data,text){
    let template="<span class=\"tag\"><input type=\"text\" class=\"text\" value='"+data+"' name=\"category\"><span class=\"close\">&times;</span></span>\n";
    $(el).parents().eq(2).find('.data').append(template);
    $(el).val('')
}

function _add_input_tag_menufacture(el,data,text){
    let template="<span class=\"tag_menufacture\"><input type=\"text\" class=\"text_menufacture\" value='"+data+"' name=\"menufacture\"><span class=\"close\">&times;</span></span>\n";
    $(el).parents().eq(2).find('.data_menufacture').append(template);
    $(el).val('')
}

function _add_input_tag_model(el,data,text){
    let template="<span class=\"tag_model\"><input type=\"text\" class=\"text_model\" value='"+data+"' name=\"model\"><span class=\"close\">&times;</span></span>\n";
    $(el).parents().eq(2).find('.data_model').append(template);
    $(el).val('')
}

$(".tags-input input").on( "keyup", function(event) {
    var query=$(this).val()

    if(event.which == 8) {
        if(query==""){
            console.log("Clearing suggestions");
            $('.tags-input .autocomplete-items').html('');
            return;
        }
    }

    $('.tags-input .autocomplete-items').html('');
    runSuggestions($(this),query)

});

$(".tags-input-menufacture input").on( "keyup", function(event) {
    var query=$(this).val()

    if(event.which == 8) {
        if(query==""){
            console.log("Clearing suggestions");
            $('.tags-input .autocomplete-items').html('');
            return;
        }
    }

    $('.tags-input-menufacture .autocomplete-items').html('');
    runSuggestions_menufatcure($(this),query)

});

$(".tags-input-model input").on( "keyup", function(event) {
    var query=$(this).val()

    if(event.which == 8) {
        if(query==""){
            console.log("Clearing suggestions");
            $('.tags-input .autocomplete-items').html('');
            return;
        }
    }

    $('.tags-input-model .autocomplete-items').html('');
    runSuggestions_model($(this),query)

});