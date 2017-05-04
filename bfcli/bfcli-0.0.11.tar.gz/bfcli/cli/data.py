import sys

import click
import terminaltables

from bfcli.lib.api import API, me

def print_data_object(data):
  pass


def print_data_list(data_list):
  headings = ['ID', 'Name', 'Created']
  table_data = [headings]

  for _d in data_list:
    table_data.append([_d.get('id'), _d.get('name'), _d.get('createdAt')])

  table = terminaltables.SingleTable(table_data, title='Data')
  click.echo(table.table)


@click.group()
def data():
  pass


@data.command()
@click.argument('path')
def upload(path):
  user = me()
  click.echo('Uploading data...')

  API.data.upload(path,
                  '/',
                  group_id=user.data['user']['defaultGroup'],
                  account_id=user.data['account']['id'])
  click.echo('Upload complete!')

@data.command()
def list():
  data_meta = API.data.list()
  print_data_list(data_meta)

# The DATA data data structure
# {
#   "_id": "59023ebde80de5003ec11349",
#   "deletedAt": null,
#   "name": "asdf",
#   "createdBy": "59022ab6c9451b00118b8b43",
#   "accountId": "59022ab6c9451b00118b8b45",
#   "groupId": "59022ab6c9451b00118b8b44",
#   "__v": 0,
#   "createdAt": "2017-04-27T18:55:57.977Z",
#   "updatedAt": "2017-04-27T18:55:57.995Z",
#   "deleted": false,
#   "path": {
#     "local": "asdf",
#     "remote": "59022ab6c9451b00118b8b45/59022ab6c9451b00118b8b44/data"
#   },
#   "status": "uploading",
#   "id": "59023ebde80de5003ec11349"
# }
