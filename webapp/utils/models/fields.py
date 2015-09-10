import json
from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from postgres.fields import JSONField as BaseJSONField

from utils.validators import JsonSchemaValidator


class JSONFormField(forms.Field):
    widget = forms.Textarea

    def prepare_value(self, value):
        return json.dumps(value, indent=4)

    def clean(self, value):
        value = super().clean(value)

        if value is None:
            return value

        try:
            return json.loads(value)
        except ValueError as error:
            raise ValidationError(str(error))


class JSONField(BaseJSONField):

    def __init__(self, schema=None, *args, **kwargs):
        self.schema = None
        if schema:
            self.schema = schema
            kwargs.setdefault('validators', []).append(JsonSchemaValidator(schema))
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': JSONFormField,
        }

        if self.schema:
            defaults['help_text'] = mark_safe(
                '<pre>{}</pre>'.format(json.dumps(self.schema, indent=4))
            )

        defaults.update(kwargs)
        return super().formfield(**defaults)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        path = 'utils.models.JSONField'
        kwargs.update(
            schema=self.schema
        )
        return name, path, args, kwargs

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return value
