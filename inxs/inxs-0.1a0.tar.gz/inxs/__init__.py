from copy import deepcopy
from functools import lru_cache
import re
from types import SimpleNamespace
from typing import Any, Callable, Iterator, Mapping, Sequence, Union

import dependency_injection
from lxml import etree


# constants

__version__ = '0.1a0'

TRAVERSE_DEPTH_FIRST = True << 0
TRAVERSE_WIDTH_FIRST = False << 0
TRAVERSE_LEFT_TO_RIGHT = True << 1
TRAVERSE_RIGHT_TO_LEFT = False << 1
TRAVERSE_TOP_TO_BOTTOM = True << 2
TRAVERSE_BOTTOM_TO_TOP = False << 2


# exceptions


class InxsException(Exception):
    pass


class FlowControl(InxsException):  # FIXME rather like StopIteration
    pass


class AbortRule(FlowControl):
    """ Can be raised to abort the evaluation of remaining rule handlers. """
    pass


class AbortTransformation(FlowControl):
    """ Can be raised to abort a transformation. """


# helpers


def dict_from_namespace(ns):
    return {x: getattr(ns, x) for x in dir(ns) if not x.startswith('_')}


# rules definition


class ConditionGroup(list):
    def __init__(self, *conditions) -> None:
        super().__init__()
        self.extend(conditions)


for condition_group in ('Any', 'Not', 'OneOf'):
    globals()[condition_group] = type(condition_group, (ConditionGroup,), {})
del condition_group


class Rule:
    __slots__ = ('name', 'conditions', 'handlers', 'traversal_order')

    def __init__(self, conditions, handlers, name: str = None,
                 traversal_order: int = None) -> None:
        self.name = name
        self.conditions = conditions
        self.handlers = handlers
        self.traversal_order = traversal_order


# transformation


Config = SimpleNamespace


def _traverse_df_ltr_ttb(root) -> Iterator[etree._Element]:
    yield from root.iter()


