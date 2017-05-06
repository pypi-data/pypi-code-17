from storer import Storer
import json
import os

class JsonStorer(Storer):
  """
  Storer of podcasts in JSON form
  """

  def __init__(self, directory):
    """
    Constructor
    """
    self.directory = directory
    # Ensure the directory exists
    if not os.path.exists('./{}'.format(self.directory)):
      os.makedirs('./{}'.format(self.directory))

  def store(self, result_dict):
    """
    See Storer#store(result_dict)
    """
    s_id = result_dict['series']['id']
    with open('./{}/{}.json'.format(self.directory, str(s_id)), 'wb') as outfile:
      json.dump(result_dict, outfile)
