# Machine: EqualCount01_amughal

## Type: 
Decider (2-tape)

## Language: 
L = { w ∈ {0,1}* : w has equal number of 0s and 1s }

## Algorithm Overview
This 2-tape Turing machine uses a marking strategy:

- Mark all 0s: Scan input left-to-right, write 'X' on tape 2 for each '0'
= Cancel marks for 1s: Scan input again, erase one 'X' for each '1'
= Verify: Accept if tape 2 is empty; reject otherwise

## State Descriptions

q_scan0 (Initial state)
Scans tape 1 from left to right:
- On '0': Write 'X' on tape 2, move both right
- On '1': Move tape 1 right only (no mark)
- On '_' (blank): Done counting 0s, transition to q_rewind1

q_rewind1
 Prepares to scan again by moving tape 2 to the left end:
- Immediately transitions to q_scan1

q_scan1
Moves tape 2 head to the leftmost position:
- Move tape 2 left while reading 'X' or '_'
- On '_' on tape 2: Reached the beginning, transition to q_check

q_check
Scans tape 1 again and cancels marks:
- On '0' with 'X' on tape 2: Skip (move right on tape 1)
- On '0' with '_' on tape 2: Skip (move right on tape 1)
- On '1' with 'X' on tape 2: Erase the 'X', move both tapes right
- On '1' with '_' on tape 2: Reject (more 1s than 0s)
- On '_' on tape 1:
- If tape 2 has 'X': Reject (more 0s than 1s)
- If tape 2 has '_': Accept (equal count!)



## Example Traces

Input: "01" → Accept

q_scan0: 01_ → Tape2: X_ (marked the 0)
q_rewind1 → q_scan1: Move tape 2 to start
q_check: Process '0' (skip), process '1' (erase X)
End of tape 1, tape 2 is empty → Accept ✓

Input: "0011" → Accept

q_scan0: Mark two 0s → Tape2: XX
q_check: Two 1s erase two Xs
Both tapes empty at end → Accept ✓

Input: "10" → Accept

q_scan0: '1' (no mark), '0' (mark X) → Tape2: X
q_check: '1' erases X, '0' (skip)
End: tape 2 empty → Accept ✓

Input: "000" → Reject

q_scan0: Three 0s → Tape2: XXX
q_check: No 1s to cancel
End: tape 2 has XXX → Reject ✓

Input: "111" → Reject

q_scan0: Three 1s → Tape2: `` (empty)
q_check: First '1' tries to erase, but tape 2 is '_'
→ Reject ✓

Input: "" (empty) → Accept

q_scan0: Immediately sees blank
q_check: Both tapes empty
→ Accept ✓

## Testing
Tape file: tapes/tapes-EqualCount01_amughal.txt

Expected Results:

Accept: ε (empty), 01, 0011, 0101, 111000, 1010, 00110, 100110

Reject: 0, 1, 001

## Implementation Notes:

- Uses wildcards (*) for "don't care" symbols
- Maximum tape length: 100 cells
- Maximum steps: 10,000
- Tape 2 alphabet: {X, _} where X is the marker
