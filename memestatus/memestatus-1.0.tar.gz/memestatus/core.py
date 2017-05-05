# Setup
import requests

statusendpoint = 'http://status.memework.org/api'

# Core magic
# Uses requests to get API data,
apiget = requests.get(statusendpoint)
# then uses the JSON function to get JSON.
apires = apiget.json()
