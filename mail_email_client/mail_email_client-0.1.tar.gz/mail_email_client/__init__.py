def console():
	try:
		from mail_email import *

		def menu():
			print 
			print '========================================================================='
			print
			print "Welcome to python email client."
			print '-------------------------------'
			print
			print
			print "Type send <sender> <smtp server> <port> [recievers] to send an email."
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
					try:
						f = open("message.txt", "r")
						message = f.read()
						f.close()

						send(sender, recievers, message, server, port)
					except:
						pass
			elif(cmd == 'exit'):
				ch = 0
			elif(cmd == 'menu'):
				menu()
			else:
				print "Invalid!!"
	except ImportError:
		import os
		print "Please install mail_email module to use this."

		q = raw_input("Should I install it? (y/n) ").upper()
		if q == 'Y':
			os.system('sudo pip install mail_email')
			console()
		else:
			pass

console()
