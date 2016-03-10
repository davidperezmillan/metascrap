(function(){ //Función anónima autoejecutable
  
  
    $.ajax({
        type: "GET",
        url: "informe.xml",
        dataType: "xml",
        success: xmlParser
    });



    function xmlParser(xml) {
        $(xml).find('serie').each(function() {
            var divserie = $('<div></div>').addClass('serie').text($(this).attr('name').trim());
            var divcontenedor =  $('<div></div>').addClass('contenedor').toggleClass("focused");
           
            $(this).find('season').each(function(){
                var divseason = $('<div></div>').addClass('season').text($(this).attr('name').trim());
                
                if ($(this).attr('name').trim() === 'Extras'){
                    divseason.addClass("extras");
                    
                }
                
                if ($(this).find('chapter').length === 0){
                    divseason.addClass("visto");
                }
                $(this).find('chapter').each(function(){
                    var divChapter = $('<div></div>').addClass('chapter').text($(this).find('id').text().trim()).toggleClass("focused");
                    divseason.on('click', function(){
                        divChapter.toggleClass("focused"); 
                    });
                    divseason.append(divChapter);
                });
                divcontenedor.append(divseason);
            });
            divserie.on('click', function(){
                divcontenedor.toggleClass("focused"); 
            });
            $('#content').append(divserie);
            $('#content').append(divcontenedor);
            $('#content').append($('<br/>'));
        });
            
    }
  
  
  /*
             $('<div/>', {
                'id':'serie',
                'class':'serie',
                'text': $(this).attr('name').trim(),
            }).on('click', function(){
               
            }).appendTo('#content');
*/
  
  /*
  var xml = "<rss version='2.0'><channel><title>RSS Title</title></channel></rss>",
  xmlDoc = $.parseXML( xml ),
  $xml = $( xmlDoc ),
  $title = $xml.find( "title" );
 
    // Append "RSS Title" to #someElement
    $( "#someElement" ).append( $title.text() );
     
    // Change the title to "XML Title"
    $title.text( "XML Title" );
  */
  
}());