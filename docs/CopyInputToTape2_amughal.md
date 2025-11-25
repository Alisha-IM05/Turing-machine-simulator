# Machine: CopyInputToTape2_amughal

## Type
Computation (2-tape)

## Goal
Copy the binary input from Tape 1 → Tape 2.

## How It Works
State q0 handles the copy:
- If Tape1 = 0 and Tape2 = _, write (0,0) and move R,R.
- If Tape1 = 1 and Tape2 = _, write (1,1) and move R,R.
- When Tape1 reads `_`, transition to accept.

## Example
Input: `101`  
Final Tape 2: `101`

## Testing
Tape file: tapes/tapes-CopyInputToTape2_netid.txt  
Three problems were tested:
- 0 → copied
- 101 → copied
- 00011 → copied

All halt in accept.



