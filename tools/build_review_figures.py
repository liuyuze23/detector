from __future__ import annotations

import csv
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageOps


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "output" / "review" / "figure_catalog.tsv"
OUT = ROOT / "output" / "review" / "figures"


FIGURE_GROUPS = [
    (
        "fig01_xdi_module.png",
        ["F01", "F02"],
        "XDi/EDXRD CdZnTe module route",
    ),
    (
        "fig02_coded_aperture.png",
        ["F03", "F28"],
        "Coded-aperture and coherent-scatter XRD route",
    ),
    (
        "fig03_redlen_stability.png",
        ["F05", "F31"],
        "Near-room-temperature Redlen HF-CdZnTe stability",
    ),
    (
        "fig04_hexitec_mhz.png",
        ["F06", "F07", "F29"],
        "High-flux CdZnTe baseline and leakage-current effects",
    ),
    (
        "fig05_czt_polarization_contacts.png",
        ["F08", "F09", "F30"],
        "CdZnTe high-flux polarization and contact engineering",
    ),
    (
        "fig06_cdte_mechanism.png",
        ["F17", "F18", "F19", "F20"],
        "CdTe Schottky temperature-dependent polarization mechanism",
    ),
    (
        "fig07_cdte_stability.png",
        ["F22", "F23", "F26", "F32"],
        "CdTe continuous-illumination stability and bias history",
    ),
]


CROP_FRACTIONS = {
    "F01": (0.04, 0.08, 0.96, 0.58),
    "F02": (0.04, 0.05, 0.96, 0.88),
    "F03": (0.05, 0.04, 0.95, 0.46),
    "F05": (0.14, 0.06, 0.86, 0.64),
    "F06": (0.08, 0.04, 0.92, 0.56),
    "F07": (0.08, 0.03, 0.92, 0.58),
    "F08": (0.05, 0.04, 0.95, 0.60),
    "F09": (0.05, 0.04, 0.95, 0.62),
    "F17": (0.05, 0.04, 0.95, 0.58),
    "F18": (0.05, 0.04, 0.95, 0.64),
    "F19": (0.05, 0.04, 0.95, 0.62),
    "F20": (0.07, 0.69, 0.50, 0.97),
    "F22": (0.05, 0.04, 0.95, 0.62),
    "F23": (0.10, 0.04, 0.90, 0.43),
    "F26": (0.05, 0.41, 0.95, 0.97),
    "F28": (0.12, 0.61, 0.49, 0.77),
    "F29": (0.05, 0.04, 0.95, 0.58),
    "F30": (0.13, 0.46, 0.90, 0.73),
    "F31": (0.05, 0.04, 0.95, 0.62),
    "F32": (0.49, 0.06, 0.95, 0.66),
}


def read_catalog() -> dict[str, dict[str, str]]:
    with CATALOG.open(newline="", encoding="utf-8") as fh:
        return {row["figure_id"]: row for row in csv.DictReader(fh, delimiter="\t")}


def trim_whitespace(image: Image.Image) -> Image.Image:
    rgb = image.convert("RGB")
    bg = Image.new("RGB", rgb.size, (255, 255, 255))
    diff = ImageChops.difference(rgb, bg)
    diff = ImageOps.grayscale(diff)
    diff = diff.point(lambda p: 255 if p > 18 else 0)
    bbox = diff.getbbox()
    if not bbox:
        return rgb
    left, upper, right, lower = bbox
    pad = 18
    left = max(0, left - pad)
    upper = max(0, upper - pad)
    right = min(rgb.width, right + pad)
    lower = min(rgb.height, lower + pad)
    return rgb.crop((left, upper, right, lower))


def crop_relevant_region(fig_id: str, image: Image.Image) -> Image.Image:
    box = CROP_FRACTIONS.get(fig_id)
    if not box:
        return trim_whitespace(image)
    w, h = image.size
    left, upper, right, lower = box
    cropped = image.crop((int(left * w), int(upper * h), int(right * w), int(lower * h)))
    return trim_whitespace(cropped)


def fit_into(image: Image.Image, box_width: int, box_height: int) -> Image.Image:
    fitted = image.copy()
    fitted.thumbnail((box_width, box_height), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (box_width, box_height), "white")
    x = (box_width - fitted.width) // 2
    y = (box_height - fitted.height) // 2
    canvas.paste(fitted, (x, y))
    return canvas


def panel_label(draw: ImageDraw.ImageDraw, label: str, xy: tuple[int, int]) -> None:
    x, y = xy
    draw.rectangle((x, y, x + 84, y + 34), fill="white", outline=(30, 30, 30), width=2)
    draw.text((x + 12, y + 7), label, fill=(0, 0, 0))


def compose_group(catalog: dict[str, dict[str, str]], ids: list[str], title: str) -> Image.Image:
    panels = []
    for fig_id in ids:
        src = ROOT / catalog[fig_id]["image_file"]
        panel = crop_relevant_region(fig_id, Image.open(src))
        panels.append((fig_id, panel))

    columns = 2 if len(panels) != 3 else 3
    rows = (len(panels) + columns - 1) // columns
    panel_w = 1050 if columns == 2 else 760
    panel_h = 760
    margin = 44
    gutter = 26
    title_h = 58
    width = columns * panel_w + (columns - 1) * gutter + 2 * margin
    height = rows * panel_h + (rows - 1) * gutter + 2 * margin + title_h

    canvas = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(canvas)
    draw.text((margin, 18), title, fill=(0, 0, 0))

    for idx, (fig_id, panel) in enumerate(panels):
        row = idx // columns
        col = idx % columns
        x = margin + col * (panel_w + gutter)
        y = margin + title_h + row * (panel_h + gutter)
        fitted = fit_into(panel, panel_w, panel_h)
        canvas.paste(fitted, (x, y))
        draw.rectangle((x, y, x + panel_w, y + panel_h), outline=(210, 210, 210), width=2)
        panel_label(draw, fig_id, (x + 12, y + 12))

    return canvas


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    catalog = read_catalog()
    for filename, ids, title in FIGURE_GROUPS:
        image = compose_group(catalog, ids, title)
        image.save(OUT / filename, optimize=True)
        print(OUT / filename)


if __name__ == "__main__":
    main()
