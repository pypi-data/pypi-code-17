from stepist.flow import step, factory_step


@step(None)
def step2(word):
    return word


@factory_step(step2)
def step1(hello, world):
    return [{'word': hello},
            {'word': world}]
