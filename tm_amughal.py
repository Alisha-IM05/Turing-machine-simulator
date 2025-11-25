#!/usr/bin/env python3
"""
k-tape Turing Machine simulator (Project 3-style).

Usage:
    python tm_netid.py <machine_file> <tape_file>

Implements:
- Arbitrary k tapes.
- Max tape length / max steps from machine file.
- '*' wildcard in read pattern (LHS) and write pattern (RHS).
- Directions L, R, S (stay).
- Grouped tape-file input (k lines per problem).
- CSV-like output trace plus final status/tapes.
"""

import csv
import sys

BLANK = '_'  # underscore stands for blank


class TuringMachine:
    def __init__(
        self,
        name,
        k,
        max_tape_len,
        max_steps,
        sigma,
        states,
        start_state,
        accept_state,
        reject_state,
        gammas,
        transitions,
    ):
        self.name = name
        self.k = k
        self.max_tape_len = max_tape_len
        self.max_steps = max_steps
        self.sigma = sigma
        self.states = states
        self.start_state = start_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.gammas = gammas
        self.transitions = transitions


def parse_csv_line(line: str):
    """Parse a comma-separated line and trim whitespace around each field."""
    reader = csv.reader([line.rstrip("\r\n")])
    for row in reader:
        return [field.strip() for field in row]
    return []


def load_machine(filename: str) -> TuringMachine:
    """Load a TM from a machine description file."""
    with open(filename, 'r', newline='') as f:
        raw_lines = [ln for ln in f.readlines() if ln.strip() != '']

    # Header
    header = parse_csv_line(raw_lines[0])
    name = header[0]
    k = int(header[1])
    max_tape_len = int(header[2])
    max_steps = int(header[3])

    # Σ
    sigma = set(parse_csv_line(raw_lines[1]))

    # States
    states = set(parse_csv_line(raw_lines[2]))

    # Start
    start_state = parse_csv_line(raw_lines[3])[0]

    # Accept, Reject
    accrej = parse_csv_line(raw_lines[4])
    accept_state = accrej[0]
    reject_state = accrej[1]

    # Γ_i
    gammas = []
    for i in range(k):
        gamma = set(parse_csv_line(raw_lines[5 + i]))
        gamma.add(BLANK)
        gammas.append(gamma)

    # Transitions
    transitions = {}
    rule_num = 0
    for line in raw_lines[5 + k:]:
        fields = parse_csv_line(line)
        if not fields:
            continue

        expected = 2 + 3 * k
        if len(fields) != expected:
            raise ValueError("Incorrect number of fields in transition.")

        init_state = fields[0]
        read_syms = tuple(fields[1:1 + k])
        new_state = fields[1 + k]
        write_syms = tuple(fields[2 + k:2 + 2 * k])
        dirs = tuple(fields[2 + 2 * k:2 + 3 * k])

        rule_num += 1
        print(f"{rule_num}: {line.strip()}")

        trans = {
            "rule_num": rule_num,
            "init_state": init_state,
            "read": read_syms,
            "new_state": new_state,
            "write": write_syms,
            "dirs": dirs,
        }
        transitions.setdefault(init_state, []).append(trans)

    return TuringMachine(
        name, k, max_tape_len, max_steps, sigma, states,
        start_state, accept_state, reject_state, gammas, transitions
    )


def pattern_matches(pattern, symbols):
    """Return True if pattern matches current tape symbols (supports * wildcard)."""
    for p, s in zip(pattern, symbols):
        if p != '*' and p != s:
            return False
    return True


def find_transition(tm, state, symbols):
    """Return the first matching transition in file order."""
    rules = tm.transitions.get(state)
    if not rules:
        return None
    for t in rules:
        if pattern_matches(t["read"], symbols):
            return t
    return None


def init_tapes(tm, init_strings):
    """Initialize k tapes with input strings padded with blanks."""
    tapes = []
    heads = [0] * tm.k

    for i in range(tm.k):
        s = init_strings[i]
        if len(s) > tm.max_tape_len:
            s = s[:tm.max_tape_len]

        tape = list(s) + [BLANK] * (tm.max_tape_len - len(s))
        tapes.append(tape)

    return tapes, heads


def tape_to_str(tape):
    return ''.join(tape).rstrip(BLANK)


def run_problem(tm, init_strings, problem_idx):
    tapes, heads = init_tapes(tm, init_strings)
    state = tm.start_state
    step = 0
    status = None

    print(f"\nProblem {problem_idx}")
    for i in range(tm.k):
        print(f"Tape {i+1}: {tape_to_str(tapes[i])}")

    while True:
        if state == tm.accept_state:
            status = "Accepted"
            break
        if state == tm.reject_state:
            status = "Rejected"
            break

        if step >= tm.max_steps:
            print("Error: exceeded maximum step count")
            status = "Error"
            break

        current_syms = tuple(tapes[i][heads[i]] for i in range(tm.k))

        # Validate
        for i, sym in enumerate(current_syms):
            if sym not in tm.gammas[i]:
                print(f"Error: invalid symbol '{sym}' on tape {i+1}")
                status = "Error"
                break
        if status is not None:
            break

        trans = find_transition(tm, state, current_syms)
        if trans is None:
            print("Error: no transition defined")
            status = "Error"
            break

        # New symbols
        new_syms = []
        for i in range(tm.k):
            w = trans["write"][i]
            new_syms.append(current_syms[i] if w == '*' else w)

        # TRACE ROW
        row = []
        row.append(str(step))
        row.append(str(trans["rule_num"]))
        row.extend(str(h) for h in heads)
        row.append(state)
        row.extend(current_syms)
        row.append(trans["new_state"])
        row.extend(new_syms)
        row.extend(trans["dirs"])
        print(','.join(row))

        # Apply writes
        for i in range(tm.k):
            tapes[i][heads[i]] = new_syms[i]

        # Move heads
        for i in range(tm.k):
            d = trans["dirs"][i]
            if d == 'L':
                heads[i] -= 1
            elif d == 'R':
                heads[i] += 1
            elif d == 'S':
                pass

            if heads[i] < 0 or heads[i] >= tm.max_tape_len:
                print(f"Error: head moved off tape {i+1}")
                status = "Error"
                break
        if status is not None:
            break

        state = trans["new_state"]
        step += 1

    print(status)
    print(f"Steps: {step}")
    for i in range(tm.k):
        print(f"Tape {i+1}: {tape_to_str(tapes[i])}")


def load_tape_file(tape_filename, k):
    """Load tape input file grouped by k lines per problem."""
    problems = []
    with open(tape_filename, 'r') as f:
        while True:
            block = []
            for _ in range(k):
                line = f.readline()
                if not line:
                    if block:
                        print("Warning: incomplete problem ignored")
                    return problems
                block.append(line.rstrip('\n'))
            problems.append(block)


def main():
    if len(sys.argv) != 3:
        print("Usage: python tm_netid.py <machine_file> <tape_file>")
        sys.exit(1)

    machine_file = sys.argv[1]
    tape_file = sys.argv[2]

    tm = load_machine(machine_file)
    print(f"Loaded machine: {tm.name}")
    print(f"Tape file: {tape_file}")

    problems = load_tape_file(tape_file, tm.k)
    for i, p in enumerate(problems, start=1):
        run_problem(tm, p, i)


if __name__ == "__main__":
    main()




