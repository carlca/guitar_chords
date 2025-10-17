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
   def __init__(self, position: int = 0, **kwargs):
      super().__init__(**kwargs)
      self.barre_type = BarreType.UNASSIGNED
      self.position = position
      self.full_pos = 0
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
      # Check if we're showing a position higher than the open position (fret 0)
      # For full barre, use full_pos; for partial barre, use part_pos
      if self.barre_type == BarreType.FULL:
         position = self.full_pos
      elif self.barre_type == BarreType.PART:
         position = self.part_pos
      else:
         position = 0
         
      if position <= 2:  # Show double lines for open position or first/second fret
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
         if self.show_pos:
            # Calculate actual fret position based on the highest barre
            max_fret = max(self.full_pos, self.part_pos)
            base_fret = max(1, max_fret - 2)  # Show at most 2 frets before the highest barre
            
            if row == 0 and self.barre_type == BarreType.FULL and self.full_pos > 0:
               s += str(self.full_pos)
            # For high fret positions (>= 4), show the fret number on the first row only
            elif self.barre_type == BarreType.PART and self.part_pos >= 3 and row == 0:
               s += str(self.part_pos)
            # For lower positions, show the fret number on the correct row
            elif (row == self.part_pos - base_fret and self.part_pos > 0 and self.part_pos < 3):
               s += str(self.part_pos)

      return s

   def compose(self) -> ComposeResult:
      self.border_title = f"{self.get_instrument_type()} Chord"
      yield Static(self.get_string_names())
      yield Static(self.get_string_tops())
      for row in range(5):
         yield Static(self.get_row(row))
         yield Static(self.get_fret_row(row))
      # yield Static(f"barre_type {self.barre_type}")
      # yield Static(f"position {self.position}")
      # yield Static(f"full_pos {self.full_pos}")
      # yield Static(f"part_pos {self.part_pos}")
      # yield Static(f"show_pos {self.show_pos}")


   def add_pattern(pattern: str, full_pos: int = 0) -> None:
      # eg: C major "x32010"
      pass

   def add_full_barre(self, full_pos: int):
      self.barre_type = BarreType.FULL
      self.full_pos = full_pos
      self.show_pos = True
      self.barre_from = 1
      self.barre_to = self.get_string_count()

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
         return s
      match self.barre_type:
         case BarreType.FULL:
            if row == 0 and (self.barre_from > 1 or self.barre_to > 1):
               return get_barre()
         case BarreType.PART:
            # For high fret positions (>= 4), display in first position
            if self.part_pos >= 3:
               display_row = 0
            else:
               # Calculate which row to display the part barre on
               max_fret = max(self.full_pos, self.part_pos)
               base_fret = max(1, max_fret - 2)  # Show at most 2 frets before the highest barre
               display_row = self.part_pos - base_fret
            
            if row == display_row and (self.barre_from > 1 or self.barre_to > 1):
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
