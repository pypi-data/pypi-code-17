from OpenGL import GL
from demosys.opengl import Texture

# Reference to the window
WINDOW = None


class WindowFBO:
    """Fake FBO representing default render target"""
    def __init__(self):
        self.window = WINDOW
        self.color_buffers = []
        self.color_buffers_ids = []
        self.depth_buffer = None

    def bind(self):
        GL.glViewport(0, 0, WINDOW.buffer_width, WINDOW.buffer_height)

    def release(self):
        pass

    def clear(self):
        pass


WINDOW_FBO = WindowFBO()


class FBO:
    """Frame buffer object"""
    def __init__(self):
        self.color_buffers = []
        self.color_buffers_ids = []
        self.depth_buffer = None
        self.fbo = GL.glGenFramebuffers(1)

    def bind(self, stack=True):
        """Bind FBO adding it to the stack"""
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self.fbo)
        if not stack:
            return

        push_fbo(self)
        if len(self.color_buffers) > 1:
            GL.glDrawBuffers(len(self.color_buffers), self.color_buffers_ids)
        w, h = self.size
        GL.glViewport(0, 0, w, h)

    def release(self, stack=True):
        """
        Bind FBO popping it from the stack
        :param stack: Should the bind be registered in the stack?
        """
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        if not stack:
            return

        parent = pop_fbo(self)
        if parent:
            parent.bind()

    def clear(self):
        self.bind(stack=False)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT | GL.GL_STENCIL_BUFFER_BIT)
        self.release(stack=False)

    @property
    def size(self):
        if self.color_buffers:
            return self.color_buffers[0].size
        if self.depth_buffer:
            return self.depth_buffer.size
        raise FBOError("Cannot determine size of FBO. No attachments.")

    @classmethod
    def create(cls, width, height, depth=False, stencil=True,
               internal_format=GL.GL_RGBA8, format=GL.GL_RGBA, type=GL.GL_UNSIGNED_BYTE):
        """Convenient shortcut for creating single color attachment FBOs"""
        fbo = FBO()
        fbo.bind(stack=False)
        c = Texture.create_2d(width, height, internal_format=internal_format, format=format, type=type)
        fbo.add_color_attachment(c)
        if depth:
            d = Texture.create_2d(width, height, internal_format=GL.GL_DEPTH24_STENCIL8,
                                  format=GL.GL_DEPTH_COMPONENT)
            fbo.set_depth_attachment(d)
        fbo.check_status()
        fbo.release(stack=False)
        return fbo

    def add_color_attachment(self, texture):
        # Internal states
        self.color_buffers_ids.append(GL.GL_COLOR_ATTACHMENT0 + len(self.color_buffers))
        self.color_buffers.append(texture)
        # Attach to fbo
        GL.glFramebufferTexture2D(
            GL.GL_FRAMEBUFFER,
            self.color_buffers_ids[-1],
            GL.GL_TEXTURE_2D,
            self.color_buffers[-1].texture,
            0
        )

    def set_depth_attachment(self, texture):
        self.depth_buffer = texture
        # Attach to fbo
        GL.glFramebufferTexture2D(
            GL.GL_FRAMEBUFFER,
            GL.GL_DEPTH_ATTACHMENT,
            GL.GL_TEXTURE_2D,
            self.depth_buffer.texture,
            0
        )

    def check_status(self):
        """Checks the completeness of the FBO"""
        status = GL.glCheckFramebufferStatus(GL.GL_FRAMEBUFFER)
        incomplete_states = {
            GL.GL_FRAMEBUFFER_UNSUPPORTED: "Framebuffer unsupported. Try another format.",
            GL.GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT: "Framebuffer incomplete attachment",
            GL.GL_FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT: "Framebuffer missing attachment",
            GL.GL_FRAMEBUFFER_INCOMPLETE_DIMENSIONS: "Framebuffer unsupported dimension.",
            GL.GL_FRAMEBUFFER_INCOMPLETE_FORMATS: "Framebuffer incoplete formats.",
            GL.GL_FRAMEBUFFER_INCOMPLETE_DRAW_BUFFER: "Framebuffer incomplete draw buffer.",
            GL.GL_FRAMEBUFFER_INCOMPLETE_READ_BUFFER: "Framebuffer incomplete read buffer",
        }
        if status == GL.GL_FRAMEBUFFER_COMPLETE:
            return
        s = incomplete_states.get(status, "Unknown error")
        raise FBOError(s)

    def __repr__(self):
        return "<FBO {} color_attachments={} depth_attachement={}".format(
            self.fbo,
            self.color_buffers,
            self.depth_buffer,
        )


# Internal FBO bind stack so we can support hierarchical binding
FBO_STACK = []


def push_fbo(fbo):
    """Push fbo into the stack"""
    global FBO_STACK
    FBO_STACK.append(fbo)
    if len(FBO_STACK) > 8:
        raise FBOError("FBO stack overflow. You probably forgot to release a bind somewhere.")


def pop_fbo(fbo):
    """
    Pops the fbo out of the stack
    Returns: The last last fbo in the stack
    """
    global FBO_STACK
    if not FBO_STACK:
        raise FBOError("FBO stack is already empty. You are probably releasing a FBO twice or forgot to bind.")
    fbo_out = FBO_STACK.pop()
    if fbo_out != fbo:
        raise FBOError("Incorrect FBO release order")
    if FBO_STACK:
        return FBO_STACK[-1]
    return WINDOW_FBO


class FBOError(Exception):
    pass
