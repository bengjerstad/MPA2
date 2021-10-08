function test(){console.log("R");}

function showUser(sam){
		GetJSONData('/Users','&sam='+sam)
		.then(data => {
			data = JSON.parse(data);
			console.log(data)
			$("#UserPane").show("fast");
			$("#UserPane").html(JSON.stringify(data));
		});
}


module.exports = {test,showUser};

