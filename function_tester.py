"""
from manim import *
from helpers import *
import numpy as np

slides = False
if slides:
    from manim_slides import Slide


class Keyword(Slide if slides else Scene):
    def construct(self):
        self.add(NumberPlane())
        keyword_overlay(self)
        slides_pause(self, 5)


class BezierSplineExample(Scene):
    def construct(self):
        p1 = np.array([0, 1, 0])
        p1b = p1 + [0, -0.5, 0]
        d1 = Dot(point=p1).set_color(BLUE)
        # l1 = Line(p1, p1b)
        p2 = np.array([-2, -1, 0])
        p2b = p2 + [0, 0.5, 0]
        d2 = Dot(point=p2).set_color(RED)
        # l2 = Line(p2b, p2)
        bezier = CubicBezier(p1, p1 + DOWN, p2 + UP, p2)
        self.play(
            LaggedStart(
                Create(d1),
                # Create(l1),
                Create(bezier),
                # Create(l2),
                Create(d2),
                lag_ratio=0.66
            ),
            run_time=2
        )
        xl_pause(self)
"""

cec = []
chr = []
with open("data.csv", "r") as inFile:
    for line in inFile:
        line = line.split()
        if line[0] == "Cecilie":
            cec.append(int(line[1]))
        elif line[0] == "Christoffer":
            chr.append(int(line[1]))

print(len(cec), len(chr))
for i in sorted(chr):
    print(int(i))
