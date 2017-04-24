import sys
import vmtools
vm_root_path = vmtools.vm_root_grabber()
sys.path.append(vm_root_path)
import pkgutil
local_settings_present = pkgutil.find_loader('local_settings')
if local_settings_present:
        from local_settings import *
# check if GMAIL_CONFIG_DICT is defined
error_record_dict = { 'GMAIL_USER': False, 'GMAIL_PASS': False, 'GMAIL_RECIPIENTS': False, 'GMAIL_CONFIG_DICT': False }
try:
    GMAIL_CONFIG_DICT
except NameError:
    print("""dictionary GMAIL_CONFIG_DICT not defined, setting all keys to None. If you store in local_settings.py at the root of the python virtual machine the following (you can avoid specifying the arguments: username, password, recipients):
    import os
    # gmail settings
    GMAIL_CONFIG_DICT = {
    GMAIL_USER='you@yourdomain.com'
    GMAIL_PASS='changeme'
    GMAIL_RECIPIENTS=['friend1@theirdomain.com', 'friend2@theirdoman.com']
    }""")
    GMAIL_CONFIG_DICT = { 'GMAIL_USER': None, 'GMAIL_PASS': None, 'GMAIL_RECIPIENTS': None }
    error_record_dict['gmail_config_dict'] = True

try:
    GMAIL_CONFIG_DICT['GMAIL_USER']
except KeyError:
    GMAIL_CONFIG_DICT['GMAIL_USER'] = None
    error_record_dict['GMAIL_USER'] = True

try:
    GMAIL_CONFIG_DICT['GMAIL_PASS']
except KeyError:
    GMAIL_CONFIG_DICT['GMAIL_PASS'] = None
    error_record_dict['GMAIL_PASS'] = True

try:
    GMAIL_CONFIG_DICT['GMAIL_RECIPIENTS']
except KeyError:
    GMAIL_CONFIG_DICT['GMAIL_RECIPIENTS'] = None
    error_record_dict['GMAIL_RECIPIENTS'] = True

if not error_record_dict['GMAIL_CONFIG_DICT']:
    for error_item in error_record_dict:
        if error_record_dict[error_item]:
           warning_message = 'Variable GMAIL_CONFIG_DICT[{}] not defined, setting to None'.format(error_item)
           print(warning_message)


__all__ = ['senderror', 'senderror_attach']

