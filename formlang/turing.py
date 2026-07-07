"""Machine de Turing déterministe (ruban dict bi-infini). À COMPLÉTER : run.
-> Jour 4 (E4.1)."""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class TMResult:
    accepted: bool
    tape: str
    steps: int
    trace: list = field(default_factory=list)


@dataclass
class TuringMachine:
    transitions: dict           # (q, a) -> (q', b, d in {'L','R','S'})
    start: str
    accept: set
    blank: str = "_"
    reject: set = field(default_factory=set)

    # ----- fourni -------------------------------------------------------------
    def _read(self, tape: dict) -> str:
        if not tape:
            return ""
        lo, hi = min(tape), max(tape)
        return "".join(tape.get(i, self.blank) for i in range(lo, hi + 1)).strip(self.blank)

    def _window(self, tape: dict) -> str:
        if not tape:
            return ""
        lo, hi = min(tape), max(tape)
        return "".join(tape.get(i, self.blank) for i in range(lo, hi + 1))

    # ----- à compléter --------------------------------------------------------
    def run(self, word: str, max_steps: int = 1_000_000, trace: bool = False) -> "TMResult":
        # --- DÉBUT MODIFICATION (E4.1) ---
        tape = {i: c for i, c in enumerate(word)}
        head = 0
        state = self.start
        steps = 0
        trace_log = []

        while steps < max_steps:
            sym = tape.get(head, self.blank)
            
            if trace:
                trace_log.append((steps, state, self._window(tape), head))

            if state in self.accept:
                return TMResult(accepted=True, tape=self._read(tape), steps=steps, trace=trace_log)
            if state in self.reject:
                return TMResult(accepted=False, tape=self._read(tape), steps=steps, trace=trace_log)

            key = (state, sym)
            if key not in self.transitions:
                return TMResult(accepted=False, tape=self._read(tape), steps=steps, trace=trace_log)

            next_state, write_sym, direction = self.transitions[key]
            tape[head] = write_sym
            state = next_state

            if direction == "R":
                head += 1
            elif direction == "L":
                head -= 1
            # "S" -> reste sur place

            steps += 1

        return TMResult(accepted=False, tape=self._read(tape), steps=steps, trace=trace_log)
        # --- FIN MODIFICATION ---
