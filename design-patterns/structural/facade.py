"""
Facade Pattern
When to use: When you need to provide a simple, unified interface to a complex subsystem. Use when you want to decouple clients from a complex system of components, or to layer your subsystem (facade as entry point to each layer).

Real-world examples:
- Django REST Framework APIView (wraps request handling, authentication, serialization)
- Complex library wrappers (FFmpeg, OpenCV, PDF generation)
- Home theater automation systems
- Database connection pool managers
- Cloud SDK service clients (boto3 S3 client)
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional
import time


class PowerState(Enum):
    OFF = auto()
    ON = auto()
    STANDBY = auto()


@dataclass
class Component:
    name: str
    _state: PowerState = PowerState.OFF

    def on(self) -> None:
        self._state = PowerState.ON
        print(f"  {self.name}: Power ON")

    def off(self) -> None:
        self._state = PowerState.OFF
        print(f"  {self.name}: Power OFF")

    @property
    def is_on(self) -> bool:
        return self._state == PowerState.ON


class Amplifier(Component):
    def __init__(self):
        super().__init__("Amplifier")
        self._volume = 30
        self._muted = False
        self._input_source: Optional[str] = None

    def set_volume(self, level: int) -> None:
        self._volume = max(0, min(100, level))
        print(f"  Amplifier: Volume set to {self._volume}")

    def set_input(self, source: str) -> None:
        self._input_source = source
        print(f"  Amplifier: Input set to {source}")

    def mute(self) -> None:
        self._muted = True
        print(f"  Amplifier: Muted")

    def unmute(self) -> None:
        self._muted = False
        print(f"  Amplifier: Unmuted")

    def set_surround_sound(self) -> None:
        print(f"  Amplifier: Surround sound enabled (5.1 channel)")


class DVDPlayer(Component):
    def __init__(self):
        super().__init__("DVD Player")
        self._disc_loaded = False
        self._playing = False
        self._current_track = 0
        self._current_title = ""

    def load_disc(self, title: str) -> None:
        self._disc_loaded = True
        self._current_title = title
        self._current_track = 1
        print(f"  DVD Player: Loaded '{title}'")

    def eject(self) -> None:
        if self._playing:
            self.stop()
        self._disc_loaded = False
        self._current_title = ""
        print(f"  DVD Player: Disc ejected")

    def play(self) -> None:
        if not self._disc_loaded:
            print(f"  DVD Player: No disc loaded!")
            return
        self._playing = True
        print(f"  DVD Player: Playing '{self._current_title}' (track {self._current_track})")

    def pause(self) -> None:
        if self._playing:
            self._playing = False
            print(f"  DVD Player: Paused")

    def stop(self) -> None:
        self._playing = False
        print(f"  DVD Player: Stopped")

    def next_track(self) -> None:
        if self._disc_loaded:
            self._current_track += 1
            print(f"  DVD Player: Track {self._current_track}")

    def previous_track(self) -> None:
        if self._disc_loaded and self._current_track > 1:
            self._current_track -= 1
            print(f"  DVD Player: Track {self._current_track}")


class Projector(Component):
    def __init__(self):
        super().__init__("Projector")
        self._resolution = "4K (3840x2160)"
        self._aspect_ratio = "16:9"
        self._lamp_hours = 0

    def set_input(self, source: str) -> None:
        print(f"  Projector: Input set to {source}")

    def set_widescreen(self) -> None:
        self._aspect_ratio = "16:9"
        print(f"  Projector: Widescreen mode (16:9)")

    def set_cinema_mode(self) -> None:
        print(f"  Projector: Cinema mode activated — enhanced contrast, warm color temp")

    def lower_screen(self) -> None:
        print(f"  Projector: Motorized screen descending...")


class TheaterLights(Component):
    def __init__(self):
        super().__init__("Theater Lights")
        self._brightness = 100
        self._color = "warm white"

    def dim(self, percent: int) -> None:
        self._brightness = max(0, min(100, percent))
        print(f"  Theater Lights: Dimmed to {self._brightness}%")

    def set_color(self, color: str) -> None:
        self._color = color
        print(f"  Theater Lights: Color set to {color}")

    def full_brightness(self) -> None:
        self._brightness = 100
        print(f"  Theater Lights: Full brightness")


class Screen(Component):
    def __init__(self):
        super().__init__("Screen")

    def lower(self) -> None:
        print(f"  Screen: Lowering...")

    def raise_screen(self) -> None:
        print(f"  Screen: Raising...")

    def set_aspect_ratio(self, ratio: str) -> None:
        print(f"  Screen: Aspect ratio set to {ratio}")


class PopcornPopper(Component):
    def __init__(self):
        super().__init__("Popcorn Popper")

    def start(self) -> None:
        print(f"  Popcorn Popper: Making fresh popcorn...")

    def stop(self) -> None:
        print(f"  Popcorn Popper: Stopped")

    def keep_warm(self) -> None:
        print(f"  Popcorn Popper: Keeping popcorn warm")


class SoundBar(Component):
    def __init__(self):
        super().__init__("SoundBar")
        self._volume = 25
        self._mode = "standard"

    def set_volume(self, level: int) -> None:
        self._volume = max(0, min(100, level))
        print(f"  SoundBar: Volume set to {self._volume}")

    def set_mode(self, mode: str) -> None:
        valid_modes = {"standard", "movie", "music", "night", "sports"}
        if mode in valid_modes:
            self._mode = mode
            print(f"  SoundBar: Mode set to '{mode}'")
        else:
            print(f"  SoundBar: Unknown mode '{mode}', keeping '{self._mode}'")


class HomeTheaterFacade:
    def __init__(self):
        self.amp = Amplifier()
        self.dvd = DVDPlayer()
        self.projector = Projector()
        self.lights = TheaterLights()
        self.screen = Screen()
        self.popper = PopcornPopper()
        self.soundbar = SoundBar()

    def watch_movie(self, movie_title: str) -> None:
        print(f"\n{'='*60}")
        print(f"[Movie] Starting movie night: '{movie_title}'")
        print(f"{'='*60}")

        self.popper.start()
        self.popper.keep_warm()

        self.lights.dim(15)
        self.lights.set_color("warm white")

        self.screen.lower()
        self.projector.on()
        self.projector.set_input("HDMI 1")
        self.projector.set_widescreen()
        self.projector.set_cinema_mode()

        self.amp.on()
        self.amp.set_input("DVD")
        self.amp.set_surround_sound()
        self.amp.set_volume(35)

        self.soundbar.on()
        self.soundbar.set_mode("movie")
        self.soundbar.set_volume(30)

        self.dvd.on()
        self.dvd.load_disc(movie_title)
        self.dvd.play()

        print(f"\n[Enjoy] Your movie! {'='*60}\n")

    def end_movie(self) -> None:
        print(f"\n{'='*60}")
        print(f"[Stop] Shutting down theater")
        print(f"{'='*60}")

        self.dvd.stop()
        self.dvd.eject()
        self.dvd.off()

        self.projector.off()
        self.screen.raise_screen()

        self.amp.off()
        self.soundbar.off()
        self.popper.stop()

        self.lights.full_brightness()
        print(f"\n[Home] Theater ready for next use {'='*60}\n")

    def listen_to_music(self) -> None:
        print(f"\n{'='*60}")
        print(f"[Music] Starting music mode")
        print(f"{'='*60}")

        self.lights.dim(40)
        self.lights.set_color("blue")

        self.amp.on()
        self.amp.set_input("AUX")
        self.amp.set_volume(25)

        self.soundbar.on()
        self.soundbar.set_mode("music")
        self.soundbar.set_volume(22)

        print(f"\n[Music] Playing... {'='*60}\n")

    def set_volume(self, level: int) -> None:
        self.amp.set_volume(level)
        self.soundbar.set_volume(level)

    def mute(self) -> None:
        self.amp.mute()
        self.soundbar.set_volume(0)


class HomeTheaterStatus:
    @staticmethod
    def report(facade: HomeTheaterFacade) -> str:
        parts = []
        for component in [facade.amp, facade.dvd, facade.projector, facade.lights, facade.screen, facade.popper, facade.soundbar]:
            state = "ON" if component.is_on else "OFF"
            parts.append(f"{component.name}: {state}")
        return " | ".join(parts)


if __name__ == "__main__":
    theater = HomeTheaterFacade()

    print("=== Home Theater System Status ===")
    print(HomeTheaterStatus.report(theater))

    theater.watch_movie("Interstellar (2014)")

    print("=== System Status During Movie ===")
    print(HomeTheaterStatus.report(theater))

    time.sleep(0.5)
    theater.set_volume(40)
    theater.end_movie()

    theater.listen_to_music()

    print("=== Final System Status ===")
    print(HomeTheaterStatus.report(theater))
