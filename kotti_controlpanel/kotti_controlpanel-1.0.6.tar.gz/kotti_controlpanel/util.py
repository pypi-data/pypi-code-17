import re
import colander
import inspect

from kotti.resources import get_root
from kotti.views.slots import objectevent_listeners
from kotti.views.slots import slot_events

from kotti_controlpanel.config import SETTINGS, CONTROL_PANEL_LINKS
from kotti_controlpanel.resources import ControlPanel
from kotti_controlpanel.resources import ModuleSettings
from kotti_controlpanel.resources import SettingObj


def slugify(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug."""
    return re.sub("[^a-zA-Z\d:]", text.lower(), "-")


def get_setting(name, default=None, modname=None):
    if modname is None:
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        modname = module.__name__
        if '.' in modname:
            modname = modname[:modname.find('.')]  # pragma: no cover
    if not name.startswith(modname):
        name = '{0}-{1}'.format(modname, name)
    settings = get_settings()
    if name in settings:
        return settings[name]
    return default


def set_setting(name, val, modname=None):
    if modname is None and "-" not in name:
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        modname = module.__name__
        if '.' in modname:
            modname = modname[:modname.find('.')]  # pragma: no cover
    if modname and not name.startswith(modname):
        name = '{0}-{1}'.format(modname, name)
    settings = get_settings()
    # It seems not possible to save a set type in a MutableDict,
    # so convert it to a list.
    if type(val) == set:
        val = list(val)
    settings[name] = val


def get_settings():
    root = get_root()
    if "kotti_controlpanel" not in root.annotations:
        root.annotations['kotti_controlpanel'] = {}
    return root.annotations['kotti_controlpanel']


def get_links(controlpanel_id):
    cpi = slugify(controlpanel_id)
    return CONTROL_PANEL_LINKS.get(cpi, [])


def add_links(controlpanel_id, *links):
    cpi = slugify(controlpanel_id)
    clinks = CONTROL_PANEL_LINKS.get(cpi, [])
    for link in links:
        clinks.append(link)
    CONTROL_PANEL_LINKS[cpi] = clinks


def add_settings(mod_settings, links=None):
    """Get a dictionary and translate this into an object structure.
    """
    settings = get_settings()
    module_settings = ModuleSettings(**mod_settings)
    if module_settings.module is None:
        # If the module name is omitted: get it
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        modname = module.__name__
        if '.' in modname:
            modname = modname[:modname.find('.')]
        module_settings.module = modname
    if module_settings.settings:
        for setting in module_settings.settings:
            setting_obj = SettingObj(**setting)
            # name and title of a setting is required
            if setting_obj.name is None:
                raise ValueError('A setting has to have a name.')
            if setting_obj.title is None:
                raise ValueError('A setting has to have a title.')
            setting_obj.module = module_settings.module
            default = None
            if 'default' in setting:
                default = setting['default']
            if not setting_obj.field_name in settings:
                settings[setting_obj.field_name] = default
            module_settings.settings_objs.append(setting_obj)
    if module_settings.schema_factory:
        schema = module_settings.schema_factory()
        for child in schema.children:
            field_name = child.name
            if not field_name.startswith(module_settings.module):
                field_name = u"%s-%s" % (module_settings.module, child.name)
            if not field_name in settings:
                value = None
                if child.default is not colander.null:
                    value = child.default
                settings[field_name] = value
    mod_slug = slugify(module_settings.name)
    if type(links) == list:
        add_links(mod_slug, *links)
    module_settings.slug_id = mod_slug
    SETTINGS[mod_slug] = module_settings


def remove_from_slots(widget, slot=None):
    """Check all slots if a widget is already set and remove it
       from the listener.
    """
    for slot_event in slot_events:
        if slot is not None:
            if slot != slot_event.name:
                continue
        try:
            listener = objectevent_listeners[(slot_event, None)]
        except TypeError:  # pragma: no cover
            listener = None
        if listener is not None:
            for func in listener:
                for closure in func.func_closure:
                    if closure.cell_contents == widget:
                        listener.remove(func)
                        break


def show_in_context(setting, context):
    """Check if the the item should be shown in the given context."""
    show = False
    if setting == u'everywhere':
        show = True
    elif setting == u'only on root':
        show = context == get_root()
    elif setting == u'not on root':
        show = context != get_root()
    return show
