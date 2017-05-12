import valideer
from valideer.base import ValidationError as ValideerValidationError

from ..exceptions import ValidationError

schema = {
    "+name": "string",
}

validator = valideer.parse(schema)

def validate_manifest(manifest):
    try:
        return validator.validate(manifest)
    except ValideerValidationError as e:
        raise ValidationError(e)
