from wtforms import Form, StringField, validators


class PlaceForm(Form):
    place = StringField('', [validators.DataRequired(message='Debe seleccionar un lugar!')])
