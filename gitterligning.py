from manim import *
from helpers import *
import numpy as np

slides = False
if slides:
    from manim_slides import Slide


class GitterLigning(Slide if slides else Scene):
    def construct(self):
        # self.udstyr()
        self.gitter_ligning()
        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t=t, slides_bool=slides_bool)

    def udstyr(self):
        laser_gun = SVGMobject("SVGs/laser_gun.svg").to_edge(LEFT).shift(0.25*DOWN)
        laser_gun.set_color(invert_color(laser_gun.get_color()))
        laser_name = Tex("Laser").set_color(color_gradient([BLUE, GREEN, RED], 3)).next_to(laser_gun, UP)
        self.play(
            LaggedStart(
                DrawBorderThenFill(laser_gun),
                Write(laser_name),
                lag_ratio=0.5
            ),
            run_time=1
        )
        self.slide_pause()

        linjer = ValueTracker(200)
        gitter_top = Line(1*DOWN, 1*UP, color=PINK).next_to(laser_gun, RIGHT, buff=2).shift(0.25*UP)
        gitter_ridser = always_redraw(lambda:
            VGroup(
                Square(5, color=gitter_top.get_color()),
                *[
                    Line(
                        start=[i, -2.5, 0],
                        end=[i, 2.5, 0],
                        stroke_width=0.5
                    ) for i in np.linspace(-2.5, 2.5, int(linjer.get_value()/10))
                ]
            ).next_to(gitter_top, RIGHT)
        )
        gitter_name = always_redraw(lambda:
            Tex(
                f"Gitter med {int(linjer.get_value())} ridser pr. mm",
                color=gitter_top.get_color()
            ).next_to(VGroup(gitter_ridser, gitter_top), UP)
        )
        gitter_name2 = always_redraw(lambda:
            # Tex(f"Gitter, d=1/{int(linjer.get_value())}", color=gitter_top.get_color()).next_to(
            #     gitter_top, UP)
            Tex(
                f"{int(linjer.get_value())} ridser",
                color=gitter_top.get_color()
            ).next_to(gitter_top, UP)
        )
        self.play(
            LaggedStart(
                # Create(gitter_top),
                Create(gitter_ridser),
                Write(gitter_name),
                lag_ratio=0.5
            ),
            run_time=2
        )
        self.play(
            linjer.animate.set_value(200),
            run_time=5
        )
        self.slide_pause()

        self.play(
            Transform(gitter_ridser, gitter_top),
            Transform(gitter_name, gitter_name2)
        )
        self.remove(gitter_name, gitter_ridser)
        self.add(gitter_top, gitter_name2)

        wall = Line(5*DOWN, 5*UP).to_edge(RIGHT)
        wall_tekst = Tex("Væg").next_to(wall, LEFT).shift(3.5*UP)
        self.play(
            Create(wall),
            Create(wall_tekst),
        )
        self.slide_pause()
        self.remove(*[m for m in self.mobjects])

    def gitter_ligning(self):
        linjer = ValueTracker(200)  # mm^-1
        wlength = ValueTracker(400)  # nm
        # dist = ValueTracker(5)  # m

        laser_gun = SVGMobject("SVGs/laser_gun.svg").to_edge(LEFT).shift(0.25*DOWN)
        laser_gun.set_color(invert_color(laser_gun.get_color()))
        laser_name = Tex("Laser").set_color(color_gradient([BLUE, GREEN, RED], 3)).next_to(laser_gun, UP)
        wall = Line(5 * DOWN, 5 * UP).to_edge(RIGHT)
        wall_name = Tex("Væg").next_to(wall, LEFT).shift(3.5 * UP)
        gitter_top = Line(1*DOWN, 1*UP, color=PINK).next_to(laser_gun, RIGHT, buff=2).shift(0.25*UP)
        # gitter_name = Tex("Gitter", color=gitter_top.get_color()).next_to(gitter_top, UP)
        gitter_name = always_redraw(lambda:
            Tex(
                f"{int(linjer.get_value())} ridser",
                color=gitter_top.get_color()
            ).next_to(gitter_top, UP)
        )
        self.add(laser_gun, laser_name, wall, wall_name, gitter_top, gitter_name)

        dist_gw = ValueTracker((wall.get_left() - gitter_top.get_left())[0])
        dist_lg = ValueTracker((gitter_top.get_left() - laser_gun.get_left())[0])

        laser_line = Line(
            start=laser_gun.get_right() + 0.25*UP,
            end=gitter_top.get_left(),
            stroke_width=2,
            color=RED
        )
        diff_lines = always_redraw(lambda:
            VGroup(
                *[
                    Line(
                        start=gitter_top.get_right(),
                        end=wall.get_left() + dist_gw.get_value() * np.tan(
                            np.arcsin(
                                n * wlength.get_value()*10**(-9) * linjer.get_value()*10**3
                            )
                        ) * UP,
                        stroke_width=2*np.exp(-0.25*np.abs(n)),
                        color=laser_line.get_color()
                    ) for n in np.arange(-5, 5.1, 1)
                ]
            )
        )
        self.play(
            Create(laser_line),
            rate_func=rate_functions.linear,
            run_time=dist_lg.get_value()
        )
        self.play(
            *[Create(dline) for dline in diff_lines],
            rate_func=rate_functions.linear,
            run_time=dist_gw.get_value()
        )
        self.slide_pause()

        self.play(
            linjer.animate.set_value(300),
            run_time=5
        )


