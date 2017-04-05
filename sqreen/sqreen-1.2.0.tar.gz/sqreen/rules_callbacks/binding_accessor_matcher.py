# -*- coding: utf-8 -*-
# Copyright (c) 2016 Sqreen. All Rights Reserved.
# Please refer to our terms for more information: https://www.sqreen.io/terms.html
""" Abstract callback for checking regex against request fields
"""

import re

from logging import getLogger
from collections import Mapping

from ..binding_accessor import BindingAccessor
from ..exceptions import InvalidArgument
from ..runtime_infos import runtime
from ..rules import RuleCallback
from ..matcher import Matcher
from ..utils import is_string


LOGGER = getLogger(__name__)


class BindingAccessorMatcherCallback(RuleCallback):
    def __init__(self, *args, **kwargs):
        super(BindingAccessorMatcherCallback, self).__init__(*args, **kwargs)

        if not isinstance(self.data, Mapping):
            msg = "Invalid data type received: {}"
            raise InvalidArgument(msg.format(type(self.data)))

        try:
            values = self.data['values']
        except KeyError:
            msg = "No key 'values' in data (had {})"
            raise InvalidArgument(msg.format(self.data.keys()))

        self.patterns = []

        for value in values:
            try:
                self.patterns.append({
                    "id": value["id"],
                    "binding_accessor": [BindingAccessor(exp) for exp in value["binding_accessor"]],
                    "matcher": Matcher([value["matcher"]]),
                })
            except (re.error, AssertionError):
                LOGGER.warning("Cannot parse the regex %s", value["matcher"])

    def pre(self, original, *args, **kwargs):
        request = runtime.get_current_request()

        if not request:
            LOGGER.warning("No request was recorded abort")
            return

        binding_eval_args = {
            "binding": locals(),
            "global_binding": globals(),
            "framework": request,
            "instance": original,
            "arguments": args,
            "kwarguments": kwargs,
            "cbdata": self.data,
            "return_value": None,
        }

        cache = {}

        for pattern in self.patterns:
            for binding_accessor in pattern["binding_accessor"]:
                expression = binding_accessor.expression

                if expression in cache:
                    data = cache[expression]
                else:
                    data = binding_accessor.resolve(**binding_eval_args)
                    cache[expression] = data

                if not data:
                    continue

                if is_string(data):
                    data = [data]

                for elem in data:
                    if not elem:
                        continue

                    # Ignore not string values as we use a string matcher
                    # that only match strings
                    if not is_string(elem):
                        continue

                    if pattern["matcher"].match(elem):
                        infos = {
                            "id": pattern["id"],
                            "binding_accessor": expression,
                            "matcher": pattern["matcher"].patterns
                        }
                        self.record_attack(infos)
                        return
