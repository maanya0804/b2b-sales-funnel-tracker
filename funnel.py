import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs('output', exist_ok=True)

# ── DATA ──────────────────────────────────────────────
# Realistic B2B funnel numbers for 3 verticals
# Each number = deals remaining at that stage

stages = ['Prospect', 'Engage', 'Propose', 'Close', 'Retain']

data = {
    'IT':            [200, 120, 60, 25, 18],
    'BFSI':          [180, 90,  40, 20, 16],
    'Manufacturing': [150, 70,  30, 12, 8 ],
}

df = pd.DataFrame(data, index=stages)

# ── CHART 1: Funnel chart per vertical ────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 6))

colors = ['#2196F3', '#4CAF50', '#FF9800']

for i, (vertical, color) in enumerate(zip(data.keys(), colors)):
    values = data[vertical]
    axes[i].barh(stages[::-1], values[::-1], color=color, alpha=0.85)
    axes[i].set_title(f'{vertical} Vertical', fontweight='bold', fontsize=12)
    axes[i].set_xlabel('Number of Deals')
    for j, v in enumerate(values[::-1]):
        axes[i].text(v + 1, j, str(v), va='center', fontsize=9)

plt.suptitle('B2B Sales Funnel — Deal Flow by Vertical', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('output/chart1_funnel.png', dpi=150)
plt.close()
print("Chart 1 done")

# ── CHART 2: Conversion rates comparison ──────────────
conv_rates = {}
for vertical, values in data.items():
    rates = [round(values[i+1]/values[i]*100, 1) for i in range(len(values)-1)]
    conv_rates[vertical] = rates

conv_df = pd.DataFrame(conv_rates,
    index=['Prospect→Engage', 'Engage→Propose', 'Propose→Close', 'Close→Retain'])

ax = conv_df.plot(kind='bar', figsize=(10, 6), color=colors, alpha=0.85)
plt.title('Stage-by-Stage Conversion Rates by Vertical (%)', fontweight='bold')
plt.ylabel('Conversion Rate (%)')
plt.xlabel('Funnel Stage Transition')
plt.xticks(rotation=15)
plt.legend(title='Vertical')
plt.tight_layout()
plt.savefig('output/chart2_conversion_rates.png', dpi=150)
plt.close()
print("Chart 2 done")

# ── CHART 3: End-to-end conversion ────────────────────
overall = {v: round(data[v][-1]/data[v][0]*100, 1) for v in data}
fig, ax = plt.subplots(figsize=(7, 5))
bars = ax.bar(overall.keys(), overall.values(), color=colors, alpha=0.85)
ax.set_title('Overall Prospect-to-Retain Conversion Rate (%)', fontweight='bold')
ax.set_ylabel('Conversion Rate (%)')
ax.set_ylim(0, 20)
for bar, val in zip(bars, overall.values()):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.3, f'{val}%',
            ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig('output/chart3_overall_conversion.png', dpi=150)
plt.close()
print("Chart 3 done")

# ── BRIEF ─────────────────────────────────────────────
brief = """
================================================
  B2B SALES FUNNEL CONVERSION ANALYSIS
  Prepared by: Maanya Saikia
  Verticals: IT, BFSI, Manufacturing
================================================

OBJECTIVE
---------
To model deal flow across a 5-stage consultative sales funnel and identify
conversion leakage points across three key industry verticals.

FUNNEL STAGES: Prospect → Engage → Propose → Close → Retain

"""

for vertical in data:
    values = data[vertical]
    rates = [round(values[i+1]/values[i]*100, 1) for i in range(len(values)-1)]
    overall_rate = round(values[-1]/values[0]*100, 1)

    brief += f"""
{vertical.upper()} VERTICAL
{'─'*40}
  Starting Pipeline : {values[0]} prospects
  Deals Closed      : {values[3]}
  Retained Clients  : {values[4]}
  Overall Conversion: {overall_rate}%

  Stage Conversion Breakdown:
  Prospect → Engage  : {rates[0]}%
  Engage   → Propose : {rates[1]}%
  Propose  → Close   : {rates[2]}%
  Close    → Retain  : {rates[3]}%

  KEY LEAKAGE POINT: {['Prospect→Engage', 'Engage→Propose', 'Propose→Close', 'Close→Retain'][rates.index(min(rates))]}
  ({min(rates)}% conversion — lowest in the funnel)

"""

brief += """
CROSS-VERTICAL RECOMMENDATIONS
───────────────────────────────
1. Propose→Close is the weakest stage across all verticals.
   Action: Strengthen proposal quality with client-specific ROI framing.

2. Manufacturing shows lowest overall conversion (5.3%).
   Action: Increase early-stage qualification rigour to reduce wasted pipeline.

3. BFSI retention rate is strongest at 80%.
   Action: Replicate BFSI engagement model in IT and Manufacturing post-close.

4. Prospect→Engage drop-off is steepest in Manufacturing (53%).
   Action: Revisit ICP (Ideal Client Profile) for Manufacturing segment.
"""

with open('output/sales_funnel_brief.txt', 'w', encoding='utf-8') as f:    f.write(brief)

print("\nBrief saved!")
print(brief)