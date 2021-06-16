import itertools as it
import note

#################### list of positions ####################

four_corners = ((-0.5,0), (0,1), (1,1), (1.5,0))

def equidistant(n, x0 = 0.0, x1 = 1.0, y0 = 1.0, y1 = None):
    if y1 is None: y1 = y0  # default horizontal
    return zip(range(x0, x1, (x1-x0)/n), range(y0, y1, (y1-y0)/n))

########################## snake ##########################

def swing(t0, t1, dt, pos, easing = 'b', color = None, black = False, arctaps = []):
    '''
    A snake made by arcs of equal length.
    Keypoints and easing cycle through pos and easing respectively.
    App: springs, successive squares, etc., or simply to create a rhythmic snake.
    '''
    n = (t1 - t0) // dt
    return note.snake(list(range(t0, t1, dt)) + [t1],
            list(it.islice(it.cycle(pos), n+1)),
            [easing] * n if isinstance(easing, str) else list(it.islice(it.cycle(easing), n)),
            color, black, arctaps)

################### collection of snakes ###################

def batch_arcs(n, data, colors = None, black = True):
    '''
    A batch of snakes with same numbers of arcs.
    Usage: data = [[[ts], [positions], [easings]]]
           None here in data means "same as above"
    App: double snakes, sky tracks for arctaps
    '''
    data_per_snake = [[] for k in range(n)]
    last = None
    for this in data:
        for i in range(3):
            if this[i] is None:
                this[i] = last[i]
        last = this
        ts, poss, easings = this
        for k in range(n):
            data_per_snake[k].append([ts[k], poss[k], easings[k]])
    if colors is None: colors = [None] * n
    return note.collection(note.snake(data_per_snake[k], colors[k], black[k]) for dat in data_per_snake)

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
