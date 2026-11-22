import math
import struct
import zlib
from io import BytesIO
from itertools import pairwise

from app.schemas.foundation_design import FoundationContext

_FONT = {
    " ": (0, 0, 0, 0, 0), "+": (8, 8, 62, 8, 8), "-": (8, 8, 8, 8, 8),
    ".": (0, 96, 96, 0, 0), "=": (20, 20, 20, 20, 20),
    "0": (62, 81, 73, 69, 62), "1": (0, 66, 127, 64, 0), "2": (98, 81, 73, 73, 70),
    "3": (34, 65, 73, 73, 54), "4": (24, 20, 18, 127, 16), "5": (39, 69, 69, 69, 57),
    "6": (60, 74, 73, 73, 48), "7": (1, 113, 9, 5, 3), "8": (54, 73, 73, 73, 54), "9": (6, 73, 73, 41, 30),
    "A": (126, 17, 17, 17, 126), "B": (127, 73, 73, 73, 54), "C": (62, 65, 65, 65, 34),
    "D": (127, 65, 65, 34, 28), "E": (127, 73, 73, 73, 65), "F": (127, 9, 9, 9, 1),
    "G": (62, 65, 73, 73, 122), "H": (127, 8, 8, 8, 127), "I": (0, 65, 127, 65, 0),
    "K": (127, 8, 20, 34, 65), "L": (127, 64, 64, 64, 64), "M": (127, 2, 12, 2, 127),
    "N": (127, 4, 8, 16, 127), "O": (62, 65, 65, 65, 62), "P": (127, 9, 9, 9, 6),
    "Q": (62, 65, 81, 33, 94), "R": (127, 9, 25, 41, 70), "S": (38, 73, 73, 73, 50),
    "T": (1, 1, 127, 1, 1), "U": (63, 64, 64, 64, 63), "V": (31, 32, 64, 32, 31),
    "W": (63, 64, 56, 64, 63), "X": (99, 20, 8, 20, 99), "Y": (7, 8, 112, 8, 7),
}


class _Drawing:
    def __init__(self, width: int = 720, height: int = 300) -> None:
        self.width, self.height = width, height
        self.rows = [bytearray([255] * width) for _ in range(height)]

    def line(self, start: tuple[float, float], end: tuple[float, float], shade: int = 30) -> None:
        x0, y0 = start
        x1, y1 = end
        length = max(1, int(max(abs(x1 - x0), abs(y1 - y0))))
        for step in range(length + 1):
            x = round(x0 + (x1 - x0) * step / length)
            y = round(y0 + (y1 - y0) * step / length)
            if 0 <= x < self.width and 0 <= y < self.height:
                self.rows[y][x] = shade

    def arrow(self, start: tuple[float, float], end: tuple[float, float]) -> None:
        self.line(start, end)
        angle = math.atan2(end[1] - start[1], end[0] - start[0])
        for delta in (-0.5, 0.5):
            self.line(end, (end[0] - 10 * math.cos(angle + delta), end[1] - 10 * math.sin(angle + delta)))

    def text(self, x: int, y: int, value: str) -> None:
        for index, char in enumerate(value.upper()):
            for column, mask in enumerate(_FONT[char]):
                for row in range(7):
                    if mask & (1 << row):
                        for dx in range(2):
                            for dy in range(2):
                                self.rows[y + row * 2 + dy][x + index * 12 + column * 2 + dx] = 30

    def png(self) -> BytesIO:
        def chunk(kind: bytes, payload: bytes) -> bytes:
            return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload))
        raw = b"".join(b"\0" + row for row in self.rows)
        return BytesIO(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", self.width, self.height, 8, 0, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


def foundation_figure(context: FoundationContext) -> BytesIO:
    drawing = _Drawing()
    drawing.text(20, 12, "LOADS")
    drawing.text(430, 12, "PRESSURE KPA")
    drawing.text(350, 32, "DIAGNOSTIC" if context.pressure_state == "diagnostic" else "FULL CONTACT" if context.pressure_state == "full_contact" else "UNAVAILABLE")
    drawing.text(45, 155, "H")
    drawing.text(145, 250, "B")
    drawing.line((15, 245), (295, 245))
    drawing.line((65, 215), (245, 215))
    drawing.line((65, 215), (65, 245))
    drawing.line((245, 215), (245, 245))
    drawing.line((125, 110), (125, 215))
    drawing.line((185, 110), (185, 215))
    drawing.line((125, 110), (185, 110))
    drawing.line((75, 110), (110, 110), 180)
    drawing.arrow((80, 118), (80, 207))
    drawing.arrow((80, 207), (80, 118))
    n = context.inputs["N"].value
    drawing.text(170, 35, "N")
    if n != 0:
        drawing.arrow((155, 35 if n > 0 else 105), (155, 105 if n > 0 else 35))
    qx, qy = context.inputs["Qx"].value, context.inputs["Qy"].value
    drawing.text(245, 90, "QX")
    drawing.text(215, 42, "QY")
    if qx != 0:
        drawing.arrow((155, 110), (155 + math.copysign(85, qx), 110))
    if qy != 0:
        direction = math.copysign(1, qy)
        drawing.arrow((155, 110), (155 + direction * 55, 110 - direction * 40))
    drawing.text(75, 45, "MX")
    drawing.text(190, 85, "MY")
    for name, cx in (("Mx", 120), ("My", 190)):
        moment = context.inputs[name].value
        if moment != 0:
            direction = math.copysign(1, moment)
            for index in range(25):
                a, b = direction * index * math.pi / 25, direction * (index + 1) * math.pi / 25
                drawing.line((cx + 20 * math.cos(a), 65 + 16 * math.sin(a)), (cx + 20 * math.cos(b), 65 + 16 * math.sin(b)))
            drawing.arrow((cx - 16, 65 + direction * 10), (cx - 20, 65))
    if context.corners:
        b, l = context.geometry["b"].value, context.geometry["l"].value
        scale = 140 / max(b, l)
        drawing.text(650, 245, "X=B")
        drawing.text(645, 180, "Y=L")
        drawing.arrow((660, 220), (690, 229))
        drawing.arrow((660, 220), (678, 206))
        amplitude = max(abs(corner.pressure.value) for corner in context.corners)
        base: dict[str, tuple[float, float]] = {}
        tips: dict[str, tuple[float, float]] = {}
        for corner in context.corners:
            x = 525 + (corner.x.value + 0.6 * corner.y.value) * scale
            y = 160 + (0.3 * corner.x.value - 0.45 * corner.y.value) * scale
            height = 0 if amplitude == 0 else 85 * corner.pressure.value / amplitude
            base[corner.name] = (x, y)
            tips[corner.name] = (x, y - height)
            drawing.line(base[corner.name], tips[corner.name])
            label = f"{corner.name} {corner.pressure.value:+.5G}"
            label_x = max(330, min(int(x) - 35, 715 - len(label) * 12))
            label_y = max(32, min(260, round(y - height) - 18))
            drawing.text(label_x, label_y, label)
        drawing.text(330, 280, f"MIN {context.trace_values['p_corner_min'].value:+.5G} MAX {context.trace_values['p_corner_max'].value:+.5G}")
        order = ("pp", "pm", "mm", "mp", "pp")
        for first, second in pairwise(order):
            drawing.line(base[first], base[second], 170)
            drawing.line(tips[first], tips[second])
    return drawing.png()
