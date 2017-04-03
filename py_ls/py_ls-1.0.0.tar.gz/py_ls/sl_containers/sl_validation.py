from py_ls.pattern_matching.pattern_matching import match, case
from py_ls.sl_containers.sl_try import Try, Success, Failure


class Yield(object):
    def __rrshift__(self, val):
        self.val = val
        return self

    def __rshift__(self, fun):
        """
        :rtype: Try
        """
        return self.val >> match >> (
                     case > Success, lambda x: Success(fun(x.get)),
                     case > Failure, lambda x: x
                     )


def _for_(to_validate, *t):
    res = Success(to_validate)
    i = 0
    stop = len(t)
    while i < stop:
        res = res >> match >> (
                    case > Success, lambda suc_res: Try(lambda: t[i](suc_res.get)) >> match >> (
                                                          case > Success, lambda x: Success(x.get),
                                                          case > Failure, lambda x: x
                                                          ),
                    case > Failure, lambda x: x
                    )
        i += 1

    return res


def validate(to_validate, *t):
    errors = []
    i = 0
    stop = len(t)
    while i < stop:
        errors_supplier = t[i + 1]
        Try(lambda: t[i](to_validate)) >> match >> (
              case > Success, lambda state: state.get >> match >> (
                                                  case > True, lambda _: None,
                                                  case > False, lambda _: errors.append(errors_supplier(to_validate))
                                                  ),
              case > Failure, lambda _: errors.append(errors_supplier(to_validate))
              )
        i += 2

    return Failure(errors) if errors else Success(to_validate)


_yield_ = Yield()
