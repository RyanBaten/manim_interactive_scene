# manim interactive scene

A repository containing manim scenes for checkpointing and interactive use.

## InteractiveScene
```InteractiveScene``` will show a scene in the order in which the commands are specified in construct one by one following keypresses.

Note: You should remove all wait calls in your construct function in the code for these scenes.

Hotkeys are:
- ```f``` to go forward a single step. If you reach the end, press one more time to exit.
- ```d``` to go back a single step.
- ```q``` to quit the interactive window.

```python
class SampleInteractiveScene(InteractiveScene):
    """Should show a square and its transformation to a circle interactively."""

    def construct(self):
        circle = Circle()
        circle.set_fill(BLUE, opacity=0.5)
        circle.set_stroke(BLUE_E, width=4)
        square = Square()
        self.play(ShowCreation(square))
        self.play(ReplacementTransform(square, circle))
```

To run the examples:
```
manimgl examples/interactive.py
```

## CheckpointScene
```CheckpointScene``` adds in methods ```save_checkpoint``` and ```load_checkpoint``` to easily save and load a scene's state within an animation.

```python
# When no keys are specified, it will load the checkpoints in reverse order, starting with the newest one.
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

# If checkpoint keys are specified, will load the specified checkpoint by key.
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
```

To run the examples:
```
manimgl examples/checkpointing.py
```