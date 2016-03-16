var orderly = (function(){
  
    var data = {reg :"", fecha : "",items : []};
    
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
        data.reg = $(xml).find('reg').text().trim();
        data.fecha = $(xml).find('fecharef').text().trim();
        $(xml).find('item').each(function(){
            //console.log($(this).attr('name').trim());
            var item = {
                nombre: $(this).find("nombre").text().trim(),
                fecha:$(this).find("fecha").text().trim(),
                descarga: $(this).find("descarga").text().trim(),
                origen : {
                    web: $(this).find("origen").find("web").text().trim(),
                    enlace: $(this).find("origen").find("enlace").text().trim(),
                    },
                
                };
            data.items.push(item);
        });
        //console.dir(data);
        buildTable();
    };
		    

    var buildTable = function(){
        $('#botonera').append($('<span>').text('Registro de actividad :' + data.reg));
        $('#botonera').append($('<span>').text('fecha de actividad :' + data.fecha));
        var arr = data.items;
        var tabla = $('<table></table>').addClass('tabla');
        var tr = $('<tr></tr>');
        for ( var i = 0; i < arr.length; i++ ) {
            if (i%orderly.n_columnas==0){
                //tabla.append(buildCabecera());
				tr = $('<tr></tr>');
                
            }
            tr.append(builditem(arr[i])); 
            tabla.append(tr);
        }
        $('#content').text('');
        $('#content').append(tabla);
    };
    
    var builditem = function(item){
        var td = $('<td></td>');
        var divitem = $('<div></div>').addClass('item');
		var enlace = $('<div></div>').addClass('btnCall').attr("href","javascript:console.log('Enviando')");
		var eEnlace = $('<a></a>').attr("href", item.descarga).text(item.nombre);
		enlace.append(eEnlace);
		var origenHtml = $('<div></div>').addClass('origen');
		var eOrigen = $('<a></a>').addClass('origen').text(item.origen.web).attr("href", item.origen.enlace);
		origenHtml.append(eOrigen);
		
		divitem.append(enlace);
		td.append(origenHtml);
		td.append(divitem);
		return td;
    };
    
	var download = function(link, path)  {
			//Vamos a llamar al proccess 
			//para que nos de la version de la pagina que pedimos
			$.ajax({
			   url:"proccess.php",
			   type:'POST',
			   data : {"url" : link, "path" : path},
			   // ,timeout: 3000 // añadir timeout????
			})
			.done(function( data, textStatus, jqXHR ) {
                console.log("Ok");
			})
			.fail(function(jqXHR, textStatus, errorThrown){
                console.log("FAIL");
			})
			.then(function( jqXHR, textStatus, errorThrown){
				// span.appendTo($('#endpointStatus'));
			});
};
    
    
	/* DEPRECATE */
	/*
	
	
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
        var divserie = $('<div></div>').addClass('serie').text(item);
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
    
    */
    
  // PUBLICA
var orderly = {
    informe_file : '',
    n_columnas : 3,
    
 	// inicializamos el objeto
    onReady : function() {
    	//alert("ON READY");
    	$('#content').text("Realizamos la llamada AjaX");
    	llamadaAjax();
    	

    	
	}
	
};
return orderly; 

}());