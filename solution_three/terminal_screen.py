import struct
import sys
from itertools import islice

class TerminalScreen:
    def __init__(self):
        self.screen = None  # Screen as a 2D array
        self.width = 0
        self.height = 0
        self.color_mode = 0
        self.cursor_x = 0
        self.cursor_y = 0
        self.colors = ["\033[37m"]  # Default to white (monochrome)

    def setup_screen(self, width, height, color_mode):
        self.width = width
        self.height = height
        self.color_mode = color_mode
        self.screen = [[' ' for _ in range(width)] for _ in range(height)]
        if color_mode == 0x01:
            self.colors = [f"\033[3{i}m" for i in range(8)] + [f"\033[9{i}m" for i in range(8)]
        elif color_mode == 0x02:
            self.colors = [f"\033[38;5;{i}m" for i in range(256)]
        print(f"Screen initialized: {width}x{height}, Color mode: {color_mode}")

    def draw_character(self, x, y, color_index, char):
        if self._in_bounds(x, y):
            self.screen[y][x] = (char, self.colors[color_index])

    def draw_line(self, x1, y1, x2, y2, color_index, char):
        for x, y in self._bresenham(x1, y1, x2, y2):
            self.draw_character(x, y, color_index, char)

    def render_text(self, x, y, color_index, text):
        for i, char in enumerate(text):
            self.draw_character(x + i, y, color_index, char)

    def move_cursor(self, x, y):
        if self._in_bounds(x, y):
            self.cursor_x, self.cursor_y = x, y

    def draw_at_cursor(self, char, color_index):
        self.draw_character(self.cursor_x, self.cursor_y, color_index, char)

    def clear_screen(self):
        self.screen = [[' ' for _ in range(self.width)] for _ in range(self.height)]

    def display(self):
        for y, row in enumerate(self.screen):
            for x, cell in enumerate(row):
                char, color = cell if isinstance(cell, tuple) else (' ', self.colors[0])
                print(f"{color}{char}", end="")
            print("\033[0m")

    def _in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def _bresenham(self, x1, y1, x2, y2):
        dx, dy = abs(x2 - x1), abs(y2 - y1)
        sx, sy = (1 if x1 < x2 else -1), (1 if y1 < y2 else -1)
        err = dx - dy
        points = []
        while True:
            points.append((x1, y1))
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
        return points


def parse_binary_stream(binary_data):
    screen = TerminalScreen()
    index = 0

    while index < len(binary_data):
        cmd = binary_data[index]
        index += 1

        if cmd == 0x1:  # Screen setup
            width, height, color_mode = binary_data[index:index+3]
            index += 3
            screen.setup_screen(width, height, color_mode)

        elif cmd == 0x2:  # Draw character
            x, y, color_index, char = binary_data[index:index+4]
            index += 4
            screen.draw_character(x, y, color_index, chr(char))

        elif cmd == 0x3:  # Draw line
            x1, y1, x2, y2, color_index, char = binary_data[index:index+6]
            index += 6
            screen.draw_line(x1, y1, x2, y2, color_index, chr(char))

        elif cmd == 0x4:  # Render text
            x, y, color_index, length = binary_data[index:index+3]
            index += 3
            text = binary_data[index:index+length]
            index += length
            screen.render_text(x, y, color_index, ''.join(map(chr, text)))

        elif cmd == 0x5:  # Cursor movement
            x, y = binary_data[index:index+2]
            index += 2
            screen.move_cursor(x, y)

        elif cmd == 0x6:  # Draw at cursor
            char, color_index = binary_data[index:index+2]
            index += 2
            screen.draw_at_cursor(chr(char), color_index)

        elif cmd == 0x7:  # Clear screen
            screen.clear_screen()

        elif cmd == 0xFF:  # End of file
            break

        else:
            print(f"Unknown command: {cmd}")
            break

    return screen


if __name__ == "__main__":
    # Example binary data (screen setup and simple drawing)
    binary_stream = bytes([
        0x1, 80, 24, 0x01,  # Screen setup: 80x24, 16 colors
        0x2, 10, 5, 1, ord('A'),  # Draw character 'A' at (10, 5)
        0x3, 0, 0, 20, 10, 2, ord('-'),  # Draw line with '-' from (0, 0) to (20, 10)
        0xFF  # End of file
    ])

    screen = parse_binary_stream(binary_stream)
    screen.display()
