from manim import *
from helpers import *

slides = False
if slides:
    from manim_slides import Slide
base_col = GREEN
rent_col = GREEN_B
graph_params = {
    "xlims": (0, 13.5, 1),
    "ylims": (0, 7500, 1000),
    "width": 12
}
plane = Axes(
    x_range=graph_params["xlims"],
    y_range=graph_params["ylims"],
    x_length=graph_params["width"],
    y_length=graph_params["width"] / 16 * 9,
    axis_config={"include_numbers": True}
)
b = 500
r1, r2 = 0.25, 0.02


class Annuitetsopsparing(Slide if slides else MovingCameraScene):
    def construct(self):
        title = "Annuitetsopsparing"
        # play_title(title)
        self.one_time_payment()

    def slide_pause(self, t=1.0, slides_bool=slides):
        if slides_bool:
            indicator = Dot(fill_opacity=0.5, fill_color=GREEN).scale(0.5).to_edge(DR, buff=0.1)
            self.play(FadeIn(indicator), run_time=0.25)
            xs_pause(self)
            self.pause()
            self.play(FadeOut(indicator), run_time=0.25)
        else:
            self.wait(t)

    def add_axis_lines(self, axes, axis, stroke_width=0.5, alpha=0.5):
        lines = VGroup()
        if axis == "y":
            for i in range(*axes.get_y_range()):
                lines += DashedLine(
                    start=axes.c2p(0, i),
                    end=axes.c2p(axes.get_x_range()[1], i),
                    color=axes.get_color(),
                    stroke_width=stroke_width,
                    stroke_opacity=alpha
                )
        return lines

    def get_rectangle(self, xpoint, height, buff=0.45, c=base_col):
        return Rectangle(
            width=(plane.c2p(xpoint+buff, 0) - plane.c2p(xpoint-buff, 0))[0],
            height=(plane.c2p(xpoint+buff, height) - plane.c2p(xpoint+buff, 0))[1],
            stroke_width=0.5,
            fill_color=c,
            fill_opacity=1,
            z_index=0
        ).move_to(plane.c2p(xpoint, height/2))

    def get_rect_height(self, rect):
        h = b/0.45 * rect.height
        return DecimalNumber(
            h,
            num_decimal_places=2,
            z_index=rect.z_index + 1,
            color=base_col
            ).scale(0.45).next_to(rect, UP, buff=0.1)
        # ).scale(0.45).next_to(rect, DOWN).shift(0.625*UP)
        #     color=DARKER_GRAY,
        #     stroke_color=DARKER_GRAY
        # ).scale(0.45).next_to(rect, UP).shift(0.45 * DOWN)

    def one_time_payment(self):
        yaxis_lines = self.add_axis_lines(plane, "y")
        self.play(
            DrawBorderThenFill(
                plane,
            ),
            Create(
                yaxis_lines
            )
        )
        self.slide_pause()

        b_rects = VGroup()
        rect_texts = VGroup()
        self.camera.frame.save_state()

        b_rect = self.get_rectangle(
            xpoint=1,
            height=b
        )
        rect_text = self.get_rect_height(b_rect)
        b_rects += b_rect
        rect_texts += rect_text
        self.play(
            self.camera.frame.animate.set(
                width=4
            ).move_to(b_rect.get_top()),
            run_time=2
        )
        srec = SurroundingRectangle(
            b_rect,
            color=BLACK,
            fill_color=BLACK,
            fill_opacity=1,
            z_index=-1
        ).shift(0.58*DOWN)
        self.add(srec)
        self.play(
            # Create(b_rect),
            # GrowFromEdge(b_rect.set_z_index(-2), DOWN),
            b_rect.set_z_index(-2).shift(0.6*DOWN).animate.shift(0.6*UP).set_z_index(0),
            rate_func=rate_functions.ease_out_back,
            run_time=1
        )
        self.remove(srec)
        self.slide_pause(0.5)
        self.play(
            Write(rect_text),
            run_time=0.5
        )
        self.slide_pause(0.5)

        r1_text =MathTex(
            f"+{100*r1:.0f}\%",
            color=rent_col,
            z_index=-1
        ).scale(0.45)

        for i in range(2, 13):
            h = b * (1+r1)**(i-1)
            b_rect = self.get_rectangle(
                xpoint=i,
                height=h
            )
            rect_text = self.get_rect_height(b_rect)

            self.play(
                self.camera.frame.animate.set(
                    width=4
                ).move_to(b_rect.get_top()),
                run_time=2
            )
            prev_rect = b_rects[-1].copy().set_z_index(-1)
            rente = self.get_rectangle(
                i,
                b * ((1+r1)**(i-1) - (1+r1)**(i-2)),
                c=rent_col
            )
            self.play(
                prev_rect.animate.move_to(
                    plane.c2p(i, h/(2*(1+r1)))
                )
            )
            prev_rect.set_z_index(0)
            self.slide_pause(0.5)
            self.play(
                TransformFromCopy(
                    prev_rect,
                    rente.next_to(prev_rect, UP, buff=0)
                ),
                Write(
                    r1_text.next_to(b_rect, UP, buff=0.1)
                )
            )
            self.slide_pause(0.5)
            self.play(
                Transform(
                    VGroup(prev_rect, rente),
                    b_rect
                ),
                # FadeOut(r1_text)
                r1_text.animate.shift(0.5*DOWN)
            )
            self.remove(r1_text)
            self.slide_pause(0.5)
            self.play(
                Write(
                    rect_text
                ),
                run_time=0.5
            )
            b_rects += b_rect
            rect_texts += rect_text
            self.slide_pause(0.5)
            # break

        self.play(
            Restore(
                self.camera.frame
            ),
            run_time=2
        )
        self.slide_pause(5)


# if i:
#     rente = self.get_rectangle(
#         xpoint=i + 1,
#         height=b * ((1 + r1) ** i - 1)
#     )
#     rente.set_fill(rent_col).next_to(b_rect)
