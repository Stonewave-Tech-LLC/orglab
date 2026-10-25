"""Verblindete Auswertung (Regel 20, D-021): Die Arme heißen bis zum Einfrieren der Auswertung nur A, B, C, …

  python -m orglab.verblindung verblinden E-xxx --feld effort --arme low medium high none [--weg completion_tokens raw cost_usd]
  python -m orglab.verblindung entblinden E-xxx

Ablauf:
  1. `verblinden` würfelt eine Zuordnung Arm → Buchstabe, legt den Schlüssel AUSSERHALB des Repos ab (SCHLUESSEL_DIR),
     schreibt nur dessen SHA-256 ins Repo (`experimente/<E>/verblindung.sha256`, ein Commitment) und erzeugt eine
     verblindete Kopie der Rohdaten (`daten/<E>/verblindet/`). Felder, die den Arm verraten können (z. B. Token-Zahlen,
     Rohtext), werden entfernt.
  2. Ausgewertet wird nur die verblindete Kopie. Die Auswertung mit allen Entscheidungen kommt nach
     `experimente/<E>/auswertung-verblindet.md` und wird committet.
  3. `entblinden` öffnet den Schlüssel erst, wenn diese Datei committet und unverändert ist, und prüft den Hash.

Schutzziel: unbewusstes Biegen der Auswertung und versehentliches Sehen, nicht absichtliches Nachschauen (der Schlüssel
liegt auf demselben Rechner). Für eine harte Sperre siehe Sandbox-Prüfung in notizen/32.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import string
import subprocess
import sys
from pathlib import Path

from .runner import ROOT

SCHLUESSEL_DIR = Path.home() / ".orglab-schluessel"    # außerhalb des Repos und der üblichen Suchpfade
NULL_ARM = "none"                                         # Name für den Wert null (z. B. Parameter weggelassen)


def _key_bytes(mapping: dict[str, str], salt: str) -> bytes:
    return json.dumps({"mapping": mapping, "salt": salt}, sort_keys=True, ensure_ascii=False).encode("utf-8")


def make_key(arms: list[str], rng: random.Random | None = None) -> tuple[dict[str, str], str]:
    rng = rng or random.SystemRandom()
    letters = list(string.ascii_uppercase[:len(arms)])
    rng.shuffle(letters)
    salt = "".join(rng.choice("0123456789abcdef") for _ in range(32))   # verhindert Raten über die Hash-Werte
    return dict(zip(arms, letters)), salt


def blind_rows(rows: list[dict], field: str, mapping: dict[str, str], drop: list[str]) -> list[dict]:
    out = []
    for r in rows:
        r = {k: v for k, v in r.items() if k not in drop}
        arm = NULL_ARM if r.get(field) is None else str(r[field])
        if arm not in mapping:
            raise ValueError(f"Unbekannter Arm {arm!r} im Feld {field!r}")
        r[field] = mapping[arm]
        out.append(r)
    return out


def verblinden(exp: str, field: str, arms: list[str], drop: list[str], key_dir: Path = SCHLUESSEL_DIR,
               root: Path = ROOT, rng: random.Random | None = None) -> Path:
    data, expdir = root / "daten" / exp, root / "experimente" / exp
    key_file = key_dir / f"{exp}.json"
    if key_file.exists():
        raise FileExistsError(f"Schlüssel für {exp} existiert schon ({key_file}); nie neu würfeln")
    mapping, salt = make_key(arms, rng)
    key_dir.mkdir(parents=True, exist_ok=True)
    key_file.write_bytes(_key_bytes(mapping, salt))
    expdir.mkdir(parents=True, exist_ok=True)
    (expdir / "verblindung.sha256").write_text(
        hashlib.sha256(_key_bytes(mapping, salt)).hexdigest() + f"  {exp}.json\n"
        f"# Feld: {field} · Arme: {', '.join(arms)} · entfernt: {', '.join(drop) or '-'}\n", encoding="utf-8")
    out = data / "verblindet"
    out.mkdir(parents=True, exist_ok=True)
    for src in sorted(data.glob("*.jsonl")):
        rows = [json.loads(l) for l in src.read_text(encoding="utf-8").splitlines() if l.strip()]
        if rows and field in rows[0]:
            (out / src.name).write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in blind_rows(rows, field, mapping, drop)),
                                        encoding="utf-8")
    return out


def _committed_unchanged(path: Path, root: Path) -> bool:
    rel = path.relative_to(root).as_posix()
    tracked = subprocess.run(["git", "ls-files", "--error-unmatch", rel], cwd=root, capture_output=True).returncode == 0
    clean = subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=root).returncode == 0
    return tracked and clean


def entblinden(exp: str, key_dir: Path = SCHLUESSEL_DIR, root: Path = ROOT, gate=_committed_unchanged) -> dict[str, str]:
    expdir = root / "experimente" / exp
    frozen = expdir / "auswertung-verblindet.md"
    if not frozen.exists() or not gate(frozen, root):
        raise PermissionError(f"Erst {frozen.relative_to(root).as_posix()} schreiben und committen, dann entblinden")
    raw = (key_dir / f"{exp}.json").read_bytes()
    expected = (expdir / "verblindung.sha256").read_text(encoding="utf-8").split()[0]
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError("Schlüssel passt nicht zum vorher committeten Hash: manipuliert oder vertauscht")
    mapping = json.loads(raw)["mapping"]
    (expdir / "entblindung.md").write_text(
        "# Entblindung\n\n| Buchstabe | Arm |\n|---|---|\n"
        + "\n".join(f"| {b} | {a} |" for a, b in sorted(mapping.items(), key=lambda x: x[1]))
        + f"\n\nHash geprüft: {expected}\n", encoding="utf-8")
    return mapping


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser()
    p.add_argument("cmd", choices=["verblinden", "entblinden"])
    p.add_argument("experiment")
    p.add_argument("--feld", default="effort")
    p.add_argument("--arme", nargs="+")
    p.add_argument("--weg", nargs="*", default=[])
    a = p.parse_args()
    if a.cmd == "verblinden":
        out = verblinden(a.experiment, a.feld, a.arme, a.weg)
        print(f"Verblindete Kopie: {out.relative_to(ROOT).as_posix()} · Schlüssel liegt außerhalb des Repos, nur der Hash ist im Repo")
    else:
        print(entblinden(a.experiment))


if __name__ == "__main__":
    main()
