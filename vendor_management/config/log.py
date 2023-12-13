import os


LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


def get_handlers():

    handlers = {}
    handlers['logfile'] = {
        'level': 'DEBUG',
        'class': 'logging.handlers.RotatingFileHandler',
        'filename': os.path.abspath(os.path.join(LOG_DIR, "vendor_management.log")),
        'maxBytes': 5 * 1024 * 1024,
        'backupCount': 10,
        'formatter': 'standard',
    }
    handlers['console'] = {
        'level': 'DEBUG',
        'class': 'logging.StreamHandler',
        'formatter': 'standard'
    }

    return handlers


handlers = get_handlers()
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': "[%(process)d %(thread)d %(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': handlers,
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'WARN',
            'propagate': False,
        },
        'django.security.DisallowedHost': {  # and this
            'handlers': [],
            'propagate': False,
        },
        'main': {
            'handlers': list(handlers.keys()),
            'level': 'DEBUG',
        },
        'apps': {
            'handlers': list(handlers.keys()),
            'level': 'DEBUG',
        }
    }
}
