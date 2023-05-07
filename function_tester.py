from manim import *
from helpers import *
import numpy as np

slides = False
if slides:
    from manim_slides import Slide


"""

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

class ShineTester(Scene):
    def construct(self):
        line = Line(LEFT, UP, stroke_width=2, color=YELLOW)

        # line_shine = VGroup(
        #     *[
        #         Line(
        #             start=line.get_left(),
        #             end=line.get_right(),
        #             stroke_width=(2*(i + 1))**2
        #         ).set_opacity(np.exp(-(i+1)**2)) for i in np.linspace(2, 0, 10)
        #     ]
        # )
        # for shine in line_shine:
        #     self.add(shine)
        #     self.wait(1)
        # self.add(line)
        line = add_shine(line, 10)
        self.play(
            *[Create(shine) for shine in line],
            run_time=4
        )

        circ = Circle(radius=2, color=BLUE, stroke_width=2).shift(DOWN).set_style(fill_opacity=0)
        circ = add_shine(circ, 10)
        self.play(
            *[Create(shine) for shine in circ],
            run_time=4
        )

        self.wait(1)
        fade_out_all(self)

        plane = NumberPlane()
        graph = plane.plot(lambda x: x**2)
        self.add(plane)
        graph = add_shine(graph)
        self.play(
            # *[Create(g) for g in graph],
            Create(graph),
            run_time=2
        )
        self.wait(2)
