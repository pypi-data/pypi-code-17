from hooky import Hook, List, Dict


class Count(Hook):
    def __init__(self):
        self.before_add_count = 0
        self.after_add_count = 0

        self.before_del_count = 0
        self.after_del_count = 0

    def _before_add(self, key, item):
        self.before_add_count += 1

    def _after_add(self, key, item):
        self.after_add_count += 1

    def _before_del(self, key, item):
        self.before_del_count += 1

    def _after_del(self, key, item):
        self.after_del_count += 1


class CountList(Count, List):
    def __init__(self, *args, **kwargs):
        Count.__init__(self)
        List.__init__(self, *args, **kwargs)


class CountDict(Count, Dict):
    def __init__(self, *args, **kwargs):
        Count.__init__(self)
        Dict.__init__(self, *args, **kwargs)


def test_list_slice():
    from time import time
    from random import randrange as r

    start_time = time()

    times = 0

    while True:
        times += 1

        l = ['s'] * r(0, 100)
        ol = ['o'] * r(0, 100)

        s = slice(r(-300, 300), r(-300, 300), r(-300, 300))

        l1_e = None
        l1 = list(l)
        try:
            l1[s] = ol
        except Exception as e:
            l1_e = e
            pass

        l2_e = None
        l2 = List(l)
        try:
            l2[s] = ol
        except Exception as e:
            l2_e = e
            pass

        if l1_e or l2_e:
            try:
                assert str(l1_e) == str(l2_e)
            except AssertionError:
                print()
                print('Error:')
                print(s)
                print('l1_e:', l1_e.__class__.__name__, ':', l1_e)
                print('l2_e:', l1_e.__class__.__name__, ':', l2_e)
                print()
                raise AssertionError

        try:
            assert l1 == l2
        except AssertionError:
            print()
            print('l1 l2 no match:')
            print(s)
            print('l:', l)
            print('ol:', ol)
            print('list:', l1)
            print('List:', l2)
            print()

            raise AssertionError

        # if time() > start_time + 60 * 0.5:
        #    break

        if times == 10000:
            break

    print('use random data run times: {}, in {:.2f}s'.format(times, time() - start_time))


########################################################################################################################
# for List
########################################################################################################################
def test_list_add():
    add_count = 0
    l = CountList()

    l.append(6)
    add_count += 1

    l.append(3)
    add_count += 1

    l *= 3
    add_count += 4

    l.extend(['a', 'hello', None, {None: 's'}])
    add_count += 4

    l.insert(2, 3.14)
    add_count += 1

    l += [3, 'a', 'hello', 'world']
    add_count += 4

    assert add_count == l.before_add_count == l.after_add_count

    assert 0 == l.before_del_count == l.after_del_count


def test_list_del():
    del_count = 0
    l = CountList([1, 2, 3, 4, 5, 6, 7, 8, 9, 0], False)

    l.pop()
    del_count += 1

    l.remove(5)
    del_count += 1

    assert del_count == l.before_del_count == l.after_del_count

    assert 0 == l.before_add_count == l.after_add_count


def test_list_add_del():
    add_count = 0
    del_count = 0

    l = CountList([0, 1, 2])
    add_count += 3

    l[2] = None
    del_count += 1
    add_count += 1

    assert add_count == l.before_add_count == l.after_add_count

    assert del_count == l.before_del_count == l.after_del_count


########################################################################################################################
# for Dict
########################################################################################################################
def test_dict_add():
    add_count = 0

    d = CountDict()
    d['hello'] = 'world'
    d[42] = None
    add_count += 2

    d.update({None: 'a', (None, 's'): 3})
    add_count += 2

    assert add_count == d.before_add_count == d.after_add_count

    assert 0 == d.before_del_count == d.after_del_count


def test_dict_del():
    del_count = 0

    d = CountDict({'hello': 'world', 42: None, None: 'a', (None, 's'): 3})

    del d['hello']
    del_count += 1

    d.pop(42)
    del_count += 1

    d[None] = 'b'
    del_count += 1

    d.popitem()
    del_count += 1

    assert del_count == d.before_del_count == d.after_del_count


def test_dict_add_del():
    add_count = 0
    del_count = 0

    d = CountDict({'a': 1, 'b': 2, 'c': 3, 'd': 4})
    add_count += 4

    d.update({'a': 11, 'c': 33})
    del_count += 2
    add_count += 2

    assert add_count == d.before_add_count == d.after_add_count
    assert del_count == d.before_del_count == d.after_del_count
