


from stepist.flow import step


@step(None)
def step3(a):
    return {'c': 'd', 'a': a}


@step(None)
def step2():
    return {'a': 'b'}


@step(step3)
@step(step2)
def step1(a):
    print(a)
    return {}



print(step1(data={'data':{'a': 'b'}}))
