import itertools
import note

four_corners = ((0,1), (1,1), (-0.5,0), (1.5,0))

def taps(*lis):
    '''
    taps((t1,lane1), (t2,lane2), ...) = [note.tap(t1,lane1), note.tap(t2,lane2), ...]
    '''
    return note.collection(note.tap(*args) for args in lis)

def batch_arcs(t1, t2, num_tracks = 2, x0 = 0.0, x1 = 1.0, y = 1.0, start_pos = None, end_pos = None, easing = 's', black = True):
    '''
    Simultaneous arcs, useful to serve as tracks for arctaps.
    start_pos, end_pos: list[coordinates.position] or list of tuples to be converted to positions.
    If start_pos not given, create equidistant positions on a line.
    If end_pos not given, default to parrellel straight arcs.
    Hint: Use zip() to aggregate results of mutliple call of batch_arcs(), then feed into note.snake() to get a batch of snakes.
    '''
    if start_pos:
        num_tracks = len(start_pos)
    elif end_pos:
        num_tracks = len(end_pos)
    if start_pos is None:
        start_pos = [(x0 + (x1 - x0) / num_tracks * i, y) for i in range(num_tracks)]
    if end_pos is None:
        end_pos = start_pos
    return note.collection(note.arc(t1, t2, start_pos[i], end_pos[i], easing, 0 if i * 2 < num_tracks else 1, black)
            for i in range(num_tracks))

def put_arctaps(items = [], snakes = []):
    '''
    Put taps with negative lane number onto sky tracks.
    '''
    new_items = note.collection(snake for snake in snakes)
    for item in items:
        if isinstance(item, note.tap) and item.lane < 0:
            new_items[-item.lane - 1].add_tap(item.t)
        else: new_items.append(item)
    return new_items

def swing(t_st, t_ed, dt, pos, easing, color = None, black = False, arctaps = []):
    '''
    A snake made by arcs of equal length.
    Keypoints, easing cycle through pos, easing respectively.
    Useful to draw springs, successive squares, etc.,
    or to simply create a rhythmic snake.
    '''
    n = (t_ed - t_st) // dt
    return note.snake(list(range(t_st, t_ed, dt)) + [t_ed],
            list(itertools.islice(itertools.cycle(pos), n+1)),
            [easing] * n if isinstance(easing, str) else list(itertools.islice(itertools.cycle(easing), n)),
            color, black, arctaps)
