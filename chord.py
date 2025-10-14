from abc import ABC, abstractmethod
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Static, Input
from textual import log


class ChordBase(Vertical):
   def __init__(self, position=0, **kwargs):
      super().__init__(**kwargs)
      self.position = position
      self.barre_from = 0
      self.barre_to = 0

   @abstractmethod
   def get_strings(self) -> list[str]:
      pass

   @abstractmethod
   def get_instrument_type(self) -> str:
      pass

   def get_string_count(self) -> int:
      return len(self.get_strings())

   def get_string_names(self) -> str:
      s = ""
      for string in self.get_strings():
         s += f" {string} "
      return s

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

   def add_pattern(pattern: str, position: int = 0) -> None:
      # eg: C major "x32010"
      pass

   def add_barre(self, position: int, barre_from: int = 0, barre_to: int = 5):
      self.position = position
      self.barre_from = barre_from
      self.barre_to = barre_to

   def get_row(self, row: int) -> str:
      if row == 0 and (self.barre_from > 0 or self.barre_to > 0):
         s = ""
         for string in range(self.get_string_count()):
            if string < self.barre_from:
               s += " │ "
            elif string > self.barre_to:               
               s += " │ "
            elif string == self.barre_from:
               s += " ◉○"
            elif string == self.barre_to:
               s += " ◉○"
            else:
               s += "━━━"
         self.barre_from = 0
         self.barre_to = 0
         return s
      s = " │ " * self.get_string_count()
      return s


class GuitarChord(ChordBase):
   def get_strings(self) -> list[str]:
      return ["E", "A", "D", "G", "B", "E"]

   def get_instrument_type(self) -> str:
      return "Guitar"


class UkeleleChord(ChordBase):
   def get_strings(self) -> list[str]:
      return ["G", "C", "E", "A"]

   def get_instrument_type(self) -> str:
      return "Ukelele"
