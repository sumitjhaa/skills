"""Protocol dunder methods — container, numeric, math protocols."""
import math

class Playlist:
    def __init__(self, songs):
        self._songs = songs
    def __contains__(self, song):
        return song in self._songs
    def __len__(self):
        return len(self._songs)
    def __getitem__(self, i):
        return self._songs[i]
    def __setitem__(self, i, v):
        self._songs[i] = v
    def __delitem__(self, i):
        del self._songs[i]
    def __reversed__(self):
        return Playlist(list(reversed(self._songs)))
    def __bool__(self):
        return len(self._songs) > 0

class Vector2D:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __int__(self):
        return int(math.sqrt(self.x**2 + self.y**2))
    def __float__(self):
        return math.sqrt(self.x**2 + self.y**2)
    def __round__(self, ndigits=0):
        return Vector2D(round(self.x, ndigits), round(self.y, ndigits))
    def __bool__(self):
        return self.x != 0 or self.y != 0
    def __format__(self, fmt):
        if fmt == "polar":
            r = math.hypot(self.x, self.y)
            θ = math.degrees(math.atan2(self.y, self.x))
            return f"({r:.1f}∠{θ:.1f}°)"
        return f"({self.x}, {self.y})"

pl = Playlist(["A", "B"])
print(f"len: {len(pl)}, 'A': {'A' in pl}")
pl[0] = "X"
print(f"reversed: {list(reversed(pl))}")
v = Vector2D(3, 4)
print(f"int: {int(v)}, float: {float(v):.1f}, polar: {v:polar}")
print(f"bool: {bool(v)}, zero: {bool(Vector2D(0,0))}")
