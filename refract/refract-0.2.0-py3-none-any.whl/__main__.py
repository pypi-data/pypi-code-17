import json
import sys
from refract.json import LegacyJSONDeserialiser


if len(sys.argv) == 1:
    print('Usage: {} [files]'.format(sys.argv[0]))
    exit(1)


for path in sys.argv[1:]:
    with open(path) as fp:
        element = LegacyJSONDeserialiser().deserialise(fp.read())

        assets = filter(lambda e: e.element == 'asset', element.recursive_children)
        assetValues = map(lambda e: e.underlying_value, assets)

        for value in assetValues:
            print('Found:')
            try:
                # if json, re-indent
                v = json.loads(value)
                print(json.dumps(v, indent=2, separators=(',', ': ')))
            except:
                print(value)

            print()
