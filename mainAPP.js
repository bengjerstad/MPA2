//imports
window.$ = window.jQuery = require('././jquery-3.4.1.min.js');


const exec = require('child_process').exec;
const fs = require('fs');
const {shell} = require('electron');
const electron = require('electron');
const { clipboard } = require('electron')
const dialog = electron.remote.dialog;

//  Modules
const Users = require("./main_modules/Users");
const KB = require("./main_modules/KB");

async function GetJSONData(path,arg){
	r = {}
	await $.ajax({type : 'GET',
		url : "http://127.0.0.1:8000"+path+"?format=json"+arg,
		success : function(response) {
			r = response;
			//console.log(response);
			return response;
		},
		error : function(xhr, status, error) {
			//var err = eval("(" + xhr.responseText + ")");
			console.log(xhr);
			//Stat('Error: '+err);
			throw err; 
		}
	})
	return r;
}
async function PostJSONData(path,arg){
	r = {}
	await $.ajax({type : 'POST',
		url : "http://127.0.0.1:8000"+path+"?format=json"+arg,
		success : function(response) {
			r = response;
			//console.log(response);
			return response;
		},
		error : function(xhr, status, error) {
			//var err = eval("(" + xhr.responseText + ")");
			console.log(xhr);
			//Stat('Error: '+err);
			throw err; 
		}
	})
	return r;
}
async function DeleteJSONData(path,arg){
	r = {}
	await $.ajax({type : 'DELETE',
		url : "http://127.0.0.1:8000"+path+"?format=json"+arg,
		success : function(response) {
			r = response;
			//console.log(response);
			return response;
		},
		error : function(xhr, status, error) {
			//var err = eval("(" + xhr.responseText + ")");
			console.log(xhr);
			//Stat('Error: '+err);
			throw err; 
		}
	})
	return r;
}
async function PutJSONData(path,arg){
	r = {}
	await $.ajax({type : 'PUT',
		url : "http://127.0.0.1:8000"+path+"?format=json"+arg,
		success : function(response) {
			r = response;
			//console.log(response);
			return response;
		},
		error : function(xhr, status, error) {
			//var err = eval("(" + xhr.responseText + ")");
			console.log(xhr);
			//Stat('Error: '+err);
			throw err; 
		}
	})
	return r;
}
async function GetData(path,arg){
	r = {}
	console.log(path)
	await $.ajax({type : 'GET',
		url : "http://127.0.0.1:8000"+path+"?"+arg,
		success : function(response) {
			r = response;
			//console.log(response);
			return response;
		},
		error : function(xhr, status, error) {
			//var err = eval("(" + xhr.responseText + ")");
			console.log(xhr);
			//Stat('Error: '+err);
			throw err; 
		}
	})
	return r;
}

//globals


var API = {}

//DateTimeGlobals
var today = new Date();

var todaylastmonth = new Date();
todaylastmonth.setMonth(todaylastmonth.getMonth()-1);
var thisyear = today.getFullYear()

var thisyearZ = today.getFullYear()

var lastmonthZ = ("0" + (today.getMonth())).slice(-2);
if (lastmonthZ == '00') {lastmonthZ == '12';thisyearZ == thisyearZ-1;}

var thismonthZ = ("0" + (today.getMonth() + 1)).slice(-2);

var thismonthlong = today.toLocaleString('default', { month: 'long' });
var lastmonthlong = todaylastmonth.toLocaleString('default', { month: 'long' });

//  Other Globals
var AdvSDisabled = 0;

//Universal Functions
//  GUI and Nav
function Clear(id){
	$("#"+id).html("");
}
function ClearHide(id){
	$("#"+id).hide('fast');
}
function Max(id){
	$("#"+id).toggleClass('max', 'addOrRemove');
	//$("#"+id).addClass('max');
}
function Min(id){
	$("#"+id).removeClass('max');
}
// Build GUI elements
function LoadViewPanes(){
	$( ".viewpane" ).each(function( index,object ) {
		//$(this).append("Test.");
		//console.log(this);
	});
}

//PopUp Menu
function newPopUp(){
	html = '<div id="popmenu" class="popmenu">';
	html += '<div id="popmenunav">'
	html += '<a href="#" onclick="$(\'#popmenu\').remove();" style="float:right;">'
	html += '<img class="nav-icon" src="images/cancel.svg"/>'
	html += '</a>'
	html += '</div>'
	html += '</div>'
	return html
}
function addcolPopUp(name){
	$("#popmenu").append('<div id="popmenu'+name+'" class="popcolumn"></div>');
}
// Search
//  Generic Search Function
function searchData(){
	$("#col0").html("");
	$("#col1").html("");
	$("#col2").html("");
	var search = $("#in0").val().toLowerCase();
	if (search != ''){
		CurrentData = $("#SearchData").val();
		
		//var lastvar = '';
		
		//users search
		GetJSONData('/Users','&s='+search)
		.then(data => {
			data = JSON.parse(data);
			//console.log(data)
			data.forEach(function(row,rownumber){
				show = '<br/><a href="#" onclick="Users.showUser(\''+row.SamAccountName+'\');return false;">'+row.SamAccountName+'</a>';
				$("#col0").append(show);
				$("#col1").append("<br/>"+row.displayName);
		});
			
		});
		
		//window[CurrentData].forEach(function(row,rownumber){
		//	lastvar = window['search'+CurrentData](row,rownumber,search,lastvar);
		//});
	}

}


