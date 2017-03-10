# from ftplib import FTP
import ftputil
from Crypto.Cipher import AES
import Crypto.Random.OSRNG.posix as defiv
import json
from getpass import getpass
import os
import ftp


def conv_bytes(val) :
	return val.to_bytes(32, byteorder='little', signed=False)


def conv_int(val) :
	return int.from_bytes(val, byteorder='little')


def load_creaditals() :
	with open('.creditals', 'rb') as file :
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
	key = getpass(ftp.col.arrow + " key: ")
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
		print(ftp.col.minus, 'key not valid')
		return None

	data = json.loads(data)
	name, passwd, server, loc = data['name'], data['passwd'], data['server'], data['loc']

	try :
		ftps = ftputil.FTPHost(server, name, passwd)
	except :
		print(ftp.col.minus, 'cannot connect, check settings')
		return None

	return ftps, loc


def get_creditals() :
	iv = os.urandom(16)
	server = input("{} server: ".format(ftp.col.arrow))
	name = input("{} name: ".format(ftp.col.arrow))
	passwd = getpass("{} passwd: ".format(ftp.col.arrow))
	key = getpass("{} key: ".format(ftp.col.arrow))
	loc = input("{} location: ".format(ftp.col.arrow))

	pt = json.dumps({ 'name' : name, 'passwd' : passwd, 'server' : server, 'loc' : loc })

	pt, padding = add_padd(pt)
	while len(key) < 32 :
		key = key + key
	key = key[:32]

	es = AES.new(key, AES.MODE_CBC, iv)
	data = es.encrypt(bytes(pt))

	creditals = { 'data' : data, 'iv' : iv, 'padd' : padding }
	save_creditals(creditals)
	return creditals


def connect():
	try:
		creditals = load_creaditals()
	except :
		print(ftp.col.minus, "login unknown - please type in your creditals:")
		creditals = get_creditals()
	try :
		ftps, loc = login(creditals)
	except:
		ftps, loc = None, None
	return ftps, loc