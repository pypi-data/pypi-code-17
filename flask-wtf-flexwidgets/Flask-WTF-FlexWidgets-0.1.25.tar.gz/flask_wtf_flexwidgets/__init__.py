# -*- coding: utf-8 -*-
"""
    Flask-WTF-FlexWidgets - A flask extension that provides customizable WTF widgets and macros.

    Author: Bill Schumacher <bill@servernet.co>
    License: LGPLv3
    Copyright: 2017 Bill Schumacher, Cerebral Power
** GNU Lesser General Public License Usage
** This file may be used under the terms of the GNU Lesser
** General Public License version 3 as published by the Free Software
** Foundation and appearing in the file LICENSE.LGPLv3 included in the
** packaging of this file. Please review the following information to
** ensure the GNU Lesser General Public License version 3 requirements
** will be met: https://www.gnu.org/licenses/lgpl.html.


    Some code copied from:
    https://github.com/maxcountryman/flask-login and https://github.com/mattupstate/flask-security  See LICENSE
"""
from flask import current_app, Blueprint, render_template
from werkzeug.local import LocalProxy
from ._compat import PY2, text_type, iteritems
from jinja2 import Template

_wtf_flex_widgets = LocalProxy(lambda: current_app.extensions['wtf_flex_widgets'])


_default_config = {
    'SUBDOMAIN': None,
    'URL_PREFIX': None,
    'BLUEPRINT_NAME': 'wtf_flex_widgets',
    'RENDER_URL': '/',
}

_default_widget_config = {
    'HTML_ATTR_ID': None,
    'HTML_ATTR_CLASS': None,
    'HTML_ATTR_LABEL_ID': None,
    'HTML_ATTR_LABEL_CLASS': None,
    'HTML_ATTR_INPUT_ID': None,
    'HTML_ATTR_INPUT_CLASS': None,
    'HTML_ATTR_INPUT_CONTAINER_ID': None,
    'HTML_ATTR_INPUT_CONTAINER_CLASS': None,
    'HTML_ATTR_INPUT_CONTAINER_ITEM_ID': None,
    'HTML_ATTR_INPUT_CONTAINER_ITEM_CLASS': None,
    'HTML_ATTR_INPUT_CONTAINER_ITEM_SELECTED_ID': None,
    'HTML_ATTR_INPUT_CONTAINER_ITEM_SELECTED_CLASS': None
}

css_template = """
.flex_container {
    display: flex;
}

.flex_container_item {
    flex: 1;
}

.form_field {
    display: flex; max-width: 400px; margin: 5px 5px 5px 5px; height: 36px;
}

.form_field_label {
    text-align: right;
    flex: 1;
}

.form_field_label label {
    margin-bottom: 0px; margin-top: 8px;
}

.form_field_input {
    margin: 5px 5px 5px 5px; height: 25px;
}

.form_field_input_container input[type=checkbox] {
    margin: 5px 5px 5px 5px;
}

.form_field_input_container {
    text-align: left;
    display: flex;
}

.form_field_input_container_item {
    flex: 1;
}

.form_field_input_container_item_selected {
    flex: 1;
}
"""


def get_config(app, widget=False):
    """Conveniently get the wtf flex widget configuration for the specified
    application without the annoying 'WTF_FLEX_WIDGET_' prefix.
    :param app: The application to inspect
    :param widget: Only return the HTML customization for widgets.
    """
    items = app.config.items()
    prefix = 'WTF_FLEX_WIDGETS_'
    if widget:
        prefix += 'HTML'

    def strip_prefix(tup):
        return tup[0].replace('WTF_FLEX_WIDGETS_', ''), tup[1]

    return dict([strip_prefix(i) for i in items if i[0].startswith(prefix)])


def _get_state(app, **kwargs):
    for key, value in get_config(app).items():
        kwargs[key.lower()] = value

    kwargs.update(dict(
        app=app,
    ))

    return _FlexWidgetState(**kwargs)


