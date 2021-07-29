from fastapi import FastAPI
import pandas as pd
from json2html import *
import json
import os
import subprocess
import sys

app = FastAPI()

datapath = 'C:\\Users\\bgjerstad\\Documents\\Data\\'

@app.get("/")
async def root():
    return {"message": "Hello World"}
	
@app.get("/Users")
async def users(s:str='',sam:str='',format:str='json'):
	if s == '' and sam == '':
		return rtformat(ADUsers[['SamAccountName','displayName','telephoneNumber']],format)
	if s != '':
		searchr0 = ADUsers[ADUsers.SamAccountName.str.lower().str.contains(s, na=False)]
		searchr1 = ADUsers[ADUsers.displayName.str.lower().str.contains(s, na=False)]
		searchr2 = ADUsers[ADUsers.telephoneNumber.str.lower().str.contains(s, na=False)]
		return rtformat(pd.concat([searchr0,searchr1,searchr2])[['SamAccountName','displayName','telephoneNumber']],format)
	if sam != '':
		searchr0 = ADUsers[ADUsers.sam == sam]
		return rtformat(searchr0.to_json(orient="records"),format)
	
#load user data
ADUsers = pd.read_csv(datapath+'ADUsers.csv')
ADUsers['sam'] = ADUsers.SamAccountName.str.lower()
ADGroups = pd.read_csv(datapath+'ADGroups.csv')
PhoneNumbers = pd.read_csv(datapath+'PhoneNumbers.csv')

@app.get("/Users/Lockout")
async def usersLockout(s:str='',sam:str='',format:str='json'):
	cmd = 'powershell "Search-ADAccount -Locked | select SamAccountName"';
	o = subprocess.run(cmd, capture_output=True)
	if o.stderr.decode("utf-8") == '':
		return "No Users are Locked Out"
	else:
		return o.stderr.decode("utf-8")
	
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
async def KB():
    return {"message": "KB"}
	
#load KB data
	
@app.get("/Newusers")
async def newusers():
    return {"message": "Newusers"}
	
#load NewUsers Data
Markdowndatapath = 'C:\\Users\\bgjerstad\\Documents\\KB\\'

def rtformat(output,format):
	if (format == "html"):
		return output.to_html(index=False).replace('\n', "") 
	if (format == "table"):
		return json2html.convert(json.loads(output.to_json(orient="records")))
	if (format == "json"):
		return output.to_json(orient="records")
	return output
