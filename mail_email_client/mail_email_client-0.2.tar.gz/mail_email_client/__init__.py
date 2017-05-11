import getpass, os

__author__  = "hmnhGeek"
__git__     = "https://www.github.com/hmnhGeek/mail_email_client/"
__version__ = 0.2

def console():
	try:
		os.system('sudo pip install mail_email --upgrade')
		print
		print
		from mail_email import *

		def get_proper_img_addr(data):
			
			recv = ''
			brackets = []
			for i in data:

				if('[' in i and ']' in i):
					return i
				else:
					if(brackets <> ['[', ']']):
						if '[' in i:
							brackets.append('[')
							recv += i
						else:
							if '[' in brackets and ']' not in brackets:
								if ']' in i:
									brackets.append(']')
									recv += (' '+i)
									return recv
								else:
									recv += (' '+i)


		def menu():
			print 
			print '========================================================================='
			print
			print "Welcome to python email client."
			print '-------------------------------'
			print
			print
			print "Type send <sender> <smtp server> <port> [recievers] to send an email."
			print "Type mms <sender> <smtp server> <port> <reciever> [<image-address>] to send an email."
			print "Type exit to exit."
			print
			print '=========================================================================='
			print
			print


		ch = 1
		menu()
		while(ch):
			cmd = raw_input('>>> ')

			if(cmd[0:4] == 'send'):
				write_mail()
				
				send_now = raw_input("Send? (y/n) ").upper()

				if(send_now == 'Y'):
					data = cmd.split(' ')
					sender = data[1]
					recievers = make_recievers(data)
					
					server = data[2]
					
					port = data[3]
				
					exec 'recievers = '+recievers
					password = getpass.getpass("password> ")
					try:
						f = open("message.txt", "r")
						message = f.read()
						f.close()

						send(sender, recievers, message, server, port, password)
					except:
						pass
			elif(cmd[0:3] == 'mms'):
				write_mail()

				send_now = raw_input("Send? (y/n) ").upper()

				if(send_now == 'Y'):
					data = cmd.split(' ')

					sender = data[1]
					server = data[2]
					port = data[3]
					recv = data[4]
					image_addr = get_proper_img_addr(data)

					exec 'image_addr = '+image_addr
					image_addrs = image_addr[0]
					
					
					subj = raw_input("subject> ")
					password = getpass.getpass("password> ")

					try:
						f = open("message.txt", "r")
						msg = f.read()
						f.close()
					
						send_MMS(sender, recv, msg, image_addrs, subj, password, port, server)
						print "Message Sent!!"
					except:
						pass

			elif(cmd == 'exit'):
				ch = 0
			elif(cmd == 'menu'):
				menu()
			else:
				print "Invalid!!"
	except ImportError:
		
		print "Please install mail_email module to use this."

		q = raw_input("Should I install it? (y/n) ").upper()
		if q == 'Y':
			os.system('sudo pip install mail_email')
			console()
		else:
			pass

console()
