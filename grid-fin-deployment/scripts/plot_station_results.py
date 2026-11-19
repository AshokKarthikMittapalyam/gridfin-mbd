"""Plot the 3DEXPERIENCE Motion Design results of the grid fin flap actuation station.

Reads the sensor CSVs exported from the 2D plots (simulation/results/) and writes PNG
figures to simulation/plots/, plus a short text summary of the key values.

Usage: python plot_station_results.py
"""
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1] / "simulation"
RES = ROOT / "results"
OUT = ROOT / "plots"


def read_pairs(name: str) -> list[tuple[list[float], list[float], str]]:
    """Return (x, y, label) for each x/y column pair of a 2D Plot export."""
    with (RES / name).open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))
    header = rows[0]
    data = [[float(v) for v in r] for r in rows[1:] if r]
    pairs = []
    for j in range(1, len(header), 2):
        label = header[j].split(": ", 1)[-1]
        pairs.append(([r[j - 1] for r in data], [r[j] for r in data], label))
    return pairs


def extremes(xs: list[float], ys: list[float]) -> str:
    i_min = min(range(len(ys)), key=ys.__getitem__)
    i_max = max(range(len(ys)), key=ys.__getitem__)
    return (f"start {ys[0]:.2f}, end {ys[-1]:.2f}, min {ys[i_min]:.2f} at {xs[i_min]:g}, "
            f"max {ys[i_max]:.2f} at {xs[i_max]:g}")


def style(ax, xlabel: str, ylabel: str, title: str) -> None:
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True, alpha=0.3)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    summary = []

    (t_s, s, _), (t_v, v, _) = read_pairs("kinematic_5s_piston_stroke_velocity.csv")
    (t_a, a, _), = read_pairs("kinematic_5s_fin_angle.csv")
    a_rel = [x - a[0] for x in a]
    fig, axs = plt.subplots(3, 1, figsize=(8, 8), sharex=True)
    axs[0].plot(t_s, s, color="tab:orange")
    style(axs[0], "", "Piston stroke (mm)", "Kinematic run: piston-driven flap actuation (5 s)")
    axs[1].plot(t_v, [x * 1000 for x in v], color="tab:red")
    style(axs[1], "", "Piston velocity (mm/s)", "")
    axs[2].plot(t_a, a_rel, color="tab:blue")
    style(axs[2], "Time (s)", "Fin rotation from start (deg)", "")
    fig.tight_layout()
    fig.savefig(OUT / "kinematic_time_histories.png", dpi=150)
    plt.close(fig)
    summary += ["Kinematic run (5 s):",
                f"  piston stroke (mm): {extremes(t_s, s)}",
                f"  piston velocity (m/s): {extremes(t_v, v)}",
                f"  Revolute.11 rotation (deg): {extremes(t_a, a)}",
                f"  fin rotation range (deg): {max(a) - min(a):.2f}"]

    (x_k, y_k, _), = read_pairs("kinematic_5s_fin_angle_vs_stroke.csv")
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(x_k, [y - y_k[0] for y in y_k], color="tab:blue")
    style(ax, "Piston stroke (mm)", "Fin rotation from start (deg)", "Fin rotation against piston stroke")
    fig.tight_layout()
    fig.savefig(OUT / "kinematic_fin_angle_vs_stroke.png", dpi=150)
    plt.close(fig)

    (t_p, p, _), = read_pairs("dynamic_1p6s_fin_angle_probe.csv")
    com = read_pairs("dynamic_1p6s_fin_centre_of_mass.csv")
    fig, axs = plt.subplots(2, 1, figsize=(8, 6.5), sharex=True)
    axs[0].plot(t_p, p, color="tab:blue")
    style(axs[0], "", "Fin angle, YZ projection (deg)", "Dynamic run (1.6 s, 1 ms output step)")
    for (t_c, c, lab), col in zip(com[1:], ("tab:green", "tab:purple")):
        axs[1].plot(t_c, [x - c[0] for x in c], color=col, label=lab.split("/")[-1])
    axs[1].legend()
    style(axs[1], "Time (s)", "Fin centre of mass shift (mm)", "")
    fig.tight_layout()
    fig.savefig(OUT / "dynamic_fin_response.png", dpi=150)
    plt.close(fig)
    summary += ["Dynamic run (1.6 s):",
                f"  angle probe (deg): {extremes(t_p, p)}"]
    summary += [f"  {lab}: {extremes(t_c, c)}" for t_c, c, lab in com]

    text = "\n".join(summary)
    (OUT / "summary.txt").write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
