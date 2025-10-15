from abc import ABC, abstractmethod
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Static, Input
from textual import log
from enum import Enum

class BarreType(Enum):
   UNASSIGNED = 0
   FULL = 1
   PART = 2


class ChordBase(Vertical):
   def __init__(self, position=0, **kwargs):
      super().__init__(**kwargs)
      self.barre_type = BarreType.UNASSIGNED
      self.position = position
      self.part_pos = 0
      self.show_pos = False
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
         s = " ╒═"
         s += "═╤═" * (self.get_string_count() - 2)
         s += "═╕ "
      else:
         s = " ┌─"
         s += "─┬─" * (self.get_string_count() - 2)
         s += "─┐ "
      return s

   def get_fret_row(self, row: int) -> str:
      if row == 4:
         s = " └─"
         s += "─┴─" * (self.get_string_count() - 2)
         s += "─┘ "
      else:
         s = " ├─"
         s += "─┼─" * (self.get_string_count() - 2)
         s += "─┤ "
         if row == 0 and self.show_pos:
            if self.position > 0:
               s += str(self.position)      
            if self.part_pos > 0:
               s += str(self.part_pos)
      return s

   def compose(self) -> ComposeResult:
      self.border_title = f"{self.get_instrument_type()} Chord"
      yield Static(self.get_string_names())
      yield Static(self.get_string_tops())
      for row in range(5):
         yield Static(self.get_row(row))
         yield Static(self.get_fret_row(row))

   def add_pattern(pattern: str, position: int = 0) -> None:
      # eg: C major "x32010"
      pass

   def add_full_barre(self, position: int):
      self.barre_type = BarreType.FULL
      self.position = position
      self.show_pos = True
      self.barre_from = 1
      self.barre_to = 6

   def add_part_barre(self, part_pos: int, show_pos: bool, barre_from: int, barre_to: int):
      self.barre_type = BarreType.PART
      self.part_pos = part_pos
      self.show_pos = show_pos
      self.barre_from = barre_from
      self.barre_to = barre_to

   def get_row(self, row: int) -> str:
      def get_barre():
         s = ""
         for string in range(1, self.get_string_count() + 1):
            if string < self.barre_from:
               s += " │ "
            elif string > self.barre_to:
               s += " │ "
            elif string == self.barre_from:
               s += " ◉ "
            elif string == self.barre_to:
               s += " ◉ "
            else:
               s += "━━━"
         self.barre_from = 0
         self.barre_to = 0
         return s
      match self.barre_type:
         case BarreType.FULL:
            if row == 0 and (self.barre_from > 1 or self.barre_to > 1):
               return get_barre()
         case BarreType.PART:
            if row == (self.part_pos - 1) and (self.barre_from > 1 or self.barre_to > 1):
               return get_barre()
      s = " │ " * (self.get_string_count())
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
