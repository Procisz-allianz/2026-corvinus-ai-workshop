import math

FONT = "Segoe UI, Segoe UI Emoji, Arial, sans-serif"
NAVY = "#0B2A5B"
BLUE = "#2563EB"
PURPLE = "#7C3AED"
GREEN = "#16A34A"
GRAY = "#475569"
RED = "#DC2626"
FE_RED = "#E11D48"
BE_BLUE = "#1E5F82"
YELLOW = "#CA8A04"
ORANGE = "#EA580C"
TEAL = "#0D9488"
PINK = "#DB2777"
INK = "#1E293B"
LINE = "#CBD5E1"

METRICS = [
    ("growth", "Growth", "📈", GREEN),
    ("ebitda", "Profitability", "💰", BLUE),
    ("grossMargin", "Gross margin", "🧾", TEAL),
    ("runway", "Runway", "⏳", ORANGE),
    ("retention", "Customer loyalty", "🤝", PINK),
    ("funding", "Funding", "🏦", PURPLE),
]

DEFAULT_WEIGHTS = {"growth": 25, "ebitda": 20, "grossMargin": 15, "runway": 20, "retention": 10, "funding": 10}

EXAMPLE = {
    "growth": 69.5,
    "ebitdaMargin": -42.6,
    "grossMargin": 65.8,
    "runway": 15.7,
    "churn": 6.9,
    "funding": 50.6,
}

ROLES = {
    "Lead developer": ("💻", FE_RED),
    "Analyst": ("🔍", BLUE),
    "Designer": ("🎨", PINK),
    "Sales leader": ("💼", GREEN),
    "Marketing leader": ("📣", ORANGE),
    "Joker": ("🃏", PURPLE),
}


def clamp(value):
    return max(0.0, min(100.0, value))


def example_components():
    e = EXAMPLE
    return {
        "growth": clamp((e["growth"] + 10) / 1.2),
        "ebitda": clamp((e["ebitdaMargin"] + 30) * 2),
        "grossMargin": clamp(e["grossMargin"]),
        "runway": clamp(e["runway"] / 24 * 100),
        "retention": clamp(100 - e["churn"] * 8),
        "funding": clamp(math.log10(max(1, e["funding"]) + 1) * 25),
    }


def example_score():
    comps = example_components()
    return sum(comps[k] * DEFAULT_WEIGHTS[k] for k in comps) / 100


def num(value, digits=1):
    return f"{value:.{digits}f}"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def r1(v):
    return round(v, 1)


def svg(w, h, body, cls="", min_width=0):
    style = ""
    return (
        f'<div class="dia"><svg class="{cls}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
        f'font-family="{FONT}"{style}>{body}</svg></div>'
    )


def t(x, y, s, size=14, fill="#fff", weight=600, anchor="middle"):
    return f'<text x="{r1(x)}" y="{r1(y)}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{esc(s)}</text>'


def lines(x, y, arr, size=14, fill="#fff", weight=600, lh=None, anchor="middle"):
    lh = lh or size * 1.35
    return "".join(t(x, y + i * lh, s, size, fill, weight, anchor) for i, s in enumerate(arr))


def rect(x, y, w, h, fill, stroke="none", rx=14, sw=2, opacity=1):
    return (
        f'<rect x="{r1(x)}" y="{r1(y)}" width="{r1(w)}" height="{r1(h)}" rx="{rx}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="{sw}" fill-opacity="{opacity}"/>'
    )


def circle(x, y, r, fill, stroke="none", sw=2):
    return f'<circle cx="{r1(x)}" cy="{r1(y)}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def arrow(x1, y1, x2, y2, col=GRAY, w=3, head=11):
    dx, dy = x2 - x1, y2 - y1
    length = math.hypot(dx, dy)
    ux, uy = dx / length, dy / length
    bx, by = x2 - ux * head, y2 - uy * head
    px, py = -uy, ux
    pts = (
        f"{r1(x2)},{r1(y2)} {r1(bx + px * head * 0.55)},{r1(by + py * head * 0.55)} "
        f"{r1(bx - px * head * 0.55)},{r1(by - py * head * 0.55)}"
    )
    return (
        f'<line x1="{r1(x1)}" y1="{r1(y1)}" x2="{r1(bx)}" y2="{r1(by)}" stroke="{col}" '
        f'stroke-width="{w}" stroke-linecap="round"/><polygon points="{pts}" fill="{col}"/>'
    )


