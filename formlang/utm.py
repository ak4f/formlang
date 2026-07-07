"""Machine universelle. À COMPLÉTER : encode/decode et run.  -> Jour 4 (E4.2)."""
from __future__ import annotations
import json
from .turing import TuringMachine, TMResult


def encode(machine: "TuringMachine") -> str:
    # TODO (E4.2) : linéarisation INJECTIVE de M en JSON (chaîne <M>).
    # --- DÉBUT MODIFICATION (E4.2) ---
    trans = {}
    for (q, a), (q_next, b, d) in machine.transitions.items():
        trans[f"{q},{a}"] = [q_next, b, d]
    
    data = {
        "transitions": trans,
        "start": machine.start,
        "accept": sorted(list(machine.accept)),
        "blank": machine.blank,
        "reject": sorted(list(machine.reject))
    }
    return json.dumps(data, sort_keys=True)
    # --- FIN MODIFICATION ---


def decode(desc: str) -> "TuringMachine":
    # TODO (E4.2) : reconstruire M depuis <M> (réciproque exacte de encode).
    # --- DÉBUT MODIFICATION (E4.2) ---
    data = json.loads(desc)
    trans = {}
    for key, val in data["transitions"].items():
        q, a = key.split(",", 1)
        trans[(q, a)] = (val[0], val[1], val[2])
    return TuringMachine(
        transitions=trans,
        start=data["start"],
        accept=set(data["accept"]),
        blank=data.get("blank", "_"),
        reject=set(data.get("reject", []))
    )
    # --- FIN MODIFICATION ---


class UniversalTM:
    def run(self, encoded_machine: str, word: str, **kw) -> "TMResult":
        # TODO (E4.2) : U décode <M> puis simule sur w.
        # --- DÉBUT MODIFICATION (E4.2) ---
        machine = decode(encoded_machine)
        return machine.run(word, **kw)
        # --- FIN MODIFICATION ---
