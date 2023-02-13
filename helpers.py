from manim import *
import numpy as np


def _prep_title(title, close=False):
    if isinstance(title, str):
        title = Tex(title)
    title_ul = Underline(title)
    title_ul_box = Rectangle(
        width=title.width * 1.05,
        height=title.height * 1.6
    ).next_to(
        title_ul, DOWN, buff=0
    ).set_style(fill_opacity=1, stroke_width=0, fill_color=BLACK)
    ul_group = VGroup(title_ul, title_ul_box)
    if close:
        ul_group.shift(UP * title_ul_box.height)
    return title_ul, title_ul_box, ul_group


def play_title(self, title, cols=None, edge=None):
    if isinstance(title, str):
        title = Tex(*[t + " " for t in title.split()])
    if cols is not None and isinstance(cols, dict):
        for k, v in cols.items():
            title[int(k)].set_color(v)
    title_ul, title_ul_box, ul_group = _prep_title(title)
    self.play(Write(title), run_time=0.5)
    self.wait(2)
    if edge is not None:
        self.play(
            title.animate.to_edge(edge, buff=0.05).set_z_index(10).set_opacity(0.15),
        )
        self.play(
            FadeIn(title_ul_box.set_opacity(0.5).to_edge(edge, buff=0.05).set_z_index(9)),
            run_time=0.1
        )
        return title, title_ul_box
    else:
        self.play(GrowFromCenter(title_ul), run_time=1)
        self.add(ul_group)
        self.play(ul_group.animate.shift(UP * title_ul_box.height))
        self.play(ShrinkToCenter(title_ul))
        self.remove(ul_group, title)
    self.wait(2)


def play_title_reverse(self, title, pos=None):
    if isinstance(title, str):
        title = Tex(title)
    title_ul, title_ul_box, ul_group = _prep_title(title, close=True)
    if pos is None:
        self.add(title, ul_group)
        self.play(GrowFromCenter(title_ul), run_time=1)
        self.play(ul_group.animate.shift(DOWN * title_ul_box.height))
        self.remove(ul_group)
        self.play(ShrinkToCenter(title_ul))
    else:
        self.play(
            title.animate.move_to(pos).set_z_index(0).set_opacity(1.0)
        )
        # title_ul, title_ul_box, ul_group = _prep_title(title, close=True)
    self.wait(1)
    self.play(Unwrite(title), run_time=0.5)
    self.wait(1)


def p2p_anim(mob1, mob2, tex1, tex2=None, index=0):
    if tex2 == None:
        tex2 = tex1
    return ReplacementTransform(
        mob1.get_parts_by_tex(tex1)[index],
        mob2.get_parts_by_tex(tex2)[index],
    )


def p2p_anim_copy(mob1, mob2, tex1, tex2=None, index=0):
    if tex2 == None:
        tex2 = tex1
    return TransformFromCopy(
        mob1.get_parts_by_tex(tex1)[index],
        mob2.get_parts_by_tex(tex2)[index],
    )


def fade_out_all(self, rt=1):
    self.play(
        *[
            FadeOut(mob) for mob in self.mobjects
        ],
        run_time=rt
    )


def ftp(point1, point2, dim="y"):  # Find Top Point
    d = {"x": 0, "y": 1, "z": 2}
    if isinstance(dim, str):
        dim = d[dim]
    return point1 if point1[dim] > point2[dim] else point2


def xs_pause(self, t=0.5):
    self.wait(t)


def s_pause(self, t=1):
    self.wait(t)


def m_pause(self, t=1.5):
    self.wait(t)


def l_pause(self, t=2.5):
    self.wait(t)


def xl_pause(self, t=5):
    self.wait(t)


def create_table(data, orientation="vertical", numcol1=BLUE, numcol2=None, dec=0, sign=False, scale=1.0):
    if numcol2 is None:
        numcol2 = numcol1
    if orientation == "horizontal":
        data = np.transpose(data)
    numbers = VGroup()
    for i in data:
        for j in i:
            numbers.add(
                DecimalNumber(
                    j,
                    color=numcol1,
                    num_decimal_places=dec,
                    include_sign=sign
                ).scale(scale)
            )
    numbers = numbers.arrange_in_grid(rows=len(data), col_alignments="rr")
    table = DecimalTable(
        data
    )
    return table


slides = False


def slides_pause(self, t=1.0, slides_bool=slides):
    if slides_bool:
        indicator = Dot(fill_opacity=0.5, fill_color=GREEN).scale(0.5).to_edge(DR, buff=0.1)
        self.play(FadeIn(indicator), run_time=0.25)
        xs_pause(self)
        self.pause()
        self.play(FadeOut(indicator), run_time=0.25)
    else:
        self.wait(t)


def scene_marker(scene_name):
    print("-" * 20)
    print(scene_name)
    print("-" * 20)


def between_mobjects(left_mob, right_mob):
    return 0.5*(right_mob.get_edge_center(LEFT) + left_mob.get_edge_center(RIGHT))

