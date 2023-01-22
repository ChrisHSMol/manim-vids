from manim import *
from helpers import *
import numpy as np

slides = False
if slides:
    from manim_slides import Slide


class UgrupperetData(Slide if slides else Scene):
    def construct(self):
        title = Tex("Ugrupperet", " data")
        title[0].set_color(YELLOW)
        # play_title(self, title)
        self.slide_pause(0.5)
        self.kvartiler()
        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides)

    def data_to_DecNum(self, data):
        return VGroup(
            *[DecimalNumber(
                    val,
                    include_sign=False,
                    num_decimal_places=0,
                ).scale(0.5) for val in data]
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.1)

    def kvartiler(self):
        data_raw = [8, 4, 16, 8, 9, 6, 16, 19, 7, 6, 4, 8, 11, 8, 9, 6, 9, 10, 11, 8, 14, 4, 6, 7, 10]
        data = self.data_to_DecNum(data_raw).to_edge(LEFT)
        self.play(
            LaggedStart(
                *[DrawBorderThenFill(d) for d in data],
                lag_ratio=0.1
            ),
            run_time=2
        )
        self.slide_pause(0.5)

        steps = VGroup(
            Tex("Trin 1: Sortér data"),
            Tex("Trin 2: Find midterste tal"),
            Tex("Trin 3: Trin 2, men øverste halvdel"),
            Tex("Trin 4: Trin 2, men øverste halvdel")
        ).scale(0.5).arrange(DOWN, aligned_edge=LEFT).to_edge(UR, buff=1.5)
        self.play(
            Write(steps[0]),
            run_time=2
        )
        self.slide_pause(0.5)

        data_ordered = self.data_to_DecNum(sorted(data_raw)).next_to(data, RIGHT, buff=2)
        self.play(
            TransformFromCopy(
                data,
                data_ordered
            )
        )
        self.slide_pause(0.5)

        self.play(
            Write(steps[1]),
            steps[0].animate.set_opacity(0.25),
            run_time=2
        )
        self.slide_pause(0.5)

        topArrow = Arrow(
            start=0.5*LEFT,
            end=0.5*RIGHT,
            color=BLUE
        ).next_to(data_ordered[0], LEFT)
        botArrow = Arrow(
            start=0.5*RIGHT,
            end=0.5*LEFT,
            color=RED
        ).next_to(data_ordered[-1], RIGHT)
        self.play(
            Create(topArrow),
            Create(botArrow),
        )

        index_median = 0
        median = np.median(data_raw)
        for i in np.arange(len(data)-2)+1:
            self.play(
                topArrow.animate.next_to(data_ordered[i], LEFT),
                botArrow.animate.next_to(data_ordered[-1-i], RIGHT)
            )
            if topArrow.get_center()[1] <= botArrow.get_center()[1]:
                self.play(
                    data_ordered[i].animate.set_color(YELLOW),
                    run_time=2
                )
                median = data_ordered[i].copy()
                self.play(
                    median.animate.next_to(steps[1], RIGHT, buff=1.5),
                    data_ordered[:i].animate.set_color(BLUE),
                    data_ordered[-i:].animate.set_color(RED),
                    topArrow.animate.next_to(data_ordered[0], LEFT).set_opacity(0),
                    botArrow.animate.next_to(data_ordered[i-1], RIGHT).set_opacity(0)
                )
                self.remove(topArrow, botArrow)
                index_median = i
                break

        topArrow.set_opacity(1)
        botArrow.set_opacity(1)

        self.slide_pause(0.5)
        self.play(
            Write(steps[2]),
            VGroup(steps[1], median).animate.set_opacity(0.25),
            run_time=2
        )
        self.slide_pause(0.5)

        self.play(
            FadeIn(topArrow),
            FadeIn(botArrow),
        )

        index_q1 = 0
        q1 = 0
        for i in np.arange(index_median) + 1:
            self.play(
                topArrow.animate.next_to(data_ordered[i], LEFT),
                botArrow.animate.next_to(data_ordered[index_median - i - 1], RIGHT)
            )
            if topArrow.get_center()[1] == botArrow.get_center()[1]:
                print("HEJ")
            if topArrow.get_center()[1] < botArrow.get_center()[1]:
                self.play(
                    VGroup(data_ordered[i], data_ordered[i-1]).animate.set_color(YELLOW),
                    run_time=2
                )
                nums = [data_ordered[i-1].get_value(), data_ordered[i].get_value()]
                print(nums)
                calculation = MathTex(
                    f"{{{data_ordered[i-1].get_value()} + {data_ordered[i].get_value()}",
                    r"\over",
                    "2}",
                    "=",
                    # f"{np.mean(data_ordered[i-1].get_value(), data_ordered[i].get_value())}"
                    f"{np.mean(nums)}"
                ).next_to(VGroup(data_ordered[i-1:i]), RIGHT)
                self.add(calculation)
                break


