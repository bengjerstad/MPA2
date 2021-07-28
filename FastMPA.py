from fastapi import FastAPI
import pandas as pd

app = FastAPI()

datapath = 'C:\\Users\\bgjerstad\\Documents\\Data\\'

@app.get("/")
async def root():
    return {"message": "Hello World"}
	
@app.get("/Users")
async def users(s:str='',sam:str='',):
	if s == '' and sam == '':
		return ADUsers[['SamAccountName','displayName','telephoneNumber']].to_json(orient="records")
	if s != '':
		searchr0 = ADUsers[ADUsers.SamAccountName.str.lower().str.contains(s, na=False)]
		searchr1 = ADUsers[ADUsers.displayName.str.lower().str.contains(s, na=False)]
		searchr2 = ADUsers[ADUsers.telephoneNumber.str.lower().str.contains(s, na=False)]
		return pd.concat([searchr0,searchr1,searchr2])[['SamAccountName','displayName','telephoneNumber']].to_json(orient="records")
	if sam != '':
		searchr0 = ADUsers[ADUsers.sam == sam]
		return searchr0.to_json(orient="records")
	
#load user data
ADUsers = pd.read_csv(datapath+'ADUsers.csv')
ADUsers['sam'] = ADUsers.SamAccountName.str.lower()
ADGroups = pd.read_csv(datapath+'ADGroups.csv')
PhoneNumbers = pd.read_csv(datapath+'PhoneNumbers.csv')
	
@app.get("/Computers")
async def computers():
    return {"message": "computer"}
	
#load computer data
Computers = pd.read_csv(datapath+'Computers.csv')	
	

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