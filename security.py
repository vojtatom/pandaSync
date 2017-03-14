import ftputil
from Crypto.Cipher import AES
import Crypto.Random.OSRNG.posix as defiv
import json
from getpass import getpass
import os
from ftp import col, create_path


def conv_bytes(val) :
	return val.to_bytes(32, byteorder='little', signed=False)


def conv_int(val) :
	return int.from_bytes(val, byteorder='little')


def load_creaditals() :
	path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '.creditals')
	with open(path, 'rb') as file :
		length = conv_int(file.read(32))
		data = file.read(length)
		length = conv_int(file.read(32))
		iv = file.read(length)
		padd = conv_int(file.read())

	return { 'data' : data, 'iv' : iv, 'padd' : padd }


def save_creditals(data) :
	with open('.creditals', 'wb') as file :
		file.write(conv_bytes(len(data['data'])))
		file.write(data['data'])
		file.write(conv_bytes(len(data['iv'])))
		file.write(data['iv'])
		file.write(conv_bytes(data['padd']))


def add_padd(pt) :
	pt = bytearray(pt, 'utf-8')
	padding = 16 - (len(pt) % 16)
	pt += os.urandom(padding)
	return pt, padding


def remove_padd(data, padding) :
	return (data[:-padding]).decode('utf-8')


def get_data(iv, data, padding) :
	key = getpass(col.arrow + " key: ")
	while len(key) < 32 :
		key = key + key
	key = key[:32]
	ds = AES.new(key, AES.MODE_CBC, iv)
	data = remove_padd(ds.decrypt(data), padding)
	return data


def login(creditals) :
	iv, data, padding = creditals['iv'], creditals['data'], creditals['padd']
	try :
		data = get_data(iv, data, padding)
	except :
		print(col.minus, 'key not valid')
		return None, None

	data = json.loads(data)
	name, passwd, server, loc = data['name'], data['passwd'], data['server'], data['loc']

	try :
		ftps = ftputil.FTPHost(server, name, passwd)
	except :
		print(col.minus, 'cannot connect, check also the settings of the server')
		return None, None

	return ftps, loc


def get_creditals() :
	iv = os.urandom(16)
	server = input("{} server: ".format(col.arrow))
	name = input("{} name: ".format(col.arrow))
	passwd = getpass("{} server passwd: ".format(col.arrow))
	key = getpass("{} my local encryption key: ".format(col.arrow))
	loc = input("{} location: ".format(col.arrow))

	loc = os.path.realpath(os.path.expanduser(loc))

	if not os.path.exists(loc):
		print(col.minus, loc, 'does not exist.')
		agree = input("{} do you want to create it? [y/n]: ".format(col.arrow))
		if agree in ['y', 'Y', 'yes', "Yes", 'agree', 'a', 'A'] :
			create_path(os.path.join(loc, 'here'))
		else :
			return None, None
	else :
		print(col.plus, 'Setting path to ', loc)

	pt = json.dumps({ 'name' : name, 'passwd' : passwd, 'server' : server, 'loc' : loc })

	pt, padding = add_padd(pt)
	while len(key) < 32 :
		key = key + key
	key = key[:32]

	es = AES.new(key, AES.MODE_CBC, iv)
	data = es.encrypt(bytes(pt))

	creditals = { 'data' : data, 'iv' : iv, 'padd' : padding }
	try :
		save_creditals(creditals)
		print(col.plus, 'creditals saved locally - you\'ll be prompted to enter the key again for login.')
	except :
		print(col.minus, 'could not save the creditals on the disk.')
	return creditals


def connect():
	try:
		creditals = load_creaditals()
	except :
		print(col.minus, "login unknown - please type in your creditals:")
		creditals = get_creditals()
	try :
		ftps, loc = login(creditals)
	except:
		ftps, loc = None, None
	return ftps, loc

