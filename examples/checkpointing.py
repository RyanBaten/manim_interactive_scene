from manimlib import *
from manim_interactive_scene.checkpoint import CheckpointScene
from manim_interactive_scene.util import EasyTex


class SampleCheckpointScene(CheckpointScene):
    """Should show a square, transformation to a circle, and the square again."""

    def construct(self):
        circle = Circle()
        circle.set_fill(BLUE, opacity=0.5)
        circle.set_stroke(BLUE_E, width=4)
        square = Square()
        self.play(ShowCreation(square))
        self.save_checkpoint()
        self.wait()
        self.play(ReplacementTransform(square, circle))
        self.wait()
        self.load_checkpoint()


class SampleCheckpointSceneWithKeys(CheckpointScene):
    """Should show a square, transformation to a circle, an empty screen, and the square again."""

    def construct(self):
        circle = Circle()
        circle.set_fill(BLUE, opacity=0.5)
        circle.set_stroke(BLUE_E, width=4)
        square = Square()
        self.save_checkpoint("b")
        self.play(ShowCreation(square))
        self.save_checkpoint("a")
        self.wait()
        self.play(ReplacementTransform(square, circle))
        self.wait()
        self.load_checkpoint("b")
        self.wait(2)
        self.load_checkpoint("a")


class TestCheckpointing(CheckpointScene):
    """Should show once with animations and once again without animations (loading checkpoints)."""

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
            self.wait()
        for i in range(1, len(texes)):
            self.load_checkpoint(i)
            self.wait()


class TestCheckpointing2(CheckpointScene):
    """Should show once and then load checkpoints in reverse order of the running order."""

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
            self.save_checkpoint()
            self.play(TransformMatchingTex(texes[i - 1], texes[i]))
            self.wait()
        for i in range(1, len(texes)):
            self.load_checkpoint()
            self.wait()
