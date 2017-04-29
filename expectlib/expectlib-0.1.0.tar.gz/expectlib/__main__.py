if __name__ == '__main__':
    from expectlib import expect as e

    # Equal
    e(10).to.equal(10)()
    (e(10) == 10)()

    # Negate
    e(10).to._not().equal(100)()
    (~e(10) == 100)()

    # True
    e(True).to.be.true()
    (e(True) % True)()

    # False
    e(False).to.be.false()
    (e(False) % False)()

    # None
    e(None).to.be.none()
    (e(None) % None)()

    # Greater Than
    e(10).to.be.greater_than(9)()
    (e(10) > 9)()

    # Less Than
    e(100).to.be.lesser_than(1000)()
    (e(100) < 1000)()

    # Greater Than Or Equal
    e(10).to.be.greater_than_or_equal(9)
    (e(10) >= 9)()

    # Less Than Or Equal
    e(100).to.be.lesser_than_or_equal(1000)()
    (e(100) <= 1000)()

    # Regex Match
    e("foobar").to.match("^foo")()
    (e("foobar") // "^foo")()

    # Starts With
    e("foobar").to.start_with("foo")("What??")
    (e("foobar") << "foo")()

    # Ends With
    e("foobar").to.end_with("bar")()
    (e("foobar") >> "bar")()

    # Contains
    e(["foo", "bar"]).to.contain("foo")("Something failed")
    (e(["foo", "bar"]) ^ "foo")()

    e([]).to.be.empty()()