class _FlexWidgetState(object):

    def __init__(self, **kwargs):
        self.blueprint_name = ""
        self.url_prefix = ""
        self.subdomain = ""
        for key, value in kwargs.items():
            setattr(self, key.lower(), value)


class WTFFlexWidgets(object):

    def __init__(self, app=None, **kwargs):
        self.app = app
        self._engine = None
        self._db = None
        if app is not None:
            self._state = self.init_app(app, **kwargs)

    def init_app(self, app, register_blueprint=True):

        for key, value in _default_config.items():
            app.config.setdefault('WTF_FLEX_WIDGETS_' + key, value)

        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

        state = _get_state(app)

        if register_blueprint:
            app.register_blueprint(create_blueprint(state, __name__))
            # app.context_processor(_context_processor)

        state.render_template = self.render_template
        app.extensions['wtf_flex_widgets'] = state

        return state

    def render_template(self, *args, **kwargs):
        return render_template(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self._state, name, None)

    def teardown(self, exception):
        pass


def create_blueprint(state, import_name):
    """Creates the flask wtf flexwidgets extension blueprint"""

    bp = Blueprint(state.blueprint_name, import_name,
                   url_prefix=state.url_prefix,
                   subdomain=state.subdomain,
                   template_folder='templates')

    return bp


form_macro_template = """
{% macro render_form(form, method="POST", action=None, upload=False) %}
    <form
     method="{{ method }}"
     {% if action != None -%} action="{{ action }}"{% endif -%}
     {% if upload %} enctype="multipart/form-data"{% endif -%}
    >
        {% if has_hidden_tag %}
            {{ form.hidden_tag() }}
        {% endif %}
        {% for field in form %}
            {{ field }}
        {% else %}
            No fields in form to render.
        {% endfor %}
    </form>
{% endmacro %}
"""

form_template = Template(form_macro_template + """
{{ render_form(form, method=method, action=action, upload=upload) }}
""")

field_top_template = """
<div {% if html_attr_id -%}id="{{ html_attr_id}}" {% endif -%}
 class="form_field{%- if html_attr_class -%} {{ html_attr_class }}{% endif -%}"
>
    <div {% if html_attr_label_id -%}id="{{ html_attr_label_id }}" {% endif -%}
     class="form_field_label{%- if html_attr_label_class -%} {{ html_attr_label_class }}{%- endif -%}"
    >
        {{ field.label }}
    </div>
    <div {% if html_attr_input_container_id -%}id="{{ html_attr_input_container_id }}" {% endif -%}
     class="form_field_input_container{%- if html_attr_input_container_class %} {{ html_attr_input_container_class }}{%- endif -%}"
    >
"""

field_bottom_template = """
    </div>
</div>
{% if field.errors %}
<div>
    <ul>
    {% for error in field.errors %}
        <li>{{ error }}</li>
    {% endfor %}
    </ul>
</div>
{% endif %}
"""


def glue_templates(widget_template):
    return Template("""{top_template}
        {widget_template}
    {bottom_template}
    """.format(top_template=field_top_template,
               widget_template=widget_template,
               bottom_template=field_bottom_template)
    )


def render_form_template(form, method='POST', action='', upload=False, *args, **kwargs):
    has_hidden_tag = False
    if hasattr(form, 'hidden_tag'):
        has_hidden_tag = True
    return form_template.render(form=form, method=method, action=action, upload=upload, has_hidden_tag=has_hidden_tag,
                                *args, **kwargs)


class FlexWidgetAbstract(object):
    def __init__(self):
        pass

    def __call__(self, field, **kwargs):

        for key, value in iteritems(_default_widget_config):
            if key.lower() not in kwargs.keys():
                kwargs[key] = value
        for key, value in iteritems(get_config(current_app, widget=True)):
            if kwargs.get(key.lower(), None) is None and value is not None:
                kwargs[key] = value
        return self.render(field, **kwargs)

    def render(self, field, **kwargs):
        raise NotImplementedError


