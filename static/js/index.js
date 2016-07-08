$(document).ready(function(){
var div = $('<div>')
    .attr('class', 'list-group')
    .append($('<a>')
        .attr('class', 'list-group-item col-xs-3').attr('style','width:140px;margin:5px')
        .append($('<h4>')
            .attr('class', 'list-group-item-heading'),
            $('<p>')
            .attr('class', 'list-group-item-text')));
	var wishObj;
	var haveObj;
	var edgeSite=[];
	var iter;
	var uninames=[];
	var anode;
	var uninode=[];
	var cnum = 0;
	console.log(cnum);
		$.ajax({
			url : '/getAllWish',
			type : 'GET',
			async: false,
			success: function(res){
				wishObj = JSON.parse(res);
				var wish = '';
				
				$.each(wishObj,function(index, value){
					wish = $(div).clone();
					$(wish).find('h4').text(value.num);
					$(wish).find('p').text(value.name);
					$(wish).find('a').attr('class','list-group-item active col-xs-3')
                    $('#numList').append(wish);
					if ($.inArray(value.name,uninames)==-1){
						uninames.push(value.name);
						anode = {id:value.name,type:"user"};
						uninode.push(anode)
					}
					if ($.inArray(value.num.toString(),uninames)==-1){
						uninames.push(value.num.toString());
						anode = {id:value.num.toString(),type:"num"};
						uninode.push(anode)
					}
					iter={source:uninames.indexOf(value.num.toString()),target:uninames.indexOf(value.name),name:"want"};
					edgeSite.push(iter);
					cnum = 1+cnum;
				});
				$.ajax({
					url : '/getAllHave',
					type : 'GET',
					async: false,
					success: function(res){
					haveObj = JSON.parse(res);
					var rhas = '';

					$.each(haveObj,function(index, value){
						rhas = $(div).clone();
						$(rhas).find('h4').text(value.num);
						$(rhas).find('p').text(value.name);
						$('#haveList').append(rhas);
						if ($.inArray(value.name,uninames)==-1){
							uninames.push(value.name);
							anode = {id:value.name,type:"user"};
							uninode.push(anode)
						}
						if ($.inArray(value.num.toString(),uninames)==-1){
							uninames.push(value.num.toString());
							anode = {id:value.num.toString(),type:"num"};
							uninode.push(anode)
						}
						iter={source:uninames.indexOf(value.num.toString()),target:uninames.indexOf(value.name),name:"have"};
						edgeSite.push(iter);
						cnum = cnum +1;
						console.log(uninames[cnum]);
					});
					},
			error: function(error){
				console.log(error);
			}
		});

			},
			error: function(error){
				console.log(error);
			}
		}).always(function(){

			var h=400;
			var w=400;

	var force = d3.layout.force()
		.nodes(uninode)
		.links(edgeSite)
		.size([w,h])
		.linkDistance((h+w)/9)
		.charge(-400*h/200)
		.start();


	var colors=d3.scale.category20();
	var svg=d3.select("#im")
    		.append("svg")
    		.attr("width","auto")
    		.attr("height",h)
		.attr("style","align-content:center")
		;

	var edges=svg.selectAll("line")
    	.data(edgeSite)
    	.enter()
    	.append("line")
		.style("stroke",function(d,i){//  设置线的颜色
        	return colors(i*7);
		})
    	.style("stroke-width",function(d,i){
        	return 3;//d.weight;
    	});



	var rnode=svg.selectAll(".rnode")
    	.data(uninode)
    	.enter()
    	.append("g")
        .attr("class","rnode").call(force.drag);

	rnode.append("image")
        .attr("xlink:href",function (d) {
            if (d.type=="user"){
                return "../../static/img/user.png"
            }   else {
                return "../../static/img/rlabel.png"
            }
        })
	        .attr("x", -35*h/600)
		    .attr("y", -35*h/600)
			.attr("width", 70*h/600)
      		.attr("height", 70*h/600);


	var svg_texts = svg.selectAll(".nodelabel")
                              .data(uninode)
                              .enter()
                              .append("text")
                              .attr("class","good")
                              .style("fill","white")
        .attr("text-anchor","middle")
		.attr("font-size",12*h/540)
        .attr("dy",function (d) {
            if (d.type=="user"){
                return 20*h/600
            }   else {
                return 6*h/600
            }
        })

        .attr("dx",function (d) {
            if (d.type=="user"){
                return 0
            }   else {
                return 6*h/800
            }
        })
		.text(function (d) {
			return d.id;
		}).call(force.drag);


	var svg_e_texts = svg.selectAll(".edgelabel")
                              .data(edgeSite)
                              .enter()
                              .append("text")
        .attr("font-weight","bolder")
		.attr("font-size",12*h/500)
        .attr("font-family","monaco")
        .attr("text-anchor","middle")
        .attr("dy",7*h/600)
                              .attr("class","good")
                              .style("fill","black")
                              .text(function(d){         //返回节点的名字
                                  return d.name;
                              }).call(force.drag);



	force.on("tick",function(){
    //边
    	edges.attr("x1",function(d){
        	return  d.source.x;
   		 })
    	.attr("y1",function(d){
        	return  d.source.y;
   	 	})
    	.attr("x2",function(d){
        	return  d.target.x;
    	})
    	.attr("y2",function(d){
        	return  d.target.y;
    	});

        svg_e_texts.attr("x", function(d){ return (d.source.x+d.target.x)/2; })
			.attr("y", function(d){  return (d.source.y+d.target.y)/2; });



    	rnode.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });


    	svg_texts.attr("x", function(d){ return d.x; })
                       .attr("y", function(d){ return d.y; });
})
		});





});




/**
 * Created by pjer on 2016/6/11.
 */
