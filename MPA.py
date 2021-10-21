import requests

objectlist = []
verblist = []

def setobject(key,val):
	for object in objectlist:
		object[key] = val

	return objectlist

# define verbs
def r(noun,adverb):
	print('r')
	
def ping(noun):
	print('ping')
	
def get(noun):
	print('get')
	
def unlock(noun):
	print('unlock')
	
def find(noun):
	if noun == 'locked':
		r = requests.get('http://127.0.0.1:8000/Users/Lockout?format=json')
		print(r.json())
	else:
		r = requests.get('http://127.0.0.1:8000/Users?format=json&s='+noun)
		print(r.json())
		
	
verbs = {'ping':ping,'get':get,'unlock':unlock,'r':r,'find':find}

while 1:
	sentence = input(">>")
	wordlist = sentence.split(" ")
	firstword = wordlist[0]
	
	#first word=context
	#second word=noun
	if firstword == 'on':
		objectlist.append({'context':'computer','noun':wordlist[1],'verb':''})
	if firstword == 'user':
		objectlist.append({'context':'user','noun':wordlist[1],'verb':''})
		
	#first word=verb
	#context implied
	#3rd word is noun
	if firstword == 'find':
		if wordlist[1] == 'user':
			objectlist.append({'context':'user','noun':wordlist[2],'verb':'find'})
		if wordlist[1] == 'locked':
			objectlist.append({'context':'user','noun':'locked','verb':'find'})
			
	#first word=verb
	if firstword == 'r':
		objectlist = setobject('verb','r')
		objectlist = setobject('adverb',wordlist[1:])
	if firstword == 'get':
		objectlist = setobject('verb','get')
		objectlist = setobject('adverb',wordlist[1:])
	if firstword == 'ping':
		objectlist = setobject('verb','ping')
	if firstword == 'unlock':
		objectlist = setobject('verb','unlock')
	
	for object in objectlist:
		#print(object)
		if object['verb']:
			#print('Do '+object['verb']+':')
			verbs[object['verb']](object['noun'])
		
	print(objectlist)
