from fastapi import FastAPI
import pandas as pd
import numpy as np
from json2html import *
import json
import os
import subprocess
import sys
from markdown import markdown

app = FastAPI()

datapath = 'C:\\Users\\bgjerstad\\Documents\\Data\\'
KBpath = 'C:\\Users\\bgjerstad\\Documents\\KB\\'
agentusername = 'bgjerstad@lwcky.com'

@app.get("/")
async def root():
    return {"message": "Hello World"}
	
@app.get("/Users")
async def users(s:str='',sam:str='',enabled:str='',format:str='json'):
	if s == '' and sam == '':
		return rtformat(ADUsers[['SamAccountName','displayName']],format,"pd")
	if s != '':
		searchr0 = ADUsers[ADUsers.SamAccountName.str.lower().str.contains(s, na=False)]
		searchr1 = ADUsers[ADUsers.displayName.str.lower().str.contains(s, na=False)]
		searchr2 = ADUsers[ADUsers.telephoneNumber.str.lower().str.contains(s, na=False)]
		concatsearch = pd.concat([searchr0,searchr1,searchr2])[['SamAccountName','displayName','Enabled','distinguishedname']].drop_duplicates()
		if enabled == '' or enabled == '0':
			#hide inactive accounts
			concatsearch = concatsearch[concatsearch['Enabled'] == True]

		
		#filter on distinguishedname
		concatsearch = concatsearch[concatsearch['distinguishedname'].str.contains("OU=LWC")]
		concatsearch = concatsearch[~concatsearch['distinguishedname'].str.contains("ADMIN UTILITY")]
		
		return rtformat(concatsearch.head(48),format,"pd")
	if sam != '':
		sam = sam.lower()
		searchr0 = ADUsers[ADUsers.sam == sam]
		return searchr0.to_json(orient="records")
			
#load user data
ADUsers = pd.read_csv(datapath+'ADUsers.csv')
ADUsers['sam'] = ADUsers.SamAccountName.str.lower()
NewUser = pd.read_csv(datapath+'NewUser.csv')
NewUser['Ticket'] = NewUser['Ticket'].astype(str)
#ADGroups = pd.read_csv(datapath+'ADGroups.csv')
#PhoneNumbers = pd.read_csv(datapath+'PhoneNumbers.csv')

@app.post("/Users")
async def users(s:str='',format:str='json'):
	global ADUsers
	if s == 'refresh':
		cmd = 'powershell ".\\extra_modules\\GetADUsers.ps1"'
		o = subprocess.run(cmd, capture_output=True)
		data = o.stdout.decode("utf-8")
		ADUsers = pd.read_csv(datapath+'ADUsers.csv')
		ADUsers['sam'] = ADUsers.SamAccountName.str.lower()
		return rtformat(data,format,'cmdstring')

@app.get("/Users/Live")
async def usersLive(sam:str='',detailed:str='',format:str='json'):
	if sam != '':
		if detailed == '':
			cmd = 'powershell ".\\extra_modules\\GetADUser.ps1" "-sam '+sam+'"'
		else:
			cmd = 'powershell ".\\extra_modules\\GetADUserDetailed.ps1" "-sam '+sam+'"'
		o = subprocess.run(cmd, capture_output=True)
		data = o.stdout.decode("utf-8")
		return rtformat(data,format,'kvstring')

		
@app.get("/Users/Attribs")
async def usersAttribsGet(sam:str='',what:str='',format:str='json'):
	if sam != '':
		cmd = 'powershell -command "Get-ADUser -Identity '+sam+' -Properties '+what+' | Select-Object -ExpandProperty '+what+'"';
		o = subprocess.run(cmd, capture_output=True)
		data = o.stdout.decode("utf-8")
		return rtformat(data,format,'cmdstring')
		
@app.post("/Users/Attribs")
async def usersAttribsSet(sam:str='',what:str='',val:str='',format:str='json'):
	if sam != '':
		cmd = 'powershell -command "Set-ADUser '+sam+' -Add @{\''+what+'\'=\''+val+'\'}"'
		o = subprocess.run(cmd, capture_output=True)
		data = o.stdout.decode("utf-8")
		return rtformat(data,format,'cmdstring')
		
