"""Opérations comme VRAIES machines de Turing. À COMPLÉTER : tables ADD, SUB.
-> Jour 4 (E4.3)."""
from formlang.turing import TuringMachine

ADD = TuringMachine(
    transitions={
        # --- DÉBUT MODIFICATION (E4.3) ---
        ("q0", "1"): ("q0", "1", "R"),
        ("q0", "+"): ("q1", "1", "R"),
        ("q1", "1"): ("q1", "1", "R"),
        ("q1", "_"): ("q2", "_", "L"),
        ("q2", "1"): ("qf", "_", "S"),
        # --- FIN MODIFICATION ---
    },
    start="q0", accept={"qf"},
)

SUB = TuringMachine(
    transitions={
        # --- DÉBUT MODIFICATION (E4.3) ---
        ("q0", "1"): ("q0", "1", "R"),
        ("q0", "X"): ("q0", "X", "R"),
        ("q0", "-"): ("q1", "-", "R"),
        
        ("q1", "X"): ("q1", "X", "R"),
        ("q1", "1"): ("q2", "X", "L"),
        ("q1", "_"): ("q3", "_", "L"),
        
        ("q2", "X"): ("q2", "X", "L"),
        ("q2", "-"): ("q2", "-", "L"),
        ("q2", "1"): ("q0", "X", "R"),
        ("q2", "_"): ("q4", "_", "R"),
        
        ("q3", "X"): ("q3", "_", "L"),
        ("q3", "-"): ("q3", "_", "L"),
        ("q3", "1"): ("q3", "1", "L"),
        ("q3", "_"): ("qf", "_", "S"),
        
        ("q4", "1"): ("q4", "_", "R"),
        ("q4", "X"): ("q4", "_", "R"),
        ("q4", "-"): ("q4", "_", "R"),
        ("q4", "_"): ("qf", "_", "S"),
        # --- FIN MODIFICATION ---
    },
    start="q0", accept={"qf"},
)
