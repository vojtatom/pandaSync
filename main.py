import security, ftp
import os
from pprint import pprint
import sys

argumetns = sys.argv
if len(argumetns) != 2 :
	print("pull or push arguments expected")
	quit()

ftps, loc = security.connect()
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


