import coordinate as cd
from copy import deepcopy

def Warning(msg):
    print('Warning:', msg)

class note:
    '''subclasses should implement these methods:
    __str__(self)
    translate(self, dp)
    mirror(self)
    time_shift(self, dt)
    time_reverse(self, sum_t)  where the center of symmetry = sum_t / 2
    '''

    def set_color(self, color):
        '''-1 means black lines'''
        pass    # only affects arc and collection containing arcs

    def translated(self, dp):
        copy = deepcopy(self)
        copy.translate(dp)
        return copy

    def mirrored(self):
        copy = deepcopy(self)
        copy.mirror()
        return copy

    def time_shifted(self, dt):
        copy = deepcopy(self)
        copy.time_shift(dt)
        return copy

    def time_reversed(self, sum_t):
        copy = deepcopy(self)
        copy.time_reverse(sum_t)
        return copy

    def set_colored(self, color):
        copy = deepcopy(self)
        copy.set_color(color)
        return copy

class tap(note):
    def __init__(self, t, lane):
        self.t = int(t)
        self.lane = int(lane)

    def __str__(self):
        if self.lane < 1 or self.lane > 4:
            Warning(f'tap({self.t},{self.lane}): lane is invalid')
        return f'({self.t},{self.lane});'

    def translate(self, dp):
        self.lane = max(1, min(4, round(self.lane + cd.position(dp).x * 2)))

    def mirror(self):
        self.lane = 5 - self.lane

    def time_shift(self, dt):
        self.t += dt

    def time_reverse(self, sum_t):
        self.t = sum_t - self.t

class hold(note):
    def __init__(self, t0, t1, lane):
        self.t0 = int(t0)
        self.t1 = int(t1)
        self.lane = int(lane)

    def __str__(self):
        if self.lane < 1 or self.lane > 4:
            Warning(f'hold({self.t0},{self.t1},{self.lane}): lane is invalid')
        if self.t0 >= self.t1:
            Warning(f'hold({self.t0},{self.t1},{self.lane}): t0 >= t1')
        return f'hold({self.t0},{self.t1},{self.lane});'

    def translate(self, dp):
        self.lane = max(1, min(4, round(self.lane + cd.position(dp).x * 2)))


    def mirror(self):
        self.lane = 5 - self.lane

    def time_shift(self, dt):
        self.t0 += dt
        self.t1 += dt

    def time_reverse(self, sum_t):
        self.t0, self.t1 = sum_t - self.t1, sum_t - self.t0

class arc(note):
    def __init__(self, t0, t1, p0, p1 = None, easing = 'b', color = None, black = False, arctaps = []):
        '''easing: b, s, si, so, sisi, siso, sosi, soso'''
        self.t0 = int(t0)
        self.t1 = int(t1)
        self.p0 = cd.position(p0)
        self.p1 = self.p0 if p1 is None else cd.position(p1)
        self.easing = str(easing)
        if color == None:
            if self.p0 == (0,1): color = 0    # TODO: refine conditions
            elif self.p0 == (1,1): color = 1
        self.color = color
        self.black = bool(black) or color == -1
        self.arctaps = list(arctaps)

    def __str__(self):
        if self.t0 > self.t1:
            Warning(f'arc({self.t0},{self.p0.x:.2f},{self.p0.y:.2f} -{self.easing}- {self.t1},{self.p1.x:.2f},{self.p1.y:.2f}): t0 > t1')
        if self.color is None:
            if self.black:
                self.color = 1 if self.p0.x > 0.5 else 0
            else:
                Warning(f'arc({self.t0},{self.p0.x:.2f},{self.p0.y:.2f} -{self.easing}- {self.t1},{self.p1.x:.2f},{self.p1.y:.2f}): color is None')
        self.p0 = cd.position(self.p0)
        self.p1 = cd.position(self.p1)
        self.arctaps.sort()
        if self.arctaps:
            str_arctaps = '[' + ','.join(f'arctap({t})' for t in self.arctaps) + ']'
        else: str_arctaps = ''
        return f'arc({self.t0},{self.t1},{self.p0.x:.2f},{self.p1.x:.2f},{self.easing},{self.p0.y:.2f},{self.p1.y:.2f},{self.color},none,{"true" if self.black else "false"}){str_arctaps};'


    def add_tap(self, t):
        assert self.t0 <= t <= self.t1, f'arctap {t} out of arc [{self.t0}, {self.t1}]'
        self.arctaps.append(t)

    def add_taps(self, ts):
        for t in ts:
            assert self.t0 <= t <= self.t1, f'arctap {t} out of arc [{self.t0}, {self.t1}]'
        self.arctaps.extend(ts)

    def translate(self, dp):
        dp = cd.position(dp)
        self.p0 += dp
        self.p1 += dp

    def mirror(self):
        self.p0.mirror()
        self.p1.mirror()
        if self.color in (0,1):
            self.color = 1 - self.color

    def time_shift(self, dt):
        self.t0 += dt
        self.t1 += dt
        self.arctaps = [t + dt for t in self.arctaps]

    def time_reverse(self, sum_t = None):
        if sum_t is not None:
            self.t0, self.t1 = sum_t - self.t1, sum_t - self.t0
        self.p0, self.p1 = self.p1, self.p0
        self.easing = self.easing.translate(str.maketrans('io','oi'))
        self.arctaps = [sum_t - t for t in self.arctaps]

    def set_color(self, color):
        if color != -1:
            self.color = color
        else:
            self.black = True

