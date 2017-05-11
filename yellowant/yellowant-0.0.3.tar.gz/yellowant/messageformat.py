import json


class MessageClass(object):
    def __init__(self, message_text="", description=" ", title=" ", image_url=" "):
        self._message_text = message_text
        self._description = description
        self._title = title
        self._image_url = image_url
        self._attachments = []

    @property
    def message_text(self):
        return self._message_text

    @property
    def description(self):
        return self._description

    @property
    def title(self):
        return self._title

    @property
    def image_url(self):
        return self._image_url

    @message_text.setter
    def message_text(self, message_text):
        self._message_text = message_text

    @description.setter
    def description(self, description):
        self._description = description

    @title.setter
    def title(self, title):
        self._title = title

    @image_url.setter
    def image_url(self, image_url):
        self._image_url = image_url

    def __repr__(self):
        to_dict = {"message_text": self._message_text, "description": self._description,
                   "title": self._title, "image_url": self._image_url}
        return json.dumps(to_dict)

    def attach(self, attachment):
        """ Checks if attachment is of valid class (MessageAttachmentsClass) and adds
		corresponding attachment if not raises TypeError """
        if not isinstance(attachment, MessageAttachmentsClass):
            raise TypeError("Attachment must be MessageAttachmentsClass() object")
        else:
            self._attachments.append(attachment.get_dict())

    def to_json(self, **kwargs):
        """ Returns object in json format with optional kwargs. **kwargs are passed as is to
		json object kwargs. If kwargs are not provided it defaults to "sort_keys=True, indent=4, separators=(",", ": ")"
		For unsorted pass, sort_keys=False """
        message = {"attachments": self._attachments,
                   "message_text": self._message_text,
                   "description": self._description,
                   "title": self._title,
                   "image_url": self._image_url}
        if kwargs == {}:
            return json.dumps(message, sort_keys=True, indent=4, separators=(",", ": "))
        else:
            return json.dumps(message, **kwargs)


