from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Static, Input


class Chord(Vertical):
   def compose(self) -> ComposeResult:
      self.border_title = "Chord"
      yield Static("E A D G B E")