import coordinate as cd
from copy import deepcopy

class note:
    def __str__(self): abstract
    def translate(self, d_pos): abstract
    def mirror(self): abstract
    def shift_time(self, dt): abstract
    def reverse_time(self, sum_t): abstract

    def translated(self):
        copy = deepcopy(self)
        copy.translate()
        return copy

    def mirrored(self):
        copy = deepcopy(self)
        copy.mirror()
        return copy

    def shifted_time(self):
        copy = deepcopy(self)
        copy.shift_time()
        return copy

    def reversed_time(self):
        copy = deepcopy(self)
        copy.reverse_time()
        return copy

class tap(note):
    def __init__(self, t, lane):
        self.t = t
        self.lane = lane

    def __str__(self):
        return '(%d,%d);' % (self.t, self.lane)

    def translate(self, d_pos):
        self.lane = max(1, min(4, round(self.lane + cd.d_position(d_pos).x * 2)))

    def mirror(self):
        self.lane = 5 - self.lane

    def shift_time(self, dt):
        self.t += dt

    def reverse_time(self, sum_t):
        '''center of symmetry = sum_t / 2'''
        self.t = sum_t - self.t

class hold(note):
    def __init__(self, t1, t2, lane):
        self.t1 = t1
        self.t2 = t2
        self.lane = lane

    def __str__(self):
        return 'hold(%d,%d,%d);' % (self.t1, self.t2, self.lane)

    def translate(self, dx, dy):
        self.lane = max(1, min(4, round(self.lane + cd.d_position(d_pos).x * 2)))

    def mirror(self):
        self.lane = 5 - self.lane

    def shift_time(self, dt):
        self.t1 += dt
        self.t2 += dt

    def reverse_time(self, sum_t):
        '''center of symmetry = sum_t / 2'''
        self.t1, self.t2 = sum_t - self.t2, sum_t - self.t1

class arc(note):
    def __init__(self, t1, t2, pos1, pos2, easing = 'b', color = None, black = False, arctaps = []):
        '''easing: b, s, si, so, sisi, siso, sosi, soso'''
        self.t1 = t1
        self.t2 = t2
        self.pos1 = cd.position(pos1)
        self.pos2 = cd.position(pos2)
        self.easing = easing
        if color is None:
            self.color = 1 if pos1[0] > 0.5 else 0
        else: self.color = color
        self.black = black
        self.arctaps = arctaps

    def __str__(self):
        self.arctaps.sort()
        if self.arctaps:
            str_arctaps = '[' + ','.join('arctap(%d)' % t for t in self.arctaps) + ']'
        else: str_arctaps = ''
        self.pos1 = cd.position(self.pos1)
        self.pos2 = cd.position(self.pos2)
        return 'arc(%d,%d,%.2f,%.2f,%s,%.2f,%.2f,%d,none,%s)%s;' % (
                self.t1, self.t2, self.pos1.x, self.pos2.x, self.easing, self.pos1.y, self.pos2.y,
                self.color, 'true' if self.black else 'false', str_arctaps)

    def add_tap(self, t):
        assert self.t1 <= t <= self.t2
        self.arctaps.append(t)

    def add_taps(self, ts):
        for t in ts:
            assert self.t1 <= t <= self.t2
        self.arctaps.extend(ts)

    def translate(self, d_pos):
        self.pos1 += d_pos
        self.pos2 += d_pos

    def mirror(self):
        self.pos1.mirror()
        self.pos2.mirror()
        if self.color in (0,1):
            self.color = 1 - self.color

    def shift_time(self, dt):
        self.t1 += dt
        self.t2 += dt
        self.arctaps = [t + dt for t in self.arctaps]

    def reverse_time(self, sum_t = None):
        '''center of symmetry = sum_t / 2'''
        if sum_t is not None:
            self.t1, self.t2 = sum_t - self.t2, sum_t - self.t1
        self.pos1, self.pos2 = self.pos2, self.pos1
        self.easing = self.easing.translate(str.maketrans('io','oi'))
        self.arctaps = [sum_t - t for t in self.arctaps]

class timing(note):
    def __init__(self, t, bpm, beats):
        self.t = t
        self.bpm = bpm
        self.beats = beats

    def __str__(self):
        return 'timing(%d,%.2f,%.2f);' % (self.t, self.bpm, self.beats)

class camera(note):
    def __init__(self, t, dt, dx, dy, dz, d_ax, d_ay, d_az, easing):
        '''easing: qi, qo, l, reset, s'''
        self.t = t
        self.dt = dt
        self.dx = dx
        self.dy = dy
        self.dz = dz
        self.d_ax = d_ax
        self.d_ay = d_ay
        self.d_az = d_az
        self.easing = easing

    def __str__(self):
        return 'camera(%d,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%s,%d);' % (self.t, self.dx, self.dy, self.dz, self.d_ax, self.d_ay, self.d_az, self.easing, self.dt)

class scenecontrol(note):
    def __init__(self, t, type, x = 0, y = 0):
        '''type: trackdisplay, redline, arcahvdistort, arcahvdebris'''
        self.t = t
        self.type = type
        self.x = x
        self.y = y

    def __str__(self):
        return 'scenecontrol(%d,%s,%f,%d);' % (self.t, self.type, self.x, self.y)

class collection(note,list):
    pass

class timinggroup(note):
    def __init__(self, *args, **kwargs):
        self.items = list(*args, **kwargs)

    def __str__(self):
        return '\n'.join(['timinggroup(){'] + [str(item) for item in self.items] + ['};'])

def snake(list):
    '''keep successive arcs sorted by time'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sort(key = lambda arc: arc.t1)

    def __str__(self):
        return '\n'.join(str(arc) for arc in self)

    def add_tap(self, t):
        i = 0
        while self[i].t2 < t: i += 1
        self[i].add_tap(t)

    def add_taps(self, ts):
        i = 0
        for t in ts:
            while self[i].t2 < t: i += 1
            self[i].add_tap(t)

    def set_color(self, color):
        for arc in self: arc.color = color

    def mirror(self):
        for arc in self: arc.mirror()

    def translate(self, d_pos):
        for arc in self: arc.translate()

    def shift_time(self, dt):
        for arc in self: arc.shift_time()

    def reverse_time(self, sum_t):
        '''center of symmetry = sum_t / 2'''
        for arc in self: arc.reverse_time()
        self.reverse()
