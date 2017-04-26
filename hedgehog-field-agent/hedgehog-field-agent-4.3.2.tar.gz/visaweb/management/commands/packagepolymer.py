import os
from distutils.file_util import copy_file

from django.core.management.base import BaseCommand, CommandError, AppCommand
from shutil import rmtree

from subprocess import call, Popen, PIPE

from visaweb.version import __version__ as frontend_version
from distutils.dir_util import copy_tree


class Command(AppCommand):
    help = 'Package polymer application to the Visaweb module.'
    label = 'visaweb'
    requires_system_checks = False
    # Can't import settings during this command, because they haven't
    # necessarily been created.
    can_import_settings = True

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--uiversion',
            dest='polymer_version',
            default='1.0.0',
            help='Version of new UI.')
        parser.add_argument(
            '--dir',
            dest='build_directory',
            default=None,
            help='Project build directory.',
            type=str)

        # Named (optional) arguments
        parser.add_argument(
            '--http2',
            action='store_true',
            dest='http2',
            default=False,
            help='HTTP2 push content compatibility flag.',
        )

    def handle_app_config(self, app, **options):
        version = options['polymer_version']
        http2 = options['http2']
        build_directory = options['build_directory']
        old_version = frontend_version
        try:
            import visaweb

            commands = "cd " + os.path.dirname(visaweb.__file__) + " && " + "polymer build"
            process = Popen('/bin/bash', stdin=PIPE, stdout=PIPE, shell=True)
            out, err = process.communicate(commands)
            try:

                print(out)

                try:
                    call(["polymer-build", "-l"])
                except:
                    pass

                self.stdout.write(self.style.SUCCESS('polymer built'))

                static_files = os.path.join(os.path.dirname(visaweb.__file__), 'static/visaweb')



                if build_directory is None:
                    build_directory = os.path.dirname(visaweb.__file__)



                working_directory = os.path.join(build_directory,
                                                 'build' + '/' + str('unbundled' if http2 else "bundled"))

                rmtree(static_files)

                self.stdout.write(self.style.SUCCESS('package from "%s" to "%s"' % (working_directory, static_files)))
                results = copy_tree(working_directory, static_files, update=True, verbose=True)
                for file in results:
                    print (file)

                self.stdout.write(self.style.SUCCESS('upgrade from "%s" -> "%s"' % (version, old_version)))
            except Exception:
                print(err)
                pass




        except Exception as ex:
            raise CommandError('polymer packaging failed: "%s"' % str(ex.message))


