import os
__version__ = '0.1.6.1'
__history_file_path__ = os.path.join('~', '.vss', 'history')
__config_file_path__ = os.path.join('~', '.vss', 'config.json')
__env_vars__ = {'user': 'VSS_API_USER',
                'pass': 'VSS_API_USER_PASS',
                'token': 'VSS_API_TOKEN',
                'endpoint': 'VSS_API_ENDPOINT',
                'config': 'VSS_CONFIG_FILE',
                'output': 'VSS_DEFAULT_OUTPUT'}
