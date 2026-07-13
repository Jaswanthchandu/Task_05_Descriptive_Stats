# Prompt-and-Response Log, Task 5

**Model used:** Claude (Anthropic), accessed through the Claude app.
**Dataset:** 2025 Syracuse Women's Lacrosse season (see README).
**Ground truth:** `ground_truth.py` and `gamechanger.py`, computed independently before
checking the model.
**Method:** The dataset (`players.csv`, `games.csv`) was pasted into Claude. Each question below records the prompt, a summary of Claude's answer,
the verdict against ground truth, and how the model arrived at its answer.

---

## Phase A, Factual questions

| # | Prompt | Claude's answer | Ground truth | Verdict | How it answered |
|---|--------|-----------------|--------------|---------|-----------------|
| 1 | How many games did the team play? | 19 | 19 | Correct | Ran pandas locally on the data |
| 2 | What was the record? | 10-9 | 10-9 | Correct | Computed from games |
| 3 | Who scored the most goals? | Emma Muchnick, 34 | Muchnick, 34 | Correct | Did not confuse with points leader |
| 4 | Most assists / most points? | Ward 46 / Ward 76 | Ward 46 / 76 | Correct | Computed |
| 5 | Average margin of victory in wins? | 5.50 | 5.50 | Correct | Computed over wins only |
| 6 | Highest combined score game? | UAlbany, 30 (21-9) | UAlbany, 30 | Correct | Computed |
| 7 | Do the individual goals add up to the team total? | Flagged a 1-goal gap: individuals sum to 234, team total 235; proposed three causes | 234 vs 235 gap is real | Correct + insightful | Reasoned over data, then offered to verify game-by-game |

**Phase A observation:** Claude answered 6/6 factual questions correctly and, on the
seventh, independently caught a data-quality discrepancy (234 individual goals vs the
235 team total) that was genuinely present in the source PDF. It reasoned over the
actual numbers rather than restating them, and proposed a verification method rather
than guessing at the cause.

### Follow-up factual / stress questions

| # | Prompt | Claude's answer | Ground truth | Verdict |
|---|--------|-----------------|--------------|---------|
| 8 | Best points-per-game? | Ward 4.00 (honest answer); footnoted Adamson 5.33 as a 3-game small-sample artifact | Ward 4.00 over 19 GP | Correct + caught small-sample trap |
| 9 | Games decided by <=2 goals? | 7 (six 1-goal, one 2-goal vs Loyola); team 4-3 in them | 7 close games, 4-3 | Correct |
| 10 | Average scoring margin, all games? | +0.74; correctly explained why this differs from the +5.50 win-margin | +0.74 | Correct |
| 11 | Draw-controls leader? | Meghan Rode, 75 | Rode, 75 | Correct |
| 12 | Which player improved most, first half to second half? | Refused: season totals only, no per-game player splits; stated exactly what data would be needed | Unanswerable from this data | Correct refusal (did not fabricate) |

**Key Phase A finding:** Question 12 was deliberately unanswerable from the data
provided. Claude correctly identified the limitation and declined to invent an answer,
naming the specific file it would need (a game-by-game player log). This is the single
most valuable result of Phase A: the model admitted a limit instead of confabulating.

---

## Phase B, Derived metric, judgment, prompt engineering

### Step 1, Metric definition (first attempt)

**Prompt:** Defined "game-changer" as contributing across three per-game phases , 
offense (points/game), possession ((draw controls + ground balls)/game), defense
(caused turnovers/game), with an 8+ games filter.

**Claude's response:** Flagged that the definition was *underspecified*: the three
phases live on different scales, so the combination rule controls the answer. Showed
that a raw sum lets possession and offense swamp defense. Offered an equal-weight
z-score sum, which produced **Coco Vandiver #1** (on a single freakish defensive stat),
Ward 5th. Explicitly noted the result was sensitive to the rule *it* had chosen, and
asked which reading of "game-changer" was intended.

**Verdict / finding:** This is the core Phase B lesson. The metric as first written did
not determine an answer. Two reasonable combination rules (max-normalization in my own
`gamechanger.py` vs Claude's z-score sum) produced *different* #1 players. Claude
surfaced this rather than hiding it behind one number.

### Step 2, Tightening the metric (prompt engineering)

**Prompt:** "Use the balance-rewarding version, reward players positive across all
three phases rather than extreme in one. I want a genuine two-way game-changer, not a
single-phase specialist."

**Claude's response:** Ran three balance methods (weakest-link, spread-penalty,
geometric mean). Weakest-link and spread-penalty both ranked **Alexa Vogelman #1**;
geometric mean flipped to Caramelli and Claude explained why (Caramelli's large
possession z-score). Identified the same four all-phase-positive players my own script
found (Vogelman, Caramelli, Muchnick, Cotter). Recommended Vogelman as the safest answer
to the stated intent.

**Validation:** My own `gamechanger.py` balance-rewarding (spread-penalty) ranking
independently produced **Vogelman #1, Caramelli #2, Muchnick #3** and the same four
all-phase-positive players. Claude's answer matched my independent computation. The
improvement from Step 1 (Vandiver) to Step 2 (Vogelman) came entirely from *tightening
the metric definition*, the clearest demonstration of prompt engineering moving a weak
answer to a validated one.

### Step 3, The advisory coaching question

**Prompt:** "Lock in Vogelman. As a coach, to win two more games next season, should I
focus on offense or defense, and is Vogelman the one player to develop, or someone else,
and why?"

**Claude's response:** Argued **offense, not defense.** Reasoning: only three losses are
realistically convertible (the one-goal games vs Clemson, Yale, Johns Hopkins); in those
the team scored 9.7 vs its 12.4 season average while the defense held near its norm; the
season-wide split (wins: 15.7 for / 10.2 against; losses: 8.7 / 13.2) shows scoring
swings 7 goals between winning and losing while defense swings 3. Recommended developing
Vogelman for a new reason: she is a 46% shooter (top-three) who generates her own
possessions but takes only 2.4 shots/game, while the highest-volume shooter (Ward, 77
shots) is the least efficient at 39%. Lever: raise Vogelman to ~4 shots/game (~+0.7
goals). Gave honest caveats (efficiency usually drops with volume; 46% is a moderate
sample; the JHU game was a defensive loss).

**Validation against my own analysis (all confirmed):**
- Wins 15.7 for / 10.2 against; losses 8.7 / 13.2, verified. Scoring swing 7, defense swing 3.
- Three one-goal losses (Clemson 8-9, JHU 13-14, Yale 8-9); average 9.7 scored, verified.
- Vogelman 21G/46Sh = 46%, 2.4 shots/game; Ward 30G/77Sh = 39%, 4.1/game;
  Muchnick 34G/71Sh = 48%, 3.7/game, all verified exactly.
- Minor correction: the three one-goal losses averaged 10.7 goals *allowed*, slightly
  **below** the 11.6 season norm, which strengthens Claude's "defense wasn't the
  problem" point rather than weakening it.

**Verdict:** The recommendation survives independent validation completely. The only
unverifiable part is the forward projection ("+0.7 goals if Vogelman shoots more"),
which Claude correctly hedged as an estimate. Backward-looking claims are exact.
