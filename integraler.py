from manim import *
from helpers import *
import numpy as np

slides = False
if slides:
    from manim_slides import Slide

xlims = (-1.5, 9.5, 1)
ylims = (-0.5, 6.5, 1)
width = 5
plane = Axes(
    x_range=xlims,
    y_range=ylims,
    x_length=width,
    y_length=width * (ylims[1]-ylims[0])/(xlims[1]-xlims[0]),
    # background_line_style={
    #     "stroke_color": TEAL,
    #     "stroke_width": 2,
    #     "stroke_opacity": 0.3
    # },
    # axis_config={"include_numbers": True}
)


class Sumregel(Slide if slides else MovingCameraScene):
    def construct(self):
        self.slide_pause(0.5)
        self.sum_af_to_funktioner()

        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t=t, slides_bool=slides_bool)

    def get_line_to_graph(self, axes, graph, x, match_col=True):
        line = always_redraw(lambda: Line(
            start=axes.c2p(x, 0),
            end=axes.c2p(x, graph.underlying_function(x)),
            color=graph.get_color() if match_col else WHITE,
            stroke_width=3.0
        ))
        return line

    def get_lines_to_graph(self, axes, graph, xrange=(0.0, 5.0, 1.0), match_col=True):
        lines = VGroup(*[
            self.get_line_to_graph(
                axes,
                graph,
                x,
                match_col
            ) for x in np.arange(*xrange)
        ])
        return lines

    def sum_af_to_funktioner(self):
        f_col = YELLOW
        g_col = BLUE
        h_col = GREEN

        intro = MathTex("f(x)", "+", "g(x)", "=", "h(x)").scale(1.5)
        intro[0].set_color(f_col)
        intro[2].set_color(g_col)
        intro[4].set_color(h_col)
        self.play(
            Write(intro),
            run_time=2
        )
        self.slide_pause(2)
        self.play(
            Unwrite(intro),
            run_time=1
        )
        self.slide_pause(0.5)

        plane1 = plane.copy().to_edge(UL)
        plane2 = plane.copy().to_edge(DL)
        plane_sum = plane.copy().to_edge(RIGHT)
        # plane_sum.set_y_range((ylims[0]-1, ylims[1]+3, 1))
        self.play(
            DrawBorderThenFill(plane1),
            run_time=0.5
        )
        self.slide_pause(0.5)
        self.play(
            DrawBorderThenFill(plane2),
            run_time=0.5
        )
        self.slide_pause(0.5)

        af = ValueTracker(0.0)
        bf = ValueTracker(1.0)
        ag = ValueTracker(-0.25)
        bg = ValueTracker(2.0)
        cg = ValueTracker(0.25)

        graph1 = always_redraw(lambda: plane1.plot(
            lambda x: af.get_value() * x + bf.get_value(),
            color=f_col,
            x_range=xlims[:2],
            stroke_width=2.5
        ))
        graph1_text = always_redraw(lambda:
            MathTex("f(x)", color=f_col).next_to(graph1, UP)
        )
        graph2 = always_redraw(lambda: plane2.plot(
            lambda x: ag.get_value() * x**2 + bg.get_value() * x + cg.get_value(),
            color=g_col,
            x_range=xlims[:2],
            stroke_width=2.5
        ))
        graph2_text = always_redraw(lambda:
            MathTex("g(x)", color=g_col).next_to(graph2, UP)
        )
        self.play(
            Create(graph1),
            Write(graph1_text),
            run_time=1.5
        )
        self.slide_pause(0.5)
        self.play(
            Create(graph2),
            Write(graph2_text),
            run_time=1.5
        )
        self.slide_pause(0.5)

        arrow = Arrow(
            start=1.25*LEFT,
            end=RIGHT
        )
        func_sum_text = MathTex("f(x)", "+", "g(x)").next_to(arrow, UP, buff=0)
        func_sum_text[0].set_color(f_col)
        func_sum_text[2].set_color(g_col)
        self.play(
            DrawBorderThenFill(arrow),
            run_time=1.5
        )
        self.slide_pause(0.5)
        # self.play(
        #     TransformFromCopy(
        #         VGroup(graph1_text, graph2_text),
        #         func_sum_text
        #     ),
        #     run_time=1
        # )
        # self.slide_pause(0.5)

        for ix, xstep in enumerate([1, 0.5, 0.25, 0.1]):
            speed_up_index = 2
            rtime = xstep ** 2
            xrange = (0, 8.1, xstep)
            graph1_lines = always_redraw(lambda:
                self.get_lines_to_graph(plane1, graph1, xrange)
            )
            graph2_lines = always_redraw(lambda:
                self.get_lines_to_graph(plane2, graph2, xrange)
            )
            graph1_lines_copy = always_redraw(lambda: VGroup(
                *[
                    Line(
                        start=plane_sum.c2p(x, 0),
                        end=plane_sum.c2p(x, graph1.underlying_function(x)),
                        color=graph1.get_color(),
                        stroke_width=3.0
                    ) for x in np.arange(*xrange)
                ]
            ))
            graph2_lines_copy = always_redraw(lambda: VGroup(
                *[
                    Line(
                        start=plane_sum.c2p(x, graph1.underlying_function(x)),
                        end=plane_sum.c2p(
                            x,
                            graph1.underlying_function(x) + graph2.underlying_function(x)
                        ),
                        color=graph2.get_color(),
                        stroke_width=3.0
                    ) for x in np.arange(*xrange)
                ]
            ))

            if ix == 0:
                self.camera.frame.save_state()
                self.play(
                    self.camera.frame.animate.set(
                        width=4
                    ).move_to(plane1.c2p(0, 0)),
                    run_time=2
                )
                self.slide_pause(0.5)
                self.play(
                    Create(graph1_lines[0]),
                    run_time=2
                )
                self.play(
                    self.camera.frame.animate.move_to(plane2.c2p(0, 0)),
                    run_time=2
                )
                self.slide_pause(0.5)
                self.play(
                    Create(graph2_lines[0]),
                    run_time=2
                )
                self.slide_pause(0.5)
                self.play(Restore(self.camera.frame), run_time=2)
                self.slide_pause(0.5)

                self.play(
                    DrawBorderThenFill(plane_sum),
                    run_time=0.5
                )
                self.slide_pause(0.5)

            graph_sum = always_redraw(lambda: plane_sum.plot(
                lambda x: graph1.underlying_function(x) + graph2.underlying_function(x),
                color=h_col,
                x_range=xlims[:2],
                stroke_width=2.5
            ))

            if ix == 0:
                self.play(
                    graph1_lines[0].copy().animate.move_to(plane_sum.c2p(
                        0,
                        0.5 * graph1.underlying_function(0)
                    )),
                    run_time=1
                )
                self.slide_pause(0.5)
                self.play(
                    graph2_lines[0].copy().animate.move_to(plane_sum.c2p(
                        0,
                        graph1_lines[0].get_top()[1] + 0.5 * graph2.underlying_function(0)
                    )),
                    run_time=1
                )
                self.slide_pause(0.5)

                for lines in (graph1_lines, graph2_lines):
                    self.play(
                        LaggedStart(
                            *[Create(lines[1:])],
                            lag_ratio=0.25
                        ),
                        run_time=2
                    )
                    self.slide_pause(0.5)

                self.add(graph1_lines_copy[0], graph2_lines_copy[0])
                lines = zip(graph1_lines[1:].copy(), graph2_lines[1:].copy())
                x = xrange[0] + xrange[2]
            else:
                for lines in (graph1_lines, graph2_lines):
                    self.play(
                        LaggedStart(
                            *[Create(lines)],
                            lag_ratio=0.25
                        ),
                        run_time=1 if ix < speed_up_index else 0.5
                    )
                    self.slide_pause(0.5)
                lines = zip(graph1_lines.copy(), graph2_lines.copy())
                x = xrange[0]

            # for line1, line2 in zip(graph1_lines[1:].copy(), graph2_lines[1:].copy()):
            for line1, line2 in lines:
                self.play(
                    line1.animate.move_to(plane_sum.c2p(
                        x,
                        0.5 * graph1.underlying_function(x)
                    )),
                    # run_time=1 if ix < speed_up_index else 0.1
                    run_time=rtime
                )
                self.play(
                    line2.animate.move_to(plane_sum.c2p(
                        x,
                        plane_sum.p2c(line1.get_top())[1] + 0.5 * graph2.underlying_function(x)
                    )),
                    # run_time=1 if ix < speed_up_index else 0.1
                    run_time=rtime
                )
                x += xrange[2]

            self.remove(*[
                m for m in self.mobjects if m not in [plane1, plane2, plane_sum,
                                                      graph1, graph2, arrow,
                                                      graph1_lines, graph2_lines,
                                                      graph1_text, graph2_text]
            ])
            self.add(
                graph1_lines, graph2_lines,
                graph1_lines_copy, graph2_lines_copy
            )

            self.play(
                Create(graph_sum),
                run_time=2
            )

            for b in [4, 0, 1]:
                self.play(
                    bf.animate.set_value(b),
                    run_time=1
                )
                self.slide_pause(0.5)
            for a in [0.5, 0]:
                self.play(
                    af.animate.set_value(a),
                    run_time=1
                )
                self.slide_pause(0.5)

            self.play(
                FadeOut(VGroup(*[
                    graph1_lines, graph2_lines,
                    graph1_lines_copy, graph2_lines_copy,
                    graph_sum
                ]))
            )


