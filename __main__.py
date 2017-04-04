#!/usr/bin/env python3
import security, ftp
import sys, os, subprocess

argumetns = sys.argv
if (len(argumetns) == 2 and argumetns[1] != 'update') or \
   (len(argumetns) == 3 and argumetns[1] not in ['pull', 'push', 'reset']) or  \
   (len(argumetns) != 3 and len(argumetns) != 2) :
	print("	panda pull <name>      - downloads newer content from the server")
	print("	panda push <name>      - uploads content of the local")
	print("	panda update	       - updates pandaSync")
	print("	panda reset <name>     - deletes saved creditals from the local disk")
	quit()

if argumetns[1] == 'reset' :
	try :
		os.remove(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".creditals-" + argumetns[2] ))
		print(ftp.col.plus, 'creditals deleted')
	except :
		print(ftp.col.minus, 'no save creditals found.')
	quit()

if argumetns[1] == 'update' :
	update = os.path.join(os.path.dirname(os.path.realpath(__file__)), "update.sh")
	os.execv(update, [''])
	quit()

ftps, loc = security.connect(argumetns[2])
if ftps is None :
	print(ftp.col.minus, 'could not connect')
	quit()

loc = os.path.abspath(loc)
ftp.create_path(os.path.join(loc, 'here'))
web = ftps.getcwd()



web_data = {}
local_data = {}

web_data = ftp.get_list(ftps)
if web_data == {} :
	print(ftp.col.minus, 'searching web')
	ftp.explore(web_data, web, ftps)

ftp.explore(local_data, loc)

print("\nChanges:")
if argumetns[1] == "pull" :
	changes, log = ftp.compare(web, loc, web_data, local_data)
	if changes == 0 :
		print(ftp.col.arrow, "no changes to be done\n")
	else :
		print(log)
		agree = input("do you wish to apply changes? ")
		if agree in ['y', 'Y', 'yes', "Yes", 'agree', 'a', 'A'] :
			ftp.download(web, loc, web_data, local_data, ftps)
elif argumetns[1] == "push" :
	changes, log = ftp.compare(loc, web, local_data, web_data)
	if changes == 0 :
		print(ftp.col.arrow, "no changes to be done\n")
	else :
		print(log)
		agree = input("do you wish to apply changes? ")
		if agree in ['y', 'Y', 'yes', "Yes", 'agree', 'a', 'A'] :
			ftp.upload(loc, web, local_data, web_data, ftps)



ftps.close()


