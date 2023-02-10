from manim import *
from helpers import *
import numpy as np
import math

slides = False
if slides:
    from manim_slides import Slide


class BasicVectors(Slide if slides else Scene):
    def construct(self):
        bool_play_titles = True
        if bool_play_titles:
            title = Tex("Grundlæggende om ", "vektorer")
            title[1].set_color(YELLOW)
            _title, _title_ul_box = play_title(self, title, edge=DL)
        self.om_vektorer()
        self.slide_pause(0.5)

        if bool_play_titles:
            title2 = Tex("Vektorers ", "koordinater").set_z_index(_title.get_z_index())
            title2[1].set_color(BLUE)
            self.play(_title.animate.set_opacity(1.0).move_to([0, 0, 0]))
            self.play(Transform(_title, title2))
            self.play(_title.animate.set_opacity(0.15).to_edge(DL, buff=0.05))

        self.vektor_koordinater()
        self.play(*[FadeOut(m) for m in self.mobjects if m != _title])
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
        plane = NumberPlane().add_coordinates()
        self.play(
            FadeIn(plane),
            run_time=0.5
        )
        scene_marker("Punkters koordinater")
        tekst_punkt = Tex("Koordinater for ", "punkter").to_edge(UL).set_z_index(plane.get_z_index()+2)
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
                "(", f"{x_tracker.get_value():3.1f}", "; ", f"{y_tracker.get_value():3.1f}", ")"
            ).next_to(point, DR).set_z_index(point.get_z_index())
        )
        point_coord = VGroup(
            point_coord,
            SurroundingRectangle(point_coord, color=BLACK, fill_color=BLACK, buff=0.1, stroke_width=0.1,
                                 fill_opacity=0.5, z_index=point_coord.get_z_index() - 1)
        )
        vert_line = always_redraw(lambda:
            Line(
                start=plane.c2p(x_tracker.get_value(), 0, 0),
                end=plane.c2p(x_tracker.get_value(), y_tracker.get_value(), 0),
                color=RED_C,
                stroke_width=3
            )
        )
        hori_line = always_redraw(lambda:
            Line(
                start=plane.c2p(0, y_tracker.get_value(), 0),
                end=plane.c2p(x_tracker.get_value(), y_tracker.get_value(), 0),
                color=RED_C,
                stroke_width=3
            )
        )

        self.slide_pause(0.5)
        self.play(
            DrawBorderThenFill(point),
            FadeIn(point_coord),
            run_time=0.5
        )
        self.add(vert_line, hori_line)
        self.slide_pause(0.5)

        i = 0
        for x, y in zip(
            [1, 3, -1, -4, 3, 0],
            [0, 1, 3, -2, -1, 0]
        ):
            self.play(
                x_tracker.animate.set_value(x),
                y_tracker.animate.set_value(y),
            )
            xs_pause(self)
            if i == 1:
                ts = VGroup(
                    DecimalNumber(y_tracker.get_value(), num_decimal_places=0,
                                  color=vert_line.get_color()).scale(0.75).next_to(vert_line, LEFT),
                    DecimalNumber(x_tracker.get_value(), num_decimal_places=0,
                                  color=hori_line.get_color()).scale(0.75).next_to(hori_line, DOWN),
                )
                self.play(FadeIn(ts))
                self.slide_pause(0.5)
                self.play(FadeOut(ts))
            i += 1
        self.slide_pause(0.5)
        self.play(
            FadeOut(point),
            FadeOut(point_coord),
            run_time=0.5
        )
        # self.remove(vert_line, hori_line)
        self.slide_pause(0.5)

        scene_marker("Vektorers koordinater")
        tekst_vektor = Tex("Koordinater for ", "vektorer").to_edge(UL).set_z_index(plane.get_z_index()+2)
        tekst_vektor[1].set_color(YELLOW)
        tekst_vektor = VGroup(
            tekst_vektor,
            SurroundingRectangle(tekst_vektor, color=BLACK, fill_color=BLACK, buff=0.1, stroke_width=0.1,
                                 fill_opacity=0.5, z_index=tekst_vektor.get_z_index() - 1)
        )
        self.play(AnimationGroup(
            FadeOut(tekst_punkt[0][-1], shift=UP*0.5),
            FadeIn(tekst_vektor[0][-1], shift=UP*0.5)
        ))
        self.slide_pause(0.5)

        vector = always_redraw(lambda:
            Vector(
                direction=plane.c2p(x_tracker.get_value(), y_tracker.get_value(), 0),
                color=YELLOW
            )
        )
        self.add(vector)
        self.play(
            x_tracker.animate.set_value(1.0),
            y_tracker.animate.set_value(2.0)
        )
        self.slide_pause(0.5)

        vector_coord = always_redraw(lambda:
            Matrix(
                [[f"{x_tracker.get_value():3.2f}"],
                 [f"{y_tracker.get_value():3.2f}"]]
            ).next_to(vector, RIGHT)
        )
        self.play(
            DrawBorderThenFill(
                vector_coord
            )
        )

        for x, y in zip(
            [1, 3, -1, -4, 3, 2],
            [0, 1, 3, -2, -1, 1]
        ):
            self.play(
                x_tracker.animate.set_value(x),
                y_tracker.animate.set_value(y),
            )
            xs_pause(self)
        self.slide_pause(0.5)
        self.play(FadeOut(vector_coord), run_time=0.5)

        scene_marker("Polære koordinater")
        vek_bue = always_redraw(lambda:
            Arc(
                radius=0.75,
                start_angle=0,
                angle=vector.get_angle(),
                color=YELLOW
            )
        )
        hori_line2 = always_redraw(lambda:
            Line(
                start=plane.c2p(0, 0, 0),
                end=plane.c2p(x_tracker.get_value(), 0, 0),
                color=RED_C,
                stroke_width=3
            )
        )
        self.play(
            # FadeOut(VGroup(vert_line, hori_line)),
            hori_line.animate.move_to(hori_line2),
            Create(
                vek_bue
            )
        )
        self.remove(hori_line)
        self.add(hori_line2)

        self.slide_pause(0.5)
        self.play(
            x_tracker.animate.set_value(5.0),
            y_tracker.animate.set_value(3.0),
        )
        vec_ang = always_redraw(lambda:
            # DecimalNumber(
            #     vector.get_angle() * 180/PI,
            #     num_decimal_places=1,
            #     include_sign=True,
            #     color=vek_bue.get_color()
            # ).scale(0.75).next_to(vek_bue, RIGHT)
            MathTex(f"{vector.get_angle() * 180/PI:.1f}^\circ",
                    color=vek_bue.get_color()).scale(0.75).next_to(vek_bue, RIGHT)
        )
        vec_len = always_redraw(lambda:
            DecimalNumber(
                vector.get_length(),
                num_decimal_places=1,
                color=vector.get_color()
            ).scale(0.75).next_to(vector, np.mean([UR, DL])).shift(0.5*UP)
        )
        self.play(
            Write(vec_ang),
            Write(vec_len)
        )
        self.slide_pause(0.5)

        for x, y in zip(
            [3, -1, -4, 3, 4],
            [1, 3, -2, -1, 3]
        ):
            self.play(
                x_tracker.animate.set_value(x),
                y_tracker.animate.set_value(y),
            )
            xs_pause(self)
        self.slide_pause(0.5)


