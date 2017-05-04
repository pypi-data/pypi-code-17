import subprocess
import requests

class IPFSDag():
  def __init__(self, gateway = "http://ipfs.hobbs.cz/"):
    self.files = []
    if not gateway.endswith("/"):
      gateway += "/"
    self.gateway = gateway

  def add(self,file):
    hash = subprocess.check_output(["ipfs","add","-Q",file]).decode("utf-8").strip()
    print("Added: "+hash)
    self.push_object_to_gateway(hash)
    print("Pushed %s to gateway."%hash)
    self.files.append(file)

  def push_object_to_gateway(self,hash):
    requests.get(self.gateway + "api/v0/refs?arg=" + hash + "&r=true")

  def push_to_gateway(self):
    self.push_object_to_gateway(self.get_hash())

  def get_hash(self):
    hash = subprocess.check_output(["ipfs","add","-wQ"]+self.files).decode("utf-8").strip()
    return hash

  def get_url(self):
    return self.gateway + "ipfs/" + self.get_hash() + "/story.html"