@app.get("/Users/Lockout")
async def usersLockout(s:str='',sam:str='',format:str='json'):
	if sam == '':
		cmd = 'powershell "Search-ADAccount -Locked | select SamAccountName"'
		o = subprocess.run(cmd, capture_output=True)
		data = o.stdout.decode("utf-8")
		return rtformat(data,format,'cmdstring')
	if sam != '':
		cmd = 'powershell "Unlock-ADAccount -Identity '+sam+'"'
		o = subprocess.run(cmd, capture_output=True)
		data = o.stdout.decode("utf-8")
		return rtformat(data,format,'cmdstring')
		
@app.get("/Users/EmailGroups")
async def usersEmailGroups(sam:str='',format:str='json'):
	if sam != '':
		cmd = 'powershell ".\\extra_modules\\GetMailGroups.ps1" "-sam '+sam+'" "-agentusername '+agentusername+'"'
		o = subprocess.run(cmd, capture_output=True)
		data = o.stdout.decode("utf-8")
		err = o.stderr.decode("utf-8")
		print(err)
		return data
		
@app.post("/Users/EmailGroups")
async def usersEmailGroups(sam:str='',emailgroup:str='',emailgroups:str='',format:str='json'):
	if sam != '':
		if emailgroup != '':
			cmd = 'powershell ".\\extra_modules\\SetMailGroups.ps1" "-sam '+sam+'" "-agentusername '+agentusername+'" "-groupname '+emailgroup+'"'
		if emailgroups != '':
			cmd = 'powershell ".\\extra_modules\\SetMailGroups2.ps1" "-sam '+sam+'" "-agentusername '+agentusername+'" "-groupnames '+emailgroups+'"'
		o = subprocess.run(cmd, capture_output=True)
		data = o.stdout.decode("utf-8")
		err = o.stderr.decode("utf-8")
		print(err)
		return data
		
		
@app.delete("/Users/EmailGroups")
async def usersEmailGroups(sam:str='',format:str='json'):
	if sam != '':
		cmd = 'powershell ".\\extra_modules\\RemoveMailGroups.ps1" "-sam '+sam+'" "-agentusername '+agentusername+'"'
		o = subprocess.run(cmd, capture_output=True)
		data = o.stdout.decode("utf-8")
		return data
	
@app.get("/Users/Licenses")
async def usersLicenses(upn:str='',format:str='json'):
	if upn != '':
		cmd = 'powershell ".\\extra_modules\\CheckLicenses.ps1" "-upn '+upn+'" "-agentusername '+agentusername+'"'
		o = subprocess.run(cmd, capture_output=True)
		err = o.stderr.decode("utf-8")
		print(err)
		data = o.stdout.decode("utf-8")
		return data	
		
@app.post("/Users/Licenses")
async def usersLicenses(upn:str='',licenses:str='',format:str='json'):
	if upn != '':
		cmd = 'powershell ".\\extra_modules\\SetLicenses.ps1" "-upn '+upn+'" "-agentusername '+agentusername+' -licenses '+licenses+'"'
		o = subprocess.run(cmd, capture_output=True)
		data = o.stdout.decode("utf-8")
		err = o.stderr.decode("utf-8")
		print(err)
		return data	
		
@app.get("/Users/MFA")
async def usersMFA(upn:str='',format:str='json'):
	if upn != '':
		cmd = 'powershell ".\\extra_modules\\CheckMFA.ps1" "-upn '+upn+'" "-agentusername '+agentusername+'"'
		o = subprocess.run(cmd, capture_output=True)
		data = o.stdout.decode("utf-8")
		err = o.stderr.decode("utf-8")
		print(err)
		return data	

@app.post("/Users/MFA")
async def usersMFA(upn:str='',format:str='json'):
	if upn != '':
		cmd = 'powershell ".\\extra_modules\\SetMFA.ps1" "-upn '+upn+'" "-agentusername '+agentusername+'"'
		o = subprocess.run(cmd, capture_output=True)
		data = o.stdout.decode("utf-8")
		return data	


@app.get("/Users/ADGroups")
async def usersADGroups(sam:str='',format:str='json'):
	if sam != '':
		cmd = 'powershell "Get-ADPrincipalGroupMembership '+sam+' | select name"';
		o = subprocess.run(cmd, capture_output=True)
		data = o.stdout.decode("utf-8")
		err = o.stderr.decode("utf-8")
		print("Error: ",err)
		return rtformat(data,format,'cmdstring')
		
