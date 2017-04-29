from jsonschema.validators import Draft4Validator, ErrorTree


class Validator:
    def __init__(self, schema):
        """
        :param schema: a JSON schema document.
        """
        self.validator = Draft4Validator(schema)

    def validate(self, data):
        """
        :param data: data structure to check against the schema that this validator represents
        :return: ValidationResult object
        """
        return ValidationResult(ErrorTree(self.validator.iter_errors(data)))


class ValidationResult:
    def __init__(self, tree):
        """
        :param tree: jsonschema.validators.ErrorTree instance
        """
        self.error_tree = tree

    def has_errors(self):
        """
        :return: number of errors entered in validation
        """
        return len(self.error_tree)

    def descriptions(self):
        """
        :return: list of strings describing all errors found in validation
        """

        return self._descriptions(self.error_tree)

    def _descriptions(self, tree):
        """
        :param tree: jsonschema.validators.ErrorTree
        :return: array of strings describing each error
        """
        results = []
        for error_type, error in tree.errors.items():
            results.append('%s at "%s" as "%s": %s' % (
                error_type,
                self._deque_as_string(error.absolute_path),
                self._deque_as_string(error.absolute_schema_path),
                error.message
            ))
        for key in tree:
            node = tree[key]
            if isinstance(node, ErrorTree):
                results += self._descriptions(node)
        return results

    def _deque_as_string(self, items):
        return '.'.join([str(item) for item in items])