def node(x, y, w, h, fill, icon, arr, size=13, tc="#fff"):
    out = rect(x, y, w, h, fill)
    out += f'<text x="{r1(x + w / 2)}" y="{r1(y + h * 0.4)}" font-size="32" text-anchor="middle">{icon}</text>'
    out += lines(x + w / 2, y + h * 0.64, arr, size, tc, 700)
    return out


def badge(x, y, n, col):
    return circle(x, y, 13, "#fff", col, 3) + t(x, y + 5, str(n), 14, col, 800)


def big_picture():
    xs = [0, 150, 300, 450, 600]
    w, y, h = 120, 28, 130
    spec = [
        (GRAY, "📄", ["Excel file", "1000 startups"]),
        (BLUE, "📥", ["Loading", "the data"]),
        (BLUE, "🧮", ["Scoring", "6 criteria"]),
        (PURPLE, "🤖", ["AI analysis", "you can ask it"]),
        (GREEN, "🏆", ["Proof", "the best startup"]),
    ]
    pills = ["The data", "The program does it", "The program does it", "The AI helps", "Your product shows it"]
    body = ""
    for i, ((col, icon, arr), x) in enumerate(zip(spec, xs)):
        body += node(x, y, w, h, col, icon, arr)
        body += badge(x + 12, y + 4, i + 1, col)
        body += rect(x, 178, w, 32, col, rx=16, opacity=0.14)
        body += t(x + w / 2, 199, pills[i], 11.5, col, 700)
        if i < 4:
            body += arrow(x + w + 3, y + h / 2, xs[i + 1] - 3, y + h / 2, GRAY, 3, 10)
    return svg(720, 225, body, min_width=560)


def architecture():
    body = ""
    body += rect(255, 8, 210, 82, FE_RED)
    body += t(360, 40, "🖥️ GUI (FE)", 17, "#fff", 800)
    body += t(360, 62, "YOU BUILD THIS", 12, "#FFE4E6", 700)
    body += rect(480, 12, 130, 34, "#9F1239", rx=10)
    body += t(545, 34, "Minimum", 13, "#fff", 700)
    body += rect(480, 52, 130, 34, "#9F1239", rx=10)
    body += t(545, 74, "Nice to have", 13, "#fff", 700)
    xs = [0, 270, 540]
    spec = [
        ("🚪", ["API", "the gate to the data"]),
        ("🧠", ["Main.py", "the brain"]),
        ("🤖", ["Gemini", "the AI"]),
    ]
    for (icon, arr), x in zip(spec, xs):
        body += node(x, 150, 180, 92, BE_BLUE, icon, arr, 12)
    body += rect(270, 300, 180, 70, BE_BLUE)
    body += t(360, 330, "📄 Excel", 16, "#fff", 800)
    body += t(360, 352, "data of 1000 startups", 12, "#fff", 600)
    body += arrow(300, 92, 150, 148, FE_RED, 3, 10)
    body += arrow(110, 148, 260, 94, FE_RED, 3, 10)
    body += arrow(184, 196, 266, 196, GRAY, 3, 10)
    body += arrow(266, 214, 184, 214, GRAY, 3, 10)
    body += arrow(454, 196, 536, 196, GRAY, 3, 10)
    body += arrow(536, 214, 454, 214, GRAY, 3, 10)
    body += arrow(360, 296, 360, 246, GRAY, 3, 10)
    body += rect(540, 290, 180, 78, "#F1F5F9", rx=12)
    body += rect(552, 302, 14, 14, FE_RED, rx=3)
    body += t(574, 314, "you build it", 12, INK, 700, "start")
    body += rect(552, 330, 14, 14, BE_BLUE, rx=3)
    body += t(574, 342, "already done", 12, INK, 700, "start")
    return svg(720, 376, body, min_width=560)


