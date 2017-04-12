from stepist.flow import step

from django.db.models import Model


@step(None)
def step3(result):
    print("CC")
    return dict(result="step3")


@step(step3)
def step2(hello, world):
    print("BB")
    return dict(result="%s %s" % (hello, world))


@step(step2)
def step1(hello, world):
    print("AA")
    return dict(hello=hello.upper(),
                world=world.upper())



step1.config(last_step=step2)\
     .execute(hello='hello',
              world='world')
