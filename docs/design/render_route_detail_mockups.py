"""Mockups de RouteDetailScreen (2 propuestas) — PNG 3x, paleta MoveUY real."""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

S = 3  # 1 dp = 3 px
W_DP, H_DP = 360, 800
W, H = W_DP * S, H_DP * S
OUT_DIR = Path(__file__).parent

# ── AppColors (lib/core/theme/app_theme.dart) ───────────────────────────────
BG = (248, 250, 252)
SURFACE = (255, 255, 255)
SURFACE_SUBTLE = (241, 245, 249)
BORDER_SUBTLE = (226, 232, 240)
BORDER_STRONG = (203, 213, 225)
TEXT = (15, 23, 42)
TEXT_2 = (71, 85, 105)
MUTED = (148, 163, 184)
PRIMARY = (242, 157, 113)
GREEN = (16, 185, 129)
AMBER = (245, 158, 11)
ALERT_RED = (197, 48, 48)
LINE_STRIPE = (165, 42, 42)
GPS_BLUE = (37, 99, 235)
WALK_SLATE = (100, 116, 139)
MAP_BG = (233, 238, 243)

FONT_DIR = Path(r"C:\Windows\Fonts")


def f(name: str, size_dp: float) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / name), int(round(size_dp * S)))


REG, SEMI, BOLD = "segoeui.ttf", "seguisb.ttf", "segoeuib.ttf"


def px(v: float) -> int:
    return int(round(v * S))


def box(x0, y0, x1, y1):
    return (px(x0), px(y0), px(x1), px(y1))


def rrect(d, x0, y0, x1, y1, r, fill=None, outline=None, w=1.0):
    d.rounded_rectangle(
        box(x0, y0, x1, y1),
        radius=px(r),
        fill=fill,
        outline=outline,
        width=max(1, px(w)),
    )


def text(d, x, y, s, font, fill, anchor="la"):
    d.text((px(x), px(y)), s, font=font, fill=fill, anchor=anchor)


def text_tracked(d, x, y, s, font, fill, tracking=1.2):
    cx = px(x)
    for ch in s:
        d.text((cx, px(y)), ch, font=font, fill=fill, anchor="la")
        cx += int(d.textlength(ch, font=font) + px(tracking))


def tw(d, s, font) -> float:
    return d.textlength(s, font=font) / S


def line(d, x0, y0, x1, y1, fill, w=1.0):
    d.line((px(x0), px(y0), px(x1), px(y1)), fill=fill, width=max(1, px(w)))


def hairline(d, x0, x1, y, fill=BORDER_SUBTLE):
    d.rectangle((px(x0), px(y), px(x1), px(y) + 1), fill=fill)


# ── Iconos ──────────────────────────────────────────────────────────────────
def icon_bus(d, cx, cy, size, color):
    """Glifo de bus (relleno) centrado en cx, cy."""
    w, h = size * 0.82, size * 0.86
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    rrect(d, x0, y0, x1, y1 - h * 0.12, size * 0.2, fill=color)
    # parabrisas / ventanas
    pad = w * 0.16
    rrect(d, x0 + pad, y0 + h * 0.18, x1 - pad, y0 + h * 0.46, size * 0.08, fill=SURFACE)
    # ruedas
    r = size * 0.11
    for ox in (-w * 0.26, w * 0.26):
        d.ellipse(
            box(cx + ox - r, y1 - h * 0.26 - r, cx + ox + r, y1 - h * 0.26 + r),
            fill=SURFACE,
        )
    # patas
    line(d, x0 + w * 0.18, y1 - h * 0.06, x0 + w * 0.18, y1, color, 1.4)
    line(d, x1 - w * 0.18, y1 - h * 0.06, x1 - w * 0.18, y1, color, 1.4)


