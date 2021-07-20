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
    note.snake([
        (7200, (1,1)),
        (7600, (0.25,1)),
        (8000, (1,1)),
        (8400, (0.25,0.5)),
        (8800, (1,0)),
        (9600, (0.25,0)),
        (10400, (1.5,0))]),
    note.snake([
        (10400, (0,1)),
        (11200, (0.5,1)),
        (11600, (0.5,0)),
        (12000, (0.5,1)),
        (12800, (0,1)),
        (13400, (-0.5,0))]),
    put_arctaps(
        taps((11200,4), (12000,-3), (12800,3)),
        batch_snakes(4, [
            [11200, [(0.5,1)] * 4, 'b'],
            [12000, four_corners, 'b']
        ], black = True)
    ),
    
])

aff.save_file('generated/2_out.aff', chart)
