import itertools as it
import note
import coordinate as cd

#################### list of positions ####################

four_corners = ((-0.5,0), (0,1), (1,1), (1.5,0))

def equidistant(n, x0 = 0, x1 = 1, y0 = 1, y1 = None):
    if y1 is None: y1 = y0  # default horizontal
    dx = (x1 - x0) / (n - 1)
    dy = (y1 - y0) / (n - 1)
    return tuple((x0 + dx * i, y0 + dy * i) for i in range(0, n))

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
    return note.snake(zip(it.chain(range(t0, t1, dt), [t1]), it.cycle(poss), it.cycle(easings)), *args, **kwargs)

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

################### collection of notes ###################

def taps(*items):
    '''Turn tuples into taps.'''
    return note.collection(note.tap(*item) if isinstance(item, tuple) else item for item in items)

def put_arctaps(items, snakes):
    '''Put taps with negative lane number onto sky tracks. '''
    new_items = note.collection(snake for snake in snakes)
    for item in items:
        if isinstance(item, note.tap) and item.lane < 0:
            new_items[-item.lane - 1].add_tap(item.t)
        else: new_items.append(item)
    return new_items
