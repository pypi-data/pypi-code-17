'''	Extract cached images of Microsoft Spotlight Project (For Windows X OS only).
	Resolution of each image is 1920 x 1080 
	Methods:
		storeimages  : store images in directory given as argument.
		getimages : return a list of PIL.Image.Image objects.
'''

def storeimages(destination_path = "C:\\spotlight") :
	'''	Usage : storeimages( destination_path ) -> None
		Store the cached Microsoft Spotlight Images in the computer to the 
		destination specified.
		Params -
			destination_path : 
				Path of the folder where Images will be saved.
				default value : "C:\\spotlight"
				If the provided path does not represent an existing 
				directory,then a new directory will be created with same 
				path, If possible.
		Errors:
			ValueError : 
			If the given path represents an already existing file and not 
			a directory.				
	'''
	import os,hashlib
	from PIL import Image
	folder = os.path.join(os.getenv("userprofile"),"AppData\\Local\\Packages\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\\Assets")
	name = ""
	if not os.path.exists(destination_path):
		os.mkdir(destination_path)
	if not os.path.isdir(destination_path):
		raise ValueError("Given path cannot be used as a directory!")
	files = os.listdir(destination_path)

	for file in os.listdir(folder):
		try : 
			img = Image.open(os.path.join(folder,file))
			if img.height == 1080 and img.width == 1920 :
				f = open(os.path.join(folder,file),'rb')
				name =  hashlib.md5(f.read()).hexdigest()+'.jpeg'
				f.close()
				if name not in files:
					img.save(os.path.join(destination_path,name))
					files.append(name)
			img.close()
		except OSError : 
			continue
	
def getimages():
	'''	Usage : getimages(None) -> list(PIL.Image)
		return a list of PIL.Image.Image objects where each object is
		a Microsoft Spotlight JPEG image of resolution 1920x1080.		
	'''
	import os
	from PIL import Image
	folder = os.path.join(os.getenv("userprofile"),"AppData\\Local\\Packages\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\\Assets")
	images =  []
	for file in os.listdir(folder):
		img = Image.open(os.path.join(folder,file))
		if img.height == 1080 and img.width == 1920 :
			images.append(img)
		img.close()
	return images