from dataclasses import dataclass, field

@dataclass
class KeyboardBase:
    row_width: int = 3
    keyboard: list[list] = field(default_factory=list)

    def add(self, *args: object) -> None:
        """Add buttons to keyboard with specified row width."""
        self.keyboard = [
            list(args[i : i + self.row_width])
            for i in range(0, len(args), self.row_width)
        ]

    def row(self, *args: object) -> None:
        """Add a row of buttons."""
        self.keyboard.append(list(args))
