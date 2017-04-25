from appconf import AppConf

__version__ = '0.2.4'


class GoogleDriveAPIConf(AppConf):

    class Meta:
        prefix = 'GOOGLE_DRIVE_API'
        required = ['JSON_KEY_FILE']

    USER_EMAIL = None
    AUTO_CONVERT_MIMETYPES = []
    NUM_RETRIES = 3
    CACHE_TTL = 60 * 60  # Cache data from Google Drive API for 1 hour.
    CACHE_DEBUG = False
