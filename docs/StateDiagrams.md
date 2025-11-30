# CopyInputToTape2_amughal

```
                         ┌─────────────────────────────────────────────┐
                         │                     q0                      │
                         │         (Copy symbols from T1 → T2)         │
                         └─────────────────────────────────────────────┘
                                   │                           │
                     (0, _) → (0,0) / R,R           (1, _) → (1,1) / R,R
                                   │                           │
                                   └──────────────┬────────────┘
                                                  │
                                      (_,_) → (_ , _) / S,S
                                                  │
                                                  ↓
                                             ┌─────────┐
                                             │   qa    │  Accept
                                             └─────────┘
```

---

# State q0 Behavior

Reads from Tape 1 and writes to Tape 2.

- **If T1 = 0 and T2 = _** → write `(0,0)`, move `R,R`, stay in `q0`
- **If T1 = 1 and T2 = _** → write `(1,1)`, move `R,R`, stay in `q0`
- **If T1 = _** → go to **qa** (accept)

---

# EqualCount01_amughal

```
                   ┌──────────────────────────────────────────────────────────┐
                   │                          q0                              │
                   │   Single-state counter: increment for 0s, decrement for  │
                   │   1s on Tape 2, check balance at end                     │
                   └──────────────────────────────────────────────────────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         │                         │                         │
         │ Increment (T1 = 0)      │ Decrement (T1 = 1)      │
         │----------------------   │----------------------    │
         │ (0,_) → (0,1) / R,S     │ (1,_) → (1,A) / R,S     │
         │ (0,0) → (0,1) / R,S     │ (1,1) → (1,0) / R,S     │
         │ (0,1) → (0,2) / R,S     │ (1,2) → (1,1) / R,S     │
         │ (0,2) → (0,3) / R,S     │ (1,3) → (1,2) / R,S     │
         │ (0,3) → (0,4) / R,S     │ (1,4) → (1,3) / R,S     │
         │ (0,4) → (0,5) / R,S     │ (1,5) → (1,4) / R,S     │
         │ (0,5) → (0,6) / R,S     │ (1,6) → (1,5) / R,S     │
         │ (0,6) → (0,7) / R,S     │ (1,7) → (1,6) / R,S     │
         │ (0,7) → (0,8) / R,S     │ (1,8) → (1,7) / R,S     │
         │ (0,8) → (0,9) / R,S     │ (1,9) → (1,8) / R,S     │
         │ (0,A) → (0,_) / R,S     │ (1,A) → (1,B) / R,S     │
         │ (0,B) → (0,A) / R,S     │ (1,B) → (1,C) / R,S     │
         │ (0,C) → (0,B) / R,S     │ (1,C) → (1,D) / R,S     │
         │ (0,D) → (0,C) / R,S     │ (1,D) → (1,E) / R,S     │
         │ (0,E) → (0,D) / R,S     │ (1,E) → (1,F) / R,S     │
         │ (0,F) → (0,E) / R,S     │ (1,F) → (1,G) / R,S     │
         │ (0,G) → (0,F) / R,S     │ (1,G) → (1,H) / R,S     │
         │ (0,H) → (0,G) / R,S     │ (1,H) → (1,I) / R,S     │
         │ (0,I) → (0,H) / R,S     │                         │
         │ All stay in q0          │ All stay in q0          │
         └─────────────────────────┴─────────────────────────┘
                                   │
                                   │
                ┌──────────────────┼──────────────────────┬───────────────────┐
                │                  │                      │                   │
      (0,9) → (0,9)/S,S     (1,0) → (1,0)/S,S      (1,I) → (1,I)/S,S        (_,_)
         Overflow              Underflow            Too many 1s               │
                │                  │                      │                   │
                │                  │                      │                   ↓
                └──────────────────┴──────────────────────┘              ┌─────────┐
                                   │                                     │   qa    │ Accept
                                   ↓                                     └─────────┘
                              ┌─────────┐                                     ▲
                              │   qr    │ Reject                              │
                              └─────────┘                                     │
                                                                      (_,0) → (_,0)/S,S
                                                                      (_,_) → (_,_)/S,S

```


# End-of-Input Behavior


- (_,_) → (_ , _) / S,S    → Balanced (0 zeros, 0 ones) → qa
- (_,0) → (_ , 0) / S,S    → Balanced (equal count)      → qa
- (_,*) → (_ , *) / S,S    → Not balanced                → qr
- * = any symbol except _ or 0.




## Counter Representation

**Tape 2 symbols represent the difference (# of 0s - # of 1s):**

**Positive difference (more 0s than 1s):**
- `_` = 0 (but only initially, later means went negative then back to 0)
- `0` = 0 (balanced)
- `1` = +1
- `2` = +2
- ...
- `9` = +9

**Negative difference (more 1s than 0s):**
- `A` = -1
- `B` = -2
- `C` = -3
- ...
- `I` = -9

---

## Summary

If final tape2 ∈ { _, 0 }   → ACCEPT (equal count)
Else                        → REJECT (unequal count)


The machine uses a **bidirectional counter** on Tape 2 that:
- Increments when reading `0` from Tape 1
- Decrements when reading `1` from Tape 1
- Accepts only if counter returns to balanced state (`_` or `0`)
- Rejects on overflow/underflow or unbalanced final state