class MessageAttachmentsClass(object):
    """Class Description"""

    def __init__(self, image_url="", thumbnail_url="", color="", text="",
                 author_name="", author_icon="", footer="", footer_icon="",
                 pre_text="", title="", title_link="", status=0):

        self._image_url = image_url
        self._thumbnail_url = thumbnail_url
        self._color = color
        self._text = text
        self._author_name = author_name
        self._author_icon = author_icon
        self._footer = footer
        self._footer_icon = footer_icon
        self._pre_text = pre_text
        self._title = title
        self._title_link = title_link
        self._fields = []
        self._buttons = []
        if isinstance(status, int):
            self._status = status
        else:
            raise TypeError("Status must be an integer")

    @property
    def image_url(self):
        return self._image_url

    @property
    def thumbnail_url(self):
        return self._thumbnail_url

    @property
    def color(self):
        return self._color

    @property
    def text(self):
        return self._text

    @property
    def author_icon(self):
        return self._author_icon

    @property
    def author_name(self):
        return self._author_name

    @property
    def footer(self):
        return self._footer

    @property
    def footer_icon(self):
        return self._footer_icon

    @property
    def pre_text(self):
        return self._pre_text

    @property
    def title(self):
        return self._title

    @property
    def title_link(self):
        return self._title_link

    @property
    def status(self):
        return self._status

    @image_url.setter
    def image_url(self, image_url):
        self._image_url = image_url

    @thumbnail_url.setter
    def thumbnail_url(self, thumbnail_url):
        self._thumbnail_url = thumbnail_url

    @color.setter
    def color(self, color):
        self._color = color

    @text.setter
    def text(self, text):
        self._text = text

    @author_name.setter
    def author_name(self, author_name):
        self._author_name = author_name

    @author_icon.setter
    def author_icon(self, author_icon):
        self._author_icon = author_icon

    @footer.setter
    def footer(self, footer):
        self._footer = footer

    @footer_icon.setter
    def footer_icon(self, footer_icon):
        self._footer_icon = footer_icon

    @pre_text.setter
    def pre_text(self, pre_text):
        self._pre_text = pre_text

    @title.setter
    def title(self, title):
        self._title = title

    @title_link.setter
    def title_link(self, title_link):
        self._title_link = title_link

    @status.setter
    def status(self, status):
        if isinstance(status, int):
            self._status = status
        else:
            raise TypeError("Status must be an integer")

    def __repr__(self):
        _to_dict = {"image_url": self._image_url, "thumbnail_url": self._thumbnail_url, "color": self._color,
                    "text": self._text, "author_name": self._author_name, "author_icon": self.author_icon,
                    "footer": self._footer, "footer_icon": self._footer_icon, "pre_text": self._pre_text,
                    "title": self._title, "title_link": self._title_link, "status": self._status,
                    "fields": self._fields, "buttons": self._buttons}
        return json.dumps(_to_dict)

    def attach_field(self, attachment_field):
        """Checks if passed arg is of class AttachmentFieldsClass, if not raises TypeError else adds Field
		"""
        if not isinstance(attachment_field, AttachmentFieldsClass):
            raise TypeError("Field should be an AttachmentFieldsClass object")
        else:
            self._fields.append(attachment_field.get_dict())

    def attach_button(self, button_field):
        """Checks if passed arg is of class MessageButtonsClass, if not raises TypeError else adds button """
        if not isinstance(button_field, MessageButtonsClass):
            raise TypeError("Button should be an MessageButtonsClass object")
        else:
            self._buttons.append(button_field.get_dict())

    def get_dict(self):
        """Returns MessageAttachmentsClass object as dictionary object"""
        return {"image_url": self._image_url, "thumbnail_url": self._thumbnail_url, "color": self._color,
                "text": self._text, "author_name": self._author_name, "author_icon": self.author_icon,
                "footer": self._footer, "footer_icon": self._footer_icon, "pre_text": self._pre_text,
                "title": self._title, "title_link": self._title_link, "status": self._status,
                "fields": self._fields, "buttons": self._buttons}


class AttachmentFieldsClass(object):
    def __init__(self, title="", short=0, value=""):
        self._title = title
        if isinstance(short, int):
            self._short = short
        else:
            raise TypeError("Short must be an integer")
        self.value = value

    @property
    def title(self):
        return self._title

    @property
    def short(self):
        return self._short

    @property
    def value(self):
        return self._value

    @title.setter
    def title(self, title):
        self._title = title

    @short.setter
    def short(self, short):
        if isinstance(short, int):
            self._short = short
        else:
            raise TypeError("Short must be an integer")

    @value.setter
    def value(self, value):
        self._value = value

    def __repr__(self):
        to_dict = {"title": self._title, "short": self._short, "value": self._value}
        return json.dumps(to_dict)

    def get_dict(self):
        """Returns AttachmentFieldsClass object as dictionary object"""
        return {"title": self._title, "short": self._short, "value": self._value}


class MessageButtonsClass(object):
    def __init__(self, value="", name="", text="", command={}):
        self._value = value
        self._name = name
        self._text = text
        self._command = command

    @property
    def value(self):
        return self._value

    @property
    def name(self):
        return self._name

    @property
    def text(self):
        return self._text

    @property
    def command(self):
        return self._command

    @value.setter
    def value(self, value):
        self._value = value

    @name.setter
    def name(self, name):
        self._name = name

    @text.setter
    def text(self, text):
        self._text = text

    @command.setter
    def command(self, command):
        self._command = command

    def __repr__(self):
        to_dict = {"value": self._value, "name": self._name,
                   "text": self._text, "command": self._command}
        return json.dumps(to_dict)

    def get_dict(self):
        """Returns MessageButtonsClass object as dictionary object"""
        return {"value": self._value, "name": self._name,
                "text": self._text, "command": self._command}
