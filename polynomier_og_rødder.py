from manim import *
from helpers import *
import numpy as np

slides = False
if slides:
    from manim_slides import Slide

width = 14
graph_col = YELLOW
plane = NumberPlane(
    x_range=(-10.5, 10.5, 1),
    y_range=(-5.5, 10.5, 1),
    x_length=width,
    y_length=width / 16 * 9,
    background_line_style={
        "stroke_color": TEAL,
        "stroke_width": 2,
        "stroke_opacity": 0.3
    },
    axis_config={"include_numbers": True}
)


class Polynomier(Slide if slides else MovingCameraScene):
    def construct(self):
        title = "Polynomier og deres ordner"
        # play_title(self, title, cols={"0": YELLOW, "-1": RED})
        self.slide_pause(0.5)
        self.play(
            DrawBorderThenFill(plane),
            run_time=0.5
        )
        self.slide_pause(0.5)
        self.andengrad()

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t=t, slides_bool=slides_bool)

    def topgraph(self, func, ytop):
        for x in np.arange(5, 10, 0.01):
            y = func(x)
            if np.abs(y - ytop) <= 0.5:
                return x


    def andengrad(self):
        a = ValueTracker(0)
        b = ValueTracker(2)
        c = ValueTracker(-2)
        graph = always_redraw(lambda:
            plane.plot(
                lambda x: a.get_value() * x**2 + b.get_value() * x + c.get_value(),
                x_range=plane.get_x_range(),
                color=graph_col,
                stroke_width=2.5
            )
        )
        # graph_text = always_redraw(lambda:
        #     MathTex(
        #         "f(x)",
        #         color=graph_col
        #     ).move_to(plane.c2p(self.topgraph(graph.underlying_function, 10) - 1, 10))
        # )
        self.play(
            LaggedStart(*[
                DrawBorderThenFill(
                    graph
                ),
                # Write(
                #     graph_text
                # )
            ], lag_ratio=0.2),
            run_time=1
        )
        self.slide_pause(2)

        # self.play(
        #     b.animate.set_value(-1), run_time=1
        # )
        # self.play(
        #     b.animate.set_value(2), run_time=0.5
        # )
        # self.play(
        #     c.animate.set_value(1), run_time=1
        # )
        # self.play(
        #     c.animate.set_value(-2), run_time=0.5
        # )
        self.play(
            a.animate.set_value(1), run_time=1
        )
        self.slide_pause(1)
        self.play(
            b.animate.set_value(0), run_time=1
        )
        self.slide_pause(1)
        self.play(
            c.animate.set_value(0), run_time=1
        )
        self.slide_pause(3)
