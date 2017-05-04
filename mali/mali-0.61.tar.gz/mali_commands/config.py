# coding=utf-8
import click

try:
    import ConfigParser as configparser
except ImportError:
    import configparser

missing_link_config = 'missinglink.cfg'


class Config(object):
    def __init__(self):
        parser = configparser.RawConfigParser()
        parser.read([missing_link_config])

        self.parser = parser

    @property
    def token_config(self):
        return self.items('token')

    @property
    def refresh_token(self):
        return self.token_config.get('refresh_token')

    @property
    def id_token(self):
        return self.token_config.get('id_token')

    def items(self, section=None):
        try:
            return dict(self.parser.items(section))
        except configparser.NoSectionError:
            return {}

    def set(self, section, key, val):
        try:
            self.parser.add_section(section)
        except configparser.DuplicateSectionError:
            pass

        self.parser.set(section, key, val)

    def write(self, fo):
        self.parser.write(fo)

    def update_and_save(self, d):
        for section, section_values in d.items():
            for key, val in section_values.items():
                self.set(section, key, val)

        with open(missing_link_config, 'w') as configfile:
            self.write(configfile)


pass_config = click.make_pass_decorator(Config, ensure=True)
