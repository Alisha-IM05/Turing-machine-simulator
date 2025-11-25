# Project 1 — Turing Machine Simulator  
Author: Alisha Mughal (netid:amughal)

## 1. Overview
This project implements a full k-tape Turing Machine simulator capable of running
arbitrary machine files and tape input files. The simulator respects the rules from the
project specification including wildcards, stay moves, maximum tape length, maximum
step count, and grouped tape initialization.

## 2. Time Spent
Approximately 48 hours total.

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
1. A **decider** (“EndsWith1”) that accepts strings ending in `1`.
2. A **2-tape computation** machine that copies input from tape 1 to tape 2.

Details are in the per-machine documents.

## 6. Testing
I ran:
- My custom machines on their tape files
- Instructor machines such as TM1d and TM1 (from Project_TM-v2.pdf)
All outputs match the expected behavior.

