from django.conf import settings as global_settings

DISABLE_DJANGO_CDC = getattr(global_settings, 'DISABLE_DJANGO_CDC', False)
AWS_ACCESS_KEY = getattr(global_settings, 'AWS_ACCESS_KEY', "")
AWS_SECRET_ACCESS_KEY = getattr(global_settings, 'AWS_SECRET_ACCESS_KEY', "")
AWS_REGION_NAME = getattr(global_settings, 'AWS_REGION_NAME', "us-east-1")
LAMBDA_FUNCTION_PREFIX = getattr(global_settings, 'LAMBDA_FUNCTION_PREFIX', "djangoCDC")
SERVERLESS_DIR = getattr(global_settings, 'SERVERLESS_DIR', "")
SERVERLESS_STAGE = getattr(global_settings, "SERVERLESS_STAGE", "dev")
SERVELESS_CONFIG = getattr(global_settings, "SERVELESS_CONFIG", "djangoCDC")

# logger
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django_cdc': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
    },
}
