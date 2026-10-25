from .base import Instance, ItemSpec, Scenario
from .phantom_done import PhantomDone, PhantomHard, PhantomStress

REGISTRY: dict[str, type[Scenario]] = {
    PhantomDone.name: PhantomDone,
    PhantomHard.name: PhantomHard,
    PhantomStress.name: PhantomStress,
}


def get_scenario(name: str) -> Scenario:
    if name.startswith("mole_") and name[5:].isdigit():
        from .mole import Mole
        return Mole(int(name[5:]))
    if name not in REGISTRY:
        raise KeyError(f"Unbekanntes Szenario {name!r}. Verfügbar: {sorted(REGISTRY)}")
    return REGISTRY[name]()


__all__ = ["Instance", "ItemSpec", "Scenario", "REGISTRY", "get_scenario"]
