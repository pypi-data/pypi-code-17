import fnmatch
import collections
import string

import re
import six
from itculate_sdk import DataType

_mapping_rules = []  # type: list[RuleInfo]

RuleInfo = collections.namedtuple("RuleInfo",
                                  [
                                      "statsd_host_regex",
                                      "statsd_counter_regex",
                                      "statsd_tags_regexs",
                                      "instance_id_regex",
                                      "vertex_key_template",
                                      "counter_template",
                                      "data_type"
                                  ])


def clear_mappings():
    global _mapping_rules
    _mapping_rules = []


def add_statsd_mapping_rule(statsd_host_pattern,
                            statsd_counter_pattern,
                            statsd_tags_patterns,
                            instance_id_pattern,
                            vertex_key_template,
                            counter_template,
                            data_type):
    """
    :param str statsd_counter_pattern: StatsD counter matching rule (can include '*' or '?')
    :param str statsd_host_pattern: Host (IP) matching rule (can include '*' or '?')
    :param dict[str, str]|None statsd_tags_patterns: Tag matching rules (for each tag value - can include '*' or '?')
    :param str|None instance_id_pattern: Instance ID matching rule (can include '*' or '?')
    :param str vertex_key_template: Template to format the ITculate vertex key
    :param str counter_template: Template to format the ITculate counter name
    :param DataType data_type: ITculate data type to associate with the counter
    """

    assert statsd_counter_pattern and statsd_counter_pattern and vertex_key_template and counter_template and data_type
    assert isinstance(data_type, DataType)

    # Convert all the patterns to regexp and then add to list of rules
    statsd_counter_regex = re.compile(fnmatch.translate(statsd_counter_pattern))
    statsd_host_regex = re.compile(fnmatch.translate(statsd_host_pattern)) if statsd_host_pattern else None
    instance_id_regex = re.compile(fnmatch.translate(instance_id_pattern)) if instance_id_pattern else None

    if statsd_tags_patterns:
        statsd_tags_regexs = {tag: re.compile(fnmatch.translate(pattern))
                              for tag, pattern in six.iteritems(statsd_tags_patterns)}
    else:
        statsd_tags_regexs = {}

    # Now add the rule
    global _mapping_rules
    _mapping_rules.append(RuleInfo(statsd_counter_regex=statsd_counter_regex,
                                   statsd_host_regex=statsd_host_regex,
                                   statsd_tags_regexs=statsd_tags_regexs,
                                   instance_id_regex=instance_id_regex,
                                   vertex_key_template=vertex_key_template,
                                   counter_template=counter_template,
                                   data_type=data_type))


def resolve_statsd_sample_keys(host,
                               counter,
                               tags=None,
                               instance_id=None,
                               only_one=False):
    """
    Given information about a counter from StatsD, this will resolve to ITculate vertex key, counter and data type.
    The lookup can yield more than one result (in case the rules

    :param str host: Agent host (IP) from Statsd
    :param str counter: StatsD counter name
    :param dict[str, str]|None tags: Tags received (typically from DD)
    :param str|None instance_id: Optional Instance ID identifying the host (e.g. AWS Instance ID)
    :param bool only_one: If True, will return only the first mapping. Otherwise will return all possible mappings.

    :rtype: collections.Iterable[(str, str, DataType)]
    :return: Generator of tuples (vertex_key, counter, data type) or None if no association found
    """

    global _mapping_rules

    # Lazy initialize variables
    variables = None

    for rule in _mapping_rules:  # type: RuleInfo
        if rule.statsd_host_regex and not rule.statsd_host_regex.match(host):
            continue

        if rule.statsd_counter_regex and not rule.statsd_counter_regex.match(counter):
            continue

        if instance_id and rule.instance_id_regex and not rule.instance_id_regex.match(instance_id):
            continue

        if tags and rule.statsd_tags_regexs:
            should_skip = False

            for tag, tag_regex in six.iteritems(rule.statsd_tags_regexs):
                tag_value = tags.get(tag)
                if tag_value and not tag_regex.match(tags[tag]):
                    should_skip = True
                    break

            if should_skip:
                continue

        if variables is None:
            variables = {
                "host": host,
                "counter": counter,
                "instance_id": instance_id,
                "data_type": rule.data_type.get_type()
            }

            # Add tags
            if tags:
                variables.update({"tags_{}".format(key): value for key, value in six.iteritems(tags)})

        # Translate the templates using the variables
        vertex_key = string.Template(rule.vertex_key_template).substitute(variables)
        vertex_counter = string.Template(rule.counter_template).substitute(variables)

        yield vertex_key, vertex_counter, rule.data_type

        if only_one:
            # Stop after first yield
            return

