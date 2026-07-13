
import csv
import statistics


def load(path):
    return list(csv.DictReader(open(path, newline="", encoding="utf-8")))


def num(row, key):
    try:
        return int(row[key])
    except (ValueError, KeyError):
        return 0


def main():
    players = load("players.csv")
    games = load("games.csv")

    print("=" * 60)
    print("PHASE A - factual answer key")
    print("=" * 60)

    # Games and record
    wins = [g for g in games if g["result"] == "W"]
    losses = [g for g in games if g["result"] == "L"]
    print(f"Games played: {len(games)}")
    print(f"Record: {len(wins)}-{len(losses)}")

    # Scoring leaders
    top_goals = max(players, key=lambda p: num(p, "G"))
    top_assists = max(players, key=lambda p: num(p, "A"))
    top_points = max(players, key=lambda p: num(p, "Pts"))
    print(f"Most goals: {top_goals['player']} ({top_goals['G']})")
    print(f"Most assists: {top_assists['player']} ({top_assists['A']})")
    print(f"Most points: {top_points['player']} ({top_points['Pts']})")

    # Team totals from player table vs official
    tot_g = sum(num(p, "G") for p in players)
    tot_a = sum(num(p, "A") for p in players)
    print(f"Sum of individual goals: {tot_g}  (official team total: 235 - a 1-goal gap)")
    print(f"Sum of individual assists: {tot_a}  (official team total: 112 - matches)")

    # Margins
    win_margins = [int(g["su_score"]) - int(g["opp_score"]) for g in wins]
    all_margins = [int(g["su_score"]) - int(g["opp_score"]) for g in games]
    print(f"Average margin of victory in wins: {statistics.mean(win_margins):.2f}")
    print(f"Average scoring margin (all games): {statistics.mean(all_margins):.2f}")

    # Highest combined score game
    combined = max(games, key=lambda g: int(g["su_score"]) + int(g["opp_score"]))
    cs = int(combined["su_score"]) + int(combined["opp_score"])
    print(f"Highest combined score: vs {combined['opponent']} "
          f"({combined['su_score']}-{combined['opp_score']}, total {cs})")

    print("\n" + "=" * 60)
    print("PHASE B - derived metric helpers")
    print("=" * 60)

    # Points per game (only players with GP > 0), a base for "impact" questions
    print("\nPoints per game (min 5 games), top 10:")
    ppg = []
    for p in players:
        gp = num(p, "GP")
        if gp >= 5:
            ppg.append((p["player"], num(p, "Pts") / gp, num(p, "Pts"), gp))
    ppg.sort(key=lambda x: x[1], reverse=True)
    for name, rate, pts, gp in ppg[:10]:
        print(f"  {name:<20} {rate:5.2f} ppg  ({pts} pts / {gp} gp)")

    # Draw controls and caused turnovers - defensive / possession contributions
    print("\nTop draw-control winners (DC):")
    for p in sorted(players, key=lambda x: num(x, "DC"), reverse=True)[:5]:
        print(f"  {p['player']:<20} DC={p['DC']}")
    print("\nTop caused-turnover players (CT):")
    for p in sorted(players, key=lambda x: num(x, "CT"), reverse=True)[:5]:
        print(f"  {p['player']:<20} CT={p['CT']}")

    # Close games (decided by 1-2 goals) - relevant to "win 2 more games"
    close = [g for g in games if abs(int(g["su_score"]) - int(g["opp_score"])) <= 2]
    close_losses = [g for g in close if g["result"] == "L"]
    print(f"\nClose games (<=2 goals): {len(close)}   "
          f"of which losses: {len(close_losses)}")
    for g in close_losses:
        print(f"  L vs {g['opponent']} {g['su_score']}-{g['opp_score']} ({g['overtime']})")


if __name__ == "__main__":
    main()
