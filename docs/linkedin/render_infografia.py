"""Infografía LinkedIn MoveUY — paleta carbón / naranja cálido / oliva / marfil."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 2160, 3240
OUT = Path(__file__).with_name("moveuy-api-infografia.png")

# Paleta editorial
CARBON = (13, 13, 12)
CARBON_2 = (22, 22, 20)
CARBON_3 = (32, 31, 28)
IVORY = (244, 239, 228)
IVORY_DIM = (196, 188, 170)
IVORY_MUTE = (140, 133, 118)
ORANGE = (201, 106, 58)
ORANGE_SOFT = (201, 106, 58, 40)
OLIVE = (90, 107, 72)
OLIVE_LIGHT = (138, 148, 112)
RED = (184, 54, 48)
RED_LIGHT = (214, 118, 110)

FONT_DIR = Path(r"C:\Windows\Fonts")


def fnt(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / name), size)


# Editorial: Georgia para titulares, Segoe para UI, Cascadia para código
T_KICKER = fnt("georgia.ttf", 22)
T_BRAND = fnt("georgiab.ttf", 26)
T_TITLE = fnt("georgiab.ttf", 68)
T_H = fnt("georgiab.ttf", 34)
T_BODY = fnt("segoeui.ttf", 28)
T_BODY_B = fnt("segoeuib.ttf", 28)
T_SM = fnt("segoeui.ttf", 24)
T_SM_B = fnt("segoeuib.ttf", 22)
T_TINY = fnt("segoeui.ttf", 20)
T_CODE = fnt("CascadiaMono.ttf", 26)
T_ITAL = fnt("georgiai.ttf", 26)


def tw(draw, s, font):
    return draw.textbbox((0, 0), s, font=font)[2]


def hairline(draw, x0, y, x1, color=CARBON_3, w=1):
    draw.line((x0, y, x1, y), fill=color, width=w)


def rule_accent(draw, x, y, length=72):
    draw.line((x, y, x + length, y), fill=ORANGE, width=3)


def panel(draw, xy, fill=CARBON_2):
    draw.rectangle(xy, fill=fill)
    # marco 1px marfil muy bajo
    draw.rectangle(xy, outline=(48, 46, 42), width=1)


def main():
    img = Image.new("RGB", (W, H), CARBON)
    d = ImageDraw.Draw(img)
    m = 96

    # Franja naranja izquierda (póster)
    d.rectangle((0, 0, 10, H), fill=ORANGE)

    # ── Header ──────────────────────────────────────────────
    d.text((m, 72), "MOVEUY  ·  MONTEVIDEO", font=T_BRAND, fill=ORANGE)
    d.text((m, 128), "API de transporte público", font=T_TITLE, fill=IVORY)
    d.text(
        (m, 218),
        "GPS de flota  ·  GTFS  ·  OpenTripPlanner 2  ·  OpenAPI 3",
        font=T_ITAL,
        fill=IVORY_DIM,
    )
    d.text((m, 268), "api.moveuy.com/docs", font=T_SM, fill=IVORY_MUTE)
    hairline(d, m, 330, W - m, (48, 46, 42), 1)
    rule_accent(d, m, 330)

    # ── 01 Arquitectura ─────────────────────────────────────
    y = 380
    d.text((m, y), "01", font=T_SM_B, fill=ORANGE)
    d.text((m + 70, y - 4), "Arquitectura", font=T_H, fill=IVORY)
    y = 450

    col_gap = 24
    col_w = (W - 2 * m - 2 * col_gap) // 3
    sources = [
        ("01", "IMM GPS", "Flota en vivo. Velocidad,\nposición y timestamp."),
        ("02", "GTFS", "Shapes, paradas y atraso\nfirmado contra el horario."),
        ("03", "OTP2", "Plan A→B y horarios\nprogramados de relleno."),
    ]
    for i, (num, title, sub) in enumerate(sources):
        x = m + i * (col_w + col_gap)
        panel(d, (x, y, x + col_w, y + 188))
        d.text((x + 32, y + 28), num, font=T_SM_B, fill=ORANGE)
        d.text((x + 32, y + 64), title, font=T_BODY_B, fill=IVORY)
        for j, line in enumerate(sub.split("\n")):
            d.text((x + 32, y + 110 + j * 30), line, font=T_SM, fill=IVORY_DIM)

    # Conector
    y2 = y + 188
    mid = W // 2
    d.line((mid, y2, mid, y2 + 36), fill=ORANGE, width=2)
    d.polygon([(mid - 8, y2 + 28), (mid + 8, y2 + 28), (mid, y2 + 44)], fill=ORANGE)

    y = y2 + 52
    panel(d, (m, y, W - m, y + 248))
    d.rectangle((m, y, m + 8, y + 248), fill=ORANGE)
    d.text((m + 40, y + 28), "api.moveuy.com", font=T_BODY_B, fill=IVORY)
    d.text((m + 320, y + 32), "inferAlert  →  AlertSmoother", font=T_SM, fill=ORANGE)
    lines = [
        "Sin GPS o señal vieja: no se evalúa.  Fuera de la shape (> 150 m): DETOUR — corta primero.",
        "DELAYED solo con embotellamiento: < 8 km/h  ·  > 120 m de parada  ·  atraso GTFS > 120 s.",
        "Histéresis 2 polls para activar, 3 para bajar.  Flutter no recalcula: solo pinta alertType.",
    ]
    for i, line in enumerate(lines):
        d.text((m + 40, y + 90 + i * 44), line, font=T_SM, fill=IVORY_DIM)

    y = y + 248 + 28
    d.line((mid, y - 28, mid, y), fill=ORANGE, width=2)
    d.polygon([(mid - 8, y - 8), (mid + 8, y - 8), (mid, y + 8)], fill=ORANGE)
    panel(d, (m + 360, y + 12, W - m - 360, y + 88))
    d.text((m + 400, y + 32), "App Flutter   ·   color e ícono según  alertType", font=T_BODY, fill=IVORY)

    # ── 02 Alertas ──────────────────────────────────────────
    y = y + 140
    hairline(d, m, y, W - m, (48, 46, 42), 1)
    rule_accent(d, m, y)
    y += 40
    d.text((m, y), "02", font=T_SM_B, fill=ORANGE)
    d.text((m + 70, y - 4), "Qué pinta cada alerta", font=T_H, fill=IVORY)
    y += 70

    cards = [
        (OLIVE, OLIVE_LIGHT, "GOOD_SERVICE", "En servicio",
         "En ruta, sin tapón ni desvío.\nUn bus tarde a velocidad\nnormal se queda aquí."),
        (ORANGE, (224, 164, 122), "DELAYED", "Tráfico",
         "Embotellamiento real.\nLento, lejos de parada\ny perdiendo tiempo vs GTFS."),
        (RED, RED_LIGHT, "DETOUR", "Desvío",
         "Fuera de la shape (> 150 m).\nPrioridad máxima: no se\nevalúa tráfico."),
    ]
    for i, (accent, label_c, code, ui, desc) in enumerate(cards):
        x = m + i * (col_w + col_gap)
        panel(d, (x, y, x + col_w, y + 292))
        d.rectangle((x, y, x + col_w, y + 6), fill=accent)
        d.text((x + 32, y + 32), code, font=T_SM_B, fill=accent)
        d.text((x + 32, y + 72), ui, font=T_H, fill=IVORY)
        for j, line in enumerate(desc.split("\n")):
            d.text((x + 32, y + 140 + j * 34), line, font=T_SM, fill=IVORY_DIM)

    y += 320
    d.text(
        (m, y),
        "Un atraso de línea no muestra tráfico: esa demora ya está en los minutos de ETA.",
        font=T_ITAL,
        fill=IVORY_DIM,
    )

    # ── 03 JSON ─────────────────────────────────────────────
    y += 70
    hairline(d, m, y, W - m, (48, 46, 42), 1)
    rule_accent(d, m, y)
    y += 40
    d.text((m, y), "03", font=T_SM_B, fill=ORANGE)
    d.text((m + 70, y - 4), "Respuesta  ·  POST  /api/eta", font=T_H, fill=IVORY)
    y += 64

    json_h = 560
    panel(d, (m, y, W - m, y + json_h), CARBON_2)
    d.text((m + 40, y + 24), "200   JSON    parada 4771  ·  Juncal y Sarandí", font=T_TINY, fill=IVORY_MUTE)

    rows = [
        ("{", IVORY_MUTE),
        ('  "4771": {', IVORY_DIM),
        ('    "false": [{', IVORY_MUTE),
        ('      "linea": "183",            "destino": "POCITOS",', IVORY),
        ('      "minutos": 6,              "horaDesc": "6 min",', IVORY),
        ('      "real": true,              "source": "fleet-seg",', IVORY),
        ('      "realtimeState": "UPDATED",', OLIVE_LIGHT),
        ('      "alertType": "GOOD_SERVICE",', OLIVE_LIGHT),
        ('      "desvio": false,           "delay": 12,', IVORY_DIM),
        ('      "gpsAccuracy": "HIGH"', IVORY_DIM),
        ("    }]", IVORY_MUTE),
        ("  }", IVORY_DIM),
        ("}", IVORY_MUTE),
    ]
    ty = y + 72
    for line, color in rows:
        d.text((m + 44, ty), line, font=T_CODE, fill=color)
        ty += 36

    y = y + json_h + 36
    d.text(
        (m, y),
        "Flutter lee alertType.  Un delay alto sin DELAYED no es tráfico.",
        font=T_ITAL,
        fill=IVORY_DIM,
    )

    hairline(d, m, H - 88, W - m, (48, 46, 42), 1)
    d.text((m, H - 64), "MOVEUY", font=T_BRAND, fill=ORANGE)
    d.text((m + 180, H - 62), "api.moveuy.com/docs", font=T_SM, fill=IVORY_MUTE)

    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT}  {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