def scoring_flow():
    comps = example_components()
    body = ""
    heads = [(95, "Criterion"), (315, "Points, 0 to 100"), (487, "Importance"), (652, "Result")]
    for x, s in heads:
        body += t(x, 22, s, 12, GRAY, 700)
    tx, ty, tw, th = 585, 130, 135, 150
    for i, (key, name, icon, col) in enumerate(METRICS):
        y = 42 + i * 58
        body += rect(0, y, 190, 44, col)
        body += f'<text x="14" y="{y + 30}" font-size="20">{icon}</text>'
        body += t(46, y + 28, name, 15, "#fff", 700, "start")
        body += arrow(194, y + 22, 228, y + 22, GRAY, 2.5, 9)
        body += rect(236, y + 12, 160, 20, "#E2E8F0", rx=10)
        body += rect(236, y + 12, max(8, 160 * comps[key] / 100), 20, col, rx=10)
        body += t(406, y + 28, f"{round(comps[key])}", 15, col, 800, "start")
        body += rect(445, y + 4, 84, 36, "#fff", col, rx=18, sw=3)
        body += t(487, y + 28, f"× {DEFAULT_WEIGHTS[key]}%", 15, col, 800)
        body += arrow(533, y + 22, tx - 4, ty + th / 2 + (y + 22 - (ty + th / 2)) * 0.25, col, 2.5, 9)
    body += rect(tx, ty, tw, th, NAVY)
    body += f'<text x="{tx + tw / 2}" y="{ty + 50}" font-size="34" text-anchor="middle">🎯</text>'
    body += lines(tx + tw / 2, ty + 80, ["Total score"], 15, "#fff", 700)
    body += t(tx + tw / 2, ty + 120, f"{num(example_score())} / 100", 22, "#FDE047", 800)
    return svg(720, 396, body, min_width=560)


def donut():
    cx = cy = 110
    r = 72
    circ = 2 * math.pi * r
    off = 0.0
    body = ""
    for key, name, icon, col in METRICS:
        length = circ * DEFAULT_WEIGHTS[key] / 100
        body += (
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="36" '
            f'stroke-dasharray="{r1(length - 3)} {r1(circ - length + 3)}" stroke-dashoffset="{r1(-off)}" '
            f'transform="rotate(-90 {cx} {cy})"/>'
        )
        mid = (off + length / 2) / circ * 2 * math.pi - math.pi / 2
        lx, ly = cx + r * math.cos(mid), cy + r * math.sin(mid)
        body += t(lx, ly + 5, f"{DEFAULT_WEIGHTS[key]}%", 14, "#fff", 800)
        off += length
    body += t(cx, cy - 2, "100%", 22, NAVY, 800)
    body += t(cx, cy + 20, "in total", 12, GRAY, 600)
    return svg(220, 220, body, cls="donut")


def risk_flow():
    body = ""
    body += rect(130, 0, 200, 40, NAVY, rx=20)
    body += t(230, 26, "🏢 One startup", 15, "#fff", 700)
    body += arrow(230, 42, 230, 66, GRAY, 3, 10)

    body += rect(0, 70, 470, 112, "#FEE2E2", RED, rx=14, sw=3)
    body += t(16, 94, "Is at least one of these true?", 15, RED, 800, "start")
    body += lines(16, 116, [
        "• its money lasts less than 6 months",
        "• it loses money AND burns over 30 M Ft a month",
        "• more than 9% of its customers leave",
    ], 13, INK, 500, 21, "start")
    body += arrow(472, 126, 546, 126, RED, 3, 10)
    body += t(509, 116, "YES", 12, RED, 800)
    body += rect(550, 90, 170, 72, RED)
    body += t(635, 120, "🔴 HIGH", 18, "#fff", 800)
    body += t(635, 144, "risk", 13, "#fff", 600)

    body += arrow(235, 184, 235, 214, GRAY, 3, 10)
    body += t(262, 205, "NO", 12, GRAY, 800)

    body += rect(0, 218, 470, 112, "#FEF3C7", YELLOW, rx=14, sw=3)
    body += t(16, 242, "Is at least one of these true?", 15, "#92400E", 800, "start")
    body += lines(16, 264, [
        "• its money lasts less than 12 months",
        "• it loses money",
        "• more than 6% of its customers leave",
    ], 13, INK, 500, 21, "start")
    body += arrow(472, 274, 546, 274, YELLOW, 3, 10)
    body += t(509, 264, "YES", 12, "#92400E", 800)
    body += rect(550, 238, 170, 72, "#F59E0B")
    body += t(635, 268, "🟡 MEDIUM", 18, "#fff", 800)
    body += t(635, 292, "risk", 13, "#fff", 600)

    body += arrow(235, 332, 235, 362, GRAY, 3, 10)
    body += t(262, 353, "NO", 12, GRAY, 800)
    body += rect(0, 366, 470, 52, GREEN)
    body += t(235, 398, "🟢 LOW risk", 18, "#fff", 800)
    return svg(720, 424, body, min_width=560)


