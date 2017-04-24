from setuptools import Command, setup
from distutils.errors import DistutilsOptionError
from ilabs.s3util.util import cli_pypi, cli_upload


class PyPICommand(Command):
    '''
    setup.py command that uploads file or files (using GLOB-style mask) to the S3 bucket.
    '''

    user_options=[
        ('file-mask', None, 'GLOB-style mask to find files to transfer. Default is "dist/*"'),
        ('target', None, 'Output S3 url in the form "s3://bucket/prefix"'),
        ('force', None, 'Force file overwrite. Default is False'),
        ('aws-access-key-id', None, 'AWS access key id'),
        ('aws-secret-access-key', None, 'AWS secret access key'),
    ]

    def initialize_options(self):
        self.file_mask = 'dist/*'
        self.target = None
        self.force = False
        self.aws_access_key_id = None
        self.aws_secret_access_key = None

    def finalize_options(self):

        if self.file_mask is None:
            raise DistutilsOptionError('must provide valid "file-mask"')

        self.file_mask = [self.file_mask]

    def run(self):
        cli_pypi(self)


class UploadCommand(Command):
    '''
    Command that uploads file or files (using GLOB-style mask) to the S3 bucket.
    '''

    user_options=[
        ('file-mask', None, 'GLOB-style mask to find files to transfer, e.g. "~/dist/package*.zip".'),
        ('target', None, 'Output S3 url in the form "s3://bucket/prefix"'),
        ('acl', None, 'One of the AWS canned access policies. To make files publicly readable, use "public-read". Default is "private"'),
        ('force', None, 'Force file overwrite. Default is False'),
        ('aws-access-key-id', None, 'AWS access key id'),
        ('aws-secret-access-key', None, 'AWS secret access key'),
    ]

    def initialize_options(self):
        self.file_mask = None
        self.target = None
        self.acl = 'private'
        self.force = False
        self.aws_access_key_id = None
        self.aws_secret_access_key = None

    def finalize_options(self):

        if self.file_mask is None:
            raise DistutilsOptionError('must provide valid "file-mask"')

        if self.target is None:
            raise DistutilsOptionError('must provide "target" value')

        self.file_mask = [self.file_mask]

    def run(self):
        cli_upload(self)
