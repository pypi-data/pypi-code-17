import math
import Util

class Matrix3(object):
    __slots__ = ['m11', 'm12', 'm13',
                 'm21', 'm22', 'm23',
                 'm31', 'm32', 'm33']
    __hash__ = None
    
    def __init__(self, m11=1.0, m12=0.0, m13=0.0,
                       m21=0.0, m22=1.0, m23=0.0,
                       m31=0.0, m32=0.0, m33=1.0):
        self.m11 = float(m11)
        self.m12 = float(m12)
        self.m13 = float(m13)
        self.m21 = float(m21)
        self.m22 = float(m22)
        self.m23 = float(m23)
        self.m31 = float(m31)
        self.m32 = float(m32)
        self.m33 = float(m33)
        
    def set(self, m11, m12, m13,
                  m21, m22, m23,
                  m31, m32, m33):
        self.m11 = float(m11)
        self.m12 = float(m12)
        self.m13 = float(m13)
        self.m21 = float(m21)
        self.m22 = float(m22)
        self.m23 = float(m23)
        self.m31 = float(m31)
        self.m32 = float(m32)
        self.m33 = float(m33)
        return self
        
    def copy(self):
        import copy
        return copy.copy(self)
    
    def __repr__(self):
        return ('Matrix3(%8.2f %8.2f %8.2f\n' \
                '        %8.2f %8.2f %8.2f\n' \
                '        %8.2f %8.2f %8.2f )') \
                % (self.m11, self.m12, self.m13,
                   self.m21, self.m22, self.m23,
                   self.m31, self.m32, self.m33)
                   
    def __eq__(self, other):
        if isinstance(other, Matrix3):
            return Util.isEqual(self.m11, other.m11) and \
                   Util.isEqual(self.m12, other.m12) and \
                   Util.isEqual(self.m13, other.m13) and \
                   Util.isEqual(self.m21, other.m21) and \
                   Util.isEqual(self.m22, other.m22) and \
                   Util.isEqual(self.m23, other.m23) and \
                   Util.isEqual(self.m31, other.m31) and \
                   Util.isEqual(self.m32, other.m32) and \
                   Util.isEqual(self.m33, other.m33)
        else:
            return False
            
    def __ne__(self, other):
        return not self.__eq__(other)
                            
    def __mul__(self, other):
        '''Multiplies two matrices.'''
        assert isinstance(other, Matrix3)
        M = Matrix3()
        M.m11 = float(self.m11 * other.m11 + self.m12 * other.m21 + self.m13 * other.m31)
        M.m12 = float(self.m11 * other.m12 + self.m12 * other.m22 + self.m13 * other.m32)
        M.m13 = float(self.m11 * other.m13 + self.m12 * other.m23 + self.m13 * other.m33)
        M.m21 = float(self.m21 * other.m11 + self.m22 * other.m21 + self.m23 * other.m31)
        M.m22 = float(self.m21 * other.m12 + self.m22 * other.m22 + self.m23 * other.m32)
        M.m23 = float(self.m21 * other.m13 + self.m22 * other.m23 + self.m23 * other.m33)
        M.m31 = float(self.m31 * other.m11 + self.m32 * other.m21 + self.m33 * other.m31)
        M.m32 = float(self.m31 * other.m12 + self.m32 * other.m22 + self.m33 * other.m32)
        M.m33 = float(self.m31 * other.m13 + self.m32 * other.m23 + self.m33 * other.m33)
        return M
    
    @property    
    def determinant(self):
        '''The determinant of the matrix.'''
        return float(self.m11 * self.m22 * self.m33 + \
                     self.m12 * self.m23 * self.m31 + \
                     self.m13 * self.m21 * self.m32 - \
                     self.m11 * self.m23 * self.m32 - \
                     self.m12 * self.m21 * self.m33 - \
                     self.m13 * self.m22 * self.m31)
    
    @property    
    def inverse(self):
        '''The inverse of this matrix.'''
        d = self.determinant
        
        # determinant equals zero, means no inverse, return identity
        if d == 0:
            return Matrix3.identity()
        
        tmp = Matrix3()
        tmp.m11 = (self.m22 * self.m33 - self.m23 * self.m32) / d
        tmp.m12 = (self.m13 * self.m32 - self.m12 * self.m33) / d
        tmp.m13 = (self.m12 * self.m23 - self.m13 * self.m22) / d
        tmp.m21 = (self.m23 * self.m31 - self.m21 * self.m33) / d
        tmp.m22 = (self.m11 * self.m33 - self.m13 * self.m31) / d
        tmp.m23 = (self.m13 * self.m21 - self.m11 * self.m23) / d
        tmp.m31 = (self.m21 * self.m32 - self.m22 * self.m31) / d
        tmp.m32 = (self.m12 * self.m31 - self.m11 * self.m32) / d
        tmp.m33 = (self.m11 * self.m22 - self.m12 * self.m21) / d
        return tmp
        
    @property
    def transpose(self):
        '''Returns the transpose of this matrix.'''
        return Matrix3(self.m11, self.m21, self.m31,
                       self.m12, self.m22, self.m32,
                       self.m13, self.m23, self.m33)
        
    def multiplyPoint(self, pnt):
        '''Transforms a position by this matrix.'''
        import Vector2
        assert isinstance(pnt, Vector2.Vector2)
        
        p = Vector2.Vector2()
        p.x = self.m11 * pnt.x + self.m12 * pnt.y + self.m13
        p.y = self.m21 * pnt.x + self.m22 * pnt.y + self.m23
        return p
        
    def multiplyVector(self, vec):
        '''Transforms a direction by this matrix.'''
        import Vector2
        assert isinstance(vec, Vector2.Vector2)
        
        p = Vector2.Vector2()
        p.x = self.m11 * vec.x + self.m12 * vec.y
        p.y = self.m21 * vec.x + self.m22 * vec.y
        return p
        
    def setIdentity(self):
        return self.set(1.0, 0.0, 0.0,
                        0.0, 1.0, 0.0,
                        0.0, 0.0, 1.0)
    
    @staticmethod
    def identity():
        '''Returns the identity matrix.'''
        return Matrix3(1.0, 0.0, 0.0,
                       0.0, 1.0, 0.0,
                       0.0, 0.0, 1.0)
                       
    @staticmethod
    def zero():
        '''Returns a matrix with all elements set to zero.'''
        return Matrix3(0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0)
                       
    @staticmethod
    def translate(x, y):
        '''Creates a translation matrix.'''
        return Matrix3(1.0, 0.0, x,
                       0.0, 1.0, y,
                       0.0, 0.0, 1.0)
                       
    @staticmethod
    def rotate(angle):
        '''Creates a rotation matrix, angle is in degree.'''
        return Matrix3.rotateInRadian(Util.degreeToRadian(angle))
                       
    @staticmethod
    def rotateInRadian(angle):
        '''Creates a rotation matrix, angle is in radian.'''
        cos = math.cos(angle)
        sin = math.sin(angle)
        return Matrix3(cos, -sin, 0.0,
                       sin,  cos, 0.0,
                       0.0,  0.0, 1.0)
        
    @staticmethod
    def scale(sx, sy):
        '''Creates a scale matrix.'''
        return Matrix3(sx,  0.0, 0.0,
                       0.0, sy,  0.0,
                       0.0, 0.0, 1.0)