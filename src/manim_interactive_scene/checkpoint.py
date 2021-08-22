from .util import Registry
from manimlib.scene.scene import Scene


class SceneCheckpoint:
    """An object which holds scene state for checkpointing.

    Args:
        scene (Scene): The input Scene to save.
    """

    def __init__(self, scene):
        self.mobjects = scene.mobjects
        self.mobject_states = [mob.copy() for mob in scene.mobjects]


class CheckpointSceneMixin:
    """Mixin to enable checkpointing in a Scene."""

    def ensure_init_checkpoint_mixin(self):
        """Ensures that the checkpoint registry exists."""
        if not hasattr(self, "_checkpoint_registry"):
            self._checkpoint_registry = Registry()

    def save_checkpoint(self, key=None):
        """Saves a checkpoint to the registry with a given key.

        Args:
            key: The key to use in the registry to store the Scene state.
        """
        self.ensure_init_checkpoint_mixin()
        self._checkpoint_registry.register(SceneCheckpoint(self), key=key)

    def load_checkpoint(self, key=None):
        """Loads a checkpoint to the current scene.

        Args:
            key: The key to use to retrieve a scene from the registry.
        """
        self.ensure_init_checkpoint_mixin()
        if not len(self._checkpoint_registry):
            return
        checkpoint = self._checkpoint_registry.pop(key=key)
        for mob, state in zip(checkpoint.mobjects, checkpoint.mobject_states):
            mob.become(state)
        self.mobjects = checkpoint.mobjects


class CheckpointScene(CheckpointSceneMixin, Scene):
    """A Scene using the CheckpointSceneMixin mixin."""

    pass
