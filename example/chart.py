import sys
sys.path.append("..")
import aff
from gen import *

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
    note.snake([7200, 7600, 8000, 8400, 8800, 9600, 10400],
        [(1,1), (0.25,1), (1,1), (0.25,0.5), (1,0), (0.25,0), (1.5,0)],
        ['b'] * 6),
    note.snake([10400, 11200, 11600, 12000, 12800, 13400],
        [(0,1), (0.5,1), (0.5,0), (0.5,1), (0,1), (-0.5,0)],
        ['b'] * 5),
    put_arctaps(
        taps((11200,4), (12000,-3), (12800,3)),
        batch_arcs(11200,12000, start_pos = [(0.5,1)] * 4,
            end_pos = four_corners, easing = 'b', black = True)
    ),
    
])

aff.save_file('generated/2_out.aff', chart)
