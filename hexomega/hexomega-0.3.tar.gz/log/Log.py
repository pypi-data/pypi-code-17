from datetime import datetime

from users.models import MemberUser, LeaderUser, AdminUser


# To do:
#   1.  test the log function, once others are done with the module.
#   2.  add a function to parse each line of a given log file and
#       render them into a HTML structure for use in a view.

def log(level, user, content, **kwargs):
    """
    Log function.
    Call from any function or context with the required parameters to
    write to the appropriate log file. Can use threading for pseudo
    non-blocking IO but due to some constraints have reasoned otherwise.

    :param level: either: INFO, WARNING or SUCCESS
    :param user: user who called a function with log.
    :param content: the path to the log
    :param kwargs: random kwargs to add to the log message.
    Will add implementation only if needed.
    :return: None
    """
    # the content attribute of the project has the entire
    # path from BASE_DIR(mentioned in settings.py).
    # l = MemberUser.objects.get(username__contains=username)
    # print(l.username)
    # INFO = 'INFO'
    # WARNING = 'WARNING'
    # SUCCESS = 'SUCCESS'
    access_level = None
    if user.is_admin:
        access_level = 'ADMIN'
    elif user.is_leader:
        access_level = 'LEADER'
    else:
        access_level = 'MEMBER'

    data = datetime.now().strftime('%A, %d. %B %Y %I:%M%p') + ' '
    # data += content

    logfile = user.project.activitylog.content

    if logfile is '':
        raise ValueError('Empty path to log file.')
    else:
        f = open(logfile, 'a')
        print('[{}] [{}] [{}] [{}] [{}] [{}]'.format(level, user.get_full_name(), access_level, user.project.name, data,
                                                     content),
              file=f)
        f.flush()
        f.close()
