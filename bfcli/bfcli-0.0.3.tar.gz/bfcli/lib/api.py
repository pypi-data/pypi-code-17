import bitfusion

from bfcli import config

API = bitfusion.BFApi(host=config.conf.get('host'), cookies=config.conf.get('cookies'))

# Try to set the user in config
try:
  config.user = API.User.get(config.conf['uid'])
except:
  pass
