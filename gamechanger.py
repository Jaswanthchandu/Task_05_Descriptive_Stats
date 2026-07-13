
import csv
import statistics

MIN_GP = 8


def num(row, key):
    try:
        return int(row[key])
    except (ValueError, KeyError):
        return 0


def zscores(values):
    mean = statistics.mean(values)
    sd = statistics.pstdev(values) or 1.0
    return [(v - mean) / sd for v in values]


def main():
    players = [p for p in csv.DictReader(open("players.csv"))
               if num(p, "GP") >= MIN_GP]

    off = [num(p, "Pts") / num(p, "GP") for p in players]
    pos = [(num(p, "DC") + num(p, "GB")) / num(p, "GP") for p in players]
    def_ = [num(p, "CT") / num(p, "GP") for p in players]

    off_z, pos_z, def_z = zscores(off), zscores(pos), zscores(def_)

    rows = []
    for i, p in enumerate(players):
        z = (off_z[i], pos_z[i], def_z[i])
        equal = sum(z)
        spread = max(z) - min(z)          # imbalance penalty
        balanced = equal - spread
        rows.append({"player": p["player"],
                     "off": off[i], "pos": pos[i], "def": def_[i],
                     "off_z": off_z[i], "pos_z": pos_z[i], "def_z": def_z[i],
                     "equal": equal, "balanced": balanced})

    print("RAW PER-GAME (min 8 games)")
    print(f"{'player':<20}{'off':>6}{'poss':>7}{'def':>6}")
    print("-" * 39)
    for r in sorted(rows, key=lambda x: x["equal"], reverse=True):
        print(f"{r['player']:<20}{r['off']:>6.2f}{r['pos']:>7.2f}{r['def']:>6.2f}")

    print("\n1) EQUAL-WEIGHT SUM (rewards single-phase extremes)")
    print(f"{'player':<20}{'offZ':>7}{'posZ':>7}{'defZ':>7}{'sum':>7}")
    print("-" * 48)
    for r in sorted(rows, key=lambda x: x["equal"], reverse=True)[:6]:
        print(f"{r['player']:<20}{r['off_z']:>7.2f}{r['pos_z']:>7.2f}"
              f"{r['def_z']:>7.2f}{r['equal']:>7.2f}")

    print("\n2) BALANCE-REWARDING (penalizes imbalance across phases)")
    print(f"{'player':<20}{'offZ':>7}{'posZ':>7}{'defZ':>7}{'score':>7}")
    print("-" * 48)
    for r in sorted(rows, key=lambda x: x["balanced"], reverse=True)[:6]:
        print(f"{r['player']:<20}{r['off_z']:>7.2f}{r['pos_z']:>7.2f}"
              f"{r['def_z']:>7.2f}{r['balanced']:>7.2f}")

    # Who is positive in ALL THREE phases?
    all_pos = [r["player"] for r in rows
               if r["off_z"] > 0 and r["pos_z"] > 0 and r["def_z"] > 0]
    print(f"\nPlayers positive in all three phases: {', '.join(all_pos) or 'none'}")


if __name__ == "__main__":
    main()
