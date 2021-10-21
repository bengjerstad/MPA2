import os
import subprocess
import sys
import colorama

colorama.init(convert=True)

objectlist = []
verblist = []

def setobject(key,val):
	for object in objectlist:
		object[key] = val

	return objectlist

# define verbs
def r():
	print('r')
	
def ping():
	print('ping')
	
def get():
	print('get')
	
def unlock():
	print('unlock')
	
verbs = {'ping':ping,'get':get,'unlock':unlock,'r':r}

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
			print('Do '+object['verb']+':')
			verbs[object['verb']]()
		
	print(objectlist)
