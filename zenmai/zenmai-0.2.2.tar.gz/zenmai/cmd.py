import sys
import argparse
import logging
from dictknife import loading
from dictknife.jsonknife.accessor import access_by_json_pointer
from zenmai.langhelpers import import_module, import_symbol


def loadfile_with_jsonref(ref):
    if "#/" not in ref:
        return loading.loadfile(ref)

    filename, query = ref.split("#")
    doc = loading.loadfile(filename)
    return access_by_json_pointer(doc, query)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--module", default="zenmai.actions")
    parser.add_argument("--driver", default="zenmai.driver:Driver")
    parser.add_argument("--logging", default="INFO", choices=list(logging._nameToLevel.keys()))
    parser.add_argument("-f", "--format", default=None, choices=loading.get_formats())
    parser.add_argument("--data", action="append")
    parser.add_argument("--select", default=None)
    parser.add_argument("file", default=None)

    loading.setup()  # xxx:
    args = parser.parse_args()

    driver_cls_path = args.driver
    if ":" not in driver_cls_path:
        driver_cls_path = "swagger_marshmallow_codegen.driver:{}".format(driver_cls_path)
    driver_cls = import_symbol(driver_cls_path)

    module = import_module(args.module)
    data = [loadfile_with_jsonref(path) for path in args.data or []]

    def wrap(d):
        if args.select is None:
            return d
        return access_by_json_pointer(d, args.select.split("#")[-1])

    driver = driver_cls(module, args.file, format=args.format, data=data)

    # todo: option
    logging.basicConfig(
        format="%(levelname)5s:%(name)30s:%(message)s",
        level=logging._nameToLevel[args.logging]
    )
    if args.file is None:
        driver.run(sys.stdin, sys.stdout, wrap=wrap)
    else:
        with open(args.file) as rf:
            driver.run(rf, sys.stdout, wrap=wrap)
