import coordinate as cd
from copy import deepcopy

class note:
    def __str__(self): abstract
    def translate(self, d_pos): abstract
    def mirror(self): abstract
    def time_shift(self, dt): abstract
    def time_reverse(self, sum_t):
        '''center of symmetry = sum_t / 2'''
        abstract

    def set_color(self, color):
        '''-1 means setting to black lines'''
        pass    # except for arc

    def translated(self, d_pos):
        copy = deepcopy(self)
        copy.translate(d_pos)
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
        return '(%d,%d);' % (self.t, self.lane)

    def translate(self, d_pos):
        self.lane = max(1, min(4, round(self.lane + cd.d_position(d_pos).x * 2)))

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
        return 'hold(%d,%d,%d);' % (self.t0, self.t1, self.lane)

    def translate(self, dx, dy):
        self.lane = max(1, min(4, round(self.lane + cd.d_position(d_pos).x * 2)))

    def mirror(self):
        self.lane = 5 - self.lane

    def time_shift(self, dt):
        self.t0 += dt
        self.t1 += dt

    def time_reverse(self, sum_t):
        self.t0, self.t1 = sum_t - self.t1, sum_t - self.t0

class arc(note):
    def __init__(self, t0, t1, pos0, pos1 = None, easing = 'b', color = None, black = False, arctaps = []):
        '''easing: b, s, si, so, sisi, siso, sosi, soso'''
        self.t0 = int(t0)
        self.t1 = int(t1)
        self.pos0 = cd.position(pos0)
        self.pos1 = self.pos0 if pos1 is None else cd.position(pos1)
        self.easing = str(easing)
        if color == None:
            if tuple(pos0) == (0,1): color = 0    # TODO: refine conditions
            elif tuple(pos0) == (1,1): color = 1
        self.color = color
        self.black = bool(black) or color == -1
        self.arctaps = list(arctaps)

    def __str__(self):
        if self.color is None:
            if self.black:
                self.color = 1 if self.pos0.x > 0.5 else 0
            else:
                print("Warning: arc(%d,%.2f,%.2f -%s- %d,%.2f,%.2f).color is None" % (self.t0, self.pos0.x, self.pos0.y, self.easing, self.t1, self.pos1.x, self.pos1.y))
        self.arctaps.sort()
        if self.arctaps:
            str_arctaps = '[' + ','.join('arctap(%d)' % t for t in self.arctaps) + ']'
        else: str_arctaps = ''
        self.pos0 = cd.position(self.pos0)
        self.pos1 = cd.position(self.pos1)
        return 'arc(%d,%d,%.2f,%.2f,%s,%.2f,%.2f,%d,none,%s)%s;' % (
                self.t0, self.t1, self.pos0.x, self.pos1.x, self.easing, self.pos0.y, self.pos1.y,
                self.color, 'true' if self.black else 'false', str_arctaps)

    def add_tap(self, t):
        assert self.t0 <= t <= self.t1
        self.arctaps.append(t)

    def add_taps(self, ts):
        for t in ts:
            assert self.t0 <= t <= self.t1
        self.arctaps.extend(ts)

    def translate(self, d_pos):
        d_pos = cd.d_position(d_pos)
        self.pos0 += d_pos
        self.pos1 += d_pos

    def mirror(self):
        self.pos0.mirror()
        self.pos1.mirror()
        if self.color in (0,1):
            self.color = 1 - self.color

    def time_shift(self, dt):
        self.t0 += dt
        self.t1 += dt
        self.arctaps = [t + dt for t in self.arctaps]

    def time_reverse(self, sum_t = None):
        if sum_t is not None:
            self.t0, self.t1 = sum_t - self.t1, sum_t - self.t0
        self.pos0, self.pos1 = self.pos1, self.pos0
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
        return 'timing(%d,%.2f,%.2f);' % (self.t, self.bpm, self.beats)

    def translate(self, d_pos): pass

    def mirror(self): pass

    def time_shift(self, dt):
        self.t += dt

    def time_reverse(self, sum_t):
        print("Warning: [undefined behavior] timing.time_reverse")
        self.t = sum_t - t

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
        return 'camera(%d,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%s,%d);' % (self.t, self.dx, self.dy, self.dz, self.drx, self.dry, self.drz, self.easing, self.dt)

    def translate(self, d_pos): pass

    def mirror(self): pass

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
            self.t = sum_t - t - dt
        else:
            self.t = sum_t - t
        if self.easing == 'qi': self.easing = 'qo'
        elif self.easing == 'qo': self.easing = 'qi'

class scenecontrol(note):
    def __init__(self, t, act, *args):
        '''act: trackhide, trackshow, redline, arcahvdistort, arcahvdebris, hidegroup'''
        self.t = int(t)
        self.act = str(act)
        self.args = args

    def __str__(self):
        str_arg = ','.join([self.act] + map(str, args))
        # There are unknown args; see wiki.
        return 'scenecontrol(%d,%s);' % (self.t, str_arg)

    def translate(self, d_pos): pass

    def mirror(self): pass

    def time_shift(self, dt):
        self.t += dt

    def time_reverse(self, sum_t):
        print("Warning: [undefined behavior] scenecontrol.time_reverse")
        self.t = sum_t - t


class collection(note,list):
    def __init__(self, *args, **kwargs):
        list.__init__(self, *args, **kwargs)

    def __str__(self):
        return '\n'.join(str(item) for item in self)

    def mirror(self):
        for item in self: item.mirror()

    def translate(self, d_pos):
        for item in self: item.translate(d_pos)

    def time_shift(self, dt):
        for item in self: item.time_shift(dt)

    def time_reverse(self, sum_t):
        '''center of symmetry = sum_t / 2'''
        for item in self: item.time_reverse(sum_t)
        self.reverse()

    def set_color(self, color):
        for item in self: item.set_color(color)

    def mirrored(self):
        return collection(item.mirrored() for item in self)

    def translated(self, d_pos):
        return collection(item.translated(d_pos) for item in self)

    def time_shifted(self, dt):
        return collection(item.time_shifted(dt) for item in self)

    def time_reversed(self, sum_t):
        return collection(reversed(item.time_reversed(sum_t) for item in self))

    def set_colored(self, color):
        return collection(item.set_colored(color) for item in self)

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
              Missing t means "skip this", missing pos or easing means "same as above".
        '''
        super().__init__()
        if data is None: return

        def proc_data():
            t, pos, easing = 0, (0,1), 'b'  # default values
            for datum in data:
                if any(type(x) == int for x in datum):
                    for x in datum:
                        if type(x) == int: t = x
                        elif cd.ispos(x): pos = x
                        elif type(x) == str: easing = x
                    yield t, pos, easing

        it_data = proc_data()
        t0, pos0, easing0 = next(it_data)
        if color == None:    # default not black lines
            if tuple(pos0) == (0,1): color = 0    # TODO: refine conditions
            elif tuple(pos0) == (1,1): color = 1
        for t, pos, easing in it_data:
            self.append(arc(t0,t, pos0,pos, easing0, color, black))
            t0, pos0, easing0 = t, pos, easing
        self.add_taps(arctaps)

    def __str__(self):
        return '\n'.join(map(str, self))

    def add_tap(self, t):
        i = 0
        while self[i].t1 < t: i += 1
        self[i].add_tap(t)

    def add_taps(self, ts):
        i = 0
        for t in ts:
            while self[i].t1 < t: i += 1
            self[i].add_tap(t)