class Transformation:
    __slots__ = ('name', 'rules', 'config', 'states')

    config_defaults = {
        'traversal_order': TRAVERSE_DEPTH_FIRST | TRAVERSE_TOP_TO_BOTTOM | TRAVERSE_LEFT_TO_RIGHT
    }

    traversers = {
        TRAVERSE_DEPTH_FIRST | TRAVERSE_LEFT_TO_RIGHT | TRAVERSE_TOP_TO_BOTTOM: _traverse_df_ltr_ttb,
    }

    def __init__(self, *rules, name: str = None,
                 config: SimpleNamespace = None) -> None:
        self.name = name
        self.rules = rules
        self.config = SimpleNamespace() if config is None else config
        self._set_config_defaults()
        self.states = None

    def _set_config_defaults(self) -> None:
        for key, value in self.config_defaults.items():
            if not hasattr(self.config, key):
                setattr(self.config, key, value)

    def __call__(self, source: Union[etree._Element, etree._ElementTree], copy=True) -> Any:
        self._init_transformation(source, copy)

        for rule in self.rules:
            self.states.current_rule = rule
            try:
                if isinstance(rule, Rule):
                    self._apply_rule(rule)
                elif callable(rule):
                    self._apply_handlers((rule,))
                else:
                    raise RuntimeError
            except AbortTransformation:
                break

        result = self._get_object_by_name(self.config.result_object)
        self._finalize_transformation()
        return result

    def _init_transformation(self, source, copy) -> None:
        self.states = SimpleNamespace()
        self.states.previous_result = None
        self.states.context = SimpleNamespace(**deepcopy(self.config.context))

        if copy:
            source = deepcopy(source)

        if isinstance(source, etree._ElementTree):
            self.states.context.tree = source
            self.states.context.root = source.getroot()
            if getattr(self.config, 'result_object', None) is None:
                self.config.result_object = 'context.tree'
        elif isinstance(source, etree._Element):
            self.states.context.tree = source.getroottree()
            self.states.context.root = source
            if getattr(self.config, 'result_object', None) is None:
                self.config.result_object = 'context.root'

        self.states.xpath_evaluator = etree.XPathEvaluator(source, smart_prefix=True)

    def _apply_rule(self, rule) -> None:
        traverser = self._get_traverser(rule.traversal_order)
        for element in traverser(self.states.context.root):
            self.states.current_element = element
            if self._test_conditions(element, rule.conditions):
                try:
                    self._apply_handlers(rule.handlers)
                except AbortRule:
                    break

    @lru_cache(8)
    def _get_traverser(self, traversal_order: Union[int, None]) -> Callable:
        if traversal_order is None:
            traversal_order = self.config.traversal_order
        traverser = self.traversers.get(traversal_order)
        if traverser is None:
            raise NotImplemented
        return traverser

    def _test_conditions(self, element, conditions) -> bool:
        if not isinstance(conditions, Sequence) or isinstance(conditions, (str, ConditionGroup)):
            conditions = (conditions,)

        for condition in conditions:
            if not self._test_condition(element, condition):
                return False
        return True

    @lru_cache()
    def _test_condition(self, element, condition) -> bool:
        if isinstance(condition, Any):
            return any(self._test_condition(element, x) for x in condition)
        elif isinstance(condition, OneOf):
            return [self._test_condition(element, x) for x in condition].count(True) == 1
        elif isinstance(condition, Not):
            return not any(self._test_condition(element, x) for x in condition)

        if isinstance(condition, str):
            if ':' in condition:
                # assumes an URI
                return etree.QName(element).namespace == condition
            elif condition.isalpha():
                # assumes a tag
                return etree.QName(element).localname == condition
            else:
                # assumes an XPath
                return element in self.states.xpath_evaluator(condition)

        if isinstance(condition, Mapping):
            return self._match_attributes(element, condition)

        raise RuntimeError('Unhandled condition: %s' % condition)

    def _match_attributes(self, element, condition) -> bool:
        def match_value():
            value = element.attrib[attrib_name]
            if isinstance(constraint, str):
                return value == constraint
            elif isinstance(constraint, re._pattern_type):
                return constraint.match(value)

        for name, constraint in condition.items():
            if isinstance(name, str):
                attrib_name = name
                if not match_value():
                    return False
            elif isinstance(name, re._pattern_type):
                for attrib_name in (x for x in element.attrib if name.match(x)):
                    if not match_value():
                        return False
        return True

    def _apply_handlers(self, handlers) -> None:
        if not isinstance(handlers, Sequence):
            handlers = (handlers,)

        for handler in handlers:
            if isinstance(handler, Sequence):
                self._apply_handlers(handlers)
            kwargs = dependency_injection.resolve_dependencies(handler, self._available_dependencies).as_kwargs
            if isinstance(handler, Transformation):
                kwargs['source'] = kwargs['element']
                kwargs['copy'] = False  # FIXME?! that may not always be desirable
            self.states.previous_result = handler(**kwargs)

    @property
    def _available_dependencies(self) -> Mapping:
        context = self.states.context
        result = dict_from_namespace(self.config)
        result.update(dict_from_namespace(context))
        result.update({
            'config': self.config,
            'context': context,
            'element': getattr(self.states, 'current_element', None),
            'previous_result': self.states.previous_result,
            'root': context.root,
            'transformation': self,
            'transformation_name': self.name,
            'tree': context.tree,
        })

        rule = self.states.current_rule
        if isinstance(rule, Rule):
            result['rule_name'] = rule.name
        elif callable(rule):
            result['rule_name'] = rule.__name__

        return result

    def _finalize_transformation(self) -> None:
        self.states = None

    def _get_object_by_name(self, fqn) -> Any:
        context = self
        if fqn.startswith('context.'):
            fqn = 'states.' + fqn

        for name in fqn.split('.'):
            context = getattr(context, name)
        return context
