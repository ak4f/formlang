"""AFD. À COMPLÉTER : run, accepts, minimize (Moore).  -> Jour 1 (E1.1, E1.2)."""
from __future__ import annotations
from dataclasses import dataclass, field
from collections import deque


@dataclass
class DFA:
    transitions: dict            # (state, sym) -> state
    start: str
    accept: set
    alphabet: set = field(default_factory=set)

    def __post_init__(self):
        if not self.alphabet:
            self.alphabet = {a for (_, a) in self.transitions}

    def run(self, w: str):
        # TODO (E1.1) : partir de self.start, suivre self.transitions lettre par
        # lettre ; renvoyer None si une transition manque, sinon l'état atteint.
        # --- DÉBUT MODIFICATION (E1.1) ---
        state = self.start
        for char in w:
            state = self.transitions.get((state, char))
            if state is None:
                return None
        return state
        # --- FIN MODIFICATION ---

    def accepts(self, w: str) -> bool:
        # TODO (E1.1) : True ssi run(w) in self.accept.
        # --- DÉBUT MODIFICATION (E1.1) ---
        state = self.run(w)
        return state in self.accept
        # --- FIN MODIFICATION ---

    # ----- fourni : utilitaires pour la minimisation --------------------------
    def _reachable(self) -> set:
        seen, todo = {self.start}, deque([self.start])
        while todo:
            s = todo.popleft()
            for a in self.alphabet:
                t = self.transitions.get((s, a))
                if t is not None and t not in seen:
                    seen.add(t)
                    todo.append(t)
        return seen

    def _completed(self):
        SINK = "__sink__"
        trans = dict(self.transitions)
        states = self._reachable()
        need = False
        for s in states:
            for a in self.alphabet:
                if (s, a) not in trans:
                    trans[(s, a)] = SINK
                    need = True
        if need:
            states = states | {SINK}
            for a in self.alphabet:
                trans[(SINK, a)] = SINK
        return states, trans

    def minimize(self) -> "DFA":
        # TODO (E1.2) : raffinement de partition (Moore).
        # --- DÉBUT MODIFICATION (E1.2) ---
        states, trans = self._completed()
        
        accepting = states & self.accept
        non_accepting = states - self.accept
        
        partition = []
        if non_accepting: partition.append(frozenset(non_accepting))
        if accepting: partition.append(frozenset(accepting))
            
        def get_block_index(state, part):
            for i, block in enumerate(part):
                if state in block:
                    return i
            return -1

        changed = True
        while changed:
            changed = False
            new_partition = []
            
            for block in partition:
                behavior_groups = {}
                for s in block:
                    behavior = tuple(get_block_index(trans[(s, a)], partition) for a in sorted(self.alphabet))
                    if behavior not in behavior_groups:
                        behavior_groups[behavior] = set()
                    behavior_groups[behavior].add(s)
                
                for group in behavior_groups.values():
                    new_partition.append(frozenset(group))
                    
                if len(behavior_groups) > 1:
                    changed = True
                    
            partition = new_partition
            
        new_transitions = {}
        new_start = None
        new_accept = set()
        
        def block_name(block):
            return "{" + ",".join(sorted(str(s) for s in block)) + "}"
            
        block_by_state = {}
        for block in partition:
            name = block_name(block)
            for s in block:
                block_by_state[s] = name
                
        for block in partition:
            name = block_name(block)
            rep = next(iter(block))
            if rep in self.accept:
                new_accept.add(name)
            if self.start in block:
                new_start = name
            
            for a in self.alphabet:
                target = trans[(rep, a)]
                new_transitions[(name, a)] = block_by_state[target]
                
        return DFA(
            transitions=new_transitions,
            start=new_start,
            accept=new_accept,
            alphabet=self.alphabet
        )
        # --- FIN MODIFICATION ---

    def num_states(self) -> int:
        st = {self.start}
        for (s, _), t in self.transitions.items():
            st.add(s)
            st.add(t)
        return len(st)
