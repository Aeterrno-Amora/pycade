import re
import note
from gen import taps


hold = note.hold
timing = note.timing
scenecontrol = note.scenecontrol
timinggroup = note.timinggroup

def arc(t1, t2, x1, x2, easing, y1, y2, color, FX, skylineBoolean, arctaps = []):
    return note.arc(t1, t2, (x1,y1), (x2,y2), easing, color, skylineBoolean, arctaps)

def camera(t, transverse, bottomzoom, linezoom, steadyangle, topzoom, angle, easing, lastingtime):
    return note.camera(t, lastingtime, transverse, bottomzoom, linezoom, steadyangle, topzoom, angle, easing)

def parse(s):
    s = s.translate(str.maketrans(';',',',' \t\n'))
    for old, new in (')[',',['),(']','])'),('noinput){','1,taps('),('){','0,taps('),('}','))'),('arctap',''),('false','False'),('true','True'):
        s = s.replace(old, new)
    for literal in 'b','s','si','so','sisi','siso','sosi','soso','qi','qo','l','reset','none','full','incremental','trackhide','trackshow','redline','arcahvdistort','arcahvdebris','hidegroup':
        s = re.sub(r'(?<=\W)' + literal + r'(?=\W)', '"' + literal + '"', s)
    return eval('taps(' + s + ')')


def make_header(AudioOffset = 0, DensityFactor = 1):
    return 'AudioOffset:%d\n' % AudioOffset + ('TimingPointDensityFactor:%f\n' % DensityFactor if DensityFactor != 1 else '') + '-\n'

def parse_header(s):
    '''
    return header_args, which is a dict used as keyword args
    '''
    for literal in 'AudioOffset','TimingPointDensityFactor':
        s = s.replace(literal, '"' + literal + '"')
    return eval('{' + s.translate(str.maketrans('\n',',')) + '}')


def save_file(f, chart, header = make_header()):
    if not (isinstance(chart[0], note.timing) and chart[0].t == 0):
        print('Warning: Should begin with a timing at t = 0.')
    if file_opened := isinstance(f, str):
        f = open(f, 'w')
    f.write(header + '\n'.join(str(item) for item in chart))
    if file_opened: f.close()

def load_file(f):
    '''
    return chart, header_args
    '''
    if file_opened := isinstance(f, str):
        f = open(f)
    header, _, content = f.read().partition('-\n')
    if file_opened: f.close()
    return parse(content), parse_header(header)