class RegnereglerVektorer(Slide if slides else Scene):
    def construct(self):
        bool_play_title = False
        if bool_play_title:
            title = Tex("Vektorers ", "regneregler")
            title[1].set_color(YELLOW)
            _title, _title_ul_box = play_title(self, title, edge=DL)

        self.sum_af_vektorer()
        self.slide_pause(5.0)

    def slide_pause(self, t=0.5, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def sum_af_vektorer(self):
        plane = NumberPlane(
            x_range=[-16, 16, 1],
            y_range=[-9, 9, 1],
            x_length=16,
            y_length=9,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 4,
                "stroke_opacity": 0.3
            }
        )
        x_a, y_a = ValueTracker(2), ValueTracker(1)
        x_b, y_b = ValueTracker(1), ValueTracker(2)
        vec_a = always_redraw(lambda: Vector(
            plane.c2p(x_a.get_value(), y_a.get_value()),
            color=RED
        ))
        vec_b = always_redraw(lambda: Vector(
            plane.c2p(x_b.get_value(), y_b.get_value()),
            color=BLUE
        ))

        self.play(
            DrawBorderThenFill(
                plane
            )
        )
        self.slide_pause()

        v_line_a = always_redraw(lambda:
            DashedLine(start=plane.c2p(x_a.get_value(), 0, 0),
                       end=plane.c2p(x_a.get_value(), y_a.get_value(), 0),
                       color=vec_a.get_color(), stroke_width=2)
        )
        h_line_a = always_redraw(lambda:
            DashedLine(start=plane.c2p(0, y_a.get_value(), 0),
                       end=plane.c2p(x_a.get_value(), y_a.get_value(), 0),
                       color=vec_a.get_color(), stroke_width=2)
        )
        v_line_b = always_redraw(lambda:
            DashedLine(start=plane.c2p(x_b.get_value(), 0, 0),
                       end=plane.c2p(x_b.get_value(), y_b.get_value(), 0),
                       color=vec_b.get_color(), stroke_width=2)
        )
        h_line_b = always_redraw(lambda:
            DashedLine(start=plane.c2p(0, y_b.get_value(), 0),
                       end=plane.c2p(x_b.get_value(), y_b.get_value(), 0),
                       color=vec_b.get_color(), stroke_width=2)
        )

        coord_a = always_redraw(lambda:
            Matrix(
                [[f"{x_a.get_value():2.1f}"],
                 [f"{y_a.get_value():2.1f}"]]
            ).next_to(vec_a, RIGHT).set_column_colors(vec_a.get_color()).scale(0.75)
        )
        coord_b = always_redraw(lambda:
            Matrix(
                [[f"{x_b.get_value():2.1f}"],
                 [f"{y_b.get_value():2.1f}"]]
            ).next_to(vec_b, UP).set_column_colors(vec_b.get_color()).scale(0.75)
        )

        va = VGroup(vec_a, coord_a, v_line_a, h_line_a)
        vb = VGroup(vec_b, coord_b, v_line_b, h_line_b)
        self.play(
            GrowArrow(vec_a),
            Write(coord_a),
            Create(VGroup(v_line_a, h_line_a))
        )
        self.slide_pause()
        for x, y in zip([4, 1, 2], [-2, 3, 1]):
            self.play(
                x_a.animate.set_value(x),
                y_a.animate.set_value(y),
                run_time=2
            )
        self.slide_pause()

        self.play(
            TransformFromCopy(va, vb),
            run_time=2
        )
        self.slide_pause()

        self.play(
            x_a.animate.set_value(4),
            y_b.animate.set_value(4),
            run_time=2
        )
        self.slide_pause()

        self.play(
            vec_a.animate.set_opacity(0.25),
            vec_b.animate.set_opacity(0.25)
        )

