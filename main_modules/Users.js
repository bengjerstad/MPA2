GroupLists = {}
GroupLists.ADGroups = [];
GroupLists.EmailGroups = [];

function RefreshData(){
	PostJSONData('/Users/','&s=refresh')
	.then(data => {
		data = JSON.parse(data)
		log(data,'User')
	});
}
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
						$("#UserLeft").append('<a href="#" onclick="clipboard.lastE(this);return false;"><img class="nav-icon" src="images/document.svg" style="height:1em; padding-top:0em;padding-bottom:0em;"/></a>');
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
	$("#UserRight").append('<div id="UserEmailGroups"><a href="#" onclick="Users.getemailgroups(\''+sam+'\',\'UserEmailGroups\');return false;">Get Email Groups</a></div>');
	$("#UserRight").append('</br><a href="#" onclick="Users.getadgroups(\''+sam+'\',\'UserADGroups\');return false;">Get AD Groups</a><div id="UserADGroups"></div>');
	$("#UserRight").append('</br><a href="#" onclick="Users.getLicense(\''+sam+'\');return false;">Get License</a><div id="UserLicense"></div>');
	$("#UserRight").append('</br><a href="#" onclick="Users.getMFA(\''+sam+'\');return false;">Get MFA</a><div id="UserMFA"></div>');
}

function UnlockAccount(sam){
	GetJSONData('/Users/Lockout','&sam='+sam)
	.then(data => {
		data = JSON.parse(data)
		if (data == ''){
			Stat('<span class="good">'+sam+' Unlocked</span> ');
			showLockouts();
		}
		else{
			console.log("Unlock: ." + data +".");	
			}
		  
	});
	
}
function showLockouts(){
	GetJSONData('/Users/Lockout','')
	.then(data => {
		data = JSON.parse(data)
		if (data.length == 0){
			$("#LockedOutUsers").html("")
			Stat('<span class="good">No Users are Locked Out</span> ');
		}
		else{
			data.forEach(function(line){
					  if (line != "" && !(line.includes('-----')) && !(line.includes('SamAccountName'))){
					$("#LockedOutUsers").append('</br/> <a href="#" onclick="Users.showUser(\''+line.trim()+'\')">'+line.trim()+'</a> ');
					unlockcode = ' <a href="#" onclick="Users.UnlockAccount(\''+line.trim()+'\')">Unlock</a>';
					$("#LockedOutUsers").append(unlockcode);
					  }
			});	
		}
	});
}
function getemailgroups(sam,appendid){
	GetJSONData('/Users/EmailGroups','&sam='+sam)
	.then(data => {
		if (data){
			data = JSON.parse(data)
			console.log(data)
			Users.GroupLists.EmailGroups = data
			$("#"+appendid).html("Email Groups:")
			data.forEach(function(line){
				$("#"+appendid).append('</br>'+line.Mail);
			});
		}
		else{console.log("No Data")}
	});
}
function setemailgroup(sam,emailgroup){
	PostJSONData('/Users/EmailGroups','&sam='+sam+'&emailgroup='+emailgroup+'')
	.then(data => {
		if (data){
			data = JSON.parse(data)
			console.log(data)
			log(data,'User')
		}
		else{console.log("No Data")}
	});
}
function setemailgroups(sam,emailgroups){
	PostJSONData('/Users/EmailGroups','&sam='+sam+'&emailgroups='+emailgroups+'')
	.then(data => {
		if (data){
			//data = JSON.parse(data)
			console.log(data)
			//log(data,'User')
		}
		else{console.log("No Data")}
	});
}
function removeemailgroups(sam,appendid){
	DeleteJSONData('/Users/EmailGroups','&sam='+sam)
	.then(data => {
		if (data){
			data = JSON.parse(data)
			console.log(data)
			$("#"+appendid).html("Email Groups:")
			data.forEach(function(line){
				$("#"+appendid).append('</br>'+line.Mail);
			});
		}
		else{console.log("No Data")}
	});
}
function getadgroups(sam,appendid){
	GetJSONData('/Users/ADGroups','&sam='+sam)
	.then(data => {
		data = JSON.parse(data)
		d = []
		d[0] = sam
		data.forEach(function(line){
			if (line != "" && !(line.includes('----')) && !(line.includes('name'))){
				$("#"+appendid).append('</br>'+line.trim());
				d.push(line.trim())
			}
		});
		Users.GroupLists.ADGroups = d
		console.log(d)
	});
}
function getLicense(sam){
	GetJSONData('/Users/Licenses','&upn='+sam+'@lwcky.com')
	.then(data => {
		//data = JSON.parse(data)
		console.log(data)
		log('Licenses: '+data,'user');
		$("#UserLicense").html('</br>'+data);
	});
}
function getMFA(sam){
	GetJSONData('/Users/MFA','&upn='+sam+'@lwcky.com')
	.then(data => {
		//data = JSON.parse(data)
		console.log(data)
		$("#UserMFA").html('</br>'+data);
	});
}
module.exports = {RefreshData,showUser,UnlockAccount,showLockouts,getemailgroups,setemailgroup,setemailgroups,getadgroups,removeemailgroups,GroupLists,getLicense,getMFA};

