import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe
import io
import numpy as np

# ── Color palette ──────────────────────────────────────────────
C = {
    "blue":      "#2E75B6",
    "darkblue":  "#1F4E79",
    "green":     "#70AD47",
    "orange":    "#ED7D31",
    "purple":    "#7030A0",
    "gray":      "#F2F2F2",
    "darkgray":  "#595959",
    "white":     "#FFFFFF",
    "red":       "#C00000",
    "lightblue": "#BDD7EE",
    "lightyellow":"#FFF2CC",
    "lightgreen": "#E2EFDA",
}

def fig_to_bytes(fig) -> bytes:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight",
                facecolor="white", edgecolor="none")
    plt.close(fig)
    buf.seek(0)
    return buf.read()


# ──────────────────────────────────────────────────────────────
# 1. Requirements Distribution Pie Chart
# ──────────────────────────────────────────────────────────────
def generate_requirements_pie(functional: list, non_functional: list) -> bytes:
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor("white")

    # Count NFR categories
    cats = {}
    for r in non_functional:
        c = r.get("category", "General")
        cats[c] = cats.get(c, 0) + 1

    labels = ["Functional"] + list(cats.keys())
    sizes  = [len(functional)] + list(cats.values())
    colors = [C["blue"], C["green"], C["orange"], C["purple"],
              C["red"], C["darkblue"], C["darkgray"]][:len(labels)]
    explode = [0.05] * len(labels)

    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=colors, explode=explode,
        autopct="%1.0f%%", startangle=140,
        textprops={"fontsize": 10, "fontfamily": "DejaVu Sans"},
        wedgeprops={"edgecolor": "white", "linewidth": 2}
    )
    for at in autotexts:
        at.set_fontsize(9)
        at.set_color("white")
        at.set_fontweight("bold")

    ax.set_title("Requirements Distribution", fontsize=14,
                 fontweight="bold", color=C["darkblue"], pad=15)
    ax.axis("equal")
    return fig_to_bytes(fig)


# ──────────────────────────────────────────────────────────────
# 2. Use Case Diagram
# ──────────────────────────────────────────────────────────────
def generate_use_case_diagram(project_name: str, functional: list) -> bytes:
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor("white")
    ax.set_xlim(0, 12); ax.set_ylim(0, 8)
    ax.axis("off")
    ax.set_facecolor("white")

    # System boundary box
    sys_box = FancyBboxPatch((2.2, 0.3), 8.5, 7.2,
                              boxstyle="round,pad=0.1",
                              linewidth=2, edgecolor=C["blue"],
                              facecolor=C["gray"])
    ax.add_patch(sys_box)
    ax.text(6.45, 7.3, f"<<System>>\n{project_name}", ha="center",
            fontsize=11, fontweight="bold", color=C["darkblue"])

    # Actor (stick figure)
    ax.add_patch(plt.Circle((0.9, 4.0), 0.3, color=C["darkblue"], zorder=5))
    ax.plot([0.9, 0.9], [3.7, 2.8], color=C["darkblue"], lw=2)
    ax.plot([0.3, 1.5], [3.2, 3.2], color=C["darkblue"], lw=2)
    ax.plot([0.9, 0.4], [2.8, 2.0], color=C["darkblue"], lw=2)
    ax.plot([0.9, 1.4], [2.8, 2.0], color=C["darkblue"], lw=2)
    ax.text(0.9, 1.7, "User", ha="center", fontsize=10,
            fontweight="bold", color=C["darkblue"])

    # Use cases — up to 8
    use_cases = [r.get("title", f"UC-{i+1}") for i, r in enumerate(functional[:8])]
    n = len(use_cases)
    ys = np.linspace(6.5, 1.0, n) if n > 1 else [4.0]

    for i, (uc, y) in enumerate(zip(use_cases, ys)):
        ellipse = mpatches.Ellipse((6.45, y), 5.5, 0.75,
                                   facecolor=C["lightblue"],
                                   edgecolor=C["blue"], linewidth=1.5, zorder=4)
        ax.add_patch(ellipse)
        label = uc[:38] + ("…" if len(uc) > 38 else "")
        ax.text(6.45, y, label, ha="center", va="center",
                fontsize=8.5, color=C["darkblue"], fontweight="bold", zorder=5)
        # Arrow from actor
        ax.annotate("", xy=(3.7, y), xytext=(1.5, 4.0),
                    arrowprops=dict(arrowstyle="->", color=C["darkgray"],
                                   lw=1.2, connectionstyle="arc3,rad=0"))

    ax.set_title("Use Case Diagram", fontsize=14,
                 fontweight="bold", color=C["darkblue"], pad=10)
    return fig_to_bytes(fig)