def icon_walk(d, cx, cy, size, color):
    s = size
    hr = s * 0.13
    d.ellipse(box(cx - hr, cy - s * 0.44, cx + hr, cy - s * 0.44 + hr * 2), fill=color)
    line(d, cx - s * 0.02, cy - s * 0.16, cx + s * 0.06, cy + s * 0.06, color, 1.7)
    line(d, cx + s * 0.06, cy + s * 0.06, cx + s * 0.16, cy + s * 0.4, color, 1.7)
    line(d, cx - s * 0.02, cy - s * 0.16, cx - s * 0.18, cy + s * 0.4, color, 1.7)
    line(d, cx - s * 0.01, cy - s * 0.1, cx + s * 0.2, cy - s * 0.02, color, 1.5)
    line(d, cx - s * 0.02, cy - s * 0.12, cx - s * 0.22, cy + s * 0.02, color, 1.5)


def icon_gps(d, cx, cy, size):
    r = size / 2
    d.ellipse(box(cx - r, cy - r, cx + r, cy + r), fill=SURFACE)
    d.ellipse(box(cx - r + 1.6, cy - r + 1.6, cx + r - 1.6, cy + r - 1.6), fill=GPS_BLUE)
    rr = size * 0.16
    d.ellipse(box(cx - rr, cy - rr, cx + rr, cy + rr), fill=SURFACE)


def icon_stop(d, cx, top, size):
    """Pin de parada: placa lineStripe + validador blanco + palito."""
    w = size
    h = size * 0.86
    rrect(d, cx - w / 2, top, cx + w / 2, top + h, size * 0.26, fill=LINE_STRIPE)
    rrect(
        d,
        cx - w * 0.26,
        top + h * 0.22,
        cx + w * 0.26,
        top + h * 0.52,
        size * 0.08,
        fill=SURFACE,
    )
    d.rectangle(
        box(cx - w * 0.18, top + h * 0.63, cx + w * 0.18, top + h * 0.75), fill=SURFACE
    )
    line(d, cx, top + h, cx, top + h + size * 0.42, LINE_STRIPE, 2.2)


def icon_pin(d, cx, top, size, color):
    r = size * 0.36
    ccy = top + r
    d.ellipse(box(cx - r, ccy - r, cx + r, ccy + r), fill=color)
    d.polygon(
        [
            (px(cx - r * 0.62), px(ccy + r * 0.66)),
            (px(cx + r * 0.62), px(ccy + r * 0.66)),
            (px(cx), px(top + size)),
        ],
        fill=color,
    )
    rr = size * 0.13
    d.ellipse(box(cx - rr, ccy - rr, cx + rr, ccy + rr), fill=SURFACE)


def icon_wifi(d, cx, cy, size, color, arcs=2):
    """Glifo de señal en vivo del chip (arcos + punto)."""
    base_y = cy + size * 0.3
    for i in range(arcs):
        rad = size * (0.26 + 0.24 * (i + 1))
        d.arc(
            box(cx - rad, base_y - rad, cx + rad, base_y + rad),
            start=215,
            end=325,
            fill=color,
            width=max(1, px(1.5)),
        )
    r = size * 0.11
    d.ellipse(box(cx - r, base_y - r, cx + r, base_y + r), fill=color)


def icon_alert_tri(d, cx, cy, size, color):
    h = size * 0.86
    pts = [(cx, cy - h / 2), (cx + h * 0.56, cy + h / 2), (cx - h * 0.56, cy + h / 2)]
    d.polygon([(px(a), px(b)) for a, b in pts], outline=color, width=max(1, px(1.5)))
    line(d, cx, cy - h * 0.14, cx, cy + h * 0.12, color, 1.6)
    d.ellipse(box(cx - 0.7, cy + h * 0.26, cx + 0.7, cy + h * 0.26 + 1.4), fill=color)


