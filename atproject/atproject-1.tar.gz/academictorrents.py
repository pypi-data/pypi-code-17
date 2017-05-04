import atproject.Download.main as dl

def get(str):
		path = str
		obj = dl.CustomLibrary()
		obj.torrent_path = path
		path_to_file = obj.get()
		
		




