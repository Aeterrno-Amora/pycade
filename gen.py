import itertools as it
import note
import coordinate as cd
from copy import deepcopy
from random import randint

flatten = it.chain.from_iterable

#################### list of positions ####################

two_corners = (cd.position(0,1), cd.position(1,1))
four_corners = (cd.position(-0.5,0), cd.position(0,1), cd.position(1,1), cd.position(1.5,0))

def equidistant(n, x0 = 0, x1 = 1, y0 = 1, y1 = None):
    if y1 is None: y1 = y0  # default horizontal
    dx = (x1 - x0) / (n - 1)
    dy = (y1 - y0) / (n - 1)
    return tuple(cd.position(x0 + dx * i, y0 + dy * i) for i in range(0, n))

#################### list of times ####################

def t_repeat(ts, end, dt):
    '''repeat until end, assume an ordered list is provided'''
    if not hasattr(ts, '__iter__'): ts = (ts,)
    end -= 1e-4
    result = []
    for i in it.count():
        for t in ts:
            t1 = t + i * dt
            if t1 >= end: return result
            result.append(int(t1))

def t_repeat_n(ts, n, dt):
    '''repeat n times, sorts the output'''
    return sorted([int(t + i * dt) for t in ts for i in range(n)]
        if hasattr(ts, '__iter__') else [int(ts + i * dt) for i in range(n)])

########################## snake ##########################
'''
Optional args to snake() and their defaults are:
    color = None, black = False, arctaps = []
'''

def swing(t0, t1, dt, poss, easings = 'b', *args, **kwargs):
    '''
    A snake composed of arcs of equal duration.
    Keypoints and easing cycle through poss and easings respectively.
    App: springs, successive squares, etc., or simply to create a rhythmic snake.
    '''
    return note.snake(zip(it.chain(t_repeat(t0, t1, dt), [t1]),
            it.cycle(poss), it.cycle(easings)), *args, **kwargs)

################### collection of snakes ###################

def batch_snakes(n, data, colors = None, black = False):
    '''
    Create snakes in batch to avoid code duplication.
    Usage: data = iterable[[ts, positions, easings]]
           where each xxxs is either an iterable to be traversed or a single value to be repeated.
           None here means "same as the previous one".
           If a data point contains less than 3 args, it is appended with None.
    App: double snakes, sky tracks for arctaps
    '''
    data_per_snake = [[] for k in range(n)]
    last = [None, None, 'b']  # default easing = 'b'
    for this in data:
        while len(this) < 3:
            this.append(None)
        for i in range(3):
            if this[i] is not None:
                last[i] = this[i]
        ts, poss, easings = last
        ts = (it.repeat if type(ts) == int else iter)(ts)
        poss = (it.repeat if cd.ispos(poss) else iter)(poss)
        easings = (it.repeat if type(easings) == str else iter)(easings)
        for dat in data_per_snake:
            dat.append((next(ts), next(poss), next(easings)))
    colors = (iter if hasattr(colors, '__iter__') else it.repeat)(colors)
    return note.collection(note.snake(dat, next(colors), black) for dat in data_per_snake)

def olive(t0, t1, t2, center = (0.5,1), radius = (0.5,0), black = False, diamond = False):
    '''2 snakes making an olive, with its fatest spot at t1'''
    center = cd.position(center)
    radius = cd.position(radius)
    return batch_snakes(2, [
            [t0, center, 's' if diamond else 'sisi'],
            [t1, [center - radius, center + radius], 's' if diamond else 'soso'],
            [t2, center, None]
        ], colors = [0, 1], black = black)

################### collection of notes ###################

def notes(*items):
    '''Build a collection, turning tuples into taps by the way.'''
    return note.collection(note.tap(*item) if isinstance(item, tuple)
                            else item for item in items)

def batch_taps(ts, *lanes):
    '''lane = int or iterable[int], iterable means multiple taps at the same time'''
    result = note.collection()
    for t, lane in zip(ts, lanes):
        if hasattr(lane, '__iter__'):
            result.extend(note.tap(t, l) for l in lane)
        else:
            result.append(note.tap(t, lane))
    return result

def double(item):
    return note.collection([item, item.mirrored()])

def repeat(n, dt, item, mirror=False):
    pattern = deepcopy(item)
    result = note.collection()
    for i in range(n):
        result.append(deepcopy(pattern))
        pattern.time_shift(dt)
        if mirror: pattern.mirror()
    return result

def put_arctaps(items, snakes, offset = 0):
    '''Put taps on lane -i onto sky track snakes[offset + (i-1)].'''
    result = deepcopy(snakes)
    for item in items:
        if isinstance(item, note.tap) and item.lane < 0:
            result[offset - item.lane - 1].add_tap(item.t)
        else: result.append(item)
    return result

def rand_taps(ts, n_tracks):
    result = note.collection()
    for t in ts:
        lane = randint(1, 4 + n_tracks)
        if lane > 4: lane = 4 - lane
        result.append(note.tap(t, lane))
    return result

def rand_double_taps(ts, n_tracks):
    result = note.collection()
    for t in ts:
        lane1 = randint(1, 4 + n_tracks)
        lane2 = randint(1, 3 + n_tracks)
        if lane2 == lane1: lane2 += 1
        if lane1 > 4: lane1 = 4 - lane1
        if lane2 > 4: lane2 = 4 - lane2
        result.append(note.tap(t, lane1))
        result.append(note.tap(t, lane2))
    return result

def rand_sky_floor_taps(ts, n_tracks):
    return flatten([note.tap(t, randint(1, 4)),
                    note.tap(t, -randint(1, n_tracks))] for t in ts)