PROFILES = [
    ("🛡️ Cautious investor", "“I want the company to survive.”", {"growth": 10, "ebitda": 20, "grossMargin": 10, "runway": 30, "retention": 25, "funding": 5}),
    ("🚀 Growth-hungry investor", "“I want the company to grow fast.”", {"growth": 45, "ebitda": 5, "grossMargin": 15, "runway": 10, "retention": 10, "funding": 15}),
]


def stacked(y, weights):
    x = 0.0
    out = ""
    for key, name, icon, col in METRICS:
        w = weights[key] * 7.2
        out += rect(x, y, w, 40, col, rx=0)
        out += t(x + w / 2, y + 26, f"{weights[key]}%", 14, "#fff", 800)
        x += w
    return out


def weight_profiles():
    body = ""
    ys = [38, 148]
    for (title, quote, weights), y in zip(PROFILES, ys):
        body += t(0, y - 16, title, 16, NAVY, 800, "start")
        body += t(720, y - 16, quote, 12, GRAY, 500, "end")
        body += f'<clipPath id="clip{y}"><rect x="0" y="{y}" width="720" height="40" rx="12"/></clipPath>'
        body += f'<g clip-path="url(#clip{y})">{stacked(y, weights)}</g>'
    body += arrow(360, 196, 360, 232, GRAY, 3, 10)
    body += rect(130, 238, 460, 50, NAVY, rx=25)
    body += t(360, 269, "Same 1000 companies, but the winner may differ! 🤔", 15, "#fff", 700)
    return svg(720, 300, body, min_width=560)


def window(title, inner, h=400):
    body = rect(1, 1, 348, h - 2, "#fff", LINE, rx=16, sw=2)
    body += f'<path d="M1 17 a16 16 0 0 1 16 -16 h316 a16 16 0 0 1 16 16 v14 h-348 z" fill="{NAVY}"/>'
    for i, c in enumerate(["#F87171", "#FBBF24", "#4ADE80"]):
        body += circle(18 + i * 16, 16, 5, c)
    body += t(175, 20, title, 12, "#fff", 700)
    return body + inner


def ranking_wireframe():
    inner = t(16, 58, "Set what matters most!", 12, INK, 700, "start")
    for i, (key, name, icon, col) in enumerate(METRICS):
        y = 78 + i * 28
        wv = DEFAULT_WEIGHTS[key]
        inner += t(16, y + 12, name, 11, INK, 600, "start")
        inner += rect(122, y + 4, 150, 7, "#E2E8F0", rx=4)
        inner += rect(122, y + 4, 150 * wv / 50, 7, col, rx=4)
        inner += circle(122 + 150 * wv / 50, y + 7.5, 8, "#fff", col, 3)
        inner += t(318, y + 12, f"{wv}%", 12, col, 800)
    inner += rect(16, 252, 130, 28, BLUE, rx=14)
    inner += t(81, 270, "Recalculate", 11, "#fff", 700)
    inner += t(16, 306, "Ranking", 12, INK, 700, "start")
    rows = [("1", "Company A", "82.4", "🟢"), ("2", "Company B", "79.1", "🟢"), ("3", "Company C", "76.8", "🟡")]
    for i, (n, name, score, risk) in enumerate(rows):
        y = 314 + i * 25
        inner += rect(16, y, 318, 22, "#F1F5F9" if i % 2 == 0 else "#fff", rx=6)
        inner += t(26, y + 15, n, 11, GRAY, 700, "start")
        inner += t(54, y + 15, name, 11, INK, 600, "start")
        inner += t(250, y + 15, score, 11, INK, 800, "end")
        inner += f'<text x="306" y="{y + 16}" font-size="11" text-anchor="middle">{risk}</text>'
    return svg(350, 400, window("Ranking", inner), cls="wire")


