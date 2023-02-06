from manim import *
from helpers import *
import numpy as np

slides = False
if slides:
    from manim_slides import Slide


class BasicVectors(Slide if slides else Scene):
    def construct(self):
        title = Tex("Grundlæggende om ", "vektorer")
        title[1].set_color(YELLOW)
        # play_title(self, title, edge=UL)
        self.om_vektorer()
        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def om_vektorer(self):
        nline = NumberLine(include_numbers=True).set_z_index(6, family=True)
        srec1 = Rectangle(width=16, height=4, z_index=4)\
            .set_style(fill_opacity=1, stroke_width=0, fill_color=BLACK).to_edge(DOWN, buff=0)
        srec2 = srec1.copy().to_edge(UP, buff=0)
        plane = NumberPlane(z_index=2)
        tekst_tal = Tex("Tal har en ", "størrelse")
        tekst_tal[1].set_color(GREEN)
        tekst_vek = Tex("Vektorer har en ", "størrelse", " og en ", "retning")
        tekst_vek[1].set_color(GREEN)
        tekst_vek[3].set_color(YELLOW)
        self.play(
            Write(tekst_tal)
        )
        self.slide_pause()
        self.play(
            tekst_tal.animate.shift(UP),
            Write(tekst_vek)
        )
        self.slide_pause()
        self.play(Unwrite(VGroup(tekst_vek, tekst_tal), reverse=False))
        self.slide_pause()
        self.play(
            DrawBorderThenFill(nline),
        )
        self.add(srec1, srec2, plane)
        self.play(
            srec1.animate.shift(5*DOWN),
            srec2.animate.shift(5*UP),
            FadeOut(nline)
        )