def chevron(d, cx, cy, size, color, direction="down", w=1.6):
    s = size / 2
    if direction == "down":
        pts = [(cx - s, cy - s * 0.42), (cx, cy + s * 0.42), (cx + s, cy - s * 0.42)]
    elif direction == "right":
        pts = [(cx - s * 0.42, cy - s), (cx + s * 0.42, cy), (cx - s * 0.42, cy + s)]
    elif direction == "left":
        pts = [(cx + s * 0.42, cy - s), (cx - s * 0.42, cy), (cx + s * 0.42, cy + s)]
    else:
        pts = [(cx - s, cy + s * 0.42), (cx, cy - s * 0.42), (cx + s, cy + s * 0.42)]
    d.line([(px(a), px(b)) for a, b in pts], fill=color, width=max(1, px(w)), joint="curve")


def icon_nav_arrow(d, cx, cy, size, color):
    s = size / 2
    pts = [(cx, cy - s), (cx + s * 0.72, cy + s * 0.8), (cx, cy + s * 0.34), (cx - s * 0.72, cy + s * 0.8)]
    d.polygon([(px(a), px(b)) for a, b in pts], fill=color)


# ── Bloques compartidos ─────────────────────────────────────────────────────
def status_bar(d):
    d.rectangle(box(0, 0, W_DP, 30), fill=SURFACE)
    text(d, 16, 9, "12:48", f(SEMI, 11.5), TEXT)
    x = W_DP - 16
    rrect(d, x - 20, 11, x - 2, 20, 2.4, outline=TEXT, w=1.2)
    d.rectangle(box(x - 18.4, 12.6, x - 8, 18.4), fill=TEXT)
    d.rectangle(box(x - 2, 13.6, x, 17.4), fill=TEXT)
    for i, hgt in enumerate((4.0, 6.0, 8.0, 10.0)):
        bx = x - 30 - (3 - i) * 4.4
        d.rectangle(box(bx, 20 - hgt, bx + 2.8, 20), fill=TEXT)
    icon_wifi(d, x - 52, 14, 13, TEXT, arcs=2)


def app_bar(d, title, sub="Detalle"):
    d.rectangle(box(0, 30, W_DP, 92), fill=SURFACE)
    chevron(d, 24, 63, 13, TEXT, "left", w=2.0)
    text(d, 48, 40, sub, f(REG, 11.5), MUTED)
    text(d, 48, 55, title, f(BOLD, 17), TEXT)
    hairline(d, 0, W_DP, 92, BORDER_SUBTLE)


def map_strip(d, y0, y1):
    d.rectangle(box(0, y0, W_DP, y1), fill=MAP_BG)
    for gy in range(int(y0) + 14, int(y1), 26):
        line(d, 0, gy, W_DP, gy + 4, (223, 230, 238), 5)
    for gx in range(20, W_DP, 74):
        line(d, gx, y0, gx + 16, y1, (223, 230, 238), 5)
    pts = [(28, y1 - 24), (96, y1 - 40), (168, y0 + 34), (250, y0 + 26), (322, y0 + 52)]
    d.line([(px(a), px(b)) for a, b in pts], fill=SURFACE, width=px(7), joint="curve")
    d.line([(px(a), px(b)) for a, b in pts], fill=PRIMARY, width=px(4.5), joint="curve")
    icon_gps(d, 28, y1 - 24, 15)
    icon_stop(d, 168, y0 + 26, 15)
    icon_pin(d, 322, y0 + 40, 20, PRIMARY)


def line_tag(d, x, y, label, h=34, icon=16, fs=14.5):
    """BusLineTag: fondo blanco, borde, franja lineStripe abajo, bus más grande."""
    fnt = f(BOLD, fs)
    pad_l, gap, pad_r = 9, 6, 10
    w = pad_l + icon + gap + tw(d, label, fnt) + pad_r
    rrect(d, x, y, x + w, y + h, 9, fill=SURFACE, outline=BORDER_STRONG, w=1)
    icon_bus(d, x + pad_l + icon / 2, y + (h - 4) / 2, icon, TEXT_2)
    text(d, x + pad_l + icon + gap, y + (h - 4) / 2, label, fnt, TEXT, anchor="lm")
    d.rectangle(box(x + 1, y + h - 4, x + w - 1, y + h - 1), fill=LINE_STRIPE)
    return w


