from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Static, Input


class Chord(Vertical):
   def __init__(self, position=0, **kwargs):
      super().__init__(**kwargs)
      self.position = position

   def compose(self) -> ComposeResult:
      self.border_title = "Chord"
      yield Static(" E  A  D  G  B  E ")
      yield Static(" ╒══╤══╤══╤══╤══╕ ")
      for row in range(5):
         yield Static(self.get_row(0))
         yield Static(" ├──┼──┼──┼──┼──┤ " if row == 4 else " ├──┼──┼──┼──┼──┤ ")


   def get_row(self, row: int) -> str:
      result = " │  │  │  │  │  │ "
      return result