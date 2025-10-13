from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.widgets import Header, Footer, Static, Button, Checkbox, Switch
from textual.binding import Binding
from textual import log
from chord import Chord


class ChordDemoApp(App):
    """A demo application showcasing the ChordWidget"""

    CSS_PATH = "guitar_chords.tcss"

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("c", "toggle_controls", "Toggle Controls"),
        Binding("f", "toggle_fingers", "Toggle Fingers"),
        Binding("t", "toggle_tuning", "Toggle Tuning"),
        Binding("n", "toggle_fret_numbers", "Toggle Fret Numbers"),
    ]

    def on_mount(self) -> None:
        """Called when the app is mounted"""
        log("Guitar Chord Widget Demo started")

    def compose(self) -> ComposeResult:
        """Compose the app's UI"""
        yield Header()

        with ScrollableContainer(id="chord-display"):
            yield Static("Chord Display", classes="title")
            with Horizontal():
                with Vertical(classes="chord-container"):
                    yield Static("Major Chords", classes="subtitle")
                    yield Chord()
                    yield Chord()
                    yield Chord()          
                with Vertical(classes="chord-container"):
                    yield Static("Minor Chords", classes="subtitle")
                    yield Chord()
                    yield Chord()
                    yield Chord()                                        
        yield Footer()


if __name__ == "__main__":
    app = ChordDemoApp()
    app.run()
