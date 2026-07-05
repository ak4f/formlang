"""Grammaire hors-contexte : génération bornée. À COMPLÉTER.  -> Jour 2 (E2.2)."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class CFG:
    rules: dict
    start: str
    nonterminals: set

    def generate(self, max_len: int) -> set:
        # TODO (E2.2) : énumérer les mots TERMINAUX dérivables de longueur <= max_len.
        # --- DÉBUT MODIFICATION (E2.2) ---
        results = set()
        queue = [(self.start,)]
        visited = set()

        while queue:
            form = queue.pop(0)
            if form in visited:
                continue
            visited.add(form)

            terminals = [s for s in form if s not in self.nonterminals]
            nonterminals = [s for s in form if s in self.nonterminals]

            # Élagage si trop de terminaux
            if len(terminals) > max_len:
                continue

            # Élagage si trop de non-terminaux (évite boucle infinie avec S -> SS)
            if len(nonterminals) > max_len:
                continue

            if not nonterminals:
                # Tous les symboles sont des terminaux
                word = "".join(form)
                if len(word) <= max_len:
                    results.add(word)
                continue

            # Dérivation la plus à gauche
            for i, s in enumerate(form):
                if s in self.nonterminals:
                    for rhs in self.rules.get(s, []):
                        new_form = form[:i] + rhs + form[i+1:]
                        if new_form not in visited:
                            queue.append(new_form)
                    break
        return results
        # --- FIN MODIFICATION ---


def balanced_cfg() -> "CFG":
    # FOURNI : S -> S S | [ S ] | ( S ) | a | o | r | eps
    return CFG(
        rules={"S": [("S", "S"), ("[", "S", "]"), ("(", "S", ")"),
                     ("a",), ("o",), ("r",), ()]},
        start="S", nonterminals={"S"},
    )
