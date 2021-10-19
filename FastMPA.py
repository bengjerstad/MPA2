from fastapi import FastAPI
import pandas as pd
from json2html import *
import json
import os
import subprocess
import sys
from markdown import markdown

app = FastAPI()

datapath = 'C:\\Users\\bgjerstad\\Documents\\Data\\'
KBpath = 'C:\\Users\\bgjerstad\\Documents\\KB\\'

@app.get("/")
async def root():
    return {"message": "Hello World"}
	
@app.get("/Users")
async def users(s:str='',sam:str='',format:str='json'):
	if s == '' and sam == '':
		return rtformat(ADUsers[['SamAccountName','displayName']],format,"pd")
	if s != '':
		searchr0 = ADUsers[ADUsers.SamAccountName.str.lower().str.contains(s, na=False)]
		searchr1 = ADUsers[ADUsers.displayName.str.lower().str.contains(s, na=False)]
		searchr2 = ADUsers[ADUsers.telephoneNumber.str.lower().str.contains(s, na=False)]
		concatsearch = pd.concat([searchr0,searchr1,searchr2])[['SamAccountName','displayName','Enabled','distinguishedname']].drop_duplicates()
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
ADGroups = pd.read_csv(datapath+'ADGroups.csv')
PhoneNumbers = pd.read_csv(datapath+'PhoneNumbers.csv')

@app.get("/Users/Live")
async def usersLockout(sam:str='',format:str='json'):
	if sam != '':
		cmd = 'powershell ".\\extra_modules\\GetADUser.ps1" "-sam '+sam+'"';
		o = subprocess.run(cmd, capture_output=True)
		data = o.stdout.decode("utf-8")
		return rtformat(data,format,'kvstring')
		

@app.get("/Users/Lockout")
async def usersLockout(s:str='',sam:str='',format:str='json'):
	if sam == '':
		cmd = 'powershell "Search-ADAccount -Locked | select SamAccountName"';
		o = subprocess.run(cmd, capture_output=True)
		data = o.stdout.decode("utf-8")
		return rtformat(data,format,'cmdstring')
	if sam != '':
		cmd = 'powershell "Unlock-ADAccount -Identity '+sam+'"';
		o = subprocess.run(cmd, capture_output=True)
		data = o.stdout.decode("utf-8")
		return rtformat(data,format,'cmdstring')
	
@app.get("/Computers")
async def computers():
    return {"message": "computer"}
	
#load computer data
Computers = pd.read_csv(datapath+'Computers.csv')	

			#o = subprocess.run('SysinternalsSuite\\PsExec.exe \\\\' + noun + ' cmd /c "' + adverb1 + '"', capture_output=True)
			#print(o.stderr.decode("utf-8"))
	

@app.get("/Tickets")
async def tickets():
    return {"message": "Tickets"}

	
@app.get("/Orders")
async def orders():
    return {"message": "Orders"}
	
#load Orders data	
Orders = pd.read_csv(datapath+'Orders.csv')	
	
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
async def usersLockout(program:str='',r:str='',format:str='json'):
	cmd = ''
	if program == 'powershell':
		cmd = 'powershell '+r
	if program == 'ex':
		cmd = 'explorer.exe '+r
	if program == 'python':
		cmd = 'python '+r
	o = subprocess.run(cmd, capture_output=True)
	data = o.stdout.decode("utf-8")
	return rtformat(data,format,'cmdstring')


@app.get("/Newusers")
async def newusers():
    return {"message": "Newusers"}
	
#load NewUsers Data
Markdowndatapath = 'C:\\Users\\bgjerstad\\Documents\\KB\\'

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

