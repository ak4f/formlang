"""Automate d'arbres ascendant (BUTA) générique. À COMPLÉTER : run, accepts,
product.  -> Jour 3 (E3.1, E3.4)."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Hashable


@dataclass(frozen=True)
class Term:
    symbol: str
    children: tuple["Term", ...] = ()
    label: Optional[str] = None


class _Reject:
    __slots__ = ()
    def __repr__(self):
        return "REJECT"


REJECT = _Reject()


class TreeAutomaton:
    def __init__(self, final_states):
        self.delta: dict[tuple[str, tuple], Hashable] = {}
        self.final: set = set(final_states)

    def add_rule(self, symbol: str, child_states, result) -> None:
        # FOURNI
        self.delta[(symbol, tuple(child_states))] = result

    def run(self, t: "Term"):
        # TODO (E3.1) : étiquetage POST-ORDRE (feuilles -> racine).
        # --- DÉBUT MODIFICATION (E3.1) ---
        child_states = []
        for child in t.children:
            state = self.run(child)
            if state is REJECT:
                return REJECT
            child_states.append(state)
        
        key = (t.symbol, tuple(child_states))
        return self.delta.get(key, REJECT)
        # --- FIN MODIFICATION ---

    def accepts(self, t: "Term") -> bool:
        # TODO (E3.1) : True ssi run(t) in self.final.
        # --- DÉBUT MODIFICATION (E3.1) ---
        res = self.run(t)
        return res is not REJECT and res in self.final
        # --- FIN MODIFICATION ---


def product(a1: "TreeAutomaton", a2: "TreeAutomaton") -> "TreeAutomaton":
    # TODO (E3.4) : automate produit, L = L(a1) inter L(a2).
    # --- DÉBUT MODIFICATION (E3.4) ---
    final_states = {(f1, f2) for f1 in a1.final for f2 in a2.final}
    p = TreeAutomaton(final_states)
    
    for (sym1, child_states1), res1 in a1.delta.items():
        for (sym2, child_states2), res2 in a2.delta.items():
            if sym1 == sym2 and len(child_states1) == len(child_states2):
                paired_child_states = tuple(zip(child_states1, child_states2))
                p.add_rule(sym1, paired_child_states, (res1, res2))
                
    return p
    # --- FIN MODIFICATION ---