def eta_chip(d, x, y, value, unit=True, state="live", w=82, h=30):
    """Chip de horario: mismo diseño (fill neutro, número/ícono por estado)."""
    color = {"live": GREEN, "delay": AMBER, "detour": ALERT_RED, "sched": (100, 116, 139)}[state]
    rrect(d, x, y, x + w, y + h, 9, fill=SURFACE_SUBTLE, outline=BORDER_SUBTLE, w=1)
    fnt = f(BOLD, 14)
    fnt_u = f(REG, 10)
    iw = 15
    gap, gap2 = 4, 3
    total = iw + gap + tw(d, value, fnt) + ((gap2 + tw(d, "min", fnt_u)) if unit else 0)
    cx = x + (w - total) / 2
    cy = y + h / 2
    if state == "detour":
        icon_alert_tri(d, cx + iw / 2, cy, iw, color)
    else:
        icon_wifi(d, cx + iw / 2, cy - 1, iw, color, arcs=2 if state == "live" else 1)
    tx = cx + iw + gap
    text(d, tx, cy + 0.5, value, fnt, color, anchor="lm")
    if unit:
        text(d, tx + tw(d, value, fnt) + gap2, cy + 1.5, "min", fnt_u, TEXT_2, anchor="lm")
    return h


def chip_column(d, right_x, y, value, extra, state="live", w=82):
    x = right_x - w
    h = eta_chip(d, x, y, value, unit=True, state=state, w=w)
    if extra:
        text(d, right_x, y + h + 4, extra, f(SEMI, 11.5), GREEN, anchor="ra")
    return h + (16 if extra else 0)


def cta(d, y_top, label="Iniciar navegación"):
    d.rectangle(box(0, y_top, W_DP, H_DP), fill=BG)
    hairline(d, 0, W_DP, y_top, BORDER_SUBTLE)
    by0, by1 = y_top + 14, y_top + 14 + 52
    rrect(d, 16, by0, W_DP - 16, by1, 14, fill=TEXT)
    fnt = f(BOLD, 15)
    lw = tw(d, label, fnt)
    icon_nav_arrow(d, W_DP / 2 - lw / 2 - 13, (by0 + by1) / 2, 16, SURFACE)
    text(d, W_DP / 2 + 10, (by0 + by1) / 2 + 0.5, label, fnt, SURFACE, anchor="mm")


def section_label(d, x, y, s):
    text_tracked(d, x, y, s.upper(), f(BOLD, 10.5), MUTED, tracking=1.4)


