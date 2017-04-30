import requests
import tarfile

import os

#download and extract tarball from github
def init(path, url):
    if os.path.exists(path):
        print(f"Error: {path} already exists")
        exit()
    print("Download", url)
    r = requests.get(url)

    with open(path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=32):
            f.write(chunk)

    t = tarfile.open(path, 'r')
    os.remove(path)
    t.extractall(path.parent)
    os.rename(t.getmembers()[0].name, path)