def chat_wireframe():
    inner = ""
    chips = [(16, 40, 90, "Top 5 startups"), (112, 40, 90, "Biggest risks"), (208, 40, 120, "Compare the best 3")]
    for x, y, w, s in chips:
        inner += rect(x, y, w, 20, "#EDE9FE", PURPLE, rx=10, sw=1.5)
        inner += t(x + w / 2, y + 14, s, 10, PURPLE, 700)
    inner += rect(110, 84, 224, 44, BLUE, rx=14)
    inner += lines(222, 102, ["Which are the 5 most", "promising startups?"], 11, "#fff", 600, 15)
    inner += rect(16, 140, 262, 82, "#F3E8FF", rx=14)
    inner += t(26, 158, "🤖", 14, INK, 600, "start")
    inner += lines(48, 160, ["Company A scored the most:", "it grows fast, few customers", "leave, and it has lots of cash.", "Its risk is low."], 11, INK, 500, 15, "start")
    inner += rect(180, 236, 154, 30, BLUE, rx=14)
    inner += t(257, 256, "Why is it number one?", 11, "#fff", 600)
    inner += rect(16, 278, 220, 44, "#F3E8FF", rx=14)
    inner += lines(26, 296, ["Because its score is the", "highest in the model."], 11, INK, 500, 15, "start")
    inner += rect(16, 358, 262, 30, "#fff", LINE, rx=15, sw=2)
    inner += t(30, 377, "Type your question here...", 11, "#94A3B8", 500, "start")
    inner += rect(286, 358, 48, 30, PURPLE, rx=15)
    inner += t(310, 378, "➤", 13, "#fff", 700)
    return svg(350, 400, window("AI assistant", inner), cls="wire")


def ai_flow():
    body = ""
    w, h = 170, 112
    xs = [0, 275, 550]
    spec = [(GREEN, "🧑‍🎓", ["You", "type a question"]), (BLUE, "💻", ["The program", "packs it up"]), (PURPLE, "🤖", ["Gemini AI", "reads and answers"])]
    for (col, icon, arr), x in zip(spec, xs):
        body += node(x, 8, w, h, col, icon, arr, 13)
    for i in range(2):
        x1 = xs[i] + w
        x2 = xs[i + 1]
        body += arrow(x1 + 4, 50, x2 - 4, 50, GRAY, 3, 10)
        body += arrow(x2 - 4, 92, x1 + 4, 92, PURPLE, 3, 10)
    body += t(xs[0] + w + 52, 42, "① question", 11, GRAY, 700)
    body += t(xs[1] + w + 52, 42, "② data + question", 11, GRAY, 700)
    body += t(xs[0] + w + 52, 112, "④ answer", 11, PURPLE, 700)
    body += t(xs[1] + w + 52, 112, "③ answer", 11, PURPLE, 700)
    body += rect(0, 140, 720, 40, "#F1F5F9", rx=20)
    body += t(360, 165, "The AI only sees what the program sends it: the data of the 1000 startups and your question.", 12, INK, 600)
    return svg(720, 190, body, min_width=560)


def split_name(name):
    if len(name) <= 11 or " " not in name:
        return [name]
    first, second = name.split(" ", 1)
    return [first, second]


