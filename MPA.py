import os
import subprocess
import sys
import colorama

colorama.init(convert=True)

objectlist = []


def parse(sentence, noun, verb, adverb1):
	wordlist = sentence.split(" ")
	thisword = wordlist[0]
	# if thisword is 'on', then next word is the noun
	if thisword == 'on':
		noun = wordlist[1]
		# if wordlist is greater than 2 then we must have a verb
		if len(wordlist) > 2:
			trash, verb, adverb1 = parse(" ".join(wordlist[2:]), noun, verb, adverb1)
	# if thisword is not 'on', then this is a verb. 
	# If noun is not set yet, then next word is the noun if noun is set then this is an adverb
	else:
		verb = thisword
		if len(wordlist) > 1:
			if noun == '' and len(objectlist) == 0:
				noun = wordlist[1]
			else:
				adverb1 = " ".join(wordlist[1:])
	return noun, verb, adverb1


def do(noun, verb, adverb1):
	if noun != '':
		print(colorama.Fore.YELLOW, "DO: ", verb, " on ", noun, colorama.Fore.RESET)

	global objectlist
	# print("N: ", noun, "V: ", verb, "Adv: ", adverb1)
	if noun != "" and verb == "":
		if noun == 'clear':
			objectlist = []
			print(colorama.Fore.YELLOW, "Cleared Objectlist!", colorama.Fore.RESET)
		else:
			objectlist.append(noun)
			print(colorama.Fore.YELLOW, "Appended: ", noun, colorama.Fore.RESET)
	if noun == "" and verb != "":
		if len(objectlist) == 0:
			print(colorama.Fore.YELLOW, 'Single Verb: ', verb, colorama.Fore.RESET)
		else:
			for object in objectlist:
				do(object, verb, adverb1)
	if noun != "" and verb != "":
		if verb == 'p' or verb == 'ping':
			print(colorama.Fore.YELLOW, "Ping: ", noun, colorama.Fore.RESET)
			o = os.system("ping -n 1 -a " + noun)
			print(o)
		if verb == 'r' or verb == 'run':
			# run the command verbatim.
			o = subprocess.run('SysinternalsSuite\\PsExec.exe \\\\' + noun + ' cmd /c "' + adverb1 + '"', capture_output=True)
			print(o.stderr.decode("utf-8"))
			#print(o)
			o = o.stdout.decode("utf-8").split("\r\n")
			
			for line in o:
				if 'PsExec' not in line and 'Copyright' not in line:
					if line != '' and 'Sysinternals' not in line:
						print(line)
		if verb == 'proc':
			# run the command verbatim.
			o = subprocess.run('SysinternalsSuite\\pslist.exe -x \\\\' + noun, capture_output=True)
			print(o.stderr.decode("utf-8"))

			o = o.stdout.decode("utf-8").split("\r\n")
			for line in o:
				if 'PsExec' not in line and 'Copyright' not in line:
					if line != '' and 'Sysinternals' not in line:
						print(line)

			# print(o)
		if verb == 'g' or verb == 'get':
			print(colorama.Fore.YELLOW, "Get: ", adverb1, " on ", noun, colorama.Fore.RESET)
			if adverb1 == 'user':
				o = subprocess.check_output('python modules\\getuser.py ' + noun)
				# print(o)
				o = o.decode(sys.stdout.encoding).split("\r\n")
				for line in o:
					if line != '':
						print(line)
			# adverbs: user, os, proccess list, ect.


while 1:
	sentence = input(">>")
	noun, verb, adverb1 = parse(sentence, '', '', '')
	do(noun, verb, adverb1)
	# print(objectlist)