@app.post("/Users/ADGroups")
async def usersADGroups(sam:str='',group:str='',format:str='json'):
	if sam != '':
		cmd = 'powershell "Add-ADGroupMember -Identity \''+group+'\' -Members '+sam+'"';
		o = subprocess.run(cmd, capture_output=True)
		data = o.stdout.decode("utf-8")
		if data == '':
			return rtformat(group,format,'cmdstring')
		else:
			return rtformat(data,format,'cmdstring')
		err = o.stderr.decode("utf-8")
		print("Error: ",err)
		
		
@app.get("/Users/NewUser")
async def getusersNewUser(ticket:str='',format:str='json'):
	if ticket == '':
		return rtformat(NewUser,format,"pd")
	else:
		return rtformat(NewUser[NewUser['Ticket'] == ticket],format,"pd")
		
@app.post("/Users/NewUser")
async def postusersNewUser(ticket:str='',key:str='',val:str='',format:str='json'):
	global NewUser
	if ticket != '':
		NewUser.loc[NewUser.Ticket == ticket, key] = val
		NewUser.to_csv(datapath+'NewUser.csv',index=False)
		return rtformat(NewUser[NewUser['Ticket'] == ticket],format,"pd")

@app.put("/Users/NewUser")
async def putusersNewUser(ticket:str='',format:str='json'):
	global NewUser
	if ticket == '':
		NewUserModified = NewUser.append(pd.Series(),ignore_index=True)
		NewUserModified['Ticket'].iloc[-1] = str(int(NewUser['Ticket'].iloc[-1])+1)
		NewUser = NewUserModified
		NewUserModified.to_csv(datapath+'NewUser.csv',index=False)
	if ticket != '':
		NewUserModified = NewUser.append(pd.Series(),ignore_index=True)
		NewUserModified['Ticket'].iloc[-1] = ticket
		NewUser = NewUserModified
		NewUserModified.to_csv(datapath+'NewUser.csv',index=False)
		
	return rtformat(NewUserModified.tail(1),format,"pd")

		
@app.get("/Computers")
async def computers():
    return {"message": "computer"}
	
#load computer data
#Computers = pd.read_csv(datapath+'Computers.csv')	

			#o = subprocess.run('SysinternalsSuite\\PsExec.exe \\\\' + noun + ' cmd /c "' + adverb1 + '"', capture_output=True)
			#print(o.stderr.decode("utf-8"))
	


@app.get("/Tickets")
async def tickets():
    return {"message": "Tickets"}

	
@app.get("/Orders")
async def orders():
    return {"message": "Orders"}
	
#load Orders data	
#Orders = pd.read_csv(datapath+'Orders.csv')	
	
@app.get("/KB")
async def KB(s:str='',f:str=''):
	if f == '':
		return os.listdir(KBpath+'\\'+s)
	else:
		with open(KBpath+'\\'+s+'\\'+f, 'r') as f:
			text = f.read()
			html = markdown(text)
		return html

	
@app.get("/run")
async def run(program:str='',r:str='',format:str='json'):
	cmd = ''
	if program == 'powershell':
		cmd = 'powershell '+r
	if program == 'ex':
		cmd = 'explorer.exe '+r
	if program == 'python':
		cmd = 'python '+r
	if program == 'cmd':
		cmd = 'cmd /c "'+r+'"'
	o = subprocess.run(cmd, capture_output=True)
	data = o.stdout.decode("utf-8")
	err = o.stderr.decode("utf-8")
	print("error: ",err)
	print(data)
	return rtformat(data,format,'cmdstring')


def rtformat(input,formatout,formatin):
	if formatin == "pd":
		if (formatout == "html"):
			return input.to_html(index=False).replace('\n', "") 
		if (formatout == "table"):
			return json2html.convert(json.loads(input.to_json(orient="records")))
		if (formatout == "json"):
			return input.to_json(orient="records")
	if formatin == "kvstring":
		input = input.splitlines()
		output = {}
		for line in input:
			if ":" in line:
				keyvalue = line.split(":",1)
				key,value = keyvalue[0].strip(),keyvalue[1].strip()
				output[key] = value
		if (formatout == "json"):
			return json.dumps(output)
	if formatin == "cmdstring":
		input = input.splitlines()
		return json.dumps(input)

