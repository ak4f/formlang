"""Hash-consing : partage de structure (DAG) sur formlang.tree.Term. À COMPLÉTER.
-> TP arbres (E4 intern/partage, E5 round-trip, Q5 compression).

Règle « gate » : INSTANCIER formlang.tree.Term, ne pas le réécrire."""
from __future__ import annotations
from formlang.tree import Term

NodeId = int


class CompactStore:
    def __init__(self):
        self._nodes: list[tuple] = []          # id -> (symbol, label, kids_ids)
        self._table: dict[tuple, NodeId] = {}   # clé canonique -> id
        self._total = 0

    def intern(self, t: Term) -> NodeId:
        # TODO (E4) :
        #   1. interner récursivement chaque enfant -> kids_ids (tuple) ;
        #   2. incrémenter self._total ;
        #   3. clé canonique = (t.symbol, t.label, kids_ids) ;
        #   4. si déjà dans self._table -> renvoyer l'id existant,
        #      sinon créer un nouvel id (= len(self._nodes)), l'enregistrer.
        # --- DÉBUT MODIFICATION (E3.5) ---
        kids_ids = tuple(self.intern(child) for child in t.children)
        self._total += 1
        key = (t.symbol, t.label, kids_ids)
        if key in self._table:
            return self._table[key]
        nid = len(self._nodes)
        self._nodes.append(key)
        self._table[key] = nid
        return nid
        # --- FIN MODIFICATION ---

    def get(self, nid: NodeId) -> Term:
        # TODO (E5) : reconstruire l'arbre interné (round-trip exact).
        # --- DÉBUT MODIFICATION (E3.5) ---
        symbol, label, kids_ids = self._nodes[nid]
        children = tuple(self.get(kid) for kid in kids_ids)
        return Term(symbol, children, label)
        # --- FIN MODIFICATION ---

    def total_nodes(self) -> int:
        return self._total

    def unique_nodes(self) -> int:
        return len(self._nodes)

    def compression(self) -> float:
        # TODO (Q5) : 1 - uniques/total (0 si total == 0).
        # --- DÉBUT MODIFICATION (E3.5) ---
        if self._total == 0:
            return 0.0
        return 1.0 - len(self._nodes) / self._total
        # --- FIN MODIFICATION ---
