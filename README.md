# Guitar Chords Widget

A Textual widget for displaying guitar chords with a simple API for representing any guitar chord.

## Features

- Visual representation of guitar chords on a fretboard
- Support for open chords, barre chords, and complex fingerings
- Configurable display options (finger numbers, tuning notes, fret numbers)
- Built-in library of common chords
- Support for different guitar tunings
- Copy chord patterns to clipboard
- Clean, customizable Textual widget

## Installation

```bash
pip install textual
```

## Quick Start

### Basic Usage

```python
from textual.app import App, ComposeResult
from chord_widget import ChordWidget
from chord import ChordLibrary

class SimpleChordApp(App):
    def compose(self) -> ComposeResult:
        yield ChordWidget(ChordLibrary.c_major())

if __name__ == "__main__":
    app = SimpleChordApp()
    app.run()
```

### Creating Custom Chords

```python
from chord import Chord, FretPosition, Barre, Tuning

# Create a simple C major chord
c_major = Chord(
    name="C",
    positions=[
        FretPosition(string=5, fret=3, finger=3),  # A string, 3rd fret
        FretPosition(string=4, fret=2, finger=2),  # D string, 2nd fret
        FretPosition(string=2, fret=0),            # G string, open
        FretPosition(string=1, fret=1, finger=1),  # B string, 1st fret
        FretPosition(string=0, fret=0),            # Low E string, open
    ]
)

# Create an F major barre chord
f_major = Chord(
    name="F",
    barre=Barre(start_string=5, end_string=1, fret=1, finger=1),
    positions=[
        FretPosition(string=4, fret=3, finger=3),  # D string, 3rd fret
        FretPosition(string=3, fret=3, finger=4),  # G string, 3rd fret
        FretPosition(string=2, fret=2, finger=2),  # B string, 2nd fret
    ]
)

# Use the chord in a widget
widget = ChordWidget(f_major)
```

### Widget Configuration

```python
# Create a widget with custom display options
widget = ChordWidget(
    chord=ChordLibrary.g_major(),
    show_fingers=True,      # Show finger numbers (1-4)
    show_tuning=True,       # Show tuning notes at the top
    show_fret_numbers=True  # Show fret numbers
)
```

### Using Different Tunings

```python
from chord import Chord, FretPosition, Tuning

# Create a chord for Drop D tuning
drop_d_chord = Chord(
    name="D Power",
    positions=[
        FretPosition(string=5, fret=0),  # Drop D (open)
        FretPosition(string=4, fret=0),  # A (open)
        FretPosition(string=3, fret=2),  # D, 2nd fret
        FretPosition(string=2, fret=3),  # G, 3rd fret
    ],
    tuning=Tuning.DROP_D
)
```

## Running the Demo

To see the widget in action with various chords and configuration options:

```bash
python demo.py
```

The demo includes:
- Multiple chord displays
- Interactive controls for toggling display options
- Keyboard shortcuts for quick navigation
- Examples of major, minor, and barre chords

### Demo Keyboard Shortcuts

- `q` - Quit the application
- `c` - Toggle control panel visibility
- `f` - Toggle finger number display
- `t` - Toggle tuning note display
- `n` - Toggle fret number display

## API Reference

### Chord Class

The main class for representing a guitar chord.

```python
@dataclass
class Chord:
    name: str
    positions: List[FretPosition]
    barre: Optional[Barre] = None
    tuning: Tuning = Tuning.STANDARD
```

#### Methods

- `get_min_fret()` - Get the minimum fret used in the chord
- `get_max_fret()` - Get the maximum fret used in the chord
- `is_string_played(string: int)` - Check if a string is played
- `get_fret_position(string: int)` - Get the fret position for a string
- `get_finger_position(string: int)` - Get the finger number for a string

### FretPosition Class

Represents a finger position on the fretboard.

```python
@dataclass
class FretPosition:
    string: int  # 0-5 (from low E to high e)
    fret: int   # 0-24, where 0 is an open string
    finger: Optional[int] = None  # 1-4 for finger numbering
```

### Barre Class

Represents a barre chord.

```python
@dataclass
class Barre:
    start_string: int  # 0-5
    end_string: int    # 0-5
    fret: int          # 1-24
    finger: int        # 1-4
```

### Tuning Enum

Supported guitar tunings.

- `Tuning.STANDARD` - E-A-D-G-B-E
- `Tuning.DROP_D` - D-A-D-G-B-E
- `Tuning.OPEN_G` - D-G-D-G-B-D
- `Tuning.OPEN_D` - D-A-D-F#-A-D
- `Tuning.OPEN_C` - C-G-C-G-C-E

### ChordWidget Class

The Textual widget for displaying chords.

```python
class ChordWidget(Static):
    def __init__(
        self,
        chord: Optional[Chord] = None,
        show_fingers: bool = True,
        show_tuning: bool = True,
        show_fret_numbers: bool = True,
        **kwargs
    )
```

#### Properties

- `chord` - The chord to display
- `show_fingers` - Whether to show finger numbers
- `show_tuning` - Whether to show tuning notes
- `show_fret_numbers` - Whether to show fret numbers

#### Methods

- `set_chord(chord: Chord)` - Set the chord to display

### ChordLibrary Class

A collection of common guitar chords.

Available methods:
- `ChordLibrary.c_major()` - C major chord
- `ChordLibrary.g_major()` - G major chord
- `ChordLibrary.d_major()` - D major chord
- `ChordLibrary.a_minor()` - A minor chord
- `ChordLibrary.e_minor()` - E minor chord
- `ChordLibrary.f_major()` - F major (barre) chord
- `ChordLibrary.b_minor()` - B minor (barre) chord

## Customization

The widget can be customized through CSS:

```python
ChordWidget {
    border: solid $primary;
    background: $surface;
}

.chord-name {
    text-align: center;
    text-style: bold;
    color: $accent;
}
```

## Contributing

Feel free to submit issues and enhancement requests!# guitar_chords
