from .object import Object

class Comment(Object):
    """
    Represents a Slack file comment.
    """
    def __init__(self, slack, comment, file):
        Object.__init__(self, comment)
        self._slack = slack
        self._file = file

    async def delete(self):
        """
        Deletes the file comment.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        return await self._slack.delete_comment(self._file, self)

    async def edit(self, comment):
        """
        Edits the comment's text to be ``comment``.

        Args:
            comment (str): The new text string to use for the comment.

        Returns:
            Comment: An updated version of the comment.
        
        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        return await self._slack.edit_comment(self._file, self, comment)