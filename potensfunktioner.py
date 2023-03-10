from manim import *
from helpers import *
import numpy as np
import math

slides = False
if slides:
    from manim_slides import Slide


class ToPunkt(Slide if slides else Scene):
    def construct(self):
        self.to_punkt()
        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def to_punkt(self):
        scene_marker("To-punkt-formel")
        plane = NumberPlane(
            x_range=[-1, 16, 1],
            y_range=[-1, 9, 1],
            x_length=17,
            y_length=10,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.4
            }
        ).scale(0.7)  # .to_edge(UL, buff=0.1)
        plane_box = get_background_rect(plane, buff=0, stroke_colour=TEAL)
        plane_group = VGroup(plane, plane_box)
        self.play(
            # DrawBorderThenFill(plane),
            # Create(plane_box)
            DrawBorderThenFill(plane_group)
        )
        self.slide_pause(0.5)

        p1col, p2col = RED, BLUE
        acol, bcol = PURPLE, GREEN

        x1, x2 = ValueTracker(1), ValueTracker(4)
        y1, y2 = ValueTracker(3), ValueTracker(15)
        points = always_redraw(lambda: VGroup(
            *[
                Dot(
                    plane.c2p(x, y),
                    color=col
                ) for x, y, col in zip(
                    (x1.get_value(), x2.get_value()),
                    (y1.get_value(), y2.get_value()),
                    (p1col, p2col)
                )
            ]
        ))
        point_eqs = VGroup(
            # MathTex(r"y_1", "=", "b", r"\cdot", r"x_1", r"^a").set_color_by_tex_by_color_map
            MathTex(r"y_1", "=", "b", r"\cdot", r"x_1", "", r"^a", substrings_to_isolate=[r"y_1", "b", r"x_1", "a"]),
            MathTex(r"y_2", "=", "b", r"\cdot", r"x_2", "", r"^a", substrings_to_isolate=[r"y_2", "b", r"x_2", "a"]),
        ).arrange(DOWN)
        i = 1
        for eq, col in zip(point_eqs, (p1col, p2col)):
            eq.set_color_by_tex("y"+f"_{i}", col)
            eq.set_color_by_tex("b", bcol)
            # eq.set_color_by_tex("x"+f"_{i}", col)
            eq.set_color_by_tex("a", acol)
            i += 1

        self.add(point_eqs)
