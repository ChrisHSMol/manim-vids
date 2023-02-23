from manim import *
from helpers import *
import numpy as np
import math

slides = False
if slides:
    from manim_slides import Slide


class Egenskaber(Slide if slides else Scene):
    def construct(self):
        self.wavelength()

        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def wavelength(self):
        plane = NumberPlane(
            x_range=[-16, 16, 1],
            y_range=[-9, 9, 1],
            x_length=16,
            y_length=9,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            }
        )
        self.play(DrawBorderThenFill(plane))
        self.slide_pause()

        l_tracker = ValueTracker(4)
        amp = 4
        wave = always_redraw(lambda: plane.plot(
            lambda x: amp*np.sin(2*x*PI/l_tracker.get_value()),
            color=BLUE
        ))
        self.play(
            Create(wave),
            run_time=4,
            # rate_func=rate_functions.double_smooth
        )
        self.slide_pause()

        x0_tracker = ValueTracker(0)
        v_dots = always_redraw(lambda: VGroup(
            Dot(
                plane.c2p(x0_tracker.get_value(), wave.underlying_function(x0_tracker.get_value())),
                color=RED
            ),
            Dot(
                plane.c2p(x0_tracker.get_value() + l_tracker.get_value(),
                          wave.underlying_function(x0_tracker.get_value() + l_tracker.get_value())),
                color=RED
            )
        ))
        self.play(Create(v_dots))

        v_lines = always_redraw(lambda: VGroup(
            *[
                Line(
                    start=plane.c2p(plane.p2c(d.get_center())[0], -1.1*amp),
                    end=plane.c2p(plane.p2c(d.get_center())[0], 1.1*amp),
                    color=RED
                ).set_opacity(0.75) for d in v_dots
            ]
        ))
        self.play(
            Create(v_lines)
        )
        self.slide_pause()

        for x in [1, 3, 4.5, 6, l_tracker.get_value()/4]:
            self.play(
                x0_tracker.animate.set_value(x),
                run_time=2
            )
            xs_pause(self)
        self.slide_pause()

        length_brace = always_redraw(lambda: BraceBetweenPoints(
            point_1=plane.c2p(x0_tracker.get_value(), 1.1*amp),
            point_2=plane.c2p(x0_tracker.get_value() + l_tracker.get_value(), 1.1*amp),
            color=RED,
            direction=UP
        ))
        # length_number = always_redraw(lambda: DecimalNumber(
        #     l_tracker.get_value(),
        #     num_decimal_places=2,
        #     include_sign=False,
        #     color=RED
        # ).next_to(length_brace, UP))
        length_number = always_redraw(lambda: MathTex(
            f"{l_tracker.get_value():.2f}",
            color=RED
        ).next_to(length_brace, UP))
        self.play(
            GrowFromCenter(length_brace)
        )
        self.slide_pause()
        self.play(
            Write(length_number)
        )
        self.slide_pause()

        for x in np.random.uniform(-5, 5, 5):
            self.play(
                x0_tracker.animate.set_value(x),
                run_time=3
            )
            xs_pause(self)
        self.play(
            x0_tracker.animate.set_value(-0.5*l_tracker.get_value()),
            run_time=3
        )
        self.slide_pause()

        length_text = always_redraw(lambda:
            MathTex(
                r"\lambda=",
                f"{l_tracker.get_value():.2f}",
                color=RED
            ).next_to(length_brace, UP)
        )
        self.play(
            TransformMatchingTex(length_number, length_text, transform_mismatches=True)
        )
        self.slide_pause()

        for l in [5, 3, 2, 6, 1, 0.4, 10, 4]:
            self.play(
                l_tracker.animate.set_value(l),
                x0_tracker.animate.set_value(-0.5*l),
                run_time=4
            )
            self.slide_pause(0.1)

    def amplitude(self):

