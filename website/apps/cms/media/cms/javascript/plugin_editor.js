$(document).ready(function() {
    $('span.add-plugin').click(function(){
        var select = $(this).parent().children("select");
        var pluginvalue = select.attr('value');
        var placeholder = $(this).parent().parent().parent().parent().parent().children("h2").text();
        var splits = window.location.href.split("/");
        var page_id = splits[splits.length-2];
        var language = $('#id_language').attr('value');
        var target_div = $(this).parent().parent().parent().children('div.plugin-editor');
        if (pluginvalue) {
            var pluginname = select.children('[selected]').text();
            var ul_list = $(this).parent().parent().children("ul.plugin-list");
            $.post("add-plugin/", { page_id:page_id, placeholder:placeholder, plugin_type:pluginvalue, language:language }, function(data){
                if ('error' != data) {
                    loadPluginForm(target_div, data);
                    ul_list.append('<li id="plugin_' + data + '" class="' + pluginvalue + ' active"><span class="drag"></span><span class="text">' + pluginname + '</span><span class="delete"></span></li>');
                    setclickfunctions();
                }
            }, "html" );
        }
    });
    $('ul.plugin-list').sortable({handle:'span.drag',
                                  axis:'y',
                                  opacity:0.9,
                                  zIndex:2000,
                                  update:function(event, ui){
                                  		var array = ui.element.sortable('toArray');
                                  		var d = "";
                                  		for(var i=0;i<array.length;i++){
                                  			d += array[i].split("plugin_")[1];
                                  			if (i!=array.length-1){
                                  				d += "_";
                                  			}
                                  		}
                                  		$.post("move-plugin", 
                                  				{ ids:d },
                                  				function(data){},
                                  				"json");

                                  		}
                                  }
    						);
    
    setclickfunctions();
});

function setclickfunctions(){
    $('ul.plugin-list .text').click(function(){
    	load_plugin($(this).parent())
        return false;
    });

    $('ul.plugin-list .delete').click(function(){
    	var question = gettext("Are you sure you want to delete this plugin?")
		var answer = confirm(question, true);
		if(answer){
	        var plugin_id = $(this).parent().attr("id").split("plugin_")[1];
	        $.post("remove-plugin/", { plugin_id:plugin_id }, function(data){
				var splits = data.split(",")
				id = splits.shift()
	       		$("#plugin_"+id).remove();
				$("#iframe_"+id).parent().html("<p>" + splits.join(",") + "</p>")
	        }, "html");
		}
    });
}

function load_plugin(li){
	var target = li.parent().parent().parent().children("div.plugin-editor");
    var id = li.attr("id").split("plugin_")[1];
    loadPluginForm(target, id);
}

function setiframeheight(height, id){
    $('#iframe_'+id).height(height+"px");
}

function hide_iframe(id, type, title, msg){
	html = "<b>"+type+"</b>"
	if( title != "" && title != null){
		html += " [ "+title+ " ]"
	}
	$('#plugin_'+id+" span.text").html(html);
    $('#iframe_'+id).parent().html("<p>"+msg+"</p>");
}

function loadPluginForm(target, id){
    var object = '<iframe id="iframe_'+id+'" src="edit-plugin/'+id+'/" frameborder="0"></iframe>';
    target.html(object);
    $('ul.plugin-list .active').removeClass("active");
    $('#plugin_'+id).addClass("active");
};
