from celery import Celery
from celery.schedules import crontab

from .utils import tasks_email_schedule, project_deadline_schedule

app = Celery()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(5.0, test.s('hello'), name='add every 10')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # sender.add_periodic_task(
    #     crontab(hour=13, minute=57),
    #     test.s('I want to hold your hand'),
    # )

    # sender.add_periodic_task(
    #     crontab(hour=7, minute=30),
    #     test.s(),
    # )


@app.task
def test(arg):
    f = open('help.txt', 'a')
    print(arg, file=f)
    f.close()
