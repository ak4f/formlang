"""AFN (eps = ''). À COMPLÉTER : to_dfa par sous-ensembles.  -> Jour 1 (E1.3)."""
from __future__ import annotations
from dataclasses import dataclass, field
from .dfa import DFA


@dataclass
class NFA:
    transitions: dict            # (state, sym|'') -> set(states)
    start: str
    accept: set
    alphabet: set = field(default_factory=set)

    def __post_init__(self):
        if not self.alphabet:
            self.alphabet = {a for (_, a) in self.transitions if a != ""}

    # ----- fourni -------------------------------------------------------------
    def _eps_closure(self, states: frozenset) -> frozenset:
        stack, clos = list(states), set(states)
        while stack:
            s = stack.pop()
            for t in self.transitions.get((s, ""), ()):
                if t not in clos:
                    clos.add(t)
                    stack.append(t)
        return frozenset(clos)

    def _move(self, states: frozenset, a: str) -> frozenset:
        out = set()
        for s in states:
            out |= self.transitions.get((s, a), set())
        return frozenset(out)

    def accepts(self, w: str) -> bool:
        cur = self._eps_closure(frozenset({self.start}))
        for c in w:
            cur = self._eps_closure(self._move(cur, c))
        return any(s in self.accept for s in cur)

    # ----- à compléter --------------------------------------------------------
    def to_dfa(self) -> DFA:
        # TODO (E1.3) : construction des sous-ensembles.
        # --- DÉBUT MODIFICATION (E1.3) ---
        # 1. État initial du DFA = ε-fermeture de l'état initial de l'AFN
        start_set = self._eps_closure(frozenset({self.start}))

        dfa_trans = {}
        dfa_accept = set()
        todo = [start_set]
        visited = {start_set}

        # 2. BFS : explorer tous les états-ensembles atteignables
        while todo:
            current = todo.pop()
            # Si l'ensemble contient un état acceptant de l'AFN → acceptant dans le DFA
            if any(s in self.accept for s in current):
                dfa_accept.add(current)
            # Pour chaque lettre, calculer l'ensemble d'états suivants
            for a in self.alphabet:
                next_set = self._eps_closure(self._move(current, a))
                if not next_set:
                    continue  # ensemble vide → pas de transition
                dfa_trans[(current, a)] = next_set
                if next_set not in visited:
                    visited.add(next_set)
                    todo.append(next_set)

        return DFA(dfa_trans, start_set, dfa_accept, set(self.alphabet))
        # --- FIN MODIFICATION ---
