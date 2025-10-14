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

   @abstractmethod
   def get_instrument_type(self) -> str:
      pass

   def get_string_tops(self) -> str:
      if self.position == 0:
         s =  " ╒═"
         s += "═╤═" * (self.get_string_count() - 2)
         s += "═╕ "
      else:
         s =  " ┌─"
         s += "─┬─" * (self.get_string_count() - 2)
         s += "─┐ "
         s += str(self.position)
      return s

   def get_fret_row(self, row: int) -> str:
      if row == 4:
         s =  " └─"
         s += "─┴─" * (self.get_string_count() - 2)
         s += "─┘ "
      else:
         s =  " ├─"
         s += "─┼─" * (self.get_string_count() - 2)
         s += "─┤ "
      return s

   def compose(self) -> ComposeResult:
      self.border_title = f"{self.get_instrument_type()} Chord"
      yield Static(self.get_string_names())
      yield Static(self.get_string_tops())
      for row in range(5):
         yield Static(self.get_row(0))
         yield Static(self.get_fret_row(row))

   def add_pattern(pattern: List[str]) -> None:
      pass

   def get_row(self, row: int) -> str:
      s = " │ " * self.get_string_count()
      return s


class GuitarChord(ChordBase):
   def get_string_count(self) -> int:
      return 6

   def get_string_names(self) -> str:
      return " E  A  D  G  B  E "

   def get_instrument_type(self) -> str:
      return "Guitar"


class UkeleleChord(ChordBase):
   def get_string_count(self) -> int:
      return 4

   def get_string_names(self) -> str:
      return " G  C  E  A "

   def get_instrument_type(self) -> str:
      return "Ukelele"
