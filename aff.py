import re
import note

hold = note.hold
timing = note.timing
scenecontrol = note.scenecontrol
timinggroup = note.timinggroup

def arctap(t):
    return t

def arc(t1, t2, x1, x2, slideeasing, y1, y2, color, FX, skylineBoolean, arctaps = []):
    return note.arc(t1, t2, (x1,y1), (x2,y2), slideeasing, color, skylineBoolean, arctaps)

def camera(t, transverse, bottomzoom, linezoom, steadyangle, topzoom, angle, easing, lastingtime):
    return note.camera(t, lastingtime, transverse, bottomzoom, linezoom, steadyangle, topzoom, angle, easing)

def parse(s):
    s = s.translate(str.maketrans('{};','[],',' \t\n'))
    for old, new in (')[',',['),(']','])'),('false','False'),('true','True'):
        s = s.replace(old, new)
    for literal in 'b','s','si','so','sisi','siso','sosi','soso','qi','qo','l','reset','none','full','incremental','trackdisplay','redline','arcahvdistort','arcahvdebris':
        s = re.sub(r'(?<=\W)' + literal + r'(?=\W)', '"' + literal + '"', s)
    items = eval('[' + s + ']')
    return [note.tap(*item) if isinstance(item, tuple) else item for item in items]

def load_file(f):
    if newly_open := isinstance(f, str):
        f = open(f)
    line = f.readline()
    if line.startswith('AudioOffset'):
        audio_offset = int(line[12:])
        f.readline()
    else:
        audio_offset = 0
        f.seek(0)
    content = f.read()
    if newly_open: f.close()
    return parse(content), audio_offset

def save_file(f, items, audio_offset = 0):
    if not (isinstance(items[0], note.timing) and items[0].t == 0):
        print('Warning: Should begin with a timing at t = 0.')
    if newly_open := isinstance(f, str):
        f = open(f, 'w')
    f.write('AudioOffset:%d\n-\n' % audio_offset)
    f.write('\n'.join(str(item) for item in items))
    if newly_open: f.close()

if __name__ == '__main__':
    import sys
    items, audio_offset = load_file('test.aff')
    save_file(sys.stdout, items, audio_offset)
