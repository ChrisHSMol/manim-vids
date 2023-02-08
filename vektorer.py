from manim import *
from helpers import *
import numpy as np
import math

slides = False
if slides:
    from manim_slides import Slide


class BasicVectors(Slide if slides else Scene):
    def construct(self):
        bool_play_titles = False
        if bool_play_titles:
            title = Tex("Grundlæggende om ", "vektorer")
            title[1].set_color(YELLOW)
            _title, _title_ul_box = play_title(self, title, edge=DL)
        # self.om_vektorer()
        self.slide_pause(0.5)

        if bool_play_titles:
            title2 = Tex("Vektorers ", "koordinater").set_z_index(_title.get_z_index())
            title2[1].set_color(BLUE)
            self.play(_title.animate.set_opacity(1.0).move_to([0, 0, 0]))
            self.play(Transform(_title, title2))
            self.play(_title.animate.set_opacity(0.15).to_edge(DL, buff=0.05))

        self.vektor_koordinater()
        if bool_play_titles:
            play_title_reverse(self, _title, pos=[0, 0, 0])
        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def om_vektorer(self):
        nline = NumberLine(include_numbers=True).set_z_index(6, family=True)
        srec1 = Rectangle(width=16, height=4, z_index=4)\
            .set_style(fill_opacity=1, stroke_width=0, fill_color=BLACK).to_edge(DOWN, buff=0)
        srec2 = srec1.copy().to_edge(UP, buff=0)
        plane = NumberPlane(z_index=2)
        tekst_tal = Tex("Tal har en ", "størrelse").set_z_index(nline.get_z_index()+2)
        tekst_tal[1].set_color(GREEN)
        tekst_vek = Tex("Vektorer har en ", "størrelse", " og en ", "retning").set_z_index(nline.get_z_index()+2)
        tekst_vek[1].set_color(GREEN)
        tekst_vek[3].set_color(YELLOW)

        tekst_tal = VGroup(
            tekst_tal,
            SurroundingRectangle(tekst_tal, color=BLACK, fill_color=BLACK, buff=0.1, stroke_width=0.1,
                                 fill_opacity=0.5, z_index=nline.get_z_index()+1)
        )
        tekst_vek = VGroup(
            tekst_vek,
            SurroundingRectangle(tekst_vek, color=BLACK, fill_color=BLACK, buff=0.1, stroke_width=0.1,
                                 fill_opacity=0.5, z_index=nline.get_z_index()+1)
        )

        scene_marker("Tal vs. vektorer")
        self.play(
            Write(tekst_tal)
        )
        self.slide_pause()
        self.play(
            tekst_tal.animate.shift(1.5*UP),
            # Write(tekst_vek)
        )

        x_tracker = ValueTracker(0)
        size_tracker = ValueTracker(1)
        dot = always_redraw(lambda:
            Dot(
                [x_tracker.get_value(), 0, 0],
                color=GREEN,
                z_index=nline.get_z_index() + 1
                # .shift(0.1*UP)
            ).scale(size_tracker.get_value())
        )
        self.play(
            Create(dot)
        )
        self.slide_pause()
        for factor in [8, 0.1, 2]:
            self.play(
                # dot.animate.scale(factor)
                size_tracker.animate.set_value(factor)
            )
            xs_pause(self)

        dotline = always_redraw(lambda:
            Line(
                start=nline.n2p(0),
                end=nline.n2p(x_tracker.get_value()),
                stroke_width=8,
                color=dot.get_color(),
                z_index=dot.get_z_index()
            )
        )
        dot_text = always_redraw(lambda:
            DecimalNumber(
                dot.get_center()[0],
                include_sign=True,
                num_decimal_places=2,
                color=dot.get_color()
            ).next_to(dot, UP)
        )
        self.add(dotline)
        self.slide_pause()
        self.play(
            DrawBorderThenFill(nline),
            TransformFromCopy(tekst_tal[0][-1], dot_text)
        )
        self.slide_pause()
        for x in [2, -6, 0]:
            self.play(
                x_tracker.animate.set_value(x)
            )
            xs_pause(self)
        self.slide_pause(0.5)

        self.play(FadeOut(dot_text, dot))

        tekst_vek.move_to(tekst_tal)
        self.play(AnimationGroup(
            FadeOut(tekst_tal, shift=UP*0.5),
            FadeIn(tekst_vek, shift=UP*0.5)
        ))
        self.slide_pause(0.5)
        scene_marker("Vektorer")
        self.add(srec1, srec2, plane)
        self.play(
            srec1.animate.shift(5*DOWN),
            srec2.animate.shift(5*UP),
            tekst_vek.animate.to_edge(UP),
            FadeOut(nline)
        )
        self.remove(srec1, srec2, dotline)
        plane.set_z_index(0)

        x_tracker = ValueTracker(0)
        y_tracker = ValueTracker(0)
        size_tracker.set_value(0.25)
        vektor = always_redraw(lambda:
            Vector(
                # dot.get_center(),
                plane.c2p(x_tracker.get_value(), y_tracker.get_value(), 0),
                color=GREEN
            ).set_z_index(plane.get_z_index() + 1)
        )
        vek_bue = always_redraw(lambda:
            Arc(
                # radius=0.25,
                radius=size_tracker.get_value(),
                start_angle=0,
                # angle=math.atan(y_tracker.get_value()/x_tracker.get_value()),
                angle=vektor.get_angle(),
                color=YELLOW
            )
        )

        self.slide_pause(0.5)
        self.add(vektor)
        self.slide_pause(0.5)
        # for x, y in zip([2, 1, -3, -2, 1], [1, 2, 3, -1, 0]):
        for x, y in zip([1, -1, 0, 0, 0, 0, 1], [0, 0, 0, 1, -1, 0, 0]):
            self.play(
                x_tracker.animate.set_value(x),
                y_tracker.animate.set_value(y),
                run_time=1
            )
            xs_pause(self)
        self.slide_pause(0.5)
        self.add(vek_bue)
        for x, y in zip([2, -1, -3, 1], [1, 2, -2, 0]):
            self.play(
                x_tracker.animate.set_value(x),
                y_tracker.animate.set_value(y),
                run_time=1
            )
            xs_pause(self)
        self.slide_pause(0.5)

        i = 0
        for x, y in zip([np.sqrt(3)/2, 0.5, 0, -0.5, -np.sqrt(3)/2, -1], [0.5, np.sqrt(3)/2, 1, np.sqrt(3)/2, 0.5, 0]):
            self.play(
                x_tracker.animate.set_value(x),
                y_tracker.animate.set_value(y),
                run_time=0.25,
                rate_func=rate_functions.linear
            )
            if i == 0:
                self.play(
                    # vek_bue.animate.set_radius(1.0),
                    size_tracker.animate.set_value(1.0),
                    run_time=1.0
                )
                i += 1

        self.slide_pause(0.5)
        unit_circle = Circle(radius=1.0, color=vek_bue.get_color())
        self.play(Create(unit_circle), x_tracker.animate.set_value(0), run_time=1)
        self.remove(vek_bue)

        self.slide_pause(0.5)
        self.play(ApplyWave(unit_circle), run_time=2)
        self.slide_pause(0.5)
        self.play(
            FadeOut(VGroup(
                plane,
                unit_circle,
                tekst_vek
            ))
        )

    def vektor_koordinater(self):
        plane = NumberPlane()
        self.play(
            FadeIn(plane),
            run_time=0.5
        )
        tekst_punkt = Tex("Vi starter med ", "punkter").to_edge(UL).set_z_index(plane.get_z_index()+2)
        tekst_punkt[1].set_color(RED)
        tekst_punkt = VGroup(
            tekst_punkt,
            SurroundingRectangle(tekst_punkt, color=BLACK, fill_color=BLACK, buff=0.1, stroke_width=0.1,
                                 fill_opacity=0.5, z_index=tekst_punkt.get_z_index() - 1)
        )
        self.play(
            FadeIn(tekst_punkt)
        )

        x_tracker = ValueTracker(0)
        y_tracker = ValueTracker(0)
        point = always_redraw(lambda:
            Dot(
                plane.c2p(x_tracker.get_value(), y_tracker.get_value(), 0),
                color=RED,
                radius=0.125
            )
        )
        point_coord = always_redraw(lambda:
            Tex(
                "(", x_tracker.get_value(), "; ", y_tracker.get_value(), ")"
            ).next_to(point, DR).set_z_index(point.get_z_index())
        )
        point_coord = VGroup(
            point_coord,
            SurroundingRectangle(point_coord, color=BLACK, fill_color=BLACK, buff=0.1, stroke_width=0.1,
                                 fill_opacity=0.5, z_index=point_coord.get_z_index() - 1)
        )

        self.play(
            DrawBorderThenFill(point),
            FadeIn(point_coord),
            run_time=0.5
        )

