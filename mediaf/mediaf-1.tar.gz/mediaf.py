import os
import getpass,string,random

def version():
	print "_Version_1"
def about():
	print"""
	Usage --------------------------------------
	First install sudo apt-get install ffmpeg
	--------------------------------------------
	>>import mediaf
	
	>>from mediaf import*
	
	>>mediaf.version()
	_Version_1
	
	>>mediaf.play("input.mp4")

	Window size---------------------------------
	
	mediaf.play("-x int -y int input.mp4") # x-width y-height
	
	>>mediaf.play("-x 400 -y 400 input.mp4")



	-------Convert Video------------------------
	For exam:

	>>i="/home/users/Desktop/string.mp4"
	>>mediaf.convert_avi(i)

	or

	>>mediaf.convert_avi("/home/users/Desktop/string.mp4")

	-------------Video format supported-------------------
	Keyword for file format
	convert_3gp
	convert_avi
	convert_mp4
	convert_vob
	convert_wmv
	convert_mpeg
	convert_dv
	convert_mov
	convert_flv
	convert_webm


	----- get audio from media file------------

	>>mediaf.getaudio("sting.mpeg")




	"""
def play(infile):
	os.system("ffplay {}".format(infile))
def convert_avi(infile):
	try:
		i=getpass.getuser()
		v=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
		outputname=random.sample(v,4)
		creat="".join(outputname)
		os.system("ffmpeg -i {} -acodec copy -vcodec copy '/home/{}/Videos/{}.avi'".format(infile,i,str(creat)))
		print "file created in /home/{}/Videos/{}.avi".format(i,creat)
	except IOError:
		print"[-] file format not supported"
	except:
		print"[-] Sorry some problem"
def convert_mp4(infile):
	try:
		i=getpass.getuser()
		v=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
		outputname=random.sample(v,5)
		creat="".join(outputname)
		os.system("ffmpeg -i {}  -acodec aac -strict experimental -ac 2 -ab 160k -vcodec libx264 -preset slow -f mp4 -crf 22 '/home/{}/Videos/{}.mp4'".format(infile,i,str(creat)))
		print "file created in /home/{}/Videos/{}.avi".format(i,creat)
	except IOError:
		print"[-] file format not supported"
	except:
		print"[-] Sorry some problem"
def convert_vob(infile):
	try:
		i=getpass.getuser()
		v=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
		outputname=random.sample(v,5)
		creat="".join(outputname)
		os.system("ffmpeg -i {}  -target ntsc-dvd -preset ultrafast '/home/{}/Videos/{}.vob'".format(infile,i,str(creat)))
		print "file created in /home/{}/Videos/{}.avi".format(i,creat)
	except IOError:
		print"[-] file format not supported"
	except:
		print"[-] Sorry some problem"


def convert_flv(infile):
	try:
		i=getpass.getuser()
		v=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
		outputname=random.sample(v,5)
		creat="".join(outputname)
		os.system("ffmpeg -i {} -vcodec flv -b:v 512k -s 480x360 -r 30 -acodec libmp3lame -ar 44100 -f flv '/home/{}/Videos/{}.flv'".format(infile,i,str(creat)))
		print "file created in /home/{}/Videos/{}.avi".format(i,creat)
	except IOError:
		print"[-] file format not supported"
	except:
		print"[-] Sorry some problem"
def convert_dv(infile):
	try:
		i=getpass.getuser()
		v=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
		outputname=random.sample(v,5)
		creat="".join(outputname)
		os.system("ffmpeg -i {} -s pal -r pal -aspect 4:3 -ar 48000 -ac 2 '/home/{}/Videos/{}.dv'".format(infile,i,str(creat)))
		print "file created in /home/{}/Videos/{}.avi".format(i,creat)
	except IOError:
		print"[-] file format not supported"
	except:
		print"[-] Sorry some problem"
def convert_mkv(infile):
	try:
		i=getpass.getuser()
		v=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
		outputname=random.sample(v,5)
		creat="".join(outputname)
		os.system("ffmpeg -i {} -f matroska -vcodec libx264 -acodec libvorbis '/home/{}/Videos/{}.mkv'".format(infile,i,str(creat)))
		print "file created in /home/{}/Videos/{}.avi".format(i,creat)
	except IOError:
		print"[-] file format not supported"
	except:
		print"[-] Sorry some problem"
def convert_mpeg(infile):
	try:
		i=getpass.getuser()
		v=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
		outputname=random.sample(v,5)
		creat="".join(outputname)
		os.system("ffmpeg -i {} -target ntsc-dvd '/home/{}/Videos/{}.mpeg'".format(infile,i,str(creat)))
		print "file created in /home/{}/Videos/{}.avi".format(i,creat)
	except IOError:
		print"[-] file format not supported"
	except:
		print"[-] Sorry some problem"
def convert_mov(infile):
	try:
		i=getpass.getuser()
		v=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
		outputname=random.sample(v,5)
		creat="".join(outputname)
		os.system("ffmpeg -i {} -acodec libmp3lame -ab 192 '/home/{}/Videos/{}.mov'".format(infile,i,str(creat)))
		print "file created in /home/{}/Videos/{}.avi".format(i,creat)
	except IOError:
		print"[-] file format not supported"
	except:
		print"[-] Sorry some problem"
def convert_webm(infile):
	try:
		i=getpass.getuser()
		v=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
		outputname=random.sample(v,5)
		creat="".join(outputname)
		os.system("ffmpeg -i {} -cpu-used 4 -threads 8 '/home/{}/Videos/{}.webm'".format(infile,i,str(creat)))
		print "file created in /home/{}/Videos/{}.avi".format(i,creat)
	except IOError:
		print"[-] file format not supported"
	except:
		print"[-] Sorry some problem"
def convert_wmv(infile):
	try:
		i=getpass.getuser()
		v=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
		outputname=random.sample(v,5)
		creat="".join(outputname)
		os.system("ffmpeg -i {} -b:v 2M -vcodec msmpeg4 -acodec wmav2 '/home/{}/Videos/{}.wmv'".format(infile,i,str(creat)))
		print "file created in /home/{}/Videos/{}.avi".format(i,creat)
	except IOError:
		print"[-] file format not supported"
	except:
		print"[-] Sorry some problem"
def convert_3gp(infile):
	try:
		i=getpass.getuser()
		v=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
		outputname=random.sample(v,5)
		creat="".join(outputname)
		os.system("ffmpeg -i {} -f 3gp -vcodec h263 -acodec amr_nb '/home/{}/Videos/{}.3gp'".format(infile,i,str(creat)))
		print "file created in /home/{}/Videos/{}.avi".format(i,creat)
	except IOError:
		print"[-] file format not supported"
	except:
		print"[-] Sorry some problem"
def getaudio(infile):
	try:
		i=getpass.getuser()
		v=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
		outputname=random.sample(v,5)
		creat="".join(outputname)
		os.system("ffmpeg -i {} -f mp3 '/home/{}/Videos/{}.mp3'".format(infile,i,str(creat)))
		print "file created in /home/{}/Videos/{}.avi".format(i,creat)
	except IOError:
		print"[-] file format not supported"
	except:
		print"[-] Sorry some problem"


		




		