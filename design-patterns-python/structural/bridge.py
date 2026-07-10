"""
Bridge Pattern
When to use: When you want to decouple an abstraction from its implementation so they can vary independently. Use when you need to avoid a permanent binding between an abstraction and its implementation, or when both the abstractions and implementations should be extensible via subclassing.

Real-world examples:
- Cross-platform GUI frameworks (Windows/Linux/macOS window rendering)
- Device driver architecture (OS abstraction over hardware)
- Database connectivity drivers (JDBC/ODBC)
- UI widget themes (widget + theme combinations)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class DeviceState(Enum):
    OFF = auto()
    ON = auto()
    STANDBY = auto()


@dataclass
class DeviceInfo:
    name: str
    device_type: str
    state: DeviceState
    volume: int
    channel: int
    brightness: Optional[int] = None
    input_source: Optional[str] = None
    temperature: Optional[int] = None


class Device(ABC):
    def __init__(self):
        self._state = DeviceState.OFF
        self._volume = 50
        self._channel = 1

    @abstractmethod
    def power_on(self) -> bool:
        pass

    @abstractmethod
    def power_off(self) -> bool:
        pass

    @abstractmethod
    def set_volume(self, percent: int) -> None:
        pass

    @abstractmethod
    def set_channel(self, channel: int) -> None:
        pass

    @abstractmethod
    def get_info(self) -> DeviceInfo:
        pass


class TV(Device):
    def __init__(self, name: str = "Samsung QLED 4K"):
        super().__init__()
        self._name = name
        self._brightness = 70
        self._input_source = "HDMI 1"

    def power_on(self) -> bool:
        if self._state == DeviceState.OFF:
            self._state = DeviceState.ON
            print(f"  {self._name}: Powering on...")
            return True
        return False

    def power_off(self) -> bool:
        if self._state == DeviceState.ON:
            self._state = DeviceState.OFF
            print(f"  {self._name}: Powering off...")
            return True
        return False

    def set_volume(self, percent: int) -> None:
        self._volume = max(0, min(100, percent))
        print(f"  {self._name}: Volume set to {self._volume}%")

    def set_channel(self, channel: int) -> None:
        self._channel = max(1, channel)
        print(f"  {self._name}: Channel changed to {self._channel}")

    def set_brightness(self, level: int) -> None:
        self._brightness = max(0, min(100, level))
        print(f"  {self._name}: Brightness set to {self._brightness}%")

    def get_info(self) -> DeviceInfo:
        return DeviceInfo(
            name=self._name,
            device_type="TV",
            state=self._state,
            volume=self._volume,
            channel=self._channel,
            brightness=self._brightness,
            input_source=self._input_source,
        )


class Radio(Device):
    def __init__(self, name: str = "Sony Portable Radio"):
        super().__init__()
        self._name = name
        self._frequency = 98.5
        self._band = "FM"

    def power_on(self) -> bool:
        if self._state == DeviceState.OFF:
            self._state = DeviceState.ON
            print(f"  {self._name}: Turning on the radio...")
            return True
        return False

    def power_off(self) -> bool:
        if self._state == DeviceState.ON:
            self._state = DeviceState.OFF
            print(f"  {self._name}: Turning off the radio...")
            return True
        return False

    def set_volume(self, percent: int) -> None:
        self._volume = max(0, min(100, percent))
        print(f"  {self._name}: Volume set to {self._volume}%")

    def set_channel(self, channel: int) -> None:
        self._channel = max(1, channel)
        self._frequency = 87.5 + (channel - 1) * 0.5
        print(f"  {self._name}: Tuned to {self._frequency:.1f} {self._band} (channel {self._channel})")

    def get_info(self) -> DeviceInfo:
        return DeviceInfo(
            name=self._name,
            device_type="Radio",
            state=self._state,
            volume=self._volume,
            channel=self._channel,
        )


class Projector(Device):
    def __init__(self, name: str = "Epson Home Cinema 4K"):
        super().__init__()
        self._name = name
        self._brightness = 80
        self._lamp_hours = 1200
        self._aspect_ratio = "16:9"

    def power_on(self) -> bool:
        if self._state == DeviceState.OFF:
            self._state = DeviceState.ON
            print(f"  {self._name}: Lamp warming up...")
            return True
        return False

    def power_off(self) -> bool:
        if self._state == DeviceState.ON:
            self._state = DeviceState.STANDBY
            print(f"  {self._name}: Cooling fan active, entering standby...")
            return True
        return False

    def set_volume(self, percent: int) -> None:
        self._volume = max(0, min(100, percent))
        print(f"  {self._name}: Built-in speaker volume set to {self._volume}%")

    def set_channel(self, channel: int) -> None:
        self._channel = max(1, channel)
        print(f"  {self._name}: Input source switched to port {self._channel}")

    def get_info(self) -> DeviceInfo:
        return DeviceInfo(
            name=self._name,
            device_type="Projector",
            state=self._state,
            volume=self._volume,
            channel=self._channel,
            brightness=self._brightness,
        )


class Remote(ABC):
    def __init__(self, device: Device):
        self._device = device

    def toggle_power(self) -> None:
        info = self._device.get_info()
        if info.state == DeviceState.OFF:
            self._device.power_on()
        else:
            self._device.power_off()

    def volume_up(self) -> None:
        info = self._device.get_info()
        self._device.set_volume(info.volume + 10)

    def volume_down(self) -> None:
        info = self._device.get_info()
        self._device.set_volume(info.volume - 10)

    def channel_up(self) -> None:
        info = self._device.get_info()
        self._device.set_channel(info.channel + 1)

    def channel_down(self) -> None:
        info = self._device.get_info()
        self._device.set_channel(info.channel - 1)

    @abstractmethod
    def show_status(self) -> None:
        pass


class BasicRemote(Remote):
    def show_status(self) -> None:
        info = self._device.get_info()
        state_name = info.state.name.title()
        print(f"[BasicRemote] {info.name} ({info.device_type}): {state_name} | Vol: {info.volume} | Ch: {info.channel}")


class AdvancedRemote(Remote):
    def mute(self) -> None:
        self._device.set_volume(0)
        print("  Device muted.")

    def set_favorite_channel(self, channel: int) -> None:
        self._device.set_channel(channel)
        print(f"  Favorite channel {channel} set.")

    def show_status(self) -> None:
        info = self._device.get_info()
        state_name = info.state.name.title()
        extras = []
        if info.brightness is not None:
            extras.append(f"Brightness: {info.brightness}%")
        if info.input_source:
            extras.append(f"Input: {info.input_source}")
        extra_str = f" | {' | '.join(extras)}" if extras else ""
        print(f"[AdvancedRemote] {info.name} ({info.device_type}): {state_name} | Vol: {info.volume} | Ch: {info.channel}{extra_str}")


if __name__ == "__main__":
    tv = TV("LG OLED 65\"")
    radio = Radio("Bose Wave")
    projector = Projector("BenQ 4K HDR")

    basic = BasicRemote(tv)
    advanced_tv = AdvancedRemote(tv)
    advanced_radio = AdvancedRemote(radio)
    advanced_projector = AdvancedRemote(projector)

    print("=== TV with BasicRemote ===")
    basic.toggle_power()
    basic.volume_up()
    basic.channel_up()
    basic.show_status()
    basic.toggle_power()

    print("\n=== TV with AdvancedRemote ===")
    advanced_tv.toggle_power()
    advanced_tv.set_favorite_channel(42)
    advanced_tv.volume_down()
    advanced_tv.mute()
    advanced_tv.show_status()
    advanced_tv.toggle_power()

    print("\n=== Radio with AdvancedRemote ===")
    advanced_radio.toggle_power()
    advanced_radio.channel_up()
    advanced_radio.channel_up()
    advanced_radio.volume_up()
    advanced_radio.show_status()
    advanced_radio.toggle_power()

    print("\n=== Projector with AdvancedRemote ===")
    advanced_projector.toggle_power()
    advanced_projector.channel_up()
    advanced_projector.volume_up()
    advanced_projector.show_status()
    advanced_projector.toggle_power()
