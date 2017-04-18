"""
A set of classes and functions that help manage applications.
"""

import importlib

__all__ = ['init_blueprints']


def init_blueprints(app, app_name, blueprints):
    """
    Import and register a list of blueprints and return a map of the modules
    imported.
    """

    blueprint_modules = {}
    for blueprint in blueprints:
        # Import the blueprint module
        blueprint_module = import_module('blueprints.{0}'.format(blueprint))
        blueprint_modules[blueprint] = blueprint_module

        # Import the app module within the blueprint
        import_module('blueprints.{0}.{1}'.format(blueprint, app_name))

        # Register the blueprint
        app.register_blueprint(blueprint_module.blueprint)

    return blueprint_modules
