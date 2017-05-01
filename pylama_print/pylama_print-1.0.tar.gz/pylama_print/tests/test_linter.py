from ..linter_print import Linter, DEFAULT_ERR


def test_no_print():
    code = (
        "import sys\n"
        "def say_somethign():\n"
        "    sys.stdout.write('Is there a pipe character?')\n"
        "    sys.stdout.flush()\n"
    )

    linter = Linter()
    messages = linter.run('', code=code)

    assert messages == []


def test_with_print():
    code = (
        "def say_somethign():\n"
        "    print('Have you changed the token?')\n"
    )

    linter = Linter()
    messages = linter.run('', code=code)

    assert isinstance(messages, list)
    assert len(messages) == 1
    assert messages[0]['lnum'] == 2
    assert messages[0]['text'] == DEFAULT_ERR