def team_chart():
    body = ""
    mx, mw, mh = 215, 290, 58
    body += rect(mx, 0, mw, mh, NAVY)
    body += t(mx + mw / 2, 26, "🏢 Your small company", 17, "#fff", 800)
    body += t(mx + mw / 2, 46, "6 people, 6 roles, 1 product", 12, "#CBD5E1", 600)
    names = [
        ("Lead developer", "The working GUI"),
        ("Analyst", "Skill and the facts"),
        ("Designer", "Look and slides"),
        ("Sales leader", "Price and the ask"),
        ("Marketing leader", "Brand and story"),
        ("Joker", "You decide!"),
    ]
    w, gap, y, h = 108, 14, 118, 86
    bus = 90
    body += f'<line x1="{mx + mw / 2}" y1="{mh}" x2="{mx + mw / 2}" y2="{bus}" stroke="{GRAY}" stroke-width="3"/>'
    body += f'<line x1="{w / 2}" y1="{bus}" x2="{5 * (w + gap) + w / 2}" y2="{bus}" stroke="{GRAY}" stroke-width="3"/>'
    for i, (name, out) in enumerate(names):
        x = i * (w + gap)
        icon, col = ROLES[name]
        body += f'<line x1="{x + w / 2}" y1="{bus}" x2="{x + w / 2}" y2="{y}" stroke="{GRAY}" stroke-width="3"/>'
        if name == "Lead developer":
            body += rect(x, y, w, h, col, "#FDE047", rx=14, sw=4)
        elif name == "Joker":
            body += rect(x, y, w, h, col, "#E9D5FF", rx=14, sw=4)
        else:
            body += rect(x, y, w, h, col, rx=14)
        body += f'<text x="{x + w / 2}" y="{y + 34}" font-size="26" text-anchor="middle">{icon}</text>'
        parts = split_name(name)
        if len(parts) == 1:
            body += t(x + w / 2, y + 62, name, 13, "#fff", 700)
        else:
            body += lines(x + w / 2, y + 54, parts, 12.5, "#fff", 700, 14)
        body += rect(x, y + h + 10, w, 26, col, rx=13, opacity=0.14)
        body += t(x + w / 2, y + h + 27, out, 10.5, col, 700)
    return svg(720, 248, body, min_width=600)


def team_flow():
    spec = [
        ("🔍", ["Facts and", "specs"], "Analyst", BLUE),
        ("🎨", ["Design"], "Designer", PINK),
        ("💻", ["Build"], "Lead developer", FE_RED),
        ("📣", ["Brand and", "story"], "Marketing leader", ORANGE),
        ("💼", ["Price and", "the ask"], "Sales leader", GREEN),
        ("🎤", ["Pitch"], "Whole team", NAVY),
    ]
    body = ""
    w, gap, y, h = 105, 18, 24, 100
    for i, (icon, arr, role, col) in enumerate(spec):
        x = i * (w + gap)
        body += node(x, y, w, h, col, icon, arr, 13)
        body += badge(x + 12, y + 4, i + 1, col)
        body += rect(x, y + h + 12, w, 28, col, rx=14, opacity=0.14)
        body += t(x + w / 2, y + h + 31, role, 11, col, 700)
        if i < 5:
            body += arrow(x + w + 2, y + h / 2, x + w + gap - 2, y + h / 2, GRAY, 2.5, 8)
    body += rect(0, 178, 720, 34, PURPLE, rx=17, opacity=0.16)
    body += t(360, 200, "🃏 Joker: helps wherever the team needs it most. You choose where!", 12, "#5B21B6", 700)
    return svg(720, 222, body, min_width=600)


def timeline():
    body = ""
    blocks = [
        ("Block 1 · 80 minutes · Build the product", 24, [
            (10, "Kick-off", NAVY), (15, "Plan + design", BLUE), (25, "Build minimum", FE_RED), (15, "Nice to have", PURPLE), (15, "Test + polish", GREEN)]),
        ("Block 2 · 80 minutes · Prepare and give the pitch", 118, [
            (10, "Story", ORANGE), (30, "Build the slides", PINK), (15, "Rehearsal", PURPLE), (25, "Pitches", GREEN)]),
    ]
    for title, y, segs in blocks:
        body += t(0, y - 8, title, 15, NAVY, 800, "start")
        x = 0.0
        body += f'<clipPath id="tl{y}"><rect x="0" y="{y}" width="720" height="52" rx="14"/></clipPath><g clip-path="url(#tl{y})">'
        for mins, name, col in segs:
            w = mins * 9
            body += rect(x + 1, y, w - 2, 52, col, rx=0)
            body += t(x + w / 2, y + 22, f"{mins} min", 14, "#fff", 800)
            body += t(x + w / 2, y + 40, name, 10 if mins < 15 else 11.5, "#fff", 600)
            x += w
        body += "</g>"
    body += t(0, 200, "0 min", 11, GRAY, 600, "start")
    body += t(720, 200, "80 min", 11, GRAY, 600, "end")
    return svg(720, 208, body, min_width=560)


