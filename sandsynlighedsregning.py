from manim import *
from helpers import *
import numpy as np
import subprocess

slides = False
if slides:
    from manim_slides import Slide

quality = "high"


class FairDie(Slide if slides else MovingCameraScene):
    def construct(self):
        self.terning()
        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def get_graph_rects(self, plane, results, bar_sep=0.25, height_sep=0.01):
        offsets = np.zeros(6)
        graph_rects = VGroup()
        rect_labels = VGroup()
        for res in results:
            rect = Rectangle(
                height=plane.c2p(0, 1-height_sep)[1] - plane.c2p(0, 0)[1],
                width=plane.c2p(1-0.5*bar_sep, 0)[0] - plane.c2p(0, 0)[0]
            ).set_style(
                fill_opacity=1,
                stroke_width=0.1,
                fill_color=BLUE_C
            ).move_to(plane.c2p(res, 0.5 + offsets[res-1] - 0.5*height_sep))
            offsets[res-1] += 1
            label = DecimalNumber(offsets[res-1], num_decimal_places=0).scale(0.5).next_to(rect, UP)
            graph_rects.add(rect)
            rect_labels.add(label)
        return graph_rects, rect_labels

    def get_axhlines(self, plane):
        axhlines = VGroup()
        xmax = plane.axes[0].get_tick_range()[-1]
        for tick in plane.axes[1].get_tick_range():
            axhlines.add(
                DashedLine(
                    start=plane.c2p(0, tick),
                    end=plane.c2p(xmax, tick),
                    stroke_width=0.25
                )
            )
        return axhlines

    def terning(self):
        np.random.seed(14)
        cmap = {
            "ærlig": PINK
        }
        opener = Tex("Hvad er en ", "ærlig", " terning?").set_color_by_tex_to_color_map(cmap)
        self.play(
            Write(opener),
            run_time=0.5
        )
        self.slide_pause()
        self.play(
            opener.animate.to_edge(UL)
        )
        self.slide_pause()

        dice = VGroup(*[DieFace(n + 1) for n in range(6)]).arrange(RIGHT).shift(2*RIGHT)
        self.play(
            LaggedStart(
                *[
                    DrawBorderThenFill(die) for die in dice
                ],
                lag_ratio=0.2
            ),
            run_time=1
        )
        self.slide_pause()

        nums_rolls = [10, 60, 60, 60, 600]
        planes = VGroup(*[
            Axes(
                x_range=[0, 7, 1],
                y_range=[0, num_rolls * 0.4, max(min(num_rolls // 15, num_rolls // 20), num_rolls // 10)],
                x_length=8,
                y_length=12,
                tips=False
            ).add_coordinates().scale(0.4).to_edge(DL) for num_rolls in nums_rolls
        ])
        axs_hlines = VGroup(*[
            self.get_axhlines(plane) for plane in planes
        ])

        for iexp, plane, num_rolls, ax_hlines in zip(range(len(nums_rolls)), planes, nums_rolls, axs_hlines):
            results = np.random.randint(low=1, high=7, size=num_rolls)
            rolls = VGroup(*[
                DieFace(num, fill_color=YELLOW).move_to(dice[num-1]) for num in results
            ])
            graph_rects, rect_labels = self.get_graph_rects(plane, results)

            if iexp == 0:
                self.play(
                    DrawBorderThenFill(plane),
                    Create(ax_hlines)
                )
                self.slide_pause()
            else:
                self.play(
                    # FadeOut(VGroup(planes[iexp-1], axs_hlines[iexp-1])),
                    FadeIn(VGroup(plane, ax_hlines)),
                    run_time=1
                )

            for i, die, graph_rect in zip(range(num_rolls), rolls, graph_rects):
                if iexp + i > 0:
                    self.remove(tekst)
                tekst = Tex(f"Antal slag med terning: {i+1}").scale(0.5).next_to(plane, UP, aligned_edge=LEFT)
                if iexp + i == 0:
                    self.play(Write(tekst), run_time=0.5)
                else:
                    self.add(tekst)
                self.add(die)
                if i <= 10:
                    self.play(
                        TransformFromCopy(die, graph_rect),
                        run_time=1 if i <= 5 and iexp <= 1 else 0.5
                    )
                else:
                    self.add(graph_rect)
                    self.wait(1/15 if quality == "low" else 1/60)
                self.remove(die)

            self.slide_pause()
            summa = [len([i for i in results if i == n]) for n in [1, 2, 3, 4, 5, 6]]
            print(summa)
            sumtekst = VGroup(*[
                MathTex(
                    f"{s}\\over{sum(summa)}", color=RED, font_size=20
                ).move_to(
                    plane.c2p(i+1, plane.axes[1].get_tick_range()[-1]*0.85)
                ) for i, s in enumerate(summa)
            ])
            self.play(
                Write(sumtekst),
                run_time=0.5
            )
            self.slide_pause()
            sumpct = VGroup(*[
                MathTex(
                    f"{s/sum(summa)*100:.2f} \\%", color=RED, font_size=32
                ).next_to(die, DOWN) for s, die in zip(summa, dice)
            ])
            self.play(
                LaggedStart(
                    *[
                        TransformFromCopy(frac, pct) for frac, pct in zip(sumtekst, sumpct)
                    ],
                    lag_ratio=0.1
                ),
                run_time=2
            )
            self.slide_pause()
            self.play(FadeOut(graph_rects, plane, ax_hlines, sumtekst, sumpct), run_time=0.25)
        self.play(FadeOut(tekst))

        scene_marker("6 MILLIONER TERNINGER")
        tekst = Tex("Nu simulerer vi 6 mio. slag med en terning", font_size=30).next_to(dice, UP)
        plane = Axes(
            x_range=[0, 6.9, 1],
            y_range=[0, 3E6 * 0.4, max(min(3E6 // 15, 3E6 // 20), 3E6 // 10)],
            x_length=8,
            y_length=12,
            tips=False
        ).add_coordinates().scale(0.4).to_edge(DL)
        ax_hlines = self.get_axhlines(plane)
        results = np.random.randint(low=1, high=7, size=6_000_000)
        summa = [len([i for i in results if i == n]) for n in [1, 2, 3, 4, 5, 6]]
        sumtekst = VGroup(*[
            MathTex(
                f"{s}\\over{sum(summa)}", color=RED, font_size=4
            ).move_to(
                plane.c2p(i+1, plane.axes[1].get_tick_range()[-1]*0.85)
            ) for i, s in enumerate(summa)
        ])
        sumpct = VGroup(*[
            MathTex(
                f"{s/sum(summa)*100:.3f} \\%", color=RED, font_size=28
            ).next_to(die, DOWN) for s, die in zip(summa, dice)
        ])
        print(summa)

        graph_rects = VGroup(*[
            Rectangle(
                height=plane.c2p(0, res)[1] - plane.c2p(0, 0)[1],
                width=plane.c2p(0.875, 0)[0] - plane.c2p(0, 0)[0]
            ).set_style(
                fill_opacity=1,
                stroke_width=0.1,
                fill_color=BLUE_C
            ).move_to(plane.c2p(i + 1, 0.5 * res)) for i, res in enumerate(summa)
        ])
        self.play(
            DrawBorderThenFill(plane, ax_hlines),
            Write(tekst),
            run_time=0.5
        )
        self.slide_pause()
        self.play(
            FadeIn(graph_rects),
            LaggedStart(
                Write(sumtekst),
                LaggedStart(
                    *[
                        TransformFromCopy(frac, pct) for frac, pct in zip(sumtekst, sumpct)
                    ],
                    lag_ratio=0.4
                ),
                lag_ratio=0.5
            ),
            run_time=2
        )
        self.slide_pause()

        self.camera.frame.save_state()
        self.play(
            self.camera.frame.animate.set(
                width=1
            ).move_to(plane.c2p(1.5, np.mean(summa))),
            run_time=4
        )
        self.slide_pause()
        self.play(
            self.camera.frame.animate.move_to(plane.c2p(5.5, np.mean(summa))),
            run_time=10
        )
        self.slide_pause()
        self.play(
            Restore(self.camera.frame),
            run_time=4
        )



class MultiOgAddiPrincip(Slide if slides else MovingCameraScene):
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

        self.play(start_level.animate.set_color(colors[0]))
        self.highlight_path(
            levels=[first_level, second_level, third_level],
            indices=[1, 0, 1],
            node_cols=node_colors,
            preserve_color=True,
            rt=5
        )
        self.slide_pause()

        scene_marker("Multiplikationsprincippet")
        self.camera.frame.save_state()
        self.play(
            self.camera.frame.animate.set(
                width=20
            ).move_to(ORIGIN + 2*DR),
            run_time=3
        )


# subprocess.call([r"manim .\sandsynlighedsregning.py FairDie -pql"])
