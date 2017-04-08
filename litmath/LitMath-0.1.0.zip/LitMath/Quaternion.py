import math
import Util

class Quaternion(object):
    __slots__ = ['x', 'y', 'z', 'w']
    __hash__ = None
    
    def __init__(self, x=0.0, y=0.0, z=0.0, w=1.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.w = float(w)
        
    def set(self, x, y, z, w):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.w = float(w)
        return self
        
    def copy(self):
        import copy
        return copy.copy(self)
    
    def __repr__(self):
        return 'Quaternion( %.2f, %.2f, %.2f, %.2f )' % \
               (self.x, self.y, self.z, self.w)
               
    def __eq__(self, other):
        if isinstance(other, Quaternion):
            return Util.isEqual(self.x, other.x) and \
                   Util.isEqual(self.y, other.y) and \
                   Util.isEqual(self.z, other.z) and \
                   Util.isEqual(self.w, other.w)
        else:
            return False
            
    def __ne__(self, other):
        return not self.__eq__(other)
    
    @property    
    def magnitude(self):
        return math.sqrt(self.x ** 2 +
                         self.y ** 2 +
                         self.z ** 2 +
                         self.w ** 2)
            
    def normalize(self):
        len = self.magnitude
        if len != 0:
            self.x /= len
            self.y /= len
            self.z /= len
            self.w /= len   
        return self
    
    @property
    def normalized(self):
        len = self.magnitude
        if len == 0:
            return self.copy()
        else:
            return Quaternion(self.x / len, self.y / len, self.z / len, self.w / len)
            
    def invert(self):
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z
        return self
    
    @property    
    def inverse(self):
        return Quaternion(-self.x, -self.y, -self.z, self.w)
               
    def __mul__(self, other):
        '''Multiplies two quaternions.'''
        assert isinstance(other, Quaternion)
        return Quaternion(
            self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y,
            self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x,
            self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w,
            self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z)
            
    def multiplyPoint(self, pnt):
        '''Rotates the point pnt by this quaternion.'''
        import Vector3
        assert isinstance(pnt, Vector3.Vector3)
        
        x = self.x
        y = self.y
        z = self.z
        w = self.w
        x2 = self.x * self.x
        y2 = self.y * self.y
        z2 = self.z * self.z
        w2 = self.w * self.w
        
        dx = (x2+w2-y2-z2)*pnt.x + 2.0*(x*y-z*w)*pnt.y + 2.0*(x*z+y*w)*pnt.z
        dy = 2.0*(x*y+z*w)*pnt.x + (w2-x2+y2-z2)*pnt.y + 2.0*(y*z-x*w)*pnt.z
        dz = 2.0*(x*z-y*w)*pnt.x + 2.0*(x*w+y*z)*pnt.y + (w2-x2-y2+z2)*pnt.z
        
        return Vector3.Vector3(dx, dy, dz)
        
    def toMatrix4(self):
        '''Converts a rotation to 4x4 matrix.'''
        # reference:FreeCAD Rotation.cpp
        x = self.x
        y = self.y
        z = self.z
        w = self.w
        
        import Matrix4
        matrix = Matrix4.Matrix4()
        matrix.m11 = 1.0-2.0*(y*y+z*z)
        matrix.m12 = 2.0*(x*y-z*w)
        matrix.m13 = 2.0*(x*z+y*w)
        matrix.m14 = 0.0
    
        matrix.m21 = 2.0*(x*y+z*w)
        matrix.m22 = 1.0-2.0*(x*x+z*z)
        matrix.m23 = 2.0*(y*z-x*w)
        matrix.m24 = 0.0
    
        matrix.m31 = 2.0*(x*z-y*w)
        matrix.m32 = 2.0*(y*z+x*w)
        matrix.m33 = 1.0-2.0*(x*x+y*y)
        matrix.m34 = 0.0
    
        matrix.m41 = 0.0
        matrix.m42 = 0.0
        matrix.m43 = 0.0
        matrix.m44 = 1.0
        
        return matrix
        
    def toAxisAngle(self):
        '''Converts a rotation to axis-angle representation(angle in degree).'''
        axis, angle = self.toAxisAngleInRadian()
        return axis, Util.radianToDegree(angle)
        
    def toAxisAngleInRadian(self):
        '''Converts a rotation to axis-angle representation(angle in radian).'''
        import Vector3
        # reference:FreeCAD Rotation.cpp
        if self.w > -1.0 and self.w < 1.0:
            t = math.acos(self.w)
            scale = math.sin(t)
            if Util.isEqualZero(scale):
                return Vector3.Vector3(0,0,1), 0.0
            else:
                axis = Vector3.Vector3(self.x / scale, self.y / scale, self.z / scale)
                return axis, 2*t
        else:
            return Vector3.Vector3(0,0,1), 0.0
        
    def setIdentity(self):
        self.set(0.0, 0.0, 0.0, 1.0)
        return self
        
    @staticmethod
    def identity():
        '''Returns the identity quaternion.'''
        return Quaternion(0.0, 0.0, 0.0, 1.0)
        
    @staticmethod
    def matrix4(matrix):
        import Matrix4
        assert isinstance(matrix, Matrix4.Matrix4)

        quat = Quaternion()
        M = matrix
        trace = M.m11 + M.m22 + M.m33

        if trace > 0:
            s = 0.5 / math.sqrt(trace + 1.0)
            quat.w = 0.25 / s
            quat.x = (M.m32 - M.m23 ) * s
            quat.y = (M.m13 - M.m31 ) * s
            quat.z = (M.m21 - M.m12 ) * s
        elif M.m11 > M.m22 and M.m11 > M.m33:
            s = 2.0 * math.sqrt(1.0 + M.m11 - M.m22 - M.m33)
            quat.w = (M.m32 - M.m23) / s
            quat.x = 0.25 * s
            quat.y = (M.m12 + M.m21) / s
            quat.z = (M.m13 + M.m31) / s
        elif M.m22 > M.m33:
            s = 2.0 * math.sqrt(1.0 + M.m22 - M.m11 - M.m33)
            quat.w = (M.m13 - M.m31) / s
            quat.x = (M.m12 + M.m21) / s
            quat.y = 0.25 * s;
            quat.z = (M.m23 + M.m32) / s
        else:
            s = 2.0 * math.sqrt(1.0 + M.m33 - M.m11 - M.m22)
            quat.w = (M.m21 - M.m12) / s
            quat.x = (M.m13 + M.m31) / s
            quat.y = (M.m23 + M.m32) / s
            quat.z = 0.25 * s
            
        return quat
        
    @staticmethod
    def axisAngle(axis, angle):
        '''Creates a rotation which rotates angle degrees around axis.'''
        return Quaternion.axisAngleInRadian(axis, Util.degreeToRadian(angle))
        
    @staticmethod
    def axisAngleInRadian(axis, angle):
        '''Creates a rotation which rotates angle degrees around axis.'''
        import Vector3
        assert isinstance(axis, Vector3.Vector3) and \
               type(angle) in (int, long, float)
        
        axis = axis.normalized
        scale = math.sin(angle / 2)
        
        quat = Quaternion()
        quat.w = math.cos(angle / 2)
        quat.x = axis.x * scale
        quat.y = axis.y * scale
        quat.z = axis.z * scale
        
        return quat
        
    @staticmethod
    def fromToRotation(f, to):
        '''Creates a rotation which rotates from from(Vector) to to(Vector).'''
        from Vector3 import Vector3
        assert isinstance(f, Vector3) and isinstance(to, Vector3)
        
        # reference:FreeCAD Rotation.cpp
        u = f.normalized
        v = to.normalized
        dot = Vector3.dot(u, v)
        w = Vector3.cross(u, v)
        
        # parallel vectors
        if w.length == 0:
            # same direction
            if dot >= 0:
                return Quaternion(0.0, 0.0, 0.0, 1.0)
            else:
                t = Vector3.cross(u, Vector3(1.0, 0.0, 0.0))
                if Util.isEqualZero(t.length):
                    t = Vector3.cross(u, Vector3(0.0, 1.0, 0.0))
                return Quaternion(t.x, t.y, t.z, 0.0)
        else:
            angleInRad = math.acos(dot)
            return Quaternion.axisAngleInRadian(w, angleInRad)