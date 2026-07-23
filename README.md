# Task_05_Descriptive_Stats

> Note: The ground-truth scripts were developed with AI assistance; the analysis, the
> LLM interrogation, the validation, and the findings are my own.

Testing whether a large language model (Claude) can be trusted to reason about a real
dataset, by checking its answers against ground-truth statistics I computed myself. The
dataset is the 2025 Syracuse Women's Lacrosse season. Phase A tests factual questions
with verifiable answers; Phase B tests derived metrics and an open-ended coaching
judgment.

## Dataset

Source: [Syracuse Women's Lacrosse statistics (cuse.com)](https://cuse.com/sports/2013/1/16/WLAX_0116134638), 2025
season combined team statistics (as of May 12, 2025), 10-9 record over 19 games.

The official report is a PDF. I transcribed it into two small CSVs, which are included
here as my own derived work:
- `players.csv`, 32 players, season totals (games, goals, assists, points, shots,
  game-winners, ground balls, draw controls, turnovers, caused turnovers).
- `games.csv`, 19 games (date, opponent, home/away/neutral, result, scores, overtime).

Note on included data: The two CSVs here (players.csv, games.csv) are my own transcription of a public box score (linked above), included so that ground_truth.py, gamechanger.py, and the prompt log are fully reproducible. Since these are small, self-transcribed public stats rather than a large provided dataset, I opted to commit them; happy to remove them and add transcription instructions instead if you'd prefer.

## Ground-truth scripts

- `ground_truth.py`, the Phase A answer key: games, record, scoring leaders, margins,
  highest combined score, plus Phase B helpers (points per game, draw controls, caused
  turnovers, close games).
- `gamechanger.py`, the Phase B answer key: z-scored offense/possession/defense per
  game, reported under two combination rules (equal-weight sum and a balance-rewarding
  spread penalty), plus the list of players positive in all three phases.

Run:
```bash
python ground_truth.py
python gamechanger.py
```

## Prompt log

`PROMPT_LOG.md` contains every prompt, Claude's answer, the ground-truth value, my
verdict, and how the model arrived at each answer.

## What I found

### Phase A: Factual Questions

Claude answered all six factual questions correctly, including the number of games, the team's record, the goal leader, the assist and point leaders, the average winning margin, and the highest combined score in a game. It also wrote code to calculate these values instead of estimating them. However, I thought the more interesting questions were the ones that tested how it handled situations where the answer was less straightforward.

One example was checking whether the total number of player goals matched the team's official total. Claude found that the players scored 234 goals, while the official team total was 235. Instead of guessing why they were different, it suggested a few possible explanations and recommended checking the game-by-game results. After comparing the game scores with my own calculations, I confirmed that the official total of 235 was correct, which means one goal is missing from the player statistics in the source PDF.

Another interesting result came from the points-per-game question. Olivia Adamson had the highest average at 5.33 points per game, but she only played three games. Instead of simply reporting the highest average, Claude pointed out that the sample size was too small and identified Emma Ward, who averaged 4.00 points per game over all 19 games, as the more meaningful answer. I thought this was a reasonable interpretation because it considered the context instead of only the numbers.

I also asked which player improved the most between the first and second half of the season. Since the dataset only contains season totals and not game-by-game player statistics, Claude explained that there was not enough information to answer the question. Rather than making an assumption, it clearly stated that the data was insufficient. This was probably the most important result from Phase A because it showed that the model was willing to admit when the available data could not support an answer.

### Phase B: Derived Metrics and a Coaching Judgment

The biggest lesson from Phase B was that the definition of "game-changer" mattered much more than I expected. My original prompt described offense, possession, and defense, but it did not explain exactly how those three areas should be combined into a single score. Claude immediately pointed out that different combination methods could produce different rankings, and after checking my own scripts, I found that this was true.

My first implementation and Claude's first answer used different methods, which resulted in different top-ranked players. One method even selected Coco Vandiver, who is a defensive specialist with no scoring contribution. After I rewrote the prompt to reward players who performed well across all three areas instead of excelling in only one, Claude recalculated the rankings and selected Alexa Vogelman as the top game-changer. This matched the balance-based ranking produced by my own gamechanger.py script, with Vogelman, Caramelli, and Muchnick as the top three players and the same four players scoring positively in all three phases.

The final coaching question asked whether the team should focus more on offense or defense to win two additional games and which player should be developed further. Before looking at the numbers, I expected the answer to be defense because several losses were close games. However, Claude's explanation pointed in the opposite direction. It showed that in the three one-goal losses, the team's scoring dropped well below its season average, while the defensive performance stayed close to normal. Across the full season, the difference in scoring between wins and losses was much larger than the difference in goals allowed. Based on that evidence, Claude recommended giving Alexa Vogelman a larger offensive role because she shoots efficiently, wins possessions, and takes relatively few shots compared to the team's highest-volume shooter. After checking all of the historical statistics against my own scripts, every value matched. The only part I could not verify was the prediction that increasing her shot volume might add about 0.7 goals per game, but Claude clearly described this as an estimate rather than a fact.

## Where I would trust the model, and where I would not

After completing both phases, I found that Claude was very reliable when the answer could be calculated directly from the data. It correctly answered factual questions, identified a real data inconsistency, avoided drawing conclusions from a very small sample, and admitted when the available data was not enough to answer a question. These were all good signs because they showed that it was reasoning from the data instead of trying to produce an answer for every prompt.

At the same time, I also learned that the quality of the answer depends on how clearly the problem is defined. When I first asked about the "game-changer" metric, I had not explained exactly how the three performance areas should be combined, so Claude chose its own interpretation. Once I made the definition more specific, its results matched my own calculations. This showed me that the responsibility for defining the problem still belongs to the person asking the question.

Overall, I would trust Claude to calculate statistics, summarize data, and reason about well-defined metrics, especially when the results can be checked against the original data. However, I would still verify important conclusions with my own calculations and make sure that any evaluation metric is clearly defined before relying on the model's recommendations.

## Reproducibility



Transcribe the 2025 season stats from the source above into `players.csv` and
`games.csv` (included), run the two ground-truth scripts, then paste the CSVs into a
fresh LLM session and repeat the prompts in `PROMPT_LOG.md`.
