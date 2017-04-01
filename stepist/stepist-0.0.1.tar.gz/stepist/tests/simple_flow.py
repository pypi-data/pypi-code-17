from stepist.flow import step

from django.db.models import Model


@step(None)
def step2(hello, world):
    return dict(result="%s %s" % (hello, world))


@step(step2)
def step1(hello, world):

    return dict(hello=hello.upper(),
                world=world.upper())
