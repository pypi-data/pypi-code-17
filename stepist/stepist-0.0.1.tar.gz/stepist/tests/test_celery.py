from stepist.flow import step, run, setup, just_do_it
from stepist.flow import workers
from celery import Celery
from django.db.models import Model


app = Celery("step_flow",
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0',)


@step(None, as_worker=True, wait_result=True)
def step3(result):
    return dict(result=result[:2])


@step(step3, as_worker=True, wait_result=True)
def step2(hello, world):
    return dict(result="%s %s" % (hello, world))


@step(step2)
def step1(hello, world):

    return dict(hello=hello.upper(),
                world=world.upper())

workers.setup_worker_engine(workers.celery_driver)
setup(celery_app=app)
print("asd")
print(app.tasks.keys())
if __name__ == "__main__":
    just_do_it(1)
    print(step1(hello='hello',
                world='world'))
