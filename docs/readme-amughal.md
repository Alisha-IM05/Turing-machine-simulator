# Project 1 — Turing Machine Simulator  
Author: Alisha Mughal (netid:amughal)

## 1. Overview
This project implements a full k-tape Turing Machine simulator capable of running
arbitrary machine files and tape input files. The simulator respects the rules from the
project specification including wildcards, stay moves, maximum tape length, maximum
step count, and grouped tape initialization.

## 2. Time Spent
Approximately 3 days.

## 3. Code Description
The main simulator is implemented in Python (`tm_amughal.py`). It reads a machine
description file, loads transitions into a structured internal representation,
and executes each set of tape inputs.

### Important design features:
- Arbitrary k tapes.
- Tape length bounds and simulation step bounds.
- `*` wildcard matching on read and no-write on write.
- Directions L, R, S.
- Trace output including rule number and head positions.

## 4. File Structure
- `tm_amughal.py` — simulator
- `machines/` — custom machine definitions
- `tapes/` — matching input problems for each machine
- `docs/` — documentation and per-machine writeups

## 5. Custom Machines
I created two machines:
1. A **2-tape computation** machine that copies input from tape 1 to tape 2.
2. A **2-tape decider** ("EqualCount01") that accepts binary strings with equal numbers of 0s and 1s.

Details are in the per-machine documents.

## Code Development Process
This project was developed using Git/GitHub for version control. The development process involved:
- Incremental testing with simple test cases first
- Debugging the simulator with instructor-provided test machines
- Iterative refinement of custom machine designs
- Regular commits to track progress and allow rollback if needed

## Key Data Structures
**Tapes**: Represented as Python lists of characters, with a fixed maximum length. Each tape is padded with blanks ('_') to the maximum length.

**Tape Heads**: A list of integers tracking the current position (0-indexed) of each tape head.

**States**: Stored as a set of strings for validation.

**Transitions**: Stored in a dictionary where:
- Key: initial state name (string)
- Value: list of transition dictionaries, each containing:
  - `rule_num`: integer rule number for tracing
  - `init_state`: initial state name
  - `read`: tuple of symbols read from each tape
  - `new_state`: next state name  
  - `write`: tuple of symbols to write to each tape
  - `dirs`: tuple of directions ('L', 'R', or 'S') for each head

This structure allows O(1) lookup of all rules for a given state, with sequential matching for wildcard support.

## 6. Testing
I ran:
- My custom machines on their tape files
- Instructor machines such as TM1d and TM1 (from Project_TM-v2.pdf)
All outputs match the expected behavior.

