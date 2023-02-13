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
            title = Tex("Sum ", "af to vektorer")
            title[0].set_color(YELLOW)
            _title, _title_ul_box = play_title(self, title, edge=UL)

        # self.sum_af_vektorer()
        self.kommutativ_regel()
        self.slide_pause(5.0)

    def slide_pause(self, t=0.5, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def _sum_af_vektorer(self):
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
        offset_a_x, offset_a_y = ValueTracker(0), ValueTracker(0)
        offset_b_x, offset_b_y = ValueTracker(0), ValueTracker(0)
        # vec_a = always_redraw(lambda: Vector(
        #     plane.c2p(x_a.get_value(), y_a.get_value()),
        #     color=RED
        # ).move_to(
        #     plane.c2p(offset_a_x.get_value(), offset_a_y.get_value()) + 0.5*plane.c2p(x_a.get_value(), y_a.get_value())
        # ))
        # vec_b = always_redraw(lambda: Vector(
        #     plane.c2p(x_b.get_value(), y_b.get_value()),
        #     color=BLUE
        # ).move_to(
        #     plane.c2p(offset_b_x.get_value(), offset_b_y.get_value()) + 0.5*plane.c2p(x_b.get_value(), y_b.get_value())
        # ))
        vec_a = always_redraw(lambda: Arrow(
            start=plane.c2p(offset_a_x.get_value(), offset_a_y.get_value()),
            end=plane.c2p(x_a.get_value(), y_a.get_value()),
            buff=0,
            color=RED
        ))
        vec_b = always_redraw(lambda: Arrow(
            start=plane.c2p(offset_b_x.get_value(), offset_b_y.get_value()),
            end=plane.c2p(x_b.get_value(), y_b.get_value()),
            buff=0,
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
            offset_a_x.animate.set_value(x_b.get_value()),
            offset_a_y.animate.set_value(y_b.get_value()),
            x_a.animate.set_value(x_a.get_value() + x_b.get_value()),
            y_a.animate.set_value(y_a.get_value() + y_b.get_value()),
        )
        self.slide_pause()

        sum_vector = always_redraw(lambda:
            Vector(
                plane.c2p(x_a.get_value() + x_b.get_value(), y_a.get_value() + y_b.get_value()),
                color=PURPLE
            )
        )
        sum_coord = always_redraw(lambda:
            Matrix(
                [[f"{x_a.get_value() + x_b.get_value():2.1f}"],
                 [f"{y_a.get_value() + y_b.get_value():2.1f}"]]
            ).next_to(sum_vector, UP).set_column_colors(sum_vector.get_color()).scale(0.75)
        )
        self.play(
            GrowArrow(sum_vector),
            # Write(sum_coord)
        )

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
        self.play(DrawBorderThenFill(plane))
        self.slide_pause()

        xa, ya = ValueTracker(4), ValueTracker(1)
        xb, yb = ValueTracker(2), ValueTracker(3)

        vec_a = always_redraw(lambda: Vector(
            plane.c2p(xa.get_value(), ya.get_value()),
            color=RED
        ))
        vec_b = always_redraw(lambda: Vector(
            plane.c2p(xb.get_value(), yb.get_value()),
            color=BLUE
        ))

        coord_a = always_redraw(lambda:
            Matrix(
                [[f"{xa.get_value():2.1f}"],
                 [f"{ya.get_value():2.1f}"]]
            ).set_column_colors(vec_a.get_color()).scale(0.75).next_to(vec_a, DR)
        )
        coord_b = always_redraw(lambda:
            Matrix(
                [[f"{xb.get_value():2.1f}"],
                 [f"{yb.get_value():2.1f}"]]
            ).set_column_colors(vec_b.get_color()).scale(0.75).next_to(vec_b, UL)
        )
        self.play(
            GrowArrow(vec_a),
            Write(coord_a)
        )
        self.slide_pause()

        for x, y in zip([1, -3, -2, 8, 4], [4, 1, -5, -1, 1]):
            self.play(
                xa.animate.set_value(x),
                ya.animate.set_value(y)
            )
            xs_pause(self)
        self.slide_pause()

        self.play(
            GrowArrow(vec_b),
            Write(coord_b)
        )
        self.slide_pause()

        vec_a_copy = always_redraw(lambda: Arrow(
            start=vec_b.get_end(),
            end=vec_b.get_end() + vec_a.get_end(),
            buff=0,
            color=RED,
        ).set_opacity(0.15))
        vec_b_copy = always_redraw(lambda: Arrow(
            start=vec_a.get_end(),
            end=vec_a.get_end() + vec_b.get_end(),
            buff=0,
            color=BLUE,
        ).set_opacity(0.15))
        self.play(LaggedStart(
            *[
                TransformFromCopy(vec_a, vec_a_copy),
                TransformFromCopy(vec_b, vec_b_copy)
            ],
            lag_ratio=0.75
        ), run_time=4)
        self.slide_pause()

        vec_sum = always_redraw(lambda: Vector(
            plane.c2p(
                xa.get_value() + xb.get_value(),
                ya.get_value() + yb.get_value()
            ),
            color=PURPLE
        ))
        coord_sum = always_redraw(lambda:
            Matrix(
                [[f"{xa.get_value() + xb.get_value():2.1f}"],
                 [f"{ya.get_value() + yb.get_value():2.1f}"]]
            ).set_column_colors(vec_sum.get_color()).scale(0.75).next_to(vec_sum, UR)
        )
        for i in range(2):
            if i:
                self.play(
                    GrowArrow(vec_sum),
                    Write(coord_sum)
                )
            for x, y in zip([1, -3, -2, 8, 4], [4, 1, -5, -1, 1]):
                self.play(
                    xa.animate.set_value(x),
                    ya.animate.set_value(y)
                )
                xs_pause(self)
            self.slide_pause()

        coord_a_fixed = always_redraw(lambda:
            Matrix(
                [[f"{xa.get_value():2.1f}"],
                 [f"{ya.get_value():2.1f}"]]
            ).set_column_colors(vec_a.get_color()).scale(0.75).to_edge(DL)
        )
        coord_b_fixed = always_redraw(lambda:
            Matrix(
                [[f"{xb.get_value():2.1f}"],
                 [f"{yb.get_value():2.1f}"]]
            ).set_column_colors(vec_b.get_color()).scale(0.75).next_to(coord_a_fixed, RIGHT, buff=1)
        )
        coord_sum_fixed = always_redraw(lambda:
            Matrix(
                [[f"{xa.get_value() + xb.get_value():2.1f}"],
                 [f"{ya.get_value() + yb.get_value():2.1f}"]]
            ).set_column_colors(vec_sum.get_color()).scale(0.75).next_to(coord_b_fixed, RIGHT, buff=1)
        )
        self.play(
            TransformFromCopy(coord_a, coord_a_fixed),
            TransformFromCopy(coord_b, coord_b_fixed),
            TransformFromCopy(coord_sum, coord_sum_fixed),
            FadeOut(coord_a),
            FadeOut(coord_b),
            FadeOut(coord_sum),
        )
        self.slide_pause()

        eq_sum_text = always_redraw(lambda: VGroup(
            Tex("+").move_to(between_mobjects(coord_a_fixed, coord_b_fixed)),
            Tex("=").move_to(between_mobjects(coord_b_fixed, coord_sum_fixed))
        ))
        self.play(FadeIn(eq_sum_text))
        self.slide_pause()

        for x, y in zip([1, -3, -2, 8, 4], [4, 1, -5, -1, 1]):
            self.play(
                xa.animate.set_value(x),
                ya.animate.set_value(y)
            )
            xs_pause(self)
        self.slide_pause()

        for x, y in zip([4, 3, -2, -7, 2], [1, -7, -5, 1, 3]):
            self.play(
                xb.animate.set_value(x),
                yb.animate.set_value(y)
            )
            xs_pause(self)
        self.slide_pause()

    def kommutativ_regel(self):
        beskrivelse = VGroup(
            Tex("Den ", "kommutative", " regneregel siger,"),
            Tex("at det er ligegyldigt i hvilken rækkefølge"),
            Tex("man lægger ", "to vektorer", " sammen.")
        ).arrange(DOWN, aligned_edge=LEFT)
        beskrivelse[0][1].set_color(YELLOW)
        beskrivelse[2][1].set_color((RED, BLUE))
        self.play(
            Write(beskrivelse)
        )
        self.slide_pause()
        regel = MathTex(r"\vec{a}", "+", r"\vec{b}", "=", r"\vec{b}", "+", r"\vec{a}")
        regel[0].set_color(RED)
        regel[6].set_color(RED)
        regel[2].set_color(BLUE)
        regel[4].set_color(BLUE)
        self.play(
            beskrivelse.animate.shift(2*UP),
            FadeIn(regel, shift=2*UP)
        )
        self.slide_pause()
        self.play(
            FadeOut(VGroup(beskrivelse, regel))
        )

        plane_left = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-6, 6, 1],
            x_length=6,
            y_length=6,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            }
        ).to_edge(LEFT).add_coordinates()
        plane_right = plane_left.copy().to_edge(RIGHT)
        self.play(
            DrawBorderThenFill(
                VGroup(plane_left, plane_right)
            )
        )
        self.slide_pause()

        xa, ya = ValueTracker(5), ValueTracker(2)
        xb, yb = ValueTracker(-1), ValueTracker(3)
        ab_opa = ValueTracker(1)
        vec_a_left = always_redraw(lambda: Arrow(
            plane_left.c2p(0, 0), plane_left.c2p(xa.get_value(), ya.get_value()), color=RED, buff=0
        ).set_opacity(ab_opa.get_value()))
        vec_b_left = always_redraw(lambda: Arrow(
            plane_left.c2p(0, 0), plane_left.c2p(xb.get_value(), yb.get_value()), color=BLUE, buff=0
        ).set_opacity(ab_opa.get_value()))
        vec_a_right = always_redraw(lambda: Arrow(
            plane_right.c2p(0, 0), plane_right.c2p(xa.get_value(), ya.get_value()), color=RED, buff=0
        ).set_opacity(ab_opa.get_value()))
        vec_b_right = always_redraw(lambda: Arrow(
            plane_right.c2p(0, 0), plane_right.c2p(xb.get_value(), yb.get_value()), color=BLUE, buff=0
        ).set_opacity(ab_opa.get_value()))

        vec_a_text = VGroup(
            MathTex(r"\vec{a}").set_color(vec_a_left.get_color()).next_to(plane_left, UP).shift(0.5*LEFT),
            MathTex(r"\vec{a}").set_color(vec_a_right.get_color()).next_to(plane_right, UP).shift(0.5*RIGHT)
        )
        vec_b_text = VGroup(
            MathTex(r"\vec{b}").set_color(vec_b_left.get_color()).next_to(plane_left, UP).shift(0.5*RIGHT),
            MathTex(r"\vec{b}").set_color(vec_b_right.get_color()).next_to(plane_right, UP).shift(0.5*LEFT)
        )

        self.play(
            *[GrowArrow(v) for v in [vec_a_left, vec_a_right, vec_b_right, vec_b_left]],
            Write(VGroup(vec_a_text, vec_b_text))
        )
        self.slide_pause()

        # for x, y in zip([-2, 1, 5], [1, 3, 2]):
        for ax, bx, ay, by in np.random.uniform(low=-5, high=5, size=(5, 4)):
            self.play(
                xa.animate.set_value(ax),
                ya.animate.set_value(ay),
                xb.animate.set_value(bx),
                yb.animate.set_value(by),
            )
            xs_pause(self)

        vec_b_left_copy = always_redraw(lambda: Arrow(
            start=plane_left.c2p(xa.get_value(), ya.get_value()),
            end=plane_left.c2p(xa.get_value() + xb.get_value(), ya.get_value() + yb.get_value()),
            color=vec_b_left.get_color(),
            buff=0
        ).set_opacity(ab_opa.get_value()))
        vec_a_right_copy = always_redraw(lambda: Arrow(
            start=plane_right.c2p(xb.get_value(), yb.get_value()),
            end=plane_right.c2p(xb.get_value() + xa.get_value(), yb.get_value() + ya.get_value()),
            color=vec_a_right.get_color(),
            buff=0
        ).set_opacity(ab_opa.get_value()))
        self.play(
            TransformFromCopy(vec_b_left, vec_b_left_copy),
            TransformFromCopy(vec_a_right, vec_a_right_copy),
            FadeOut(VGroup(vec_a_right, vec_b_left))
        )
        self.slide_pause()

        vec_sum_left = always_redraw(lambda: Arrow(
            plane_left.c2p(0, 0),
            plane_left.c2p(xa.get_value() + xb.get_value(), ya.get_value() + yb.get_value()),
            color=PURPLE, buff=0
        ))
        vec_sum_right = always_redraw(lambda: Arrow(
            plane_right.c2p(0, 0),
            plane_right.c2p(xb.get_value() + xa.get_value(), yb.get_value() + ya.get_value()),
            color=PURPLE, buff=0
        ))
        eq_symbols = VGroup(
            Tex("+").move_to(between_mobjects(vec_a_text[0], vec_b_text[0])),
            Tex("+").move_to(between_mobjects(vec_b_text[1], vec_a_text[1])),
            # Tex("=").move_to(between_mobjects(vec_b_text[0], vec_b_text[1]))
        )
        self.play(
            *[GrowArrow(v) for v in [vec_sum_right, vec_sum_left]],
            ab_opa.animate.set_value(0.25),
            FadeIn(eq_symbols[:2])
        )
        self.slide_pause()

        # for ax, bx, ay, by in zip(
        #     [3, 5, 5, 5, -2],
        #     [-1, -1, -4, -1, -2],
        #     [-1, 2, 2, 2, -1],
        #     [3, 3, -1, 3, 5]
        # ):
        for ax, bx, ay, by in np.random.uniform(low=-3, high=3, size=(5, 4)):
            self.play(
                xa.animate.set_value(ax),
                xb.animate.set_value(bx),
                ya.animate.set_value(ay),
                yb.animate.set_value(by)
            )
            xs_pause(self)
        self.play(
            xa.animate.set_value(-2),
            xb.animate.set_value(-2),
            ya.animate.set_value(-1),
            yb.animate.set_value(5)
        )

        regel.to_edge(UP, buff=0)
        self.play(
            plane_left.animate.move_to(ORIGIN),
            plane_right.animate.move_to(ORIGIN),
            Transform(VGroup(vec_a_text, vec_b_text, eq_symbols), regel),
            run_time=3
        )
        self.slide_pause()

