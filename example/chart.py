import sys
sys.path.append("..")
import aff
from note import *
from gen import *

########################################

chart = aff.parse("""
timing(0,150.00,4.00);
(800,3);
(1100,3);
(1400,3);
(1600,2);
(1900,2);
(2200,2);
arc(0,6380,0.00,0.00,s,1.00,1.00,0,none,true)[arctap(3200),arctap(3500),arctap(3800),arctap(4800)];
arc(0,7200,1.00,1.00,s,1.00,1.00,1,none,true)[arctap(2400),arctap(2700),arctap(3000),arctap(4400),arctap(5600)];
(4000,4);
(5200,1);
(6000,3);
""")

chart.extend([
    swing(6400,7192,66, [(0,1),(0.25,1)], 'b'),
    snake([
        (7200, (1,1)),
        (7600, (0.25,1)),
        (8000, (1,1)),
        (8400, (0.25,0.5)),
        (8800, (1,0)),
        (9600, (0.25,0)),
        (10400, (1.5,0)),
    ]),
    snake([
        (10400, (0,1)),
        (11200, (0.5,1)),
        (11600, (0.5,0)),
        (12000, (0.5,1)),
        (12800, (0,1)),
        (13400, (-0.5,0)),
    ]),
    put_arctaps(
        taps((11200,4), (12000,-3), (12800,3)),
        batch_snakes(4, [
            [11200, [(0.5,1)] * 4, 'b'],
            [12000, four_corners, 'b'],
        ], black=True)
    ),
])

########################################

high_olive = olive(0,400,750)
high_olive.append(arc(750,799, (0.5,1), easing='s', black=True))
low_olive = high_olive.translated((0,-1))
LlRh_olive = olive(0,400,750, (0.5,0.5), (0.5,0.5))
LlRh_olive.append(arc(750,799, (0.5,0.5), easing='s', black=True))
LhRl_olive = LlRh_olive.mirrored()
low_taps = collection([
    arc(799,799, (114,514),(0.5,-0.2), 's', -1),
    arc(799,799, (0.25,-0.2),(0.75,-0.2), 's', -1),
    tap(800,2), tap(800,3),
])
high_taps = collection([
    arc(799,799, (114,514),(0.5,1), 's', -1),
    arc(799,800, (0.5,1),(0.25,1), 's', -1, arctaps = [800]),
])
high_taps.append(high_taps[-1].mirrored())

def link(t, _olive, _taps):
    olive = _olive.time_shifted(t)
    taps = _taps.time_shifted(t)
    taps[0].pos0 = olive[0][-1].pos1
    olive.extend(taps)
    return olive

chart.extend([
    link(13600, high_olive, high_taps),
    link(15200,  low_olive,  low_taps),
    link(16800, high_olive,  low_taps),
    link(18400,  low_olive, high_taps),
    link(20000, LlRh_olive,  low_taps.translated(( 0.5,0))),
    link(21600, LhRl_olive,  low_taps.translated((-0.5,0))),
    link(23200, LlRh_olive, high_taps.translated((-0.5,0))),
    link(24800, LhRl_olive, high_taps.translated(( 0.5,0))),
])

########################################

thispart = taps(
    (26400,2),
    hold(27200,27999,4),
    (27500,3),
    (27800,2),
    hold(28100,28999,1),
    (28600,3),
    (28800,3),
    (29200,3),
    (29400,2),
    hold(29500,32099,3),
    (30000,-2),
    (30400,1),
    (30800,-1),
    (31000,-1),
    (31400,-2),
    (31600,-2),
    (31800,-2),
    hold(32400,33199,4),
    hold(32800,35199,1),
    (33400,2),
    (33600,2),
    (33800,2),
    snake([
        (34200, (1,1), 's'), 
        (34600, (0,1), 'b'),
        (35400, (1.5,0))
    ]),
    (35400,1),
    (35600,2),
    (35800,3),
    (36000,1), (36000,4),
    snake([
        (36300, (0,1), 'si'),
        (36800, (1,1), 'b'),
        (37200, (0,1))
    ]),
    (36800,3),
    (37400,4),
)

chart.extend(
    put_arctaps(
        thispart,
        batch_snakes(2, [
            [29200, [(0,1),(1,1)], 's'],
            [[None,31200], None, 'b'],
            [32000, (0,1), 'b'],
        ], black=True)
    )
)

########################################

aff.save_file('generated/2_out.aff', chart)
