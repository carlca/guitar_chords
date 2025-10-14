from abc import ABC, abstractmethod
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Static, Input


class ChordBase(Vertical):
   def __init__(self, position=0, **kwargs):
      super().__init__(**kwargs)
      self.position = position

   @abstractmethod
   def get_string_names(self) -> str:
      pass

   @abstractmethod
   def get_string_count(self) -> int:
      pass

   def get_string_tops(self) -> str:
      s = " ╒═"
      s += "═╤═" * self.get_string_count() - 2
      s += "═╕ "
      return s

   def compose(self) -> ComposeResult:
      self.border_title = "Chord"
      yield Static(self.get_string_names())
      yield Static(self.get_string_tops() if self.position == 0 else f" ┌──┬──┬──┬──┬──┐ {self.position}")
      # " ╒══╤══╤══╤══╤══╕ " if self.position == 0 else f" ┌──┬──┬──┬──┬──┐ {self.position}")
      for row in range(5):
         yield Static(self.get_row(0))
         yield Static(" ├──┼──┼──┼──┼──┤ " if row < 4 else " └──┴──┴──┴──┴──┘ ")

   def add_pattern(pattern: List[str])-> None:
      pass

   def get_row(self, row: int) -> str:
      result = " │  │  │  │  │  │ "
      return result


class GuitarChord(ChordBase):

   def get_string_count(self) -> int:
      return 6

   def get_string_names(self) -> str:
      return " E  A  D  G  B  E "