class timing(note):
    def __init__(self, t, bpm, beats):
        self.t = int(t)
        self.bpm = float(bpm)
        self.beats = float(beats)

    def __str__(self):
        return f'timing({self.t},{self.bpm},{self.beats});'

    def translate(self, dp): pass

    def mirror(self): pass

    def time_shift(self, dt):
        self.t += dt

    def time_reverse(self, sum_t):
        Warning('[undefined behavior] timing.time_reverse')
        self.t = sum_t - self.t

class camera(note):
    def __init__(self, t, dt, dx, dy, dz, drx, dry, drz, easing):
        '''easing: qi, qo, l, reset, s'''
        self.t = int(t)
        self.dt = float(dt)
        self.dx = float(dx)
        self.dy = float(dy)
        self.dz = float(dz)
        self.drx = float(drx)
        self.dry = float(dry)
        self.drz = float(drz)
        self.easing = str(easing)

    def __str__(self):
        if self.dt < 0:
            Warning(f'camera({self.t},{self.dx:.2f},{self.dy:.2f},{self.dz:.2f},{self.drx:.2f},{self.dry:.2f},{self.drz:.2f},{self.easing},{self.dt}): dt < 0')
        return f'camera({self.t},{self.dx:.2f},{self.dy:.2f},{self.dz:.2f},{self.drx:.2f},{self.dry:.2f},{self.drz:.2f},{self.easing},{self.dt});'

    def translate(self, dp): pass

    def mirror(self): pass # TODO

    def time_shift(self, dt):
        self.t += dt

    def time_reverse(self, sum_t):
        self.dx = -self.dx
        self.dy = -self.dy
        self.dz = -self.dz
        self.drx = -self.drx
        self.dry = -self.dry
        self.drz = -self.drz
        if self.easing != 'reset':
            self.t = sum_t - self.t - self.dt
        else:
            self.t = sum_t - self.t
        if self.easing == 'qi': self.easing = 'qo'
        elif self.easing == 'qo': self.easing = 'qi'

class scenecontrol(note):
    def __init__(self, t, act, *args):
        '''act: trackhide, trackshow, redline, arcahvdistort, arcahvdebris, hidegroup'''
        self.t = int(t)
        self.act = str(act)
        self.args = args

    def __str__(self):
        # There are unknown args; see wiki.
        return f'scenecontrol({self.t},{",".join([self.act] + map(str, self.args))});'

    def translate(self, dp): pass

    def mirror(self): pass

    def time_shift(self, dt):
        self.t += dt

    def time_reverse(self, sum_t):
        Warning('[undefined behavior] scenecontrol.time_reverse')
        self.t = sum_t - self.t


class collection(note,list):
    def __init__(self, *args, **kwargs):
        list.__init__(self, *args, **kwargs)

    def __str__(self):
        return '\n'.join(map(str, self))

    def mirror(self):
        for item in self: item.mirror()

    def translate(self, dp):
        for item in self: item.translate(dp)

    def time_shift(self, dt):
        for item in self: item.time_shift(dt)

    def time_reverse(self, sum_t):
        '''center of symmetry = sum_t / 2'''
        for item in self: item.time_reverse(sum_t)
        self.reverse()

    def set_color(self, color):
        for item in self: item.set_color(color)

class timinggroup(collection):
    def __init__(self, noinput = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.noinput = bool(noinput)

    def __str__(self):
        return 'timinggroup(' + ('noinput' if self.noinput else '') + '){\n' + collection.__str__(self) + '\n};'

class ordered_collection(collection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sort(key = lambda item: item.t0)

class snake(ordered_collection):
    '''keep successive arcs sorted by time'''
    def __init__(self, data = None, color = None, black = False, arctaps = []):
        '''
        data: iterable through (t, position, easing)s
              3 args in the tuple can be arbitrarily ordered, and are told by type.
              Missing t means "skip this", missing p or easing means "same as above".
        '''
        super().__init__()
        if data is None: return

        def proc_data():
            t, p, easing = 0, (0,1), 'b'  # default values
            for datum in data:
                if any(type(x) == int for x in datum):
                    for x in datum:
                        if type(x) == int: t = x
                        elif cd.ispos(x): p = x
                        elif type(x) == str: easing = x
                    yield t, p, easing

        it_data = proc_data()
        t0, p0, easing0 = next(it_data)
        if color == None:    # default not black lines
            if cd.position(p0) == (0,1): color = 0    # TODO: refine conditions
            elif cd.position(p0) == (1,1): color = 1
        for t, p, easing in it_data:
            self.append(arc(t0,t, p0,p, easing0, color, black))
            t0, p0, easing0 = t, p, easing
        self.add_taps(arctaps)

    def add_tap(self, t):
        i = 0
        while self[i].t1 < t: i += 1
        self[i].add_tap(t)

    def add_taps(self, ts):
        i = 0
        for t in ts:
            while self[i].t1 < t: i += 1
            self[i].add_tap(t)
