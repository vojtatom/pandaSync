from ftplib import FTP_TLS
import ftputil
import json
import os

class col:
	minus = '\033[91m-\033[0m'
	plus = '\033[92m+\033[0m'
	arrow = '\033[96m>\033[0m'

def get_list(ftps) :
	path = os.path.join(os.path.dirname(os.path.realpath(__file__)), ".tmp.json")
	try :
		ftps.download("/.ftplist.json", path)
		with open('.tmp.json', 'r') as file :
			database = json.loads(file.read())	
		os.remove(path)
		return database
	except :
		try :
			os.remove(path)
		except :
			pass
		return {}

def upload_list(database, ftps) :
	path = os.path.join(os.path.dirname(os.path.realpath(__file__)), ".tmp.json")
	try :
		with open('.tmp.json', 'w') as file :
			file.write(json.dumps(database))
		ftps.upload(path, "/.ftplist.json")
		os.remove(path)
	except :
		try :
			os.remove(path)
		except :
			pass
		print(col.arrow, 'database not updated')


def explore(database, dic, inter=os) :
	cf = inter.listdir(dic)
	for f in cf :
		f = inter.path.join(dic, f)
		if inter.path.islink(f) :
			pass
		elif inter.path.isdir(f) :
			explore(database, f, inter)
		else :
			database[f] = inter.path.getmtime(f)


def compare(src, dst, src_dat, dst_dat) :
	src_len = len(src)
	changes = 0
	log = ""
	for file in src_dat :
		if os.path.basename(file) in ('.DS_Store', '.ftplist.json') :
			src_dat[file] = [ False, src_dat[file]]
			continue

		path = os.path.join(dst, file[src_len:])
		if path in dst_dat :
			if dst_dat[path] >= src_dat[file] :
				src_dat[file] = [ False, src_dat[file]]
			else :
				# print('local', dst_dat[path], 'web', src_dat[file])
				src_dat[file] = [ True, src_dat[file]]
				log = log + col.plus + " {}\n".format(path)
				changes += 1
		else :
			src_dat[file] = [ True, src_dat[file]]
			log = log + col.plus + " {}\n".format(path)
			changes += 1

	dst_len = len(dst)
	for file in dst_dat :
		if os.path.basename(file) in ('.DS_Store', '.ftplist.json') :
			dst_dat[file] = [ False, dst_dat[file]]
			continue

		path = os.path.join(src, file[dst_len:])
		if path not in src_dat :
			dst_dat[file] = [ True, dst_dat[file]]
			log = log + col.minus + " {}\n".format(file)
		else :
			dst_dat[file] = [ False, dst_dat[file]]

	return changes, log


def create_path(path, inter=os) :
	directory = inter.path.dirname(path)
	if not inter.path.exists(directory):
		inter.makedirs(directory)


def delete_folder(path, inter=os) :
	directory = inter.path.dirname(path)
	if not inter.listdir(directory):
		inter.rmdir(directory)


def download(src, dst, src_dat, dst_dat, ftps) :
	src_len = len(src)
	for file in src_dat :
		if src_dat[file][0] :
			path = os.path.join(dst, file[src_len:])
			create_path(path)
			print(col.plus, "downloading", path)
			ftps.download(file, path)
			os.utime(path, (src_dat[file][1], src_dat[file][1]))

	dst_len = len(dst)
	for file in dst_dat :
		if dst_dat[file][0] :
			print(col.minus, "deleting", file)
			os.remove(file)
			delete_folder(file)

def upload(src, dst, src_dat, dst_dat, ftps) :
	src_len = len(src)
	server_dict = {}

	for file in src_dat :
		path = ftps.path.join(dst, file[src_len:])
		if src_dat[file][0] :
			create_path(path, ftps)
			print(col.plus, "uploading", path)
			ftps.upload(file, path)
			server_dict[path] = src_dat[file][1]
		else :
			if path in dst_dat :
				server_dict[path] = dst_dat[path][1]

	dst_len = len(dst)
	for file in dst_dat :
		if dst_dat[file][0] :
			print(col.minus, "deleting", file)
			ftps.remove(file)
			delete_folder(file, ftps)
		else :
			if file not in server_dict :
				server_dict[file] = dst_dat[file][1]

	upload_list(server_dict, ftps)

			