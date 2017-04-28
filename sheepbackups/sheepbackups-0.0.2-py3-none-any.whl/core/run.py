import argparse
import sys, os
import requests
from tabulate import tabulate
import yaml
import time
import shutil

VERSION = (0,0,2)

def copy(source, dest, filename=None):
    """
    types:
        copy(/srv/sqlite.db, /tmp/db/)
    """
    if filename is None:
        filename = os.path.basename(source)
    
    # Log it too
    shutil.copy2(source, dest)

def api_request(endpoint, post=None):
    url = CONFIG['api_url'] + endpoint
    
    headers = {
        'X-Sheepkey': CONFIG['api_key'],
    }
    
    if post is None:
        return requests.get(url, headers=headers)
    else:
        return requests.post(url, post, headers=headers)

def entries_lookup(prefix=None, match=None):
    endpoint = 'entries/'
    
    if prefix is None:
        prefix = 'all'
    endpoint += prefix
        
    if match is not None:
        endpoint += '/' + match
    
    r = api_request(endpoint)
    j = r.json()
    table = []
    num = 1
    for result in j['entries']:
        if result['meta']:
            meta = ', '.join([ '{0}: {1}'.format(k,v) for k, v in result['meta'].items() ])
        else:
            meta = ''
            
        table.append([num, result['id'], result['created_servertime'], meta])
        num += 1
    print(tabulate(table, headers=['', 'uuid', 'date', 'meta']))
    

def run_backup():
    # Check config
    # Create temp dir
    temp_dir = os.path.join('/tmp', 'sheepbackups', 'backup{0}'.format(time.time()))
    try:
        os.makedirs(temp_dir)
    except:
        raise
    
    for prefix, opts in CONFIG['backups'].items():
        # Start with db
        if 'db' in opts:
            backup_path = [temp_dir, prefix, 'db']
            if 'mysql' in opts['db']:
                # Run mysqldump
                export_db_mysql = 'mysqldump {0} 2>&1 > .sheeplog.export_db_mysql.log'.format(opts['db']['mysql']['opts'])
            
            if 'sqlite' in opts['db']:
                # Collect it
                locations = opts['db']['sqlite']['locations']
                # Check location exists
                
                # Move location 
                for location in locations:
                    copy(location, os.path.join(*backup_path + [os.path.basename(location)]))
                
        # Collect directories
        if 'collect' in opts:
            backup_path = [temp_dir, prefix, 'files']
            if 'dirs' in opts['collect']:
                for dest_dir, src_dir in opts['collect']['dirs'].items():
                    print(dest_dir, src_dir)

def run_restore(id=None):
    pass

def loader():
            
    parser = argparse.ArgumentParser(description='Sheep Backups. For more information on the Python cli, visit https://docs.sheepbackups.com/python', prog='sheep')
    parser.add_argument('action', nargs='?', help='What action to perform (backup, restore, list)')
    parser.add_argument('match', nargs='?', help='ID to match')
    parser.add_argument('--prefix', help='Which prefix to use when searching')
    parser.add_argument('--test', action='store_true', help='Do a test backup/restore, but don\'t actually run')
    parser.add_argument('--config', help='Path to config file (default ~/.sheepbackups/config.yaml)')
    parser.add_argument('-V', '--version', action='store_true', help='Return this version')
    
    opts = parser.parse_args()
    if opts.config is None:
        opts.config = os.path.join(os.path.expanduser("~"), ".sheepbackups", "config.yaml")
        
    with open(opts.config, 'r') as stream:
        try:
            global CONFIG
            CONFIG = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            
    try:
        CONFIG
    except NameError:
        raise RuntimeError("No config loaded. Either the path was not found, or the yaml config could not be parsed.")
        sys.exit(2)
    
    if opts.action == 'backup':
        run_backup()
    elif opts.action == 'restore':
        pass
    elif opts.action == 'list':
        entries_lookup(opts.prefix, opts.match)
    elif opts.action == 'config':
        print(CONFIG)
    elif opts.version:
        print('{0}.{1}.{2}'.format(*VERSION))
    else:
        #print('Unknown action: {0}. Possible actions: backup, restore, list'.format(opts.action))
        print(parser.print_help())
   
if __name__ == "__main__":
    loader()
    