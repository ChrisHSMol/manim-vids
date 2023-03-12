from manim import *
from helpers import *
import numpy as np
import math

slides = False
if slides:
    from manim_slides import Slide


class MultiOgAddiPrincip(Slide if slides else Scene):
    def construct(self):
        self.counting_tree()

        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    # def get_tree_branch(self, width: float, labels: list[str]) -> mobject:
    def get_tree_branch(self, width, labels, color=WHITE, loc=None, font_size=48, softness=0.5, node_cols=None):
        if loc is None:
            loc = ORIGIN
        else:
            loc = loc.get_bottom() + 0.2*DOWN
        output = {
            "dot": VGroup(Dot(loc, radius=0.04, color=node_cols[0], z_index=2)),
            "branches": VGroup(),
            "labels": VGroup()
        }
        end_points = np.linspace(-width/2, width/2, len(labels))
        for point, label in zip(end_points, labels):
            # line = Line(
            #     start=loc,
            #     end=loc + np.array([point, -1, 0]),
            #     color=color
            # )
            p2 = Dot(loc + np.array([point, -1, 0]), radius=0.04, color=node_cols[1], z_index=2)
            line = CubicBezier(
                loc,
                loc + softness * DOWN,
                p2.get_center() + softness * UP,
                p2.get_center()
            )
            lab = Tex(
                label,
                color=color,
                font_size=font_size
            ).next_to(line.get_end(), DOWN, buff=0.1)
            output["branches"].add(line)
            output["dot"].add(p2)
            output["labels"].add(lab)
        return output

    def create_branch(self, branch, rt=1.0, skip_animations=False):
        if isinstance(branch, list):
            for elem in branch:
                self.create_branch(elem, rt=rt/2)
        else:
            for key in branch.keys():
                if skip_animations:
                    self.add(branch[key])
                    continue
                if key == "dot":
                    continue
                self.play(
                    Write(branch[key]) if key == "labels" else Create(branch[key]),
                    run_time=rt
                )
            if not skip_animations:
                self.play(FadeIn(branch["dot"]), run_time=0.5)

    def highlight_path_backup(self, levels, indices, rt=2.0, color=YELLOW, preserve_color=False):
        for i, level, index in zip(range(len(levels)), levels, indices):
            while isinstance(level, list):
                j = i
                j -= 1 * len(np.shape(level))
                level = level[indices[j]]

            self.play(
                LaggedStart(
                    ShowPassingFlash(level["branches"][index].copy().set_color(color), time_width=2),
                    level["branches"][index].animate.set_color(color if preserve_color else None),
                    level["labels"][index].animate.set_color(color) if preserve_color else Indicate(level["labels"][index]),
                    lag_ratio=0.33
                ),
                run_time=rt
            )

    def highlight_path(self, levels, indices, rt=2.0, node_cols=None, preserve_color=False):
        if node_cols is None:
            node_cols = [YELLOW, YELLOW]
        for i, level, index, colors in zip(range(len(levels)), levels, indices, node_cols):
            while isinstance(level, list):
                j = i
                j -= 1 * len(np.shape(level))
                level = level[indices[j]]
                colors = [colors[1], colors[0]]
            colors = [colors[1], colors[0]]
            # node_cols = [dot.get_color() for dot in level["dot"]]
            # node_cols = [node_cols[-1], node_cols[0]]
            self.play(
                LaggedStart(
                    ShowPassingFlash(level["branches"][index].copy().set_color(color_gradient(colors, 2)), time_width=2),
                    level["branches"][index].animate.set_color(color_gradient(colors, 2) if preserve_color else None),
                    level["labels"][index].animate.set_color(colors[i%2]) if preserve_color else Indicate(level["labels"][index]),
                    lag_ratio=0.33
                ),
                run_time=rt
            )

    def counting_tree(self):
        scene_marker("Tælletræ")
        start_level = Tex("Isbutik").to_edge(UP)
        self.play(Write(start_level), run_time=0.5)

        labels = [
            ["Vaffel", "Bæger"],
            ["Vanille", "Chokolade", "Jordbær"],
            ["Krymmel", "Guf"]
        ]
        # node_colors = [
        #     [RED, YELLOW],
        #     [YELLOW, GREEN],
        #     [GREEN, PINK]
        # ]
        colors = [RED, YELLOW, GREEN, BLUE]
        node_colors = []
        for i in range(len(colors[:-1])):
            node_colors.append([colors[i], colors[i+1]])

        first_level = self.get_tree_branch(
            width=7,
            labels=labels[0],
            loc=start_level,
            font_size=42,
            node_cols=node_colors[0]
        )
        self.create_branch(first_level)
        self.slide_pause()

        second_level = [
            self.get_tree_branch(
                width=4,
                labels=labels[1],
                loc=label,
                font_size=32,
                node_cols=node_colors[1]
            ) for label in first_level["labels"]
        ]
        self.create_branch(second_level)
        self.slide_pause()

        third_level = [
            [
                self.get_tree_branch(
                    width=1,
                    labels=labels[2],
                    loc=label,
                    font_size=24,
                    node_cols=node_colors[2]
                ) for label in group["labels"]
            ] for group in second_level
        ]
        self.create_branch(third_level)
        self.slide_pause()

        # for i in range(len(labels[0])):
        #     for j in range(len(labels[1])):
        #         for k in range(len(labels[2])):
        #             self.highlight_path(
        #                 levels=[first_level, second_level, third_level],
        #                 indices=[i, j, k],
        #                 node_cols=node_colors,
        #                 preserve_color=True,
        #                 rt=0.5
        #             )

        self.play(start_level.animate.set_color(colors[0]))
        self.highlight_path(
            levels=[first_level, second_level, third_level],
            indices=[1, 0, 1],
            # color=YELLOW,
            node_cols=node_colors,
            preserve_color=True,
            rt=5
        )
        self.slide_pause()
