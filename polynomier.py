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
        self.etymologi()
        # self.slide_pause()
        # self.andengrad()

        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t=t, slides_bool=slides_bool)

    def topgraph(self, func, ytop):
        for x in np.arange(5, 10, 0.01):
            y = func(x)
            if np.abs(y - ytop) <= 0.5:
                return x

    def etymologi(self):
        play_latest = True
        open_quote = Tex(r"Kært ", "barn ", "har ", "mange ", "navne")
        if not play_latest:
            self.play(
                Write(open_quote),
                run_time=3
            )
            self.slide_pause()
        else:
            self.add(open_quote)

        mit_navn = Tex("Christoffer ", "Hammar ", "Skovgaard ", "Møller").next_to(open_quote, DOWN)
        if not play_latest:
            self.play(
                Write(mit_navn),
                run_time=2
            )
            self.play(FadeOut(mit_navn), run_time=0.5)
            self.slide_pause()

            self.play(
                open_quote[-2].animate.set_color(YELLOW),
                open_quote[-1].animate.set_color(BLUE)
            )
            self.slide_pause()
        else:
            open_quote[-2].set_color(YELLOW),
            open_quote[-1].set_color(BLUE)

        roots = VGroup(
            Tex("poly").set_color(YELLOW),
            Tex("nomen").set_color(BLUE)
        ).arrange(RIGHT).next_to(open_quote[-2:], DOWN)
        polytekst = Tex(r"polynomium").set_color(color_gradient((YELLOW, BLUE), 2)).next_to(roots, DOWN)
        if not play_latest:
            for i, word in enumerate(roots):
                self.play(
                    TransformFromCopy(
                        open_quote[i-2], word
                    ),
                    run_time=1
                )
                self.slide_pause()
            self.play(
                TransformFromCopy(
                    roots, polytekst
                )
            )
            self.slide_pause()
            self.play(
                FadeOut(roots),
                FadeOut(open_quote),
                polytekst.animate.set_color(GREEN).to_edge(UL).set_z_index(3),
                run_time=2
            )
            self.slide_pause()
        else:
            self.add(polytekst.set_color(GREEN).to_edge(UL))
            self.remove(open_quote)

        # polyrect = get_background_rect(polytekst, buff=0.01)
        # self.add(polyrect)

        pmap = {
            "a_0": YELLOW_A,
            "a_1": YELLOW_B,
            "a_2": YELLOW_C,
            "a_3": YELLOW_D,
            "a_4": YELLOW_E,
            "x": RED,
            # "^": BLUE
        }
        polynomier = VGroup(
            MathTex(
                "y_0", " = ", "a_0",
            ),
            MathTex(
                "y_1", " = ", "a_0", " + ", "a_1", r"\cdot", "x",
            ),
            MathTex(
                "y_2", " = ", "a_0", " + ", "a_1", r"\cdot", "x", " + ", "a_2", r"\cdot", "x", "^2",
            ),
            MathTex(
                "y_3", " = ", "a_0" " + ", "a_1", r"\cdot", "x", " + ",
                "a_2", r"\cdot", "x", "^2", " + ", "a_3", r"\cdot", "x", "^3",
            ),
            MathTex(
                "y_4", " = ", "a_0", " + ", "a_1", r"\cdot", "x", " + ", "a_2", r"\cdot", "x", "^2", " + ",
                "a_3", r"\cdot", "x", "^3", " + ", "a_4", r"\cdot", "x", "^4",
            )
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        for poly in polynomier:
            poly.set_color_by_tex_to_color_map(pmap)

        if not play_latest:
            self.play(
                Write(polynomier[0])
            )
            self.slide_pause()
            for i, poly in enumerate(polynomier[1:]):
                self.play(
                    TransformMatchingTex(
                        polynomier[i].copy(), poly
                    ),
                    run_time=2
                )
                self.slide_pause()
        else:
            self.add(polynomier)

        # moving_rect = Rectangle(
        #     height=polynomier.height + 0.25,
        #     width=polynomier[0].width + 0.25
        # ).move_to(
        #     VGroup(polynomier[0], polynomier[-1][:3])
        # ).set_style(
        #     fill_opacity=0,
        #     stroke_width=2,
        #     fill_color=BLACK,
        #     stroke_color=pmap["a_0"]
        # )
        # self.play(
        #     Create(moving_rect)
        # )
        # self.slide_pause()
        # self.play(
        #     moving_rect.animate.set_height(
        #         polynomier[1:].height+0.25
        #     ).set_width(
        #         polynomier[1].width+0.25
        #     ).set_style(
        #         stroke_color=pmap["a_1"]
        #     ).move_to(
        #         VGroup(polynomier[1], polynomier[-1][:7])
        #     )
        # )
        moving_rects = VGroup(*[
            get_background_rect(
                VGroup(polynomier[i], polynomier[-1][:3]),
                buff=0.25,
                stroke_colour=pmap[f"a_{i}"],
                stroke_width=2,
                fill_opacity=0
            ) for i in range(len(polynomier))
        ])
        # self.add(moving_rects)
        for i, rect in enumerate(moving_rects):
            if i == 0:
                self.play(Create(rect))
            else:
                self.play(
                    TransformFromCopy(moving_rects[i-1], rect),
                    FadeOut(moving_rects[i-1], run_time=0.25),
                    run_time=2
                )
            self.slide_pause()

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
        self.play(
            DrawBorderThenFill(plane),
            run_time=1
        )
        self.slide_pause()
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
