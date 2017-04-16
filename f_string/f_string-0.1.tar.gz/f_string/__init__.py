from parse import findall
import inspect
def convert_f_string_to_normal(f_string):
    ptn = "{{{var_name}}}"
    cnt = 0
    var_list = list()
    for r in findall(ptn, f_string):
        var_list.append(r['var_name'])
        origin = "{var_name}"
        replaced = origin.replace('var_name', r['var_name'])
        f_string = f_string.replace(replaced, "{{{0}}}".format(cnt))
        cnt += 1
    result = "\"{0}\".format({1})".format(f_string, ", ".join(var_list))
    return result

def f(con_string):
    cr = inspect.stack()[0][0]
    frame = inspect.stack()[1][0]
    cr.f_locals.update(frame.f_locals)
    return eval(convert_f_string_to_normal(con_string))