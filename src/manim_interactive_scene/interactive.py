from .util import Registry
from .checkpoint import CheckpointSceneMixin
from .keyboard import KeyboardControlledSceneMixin

from manimlib.scene.scene import EndSceneEarlyException, Scene
import time


class SceneStep:
    """An object representing a single interactive step to be performed.

    Args:
        func (str): String indicating the method name.
        *args: Arguments to pass to the method later.
        **kwargs: Keyword arguments to pass to the method later.
    """

    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs


class InteractiveScene(CheckpointSceneMixin, KeyboardControlledSceneMixin, Scene):
    """An interactive scene which only runs steps when the user presses certain buttons.

    Hotkeys are:
    - f to step forward
    - d to step backward
    - q to exit

    Args:
        **kwargs: Keyword arguments to pass through to Scene.
    """

    def __init__(self, **kwargs):
        super(InteractiveScene, self).__init__(**kwargs)
        self._interactive_step_registry = Registry()
        self._register_mode = False
        self._current_step = 0
        self.ensure_init_checkpoint_mixin()
        self.ensure_init_keyboard_mixin()

    @property
    def is_done(self):
        """Condition indicating if all steps have been cycled through."""
        return self._current_step > len(self._interactive_step_registry)

    def run(self):
        """Override run to handle registering steps vs running them. Also properly handles keypresses only when animations finish."""
        self.virtual_animation_start_time = 0
        self.real_animation_start_time = time.time()
        self.setup()
        try:
            self._register_mode = True
            self.construct()
            self._register_mode = False
            while not self.is_done:
                self.handle_pressed_keys()
                self.wait_until(self._keyboard_controller.was_pressed, max_time=0.1)
        except EndSceneEarlyException:
            pass
        exit()

    def register_step(self, func, *args, **kwargs):
        """Registers a single step in the step registry to run later, interactively.

        Args:
            func (str): String indicating the method name.
            *args: Arguments to pass to the method later.
            **kwargs: Keyword arguments to pass to the method later.
        """
        self._interactive_step_registry.register(
            SceneStep(func, *args, **kwargs), key=len(self._interactive_step_registry)
        )

    def add(self, *args, **kwargs):
        """Override to add to handle registering vs running.

        Args:
            *args: Passthrough arguments to Scene.add
            **kwargs: Passthrough keyword arguments to Scene.add
        """
        if self._register_mode:
            self.register_step("add", *args, **kwargs)
        else:
            super().add(*args, **kwargs)

    def play(self, *args, **kwargs):
        """Override to play to handle registering vs running.

        Args:
            *args: Passthrough arguments to Scene.play
            **kwargs: Passthrough keyword arguments to Scene.play
        """
        if self._register_mode:
            self.register_step("play", *args, **kwargs)
        else:
            super().play(*args, **kwargs)
            self.wait()

    def handle_pressed_keys(self):
        """Binds keys for keyboard presses to actions."""
        if "d" in self._keyboard_controller.pressed_keys:
            self.step_backward()
        elif "f" in self._keyboard_controller.pressed_keys:
            self.step_forward()
        elif "q" in self._keyboard_controller.pressed_keys:
            exit()
        self._keyboard_controller.reset()

    def step_forward(self):
        """Takes a single step forward in the registered steps to run."""
        self._current_step += 1
        if self.is_done:
            exit()
        self.save_checkpoint()
        step = self._interactive_step_registry[self._current_step - 1]
        getattr(super(InteractiveScene, self), step.func)(*step.args, **step.kwargs)

    def step_backward(self):
        """Loads the checkpoint for the previous step ran."""
        self._current_step = max(0, self._current_step - 1)
        self.load_checkpoint()
