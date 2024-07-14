from shutil import get_terminal_size
import sys
from typing import Callable, Iterable, Any
import evdev
import time
from threading import Thread, Event


class ScreenOverflowError(Exception):
    def __init__(self, lines=None, columns=None):
        if lines and columns:
            super().__init__(f"Overflow of the screen size (current terminal size: (lines: {lines}, columns: {columns})).")
        else:
            super().__init__(f'Overflow of the screen size')


class Keyboard:
    ecodes = evdev.ecodes

    def __init__(self) -> None:
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device in devices:
            if device.name == 'SIGMACHIP USB Keyboard':
                self.device = device
                return

        raise Exception("Was not possible to identify the keyboard")

    def __iter__(self) -> Iterable:
        for event in self.device.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                yield event

    def _verify_interrupt(self):
        ctrl_pressed = any([self.ecodes.KEY_LEFTCTRL in self.device.active_keys(), 
                            self.ecodes.KEY_RIGHTCTRL in self.device.active_keys()])

        escape_key_pressed = any([self.ecodes.KEY_Q in self.device.active_keys(),
                                  self.ecodes.KEY_Z in self.device.active_keys(),
                                  self.ecodes.KEY_C in self.device.active_keys()])

        if ctrl_pressed and escape_key_pressed:
            raise KeyboardInterrupt()

    def listener(self, func: Callable) -> Any:
        def listener_loop(func):
            for event in self:
                func(event)
                    
        listener_thread = Thread(target=listener_loop, args=(func, ), daemon=True)
        listener_thread.start()


class Screen:
    def _get_screen(self, lines: int, columns: int) -> list[list, ...]:
        screen = []
        for line in range(self.lines):
            new_line = []
            for column in range(self.columns):
                new_line.append(' ')
            screen.append(new_line)

        return screen

    def __init__(self) -> None:
        terminal_size = get_terminal_size()
        self.lines = terminal_size.lines
        self.columns = terminal_size.columns
        self.screen = self._get_screen(self.lines, self.columns)
        self.base = self._get_screen(self.lines, self.columns)
        self.keyboard = Keyboard()

    def _hide_cursor(self) -> None:
        sys.stdout.write('\033[?25l', caller=True)

    def _write_screen(self) -> None:
        sys.stdout.write('\033[3J', caller=True)
        sys.stdout.write('\033[1;1H', caller=True)
        for line in self.screen:
            for char in line:
                sys.stdout.write(char, caller=True)

    def refresh(self, sleep=0) -> None:
        self.keyboard._verify_interrupt()
        self._write_screen()

    def clear(self) -> None:
        self.screen = [line[:] for line in self.base]

    def getmaxyx(self) -> tuple[int, int]:
        return self.lines, self.columns

    def addstr(self, line: int, column: int, string: str) -> None:
        try:
            if line < 0 or column < 0:
                raise IndexError()
            if line > self.lines or column > self.columns:
                raise IndexError()

            for i in range(len(string)):
                self.screen[line][column + i] = string[i]

        except IndexError:
            raise ScreenOverflowError(self.lines, self.columns)
    
    def enum_lines(self) -> None:
        for i in range(self.lines):
            self.addstr(i, 0, str(i))

    def __repr__(self) -> str:
        return f'Screen(lines={self.lines}, columns={self.columns})'


class WrapperContextManager:
    def __init__(self, screen: Screen) -> None:
        self.screen = screen
        self.default_writer = sys.stdout.write

        def new_writer(string: str, caller=False) -> int:
            if not caller:
                self.default_writer('')
            else:
                self.default_writer(string)

        sys.stdout.write = new_writer

    def __enter__(self):
        self.screen._hide_cursor()
        self.screen.keyboard.device.grab()

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.screen.keyboard.device.ungrab()
        sys.stdout.write = self.default_writer
        sys.stdout.write('\033[H\033[3J\033[2J')
        sys.stdout.write('\033[?25h')


def wrapper(func: Callable) -> None:
    screen = Screen()
    with WrapperContextManager(screen):
            func(screen)


if __name__ == '__main__':
    def teste(scr):
        x = y = 10

        @scr.keyboard.listener
        def controller(event):
            with open('log.log', 'a') as log:
                print(event.code, file=log)
                print(event, file=log)
            if event.code == 36:
                y += 1

        while True:
            scr.addstr(y, 10, 'Gustavo')
            scr.refresh()

    wrapper(teste)
