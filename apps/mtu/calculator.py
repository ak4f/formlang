"""Calculatrice unaire. À COMPLÉTER.  -> Jour 4 (E4.3)."""
from .machines import ADD, SUB


def _ones(s: str) -> int:
    return s.count("1")


class Calculatrice:
    def addition(self, n: int, m: int) -> int:
        # TODO (E4.3)
        # --- DÉBUT MODIFICATION (E4.3) ---
        word = "1" * n + "+" + "1" * m
        res = ADD.run(word)
        return _ones(res.tape)
        # --- FIN MODIFICATION ---

    def soustraction(self, n: int, m: int) -> int:   # tronquée à 0
        # TODO (E4.3)
        # --- DÉBUT MODIFICATION (E4.3) ---
        word = "1" * n + "-" + "1" * m
        res = SUB.run(word)
        return _ones(res.tape)
        # --- FIN MODIFICATION ---

    def multiplication(self, n: int, m: int) -> int:
        # TODO (E4.3)
        # --- DÉBUT MODIFICATION (E4.3) ---
        res = 0
        for _ in range(m):
            res = self.addition(res, n)
        return res
        # --- FIN MODIFICATION ---

    def division(self, n: int, m: int):              # -> (quotient, reste)
        # TODO (E4.3)
        # --- DÉBUT MODIFICATION (E4.3) ---
        if m == 0:
            raise ZeroDivisionError("Division par zéro")
        q = 0
        r = n
        while r >= m:
            r = self.soustraction(r, m)
            q = self.addition(q, 1)
        return q, r
        # --- FIN MODIFICATION ---

    def chainer(self, v0: int, ops: list) -> int:
        # TODO (E4.3)
        # --- DÉBUT MODIFICATION (E4.3) ---
        val = v0
        for op, arg in ops:
            if op == "+":
                val = self.addition(val, arg)
            elif op == "-":
                val = self.soustraction(val, arg)
            elif op == "*":
                val = self.multiplication(val, arg)
            elif op == "/":
                val, _ = self.division(val, arg)
        return val
        # --- FIN MODIFICATION ---
