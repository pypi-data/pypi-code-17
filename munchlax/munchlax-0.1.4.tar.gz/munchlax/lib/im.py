from .object import Object

class IM(Object):
    """
    Represents a Slack IM channel.
    """
    def __init__(self, slack, im):
        Object.__init__(self, im)
        self._slack = slack
    
    async def close(self):
        """
        Closes the IM channel.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        return await self._slack.close_im(self)

    async def get_history(self, latest='now', oldest=0, inclusive=True, count=100):
        """
        Fetches and returns the message history for the IM.

        Args:
            latest (float | ``now``): The end of time range of messages to include.
                This can be a float or ``now`` If ``now`` is specified then the current
                time is used.
                Defaults to ``now``.
            oldest (float): The start of time range of messages to include.
                Defaults to 0.
            inclusive (bool): Whether or not to include messages with latest of
                oldest timestamps.
                Defaults to True.
            count (int): The number of messages to return, between 1 and 1000.
                Defaults to 100.

        Returns:
            list (Message): A list of ``Message`` objects.
            bool: Whether or not there are more messages in the IM's history.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        return await self._slack.get_im_history(
            self,
            latest=latest,
            oldest=oldest,
            inclusive=inclusive,
            count=count
        )

    async def mark(self, ts):
        """
        Changes the last-read indicator in the IM for the current user.

        Args:
            ts (float): The timestamp to use when changing the
                last-read indicator.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        self._slack.mark_im(self, ts)

    async def get_replies(self, ts):
        """
        Fetches and returns all replies to a message within the IM.

        Args:
            ts: The timestamp of the parent message to look for.

        Returns:
            list (Message):
                A list of ``Message`` objects representing a message thread.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        return await self._slack.get_im_replies(self, ts)