# ──────────────────────────────────────────────────────────────
# 3. System Architecture Diagram (3-tier)
# ──────────────────────────────────────────────────────────────
def generate_architecture_diagram(project_name: str) -> bytes:
    fig, ax = plt.subplots(figsize=(11, 7))
    fig.patch.set_facecolor("white")
    ax.set_xlim(0, 11); ax.set_ylim(0, 7)
    ax.axis("off")

    layers = [
        ("Presentation Layer",  ["Web Browser", "Mobile App", "Admin Panel"],
         C["lightblue"], C["blue"], 5.2),
        ("Application Layer",   ["Auth Service", "Business Logic", "API Gateway"],
         C["lightgreen"], C["green"], 3.4),
        ("Data Layer",          ["Database", "File Storage", "Cache (Redis)"],
         C["lightyellow"], C["orange"], 1.6),
    ]

    for title, boxes, bg, border, y_center in layers:
        # Layer background
        rect = FancyBboxPatch((0.3, y_center - 0.75), 10.4, 1.5,
                               boxstyle="round,pad=0.05",
                               facecolor=bg, edgecolor=border,
                               linewidth=2, zorder=2)
        ax.add_patch(rect)
        ax.text(0.65, y_center, title, va="center", fontsize=9,
                fontweight="bold", color=border, rotation=90)

        xs = [2.8, 5.5, 8.2]
        for x, label in zip(xs, boxes):
            b = FancyBboxPatch((x - 1.0, y_center - 0.45), 2.0, 0.9,
                                boxstyle="round,pad=0.05",
                                facecolor="white", edgecolor=border,
                                linewidth=1.5, zorder=3)
            ax.add_patch(b)
            ax.text(x, y_center, label, ha="center", va="center",
                    fontsize=9, color=C["darkblue"], fontweight="bold", zorder=4)

    # Arrows between layers
    for y_top, y_bot in [(4.45, 4.15), (2.65, 2.35)]:
        for x in [2.8, 5.5, 8.2]:
            ax.annotate("", xy=(x, y_bot), xytext=(x, y_top),
                        arrowprops=dict(arrowstyle="<->", color=C["darkgray"], lw=1.5))

    ax.set_title(f"System Architecture — {project_name}", fontsize=13,
                 fontweight="bold", color=C["darkblue"], pad=12)
    return fig_to_bytes(fig)


# ──────────────────────────────────────────────────────────────
# 4. Data Flow Diagram (DFD Level 0)
# ──────────────────────────────────────────────────────────────
def generate_dfd(project_name: str, functional: list) -> bytes:
    fig, ax = plt.subplots(figsize=(11, 6))
    fig.patch.set_facecolor("white")
    ax.set_xlim(0, 11); ax.set_ylim(0, 6)
    ax.axis("off")

    def box(cx, cy, w, h, label, color, tcolor="white"):
        r = FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                            boxstyle="round,pad=0.12",
                            facecolor=color, edgecolor=C["darkblue"],
                            linewidth=2, zorder=3)
        ax.add_patch(r)
        for i, line in enumerate(label.split("\n")):
            offset = (len(label.split("\n")) - 1) * 0.13
            ax.text(cx, cy + offset - i * 0.27, line,
                    ha="center", va="center", fontsize=9,
                    fontweight="bold", color=tcolor, zorder=4)

    def arrow(x1, y1, x2, y2, label=""):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color=C["blue"],
                                   lw=2, connectionstyle="arc3,rad=0"), zorder=2)
        if label:
            mx, my = (x1+x2)/2, (y1+y2)/2
            ax.text(mx, my + 0.18, label, ha="center", fontsize=8,
                    color=C["darkgray"], style="italic")

    # External entities
    box(1.2, 3.0, 1.6, 0.8, "User /\nClient",      C["darkblue"])
    box(9.8, 3.0, 1.6, 0.8, "Database /\nStorage",  C["darkblue"])

    # Central process
    box(5.5, 3.0, 2.8, 1.2, f"{project_name}\n(Core System)", C["blue"])

    # Sub-processes
    processes = [r.get("title", "Process")[:20] for r in functional[:3]]
    ys = [5.0, 3.0, 1.0]
    xs_proc = [5.5, 5.5, 5.5]
    pcolors = [C["green"], C["orange"], C["purple"]]
    for i, (proc, yp, xp, pc) in enumerate(zip(processes, ys, xs_proc, pcolors)):
        box(xp, yp + (1 if i == 0 else -1 if i == 2 else 0) * 0.0,
            2.4, 0.75, proc, pc)

    # Arrows
    arrow(1.95, 3.0, 4.1, 3.0, "Request / Input")
    arrow(6.9,  3.0, 8.95, 3.0, "Store / Retrieve")
    arrow(5.5,  3.6, 5.5,  4.6, "Process")
    arrow(5.5,  2.4, 5.5,  1.4, "Process")
    arrow(5.5,  5.0, 1.5,  3.4, "Response")

    ax.set_title(f"Data Flow Diagram (Level 0) — {project_name}",
                 fontsize=13, fontweight="bold", color=C["darkblue"], pad=10)
    return fig_to_bytes(fig)


