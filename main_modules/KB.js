function LoadKBList(loc){
	$("#KBPane").show("fast");
	$("#listKB").html("");
	GetData('/KB','&s='+loc)
	.then(data => {
		data.forEach(file => {
			if (file.includes(".md")){
				filename = file.split(".")[0];
				$("#listKB").append('<div class="iconblock"><a href="#" onclick="KB.ShowKB(\''+file+'\',\''+loc+'\');return false;"> '+file.split('.')[0]+'</a></div>');
			}
		});
	});
	
}
function ShowKB(file,loc){
	$("#KBPane").show("fast");
	$("#listMD").html("");
	GetData('/KB','s='+loc+'&f='+file)
	.then(data => {
		$("#viewKB").html(data);
	});
	
}
module.exports = {LoadKBList,ShowKB};