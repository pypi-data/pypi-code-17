from abc import abstractmethod

from oe_utils.email.smtp import SMTPClient


class Notifier(object):

    def __init__(self, settings, logger):
        self.settings = settings
        self.logger = logger
        self.email_client = SMTPClient(
            self.settings.get('daemon.email.smtp'),
            self.settings.get('daemon.email.sender')
        )

    @abstractmethod
    def notify(self):
        """
        abstract method to notify by sending emails

        """
        pass
