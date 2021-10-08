function test(){console.log("R");}

function showUser(sam){
		GetJSONData('/Users','&sam='+sam)
		.then(data => {
			data = JSON.parse(data);
			console.log(data)
			$("#UserPane").show("fast");
			$("#UserLeft").html("");
			Object.keys(data[0]).forEach(key => {
				$("#UserPane").append("<br/>"+key+" : "+data[0][key]);
			});
			
		});
		GetJSONData('/Users/Live','&sam='+sam)
		.then(data => {
			//data = JSON.parse(data);
			console.log(data)
			$("#UserPane").show("fast");
			$("#UserRight").html(data);
			//$("#UserRight").html("");
			//Object.keys(data[0]).forEach(key => {
			//	$("#UserPane").append("<br/>"+key+" : "+data[0][key]);
			//});
			
		});
}


module.exports = {test,showUser};