# ── Mockup A — tarjetas por sección ─────────────────────────────────────────
def mockup_a() -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    status_bar(d)
    app_bar(d, "Punta Carretas Shopping")
    map_strip(d, 92, 170)

    # Sheet
    rrect(d, 0, 158, W_DP, H_DP, 20, fill=BG)
    rrect(d, W_DP / 2 - 18, 166, W_DP / 2 + 18, 170, 2, fill=BORDER_STRONG)

    # ── Resumen ──
    cy0, cy1 = 178, 286
    rrect(d, 14, cy0, W_DP - 14, cy1, 16, fill=SURFACE, outline=BORDER_SUBTLE, w=1)
    text(d, 28, cy0 + 16, "19 min", f(BOLD, 27), TEXT)
    text(d, 28, cy0 + 50, "Llegada 13:08", f(SEMI, 13), TEXT_2)
    pill_w = 92
    rrect(d, W_DP - 28 - pill_w, cy0 + 20, W_DP - 28, cy0 + 46, 8, fill=SURFACE_SUBTLE)
    text(d, W_DP - 28 - pill_w / 2, cy0 + 33.5, "12:50 – 13:08", f(SEMI, 11.5), TEXT_2, anchor="mm")
    hairline(d, 28, W_DP - 28, cy0 + 70, BORDER_SUBTLE)
    tag_w = line_tag(d, 28, cy0 + 82, "582 / 117 / 121", h=30, icon=15, fs=13.5)
    chevron(d, 28 + tag_w + 14, cy0 + 96, 9, MUTED, "right", w=1.6)
    icon_walk(d, 28 + tag_w + 34, cy0 + 96, 17, WALK_SLATE)
    text(d, 28 + tag_w + 46, cy0 + 96, "2 min", f(SEMI, 12.5), TEXT_2, anchor="lm")

    # ── Timeline ──
    rail_x = 32
    y = 304
    section_label(d, 16, y, "Tu viaje")
    y += 22

    # Origen
    icon_gps(d, rail_x, y + 12, 22)
    d.rectangle(box(rail_x - 2.2, y + 23, rail_x + 2.2, y + 60), fill=(160, 190, 240))
    text(d, 56, y + 4, "Tu ubicación", f(BOLD, 15), TEXT)
    text(d, 56, y + 23, "Salir a las 12:50", f(REG, 12.5), TEXT_2)
    y += 50

    # Tarjeta BUS
    card0 = y
    icon_stop(d, rail_x, y + 12, 20)
    card_x0, card_x1 = 56, W_DP - 16
    text(d, card_x0 + 14, y + 14, "San José – Zelmar Michelini", f(BOLD, 14.5), TEXT)
    text(d, card_x0 + 14, y + 33, "Parada de subida", f(REG, 11.5), MUTED)
    ly = y + 54
    for label, dest, val, extra, state in (
        ("582", "Punta Carretas", "2", "13, 19 min", "live"),
        ("121", "Punta Carretas", "5", "14, 26 min", "delay"),
    ):
        lw = line_tag(d, card_x0 + 14, ly, label, h=34, icon=17, fs=14.5)
        text(d, card_x0 + 14 + lw + 10, ly + 15, dest, f(SEMI, 12.5), TEXT_2, anchor="lm")
        chip_column(d, card_x1 - 14, ly + 1, val, extra, state=state)
        ly += 48
    text(d, card_x0 + 14, ly - 4, "Mostrar más opciones ›", f(BOLD, 12.5), GREEN)
    hairline(d, card_x0 + 14, card_x1 - 14, ly + 16, BORDER_SUBTLE)
    text(d, card_x0 + 14, ly + 27, "Viaja 16 paradas · 17 min", f(SEMI, 12.5), TEXT_2)
    chevron(d, card_x1 - 22, ly + 33, 10, MUTED, "down")
    hairline(d, card_x0 + 14, card_x1 - 14, ly + 47, BORDER_SUBTLE)
    text(d, card_x0 + 14, ly + 57, "Bajás", f(REG, 11.5), MUTED)
    text(d, card_x0 + 14, ly + 72, "Jose Ellauri y F. García Cortinas", f(BOLD, 14), TEXT)
    card1 = ly + 96
    rrect(d, card_x0, card0, card_x1, card1, 16, outline=BORDER_SUBTLE, w=1)
    d.rectangle(box(rail_x - 2.2, card0 + 22, rail_x + 2.2, card1 + 12), fill=(214, 176, 176))
    y = card1 + 12

    # Caminata
    icon_walk(d, rail_x, y + 22, 20, WALK_SLATE)
    rrect(d, 56, y, W_DP - 16, y + 46, 14, fill=SURFACE_SUBTLE)
    text(d, 70, y + 23, "Camina 145 m · 2 min", f(BOLD, 13.5), TEXT, anchor="lm")
    chevron(d, W_DP - 34, y + 23, 10, TEXT_2, "down")
    d.rectangle(box(rail_x - 2.2, y + 33, rail_x + 2.2, y + 62), fill=(190, 197, 208))
    y += 58

    # Destino
    icon_pin(d, rail_x - 1, y, 24, PRIMARY)
    text(d, 56, y + 2, "Punta Carretas Shopping", f(BOLD, 15), TEXT)

    cta(d, H_DP - 82)
    return img


