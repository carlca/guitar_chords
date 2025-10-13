from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Static, Input


class Chord(Vertical):
   def __init__(self, **kwargs):
      super().__init__(position: int=0, **kwargs)
      self.position = position

   def compose(self) -> ComposeResult:
      self.border_title = "Chord"
      yield Static(" E  A  D  G  B  E ")
      yield Static("═╤══╤══╤══╤══╤══╤═")
      for f in range(5):
         yield Static()