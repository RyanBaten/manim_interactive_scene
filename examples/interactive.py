from manimlib import *
from manim_interactive_scene.interactive import InteractiveScene
from manim_interactive_scene.util import EasyTex


class SampleInteractiveScene(InteractiveScene):
    """Should show a square and its transformation to a circle interactively."""

    def construct(self):
        circle = Circle()
        circle.set_fill(BLUE, opacity=0.5)
        circle.set_stroke(BLUE_E, width=4)
        square = Square()
        self.play(ShowCreation(square))
        self.play(ReplacementTransform(square, circle))


class TestInteractive(InteractiveScene):
    """Should be an interactive scene, use f and d to switch between animations, q to exit"""

    def construct(self):
        texes = [
            EasyTex(x)
            for x in [
                "A x + b = 0",
                "A x = - b",
                "A^{-1} A x = - A^{-1} b",
                "I x = - A^{-1} b",
                "x = - A^{-1} b",
                "Done",
            ]
        ]
        self.add(texes[0])
        for i in range(1, len(texes)):
            self.save_checkpoint(i)
            self.play(TransformMatchingTex(texes[i - 1], texes[i]))
        for i in range(1, len(texes)):
            self.load_checkpoint(i)
