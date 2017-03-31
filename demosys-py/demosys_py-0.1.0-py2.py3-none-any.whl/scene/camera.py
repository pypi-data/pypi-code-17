import glfw
from pyrr import matrix44, vector3, vector, Vector3

# Direction Definitions
RIGHT = 1
LEFT = 2
FORWARD = 3
BACKWARD = 4
UP = 5
DOWN = 6

# Movement Definitions
STILL = 0
POSITIVE = 1
NEGATIVE = 2


class Camera:
    """Simple camera class containing projection"""
    def __init__(self, fov=60, aspect=1.0, near=1, far=100):
        """
        Initialize camera using a specific projeciton
        :param fov: Field of view
        :param aspect: Aspect ratio
        :param near: Near plane
        :param far: Far plane
        """
        self.cam_pos = Vector3([0.0, 0.0, 5.0])
        # Default camera placement
        self.cam_up = Vector3([0.0, 1.0, 0.0])
        self.cam_right = Vector3([1.0, 0.0, 0.0])
        self.cam_dir = Vector3([0.0, 0.0, -1.0])
        # Yaw and Pitch
        self.yaw = 0
        self.pitch = 0

        # World up vector
        self._up = Vector3([0.0, 1.0, 0.0])
        # Position movement states
        self._xdir = STILL
        self._zdir = STILL
        self._ydir = STILL
        self._last_time = 0
        # Velocity in axis units per second
        self.velocity = 10.0

        # Projection attributes
        self.projection = None
        self.fov = fov
        self.aspect = aspect
        self.near = near
        self.far = far
        self.set_projection()

    def set_position(self, x, y, z):
        self.cam_pos = Vector3([x, y, z])

    def move_state(self, direction, activate):
        """
        Set the camera position move state
        :param direction: What direction to update
        :param activate: Start or stop moving in the direction
        """
        if direction == RIGHT:
            self._xdir = POSITIVE if activate else STILL
        elif direction == LEFT:
            self._xdir = NEGATIVE if activate else STILL
        elif direction == FORWARD:
            self._zdir = NEGATIVE if activate else STILL
        elif direction == BACKWARD:
            self._zdir = POSITIVE if activate else STILL
        elif direction == UP:
            self._ydir = POSITIVE if activate else STILL
        elif direction == DOWN:
            self._ydir = NEGATIVE if activate else STILL

    # def rot_state(self, ):

    @property
    def view_matrix(self):
        # Use separate time in camera so we can move it when the demo is paused
        time = glfw.get_time()
        # If the camera has been inactive for a while, a large time delta
        # can suddenly move the camera far away from the scene
        t = max(time - self._last_time, 0)
        self._last_time = time

        # X Movement
        if self._xdir == POSITIVE:
            self.cam_pos += self.cam_right * self.velocity * t
        elif self._xdir == NEGATIVE:
            self.cam_pos -= self.cam_right * self.velocity * t
        # Z Movement
        if self._zdir == NEGATIVE:
            self.cam_pos += self.cam_dir * self.velocity * t
        elif self._zdir == POSITIVE:
            self.cam_pos -= self.cam_dir * self.velocity * t
        # Y Movement
        if self._ydir == POSITIVE:
            self.cam_pos += self.cam_up * self.velocity * t
        elif self._ydir == NEGATIVE:
            self.cam_pos -= self.cam_up * self.velocity * t

        return self._gl_look_at(self.cam_pos, self.cam_pos + self.cam_dir, self._up)

    def set_projection(self, fov=None, aspect=None, near=None, far=None):
        """
        Update projection parameters and return the new version
        :param fov: Field of view
        :param aspect: Aspect ratio
        :param near: Near plane
        :param far: Far plane
        :return: Projection matrix
        """
        self.fov = fov or self.fov
        self.near = near or self.near
        self.far = far or self.far
        self.aspect = aspect or self.aspect
        self.projection = matrix44.create_perspective_projection_matrix(
            self.fov, self.aspect, self.near, self.far)
        return self.projection

    def look_at(self, vec=None, pos=None):
        """
        Look at a specific point
        :param vec: Vector3 position
        :param pos: python list [x, y, x]
        :return: Camera matrix
        """
        if pos:
            vec = Vector3(pos)
        if vec is None:
            raise ValueError("vector or pos must be set")
        return self._gl_look_at(self.cam_pos, vec, self._up)

    def _gl_look_at(self, pos, target, up):
        """
        The standard lookAt method
        :param pos: current position
        :param target: target position to look at
        :param up: direction up
        """
        z = vector.normalise(pos - target)
        x = vector.normalise(vector3.cross(vector.normalise(up), z))
        y = vector3.cross(z, x)

        translate = matrix44.create_identity()
        translate[3][0] = -pos.x
        translate[3][1] = -pos.y
        translate[3][2] = -pos.z

        rotate = matrix44.create_identity()
        rotate[0][0] = x[0]  # -- X
        rotate[1][0] = x[1]
        rotate[2][0] = x[2]
        rotate[0][1] = y[0]  # -- Y
        rotate[1][1] = y[1]
        rotate[2][1] = y[2]
        rotate[0][2] = z[0]  # -- Z
        rotate[1][2] = z[1]
        rotate[2][2] = z[2]

        # return matrix44.multiply(rotate, translate)
        return matrix44.multiply(translate, rotate)
