from manimlib.event_handler import EVENT_DISPATCHER
from manimlib.event_handler.event_type import EventType


class KeyboardController:
    """Class to keep track of keyboard state."""

    def __init__(self):
        self.was_pressed = False
        self.pressed_keys = []

    def reset(self):
        """Resets the keyboard tracking state."""
        self.was_pressed = False
        self.pressed_keys = []

    def register_press(self, key):
        """Logs a key press to the set of pressed keys."""
        self.pressed_keys.append(key)
        self.was_pressed = True


class KeyboardControlledSceneMixin:
    """Mixin class that sets up on_key_press to handle key presses using the KeyboardController to track presses."""

    def ensure_init_keyboard_mixin(self):
        """Ensures that the keyboard controller exists."""
        if not hasattr(self, "_keyboard_controller"):
            self._keyboard_controller = KeyboardController()

    def on_key_press(self, symbol, modifiers):
        """Modified on_key_press to use the KeyboardController."""
        self.ensure_init_keyboard_mixin()
        try:
            char = chr(symbol)
        except OverflowError:
            print(" Warning: The value of the pressed key is too large.")
            return
        event_data = {"symbol": symbol, "modifiers": modifiers}
        propagate_event = EVENT_DISPATCHER.dispatch(
            EventType.KeyPressEvent, **event_data
        )
        if propagate_event is not None and propagate_event is False:
            return
        if char is not None:
            self._keyboard_controller.register_press(char)

    def handle_pressed_keys(self):
        """Use this function in the inheriting class to bind keys to actions."""
        pass
