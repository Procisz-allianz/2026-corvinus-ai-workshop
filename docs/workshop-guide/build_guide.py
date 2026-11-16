import pathlib
import subprocess
import sys

import diagrams as d

HERE = pathlib.Path(__file__).resolve().parent
HTML_FILE = HERE / "guide.html"
PDF_FILE = HERE.parent / "Startup_Intelligence_Workshop_Guide.pdf"
TOTAL_PAGES = 12

BROWSER_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
]

CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
html, body { margin: 0; padding: 0; background: #fff; }
body { font-family: "Segoe UI", "Segoe UI Emoji", system-ui, Arial, sans-serif; color: #1E293B; font-size: 12.5px; line-height: 1.5; }
.page { width: 210mm; height: 297mm; padding: 13mm 15mm 15mm; position: relative; overflow: hidden; page-break-after: always; background: #fff; }
.page:last-child { page-break-after: auto; }
.top { display: flex; align-items: center; gap: 12px; margin-bottom: 10px; }
.top .pn { width: 38px; height: 38px; border-radius: 50%; background: #0B2A5B; color: #fff; font-weight: 800; font-size: 19px; display: flex; align-items: center; justify-content: center; flex: none; }
.top h2 { margin: 0; font-size: 25px; color: #0B2A5B; font-weight: 800; letter-spacing: -0.3px; }
.foot { position: absolute; left: 15mm; right: 15mm; bottom: 7mm; display: flex; justify-content: space-between; gap: 10px; font-size: 10px; color: #64748B; border-top: 1px solid #E2E8F0; padding-top: 5px; }
p { margin: 0 0 8px; }
h3 { margin: 14px 0 6px; font-size: 15px; color: #0B2A5B; font-weight: 800; }
.lead { font-size: 14px; color: #334155; }
.note { font-size: 12.3px; color: #475569; }
.quote { background: linear-gradient(90deg, #0B2A5B, #2563EB); color: #fff; border-radius: 14px; padding: 14px 20px; font-size: 20px; font-weight: 800; text-align: center; margin: 10px 0 12px; }
.callout { border-radius: 12px; padding: 10px 14px; margin: 10px 0; border-left: 6px solid; font-size: 12.5px; }
.callout.green { background: #DCFCE7; border-color: #16A34A; }
.callout.blue { background: #DBEAFE; border-color: #2563EB; }
.callout.yellow { background: #FEF3C7; border-color: #F59E0B; }
.callout.red { background: #FEE2E2; border-color: #DC2626; }
.callout.purple { background: #EDE9FE; border-color: #7C3AED; }
.callout b.t { display: block; font-size: 13.5px; margin-bottom: 2px; }
.grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.grid3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; }
.card { border-radius: 12px; padding: 10px 12px; border: 2px solid #E2E8F0; background: #fff; }
.card h4 { margin: 0 0 3px; font-size: 14px; font-weight: 800; }
.card p { margin: 0; font-size: 12px; color: #334155; }
.mcard { border-radius: 12px; padding: 10px 12px; color: #1E293B; border-left: 8px solid; }
.mcard h4 { margin: 0 0 3px; font-size: 14.5px; font-weight: 800; }
.mcard p { margin: 0; font-size: 12px; }
.mcard .ex { margin-top: 4px; font-size: 11.5px; font-style: italic; color: #475569; }
.step { display: flex; gap: 10px; align-items: flex-start; margin-bottom: 7px; }
.step .n { flex: none; width: 26px; height: 26px; border-radius: 50%; color: #fff; font-weight: 800; display: flex; align-items: center; justify-content: center; font-size: 13px; }
.tbl { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; font-size: 12px; }
th { text-align: left; background: #0B2A5B; color: #fff; padding: 5px 8px; font-weight: 700; }
th:first-child { border-radius: 8px 0 0 8px; }
th:last-child { border-radius: 0 8px 8px 0; }
td { padding: 5px 8px; border-bottom: 1px solid #E2E8F0; vertical-align: top; }
.dot { display: inline-block; width: 11px; height: 11px; border-radius: 50%; margin-right: 6px; vertical-align: -1px; }
.phase { border-radius: 14px; border: 3px solid; padding: 8px 12px; margin-bottom: 8px; }
.phase .mh { display: flex; align-items: center; gap: 10px; margin-bottom: 4px; }
.phase .mh .mn { width: 28px; height: 28px; border-radius: 50%; color: #fff; font-weight: 800; display: flex; align-items: center; justify-content: center; font-size: 14px; flex: none; }
.phase .mh b { font-size: 14.5px; font-weight: 800; }
.phase .mh span.min { margin-left: auto; font-size: 11.5px; font-weight: 800; padding: 2px 10px; border-radius: 99px; color: #fff; white-space: nowrap; }
.phase ul { list-style: none; margin: 0; padding: 0; }
.phase li { margin: 3px 0; font-size: 12px; display: flex; gap: 8px; align-items: baseline; }
.phase li .r { flex: none; min-width: 140px; }
.rchip { display: inline-block; padding: 1px 9px; border-radius: 99px; color: #fff; font-weight: 700; font-size: 11px; white-space: nowrap; }
.role { border-radius: 12px; padding: 7px 11px; color: #fff; }
.role b { display: block; font-size: 14px; }
.role .what { font-size: 11.2px; line-height: 1.4; opacity: 0.96; }
.role .ai { font-size: 11px; margin-top: 3px; background: rgba(255,255,255,0.18); border-radius: 8px; padding: 2px 8px; }
.cover { padding: 0; background: linear-gradient(160deg, #0B2A5B 0%, #1D4ED8 55%, #7C3AED 100%); color: #fff; }
.cover .inner { padding: 22mm 18mm 12mm; }
.cover .tag { display: inline-block; background: rgba(255,255,255,0.18); border-radius: 99px; padding: 5px 16px; font-weight: 700; font-size: 13px; letter-spacing: 0.5px; }
.cover h1 { font-size: 54px; line-height: 1.02; margin: 18px 0 10px; font-weight: 900; letter-spacing: -1.5px; }
.cover .sub { font-size: 20px; max-width: 135mm; font-weight: 500; color: #E0E7FF; }
.cover .chips { margin-top: 20px; }
.cover .chips span { display: inline-block; background: #fff; color: #0B2A5B; font-weight: 800; padding: 6px 16px; border-radius: 99px; margin: 0 8px 8px 0; font-size: 13.5px; }
.cover .hero { position: absolute; right: 12mm; top: 92mm; width: 100mm; }
.cover .toc { position: absolute; left: 18mm; right: 18mm; bottom: 14mm; background: rgba(255,255,255,0.95); color: #1E293B; border-radius: 18px; padding: 14px 20px; }
.cover .toc h3 { margin: 0 0 8px; color: #0B2A5B; }
.cover .toc ol { margin: 0; padding: 0; list-style: none; display: grid; grid-template-columns: 1fr 1fr; gap: 4px 20px; font-size: 12.5px; }
.cover .toc li { display: flex; gap: 8px; align-items: center; }
.cover .toc li i { width: 22px; height: 22px; border-radius: 50%; color: #fff; font-style: normal; font-weight: 800; font-size: 11.5px; display: flex; align-items: center; justify-content: center; flex: none; }
.dia { overflow-x: auto; max-width: 100%; }
.grid2 > *, .grid3 > *, .two > *, .sidebyside > * { min-width: 0; }
svg { display: block; width: 100%; height: auto; }
svg.donut { max-width: 250px; margin: 0 auto; }
.legend { display: flex; flex-wrap: wrap; gap: 4px 14px; font-size: 11.5px; margin-top: 6px; }
.legend-dot { display: inline-flex; align-items: center; gap: 5px; }
.two { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.sidebyside { display: grid; grid-template-columns: 250px 1fr; gap: 14px; align-items: center; }
.levels { border-radius: 14px; overflow: hidden; border: 3px solid; }
.levels .lh { color: #fff; padding: 7px 14px; font-weight: 800; font-size: 15px; }
.levels ul { list-style: none; margin: 0; padding: 8px 14px; }
.levels li { margin: 4px 0; }
.bubble { background: #EDE9FE; border: 2px solid #7C3AED; border-radius: 14px 14px 14px 2px; padding: 6px 12px; font-size: 12.3px; font-weight: 600; color: #4C1D95; }
.cardhead { background: #0B2A5B; color: #fff; padding: 8px 14px; font-weight: 800; font-size: 14px; display: flex; justify-content: space-between; gap: 8px; flex-wrap: wrap; }
.cardcell { padding: 8px 14px; }

@media screen {
  body { background: #E2E8F0; }
  .page { width: auto; max-width: 980px; height: auto; margin: 18px auto; padding: 30px 36px 18px; overflow: visible; border-radius: 18px; box-shadow: 0 4px 24px rgba(15, 23, 42, 0.12); }
  .foot { position: static; margin-top: 26px; }
  .cover .inner { padding: 46px 40px 8px; }
  .cover .hero { position: static; width: 280px; max-width: 80%; margin: 8px auto 0; }
  .cover .toc { position: static; margin: 22px 40px 40px; }
  .grid3 .cardcell + .cardcell { border-left: 1px solid #E2E8F0; }
}

@media screen and (max-width: 820px) {
  .grid3 { grid-template-columns: 1fr 1fr; }
}

@media screen and (max-width: 640px) {
  body { font-size: 14px; overflow-x: hidden; }
  .page { margin: 0 0 10px; border-radius: 0; padding: 20px 16px 14px; }
  .grid2, .grid3, .two, .sidebyside { grid-template-columns: 1fr; }
  .grid3 .cardcell + .cardcell { border-left: none; border-top: 1px solid #E2E8F0; }
  .top h2 { font-size: 21px; }
  .top .pn { width: 32px; height: 32px; font-size: 16px; }
  .lead { font-size: 15px; }
  .quote { font-size: 17px; }
  .cover .inner { padding: 30px 18px 4px; }
  .cover h1 { font-size: 40px; }
  .cover .sub { font-size: 17px; }
  .cover .toc { margin: 18px 14px 26px; }
  .cover .toc ol { grid-template-columns: 1fr; }
  .phase li { flex-direction: column; gap: 2px; }
  .phase .mh { flex-wrap: wrap; }
  .foot { flex-direction: column; gap: 2px; }
  .dia svg:not(.donut):not(.wire) { min-width: 600px; }
  div[style*="width:88%"], div[style*="width:80%"] { width: 100% !important; }
  td, th { padding: 5px 6px; }
}
"""


def foot(n):
    return f'<div class="foot"><span>Startup Intelligence · Corvinus AI workshop · Day 3</span><span>{n} / {TOTAL_PAGES}</span></div>'


def page(n, title, body):
    return f'<section class="page"><div class="top"><div class="pn">{n - 1}</div><h2>{title}</h2></div>{body}{foot(n)}</section>'


def chip(role):
    icon, col = d.ROLES[role]
    return f'<span class="rchip" style="background:{col}">{icon} {role}</span>'


def cover():
    toc_items = [
        ("What is the task?", "#2563EB"),
        ("What is in the Excel file?", "#0D9488"),
        ("How the program scores", "#16A34A"),
        ("Risk and weights", "#EA580C"),
        ("The web page you build", "#DB2777"),
        ("The role of the AI", "#7C3AED"),
        ("Your small company: roles", "#0B2A5B"),
        ("Your mission, phase by phase", "#2563EB"),
        ("Time plan and teamwork", "#0D9488"),
        ("The presentation", "#16A34A"),
        ("Good to know and glossary", "#EA580C"),
    ]
    toc = "".join(f'<li><i style="background:{c}">{i + 1}</i>{name}</li>' for i, (name, c) in enumerate(toc_items))
    return f"""
<section class="page cover">
  <div class="inner">
    <span class="tag">CORVINUS AI SEMINAR · DAY 3 · WORKSHOP</span>
    <h1>Startup<br>Intelligence</h1>
    <div class="sub">Let us find the most promising startup with the help of artificial intelligence!</div>
    <div class="chips"><span>⏱️ 2 × 80 minutes</span><span>👥 Teams of 5-7 people</span><span>🏢 You are a small company</span></div>
  </div>
  <div class="hero">{d.hero()}</div>
  <div class="toc">
    <h3>📖 Everything you need to get started is in this guide</h3>
    <ol>{toc}</ol>
  </div>
</section>"""


def page_task():
    body = f"""
<p class="lead">Imagine that your team is a <b>small company that advises investors</b>. You received a big Excel table with the data of <b>1000 young companies</b>. Your company has one single question to answer:</p>
<div class="quote">Which startup deserves our trust the most?</div>
<div class="grid2">
  <div class="callout blue"><b class="t">🌱 What is a startup?</b>A newly founded business that wants to grow fast. It often spends a lot of money before it makes a profit, so it is hard to tell which one will succeed.</div>
  <div class="callout yellow"><b class="t">🎭 Every company is made up!</b>The numbers are artificial. Nothing real is at stake, but the way of thinking is the same as in real life.</div>
</div>
<h3>🗺️ The road from the Excel table to the decision</h3>
{d.big_picture()}
<h3>🧩 What is already done, and what do you build?</h3>
<div style="width:88%;margin:0 auto">{d.architecture()}</div>
<div class="callout green" style="margin-top:10px"><b class="t">🏁 Your job is the web page!</b>The blue parts (reading the data, scoring, the connection to the AI) are <b>already done</b>. Your company builds the <b>red web page</b> through which everything can be used. Then you decide which startup is the best, and you present it. <b>Only one person in your team writes the page (with the AI's help): the developer.</b> Everyone else has a different job. See page 8.</div>"""
    return page(2, "What is the task?", body)


def metric_card(name, icon, color, bg, what, example):
    return f'<div class="mcard" style="background:{bg};border-color:{color}"><h4 style="color:{color}">{icon} {name}</h4><p>{what}</p><div class="ex">{example}</div></div>'


def page_data():
    cards = [
        ("Growth", "📈", d.GREEN, "#DCFCE7", "How much did the revenue of the company grow compared to last year?", "Like a snack bar whose sales grew by half in one year."),
        ("Profitability (EBITDA margin)", "💰", d.BLUE, "#DBEAFE", "If the company takes in 100 forints, how much is left after the running costs? If it is negative, the company loses money.", "Like your monthly pocket money: income minus spending."),
        ("Gross margin", "🧾", d.TEAL, "#CCFBF1", "From a product sold for 100 forints, how much is left after the cost of making it?", "Lemonade: sold for 100 Ft, ingredients cost 30 Ft, so the margin is 70%."),
        ("Runway", "⏳", d.ORANGE, "#FFEDD5", "For how many months can the company live on its current cash, if no more money came in?", "Like the battery of your phone: how many hours are left?"),
        ("Customer loyalty", "🤝", d.PINK, "#FCE7F3", "What share of the customers stays? The Excel shows the churn (customers who leave): the lower, the better.", "Like the regulars of a cafe: how many come back?"),
        ("Funding", "🏦", d.PURPLE, "#EDE9FE", "How much money have investors trusted the company with so far?", "If many people gave money, they probably believe in it."),
    ]
    mc = "".join(metric_card(*c) for c in cards)
    body = f"""
<p class="lead">The Excel file contains <b>23 data points</b> about every startup. This is the data card of one company. Money amounts are in <b>millions of forints</b> (written M Ft).</p>
<div class="card" style="border-color:#0B2A5B;padding:0;overflow:hidden">
  <div class="cardhead"><span>🏢 Green Labs 0001 (ST0001)</span><span style="font-weight:600">AI / SaaS · Vienna · founded 2025 · Seed stage</span></div>
  <div class="grid3" style="gap:0">
    <div class="cardcell"><b style="color:#2563EB">👥 People</b><br>38 employees<br>24,172 customers</div>
    <div class="cardcell"><b style="color:#16A34A">💶 Revenue</b><br>2023: 21.1 · 2024: 40.0<br>2025: 67.8 (growth: +69.5%)</div>
    <div class="cardcell"><b style="color:#EA580C">📉 Money</b><br>Cash: 397.3 · monthly burn: 25.3<br>Loss (EBITDA): -28.9</div>
  </div>
</div>
<p class="note" style="margin-top:6px">The column names in the Excel file and the existing app screens are in Hungarian. The meaning is the same as in this guide.</p>
<h3>🔑 The six most important criteria, in simple words</h3>
<div class="grid2">{mc}</div>
<h3>🪜 The maturity of a company: funding stages</h3>
<p class="note" style="margin-bottom:6px">Like school grades: the further right, the more mature the company. This is how the 1000 startups are spread out:</p>
{d.fund_stages()}
<p style="font-size:11.5px;color:#64748B;margin-top:6px">The companies work in 10 fields, for example EdTech (education), HealthTech, FinTech (finance), AgriTech (farming), CleanTech and ClimateTech (environment), Cybersecurity, Logistics, E-commerce (web shops) and AI / SaaS (software).</p>"""
    return page(3, "What is in the Excel file?", body)


def page_scoring():
    comps = d.example_components()
    rows = ""
    total = 0.0
    for key, name, icon, col in d.METRICS:
        w = d.DEFAULT_WEIGHTS[key]
        part = comps[key] * w / 100
        total += part
        rows += f'<tr><td><span class="dot" style="background:{col}"></span><b>{name}</b></td><td>{d.num(comps[key])}</td><td>× {w}%</td><td><b>{d.num(part)}</b></td></tr>'
    rows += f'<tr><td colspan="3"><b>Total score</b></td><td><b style="color:#0B2A5B;font-size:14px">{d.num(total)} / 100</b></td></tr>'
    legend = "".join(
        f'<div class="legend-dot"><span class="dot" style="background:{col}"></span><b>{name}</b></div>' for _, name, _, col in d.METRICS
    )
    body = f"""
<p class="lead">The program gives every startup a <b>score between 0 and 100</b>. It works like a school report: several subjects make up the average, and some subjects count more than others.</p>
<div class="step"><div class="n" style="background:#2563EB">1</div><div><b>Points.</b> Each of the six criteria gets 0 to 100 points. The better the company is at it, the more points.</div></div>
<div class="step"><div class="n" style="background:#EA580C">2</div><div><b>Weight.</b> Not every criterion is equally important. Growth is worth 25%, customer loyalty only 10%.</div></div>
<div class="step"><div class="n" style="background:#16A34A">3</div><div><b>Adding up.</b> We add up the weighted points. This is the total score of the company.</div></div>
<h3>🧮 How one score is made (example: Green Labs 0001)</h3>
{d.scoring_flow()}
<div class="sidebyside" style="margin-top:6px">
  <div>{d.donut()}<div class="legend" style="justify-content:center">{legend}</div></div>
  <div>
    <h3 style="margin-top:0">🍰 The default weights</h3>
    <p style="font-size:12px">The circle shows how important the program considers each criterion by default. <b>You can change this!</b></p>
    <div class="tbl"><table>
      <tr><th>Criterion</th><th>Points</th><th>Weight</th><th>Result</th></tr>
      {rows}
    </table></div>
  </div>
</div>"""
    return page(4, "How the program scores", body)


def page_risk():
    legend = "".join(f'<div class="legend-dot"><span class="dot" style="background:{col}"></span>{name}</div>' for _, name, _, col in d.METRICS)
    body = f"""
<p class="lead">Next to the score, the program shows a <b>traffic light</b> for every company. It tells how likely the company is to get into trouble. Like a real traffic light: red, yellow or green.</p>
{d.risk_flow()}
<div class="callout blue" style="margin-top:8px"><b class="t">💡 Why does this matter?</b>A company can have a high score and still a red light. For a good decision, look at both.</div>
<h3>🎚️ What happens if you change the weights?</h3>
<p class="note">Two different investors judge the same 1000 companies differently. These two profiles are only ideas: you can choose your own.</p>
{d.weight_profiles()}
<div class="legend">{legend}</div>"""
    return page(5, "Risk and weights", body)


def page_app():
    mins = [
        "📥 <b>Excel upload:</b> a button that loads the 1000 startups.",
        "🏆 <b>Ranking:</b> a table with each company's name, score and risk light.",
        "🤖 <b>Ask the AI:</b> a text box where you type a question and the answer appears.",
    ]
    nices = [
        "🎚️ <b>Weight sliders:</b> set what matters most and recalculate the ranking.",
        "⇄ <b>Comparison:</b> two startups side by side.",
        "📊 <b>Charts:</b> revenue, sectors or the top 5.",
        "🚦 <b>Colored risk light:</b> red, yellow, green in the table.",
        "🔎 <b>Search and filter:</b> by company or by sector.",
        "✨ <b>Good looks:</b> colors, cards, your own style.",
    ]
    mh = "".join(f'<li>{m}</li>' for m in mins)
    nh = "".join(f'<li>{m}</li>' for m in nices)
    body = f"""
<p class="lead">The web page is what people see and use: buttons, tables, sliders. It has two levels: what is <b>a must</b>, and what is <b>nice if there is time</b>.</p>
<div class="two">
  <div class="levels" style="border-color:#E11D48"><div class="lh" style="background:#E11D48">🔴 Minimum: this must work</div><ul>{mh}</ul></div>
  <div class="levels" style="border-color:#7C3AED"><div class="lh" style="background:#7C3AED">⭐ Nice to have: if time remains</div><ul style="font-size:12px">{nh}</ul></div>
</div>
<h3>🖼️ An idea of how it could look (two example screens)</h3>
<div class="two">
  <div>{d.ranking_wireframe()}<p style="text-align:center;font-size:11.5px;color:#475569;margin-top:4px"><b>Ranking:</b> sliders and a table</p></div>
  <div>{d.chat_wireframe()}<p style="text-align:center;font-size:11.5px;color:#475569;margin-top:4px"><b>Ask the AI:</b> question and answer</p></div>
</div>
<div class="callout yellow" style="margin-top:10px"><b class="t">📌 This is only an idea, not a rule</b>The drawings are examples. Feel free to invent your own layout, colors and title!</div>
<div class="callout blue"><b class="t">🔌 How does the web page get the data?</b>The back end offers "gates" (API): one accepts the Excel file, another gives the ranking, a third answers questions for the AI. After the start you find the list of gates in the browser at the <b>/docs</b> address. <b>The developer gives this page to the AI</b> and asks it to write the web page for it.</div>"""
    return page(6, "The web page you build", body)


def page_ai():
    qs = [
        "Which are the 5 most promising startups?",
        "Which companies have the highest financial risk?",
        "Compare the best three companies!",
        "Why did the best company get the first place?",
        "In which sector are the most stable companies?",
        "Whom would you recommend to a cautious investor?",
    ]
    qh = "".join(f'<div class="bubble">💬 {q}</div>' for q in qs)
    body = f"""
<p class="lead">The AI is a <b>language model</b> (Google Gemini). It is like a very fast, well-read colleague: it reads the data of the 1000 startups and answers your questions. The question box of your web page reaches it.</p>
<h3>🔄 What happens when you ask a question?</h3>
{d.ai_flow()}
<div class="grid2" style="margin-top:10px">
  <div class="callout blue"><b class="t">🧮 The program calculates</b>The ranking and the scores are calculated by the program, always the same way. This is not done by the AI.</div>
  <div class="callout purple"><b class="t">🗣️ The AI explains</b>The AI interprets the result, gives reasons, compares and answers your questions.</div>
</div>
<h3>💬 Questions to start with</h3>
<div class="grid2" style="gap:7px">{qh}</div>
<p class="note" style="margin-top:6px">A good question is <b>specific</b>. Do not only ask "What is the best?", also ask "Why?" and "What could be wrong with it?". By default the AI answers in Hungarian, ask your trainer if you need English.</p>
<div class="grid2" style="margin-top:8px">
  <div class="card" style="border-color:#16A34A"><h4 style="color:#16A34A">👍 It is good at</h4><p>Summarizing quickly, explaining, comparing, giving ideas and writing in a simple way.</p></div>
  <div class="card" style="border-color:#DC2626"><h4 style="color:#DC2626">⚠️ Be careful!</h4><p>The AI <b>can be wrong</b> and say a wrong thing with confidence. Always check every important number in the table!</p></div>
</div>
<div class="callout yellow" style="margin-top:10px"><b class="t">🔑 The AI needs a secret key</b>The trainer tells you how to set up a key. It is like a password: do not share it, and never put it on a slide!</div>"""
    return page(7, "The role of the AI", body)


def role_card(name, what, ai):
    icon, col = d.ROLES[name]
    return f'<div class="role" style="background:{col}"><b>{icon} {name}</b><div class="what">{what}</div><div class="ai">🤖 With AI: {ai}</div></div>'


def page_roles():
    cards = [
        role_card("Manager", "Sets goals and deadlines, keeps time, removes blockers and makes the final call.", "asks for a plan and a checklist"),
        role_card("Developer", "The ONLY person who builds the page. Works from the spec and design. No coding skills needed: you describe, the AI writes.", "builds the page, pastes errors to fix them"),
        role_card("Spec writer", "Turns ideas into clear written requirements: minimum first, then nice-to-haves. Answers the developer.", "drafts and sharpens the requirements"),
        role_card("Designer", "Sketches the layout, picks colors and style, reviews the result, later designs the slides.", "asks for layout and color ideas"),
        role_card("Financial analyst", "Understands the criteria, picks the investor profile and weights, finds the winner, judges risks.", "asks the startup questions in the app"),
        role_card("Tester", "Writes a checklist from the spec, tests the page, reports bugs, checks the AI's claims.", "turns the spec into a checklist"),
        role_card("Presenter", "Builds the story, speaks for the team and turns everyone's results into a pitch.", "suggests slide texts and titles"),
    ]
    own = '<div class="role" style="background:#F1F5F9;color:#334155;border:2px dashed #94A3B8"><b>✨ Your own role</b><div class="what">Invent another role your company needs, for example customer support or legal.</div></div>'
    body = f"""
<p class="lead">You are a <b>small company</b>: everybody has a job and depends on the others. Your team has 5 to 7 people, and <b>only one of you is the developer</b>.</p>
<div style="width:80%;margin:0 auto">{d.team_chart()}</div>
<h3 style="margin-top:6px">🔁 How the work flows in a small company</h3>
<div style="width:80%;margin:0 auto">{d.team_flow()}</div>
<h3 style="margin-top:8px">🎭 The roles</h3>
<div class="grid2" style="gap:7px">{"".join(cards)}{own}</div>
<div class="callout yellow" style="margin-top:10px"><b class="t">👥 How many people are you?</b>5 people: the Manager also presents and the Spec writer also tests. 6 people: add the Tester. 7 people: add the Presenter, so everyone has one role.</div>"""
    return page(8, "Your small company: roles", body)


def phase(n, title, mins, color, items):
    li = "".join(f'<li><span class="r">{chip(r)}</span><span>{text}</span></li>' for r, text in items)
    return f'<div class="phase" style="border-color:{color}"><div class="mh"><div class="mn" style="background:{color}">{n}</div><b style="color:{color}">{title}</b><span class="min" style="background:{color}">about {mins} min</span></div><ul>{li}</ul></div>'


def page_tasks():
    ps = [
        phase(1, "Kick-off", 10, d.NAVY, [
            ("Manager", "Hands out the roles, states the goal: a working page and a winning startup."),
            ("Developer", "Starts the ready back end with the trainer's guide and opens the <b>/docs</b> page."),
            ("Spec writer", "Reads the pages about the web page and the AI, with everyone else."),
        ]),
        phase(2, "Specs and design", 15, d.BLUE, [
            ("Spec writer", "Writes the requirements in simple sentences: the minimum first, then the nice-to-haves."),
            ("Designer", "Sketches the layout on paper or a slide, picks colors and a name."),
            ("Financial analyst", "Chooses an investor profile and the weights, and guesses what the winner looks like."),
            ("Developer", "Asks the AI for a first empty page that talks to the back end."),
        ]),
        phase(3, "Build the minimum", 25, d.FE_RED, [
            ("Developer", "Builds the page with the AI from the spec, the sketch and the list of gates."),
            ("Spec writer", "Answers the developer's questions and fixes the spec if needed."),
            ("Tester", "Prepares a test checklist from the spec."),
            ("Financial analyst", "Prepares five good questions for the AI."),
        ]),
        phase(4, "Nice to have", 15, d.PURPLE, [
            ("Manager", "With the team, picks at least two nice-to-haves that fit the time."),
            ("Developer", "Adds them with the AI. Pastes error messages back to the AI when something breaks."),
            ("Designer", "Reviews the look and asks for polishing."),
        ]),
        phase(5, "Test and decide", 15, d.GREEN, [
            ("Tester", "Runs the checklist, reports bugs, checks one AI claim against the table."),
            ("Financial analyst", "Uses the page to find the winner and a runner-up: 3 reasons for, 2 risks against."),
            ("Manager", "Makes the final call and confirms what the team hands in."),
        ]),
    ]
    body = f"""
<p class="lead">Your company works in <b>five phases</b>. Everybody has something to do in each phase, and most of the work runs in parallel. The times are only suggestions, the trainer helps with the schedule.</p>
{"".join(ps)}
<div class="callout green"><b class="t">📦 What your company hands in at the end</b>
<div class="grid2" style="margin-top:3px;gap:2px 16px">
<span>🖥️ The working web page</span><span>🏆 The winner startup and the reasons</span>
<span>🚦 Two risks you found</span><span>🤖 What you learned about using AI</span></div></div>"""
    return page(9, "Your mission, phase by phase", body)


def page_team():
    body = f"""
<p class="lead">There are two blocks of 80 minutes. In the first one you build the web page and decide. In the second one you prepare the presentation.</p>
{d.timeline()}
<div class="two" style="margin-top:6px">
  <div class="callout blue"><b class="t">Block 1: the web page</b>Kick-off, specs and design, the minimum page, the nice-to-haves, test and decision. See the phases on page 9.</div>
  <div class="callout green"><b class="t">Block 2: the presentation</b>Think up the story, build the slides, rehearse. The trainer tells you the order of the show.</div>
</div>
<h3>🎬 Who does what in block 2?</h3>
<div class="tbl"><table>
<tr><th style="width:150px">Role</th><th>Task during the presentation work</th></tr>
<tr><td>{chip("Manager")}</td><td>Leads the story discussion, watches the time, approves the final slides.</td></tr>
<tr><td>{chip("Presenter")}</td><td>Writes the storyline and the speaker notes, leads the rehearsal.</td></tr>
<tr><td>{chip("Designer")}</td><td>Builds the slides and the charts.</td></tr>
<tr><td>{chip("Financial analyst")}</td><td>Provides the numbers, the reasons for the choice and the risks.</td></tr>
<tr><td>{chip("Developer")}</td><td>Prepares a short live demo or screenshots of the web page.</td></tr>
<tr><td>{chip("Tester")}</td><td>Checks that every number and claim on the slides is true.</td></tr>
<tr><td>{chip("Spec writer")}</td><td>Explains what was asked for and how the page matches it.</td></tr>
</table></div>
<div class="callout yellow" style="margin-top:10px"><b class="t">💬 If you get stuck</b>1. Ask the AI. 2. Ask a teammate. 3. Call the trainer. Getting stuck is normal: it is part of learning!</div>"""
    return page(10, "Time plan and teamwork", body)


def page_presentation():
    must = [
        ("👤", "Understandable", "Speak so that anyone who was not with you can follow."),
        ("🧠", "Reasoned", "Explain why you chose these weights."),
        ("🎭", "Honest", "Show the risks, and where the AI can be wrong."),
        ("🎨", "Visual", "Use pictures, colors and numbers, not long texts."),
    ]
    mh = "".join(f'<div class="card"><h4>{i} {t}</h4><p>{s}</p></div>' for i, t, s in must)
    body = f"""
<p class="lead">In the second 80 minutes you <b>present</b> your solution to the other teams. It does not have to be perfect, but it needs a story: where you started, what you found and where you ended up.</p>
<h3>🎞️ The suggested story: 5 slides</h3>
{d.presentation_flow()}
<div class="grid2" style="margin-top:12px">
  <div class="card" style="border-color:#2563EB"><h4 style="color:#2563EB">Slides 1-2: the base</h4><p>What did you look at? Which criteria did you find important, and why?</p></div>
  <div class="card" style="border-color:#16A34A"><h4 style="color:#16A34A">Slide 3: the winner</h4><p>Who won? Show it with a chart or a picture of your ranking and tell why this one.</p></div>
  <div class="card" style="border-color:#EA580C"><h4 style="color:#EA580C">Slide 4: the risks</h4><p>What could go wrong with the winner? Did the winner stay the same when you changed a weight?</p></div>
  <div class="card" style="border-color:#7C3AED"><h4 style="color:#7C3AED">Slide 5: the AI</h4><p>How did the AI help, and where did you have to correct it? What would you do differently next time?</p></div>
</div>
<h3>⭐ What to pay attention to</h3>
<div class="grid2">{mh}</div>
<div class="callout purple" style="margin-top:12px"><b class="t">🏢 Show your company!</b>Let every role say one sentence about what they contributed. It shows that you worked as a real team.</div>
<div class="callout green"><b class="t">✅ Before you present, ask yourselves</b>Would someone who hears it for the first time understand it? Is every number true? Does everybody have a part in the show?</div>"""
    return page(11, "The presentation", body)


def page_glossary():
    terms = [
        ("Startup", "A new business that wants to grow fast."),
        ("Sector", "The field the company works in (for example health or finance)."),
        ("EBITDA", "The profit from running the business. If negative, the company loses money."),
        ("Gross margin", "The part of the selling price that is left after the costs."),
        ("Runway", "For how many months the company's money is enough."),
        ("Churn", "The share of customers who leave the company."),
        ("Weight", "How important a criterion is."),
        ("Ranking", "The companies in order of their score."),
        ("M Ft", "Million forints. Money amounts are given in this."),
        ("Prompt", "The question or instruction you write to the AI."),
        ("FE (front end)", "The web page that the user sees and uses."),
        ("API", "A gate through which the web page asks the back end for data."),
        ("Spec", "A written description of what the page must do."),
    ]
    th = "".join(f'<tr><td style="width:120px"><b style="color:#2563EB">{t}</b></td><td>{s}</td></tr>' for t, s in terms)
    body = f"""
<div class="grid2">
  <div class="callout red"><b class="t">🚫 Not investment advice</b>The score and the ranking are only estimates to help you think. They are not enough for a real financial decision.</div>
  <div class="callout yellow"><b class="t">🎭 The data is made up</b>The companies do not exist, the numbers were generated. Any similarity to real companies is a coincidence.</div>
  <div class="callout purple"><b class="t">🤖 The AI can be wrong</b>Always check the important numbers before you put a claim on a slide.</div>
  <div class="callout blue"><b class="t">🔑 The key is a secret</b>Do not copy the key of the AI anywhere, and do not show it on the screen.</div>
</div>
<h3>📚 Small glossary</h3>
<div class="tbl"><table>{th}</table></div>
<div class="callout green" style="margin-top:14px;text-align:center;font-size:14px"><b>🚀 Good luck, and have a great workshop!</b><br>Curious questions and honest reasoning are worth more than a perfect result.</div>"""
    return page(12, "Good to know and glossary", body)


def build_html():
    pages = [cover(), page_task(), page_data(), page_scoring(), page_risk(), page_app(), page_ai(), page_roles(), page_tasks(), page_team(), page_presentation(), page_glossary()]
    return (
        '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>Startup Intelligence · Workshop Guide</title><style>{CSS}</style></head><body>{"".join(pages)}</body></html>'
    )


def find_browser():
    for candidate in BROWSER_CANDIDATES:
        if pathlib.Path(candidate).exists():
            return candidate
    raise SystemExit("No Edge or Chrome found")


def main():
    HTML_FILE.write_text(build_html(), encoding="utf-8")
    subprocess.run(
        [find_browser(), "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={PDF_FILE}", HTML_FILE.as_uri()],
        check=True,
        timeout=120,
    )
    print(PDF_FILE)


if __name__ == "__main__":
    sys.exit(main())
