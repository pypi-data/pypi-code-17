"""
@file
@brief Record a couple of seconds and returns the raw stream.
"""


def take_picture(filename=None, size=(640, 480), module="cv2"):
    """
    Take a picture with the camera.

    @param          filename        picture to save (if not None)
    @param          module          module to use (look at the code).
    @return                         image object

    We use the examples from
    `Capturing a single image from my webcam in Java or Python <http://stackoverflow.com/questions/11094481/capturing-a-single-image-from-my-webcam-in-java-or-python>`_.
    """

    if module == "pygame":
        import pygame
        import pygame.camera
        pygame.camera.init()
        # pygame.camera.list_camera()
        try:
            cam = pygame.camera.Camera(0, size, "RGB")
        except Exception as e:
            raise Exception(
                "Unable to change resolution into {0}".format(size)) from e
        cam.start()
        img = cam.get_image()
        if filename is not None:
            pygame.image.save(img, filename)
        return img
    elif module == "cv2":
        from cv2 import VideoCapture, imwrite
        # initialize the camera
        cam = VideoCapture(0)   # 0 -> index of camera
        s, img = cam.read()
        if filename is not None:
            imwrite(filename, img)
        return img
    else:
        raise ImportError("No module '{0}'".format(module))
