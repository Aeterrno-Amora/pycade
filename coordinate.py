PIX_PER_X = 850
PIX_PER_Y = 450
ORIGIN = (0.5, 1.0)

class vector:
    '''coordinates on the parallel plane messured in pixels, with the middle of the sky input line as the origin'''
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __init__(self, p):
        if isinstance(p, tuple):
            self.x, self.y = p
        elif isinstance(p, vector):
            self.x, self.y = p.x, p.y
        elif isinstance(p, position):
            self.x, self.y = (p.x - ORIGIN[0]) * PIX_PER_X, (p.y - ORIGIN[1]) * PIX_PER_Y
        elif isinstance(p, d_position):
            self.x, self.y = p.x * PIX_PER_X, p.y * PIX_PER_Y
        else: raise TypeError("Can't convert " + str(type(p)) + " to vector")

    def __add__(self, p):
        p = vector(p)
        return vector(self.x + p.x, self.y + p.y)

    def __sub__(self, p):
        p = vector(p)
        return vector(self.x - p.x, self.y - p.y)

    def __mul__(self, a):
        return vector(self.x * a, self.y * a)

    def __div__(self, a):
        return vector(self.x / a, self.y / a)

    def mirror(self):
        return vector(-self.x, self.y)

    def mirror_(self):
        self.x = -self.x

class position:
    '''chart position'''
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __init__(self, p):
        if isinstance(p, tuple):
            self.x, self.y = p
        elif isinstance(p, position):
            self.x, self.y = p.x, p.y
        elif isinstance(p, vector):
            self.x, self.y = p.x / PIX_PER_X + ORIGIN[0], p.y / PIX_PER_Y + ORIGIN[1]
        else: raise TypeError("Can't convert " + str(type(p)) + " to position")

    def __add__(self, p):
        p = d_position(p)
        return position(self.x + p.x, self.y + p.y)

    def __sub__(self, p):
        if isinstance(p, position):
            return d_position(self.x - p.x, self.y - p.y)
        p = d_position(p)
        return position(self.x - p.x, self.y - p.y)

    def mirror(self):
        return position(1.0 - self.x, self.y)

    def mirror(self):
        self.x = 1.0 - self.x

class d_position:
    '''difference of chart position'''
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __init__(self, p):
        if isinstance(p, tuple):
            self.x, self.y = p
        elif isinstance(p, d_position):
            self.x, self.y = p.x, p.y
        elif isinstance(p, vector):
            self.x, self.y = p.x / PIX_PER_X, p.y / PIX_PER_Y
        else: raise TypeError("Can't convert " + str(type(p)) + " to d_position")

    def __add__(self, p):
        if isinstance(p, postion):
            return position(self.x + p.x, self.y + p.y)
        elif isinstance(p, d_postion):
            return d_position(self.x + p.x, self.y + p.y)
        elif isinstance(p, vector):
            q = vector(self)
            return vector(q.x + p.x, q.y + p.y)
        else: raise TypeError("Can't add " + str(type(p)) + " to d_position")

    def __sub__(self, p):
        p = d_position(p)
        return d_position(self.x - p.x, self.y - p.y)

    def __mul__(self, a):
        return d_position(self.x * a, self.y * a)

    def __div__(self, a):
        return d_position(self.x / a, self.y / a)

    def mirror(self):
        return d_position(-self.x, self.y)

    def mirror_(self):
        self.x = -self.x


def lane_position(lane):
    return position(lane * 0.5 - 0.75, -0.2)


class vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class position3:
    def __init__(self, x, y, t):
        self.x = x
        self.y = y
        self.t = t

    def pos2(self):
        return position(x, y)


def ispos(p):
    return (isinstance(p, tuple) and (len(p) == 2 or len(p) == 3) and (isinstance(p[0],float) or isinstance(p[0],int))) or isinstance(p, vector) or isinstance(p, position) or isinstance(p, d_position) or isinstance(p, vector3) or isinstance(p, position3)
