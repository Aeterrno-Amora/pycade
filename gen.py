import itertools as it
import note

#################### list of positions ####################

four_corners = ((-0.5,0), (0,1), (1,1), (1.5,0))

def equidistant(n, x0 = 0.0, x1 = 1.0, y0 = 1.0, y1 = None):
    if y1 is None: y1 = y0  # default horizontal
    return zip(range(x0, x1, (x1-x0)/n), range(y0, y1, (y1-y0)/n))

########################## snake ##########################
'''
Optional args to snake() and their defaults are:
    color = None, black = False, arctaps = []
'''

def swing(t0, t1, dt, poss, easings = 'b', *args, **kwargs):
    '''
    A snake made by arcs of equal length.
    Keypoints and easing cycle through poss and easings respectively.
    App: springs, successive squares, etc., or simply to create a rhythmic snake.
    '''
    return note.snake(zip(it.chain(range(t0, t1, dt), [t1]), it.cycle(poss), it.cycle(easings)), *args, **kwargs)

################### collection of snakes ###################

def batch_snakes(n, data, colors = None, black = False):
    '''
    A batch of snakes with same numbers of arcs.
    Usage: data = iterable through [ts, positions, easings]
           xxxs is an iterable through xxx to be traversed or a single xxx to be repeated
           None here means "same as above"
    App: double snakes, sky tracks for arctaps
    '''
    data_per_snake = [[] for k in range(n)]
    last = [None, None, 'b']  # default easing = 'b'
    for this in data:
        for i in range(3):
            if this[i] is None:
                this[i] = last[i]
        last = this
        ts, poss, easings = this
        ts = (it.repeat if type(ts) == int else iter)(ts)
        poss = (it.repeat if note.cd.ispos(poss) else iter)(poss)
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
