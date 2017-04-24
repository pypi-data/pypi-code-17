import os
import json
import shutil
import shlex
import subprocess
import argparse
from .tzogitlab import TZOGitLab


def main():
    parser = argparse.ArgumentParser(description='Create a new SilverStripe website.')
    parser.add_argument('repo_name', type=str, help='The repo name of the website.')
    repo_name = parser.parse_args().repo_name
    installer = SilverStripeInstaller(repo_name)
    installer.create_site()


class SilverStripeInstaller:
    def __init__(self, repo):
        self.repo = repo
        self.path = os.path.abspath(repo).replace('\\', '\\\\')
        self.gitlab_ssh_url = None
        self.description = input(
            'Enter the project description(it will appear in your composer.json file):'
        )
        self.database_user = input('Please input the username of your database:')
        self.database_password = input('Please input the password of your database, press enter if no password:')
        self.your_domain = input('Please input the domain of your LOCAL DEVELOPMENT'
                                 ' site without "http://" (e.g. new-site.dev).')
        self.locale = input('Please input the website locale(e.g. en_US):')
        self.gitlab_token = self.get_gitlab_token()

    @staticmethod
    def run_command(command):
        args = shlex.split(command)
        subprocess.run(args, shell=True)

    @staticmethod
    def get_gitlab_token():
        credential_path = os.path.join(os.path.expanduser('~'), '.tzo_credentials')
        input_message = 'Please input your GitLab private token ' \
                        '(it can be found by clicking Settings->Account):'
        try:
            with open(credential_path, 'r+') as fh:
                tzo_credentials = json.load(fh)
                token = tzo_credentials['gitlab_token']
        except FileNotFoundError:
            token = input(input_message)
            with open(credential_path, 'w') as fh:
                json.dump({'gitlab_token': token}, fh, indent=4)
        except IndexError:
            token = input(input_message)
            with open(credential_path, 'r+') as fh:
                token_dict = {'gitlab_token': token}
                credentials_before = json.load(fh)
                credentials_after = token_dict if credentials_before is None else {**credentials_before, **token_dict}
                json.dump(credentials_after, fh, indent=4)
        return token

    def create_site(self):
        self.init_site()
        os.chdir(self.path)
        self.install_dependencies()
        self.alter_gitignore()
        self.gen_env_file()
        self.alter_config()
        self.add_theme()
        self.dev_build()
        self.create_gitlab_repo()
        print('Congratulations! Your site {repo} has been created successfully.'.format(repo=self.repo))

    def init_site(self):
        command = 'composer create-project silverstripe/installer {path}'.format(path=self.path)
        self.run_command(command)

    def install_dependencies(self):
        dependencies = {
            'timezoneone/silverstripe-essentials': 'dev-master',
            'silverstripe/googlesitemaps': None,
            'jonom/focuspoint': None,
            'silverstripe/redirectedurls': None,
            'silverstripe/userforms': None,
            'unclecheese/betterbuttons': None,
            'gdmedia/ss-auto-git-ignore': None,
            'silverstripe-australia/sitemap': None,
        }
        repos = {
            'timezoneone/silverstripe-essentials': 'git@git.timezoneone.com:timezoneone/silverstripe-essentials.git'
        }
        # Config repos
        for package, repo in repos.items():
            self.config_repo(package, repo)
        # Update composer json
        self.update_composer_json()
        # Install dependencies
        command = 'composer require'
        for package, version in dependencies.items():
            package_string = package if version is None else package + ':' + version
            command += ' ' + package_string
        self.run_command(command)

    def config_repo(self, package, repo, vcs_type='git'):
        command = 'composer config repositories.{package} {vcs_type} {repo}' \
            .format(package=package, repo=repo, vcs_type=vcs_type)
        self.run_command(command)

    def update_composer_json(self):
        with open('./composer.json', 'r+') as fh:
            composer_json = json.load(fh)
            # Add script for automatically generating gitignore file
            scripts_before = composer_json.get('scripts')
            gitignore_script = {'post-update-cmd': 'GDM\\SSAutoGitIgnore\\UpdateScript::Go'}
            scripts_after = gitignore_script if scripts_before is None \
                else {**scripts_before, **gitignore_script}
            composer_json['scripts'] = scripts_after
            # Add name and description info.
            composer_json['name'] = self.repo
            composer_json['description'] = self.description
            fh.seek(0)
            json.dump(composer_json, fh, indent=4)
            fh.truncate()

    @staticmethod
    def alter_gitignore():
        with open('./.gitignore', 'a+') as fh:
            addition = '\n# additional ignores\n' \
                       '/assets/*\n' \
                       '*.log\n' \
                       '**npm_modules\n'
            fh.write(addition)

    def gen_env_file(self):
        with open('./_ss_environment.php', 'w') as fh:
            _ss_environment = "<?php\n" \
                              "    define('SS_ENVIRONMENT_TYPE', 'dev');\n" \
                              "    define('SS_DATABASE_SERVER', 'localhost');\n" \
                              "    define('SS_DATABASE_USERNAME', '{database_user}');\n" \
                              "    define('SS_DATABASE_PASSWORD', '{database_password}');\n" \
                              "    define('SS_DATABASE_NAME', '{database_name}');\n" \
                              "    define('SS_DEFAULT_ADMIN_USERNAME', 'admin');\n" \
                              "    define('SS_DEFAULT_ADMIN_PASSWORD', 'admin');\n" \
                              "    define('TEMP_FOLDER', dirname(__FILE__) . '/silverstripe-cache');\n" \
                              "    global $_FILE_TO_URL_MAPPING;\n" \
                              "    $_FILE_TO_URL_MAPPING[dirname(__FILE__)] = 'http://{your_domain}';\n" \
                .format(
                database_user=self.database_user,
                database_password=self.database_password,
                database_name=self.repo,
                your_domain=self.your_domain
            )
            fh.write(_ss_environment)

    def alter_config(self):
        with open('./mysite/_config.php', 'r+') as fh:
            content = fh.read().replace('en_US', self.locale)
            fh.seek(0)
            fh.write(content)
            fh.truncate()
        with open('./mysite/_config/config.yml', 'r+') as fh:
            content = fh.read().replace('simple', self.repo)
            fh.seek(0)
            fh.write(content)
            fh.truncate()

    def add_theme(self):
        command = 'git clone git@git.timezoneone.com:timezoneone/silverstripe-theme-boilerplate.git themes/' \
                  + self.repo
        self.run_command(command)

        def handle_remove_readonly(func, path, exc_info):
            """
            Error handler for ``shutil.rmtree``.

            If the error is due to an access error (read only file)
            it attempts to add write permission and then retries.

            If the error is for another reason it re-raises the error.

            Usage : ``shutil.rmtree(path, onerror=onerror)``
            """
            import stat
            if not os.access(path, os.W_OK):
                # Is the error an access error ?
                os.chmod(path, stat.S_IWUSR)
                func(path)
        shutil.rmtree('./themes/{theme_folder}/.git'.format(theme_folder=self.repo),
                      ignore_errors=False, onerror=handle_remove_readonly)

    def dev_build(self):
        cache_path = './silverstripe-cache'
        if not os.path.exists(cache_path):
            os.mkdir(cache_path)
        self.run_command('chmod -R 777 ' + cache_path)
        self.run_command('./framework/sake dev/build "flush=all"')
        os.remove('./install.php')

    def create_gitlab_repo(self):
        gitlab = TZOGitLab(self.gitlab_token)
        gitlab_repo = gitlab.create_repo(self.repo)
        self.gitlab_ssh_url = gitlab_repo['ssh_url_to_repo']
        self.run_command('git init')
        self.run_command('git add .')
        self.run_command('git commit -m "Initial site setup."')
        self.run_command('git remote add origin ' + self.gitlab_ssh_url)
        self.run_command('git push --set-upstream origin master')
