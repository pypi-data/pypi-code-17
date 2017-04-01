from stepist.flow import step, run, setup, just_do_it
from stepist.flow import workers
from celery import Celery
from django.db.models import Model


from rq import Queue, Worker
from redis import Redis

redis_conn = Redis()
q = Queue(connection=redis_conn)


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

workers.setup_worker_engine(workers.rq_driver)
setup(rq_queue=q)

if __name__ == "__main__":
    just_do_it(workers_count=3, queues=q)

    print(step1.config(last_step=step3)
               .execute(hello='hello',world='world'))
