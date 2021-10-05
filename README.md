# MPA2
MPA - My Personal AdminConsole
MPA combines tools and functions in a moduler way to help IT professionals complete routine tasks. 

## Target Goals
MPA is built as a moduler as possible so that, as goals change, extra features can be incorprtated later. Each Module represents a certin set of goals, but is usally built around the functions of a data(CSV file,json or markdown files) and an API.

For example, the users core module is built around a csv file that is a user data dump of the Active Directory. All functions for viewing the data and interacting with the Active Directory(users objects only) will be placed within this module. A module can be built around a data dump and API calls to a helpdesk ticking sytem. The module would contain only functions for interacting with the data dump or the ticketing system. 

###Core Modules:
Users:
Searching for users by username or display name or telephone from an AD dump. 
Viewing important user details from an active AD connection such as password last set and is account locked out.
Unlocking user accounts.

Computers: 
ping, finding who is logged in, running commands, opening the admin share in explorer ect. 

KB:
Use markdown for Knowlage base articles to create interactive procedures.




## Install
1. Install Electron, fastapi and uvicorn

npm install electron --save-dev
pip install fastapi
pip install uvicorn[standard]

2. Install other python modules
### json2html
pip install json2html

##Why 2
MPA is a re-write of my MPA project to use FastAPI as the core logic and either MPAGui(electron) or python MPA.py as the front end. 
In MPA, MPAGui had all of the core logic written in JavaScript and the python MPA.py was left with little to work with since the core logic was all in the Javascript Modules. In MPA2, all core logic is going to be put into fastAPI. 