//  Extra Search Features
function ViewMoreSearch(){
	if ($("#AdvS").html() == ''){
		html = ' <li><a href="#" onclick="$(\'#SearchData\').val(\'ADUsers\searchData();"><img class="icon iconred" src="images/multiple-users-silhouette.svg"/></a></li>';
	    html += '<li><a href="#" onclick="$(\'#SearchData\').val(\'Computers\');searchData();"><img class="icon iconred" src="images/desktop-monitor.svg"/></a></li>';
	    html += '<li><a href="#" onclick="$(\'#SearchData\').val(\'Apps\');searchData();">App</a></li>';
		html += '<li><a href="#" onclick="$(\'#SearchData\').val(\'JTtoGroups\');searchData();">JT</a></li></span>';
		html += '<span id="AdvSDisabledButton" class="off" onclick="ToggleAdvSDisabled();">Disabled</a>';
		$("#AdvS").html(html);
	   $("#ViewMoreSearchButton").css("transform","scale(-1, 1)");
	}
	else{
	   $("#AdvS").html("");
	   $("#ViewMoreSearchButton").css("transform","scale(1, 1)");
	   AdvSDisabled = 0;
	}
}
function ToggleAdvSDisabled(){
	if (AdvSDisabled == 0){
	   AdvSDisabled = 1;
	   $("#AdvSDisabledButton").attr('class','good');
	}
	else{
	   AdvSDisabled = 0;
	   $("#AdvSDisabledButton").attr('class','off');
	}
}
function ClickFirstOption(){
	$("#col0 a").first().trigger('click');
}
//  Stat Functions
function Stat(msg){
	$("#tasklog").prepend("<br/>"+msg);
}
function log(msg,context){
	$("#tasklog").prepend(msg+'<span style="font-size:.8em">('+context+')</span>');
}
function MaxStat(){ 
	fs.readFile('statlog.log', function (err,statloglines) {
		if (err) {console.log(err)}
		$("#stat").html('<a href="#" onclick="MinStat();"><img class="nav-icon" src="images/cancel.svg" /></a>');
		lines = statloglines.toString().split("\r\n");
		
		lines.forEach(function(line) {
			$("#stat").append('<br/>'+line);
		});
		
		$("#stat").css({"height":"100%"});
		//$("#stat").attr( "onClick", "MinStat()" );
		$("#stat").attr( "onClick", "" );
	});	
}
function MinStat(){ 
	fs.readFile('statlog.log', function (err,data) {
		if (err) {console.log(err)}
		else{
			//$("#stat").html(data);
			$("#stat").html('<a href="#" onclick="MaxStat();"><img class="nav-icon" src="images/cancel.svg" /></a>');
			$("#stat").css({"height":"1em"});
			//$("#stat").attr( "onClick", "MaxStat()" );
			}
	});	
}
function KeepLogStat(line){
	fs.appendFile(path.data+'MPA.log', line+"\r\n", function (err) {if (err) {console.log(err)}});
} 
function ClearStat(){ 
	fs.readFile('statlog.log', function (err,statloglines) {
		if (err) {console.log(err)}
		lines = statloglines.toString().split("\r\n");
		lines.forEach(function(line) {
			if (line.includes('AD Change')){
				KeepLogStat(line);
			}
			if (line.includes('AD Account')){
				KeepLogStat(line);
			}
			if (line.includes('Unlocked account')){
				KeepLogStat(line);
			}
			if (line.includes('R:')){
				KeepLogStat(line);
			}
			if (line.includes('new Work Order')){
				KeepLogStat(line);
			}
		});
		logmsg = 'R:'+today.toDateString()+' '+today.toLocaleTimeString()+"\r\n";
		fs.writeFile('statlog.log', logmsg, function (err) {if (err) {console.log(err)}});
	});	
	
}

//Functions for Modules to use
function clearallinputs(Section){
		$("#"+Section+" > input").each((x,y) =>{
		var inputs = $(y);
		if (inputs.attr('type') != 'checkbox'){
			inputs.val("");
			//console.log(inputs.val());
		}
	});
}


clipboard['lastE'] =  function(x){
	clipboard.writeText(x.previousSibling.innerText);
}

//shortcut functions for running external functions and scripts
function ex(path){
	GetData('/run','program=ex&r='+path);
}
function python(path){
	GetData('/run','program=python&r='+path)
	.then(data => {
		console.log(data);
		Stat(data);
	});
}
function powershell(path){
	GetData('/run','program=powershell&r='+path)
	.then(data => {
		console.log(data);
	});
}
function cmd(path){
	GetData('/run','program=cmd&r='+path)
	.then(data => {
		console.log(data);
	});
}