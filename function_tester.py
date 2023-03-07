from manim import *
from helpers import *

slides = False
if slides:
    from manim_slides import Slide


class Keyword(Slide if slides else Scene):
    def construct(self):
        self.add(NumberPlane())
        keyword_overlay(self)
        slides_pause(self, 5)
