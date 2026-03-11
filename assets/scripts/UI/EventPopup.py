from py4godot.classes import gdclass
from py4godot.classes.Control import Control


@gdclass
class EventPopup(Control):

    def _ready(self) -> None:
        self.panel = self.get_node("Panel")
        self.event_text = self.get_node("Panel/VBoxContainer/EventText")
        self.choice1 = self.get_node("Panel/VBoxContainer/Choice1")
        self.choice2 = self.get_node("Panel/VBoxContainer/Choice2")
        self.choice3 = self.get_node("Panel/VBoxContainer/Choice3")

        self.choice1.pressed.connect(self._on_choice1_pressed)
        self.choice2.pressed.connect(self._on_choice2_pressed)
        self.choice3.pressed.connect(self._on_choice3_pressed)

        self.visible = False
        self.correct_choice = -1
        self.event_manager = None

    def show_event(self, event_data, event_manager) -> None:
        self.event_manager = event_manager
        self.correct_choice = event_data["correct"]

        self.event_text.text = event_data["text"]
        self.choice1.text = event_data["choices"][0]
        self.choice2.text = event_data["choices"][1]
        self.choice3.text = event_data["choices"][2]

        self.visible = True

    def hide_event(self) -> None:
        self.visible = False

    def _on_choice1_pressed(self) -> None:
        self._submit_choice(0)

    def _on_choice2_pressed(self) -> None:
        self._submit_choice(1)

    def _on_choice3_pressed(self) -> None:
        self._submit_choice(2)

    def _submit_choice(self, index: int) -> None:
        self.visible = False

        if self.event_manager is not None:
            self.event_manager.resolve_event(index, self.correct_choice)