function test(){console.log("R");}

function showUser(sam){
		$("#UserLeft").html("");
		$("#UserRight").html("");
		$("#UserPane").show("fast");
		//add link to stat output
		Stat('<a href="#" onclick="Users.showUser(\''+sam+'\');return false;">'+sam+'</a>');
		GetJSONData('/Users','&sam='+sam)
		.then(data => {
			data = JSON.parse(data);
			//console.log(data)
			Object.keys(data[0]).forEach(key => {
				if (key == "distinguishedname"){
					value = data[0][key].split(',')[1].split("=")[1];
					$("#UserLeft").append("<br/>OU: "+value);
				}
				else if (key == "employeeType"){$("#UserLeft").append("<br/>"+key+": "+data[0][key]);}
				else if (key == "Enabled"){}
				else if (key == "mailnickname"){}
				else if (key == "pwdlastset"){}
				else if (key == "AccountExpires"){}
				else if (key == "LastLogon"){}
				
				else {
					if (data[0][key] != null){
						$("#UserLeft").append("<br/>"+key+": <span>"+data[0][key]+"</span>");
						$("#UserLeft").append('<a href="#" onclick="clipboard.lastE(this);return false;"><img class="nav-icon" src="images/document.svg" /></a>');
					}
				}
				
			});
			
		});
		GetJSONData('/Users/Live','&sam='+sam)
		.then(data => {
			data = JSON.parse(data);
			//console.log(data)
			Object.keys(data).forEach(key => {
				val = data[key]
				if (key == "LockedOut"){
					if (val == "False"){
						$("#UserRight").append('<br/><span class="good">'+key+': '+val+'</span>');
					}
					if (val == "True"){
						$("#UserRight").append('<br/><span class="bad">'+key+': '+val+'</span>');
						$("#UserRight").append(' <a href="#" onclick="Users.UnlockAccount(\''+sam+'\');return false;">Unlock</a>');
					}
				}
				else if (key == "pwdlastset"){
				  today = new Date();
			      pwdlastsetdate = new Date(val);
			      days = (today - pwdlastsetdate)/86400000;
			      if (days>=400){
					  $("#UserRight").append('<br/><span class="bad">Password Last Set : '+days.toFixed(2)+' days ago</span>');
					  }
				  else{
					  $("#UserRight").append('<br/><span class="good">Password Last Set : '+days.toFixed(2)+' days ago</span>');
				  }
				}
				else if (key == "AccountExpires"){
					if (!val.includes('12/31/1600') && val != ''){
						$("#viewRight").append('<br/><span>'+key+' : '+val+'</span>');
					}
				}
				else{$("#UserRight").append("<br/>"+key+" : "+val);}

			});
			
		});
}

function UnlockAccount(sam){
	
}
function showLockouts(){
	GetJSONData('/Users/Lockout')
	.then(data => {
		data = JSON.parse(data)
		console.log(data);
	});
}

module.exports = {test,showUser,UnlockAccount,showLockouts};

