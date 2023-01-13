from manim import *
from helpers import *

slides = False
if slides:
    from manim_slides import Slide


class HoppendeBold(Slide if slides else MovingCameraScene):
    def construct(self):
        title = Tex("Mekanisk energi af en", "hoppende bold").arrange(DOWN, aligned_edge=LEFT)
        title[1].set_color(YELLOW)
        # play_title(self, title)
        self.slide_pause(0.5)
        self.basketbold()

    def slide_pause(self, t=0.5, slides_bool=slides):
        if slides_bool:
            indicator = Dot(fill_opacity=0.5, fill_color=GREEN).scale(0.5).to_edge(DR, buff=0.1)
            self.play(FadeIn(indicator), run_time=0.25)
            xs_pause(self)
            self.pause()
            self.play(FadeOut(indicator), run_time=0.25)
        else:
            self.wait(t)

    def get_ground_lines(self, line, n=10, alpha=0.25):
        line_length = line.get_length()/n
        ground_lines = VGroup()
        for i in range(n):
            ground_lines.add(
                Line(
                    start=line.get_start() + line_length*(i+1)*RIGHT,
                    end=line.get_start() + line_length*(i*RIGHT + DOWN),
                    stroke_opacity=alpha
                )
            )
        return ground_lines

    def basketbold(self):
        svg_path = r"SVGs\basketball.svg"
        ball = SVGMobject(svg_path)
        self.play(
            DrawBorderThenFill(ball)
        )
        self.slide_pause()
        ground = VGroup(
            Line().scale(2).to_edge(DL, buff=1)
        )
        ground.add(*self.get_ground_lines(ground[0]))
        self.play(
            DrawBorderThenFill(ground)
        )
        self.slide_pause()
        self.play(
            ball.animate.scale(0.5).next_to(ground, UP, buff=0)
        )
        self.slide_pause()
        ball_ref = ball.copy()

        h = ValueTracker(0)
        # ball.add_updater(lambda mob: mob.shift(h.get_value() * UP))
        ball.add_updater(lambda mob: mob.move_to(ball_ref.get_center() + h.get_value()*UP))
        self.play(
            h.animate.set_value(5),
            run_time=2
        )
        self.slide_pause()
        h_text = always_redraw(lambda:
            DecimalNumber(
                h.get_value()*10,
                num_decimal_places=1,
                include_sign=False
            ).next_to(ball, LEFT)
        )
        h_brace = always_redraw(lambda:
            BraceBetweenPoints(
                point_1=ball_ref.get_center() + 0.5*ball_ref.get_height()*DL,
                point_2=ball.get_center() + 0.5*ball_ref.get_height()*DL,
                direction=LEFT
            )
        )
        self.play(
            Write(h_text),
            GrowFromCenter(h_brace)
        )
        self.slide_pause()
        self.play(
            h.animate.set_value(0),
            run_time=2
        )
        self.slide_pause()



