"""
** Proxy Pattern (Interview Important)
When to use: When you need a surrogate or placeholder for another object to control access to it. Use for lazy loading (virtual proxy), access control (protection proxy), logging (logging proxy), caching (cache proxy), or synchronization.

Real-world examples:
- Django QuerySet lazy evaluation (database queries deferred until iteration)
- SQLAlchemy lazy loading (related objects loaded on access)
- ORM virtual proxies in Hibernate/NHibernate
- Image placeholders in web browsers
- API rate-limiting proxies
- Remote proxies (gRPC stubs, Java RMI)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import hashlib
import json
import os
import time


@dataclass
class ImageMetadata:
    filename: str
    width: int
    height: int
    format: str
    file_size: int
    dimensions: tuple[int, int]
    aspect_ratio: float


@dataclass
class ImageData:
    metadata: ImageMetadata
    pixels: list[list[tuple[int, int, int]]]
    loaded_at: datetime = field(default_factory=datetime.now)

    @property
    def data_size_mb(self) -> float:
        total_pixels = self.metadata.width * self.metadata.height
        return (total_pixels * 3) / (1024 * 1024)


class Image(ABC):
    @abstractmethod
    def display(self) -> str:
        pass

    @abstractmethod
    def get_metadata(self) -> Optional[ImageMetadata]:
        pass

    @abstractmethod
    def get_size_mb(self) -> float:
        pass


class HighResolutionImage(Image):
    def __init__(self, filename: str):
        self._filename = filename
        self._data: Optional[ImageData] = None

    def load_from_disk(self) -> ImageData:
        print(f"  [Disk] Loading image from {self._filename}...")
        time.sleep(0.3)

        ext = os.path.splitext(self._filename)[1].lower()
        fmt = ext.lstrip(".") if ext else "png"
        width, height = 160, 90

        import random
        rng = random.Random(hashlib.md5(self._filename.encode()).hexdigest())
        pixels = []
        for y in range(height):
            row = []
            for x in range(width):
                row.append((rng.randint(0, 255), rng.randint(0, 255), rng.randint(0, 255)))
            pixels.append(row)

        file_size = width * height * 3
        metadata = ImageMetadata(
            filename=self._filename,
            width=width,
            height=height,
            format=fmt,
            file_size=file_size,
            dimensions=(width, height),
            aspect_ratio=round(width / height, 2),
        )
        self._data = ImageData(metadata=metadata, pixels=pixels)
        print(f"  [Disk] Loaded {self._data.data_size_mb:.1f} MB image ({width}x{height})")
        return self._data

    @property
    def data(self) -> ImageData:
        if self._data is None:
            self.load_from_disk()
        result = self._data
        assert result is not None
        return result

    def display(self) -> str:
        d = self.data
        meta = d.metadata
        desc = f" [Image: {meta.filename} ({meta.width}x{meta.height}, {meta.format.upper()})]"
        row_step = max(1, meta.height // 10)
        col_step = max(1, meta.width // 80)
        for y in range(0, meta.height, row_step):
            row_pixels = d.pixels[y][::col_step][:80]
            row = "".join(
                "\033[48;2;{};{};{}m \033[0m".format(r, g, b)
                for r, g, b in row_pixels
            )
            print(row)
        print(desc)
        return desc

    def get_metadata(self) -> ImageMetadata:
        return self.data.metadata

    def get_size_mb(self) -> float:
        return self.data.data_size_mb


class ImageProxy(Image):
    def __init__(self, filename: str, access_control: Optional[dict] = None):
        self._filename = filename
        self._real_image: Optional[HighResolutionImage] = None
        self._access_control = access_control or {}
        self._access_log: list[dict] = []
        self._cache: Optional[ImageData] = None
        self._load_count = 0

    def _check_access(self, user_role: str = "anonymous") -> bool:
        allowed_roles = self._access_control.get("roles", ["admin", "user"])
        if user_role not in allowed_roles:
            print(f"  [Proxy] ACCESS DENIED for role '{user_role}' to {self._filename}")
            self._log_access("denied", user_role)
            return False
        print(f"  [Proxy] Access granted for role '{user_role}'")
        return True

    def _log_access(self, action: str, user_role: str) -> None:
        self._access_log.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "user_role": user_role,
            "filename": self._filename,
        })

    def display(self, user_role: str = "user", force_reload: bool = False) -> str:
        self._log_access("display_attempt", user_role)
        if not self._check_access(user_role):
            return "Access Denied"

        if self._cache and not force_reload:
            print(f"  [Proxy] Serving from cache: {self._filename}")
            meta = self._cache.metadata
            print(f" [Cached: {meta.filename} ({meta.width}x{meta.height})]")
            return "Displayed from cache"

        if self._real_image is None:
            self._real_image = HighResolutionImage(self._filename)
            self._load_count += 1

        self._real_image.display()
        self._cache = self._real_image._data
        return "Displayed"

    def get_metadata(self, user_role: str = "user") -> Optional[ImageMetadata]:
        if not self._check_access(user_role):
            return None
        if self._real_image is None:
            print(f"  [Proxy] Loading metadata without full image load (lazy)")
            meta = ImageMetadata(
                filename=self._filename,
                width=3840,
                height=2160,
                format=os.path.splitext(self._filename)[1].lstrip(".") or "png",
                file_size=3840 * 2160 * 3,
                dimensions=(3840, 2160),
                aspect_ratio=16 / 9,
            )
            return meta
        return self._real_image.get_metadata()

    def get_size_mb(self) -> float:
        if self._cache:
            return len(json.dumps(self._cache.pixels)) / (1024 * 1024)
        return 0.0

    @property
    def load_count(self) -> int:
        return self._load_count

    @property
    def access_log(self) -> list[dict]:
        return list(self._access_log)

    def clear_cache(self) -> None:
        self._cache = None
        print(f"  [Proxy] Cache cleared for {self._filename}")

    def invalidate(self) -> None:
        self._cache = None
        self._real_image = None
        print(f"  [Proxy] Image invalidated, will reload on next access")


class ImageGallery:
    def __init__(self):
        self._images: dict[str, ImageProxy] = {}
        self._current_user_role: str = "user"

    def add_image(self, filename: str, allowed_roles: Optional[list[str]] = None) -> None:
        access_control = {"roles": allowed_roles or ["admin", "user"]}
        self._images[filename] = ImageProxy(filename, access_control)

    def set_user_role(self, role: str) -> None:
        self._current_user_role = role
        print(f"\n[Gallery] User role set to '{role}'")

    def view(self, filename: str, force_reload: bool = False) -> None:
        proxy = self._images.get(filename)
        if not proxy:
            print(f"[Gallery] Image '{filename}' not found")
            return
        print(f"\n--- Viewing: {filename} ---")
        result = proxy.display(self._current_user_role, force_reload)
        print(f"  Result: {result}")

    def show_gallery(self) -> None:
        print(f"\n{'='*60}")
        print(f"  Image Gallery ({len(self._images)} images)")
        print(f"{'='*60}")
        for name in self._images:
            meta = self._images[name].get_metadata(self._current_user_role)
            if meta:
                print(f"  {name:40s} {meta.width}x{meta.height}  {meta.format.upper()}")

    def show_access_log(self) -> None:
        print(f"\n--- Access Log ---")
        for entry in self._access_logs():
            print(f"  [{entry['timestamp']}] {entry['action']} by '{entry['user_role']}' - {entry['filename']}")

    def _access_logs(self) -> list[dict]:
        logs = []
        for proxy in self._images.values():
            logs.extend(proxy.access_log)
        return sorted(logs, key=lambda x: x["timestamp"])


def demo_gallery():
    gallery = ImageGallery()
    gallery.add_image("vacation_beach.png", ["admin", "user"])
    gallery.add_image("family_reunion.jpg", ["admin", "user"])
    gallery.add_image("confidential_report.png", ["admin"])
    gallery.add_image("product_banner.png", ["admin", "user"])
    gallery.add_image("server_credentials.png", ["admin"])

    gallery.show_gallery()

    gallery.set_user_role("user")
    gallery.view("vacation_beach.png")
    gallery.view("confidential_report.png")
    gallery.view("vacation_beach.png")

    gallery.set_user_role("admin")
    gallery.view("confidential_report.png")
    gallery.view("server_credentials.png")

    gallery.set_user_role("user")
    gallery.view("server_credentials.png")

    print(f"\n=== Load Statistics ===")
    for name, proxy in gallery._images.items():
        print(f"  {name}: loaded {proxy.load_count} time(s)")

    gallery.show_access_log()


if __name__ == "__main__":
    print("=" * 60)
    print("  Proxy Pattern: Image Gallery with Lazy Loading & Access Control")
    print("=" * 60)
    demo_gallery()

