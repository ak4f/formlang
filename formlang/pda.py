"""Automate à pile (acceptation pile vide). À COMPLÉTER.  -> Jour 2 (E2.1)."""
from __future__ import annotations


class DelimiterPDA:
    def __init__(self, pairs=(("[", "]"), ("(", ")")), ignore=("a", "o", "r", "e")):
        self.open = {o for o, _ in pairs}
        self.match = {c: o for o, c in pairs}     # fermant -> ouvrant attendu
        self.ignore = set(ignore)

    def accepts(self, w: str) -> bool:
        # TODO (E2.1) : avec une pile (list).
        # --- DÉBUT MODIFICATION (E2.1) ---
        stack = []
        for c in w:
            if c in self.open:
                stack.append(c)          # délimiteur ouvrant → empiler
            elif c in self.match:
                # délimiteur fermant → vérifier que le sommet correspond
                if not stack or stack[-1] != self.match[c]:
                    return False          # mal imbriqué ou pile vide → rejet
                stack.pop()              # sommet correct → dépiler
            elif c not in self.ignore:
                return False             # caractère non reconnu → rejet
        return len(stack) == 0           # accepté ssi pile vide (tout fermé)
        # --- FIN MODIFICATION ---
