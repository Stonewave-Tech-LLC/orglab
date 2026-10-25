"""Verhindert Ruhezustand, solange ein Experimentprozess läuft (Windows: SetThreadExecutionState).

Ändert keine Systemeinstellungen; die Anforderung endet automatisch mit dem Prozess.
"""

from __future__ import annotations

import sys

ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001


def hold() -> bool:
    if sys.platform != "win32":
        return False
    import ctypes
    return bool(ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED))