class FlexIntegerWidget(FlexWidgetAbstract):

    def render(self, field, **kwargs):
        return glue_templates("""
            <input
                 type="number"
                 name="{{ field.name }}"
                 value="{% if field.data %}{{ field.data }}{% endif %}"
                 {%- if html_attr_input_id -%}id="{{ html_attr_input_id }}"{%- endif %} class="form_field_input
                 {%- if html_attr_input_class -%} {{ html_attr_input_class }}{%- endif -%}"
            />
        """).render(field=field, **kwargs)


class FlexDateWidget(FlexWidgetAbstract):

    def render(self, field, **kwargs):
        return glue_templates("""
            <input
                 type="date"
                 name="{{ field.name }}"
                 value="{% if field.data %}{{ field.data }}{% endif %}"
                 {%- if html_attr_input_id -%}id="{{ html_attr_input_id }}"{%- endif %} class="form_field_input
                 {%- if html_attr_input_class -%} {{ html_attr_input_class }}{%- endif -%}"
            />
        """).render(field=field, **kwargs)


class FlexDateTimeWidget(FlexWidgetAbstract):

    def render(self, field, **kwargs):
        return glue_templates("""
            <input
                 type="datetime"
                 name="{{ field.name }}"
                 value="{% if field.data %}{{ field.data }}{% endif %}"
                 {%- if html_attr_input_id -%}id="{{ html_attr_input_id }}"{%- endif %} class="form_field_input
                 {%- if html_attr_input_class -%} {{ html_attr_input_class }}{%- endif -%}"
            />
        """).render(field=field, **kwargs)


class FlexStringWidget(FlexWidgetAbstract):

    def render(self, field, **kwargs):
        return glue_templates("""
            <input
                 type="text"
                 name="{{ field.name }}"
                 value="{% if field.data %}{{ field.data }}{% endif %}"
                 {%- if html_attr_input_id -%}id="{{ html_attr_input_id }}"{%- endif %} class="form_field_input
                 {%- if html_attr_input_class -%} {{ html_attr_input_class }}{%- endif -%}"
            />
        """).render(field=field, **kwargs)


class FlexPasswordWidget(FlexWidgetAbstract):

    def render(self, field, **kwargs):
        return glue_templates("""
            <input
                 type="password"
                 name="{{ field.name }}"
                 value="{% if field.data %}{{ field.data }}{% endif %}"
                 {%- if html_attr_input_id -%}id="{{ html_attr_input_id }}"{%- endif %} class="form_field_input
                 {%- if html_attr_input_class -%} {{ html_attr_input_class }}{%- endif -%}"
            />
        """).render(field=field, **kwargs)


class FlexBoolWidget(FlexWidgetAbstract):

    def render(self, field, **kwargs):
        return glue_templates("""
            <input
                 type="checkbox"
                 name="{{ field.name }}"
                 value="{% if field.data %}{{ field.data }}{% endif %}"
                 {%- if html_attr_input_id -%}id="{{ html_attr_input_id }}"{%- endif %} class="form_field_input
                 {%- if html_attr_input_class -%} {{ html_attr_input_class }}{%- endif -%}"
                 {%- if field.checked -%}checked=CHECKED{%- endif -%}
            />
        """).render(field=field, **kwargs)


