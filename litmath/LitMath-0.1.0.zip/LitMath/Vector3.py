import math
import Util

class Vector3(object):
    __slots__ = ['x', 'y', 'z']
    __hash__ = None
    
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        
    def set(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        return self
        
    def copy(self):
        import copy
        return copy.copy(self)
    
    def __repr__(self):
        return 'Vector3(%.2f, %.2f, %.2f)' % (self.x, self.y, self.z)
        
    def __eq__(self, other):
        if isinstance(other, Vector3):
            return Util.isEqual(self.x, other.x) and \
                   Util.isEqual(self.y, other.y) and \
                   Util.isEqual(self.z, other.z)
        else:
            return False
            
    def __ne__(self, other):
        return not self.__eq__(other)
            
    def __add__(self, other):
        assert isinstance(other, Vector3)
        return Vector3(self.x + other.x,
                       self.y + other.y,
                       self.z + other.z)
    
    def __sub__(self, other):
        assert isinstance(other, Vector3)
        return Vector3(self.x - other.x,
                       self.y - other.y,
                       self.z - other.z)
                       
    def __mul__(self, other):
        assert type(other) in (int, long, float)
        return Vector3(self.x * other, self.y * other, self.z * other)
    __rmul__ = __mul__
            
    def __div__(self, other):
        assert type(other) in (int, long, float)
        return Vector3(self.x / other, self.y / other, self.z / other)
            
    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)
    
    @property
    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        
    @property
    def lengthSquared(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2
        
    def normalize(self):
        m = self.length
        if m != 0:
            self.x /= m
            self.y /= m
            self.z /= m
        return self
    
    @property
    def normalized(self):
        m = self.length
        if m != 0:
            return Vector3(self.x / m, self.y / m, self.z / m)
        else:
            return self.copy()
    
    @staticmethod    
    def dot(a, b):
        assert isinstance(a, Vector3) and isinstance(b, Vector3)
        return a.x * b.x + a.y * b.y + a.z * b.z
    
    @staticmethod    
    def cross(a, b):
        assert isinstance(a, Vector3) and isinstance(b, Vector3)
        return Vector3(a.y * b.z - a.z * b.y,
                       a.z * b.x - a.x * b.z,
                       a.x * b.y - a.y * b.x)
        
    @staticmethod
    def angle(a, b):
        return Util.radianToDegree(Vector3.angleInRadian(a, b))
    
    @staticmethod    
    def angleInRadian(a, b):
        assert isinstance(a, Vector3) and isinstance(b, Vector3)
        m2 = a.length * b.length
        if m2 == 0:
            return 0.0
        else:
            v = Vector3.dot(a, b) / m2
            return math.acos( Util.clamp(v, -1.0, 1.0) )