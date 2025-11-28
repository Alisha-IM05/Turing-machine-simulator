- T1 = Tape 1, T2 = Tape 2
- Format: (read) → (write) / direction
- R = move right, S = stay
- qa = accept state, qr = reject state
- = wildcard (any symbol)


  

CopyInputToTape2_amughal
       ┌─────────────────────────────────────┐
       │              q0                     │
       │  (Copy symbols from T1 to T2)       │
       └─────────────────────────────────────┘
              │                    │
              │ (0,_)→(0,0)/R,R   │ (1,_)→(1,1)/R,R
              └────────┐  ┌────────┘
                       ↓  ↑
                       │  │
                       └──┘
              
              │
              │ (_,_)→(_,_)/S,S
              ↓
           ┌─────┐
           │ qa  │ (Accept)
           └─────┘

State q0: Main loop - reads from tape 1, writes to tape 2

If T1=0 and T2=_: Write (0,0), move both right, stay in q0
If T1=1 and T2=_: Write (1,1), move both right, stay in q0
If T1=_ (end of input): Go to qa (accept)




EqualCount01_amughal
       ┌──────────────────────────────────────────────────────┐
       │                      q0                              │
       │  (Maintain counter on T2: increment for 0s,          │
       │   decrement for 1s, check balance at end)            │
       └──────────────────────────────────────────────────────┘
              │                                    │
              │  Increment (T1=0):                │  Decrement (T1=1):
              │  • _→1, 0→1, 1→2, ..., 8→9       │  • _→A, 1→0, 2→1, ..., 9→8
              │  • A→_, B→A, ..., I→H            │  • A→B, B→C, ..., H→I
              │  All move R,S, stay in q0         │  All move R,S, stay in q0
              │                                    │
              ├────────────────┐  ┌────────────────┤
              │                ↓  ↑                │
              │                └──┘                │
              │                                    │
              ├─── (0,9)→(0,9)/S,S ────────────────┤
              │    [Overflow]                      │
              │                                    │
              ├─── (1,0)→(1,0)/S,S ────────────────┤
              │    [Underflow]                     │
              │                                    │
              └─── (1,I)→(1,I)/S,S ────────────────┤
                   [Too many 1s]                   │
                                                    ↓
                                                 ┌─────┐
                                                 │ qr  │ (Reject)
                                                 └─────┘
              
       At end of input (T1=_):
              │
              ├─── (_,_)→(_,_)/S,S ────────────────┐
              │    [Balanced]                      │
              │                                    ↓
              ├─── (_,0)→(_,0)/S,S ─────────────► ┌─────┐
              │    [Balanced]                     │ qa  │ (Accept)
              │                                   └─────┘
              └─── (_,*)→(_,*)/S,S ─────────────► qr
                   [Not balanced]


State q0: Single state that processes entire input
When T1 = '0' (increment counter):

T2=_: Write 1, move R,S, stay q0
T2=0-8: Write next digit, move R,S, stay q0
T2=9: REJECT (overflow)
T2=A-I: Write prev letter (canceling negative), move R,S, stay q0

When T1 = '1' (decrement counter):

T2=_: Write A (go negative), move R,S, stay q0
T2=0: REJECT (tried to decrement past 0)
T2=1-9: Write prev digit, move R,S, stay q0
T2=A-H: Write next letter (more negative), move R,S, stay q0
T2=I: REJECT (underflow)

When T1 = '_' (end of input - check balance):

T2=_ or T2=0: ACCEPT (balanced!)
T2=anything else: REJECT (not balanced)
