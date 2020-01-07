def taxicab_distance(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1])


class Point3D:
    __slots__ = 'data'

    def __init__(self, x, y, z):
        self.data = [x, y, z]

    def __repr__(self):
        return f'Point(x={self.x}, y={self.y}, z={self.z})'

    @property
    def x(self):
        return self.data[0]

    @property
    def y(self):
        return self.data[1]

    @property
    def z(self):
        return self.data[2]

    @x.setter
    def x(self, value):
        self.data[0] = value

    @y.setter
    def y(self, value):
        self.data[1] = value

    @z.setter
    def z(self, value):
        self.data[2] = value

    @classmethod
    def from_point(cls, other):
        return cls(other.x, other.y, other.z)

    def __getitem__(self, i):
        return self.data[i]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __add__(self, other):
        return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __iadd__(self, other):
        self.data[0], self.data[1], self.data[2] = (
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )
        return self

    def __eq__(self, other):
        return all([self.x == other.x, self.y == other.y, self.z == other.z,])


class Point2D:
    __slots__ = 'data'

    def __init__(self, x, y):
        self.data = [x, y]

    def __repr__(self):
        return f'Point(x={self.x}, y={self.y})'

    @property
    def x(self):
        return self.data[0]

    @property
    def y(self):
        return self.data[1]

    @x.setter
    def x(self, value):
        self.data[0] = value

    @y.setter
    def y(self, value):
        self.data[1] = value

    @classmethod
    def from_point(cls, other):
        return cls(other.x, other.y)

    def __getitem__(self, i):
        return self.data[i]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __add__(self, other):
        return Point2D(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.data[0], self.data[1] = (
            self.x + other.x,
            self.y + other.y,
        )
        return self

    def __eq__(self, other):
        return all([self.x == other.x, self.y == other.y])