class FlexSelectWidget(FlexWidgetAbstract):

    def render(self, field, **kwargs):
        return Template("""
            <div{%- if html_attr_id -%} id="{{ html_attr_id}}"{%- endif -%}
             class="form_field{%- if html_attr_class -%} {{ html_attr_class }}{% endif -%}"
            >
                <div{%- if html_attr_label_id -%} id="{{ html_attr_label_id }}"{%- endif -%}
                 class="form_field_label{%- if html_attr_label_class -%} {{ html_attr_label_class }}{%- endif -%}"
                >
                    {{ field.label }}
                </div>
                <div{%- if html_attr_input_container_id -%} id="{{ html_attr_input_container_id }}"{%- endif -%}
                 class="form_field_input_container{%- if html_attr_input_container_class -%}
                                                      {{ html_attr_input_container_class }}{%- endif -%}"
                >
                    {% for choice in field.choices %}
                    <div{%- if html_attr_input_container_item_id -%}
                        id="{{ html_attr_input_container_item_id }}"{%- endif -%}
                     class="form_field_input_container_item{%- if html_attr_input_container_item_class -%}
                                                               {{ html_attr_input_container_item_class }}{%- endif -%}"
                    >
                        <input
                         type="radio"
                         name="{{ field.name }}"
                         value="{{ field.value }}"
                         {%- if html_attr_input_id -%}id="{{ html_attr_input_id }}"{%- endif -%}
                         class="form_field_input{%- if html_attr_input_class -%}
                                                    {{ html_attr_input_class }}{%- endif -%}"
                         {%- if field.checked -%}checked=CHECKED{%- endif -%}
                        />
                    </div>
                    {% else %}
                        No choices configured.
                    {% endfor %}
                </div>
            </div>
        """).render(field=field, **kwargs)


class FlexSelectMultipleWidget(FlexWidgetAbstract):

    def render(self, field, **kwargs):
        return Template("""
            <div{%- if html_attr_id -%} id="{{ html_attr_id}}"{%- endif -%}
             class="form_field{%- if html_attr_class -%} {{ html_attr_class }}{% endif -%}"
            >
                <div{%- if html_attr_label_id -%} id="{{ html_attr_label_id }}"{%- endif -%}
                 class="form_field_label{%- if html_attr_label_class -%} {{ html_attr_label_class }}{%- endif -%}"
                >
                    {{ field.label }}
                </div>
                <div{%- if html_attr_input_container_id -%} id="{{ html_attr_input_container_id }}"{%- endif -%}
                 class="form_field_input_container{%- if html_attr_input_container_class -%}
                                                      {{ html_attr_input_container_class }}{%- endif -%}"
                >
                    {% for choice in field.choices %}
                    <div{% if choice.selected and html_attr_input_container_item_selected_id %}
                            id="{{ html_attr_input_container_item_selected_id }}"
                        {% else %}
                            {%- if html_attr_input_container_item_id -%}
                                id="{{ html_attr_input_container_item_id }}"
                            {%- endif -%}
                        {%- endif -%}
                        class="form_field_input_container_item
                        {%- if html_attr_input_container_item_class -%}
                            {{ html_attr_input_container_item_class }}
                        {%- endif -%}"
                    >
                        <input
                         type="checkbox"
                         name="{{ field.name }}"
                         value="{{ field.value }}"
                         {%- if html_attr_input_id -%}
                            id="{{ html_attr_input_id }}"
                         {%- endif -%}
                         class="form_field_input
                         {%- if html_attr_input_class -%}
                             {{ html_attr_input_class }}
                         {%- endif -%}"
                         {%- if choice.checked -%}
                             checked=CHECKED
                         {%- endif -%}
                        />
                    </div>
                    {% else %}
                        No choices configured.
                    {% endfor %}
                </div>
            </div>
        """).render(field=field, **kwargs)


class FlexSubmitWidget(FlexWidgetAbstract):
    # TODO: Fix the template.
    def render(self, field, **kwargs):
        return Template("""
            <input
                 type="submit"
                 name="{{ field.name }}"
                 value="{{ field.label.text }}"
                 {%- if html_attr_input_id -%}id="{{ html_attr_input_id }}"{%- endif %} class="form_field_input
                 {%- if html_attr_input_class -%} {{ html_attr_input_class }}{%- endif -%}"
            />
        """).render(field=field, **kwargs)
