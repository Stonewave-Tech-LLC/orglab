"""OpenRouter-Anbindung (Fremdmodelle, Decision Models) mit hartem Budget-Schutz.

- Der Key wird aus `.env` bzw. der Umgebung gelesen (OPENROUTER_API_KEY) und nie ausgegeben oder geloggt.
- Jeder kostenpflichtige Aufruf landet im Ledger `daten/openrouter_ledger.jsonl` (Zeit, Modell, Tokens, Kosten).
- Bevor ein Aufruf rausgeht, wird das Tagesbudget geprüft (OPENROUTER_DAILY_BUDGET_USD, Standard 50 $, gleich Neos Key-Limit bei OpenRouter).
  Ist es erreicht, wird der Aufruf verweigert. Zusätzlich gilt Neos Limit am Key bei OpenRouter.
- Nur Standardbibliothek (urllib), keine zusätzliche Abhängigkeit.
"""

from __future__ import annotations

import json
import os
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "daten" / "openrouter_ledger.jsonl"
BASE = "https://openrouter.ai/api/v1"
_LEDGER_LOCK = threading.Lock()   # mehrere Threads schreiben/lesen das Ledger gleichzeitig


class BudgetExceeded(RuntimeError):
    pass


def _load_env() -> None:
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def _key() -> str:
    _load_env()
    key = os.environ.get("OPENROUTER_API_KEY", "")
    if not key:
        raise RuntimeError("OPENROUTER_API_KEY fehlt (.env im Projektordner)")
    return key


def daily_budget() -> float:
    _load_env()
    return float(os.environ.get("OPENROUTER_DAILY_BUDGET_USD", "50"))


def spent_today() -> float:
    if not LEDGER.exists():
        return 0.0
    today = time.strftime("%Y-%m-%d")
    total = 0.0
    with _LEDGER_LOCK:
        lines = LEDGER.read_text(encoding="utf-8").splitlines()
    for line in lines:
        try:
            e = json.loads(line)
        except json.JSONDecodeError:   # halbe oder leere Zeile (E-016 brach daran ab)
            continue
        if e.get("date") == today:
            total += float(e.get("cost_usd") or 0.0)
    return total


def _request(method: str, path: str, body: dict[str, Any] | None = None, timeout: float = 120) -> dict[str, Any]:
    req = urllib.request.Request(BASE + path, method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Authorization": f"Bearer {_key()}", "Content-Type": "application/json",
                                          "X-Title": "orglab research"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read().decode()
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            raise RuntimeError(f"OpenRouter: keine gültige JSON-Antwort ({raw[:120]!r})") from None
    except urllib.error.HTTPError as e:
        # Fehlertext ohne Header ausgeben, damit der Key nie in Logs landet
        raise RuntimeError(f"OpenRouter HTTP {e.code}: {e.read().decode(errors='replace')[:300]}") from None


def key_info() -> dict[str, Any]:
    """Kostenloser Check: Ist der Key gültig, welches Limit und welcher Verbrauch? (ohne den Key selbst)"""
    data = _request("GET", "/key").get("data", {})
    return {k: data.get(k) for k in ("label", "limit", "limit_remaining", "usage", "usage_daily", "is_free_tier")}


def models() -> list[dict[str, Any]]:
    return _request("GET", "/models").get("data", [])


def chat(model: str, messages: list[dict[str, Any]], max_tokens: int = 512, purpose: str = "",
         estimate_usd: float = 0.05, **extra: Any) -> dict[str, Any]:
    """Ein Chat-Aufruf mit Budget-Prüfung und Ledger-Eintrag. `estimate_usd` ist die Obergrenze, die vorab
    gegen das Restbudget geprüft wird (konservativ)."""
    budget, spent = daily_budget(), spent_today()
    if spent + estimate_usd > budget:
        raise BudgetExceeded(f"Tagesbudget {budget:.2f} $ erreicht (verbraucht {spent:.2f} $)")
    t0 = time.time()
    resp = _request("POST", "/chat/completions", {"model": model, "messages": messages, "max_tokens": max_tokens,
                                                   "usage": {"include": True}, **extra})
    usage = resp.get("usage") or {}
    entry = {"date": time.strftime("%Y-%m-%d"), "t": time.strftime("%H:%M:%S"), "model": model, "purpose": purpose,
             "prompt_tokens": usage.get("prompt_tokens"), "completion_tokens": usage.get("completion_tokens"),
             "cost_usd": usage.get("cost"), "latency_s": round(time.time() - t0, 2)}
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with _LEDGER_LOCK, open(LEDGER, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")
    return resp
