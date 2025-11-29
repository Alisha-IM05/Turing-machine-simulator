### State Diagrams

## Notation:

- T1 = Tape 1

- T2 = Tape 2

## Format: (read) → (write) / direction

- R = move right

- S = stay

- qa = accept state

- qr = reject state

- _ = wildcard / blank

  ## CopyInputToTape2_amughal

  ┌──────────────────────────────────────────┐
│ q0                                       │
│ (Copy symbols from T1 to T2)             │
└──────────────────────────────────────────┘
       │                    │
       │ (0, _) → (0, 0) / R, R
       │ (1, _) → (1, 1) / R, R
       └──────────────┐  ┌───────────────┘
                      ↓  ↑
                     (_, _) → (_, _) / S, S
                      ↓
                 ┌─────────┐
                 │   qa    │  Accept
                 └─────────┘

## State q0 Behavior

Reads from Tape 1 and writes to Tape 2.

- If T1 = 0 and T2 = _ → write (0,0), move R,R, stay in q0

- If T1 = 1 and T2 = _ → write (1,1), move R,R, stay in q0

- If T1 = _ (end of input) → go to qa (accept)


## EqualCount01_amughal

┌───────────────────────────────────────────────────────────────┐
│ q0                                                            │
│ (Maintain counter on T2: increment for 0s,                    │
│  decrement for 1s, check balance at end)                      │
└───────────────────────────────────────────────────────────────┘
       │                               │
       │ Increment (T1 = 0):           │ Decrement (T1 = 1):
       │ • _ → 1                       │ • _ → A
       │ • 0 → 1                       │ • 1 → 0
       │ • 1 → 2                       │ • 2 → 1
       │ • … up to 8 → 9               │ • … 9 → 8
       │ • A → _                       │ • A → B
       │ • B → A                       │ • B → C
       │ • … I → H                     │ • … H → I
       │ All moves: R,S, stay q0       │ All moves: R,S, stay q0
       │
       ├───────────────────────┐   ┌───────────────────────────┤
       │                       ↓   ↑                           │
       │              (0, 9) → (0, 9) / S,S   [Overflow]       │
       │              (1, 0) → (1, 0) / S,S   [Underflow]      │
       │              (1, I) → (1, I) / S,S   [Too many 1s]    │
       │                       ↓
       │                   ┌────────┐
       │                   │  qr    │ Reject
       │                   └────────┘
       ├── (_, _) → (_, _) / S,S  →  Balanced → qa
       │
       ├── (_, 0) → (_, 0) / S,S  →  Balanced → qa
       │
       └── (_, *) → (_, *) / S,S  →  Not balanced → qr

# Case: T1 = '0' (increment counter)

| T2 value | Action                                              |
| -------- | --------------------------------------------------- |
| `_`      | Write **1**, move **R,S**, stay q0                  |
| `0`–`8`  | Write next digit, move **R,S**, stay q0             |
| `9`      | **Reject** (overflow)                               |
| `A`–`I`  | Write previous letter (canceling negative), stay q0 |


# Case: T1 = '1' (decrement counter)

| T2 value | Action                                     |
| -------- | ------------------------------------------ |
| `_`      | Write **A**, move **R,S**, stay q0         |
| `0`      | **Reject** (underflow)                     |
| `1`–`9`  | Write previous digit, stay q0              |
| `A`–`H`  | Write next letter (more negative), stay q0 |
| `I`      | **Reject** (too negative)                  |


# Case: T1 = '_' (end of input — check balance)

| T2 value      | Result                    |
| ------------- | ------------------------- |
| `_` or `0`    | **ACCEPT** (balanced)     |
| anything else | **REJECT** (not balanced) |