# ── Mockup B — riel continuo, sin tarjetas ──────────────────────────────────
def mockup_b() -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    status_bar(d)
    app_bar(d, "Punta Carretas Shopping")

    # Encabezado de viaje (banda, sheet a tope: sin mapa)
    d.rectangle(box(0, 92, W_DP, 200), fill=SURFACE)
    text(d, 20, 104, "19 min", f(BOLD, 30), TEXT)
    text(d, 20 + tw(d, "19 min", f(BOLD, 30)) + 10, 118, "· Llegada 13:08", f(SEMI, 14), TEXT_2)
    text(d, 20, 142, "12:50 – 13:08", f(REG, 12.5), MUTED)
    tag_w = line_tag(d, 20, 162, "582 / 117 / 121", h=30, icon=15, fs=13.5)
    chevron(d, 20 + tag_w + 13, 176, 9, MUTED, "right", w=1.6)
    icon_walk(d, 20 + tag_w + 32, 176, 17, WALK_SLATE)
    text(d, 20 + tag_w + 44, 176, "2 min", f(SEMI, 12.5), TEXT_2, anchor="lm")
    hairline(d, 0, W_DP, 200, BORDER_SUBTLE)

    rail_x = 34
    lbl_x = 62
    y = 216

    # SALIDA
    section_label(d, lbl_x, y, "Salida")
    y += 18
    icon_gps(d, rail_x, y + 12, 24)
    d.rectangle(box(rail_x - 2.5, y + 24, rail_x + 2.5, y + 66), fill=(160, 190, 240))
    text(d, lbl_x, y + 3, "Tu ubicación", f(BOLD, 16), TEXT)
    text(d, lbl_x, y + 24, "Salir a las 12:50", f(REG, 13), TEXT_2)
    y += 58

    # BUS
    section_label(d, lbl_x, y, "En bus")
    y += 18
    icon_stop(d, rail_x, y + 8, 22)
    text(d, lbl_x, y + 2, "San José – Zelmar Michelini", f(BOLD, 15.5), TEXT)
    ly = y + 26
    for label, dest, val, extra, state in (
        ("582", "Punta Carretas", "2", "13, 19 min", "live"),
        ("121", "Punta Carretas", "5", "14, 26 min", "delay"),
    ):
        lw = line_tag(d, lbl_x, ly, label, h=36, icon=18, fs=15)
        text(d, lbl_x + lw + 11, ly + 16, dest, f(SEMI, 13), TEXT_2, anchor="lm")
        chip_column(d, W_DP - 18, ly + 2, val, extra, state=state)
        ly += 52
    text(d, lbl_x, ly - 6, "Mostrar más opciones ›", f(BOLD, 13), GREEN)
    rrect(d, lbl_x, ly + 14, W_DP - 18, ly + 50, 12, fill=SURFACE_SUBTLE)
    text(d, lbl_x + 14, ly + 32, "Viaja 16 paradas · 17 min", f(SEMI, 13), TEXT_2, anchor="lm")
    chevron(d, W_DP - 34, ly + 32, 10, MUTED, "down")
    d.rectangle(box(rail_x - 2.5, y + 20, rail_x + 2.5, ly + 66), fill=(214, 176, 176))
    ly += 64
    icon_stop(d, rail_x, ly - 4, 22)
    text(d, lbl_x, ly - 8, "Jose Ellauri y F. García Cortinas", f(BOLD, 15.5), TEXT)
    text(d, lbl_x, ly + 12, "Bajás acá", f(REG, 12.5), MUTED)
    y = ly + 38

    # A PIE
    section_label(d, lbl_x, y, "A pie")
    y += 18
    icon_walk(d, rail_x, y + 12, 22, WALK_SLATE)
    d.rectangle(box(rail_x - 2.5, y - 32, rail_x + 2.5, y + 2), fill=(190, 197, 208))
    d.rectangle(box(rail_x - 2.5, y + 24, rail_x + 2.5, y + 62), fill=(190, 197, 208))
    text(d, lbl_x, y + 3, "Camina 145 m", f(BOLD, 15), TEXT)
    text(d, lbl_x, y + 24, "2 min hasta el destino", f(REG, 12.5), TEXT_2)
    chevron(d, W_DP - 30, y + 16, 11, TEXT_2, "down")
    y += 56

    # LLEGADA
    section_label(d, lbl_x, y, "Llegada")
    y += 18
    icon_pin(d, rail_x - 1, y, 26, PRIMARY)
    text(d, lbl_x, y + 1, "Punta Carretas Shopping", f(BOLD, 16), TEXT)
    text(d, lbl_x, y + 22, "Llegás 13:08", f(REG, 13), TEXT_2)

    cta(d, H_DP - 82)
    return img


