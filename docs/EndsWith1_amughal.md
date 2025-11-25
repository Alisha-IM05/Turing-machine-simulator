# Machine: EndsWith1_amughal

## Type
Decider.

## Language
L = { w ∈ {0,1}* : w ends in 1 }

## How It Works
- q0 scans right until it hits `_`.
- q1 moves back one cell:
  - If the last symbol is `1`, go to accept.
  - Otherwise reject.

## State Diagram (textual)

q0:
- 0 → q0 (R)
- 1 → q0 (R)
- _ → q1 (L)

q1:
- 1 → qa
- 0 → qr
- _ → qr

## Testing
Tape file: tapes/tapes-EndsWith1_netid.txt  
Results:
- Accept: 1, 101, 111  
- Reject: 0, 10, 1010

