import math
import Util

class Matrix4(object):
    __slots__ = ['m11', 'm12', 'm13', 'm14',
                 'm21', 'm22', 'm23', 'm24',
                 'm31', 'm32', 'm33', 'm34',
                 'm41', 'm42', 'm43', 'm44']
    __hash__ = None
    
    def __init__(self, m11=1.0, m12=0.0, m13=0.0, m14=0.0,
                       m21=0.0, m22=1.0, m23=0.0, m24=0.0,
                       m31=0.0, m32=0.0, m33=1.0, m34=0.0,
                       m41=0.0, m42=0.0, m43=0.0, m44=1.0):
        self.m11 = float(m11)
        self.m12 = float(m12)
        self.m13 = float(m13)
        self.m14 = float(m14)
        self.m21 = float(m21)
        self.m22 = float(m22)
        self.m23 = float(m23)
        self.m24 = float(m24)
        self.m31 = float(m31)
        self.m32 = float(m32)
        self.m33 = float(m33)
        self.m34 = float(m34)
        self.m41 = float(m41)
        self.m42 = float(m42)
        self.m43 = float(m43)
        self.m44 = float(m44)
        
    def set(self, m11, m12, m13, m14,
                  m21, m22, m23, m24,
                  m31, m32, m33, m34,
                  m41, m42, m43, m44):
        self.m11 = float(m11)
        self.m12 = float(m12)
        self.m13 = float(m13)
        self.m14 = float(m14)
        self.m21 = float(m21)
        self.m22 = float(m22)
        self.m23 = float(m23)
        self.m24 = float(m24)
        self.m31 = float(m31)
        self.m32 = float(m32)
        self.m33 = float(m33)
        self.m34 = float(m34)
        self.m41 = float(m41)
        self.m42 = float(m42)
        self.m43 = float(m43)
        self.m44 = float(m44)
        return self
        
    def copy(self):
        import copy
        return copy.copy(self)
    
    def __repr__(self):
        return ('Matrix4(%8.2f %8.2f %8.2f %8.2f\n' \
                '        %8.2f %8.2f %8.2f %8.2f\n' \
                '        %8.2f %8.2f %8.2f %8.2f\n' \
                '        %8.2f %8.2f %8.2f %8.2f )') \
                % (self.m11, self.m12, self.m13, self.m14,
                   self.m21, self.m22, self.m23, self.m24,
                   self.m31, self.m32, self.m33, self.m34,
                   self.m41, self.m42, self.m43, self.m44)
                   
    def __eq__(self, other):
        if isinstance(other, Matrix4):
            return Util.isEqual(self.m11, other.m11) and \
                   Util.isEqual(self.m12, other.m12) and \
                   Util.isEqual(self.m13, other.m13) and \
                   Util.isEqual(self.m14, other.m14) and \
                   Util.isEqual(self.m21, other.m21) and \
                   Util.isEqual(self.m22, other.m22) and \
                   Util.isEqual(self.m23, other.m23) and \
                   Util.isEqual(self.m24, other.m24) and \
                   Util.isEqual(self.m31, other.m31) and \
                   Util.isEqual(self.m32, other.m32) and \
                   Util.isEqual(self.m33, other.m33) and \
                   Util.isEqual(self.m34, other.m34) and \
                   Util.isEqual(self.m41, other.m41) and \
                   Util.isEqual(self.m42, other.m42) and \
                   Util.isEqual(self.m43, other.m43) and \
                   Util.isEqual(self.m44, other.m44)
        else:
            return False
            
    def __ne__(self, other):
        return not self.__eq__(other)
                   
    def __mul__(self, other):
        '''Multiplies two matrices.'''
        assert isinstance(other, Matrix4)
        
        M = Matrix4()
        M.m11 = float(self.m11 * other.m11 + self.m12 * other.m21 + self.m13 * other.m31 + self.m14 * other.m41)
        M.m12 = float(self.m11 * other.m12 + self.m12 * other.m22 + self.m13 * other.m32 + self.m14 * other.m42)
        M.m13 = float(self.m11 * other.m13 + self.m12 * other.m23 + self.m13 * other.m33 + self.m14 * other.m43)
        M.m14 = float(self.m11 * other.m14 + self.m12 * other.m24 + self.m13 * other.m34 + self.m14 * other.m44)
        
        M.m21 = float(self.m21 * other.m11 + self.m22 * other.m21 + self.m23 * other.m31 + self.m24 * other.m41)
        M.m22 = float(self.m21 * other.m12 + self.m22 * other.m22 + self.m23 * other.m32 + self.m24 * other.m42)
        M.m23 = float(self.m21 * other.m13 + self.m22 * other.m23 + self.m23 * other.m33 + self.m24 * other.m43)
        M.m24 = float(self.m21 * other.m14 + self.m22 * other.m24 + self.m23 * other.m34 + self.m24 * other.m44)
        
        M.m31 = float(self.m31 * other.m11 + self.m32 * other.m21 + self.m33 * other.m31 + self.m34 * other.m41)
        M.m32 = float(self.m31 * other.m12 + self.m32 * other.m22 + self.m33 * other.m32 + self.m34 * other.m42)
        M.m33 = float(self.m31 * other.m13 + self.m32 * other.m23 + self.m33 * other.m33 + self.m34 * other.m43)
        M.m34 = float(self.m31 * other.m14 + self.m32 * other.m24 + self.m33 * other.m34 + self.m34 * other.m44)
        
        M.m41 = float(self.m41 * other.m11 + self.m42 * other.m21 + self.m43 * other.m31 + self.m44 * other.m41)
        M.m42 = float(self.m41 * other.m12 + self.m42 * other.m22 + self.m43 * other.m32 + self.m44 * other.m42)
        M.m43 = float(self.m41 * other.m13 + self.m42 * other.m23 + self.m43 * other.m33 + self.m44 * other.m43)
        M.m44 = float(self.m41 * other.m14 + self.m42 * other.m24 + self.m43 * other.m34 + self.m44 * other.m44)
        
        return M
    
    @property
    def determinant(self):
        '''The determinant of the matrix.'''
        A0 = self.m11 * self.m22 - self.m12 * self.m21
        A1 = self.m11 * self.m23 - self.m13 * self.m21
        A2 = self.m11 * self.m24 - self.m14 * self.m21
        A3 = self.m12 * self.m23 - self.m13 * self.m22
        A4 = self.m12 * self.m24 - self.m14 * self.m22
        A5 = self.m13 * self.m24 - self.m14 * self.m23
        B0 = self.m31 * self.m42 - self.m32 * self.m41
        B1 = self.m31 * self.m43 - self.m33 * self.m41
        B2 = self.m31 * self.m44 - self.m34 * self.m41
        B3 = self.m32 * self.m43 - self.m33 * self.m42
        B4 = self.m32 * self.m44 - self.m34 * self.m42
        B5 = self.m33 * self.m44 - self.m34 * self.m43
        
        return float(A0*B5 - A1*B4 + A2*B3 + A3*B2 - A4*B1 + A5*B0)
    
    @property
    def inverse(self):
        '''The inverse of this matrix.'''
        d = self.determinant
        
        # determinant equals zero, means no inverse, return identity
        if d == 0:
            return Matrix4.identity()
        
        M = Matrix4()
        M.m11 = (self.m23*self.m34*self.m42 - self.m24*self.m33*self.m42 + self.m24*self.m32*self.m43 - \
                self.m22*self.m34*self.m43 - self.m23*self.m32*self.m44 + self.m22*self.m33*self.m44) / d
        M.m12 = (self.m14*self.m33*self.m42 - self.m13*self.m34*self.m42 - self.m14*self.m32*self.m43 + \
                self.m12*self.m34*self.m43 + self.m13*self.m32*self.m44 - self.m12*self.m33*self.m44) / d
        M.m13 = (self.m13*self.m24*self.m42 - self.m14*self.m23*self.m42 + self.m14*self.m22*self.m43 - \
                self.m12*self.m24*self.m43 - self.m13*self.m22*self.m44 + self.m12*self.m23*self.m44) / d
        M.m14 = (self.m14*self.m23*self.m32 - self.m13*self.m24*self.m32 - self.m14*self.m22*self.m33 + \
                self.m12*self.m24*self.m33 + self.m13*self.m22*self.m34 - self.m12*self.m23*self.m34) / d
        M.m21 = (self.m24*self.m33*self.m41 - self.m23*self.m34*self.m41 - self.m24*self.m31*self.m43 + \
                self.m21*self.m34*self.m43 + self.m23*self.m31*self.m44 - self.m21*self.m33*self.m44) / d
        M.m22 = (self.m13*self.m34*self.m41 - self.m14*self.m33*self.m41 + self.m14*self.m31*self.m43 - \
                self.m11*self.m34*self.m43 - self.m13*self.m31*self.m44 + self.m11*self.m33*self.m44) / d
        M.m23 = (self.m14*self.m23*self.m41 - self.m13*self.m24*self.m41 - self.m14*self.m21*self.m43 + \
                self.m11*self.m24*self.m43 + self.m13*self.m21*self.m44 - self.m11*self.m23*self.m44) / d
        M.m24 = (self.m13*self.m24*self.m31 - self.m14*self.m23*self.m31 + self.m14*self.m21*self.m33 - \
                self.m11*self.m24*self.m33 - self.m13*self.m21*self.m34 + self.m11*self.m23*self.m34) / d
        M.m31 = (self.m22*self.m34*self.m41 - self.m24*self.m32*self.m41 + self.m24*self.m31*self.m42 - \
                self.m21*self.m34*self.m42 - self.m22*self.m31*self.m44 + self.m21*self.m32*self.m44) / d
        M.m32 = (self.m14*self.m32*self.m41 - self.m12*self.m34*self.m41 - self.m14*self.m31*self.m42 + \
                self.m11*self.m34*self.m42 + self.m12*self.m31*self.m44 - self.m11*self.m32*self.m44) / d
        M.m33 = (self.m12*self.m24*self.m41 - self.m14*self.m22*self.m41 + self.m14*self.m21*self.m42 - \
                self.m11*self.m24*self.m42 - self.m12*self.m21*self.m44 + self.m11*self.m22*self.m44) / d
        M.m34 = (self.m14*self.m22*self.m31 - self.m12*self.m24*self.m31 - self.m14*self.m21*self.m32 + \
                self.m11*self.m24*self.m32 + self.m12*self.m21*self.m34 - self.m11*self.m22*self.m34) / d
        M.m41 = (self.m23*self.m32*self.m41 - self.m22*self.m33*self.m41 - self.m23*self.m31*self.m42 + \
                self.m21*self.m33*self.m42 + self.m22*self.m31*self.m43 - self.m21*self.m32*self.m43) / d
        M.m42 = (self.m12*self.m33*self.m41 - self.m13*self.m32*self.m41 + self.m13*self.m31*self.m42 - \
                self.m11*self.m33*self.m42 - self.m12*self.m31*self.m43 + self.m11*self.m32*self.m43) / d
        M.m43 = (self.m13*self.m22*self.m41 - self.m12*self.m23*self.m41 - self.m13*self.m21*self.m42 + \
                self.m11*self.m23*self.m42 + self.m12*self.m21*self.m43 - self.m11*self.m22*self.m43) / d
        M.m44 = (self.m12*self.m23*self.m31 - self.m13*self.m22*self.m31 + self.m13*self.m21*self.m32 - \
                self.m11*self.m23*self.m32 - self.m12*self.m21*self.m33 + self.m11*self.m22*self.m33) / d
        return M
    
    @property    
    def transpose(self):
        '''Returns the transpose of this matrix.'''
        return Matrix4(self.m11, self.m21, self.m31, self.m41,
                       self.m12, self.m22, self.m32, self.m42,
                       self.m13, self.m23, self.m33, self.m43,
                       self.m14, self.m24, self.m34, self.m44)
                       
    def multiplyPoint(self, pnt):
        '''Transforms a position by this matrix.'''
        import Vector3
        assert isinstance(pnt, Vector3.Vector3)
        
        p = Vector3.Vector3()
        p.x = self.m11 * pnt.x + self.m12 * pnt.y + self.m13 * pnt.z + self.m14
        p.y = self.m21 * pnt.x + self.m22 * pnt.y + self.m23 * pnt.z + self.m24
        p.z = self.m31 * pnt.x + self.m32 * pnt.y + self.m33 * pnt.z + self.m34
        return p
        
    def multiplyVector(self, vec):
        '''Transforms a direction by this matrix.'''
        import Vector3
        assert isinstance(vec, Vector3.Vector3)
        
        v = Vector3.Vector3()
        v.x = self.m11 * vec.x + self.m12 * vec.y + self.m13 * vec.z
        v.y = self.m21 * vec.x + self.m22 * vec.y + self.m23 * vec.z
        v.z = self.m31 * vec.x + self.m32 * vec.y + self.m33 * vec.z
        return v
        
    def setIdentity(self):
        return self.set(1.0, 0.0, 0.0, 0.0,
                        0.0, 1.0, 0.0, 0.0,
                        0.0, 0.0, 1.0, 0.0,
                        0.0, 0.0, 0.0, 1.0)
    
    @staticmethod
    def identity():
        '''Returns the identity matrix.'''
        return Matrix4(1.0, 0.0, 0.0, 0.0,
                       0.0, 1.0, 0.0, 0.0,
                       0.0, 0.0, 1.0, 0.0,
                       0.0, 0.0, 0.0, 1.0)
               
    @staticmethod
    def zero():
        '''Returns a matrix with all elements set to zero.'''
        return Matrix4(0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0)
                       
    @staticmethod
    def translate(tx, ty, tz):
        '''Creates a translation matrix.'''
        return Matrix4(1.0, 0.0, 0.0, tx,
                       0.0, 1.0, 0.0, ty,
                       0.0, 0.0, 1.0, tz,
                       0.0, 0.0, 0.0, 1.0)
                       
    @staticmethod
    def rotateX(x):
        return Matrix4.rotateXInRadian(Util.degreeToRadian(x))
        
    @staticmethod
    def rotateXInRadian(x):
        cos = math.cos(x)
        sin = math.sin(x)
        return Matrix4(1.0, 0.0,  0.0, 0.0,
                       0.0, cos, -sin, 0.0,
                       0.0, sin,  cos, 0.0,
                       0.0, 0.0,  0.0, 1.0)
        
    @staticmethod
    def rotateY(y):
        return Matrix4.rotateYInRadian(Util.degreeToRadian(y))
        
    @staticmethod
    def rotateYInRadian(y):
        cos = math.cos(y)
        sin = math.sin(y)
        return Matrix4(cos, 0.0, sin, 0.0,
                       0.0, 1.0, 0.0, 0.0,
                      -sin, 0.0, cos, 0.0,
                       0.0, 0.0, 0.0, 1.0)
        
    @staticmethod
    def rotateZ(z):
        return Matrix4.rotateZInRadian(Util.degreeToRadian(z))
        
    @staticmethod
    def rotateZInRadian(z):
        cos = math.cos(z)
        sin = math.sin(z)
        return Matrix4(cos, -sin, 0.0, 0.0,
                       sin,  cos, 0.0, 0.0,
                       0.0,  0.0, 1.0, 0.0,
                       0.0,  0.0, 0.0, 1.0)
                       
    @staticmethod
    def scale(sx, sy, sz):
        return Matrix4( sx, 0.0, 0.0, 0.0,
                       0.0,  sy, 0.0, 0.0,
                       0.0, 0.0,  sz, 0.0,
                       0.0, 0.0, 0.0, 1.0)
                       
    @staticmethod
    def axisAngle(axis, angle):
        return Matrix4.axisAngleInRadian(axis, Util.degreeToRadian(angle))
        
    @staticmethod
    def axisAngleInRadian(axis, angle):
        import Vector3
        assert isinstance(axis, Vector3.Vector3) and type(angle) in (int, long, float)
        
        n = axis.normalized
        x = n.x
        y = n.y
        z = n.z
        sin = math.sin(angle)
        cos = math.cos(angle)
        l_cos = 1.0 - cos
        
        M = Matrix4()
        M.m11 = x * x * l_cos + cos
        M.m12 = x * y * l_cos - z * sin
        M.m13 = x * z * l_cos + y * sin
        M.m21 = y * x * l_cos + z * sin
        M.m22 = y * y * l_cos + cos
        M.m23 = y * z * l_cos - x * sin
        M.m31 = x * z * l_cos - y * sin
        M.m32 = y * z * l_cos + x * sin
        M.m33 = z * z * l_cos + cos
        return M