# ── Preview del resumen (dos columnas + divisor centrado) ───────────────────
def _summary_band(d, y0, lines, walk, start, end, strip_scale=1.0):
    """Reproduce el layout real: dos Expanded + divisor de 1 dp al centro."""
    x0, x1 = 16, W_DP - 16
    gutter, div_w = 12, 1
    half = (x1 - x0 - gutter * 2 - div_w) / 2
    div_x = x0 + half + gutter

    d.rectangle(box(0, y0, W_DP, y0 + 104), fill=SURFACE)
    text(d, x0, y0 + 16, "19 min", f(BOLD, 27), TEXT)

    # FittedBox(scaleDown): con varias líneas la tira se achica, no se corta.
    s = strip_scale
    cy = y0 + 73
    tag_w = line_tag(d, x0, cy - 15 * s, lines, h=30 * s, icon=15 * s, fs=13.5 * s)
    chevron(d, x0 + tag_w + 13 * s, cy, 9 * s, MUTED, "right", w=1.6)
    icon_walk(d, x0 + tag_w + 32 * s, cy, 17 * s, WALK_SLATE)
    text(d, x0 + tag_w + 44 * s, cy, walk, f(SEMI, 12.5 * s), TEXT_2, anchor="lm")

    d.rectangle(box(div_x, y0 + 21, div_x + div_w, y0 + 83), fill=BORDER_SUBTLE)

    cx = div_x + div_w + gutter + half / 2
    text(d, cx, y0 + 32, start, f(BOLD, 16), TEXT, anchor="mm")
    rrect(d, cx - 13, y0 + 39, cx + 13, y0 + 65, 13, fill=SURFACE_SUBTLE, outline=BORDER_SUBTLE, w=1)
    ax = cx
    line(d, ax, y0 + 45, ax, y0 + 58, TEXT_2, 1.6)
    d.polygon(
        [(px(ax - 3.4), px(y0 + 54)), (px(ax + 3.4), px(y0 + 54)), (px(ax), px(y0 + 59.5))],
        fill=TEXT_2,
    )
    text(d, cx, y0 + 72, end, f(BOLD, 16), TEXT, anchor="mm")
    hairline(d, 0, W_DP, y0 + 104, BORDER_SUBTLE)


def summary_preview() -> Image.Image:
    h_dp = 236
    img = Image.new("RGB", (W, h_dp * S), SURFACE)
    d = ImageDraw.Draw(img)
    for i, (lines, walk, start, end, scale) in enumerate(
        (
            ("121", "8", "13:48", "14:06", 1.0),
            ("21 / 64 / …", "4", "13:52", "14:08", 0.88),
        )
    ):
        y0 = 14 + i * 118
        rrect(d, W_DP / 2 - 18, y0 - 8, W_DP / 2 + 18, y0 - 4, 2, fill=BORDER_STRONG)
        _summary_band(d, y0, lines, walk, start, end, scale)
    return img


def main():
    out = OUT_DIR / "route-detail-summary.png"
    summary_preview().save(out, "PNG", optimize=True)
    print(f"wrote {out}")
    for name, fn in (("a", mockup_a), ("b", mockup_b)):
        out = OUT_DIR / f"route-detail-mockup-{name}.png"
        fn().save(out, "PNG", optimize=True)
        print(f"wrote {out}  {W}x{H}")


if __name__ == "__main__":
    main()
