from abc import ABC, abstractmethod
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Static, Input
from textual import log
from enum import Enum


class BarreType(Enum):
   NONE = 0
   FULL = 1
   PART = 2


SECOND_FRET = 2
FRET_OFFSET = 2
FRET_COUNT = 4

class ChordBase(Vertical):
   def __init__(self, **kwargs):
      super().__init__(**kwargs)
      self.barre_type = BarreType.NONE
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

   @property
   def string_count(self) -> int:
      return len(self.get_strings())

   def get_string_names(self) -> str:
      return " ".join(f" {s}" for s in self.get_strings())

   def _get_current_barre_position(self) -> int:
      """Get the current barre position based on barre type."""
      if self.barre_type == BarreType.FULL:
         return self.full_pos
      elif self.barre_type == BarreType.PART:
         return self.part_pos
      else:
         return 0

   def get_string_tops(self) -> str:
      position = self._get_current_barre_position()
      count = self.string_count
      if position <= SECOND_FRET:
         parts = [" ╒═"] + ["═╤═"] * (count - 2) + ["═╕ "]
      else:
         parts = [" ┌─"] + ["─┬─"] * (count - 2) + ["─┐ "]
      return "".join(parts)

   def _calculate_base_fret(self) -> int:
      """Calculate the base fret position."""
      max_fret = max(self.full_pos, self.part_pos)
      return max(1, max_fret - FRET_OFFSET)

   def _get_fret_number_to_show(self, row: int, base_fret: int) -> int | None:
      """Determine which fret number to show for a given row."""
      if not self.show_pos:
         return None

      if row == 0 and self.barre_type == BarreType.FULL and self.full_pos > 0:
         return self.full_pos
      elif self.barre_type == BarreType.PART and self.part_pos >= 3 and row == 0:
         return self.part_pos
      elif row == self.part_pos - base_fret and 0 < self.part_pos < 3:
         return self.part_pos
      return None

   def _calculate_display_row(self) -> int:
      """Calculate which row to display a partial barre on."""
      max_fret = max(self.full_pos, self.part_pos)
      base_fret = max(1, max_fret - FRET_OFFSET)
      return self.part_pos - base_fret

   def get_fret_row(self, row: int) -> str:
      count = self.string_count
      if row == FRET_COUNT - 1:
         parts = [" └─"] + ["─┴─"] * (count - 2) + ["─┘ "]
      else:
         parts = [" ├─"] + ["─┼─"] * (count - 2) + ["─┤ "]
      # Check if we need to add a fret number
      if self.show_pos:
         base_fret = self._calculate_base_fret()
         fret_num = self._get_fret_number_to_show(row, base_fret)
         if fret_num:
            parts[-1] = parts[-1][:-1] + str(fret_num) + " "

      return "".join(parts)

   def compose(self) -> ComposeResult:
      self.border_title = f"{self.get_instrument_type()} Chord"
      yield Static(self.get_string_names())
      yield Static(self.get_string_tops())
      for row in range(FRET_COUNT):
         yield Static(self.get_row(row))
         yield Static(self.get_fret_row(row))

   def add_pattern(self, pattern: str, full_pos: int = 0) -> None:
      # eg: C major "x32010"
      pass

   def add_full_barre(self, full_pos: int):
      self.barre_type = BarreType.FULL
      self.full_pos = full_pos
      self.show_pos = True
      self.barre_from = 1
      self.barre_to = self.string_count

   def add_part_barre(self, part_pos: int, show_pos: bool, barre_from: int, barre_to: int):
      self.barre_type = BarreType.PART
      self.part_pos = part_pos
      self.show_pos = show_pos
      self.barre_from = barre_from
      self.barre_to = barre_to

   def _should_show_barre(self, row: int) -> bool:
      if self.barre_type == BarreType.FULL:
         return row == 0 and (self.barre_from > 1 or self.barre_to > 1)

      if self.barre_type == BarreType.PART:
         display_row = 0 if self.part_pos >= 3 else self._calculate_display_row()
         return row == display_row and (self.barre_from > 1 or self.barre_to > 1)

      return False

   def _build_barre_row(self) -> str:
      cells = []
      for string in range(1, self.string_count + 1):
         if string < self.barre_from or string > self.barre_to:
            cells.append(" │ ")
         elif string == self.barre_from or string == self.barre_to:
            cells.append(" ◉ ")
         else:
            cells.append("━━━")
      return "".join(cells)

   def get_row(self, row: int) -> str:
      if self._should_show_barre(row):
         return self._build_barre_row()

      return " │ " * self.string_count



class GuitarChord(ChordBase):
   def get_strings(self) -> list[str]:
      return ["E", "A", "D", "G", "B", "E"]

   def get_instrument_type(self) -> str:
      return "Guitar"


class UkuleleChord(ChordBase):
   def get_strings(self) -> list[str]:
      return ["G", "C", "E", "A"]

   def get_instrument_type(self) -> str:
      return "Ukulele"
