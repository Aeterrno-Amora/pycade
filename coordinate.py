PIX_PER_X = 850
PIX_PER_Y = 450
IS_16by9 = False

class position:
    '''chart position, in which the four corners are (-0.5,0), (0,1), (1,1), (1.5,0)'''
    def __init__(self, *a):
        if len(a) == 1: a = a[0]
        if hasattr(a, "__getitem__"):
            self.x, self.y = float(a[0]), float(a[1])
        elif isinstance(a, position) or isinstance(a, position3):
            self.x, self.y = a.x, a.y
        elif isinstance(a, vector) or isinstance(a, vector3):
            self.x, self.y = a.x / PIX_PER_X, a.y / PIX_PER_Y
        else: raise TypeError("Can't convert " + str(type(a)) + " to d_position")

    def __tuple__(self):
        return (self.x, self.y)

    def __add__(self, p):
        p = position(p)
        return position(self.x + p.x, self.y + p.y)

    def __sub__(self, p):
        p = position(p)
        return position(self.x - p.x, self.y - p.y)

    def __mul__(self, a):
        return position(self.x * a, self.y * a)

    def __div__(self, a):
        return position(self.x / a, self.y / a)

    def __eq__(self, p):
        p = position(p)
        return self.x == p.x and self.y == p.y

    def mirror(self):
        self.x = 1 - self.x

    def mirrored(self):
        return position(1 - self.x, self.y)

class vector:
    '''coordinate messured in pixels, in which the four corners are (-425,0), (0,450), (850,450), (1275,0)'''
    def __init__(self, *a):
        if len(a) == 1: a = a[0]
        if hasattr(a, "__getitem__"):
            self.x, self.y = float(a[0]), float(a[1])
        elif isinstance(a, vector) or isinstance(a, vector3):
            self.x, self.y = a.x, a.y
        elif isinstance(a, position) or isinstance(a, position3):
            self.x, self.y = a.x * PIX_PER_X, a.y * PIX_PER_Y
        else: raise TypeError("Can't convert " + str(type(a)) + " to vector")

    def __tuple__(self):
        return (self.x, self.y)

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

    def __eq__(self, p):
        p = vector(p)
        return self.x == p.x and self.y == p.y

    def mirror(self):
        self.x = PIX_PER_X - self.x

    def mirrored(self):
        return vector(PIX_PER_X - self.x, self.y)

class position3:
    def __init__(self, *a):
        if len(a) == 1: a = a[0]
        if hasattr(a, "__getitem__"):
            if len(a) == 2:
                self.x, self.y = tuple(position(a[0]))
                if isinstance(a[0], position) or isinstance(a[0], vector):
                    # position3(position, t), position3(vector, t)
                    self.t = float(a[1])
                elif isinstance(a[0], vector3): # position3(vector3, timing_seq)
                    self.t = a[1].z2t(a[0].z)
            else:   # position3(x, y, t)
                self.x, self.y, self.t = float(a[0]), float(a[1]), float(a[2])
        elif isinstance(a, position3):  # position3(position3)
            self.x, self.y, self.t = tuple(a)
        else: raise TypeError("Can't convert " + str(type(a)) + " to d_position")

    def __tuple__(self):
        return (self.x, self.y, self.t)

    def __add__(self, p):
        p = position3(p)
        return position(self.x + p.x, self.y + p.y, self.t + p.t)

    def __sub__(self, p):
        p = position3(p)
        return position(self.x - p.x, self.y - p.y, self.t - p.t)

    def __mul__(self, a):
        return position3(self.x * a, self.y * a, self.t * a)

    def __div__(self, a):
        return position3(self.x / a, self.y / a, self.t / a)

    def __eq__(self, p):
        p = position3(p)
        return self.x == p.x and self.y == p.y and self.z == p.z

    def mirror(self):
        self.x = 1 - self.x

    def mirrored(self):
        return position3(1 - self.x, self.y, self.t)

class vector3:
    def __init__(self, *a):
        if len(a) == 1: a = a[0]
        if hasattr(a, "__getitem__"):
            if len(a) == 2:
                self.x, self.y = tuple(vector(a[0]))
                if isinstance(a[0], position) or isinstance(a[0], vector):
                    # vector3(position, z), vector3(vector, z)
                    self.z = float(a[1])
                elif isinstance(a[0], position3): # vector3(position3, timing_seq)
                    self.z = a[1].t2z(a[0].t)
            else:   # vector3(x, y, z)
                self.x, self.y, self.t = float(a[0]), float(a[1]), float(a[2])
        elif isinstance(a, vector3):  # vector3(vector3)
            self.x, self.y, self.t = tuple(a)
        else: raise TypeError("Can't convert " + str(type(a)) + " to d_position")

    def __tuple__(self):
        return (self.x, self.y, self.z)

    def __add__(self, p):
        p = position3(p)
        return position(self.x + p.x, self.y + p.y, self.z + p.z)

    def __sub__(self, p):
        p = position3(p)
        return position(self.x - p.x, self.y - p.y, self.z - p.z)

    def __mul__(self, a):
        return position3(self.x * a, self.y * a, self.z * a)

    def __div__(self, a):
        return position3(self.x / a, self.y / a, self.z / a)

    def __eq__(self, p):
        p = vector3(p)
        return self.x == p.x and self.y == p.y and self.z == p.z

    def mirror(self):
        self.x = 1 - self.x

    def mirrored(self):
        return position3(1 - self.x, self.y, self.z)

def ispos(p):
    return (isinstance(p, tuple) and (len(p) == 2 or len(p) == 3) and (isinstance(p[0],float) or isinstance(p[0],int))) or isinstance(p, vector) or isinstance(p, position) or isinstance(p, vector3) or isinstance(p, position3)

################ frequently used positions ################

def lane_position(lane):
    return position(lane * 0.5 - 0.75, -0.2)

#def initial_cemera()
INITIAL_CAMERA = vector3(425, 800, 900 if IS_16by9 else 800)  # to be measured

################ utils ################

start, bpm, beats = 0, 150.0, 4.0

def tempo2tf(bar, beat = 0):
    beat += (bar - 1) * beats
    return start + beat * 60000 / bpm

def tempo2t(bar, beat = 0):
    return int(tempo2tf(bar, beat))

def tempo2dtf(bar, beat = 0):
    beat += bar * beats
    return beat * 60000 / bpm

def tempo2dt(bar, beat = 0):
    return int(tempo2dtf(bar, beat))
