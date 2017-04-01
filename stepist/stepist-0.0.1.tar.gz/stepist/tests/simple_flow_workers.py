from stepist.flow import step, run, setup, just_do_it


@step(None, as_worker=True, wait_result=True)
def step3(a):
    return dict(c='d',
                a=a)


@step(step3, as_worker=True, wait_result=True)
def step2():
    return {'a': 'b'}


@step(step2)
def step1():
    print("ASD")
    return {}


setup()
just_do_it(5, step2, step3, _warning=False)


print(step1.config())

