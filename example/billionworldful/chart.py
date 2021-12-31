import sys
sys.path.append("..\\..")
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
    (7200, (1,1), 'b'),
    (7600, (0.25,1)),
    (8000, (1,1)),
    (8400, (0.25,0.5)),
    (8800, (1,0)),
    (9600, (0.25,0)),
    (10400, (1.5,0)),
  ]),
  snake([
    (10400, (0,1), 'b'),
    (11200, (0.5,1)),
    (11600, (0.5,0)),
    (12000, (0.5,1)),
    (12800, (0,1)),
    (13400, (-0.5,0)),
  ]),
  put_arctaps(
    notes(
      (11200,4),
      (12000,-3),
      (12800,3),
    ),
    batch_snakes(4, [
      [11200, [(0.5,1)] * 4, 'b'],
      [12000, four_corners],
    ], black=True)
  ),
])

########################################
# Ah
# You strike me like I've never felt before
# For you, I can go through Naraka and more

high_olive = olive(0,400,750)
high_olive.append(arc(750,799, (0.5,1), black=True))
low_olive = high_olive.translated((0,-1))
LlRh_olive = olive(0,400,750, (0.5,0.5), (0.5,0.5))
LlRh_olive.append(arc(750,799, (0.5,0.5), black=True))
LhRl_olive = LlRh_olive.mirrored()
place_holder = (114,514)
low_taps = collection([
  arc(799,799, place_holder,(0.5,-0.2), 's', -1),
  arc(799,799, (0.25,-0.2),(0.75,-0.2), 's', -1),
  tap(800,2), tap(800,3),
])
high_taps = collection([
  arc(799,799, place_holder,(0.5,1), 's', -1),
  arc(799,800, (0.5,1),(0.25,1), 's', -1, arctaps = [800]),
])
high_taps.append(high_taps[-1].mirrored())

def link(start_t, _olive, _taps):
  olive = _olive.time_shifted(start_t)
  taps = _taps.time_shifted(start_t)
  taps[0].p0 = olive[0][-1].p1
  olive.extend(taps)
  return olive

chart.extend(notes(
  link(13600, high_olive, high_taps),
  link(15200,  low_olive,  low_taps),
  link(16800, high_olive,  low_taps),
  link(18400,  low_olive, high_taps),
  link(20000, LlRh_olive,  low_taps.translated(( 0.5,0))),
  link(21600, LhRl_olive,  low_taps.translated((-0.5,0))),
  link(23200, LlRh_olive, high_taps.translated((-0.5,0))),
  link(24800, LhRl_olive, high_taps.translated(( 0.5,0))),

########################################
# Hummus and tofu burgers
# In the shape of my ever beating heart
# Vanilla rice pudding laced with aphrodisiac liquor

  (26400,2), # Hu-
  hold(27200,27999,4), # -mus
  (27500,3), # and
  (27800,2), # to-
  hold(28100,28999,1), # -fu
  (28600,3), # bur-
  (28800,3), # -gers
  put_arctaps(
    notes(
      (29200,3),  # In
      (29400,2),  # the
      hold(29500,32099,3), # shape
      (30000,-2), # of
      (30400,1),  # my
      (30800,-1), # ev-
      (31000,-1), # -er
      (31400,-2), # bea-
      (31600,-2), # -ting
      (31800,-2), # heart
    ),
    batch_snakes(2, [
      [29200, [(0,1),(1,1)], 's'],
      [[None,31200], None, 'b'],
      [32000, (0,1)],
    ], black=True)
  ),
  hold(32400,33199,4), # Va-
  hold(32800,35199,1), # -ni-
  (33400,2), # -lla
  (33600,2), # rice
  (33800,2), # pud-
  snake([
    (34200, (1,1), 's'), # -ding
    (34600, (0,1), 'b'), # laced
    (35400, (1.5,0))
  ]),
  (35400,1), # with
  (35600,2), # a-
  (35800,3), # -phro-
  (36000,1), (36000,4), # -di-
  snake([
    (36300, (0,1), 'si'), # -si-
    (36800, (1,1), 'b'),  # -ac
    (37200, (0,1))
  ]),
  (36800,3), # -ac
  (37400,4), # liq-

########################################
# You sit tall and straight, not making a sound

  (37600,1), (37600,4),
  (37800,2),
  (38000,3),
  (38200,4),
  (38400,1), (38400,4),
  (38600,2),
  arc(38800,39800, (1,1),(0.25,1), 'so'),
  (39200,1),
  (39400,2),
  arc(39800,39800, (0.25,1),(0.75,1), black=True),
  put_arctaps(
    notes(
      (40000,2),
      (40200,3),
      (40300,-1),
      (40400,3),
      (40800,2),
      (41000,3),
      (41200,2),
      (41300,3),
      (41400,2),
      (41500,3),
      hold(41600,41999,1), hold(41600,41999,4),
    ),
    double(snake([
      (39800, (0.25,1), 'b'),
      (41600,),
      (42000, (0,1)),
      (42400,),
    ], black=True))
  ),

########################################
# Chanting the heavens' song
# *cross-hand*

  repeat(2, 800,
    double(notes(
      arc(42400,42700, (0,1),(0,0), 'b'),
      snake([
        (42700, (0,0), 'b'),
        (42800,),
        (43200, (0,1)),
      ], black=True, arctaps=[42800,43000])
    ))
  ),
  put_arctaps(
    [tap(44000,-2)],
    batch_snakes(2, [
      [44000, [(0,1),(1,1)], 'b'],
      [44800, [(0.75,1),(0.25,1)]],
      [45000]
    ], colors=[0,-1])
  ),
  (44400,3),
  (44600,2),
  (44800,1),
  double(snake([
    (45000, (0.75,1), 'b'),
    (45200, (0.75,0.2)),
    (45400, (0.75,0.8)),
    (45600, (0.75,0)),
    (46400, (1.5,0)),
  ], color=0)),

########################################
# Bring me along

  arc(47200,48400, (1,1),(0.3,1), 's'),
  (47200,3),
  (47400,2),
  (47600,3),
  (47800,2),
  (48000,1),
  (48200,2),
  (48400,3),

########################################
# Thought you look through me

  put_arctaps(
    notes(
      hold(48800,49599,2),
      (49000,-2),
      (49200,-4),
      (49400,-3),
      hold(49600,50399,3),
      (50200,-2),
      (50300,-3),
      hold(50400,51199,4),
      (50600,-2),
      (50800,-1),
      hold(51200,51999,1),
      (51200,-4),
      (51400,-1),
      (51600,-2),
    ),
    batch_snakes(4, [
      [48800, equidistant(4)],
      [52000]
    ], black=True)
  ),
  arc(52000,52000, (0,1),(1,1), black=True),

########################################
# Like I wasn't there

  hold(52000,52799,4),
  (52400,3),
  hold(52800,53599,1),
  (53200,2),
  double(notes(
    arc(53600,54000, (0.5,1),(0,1), 'sisi', color=0),
    arc(53600,54400, (0.5,1),(-0.5,0), 'sisi', black=True),
  )),
  (54400,1),
  (54500,2),
  (54600,1),
  (54800,4),
  (54900,3),
  (55000,4),

########################################
# Soaked myself in cold water
# Breaking this endless wheel
# Praying for divine powers
# So we can become one

  repeat(6, 1600, olive(55200,56000,56800)),
))

########################################

aff.save_file('2.aff', chart)