def presentation_flow():
    spec = [
        ("1", "The problem", "and our team", BLUE),
        ("2", "Our product", "(live demo)", TEAL),
        ("3", "Proof: the", "winner we found", GREEN),
        ("4", "Business", "and the ask", ORANGE),
        ("5", "Risks and", "what we learned", PURPLE),
    ]
    body = ""
    w, gap = 120, 30
    for i, (n, a, b, col) in enumerate(spec):
        x = i * (w + gap)
        body += rect(x, 10, w, 120, "#fff", col, rx=12, sw=3)
        body += f'<path d="M{x} 22 a12 12 0 0 1 12 -12 h{w - 24} a12 12 0 0 1 12 12 v18 h-{w} z" fill="{col}"/>'
        body += t(x + w / 2, 33, f"Slide {n}", 13, "#fff", 800)
        body += lines(x + w / 2, 76, [a, b], 12.5, col, 800, 18)
        body += rect(x + 22, 100, w - 44, 6, col, rx=3, opacity=0.35)
        body += rect(x + 22, 112, w - 70, 6, col, rx=3, opacity=0.2)
        if i < 4:
            body += arrow(x + w + 3, 70, x + w + gap - 3, 70, GRAY, 3, 10)
    return svg(720, 140, body, min_width=560)


def product_parts():
    body = ""
    cards = [
        (0, FE_RED, "🖥️", ["GUI", "what people see and click"]),
        (250, TEAL, "🧩", ["Skill", "a saved recipe for the AI"]),
        (500, ORANGE, "🦾", ["Agent", "an AI helper that works alone"]),
    ]
    body += t(0, 22, "🚀 YOUR PRODUCT has three parts", 15, NAVY, 800, "start")
    for x, col, icon, arr in cards:
        body += node(x, 36, 220, 120, col, icon, arr, 13)
    body += rect(0, 206, 230, 52, BE_BLUE)
    body += t(115, 228, "🔌 Ready for you", 13, "#fff", 800)
    body += t(115, 246, "API, Main.py, Excel", 11.5, "#DBEAFE", 600)
    body += rect(250, 206, 470, 52, PURPLE)
    body += t(485, 228, "🤖 Gemini", 13, "#fff", 800)
    body += t(485, 246, "the AI brain behind your skill and your agent", 11.5, "#EDE9FE", 600)
    body += arrow(110, 158, 110, 202, FE_RED, 3, 10)
    body += arrow(360, 158, 360, 202, TEAL, 3, 10)
    body += arrow(610, 158, 610, 202, ORANGE, 3, 10)
    body += arrow(360, 262, 360, 290, GRAY, 3, 10)
    body += rect(0, 294, 720, 40, GREEN, rx=20)
    body += t(360, 320, "🏦 Then you sell it to the investors", 15, "#fff", 800)
    return svg(720, 342, body, min_width=560)


def fund_stages():
    spec = [("Pre-seed", 205, "#93C5FD"), ("Seed", 320, "#60A5FA"), ("Series A", 285, "#3B82F6"), ("Series B", 136, "#2563EB"), ("Series C", 54, "#1E40AF")]
    body = ""
    w = 138
    for i, (name, count, col) in enumerate(spec):
        x = i * (w - 6)
        body += f'<polygon points="{x},0 {x + w - 16},0 {x + w},28 {x + w - 16},56 {x},56 {x + 16},28" fill="{col}"/>'
        body += t(x + w / 2 + 2, 24, name, 13, "#fff", 800)
        body += t(x + w / 2 + 2, 42, f"{count} companies", 11, "#fff", 600)
    return svg(720, 60, body, min_width=560)


def hero():
    body = ""
    bars = [(60, 150, "#60A5FA", "🥈"), (140, 200, "#FBBF24", "🥇"), (220, 110, "#F97316", "🥉")]
    for x, h, col, medal in bars:
        body += rect(x, 280 - h, 70, h, col, rx=10)
        body += f'<text x="{x + 35}" y="{280 - h - 10}" font-size="34" text-anchor="middle">{medal}</text>'
    body += rect(30, 280, 280, 8, "#fff", rx=4, opacity=0.5)
    for cx, cy, r, o in [(40, 60, 20, 0.5), (320, 90, 14, 0.4), (300, 30, 8, 0.6)]:
        body += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" fill-opacity="{o}"/>'
    return svg(350, 300, body, cls="wire")
