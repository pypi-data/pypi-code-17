
# Tiros Service configuration
BACKEND = "souffle-compiler"
HOST = 'localhost:9000'
SNAPSHOT_SESSIONS = None
SSL = False
THROTTLE = None
TRANSFORMS = ['magic-sets']
UIC = True  # UNSAFE_IGNORE_CLASSIC
UR = None  # USER_RELATIONS


# Queries to be cached when a snapshot is uploaded
TIROS_QUERIES = {'ok-instance': 'list: instance-ok(I).',
                 'ssh-instance': 'list: instance-can-ssh-to-internet(I).'}
