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
                   │   Maintain counter on T2 (increment for 0s,              │
                   │   decrement for 1s, check balance at end)               │
                   └──────────────────────────────────────────────────────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         │                         │                         │
         │ Increment (T1 = 0)      │ Decrement (T1 = 1)      │
         │----------------------   │----------------------    │
         │ _ → 1                   │ _ → A                   │
         │ 0 → 1                   │ 1 → 0                   │
         │ 1 → 2                   │ 2 → 1                   │
         │ ...                     │ ...                     │
         │ 8 → 9                   │ 9 → 8                   │
         │ A → _                   │ A → B                   │
         │ B → A                   │ B → C                   │
         │ C → B                   │ C → D                   │
         │ ...                     │ ...                     │
         │ H → G                   │ H → I                   │
         │ I → H                   │ I → * (underflow)       │
         │ All moves = R,S         │ All moves = R,S         │
         │ Stay in q0              │ Stay in q0              │
         └─────────────────────────┴─────────────────────────┘
                                   │
                                   │
                ┌──────────────────┼──────────────────────┬───────────────────┐
                │                  │                      │                   │
      (0,9) → (0,9)/S,S     (1,0) → (1,0)/S,S      (1,I) → (1,I)/S,S        (_,_)
         Overflow              Underflow            Too many 1s               │
                │                  │                      │                   │
                │                  │                      │                   ↓
                └──────────────────┴──────────────────────┴───────────────┐
                                                                            │
                                                                      ┌─────────┐
                                                                      │   qr    │ Reject
                                                                      └─────────┘
```

---

# End-of-Input Behavior

```
T1 = _ (input finished):

(_,_) → (_ , _) / S,S    → Balanced → qa
(_,0) → (_ , 0) / S,S    → Balanced → qa
(_,*) → (_ , *) / S,S    → Not balanced → qr
```

---

# Summary

```
If final tape2 ∈ { _, 0 }   → ACCEPT
Else                        → REJECT
```

