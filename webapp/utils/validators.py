from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError
from jsonschema import validate
from jsonschema.exceptions import ValidationError as SchemaError


@deconstructible
class JsonSchemaValidator:

    def __init__(self, schema):
        self.schema = schema

    def __call__(self, value):
        try:
            validate(value, self.schema)
        except SchemaError as error:
            raise ValidationError(error.message)
