import logging

import datafaser.operations
from datafaser.validation import Validator


class Runner:

    def __init__(self, data_tree, operations=None):
        """
        :param data_tree: DataTree object
        :param operations: map of operation names to functions implementing them
        """

        self.data_tree = data_tree
        self.operations = operations or datafaser.operations.get_default_operations_map(data_tree)
        self.phase_number = 0
        self.create_logger()

    def create_logger(self):
        self.logger = logging.getLogger(__name__)

    def load_and_run_all_plans(self):
        """
        Runs plans as long as any are available at `datafaser.run.plan`.
        """

        while len(self.data_tree.reach('datafaser.run.plan')) > 0:
            self.run_next_phase()

    def run_next_phase(self):
        """
        Runs next phase from current plan at `datafaser.run.plan`.
        """

        self.phase_number += 1
        run = self.data_tree.reach('datafaser.run')
        phase = run['plan'].pop()
        if isinstance(phase, dict) and len(phase) == 1:
            run['phase'] = phase
            for phase_name, operations in phase.items():
                self.logger.info('Running phase #%d: "%s"' % (self.phase_number, phase_name))
                self.run_operation(operations)
            self.validate()
            if 'done' not in run:
                run['done'] = []
            run['done'].append(phase)
            del run['phase']
        else:
            raise ValueError(
                    'Phase #%d in plan does not map one name to operations: %s' %
                    (self.phase_number, str(phase))
            )

    def run_operation(self, operations):
        """
        :param operations: list of operations: a map from operation name to its parameter structure.
        """

        for step in operations:
            for operation in step.keys():
                if operation in self.operations:
                    self.logger.debug('Run operation "%s"' % operation)
                    self.operations[operation](self.data_tree, step[operation])
                else:
                    raise ValueError('Unknown operation: "%s"' % operation)

    def validate(self):
        validator = Validator(self.data_tree.reach('schema'))
        result = validator.validate(self.data_tree.data)
        errors = result.has_errors()
        if errors:
            for description in result.descriptions():
                self.logger.error("%s\n" % description)
            raise ValueError('%d errors after phase #%d' % (errors, self.phase_number))
