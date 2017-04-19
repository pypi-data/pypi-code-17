from binascii import *
from struct import *
import json

def decode(package):
	outData={'header':"",'payload':[]}
	p=package.split("\r\n\r\n");
	header=p[0];
	payload=p[1];
	#print("len:"+str(int(len(package)/1024)));
	print("header:"+header)
	outData['header']=json.loads(header);
	payload=b2a_hex(payload);
	payloads=payload.split('0d0a');
	for b in payloads:
		record={};
#		print("    "+b+"\r");
		try:
#			print("begin:"+b[0:2]+" len:"+str(int(b[2:4],16))+" type:"+b[4:6]+" mac:"+b[6:18]+" rssi:"+str(int(b[18:20],16))+" rawdata:"+b[20:]);
#			rawdata=b[20:];
			record['type']=b[4:6]
			record['mac']=b[6:18]
			record['rssi']=str(int(b[18:20],16));
			record['rawdata']=a2b_hex(b[20:]);
#			print(len(rawdata));
#			print("rawdata:"+b[20:]);
#			print(a2b_hex(rawdata));
		except:
			pass;
		outData['payload'].append(record);
	return outData;
