var orderly = (function(){
  
    var data = {inicio :"",a : [],fin :""};
    
    /*
    [{
        serie:{
            name:"",
            season : [{
                name: "",
                chapter : [{
                    id :"",
                    name:"",
                    status:false
                }]
            }]
        }
    }];
    */
  
    var llamadaAjax = function(){
		var req = $.ajax({
			type: "POST",
			url: orderly.informe_file,
			dataType: "xml",
			data: {}
		});
		req.done(function (xml){
		    xmlParser(xml);
		});
    };
    
    var xmlParser =  function(xml) {
        data.inicio = $(xml).find('inicio').text().trim();
        data.fin = $(xml).find('fin').text().trim();
        $(xml).find('serie').each(function(){
            //console.log($(this).attr('name').trim());
            var serie = {
                name: $(this).attr(orderly.serie_name).trim(),
                season :[]
                };
            $(this).find('season').each(function(){
                //console.log($(this).attr('name').trim());
                var season = {
                    name: $(this).attr(orderly.season_name).trim(),
                    chapter: []
                };
                $(this).find('chapter').each(function(){
                    //console.log($(this).attr('name').trim());
                    //console.log($(this).find('id').text().trim());
                    //console.log($(this).find('id').text().trim());
                    var chapter = {
                        id : $(this).find(orderly.chapter_id).text().trim(),
                        name:$(this).find(orderly.chapter_name).text().trim(),
                        status:$(this).attr(orderly.chapter_status).trim()
                    };
                    season.chapter.push(chapter);
                 });
                 serie.season.push(season);
            });
            data.a.push(serie);
        });
        buildTable();
    };
		    

    var buildTable = function(){
        $('#botonera').append($('<span>').text('Inicio = ' + data.inicio));
        $('#botonera').append($('<span>').text('Fin = ' + data.fin));
        var arr = data.a;
        var tabla = $('<table></table>').addClass('tabla');
        var tr;
        for ( var i = 0; i < arr.length; i++ ) {
            if (i%orderly.n_columnas==0){
                tabla.append(buildCabecera());
                tr = $('<tr></tr>');
            }
            tr.append(buildSerie(arr[i])); 
            tabla.append(tr);
        }
        $('#content').text('');
        $('#content').append(tabla);
    };
    
    var buildCabecera = function(){
        var tr = $('<tr></tr>');
        for (var i = orderly.n_columnas; i--; ) {
            var td = $('<th></th>').text("Serie");
            tr.append(td);
        }
        return tr;
    };
    
    var buildSerie = function(serie){
        var td = $('<td></td>');
        var divserie = $('<div></div>').addClass('serie').text(serie.name);
        var divcontenedor =  $('<div></div>').addClass('contenedor').toggleClass("focused");
        for (var s in serie.season) {
            var season =serie.season[s];
            var divseason = $('<div></div>').addClass('season').text(season.name);
            
            if (season.name === 'Extras'){
                divseason.addClass("extras");
            }
            if (season.chapter.length === 0){
                divseason.addClass("visto");
            }
            
            for (var c in season.chapter) {
                var chapter = season.chapter[c];
                var divChapter = $('<div></div>').addClass('chapter').text(chapter.id);//.toggleClass("focused");
                if (chapter.status.toLowerCase() === 'true'){
                  divChapter.addClass("visto");  
                } 
                divseason.append(divChapter);
            }
            divcontenedor.append(divseason);
        }
        divserie.on('click', function(){
            divcontenedor.toggleClass("focused"); 
        });
        td.append(divserie);
        td.append(divcontenedor);
        return td;
    };
    
    
    
  // PUBLICA
var orderly = {
    informe_file : 'informe.xml',
    n_columnas : 3,
    serie_name : 'name',
    season_name : 'name',
    chapter_name : 'name',
    chapter_id : 'id',
    chapter_status : 'status',
    
 	// inicializamos el objeto
    onReady : function() {
    	//alert("ON READY");
    	$('#content').text("Realizamos la llamada AjaX");
    	llamadaAjax();
    	

	}
};
return orderly; 

}());