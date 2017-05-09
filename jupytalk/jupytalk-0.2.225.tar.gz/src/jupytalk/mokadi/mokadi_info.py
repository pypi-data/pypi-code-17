"""
@file
@brief Defines results for mokadi.
"""
import os


class MokadiInfo:
    """
    Defines results for Mokadi.
    """

    _allowed_status = {"error", "ok", "empty"}

    def __init__(self, status: str, info="", error="", image=None, sound=None, url=None):
        """
        Constructor

        @param      status          message (string)
        @param      info            text to display
        @param      error           error message
        @param      image           image name
        @param      sound           sound
        @param      url             one URL
        """
        self._status = status
        self._info = info
        self._error = error
        self._image = image
        self._sound = sound
        self._url = url

        if not isinstance(status, str):
            raise TypeError("status must be a string")
        if not isinstance(info, str):
            raise TypeError("info must be a string")
        if not isinstance(error, str):
            raise TypeError("error must be a string")
        if status not in MokadiInfo._allowed_status:
            raise ValueError("status must be in {0}".format(
                MokadiInfo._allowed_status))
        if image is not None and len(image) > 0:
            if not image.startswith("http") and not os.path.exists(image):
                raise FileNotFoundError(image)
        if sound is not None and len(sound) > 0:
            if not os.path.exists(sound):
                raise FileNotFoundError(sound)

    @property
    def has_sound(self):
        """
        Tells if there is sound.
        """
        return hasattr(self, "_sound") and self._sound is not None

    @property
    def has_image(self):
        """
        Tells if there is an image.
        """
        return hasattr(self, "_image") and self._image is not None

    @property
    def has_url(self):
        """
        Tells if there is an image.
        """
        return hasattr(self, "_url") and self._url is not None

    @property
    def Url(self):
        """retrieve the url"""
        return self._url

    @property
    def image(self):
        """retrieve the image"""
        return self._image

    @property
    def sound(self):
        """retrieve the sound"""
        return self._sound

    def __str__(self):
        """
        message to string
        """
        if self._error:
            return "%s - %s" % (self._status, self._error)
        else:
            return "%s - %s" % (self._status, self._info)

    def __repr__(self):
        """
        message to string
        """
        return "MokadiInfo('%s', '%s', '%s')" % (self._status, self._info.replace("'", "\\'"), self._error.replace("'", "\\'"))

    def _repr_html_(self):
        """
        for notebooks
        """
        if self._status == "ok":
            if self._image:
                return "<i>%s</i><br /><img src=\"%s\" />" % (self._info, self._image)
            else:
                return "<i>%s</i>" % self._info
        else:
            return "<b>%s<b> <i>%s</i>" % (self._status, self._info)

    @property
    def info(self):
        """
        property
        """
        return self._info

    @property
    def error(self):
        """
        property
        """
        return self._error

    @property
    def status(self):
        """
        property
        """
        return self._status
