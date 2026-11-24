#!/usr/bin/env python3
"""Penghitung suku kata Bahasa Indonesia dan validator tabel timing dialog VO serta urutan timestamp."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

DIPHTHONG_RE = re.compile(r"(ai|au|oi|ei)", re.IGNORECASE)
VOWEL_RE = re.compile(r"[aeiou@]")
DIGIT_RE = re.compile(r"[0-9]")
ALPHA_RE = re.compile(r"[a-z]")

DEFAULT_RATE = 5.0
MAX_EFFECTIVE_RATE = 6.0
MIN_FILL_RATIO = 0.60
MAX_FILL_RATIO = 1.05
MAX_FINAL_DURATION = 40.0
TIMESTAMP_TOLERANCE = 0.05

TABLE_HEADING_RE = re.compile(r"^##\s+Tabel\s+Timing\s+Dialog\s*$", re.IGNORECASE)


def parse_timecode(token: str) -> float:
    """Ubah format waktu MM:SS, MM:SS.s, atau detik desimal menjadi angka detik float."""
    raw = token.strip()
    if not raw:
        raise ValueError("Timecode kosong")
    if ":" in raw:
        parts = raw.split(":")
        if len(parts) != 2:
            raise ValueError(f"Format timecode tidak valid: '{token}'")
        mins = int(parts[0])
        secs = float(parts[1])
        if mins < 0 or secs < 0 or secs >= 60.0:
            raise ValueError(f"Nilai menit/detik di luar batas pada '{token}'")
        return mins * 60.0 + secs
    val = float(raw)
    if val < 0:
        raise ValueError(f"Nilai waktu negatif pada '{token}'")
    return val


def parse_timestamp_range(timestamp: str) -> tuple[float, float]:
    """Parse rentang timestamp seperti '00:00–00:03.5' menjadi tuple (mulai, selesai)."""
    cleaned = timestamp.strip().strip("`")
    parts = re.split(r"\s*[-–—]\s*", cleaned, maxsplit=1)
    if len(parts) != 2:
        raise ValueError(f"Format rentang timestamp tidak valid: '{timestamp}'")
    start_s = parse_timecode(parts[0])
    end_s = parse_timecode(parts[1])
    if end_s <= start_s:
        raise ValueError(f"Waktu selesai harus lebih besar dari mulai pada '{timestamp}'")
    return start_s, end_s


def analyze_text(text: str) -> tuple[int, list[str]]:
    """Hitung estimasi suku kata Bahasa Indonesia dan kumpulkan peringatan angka digit."""
    cleaned = text.strip().strip('"').strip("'").strip("“”")
    if not cleaned or cleaned.lower() == "[jeda]":
        return 0, []

    warnings: list[str] = []
    total_syllables = 0
    has_digits = False

    # Pisahkan kata berdasarkan spasi, tanda hubung, garis miring, dan pemisah umum.
    raw_tokens = re.split(r"[\s\-/—–]+", cleaned)
    for raw in raw_tokens:
        token = re.sub(r"[^a-zA-Z0-9]", "", raw).lower()
        if not token:
            continue

        digits = DIGIT_RE.findall(token)
        if digits:
            has_digits = True
            total_syllables += 2 * len(digits)

        letters_only = DIGIT_RE.sub("", token)
        if letters_only:
            collapsed = DIPHTHONG_RE.sub("@", letters_only)
            vowels = VOWEL_RE.findall(collapsed)
            if vowels:
                total_syllables += len(vowels)
            elif ALPHA_RE.search(letters_only):
                # Singkatan konsonan saja (mis. TV, HP, TWS) tetap dihitung berbunyi.
                total_syllables += max(1, min(len(letters_only), 3))

    if has_digits:
        warnings.append("tulis angka dengan kata")

    return total_syllables, warnings


def count_syllables(text: str) -> int:
    """Kembalikan jumlah suku kata Bahasa Indonesia untuk teks dialog."""
    syllables, _ = analyze_text(text)
    return syllables


def _parse_markdown_row(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def _is_separator_row(cells: list[str]) -> bool:
    if not cells:
        return False
    return all(bool(re.match(r"^:?-{2,}:?$", c.replace(" ", ""))) for c in cells)


def extract_timing_rows(markdown_text: str) -> tuple[bool, list[list[str]]]:
    """Cari heading '## Tabel Timing Dialog' dan ekstrak baris data tabel di bawahnya."""
    lines = markdown_text.splitlines()
    heading_idx = None
    for idx, line in enumerate(lines):
        if TABLE_HEADING_RE.match(line.strip()):
            heading_idx = idx
            break

    if heading_idx is None:
        return False, []

    table_lines: list[str] = []
    started = False
    for line in lines[heading_idx + 1 :]:
        s = line.strip()
        if not s:
            if started:
                break
            continue
        if s.startswith("|"):
            started = True
            table_lines.append(s)
        elif started:
            break
        elif s.startswith("#"):
            break

    if len(table_lines) < 3:
        return True, []

    rows: list[list[str]] = []
    header_seen = False
    for tline in table_lines:
        cells = _parse_markdown_row(tline)
        if _is_separator_row(cells):
            continue
        if not header_seen:
            header_seen = True
            continue
        rows.append(cells)

    return True, rows


def check_table(
    path: Path | str,
    rate: float = DEFAULT_RATE,
    max_total_duration: float | None = MAX_FINAL_DURATION,
    require_start_zero: bool | None = None,
    validate_timestamps: bool = True,
) -> dict:
    """Validasi '## Tabel Timing Dialog' termasuk urutan timestamp, batas durasi, dan laju dialog."""
    file_path = Path(path)
    if not file_path.is_file():
        return {
            "ok": False,
            "file": str(file_path),
            "total_duration": 0.0,
            "rows": [],
            "errors": [f"File tidak ditemukan: {file_path}"],
            "warnings": [],
        }

    if require_start_zero is None:
        require_start_zero = file_path.name.lower() == "storyboard.md"

    content = file_path.read_text(encoding="utf-8")
    found_heading, raw_rows = extract_timing_rows(content)

    if not found_heading:
        return {
            "ok": False,
            "file": str(file_path),
            "total_duration": 0.0,
            "rows": [],
            "errors": ["Heading '## Tabel Timing Dialog' tidak ditemukan"],
            "warnings": [],
        }

    if not raw_rows:
        return {
            "ok": False,
            "file": str(file_path),
            "total_duration": 0.0,
            "rows": [],
            "errors": ["Tabel timing di bawah '## Tabel Timing Dialog' kosong atau format tidak valid"],
            "warnings": [],
        }

    rows_out: list[dict] = []
    errors: list[str] = []
    warnings: list[str] = []
    total_duration = 0.0
    prev_end: float | None = None

    for idx, cells in enumerate(raw_rows, start=1):
        if len(cells) < 4:
            errors.append(f"Baris {idx}: kolom kurang dari 4 ({cells})")
            continue

        scene_label = cells[0]
        timestamp = cells[1]
        dur_str = cells[2].replace(",", ".").lower().replace("dtk", "").replace("s", "").strip()
        dialog = cells[3]

        try:
            duration = float(dur_str)
        except ValueError:
            errors.append(f"Adegan {scene_label}: durasi tidak valid ('{cells[2]}')")
            continue

        if duration <= 0:
            errors.append(f"Adegan {scene_label}: durasi harus > 0")
            continue

        start_s: float | None = None
        end_s: float | None = None
        if validate_timestamps:
            try:
                start_s, end_s = parse_timestamp_range(timestamp)
                span = end_s - start_s
                if abs(span - duration) > TIMESTAMP_TOLERANCE:
                    errors.append(
                        f"Adegan {scene_label}: rentang timestamp '{timestamp}' ({span:.2f}s) "
                        f"tidak cocok dengan durasi ({duration:.2f}s)"
                    )
                if prev_end is None:
                    if require_start_zero and abs(start_s) > TIMESTAMP_TOLERANCE:
                        errors.append(
                            f"Adegan {scene_label}: timestamp awal storyboard harus mulai dari 00:00 (ditemukan '{timestamp}')"
                        )
                else:
                    if start_s < prev_end - TIMESTAMP_TOLERANCE:
                        errors.append(
                            f"Adegan {scene_label}: timestamp tumpang-tindih (overlap) pada '{timestamp}' "
                            f"(sebelumnya selesai di {prev_end:.2f}s)"
                        )
                    elif start_s > prev_end + TIMESTAMP_TOLERANCE:
                        errors.append(
                            f"Adegan {scene_label}: terdapat celah timestamp hilang (gap) sebelum '{timestamp}' "
                            f"(sebelumnya selesai di {prev_end:.2f}s)"
                        )
                prev_end = end_s
            except ValueError as exc:
                errors.append(f"Adegan {scene_label}: {exc}")

        total_duration += duration

        is_pause = dialog.strip().strip('"').strip("'").strip("“”").lower() == "[jeda]"
        syllables, row_warnings = analyze_text(dialog)

        for w in row_warnings:
            warnings.append(f"Adegan {scene_label}: {w}")

        if is_pause:
            est = 0.0
            fill_ratio = 0.0
            eff_rate = 0.0
            status = "OK_JEDA"
        else:
            est = round(syllables / rate, 2)
            fill_ratio = est / duration
            eff_rate = syllables / duration

            if eff_rate > MAX_EFFECTIVE_RATE or fill_ratio > MAX_FILL_RATIO:
                status = "TERLALU_CEPAT"
                errors.append(
                    f"Adegan {scene_label}: dialog terlalu padat/cepat "
                    f"({syllables} suku kata dalam {duration:.1f} dtk = {eff_rate:.2f} sk/dtk, "
                    f"estimasi {est:.2f} dtk)"
                )
            elif fill_ratio < MIN_FILL_RATIO:
                status = "TERLALU_SINGKAT"
                errors.append(
                    f"Adegan {scene_label}: dialog terlalu singkat "
                    f"({est:.2f} dtk dari {duration:.1f} dtk = {fill_ratio * 100:.0f}%, minimal 60%; "
                    "tulis [jeda] jika memang hening sengaja)"
                )
            else:
                status = "OK"

        rows_out.append(
            {
                "scene": scene_label,
                "timestamp": timestamp,
                "start": start_s,
                "end": end_s,
                "duration": duration,
                "dialog": dialog,
                "syllables": syllables,
                "estimate": est,
                "fill_pct": round(fill_ratio * 100, 1),
                "effective_rate": round(eff_rate, 2),
                "status": status,
                "warnings": row_warnings,
            }
        )

    if max_total_duration is not None and total_duration > max_total_duration + 1e-6:
        errors.append(
            f"Total durasi ({total_duration:.2f} dtk) melebihi batas maksimal {max_total_duration:.1f} detik"
        )

    return {
        "ok": len(errors) == 0,
        "file": str(file_path),
        "total_duration": round(total_duration, 3),
        "rows": rows_out,
        "errors": errors,
        "warnings": warnings,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validasi timing dialog Bahasa Indonesia, urutan timestamp, dan durasi tabel Markdown."
    )
    parser.add_argument("file", help="Path file storyboard.md atau video-NN.md")
    parser.add_argument(
        "--rate",
        type=float,
        default=DEFAULT_RATE,
        help="Laju bicara dalam suku kata/detik (default: 5.0)",
    )
    parser.add_argument(
        "--max-duration",
        type=float,
        default=MAX_FINAL_DURATION,
        help="Batas maksimal total durasi tabel dalam detik (default: 40.0)",
    )
    args = parser.parse_args(argv)

    result = check_table(args.file, rate=args.rate, max_total_duration=args.max_duration)
    print(
        f"=== Audit Timing Dialog: {args.file} "
        f"(rate={args.rate} sk/dtk, total={result['total_duration']:.2f}s) ==="
    )
    for row in result["rows"]:
        print(
            f"  Adegan {row['scene']} [{row['timestamp']}] "
            f"{row['duration']:.1f}s | {row['syllables']} sk -> {row['estimate']:.2f}s "
            f"({row['fill_pct']:.0f}%, {row['effective_rate']:.2f} sk/dtk) | {row['status']}"
        )

    if result["warnings"]:
        print("\nPeringatan:")
        for w in result["warnings"]:
            print(f"  [PERINGATAN] {w}")

    if result["errors"]:
        print("\nKesalahan:")
        for e in result["errors"]:
            print(f"  [GAGAL] {e}")
        return 1

    print("\nHasil: LOLOS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
