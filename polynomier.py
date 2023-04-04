from manim import *
from helpers import *
import numpy as np

slides = True
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

    def highest_power_in_tex(self, tex):
        hpow = 0
        str_ind = 0
        search_number = False
        for ind, s in enumerate(tex.get_tex_string()):
            print(ind, s)
            if search_number:
                try:
                    s = int(s)
                    if s > hpow:
                        print("hpow increased")
                        hpow = s
                        str_ind = ind
                        search_number = False
                except:
                    continue
            if s == "x":
                if hpow == 0:
                    hpow = 1
                    str_ind = ind
                else:
                    search_number = True
        return str_ind

    def etymologi(self):
        self.slide_pause()
        play_latest = False
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
            self.slide_pause()
            self.play(FadeOut(mit_navn), run_time=0.5)

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

        pmap = {
            "a_0": YELLOW_A,
            "a_1": YELLOW_B,
            "a_2": YELLOW_C,
            "a_3": YELLOW_D,
            "a_4": YELLOW_E,
            "x": RED,
        }
        polynomier = VGroup(
            MathTex(
                "f_0(", "x", ")", " = ", "a_0",
            ),
            MathTex(
                "f_1(", "x", ")", " = ", "a_0", " + ", "a_1", r"\cdot", "x",
            ),
            MathTex(
                "f_2(", "x", ")", " = ", "a_0", " + ", "a_1", r"\cdot", "x", " + ", "a_2", r"\cdot", "x", "^2",
            ),
            MathTex(
                "f_3(", "x", ")", " = ", "a_0" " + ", "a_1", r"\cdot", "x", " + ",
                "a_2", r"\cdot", "x", "^2", " + ", "a_3", r"\cdot", "x", "^3",
            ),
            MathTex(
                "f_4(", "x", ")", " = ", "a_0", " + ", "a_1", r"\cdot", "x", " + ", "a_2", r"\cdot", "x", "^2", " + ",
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

        moving_rects = VGroup(*[
            get_background_rect(
                VGroup(polynomier[i], polynomier[-1][:3]),
                buff=0.25,
                stroke_colour=pmap[f"a_{i}"],
                stroke_width=2,
                fill_opacity=0
            ) for i in range(len(polynomier))
        ])
        rect_labels = VGroup(*[
            Tex(f"{i}. orden").set_color(pmap[f"a_{i}"]).next_to(moving_rects[i], LEFT) for i in range(len(moving_rects))
        ])
        if not play_latest:
            for i, rect, lab in zip(range(len(moving_rects)), moving_rects, rect_labels):
                if i == 0:
                    self.play(
                        Create(rect),
                        Write(lab)
                    )
                else:
                    self.remove(moving_rects[i-1], rect_labels[i-1])
                    self.play(
                        TransformFromCopy(moving_rects[i-1], rect),
                        TransformFromCopy(rect_labels[i-1], lab),
                        run_time=2
                    )
                self.slide_pause()
            self.play(FadeOut(lab, rect, polynomier))
            self.slide_pause()
        else:
            self.remove(polynomier)

        ex_pol = VGroup(
            VGroup(
                MathTex(r"f(x) = 2 \cdot x - 4").set_color(YELLOW_B),
                MathTex(r"f(x) = -4 \cdot x + 2").set_color(YELLOW_C),
                MathTex(r"f(x) = x^2 + 2 \cdot x - 1").set_color(YELLOW_D)
            ).arrange(DOWN, aligned_edge=LEFT, buff=1.5),
            VGroup(
                MathTex(r"f(x) = x^6 + 2 \cdot x^4 - x^3 + 2 \cdot x").set_color(BLUE_B),
                MathTex(r"f(x) = x^3 - 5 \cdot x^4 + x - 1").set_color(BLUE_C),
                MathTex(r"f(x) = x + 2\cdot x - 30 \cdot x^3 + x^{25}").set_color(BLUE_D)
            ).arrange(DOWN, aligned_edge=LEFT, buff=1.5)
        ).arrange(RIGHT, aligned_edge=DOWN, buff=1)

        answers = VGroup(*[
            Tex("Svar: ", f"{n}. orden").scale(0.65).set_color(
                ex.get_color()
            ).next_to(ex, DOWN, aligned_edge=LEFT) for n, ex in zip(
                ["1", "1", "2", "6", "4", "25"],
                list(ex_pol[0])+list(ex_pol[1])
            )
        ])
        ans_rect = VGroup(*[
            get_background_rect(
                ans[-1], fill_opacity=1, buff=0.25
            ).set_style(fill_color=ans.get_color()).set_z_index(ans.get_z_index() + 2) for ans in answers
        ])
        for ex, ans, ansr in zip(list(ex_pol[0])+list(ex_pol[1]), answers, ans_rect):
            self.play(
                Write(ex),
                LaggedStart(
                    DrawBorderThenFill(ansr),
                    Write(ans),
                    lag_ratio=1
                ),
                run_time=1
            )
        self.slide_pause()

        [tekst[-1].set_opacity(0.01) for tekst in answers]
        for iq, eq in enumerate(list(ex_pol[0])+list(ex_pol[1])):
            self.play(
                *[pol.animate.set_opacity(0.15) for pol in list(ex_pol[0])+list(ex_pol[1]) if not pol == eq],
                *[tekst[0].animate.set_opacity(0.15) for tekst in answers if not tekst == answers[iq]],
                # *[rect.animate.set_opacity(0.25) for rect in ans_rect if not rect == ans_rect[iq]],
                *[rect.animate.set_opacity(0.15) for rect in ans_rect[iq+1:]],
                run_time=2
            )
            self.slide_pause()

            self.play(
                ans_rect[iq].animate.set_opacity(0.05),
                answers[iq].animate.set_opacity(1.0),
                run_time=1
            )
            # print(self.highest_power_in_tex(eq))
            # self.play(
            #     Circumscribe(
            #         eq[self.highest_power_in_tex(eq)]
            #     ),
            #     Circumscribe(
            #         answers[iq][:2]
            #     ),
            #     run_time=2
            # )

            self.slide_pause()
            self.play(
                *[pol.animate.set_opacity(1) for pol in list(ex_pol[0]) + list(ex_pol[1]) if not pol == eq],
                *[tekst[0].animate.set_opacity(1) for tekst in answers if not tekst == answers[iq]],
                *[rect.animate.set_opacity(1) for rect in ans_rect[iq+1:]],
                answers[iq].animate.set_opacity(0.15),
                run_time=2
            )

        self.play(
            *[m.animate.set_opacity(1) for m in self.mobjects if m not in ans_rect],
            run_time=0.5
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


class PolyRod(Slide if slides else MovingCameraScene):
    def construct(self):
        self.roots()
        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t=t, slides_bool=slides_bool)

    def roots(self):
        cmap = {
            "rod": YELLOW,
            "rødder": YELLOW,
            "nulpunkt": BLUE_B
        }
        opener = VGroup(
            Tex("En rod er et nulpunkt for grafen."),
            Tex("Et nulpunkt er, når y-værdien for grafen er 0.")
        ).arrange(DOWN, aligned_edge=LEFT)
        for line in opener:
            line.set_color_by_tex_to_color_map(cmap)

        self.play(
            Write(opener),
            run_time=1
        )


class MonotoniForhold(Slide if slides else Scene):
    def construct(self):
        self.slide_pause(0.1)
        plane, graph = self.start_graph()
        toppunkter, sub_graphs = self.toppunkter(plane, graph)
        self.monotoni(plane, graph, toppunkter, sub_graphs)

        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t=t, slides_bool=slides_bool)

    def start_graph(self):
        plane = NumberPlane(
            x_range=(-5.5, 10.5, 1),
            y_range=(-8.5, 9.5, 2),
            x_length=width,
            y_length=width / 16 * 9,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1.5,
                "stroke_opacity": 0.3
            },
        )
        graph = plane.plot(
            lambda x: 0.2 * x ** 3 - 2 * x ** 2 + 3 * x + 5,
            color=BLUE,
            z_index=2,
            stroke_width=6
        )
        self.play(
            LaggedStart(
                DrawBorderThenFill(plane),
                Create(graph),
                lag_ratio=0.5
            ),
            run_time=2
        )
        self.slide_pause()
        return plane, graph

    def toppunkter(self, plane, graph):
        toptekst = Tex("Toppunkter er der, hvor grafen skifter retning").scale(0.75).to_edge(UL, buff=0.1).set_z_index(3)
        toptekst[0][:10].set_color(YELLOW)
        srec = get_background_rect(toptekst, buff=0.1)
        self.play(
            Write(toptekst),
            FadeIn(srec),
            run_time=0.5
        )
        self.slide_pause()

        top_x = [0.8612671710, 5.805399496]
        toppunkter = VGroup(*[
            Dot(
                plane.c2p(x, graph.underlying_function(x)),
                radius=0.06,
                color=YELLOW,
                z_index=3
            ) for x in top_x
        ]).add(Dot(radius=0.00))
        punktlabels = VGroup(*[
            Tex(
                f"({plane.p2c(p.get_center())[0]:.2f}; {plane.p2c(p.get_center())[1]:.2f})",
                color=p.get_color(), z_index=p.get_z_index()
            ).scale(0.45 if p != toppunkter[-1] else 0.0).next_to(p, UP) for p in toppunkter
        ])
        xlows = [-3, *top_x]
        xhighs = [*top_x, 10]
        sub_graphs = VGroup(*[
            plane.plot(
                lambda x: graph.underlying_function(x),
                x_range=[xlow, xhigh],
                color=YELLOW,
                z_index=2,
                stroke_width=6
            ) for xlow, xhigh in zip(xlows, xhighs)
        ])
        for sub_graph, toppunkt, label in zip(sub_graphs, toppunkter, punktlabels):
            self.play(
                LaggedStart(
                    ShowPassingFlash(
                        sub_graph,
                        time_width=2,
                        run_time=4
                    ),
                    DrawBorderThenFill(
                        toppunkt,
                        run_time=1
                    ),
                    Write(
                        label,
                        run_time=0.5
                    ),
                    lag_ratio=0.4
                ),
            )
            self.slide_pause()
        self.play(FadeOut(toptekst), FadeOut(srec))
        self.remove(punktlabels)
        return toppunkter, sub_graphs

    def monotoni(self, plane, graph, toppunkter, sub_graphs):
        punktlabels = VGroup(*[
            Tex(
                f"({plane.p2c(p.get_center())[0]:.2f}; {plane.p2c(p.get_center())[1]:.2f})",
                color=p.get_color(), z_index=p.get_z_index()
            ).scale(0.45 if p != toppunkter[-1] else 0.0).next_to(p, UP) for p in toppunkter
        ])
        self.add(punktlabels)
        cmap = {
            "voksende": GREEN,
            "aftagende": RED
        }
        monotonitekst = VGroup(
            Tex("En funktion kan være"),
            Tex("voksende", " eller ", "aftagende").set_color_by_tex_to_color_map(cmap),
            Tex("i et interval")
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.75).to_edge(UL).set_z_index(3)
        mrec = get_background_rect(monotonitekst, buff=0.1)
        self.play(
            Write(monotonitekst),
            FadeIn(mrec),
            run_time=1
        )
        self.slide_pause()
        intervaller = VGroup(
            MathTex(f"]-\\infty; {plane.p2c(toppunkter[0].get_center())[0]:.2f}["),
            MathTex(f"]{plane.p2c(toppunkter[0].get_center())[0]:.2f}; {plane.p2c(toppunkter[1].get_center())[0]:.2f}["),
            MathTex(f"]{plane.p2c(toppunkter[1].get_center())[0]:.2f}; \\infty[")
        ).arrange(DOWN, aligned_edge=LEFT).next_to(monotonitekst, DOWN, aligned_edge=LEFT)
        irec = get_background_rect(intervaller, buff=0.1)
        self.play(FadeIn(irec))
        for sub_graph, interval, col in zip(sub_graphs, intervaller, (cmap["voksende"], cmap["aftagende"], cmap["voksende"])):
            sub_graph.set_color(col)
            interval.set_color(col)
            self.play(
                LaggedStart(
                    Create(sub_graph),
                    Write(interval),
                    lag_ratio=0.5,
                    run_time=2
                )
            )
            self.slide_pause()