# ──────────────────────────────────────────────────────────────
# 5. Non-Functional Requirements Bar Chart
# ──────────────────────────────────────────────────────────────
def generate_nfr_bar(non_functional: list) -> bytes:
    cats = {}
    for r in non_functional:
        c = r.get("category", "General")
        cats[c] = cats.get(c, 0) + 1

    if not cats:
        cats = {"General": len(non_functional) or 1}

    fig, ax = plt.subplots(figsize=(9, 4))
    fig.patch.set_facecolor("white")
    ax.set_facecolor(C["gray"])

    labels = list(cats.keys())
    values = list(cats.values())
    colors = [C["blue"], C["green"], C["orange"], C["purple"],
              C["red"], C["darkblue"]][:len(labels)]

    bars = ax.barh(labels, values, color=colors, height=0.5,
                   edgecolor="white", linewidth=1.5)
    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
                str(val), va="center", fontsize=10, fontweight="bold",
                color=C["darkblue"])

    ax.set_xlabel("Number of Requirements", fontsize=10, color=C["darkgray"])
    ax.set_title("Non-Functional Requirements by Category",
                 fontsize=13, fontweight="bold", color=C["darkblue"], pad=12)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(colors=C["darkgray"])
    ax.set_xlim(0, max(values) + 1.5)
    fig.tight_layout()
    return fig_to_bytes(fig)


# ──────────────────────────────────────────────────────────────
# 6. User Flow / Activity Diagram
# ──────────────────────────────────────────────────────────────
def generate_user_flow(functional: list) -> bytes:
    steps = [r.get("title", f"Step {i+1}") for i, r in enumerate(functional[:6])]
    if not steps:
        steps = ["Start", "Process", "End"]

    fig, ax = plt.subplots(figsize=(10, len(steps) * 1.4 + 1.5))
    fig.patch.set_facecolor("white")
    ax.axis("off")
    total_h = len(steps) * 1.4 + 1.5
    ax.set_xlim(0, 10); ax.set_ylim(0, total_h)

    cx = 5.0
    box_colors = [C["blue"], C["green"], C["orange"],
                  C["purple"], C["red"], C["darkblue"]]

    # Start oval
    start_y = total_h - 0.8
    start_e = mpatches.Ellipse((cx, start_y), 2.5, 0.6,
                                facecolor=C["darkblue"], edgecolor="white",
                                linewidth=2, zorder=3)
    ax.add_patch(start_e)
    ax.text(cx, start_y, "START", ha="center", va="center",
            fontsize=10, fontweight="bold", color="white", zorder=4)

    prev_y = start_y - 0.3
    for i, (step, bc) in enumerate(zip(steps, box_colors)):
        y = total_h - 1.5 - i * 1.4
        # Arrow
        ax.annotate("", xy=(cx, y + 0.4), xytext=(cx, prev_y),
                    arrowprops=dict(arrowstyle="->", color=C["darkgray"], lw=2))
        # Box
        b = FancyBboxPatch((cx - 2.8, y - 0.35), 5.6, 0.75,
                            boxstyle="round,pad=0.08",
                            facecolor=bc, edgecolor="white",
                            linewidth=1.5, zorder=3)
        ax.add_patch(b)
        label = step[:45] + ("…" if len(step) > 45 else "")
        ax.text(cx, y, label, ha="center", va="center",
                fontsize=9, fontweight="bold", color="white", zorder=4)
        prev_y = y - 0.35

    # End oval
    end_y = prev_y - 0.5
    ax.annotate("", xy=(cx, end_y + 0.3), xytext=(cx, prev_y),
                arrowprops=dict(arrowstyle="->", color=C["darkgray"], lw=2))
    end_e = mpatches.Ellipse((cx, end_y), 2.5, 0.6,
                              facecolor=C["darkblue"], edgecolor="white",
                              linewidth=2, zorder=3)
    ax.add_patch(end_e)
    ax.text(cx, end_y, "END", ha="center", va="center",
            fontsize=10, fontweight="bold", color="white", zorder=4)

    ax.set_title("User Activity Flow Diagram", fontsize=13,
                 fontweight="bold", color=C["darkblue"], pad=10)
    fig.tight_layout()
    return fig_to_bytes(fig)