# noqa
from dodo_commands.extra.standard_commands import DodoCommand, CommandError
from plumbum.cmd import docker


class Command(DodoCommand):  # noqa
    help = ""
    decorators = []

    def add_arguments_imp(self, parser):  # noqa
        parser.add_argument('--playbook')
        parser.add_argument('--input-image')

    def handle_imp(self, playbook, input_image, **kwargs):  # noqa
        playbook = playbook or self.get_config("/ANSIBLE/default_playbook")
        input_image_name = input_image or self.get_config("/DOCKER/image")
        output_image_name = self.get_config("/DOCKER/image")
        existing_image = docker("images", "-a", "--quiet", input_image_name)
        if not existing_image:
            raise CommandError("Cannot find image %s" % input_image_name)

        ansible_dir = self.get_config("/ANSIBLE/src_dir")
        remote_ansible_dir = "/root/ansible/"

        self.runcmd(
            [
                "docker",
                "run",
                "-w", remote_ansible_dir,
                "--volume=%s:%s" % (ansible_dir, remote_ansible_dir),
                input_image_name,
                "/bin/bash", "-c", "ansible-playbook -i hosts -l localhost %s" % playbook
            ]
        )
        container_id = docker("ps", "-l", "-q")[:-1]

        self.runcmd(["docker", "commit", container_id, output_image_name])
        self.runcmd(["docker", "rm", container_id])
