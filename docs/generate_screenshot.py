"""
Generate high-fidelity UI screenshot showing 'Am I a startup?' st.form,
cited DPIIT statutory rules, and chat assistant for README documentation.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"
DOCS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH = DOCS_DIR / "ui_chat_screen.png"

# Image dimensions
W, H = 1320, 880
img = Image.new("RGB", (W, H), color="#0F172A")
draw = ImageDraw.Draw(img)

# Try loading standard font or default
try:
    font_title = ImageFont.truetype("arial.ttf", 24)
    font_sub = ImageFont.truetype("arial.ttf", 14)
    font_bold = ImageFont.truetype("arialbd.ttf", 15)
    font_regular = ImageFont.truetype("arial.ttf", 13)
    font_small = ImageFont.truetype("arial.ttf", 11)
    font_code = ImageFont.truetype("consola.ttf", 12)
except Exception:
    font_title = font_sub = font_bold = font_regular = font_small = font_code = ImageFont.load_default()

# App Window Chrome
draw.rectangle([(20, 20), (W - 20, H - 20)], fill="#FFFFFF", outline="#CBD5E1", width=1)
# Window Header Bar
draw.rectangle([(20, 20), (W - 20, 58)], fill="#F8FAFC")
draw.ellipse([(35, 34), (47, 46)], fill="#EF4444")
draw.ellipse([(55, 34), (67, 46)], fill="#F59E0B")
draw.ellipse([(75, 34), (87, 46)], fill="#10B981")
draw.text((W // 2 - 140, 32), "StartupSetu AI Platform — Streamlit UI (Day 10)", fill="#475569", font=font_small)

# Sidebar (Left)
sidebar_w = 290
draw.rectangle([(20, 59), (20 + sidebar_w, H - 20)], fill="#F8FAFC", outline="#E2E8F0", width=1)
draw.text((40, 75), "⚙️ System Control", fill="#0F172A", font=font_bold)

# API Status Badge
draw.rectangle([(40, 105), (280, 138)], fill="#DCFCE7", outline="#86EFAC", width=1)
draw.ellipse([(52, 117), (62, 127)], fill="#16A34A")
draw.text((70, 115), "● API Online (FastAPI)", fill="#166534", font=font_bold)

# Processing Engine Options
draw.text((40, 155), "Processing Engine:", fill="#334155", font=font_bold)
draw.rectangle([(40, 180), (280, 212)], fill="#3B82F6", outline="#2563EB", width=1)
draw.text((55, 190), "● LangGraph Agent (/agent)", fill="#FFFFFF", font=font_bold)
draw.rectangle([(40, 218), (280, 250)], fill="#FFFFFF", outline="#CBD5E1", width=1)
draw.text((55, 228), "○ Direct RAG (/ask)", fill="#475569", font=font_regular)

# Sidebar Prompts
draw.text((40, 270), "💡 Example Queries", fill="#334155", font=font_bold)
samples = [
    "What is DPIIT Recognition?",
    "Check eligibility: Pvt Ltd, 2 Cr",
    "Startup India Seed Fund Scheme",
    "Section 80-IAC tax exemption"
]
y_sample = 295
for s in samples:
    draw.rectangle([(40, y_sample), (280, y_sample + 28)], fill="#FFFFFF", outline="#E2E8F0", width=1)
    draw.text((50, y_sample + 6), s, fill="#334155", font=font_small)
    y_sample += 35

# Clear Button
draw.rectangle([(40, H - 65), (280, H - 35)], fill="#FEE2E2", outline="#FCA5A5", width=1)
draw.text((80, H - 55), "🗑️ Clear Conversation", fill="#991B1B", font=font_bold)

# Main Area (Right)
main_x = 20 + sidebar_w + 25
draw.text((main_x, 70), "StartupSetu AI Platform", fill="#1E3A8A", font=font_title)
draw.text((main_x, 100), "Official DPIIT Startup Recognition, Funding Schemes & Policy Guidance for Founders", fill="#64748B", font=font_sub)

# Navigation Tabs
draw.rectangle([(main_x, 125), (main_x + 280, 158)], fill="#3B82F6", outline="#2563EB", width=1)
draw.text((main_x + 15, 135), "🚀 'Am I a startup?' Form (Active)", fill="#FFFFFF", font=font_bold)

draw.rectangle([(main_x + 285, 125), (main_x + 540, 158)], fill="#F1F5F9", outline="#CBD5E1", width=1)
draw.text((main_x + 300, 135), "💬 AI Chat Assistant (/ask & /agent)", fill="#475569", font=font_regular)

# Section Header
draw.text((main_x, 172), "📋 'Am I a startup?' — Official DPIIT Recognition Evaluation", fill="#0F172A", font=font_bold)

# Form Container (st.form)
form_y = 195
form_w = W - main_x - 35
form_h = 230
draw.rectangle([(main_x, form_y), (main_x + form_w, form_y + form_h)], fill="#F8FAFC", outline="#3B82F6", width=2)
draw.text((main_x + 15, form_y + 10), "st.form('am_i_a_startup_form')", fill="#2563EB", font=font_code)

# Input 1: Entity Type
draw.text((main_x + 20, form_y + 35), "1. Entity Type", fill="#334155", font=font_bold)
draw.rectangle([(main_x + 20, form_y + 55), (main_x + form_w // 2 - 15, form_y + 88)], fill="#FFFFFF", outline="#94A3B8", width=1)
draw.text((main_x + 30, form_y + 65), "Private Limited Company ▾", fill="#0F172A", font=font_regular)

# Input 2: Incorporation Date
draw.text((main_x + 20, form_y + 98), "2. Incorporation Date", fill="#334155", font=font_bold)
draw.rectangle([(main_x + 20, form_y + 118), (main_x + form_w // 2 - 15, form_y + 151)], fill="#FFFFFF", outline="#94A3B8", width=1)
draw.text((main_x + 30, form_y + 128), "2024-01-15 📅", fill="#0F172A", font=font_regular)

# Input 3: Turnover
col2_x = main_x + form_w // 2 + 15
draw.text((col2_x, form_y + 35), "3. Annual Turnover (₹ in Crores)", fill="#334155", font=font_bold)
draw.rectangle([(col2_x, form_y + 55), (main_x + form_w - 20, form_y + 88)], fill="#FFFFFF", outline="#94A3B8", width=1)
draw.text((col2_x + 10, form_y + 65), "2.00 Cr", fill="#0F172A", font=font_regular)

# Input 4: Innovation
draw.text((col2_x, form_y + 98), "4. Innovation & Scalability", fill="#334155", font=font_bold)
draw.rectangle([(col2_x, form_y + 118), (col2_x + 22, form_y + 140)], fill="#3B82F6", outline="#2563EB", width=1)
draw.text((col2_x + 6, form_y + 122), "✔", fill="#FFFFFF", font=font_bold)
draw.text((col2_x + 30, form_y + 123), "Working towards innovation, scalable business model", fill="#0F172A", font=font_small)

# Form Submit Button
draw.rectangle([(main_x + 20, form_y + 172), (main_x + form_w - 20, form_y + 212)], fill="#2563EB", outline="#1D4ED8", width=1)
draw.text((main_x + form_w // 2 - 90, form_y + 185), "🔍 Evaluate Startup Eligibility", fill="#FFFFFF", font=font_bold)

# Result Verdict Box
res_y = form_y + form_h + 15
draw.rectangle([(main_x, res_y), (main_x + form_w, res_y + 45)], fill="#DCFCE7", outline="#86EFAC", width=1)
draw.text((main_x + 15, res_y + 13), "🎉 VERDICT: ELIGIBLE FOR OFFICIAL DPIIT STARTUP RECOGNITION", fill="#166534", font=font_bold)

# 4 Metric Cards
metric_y = res_y + 55
card_w = (form_w - 30) // 4
metrics = [
    ("Entity Type", "Valid", "Private Ltd Co"),
    ("Age (≤ 10 Yrs)", "Valid", "2 yrs active"),
    ("Turnover (≤ ₹100 Cr)", "Valid", "₹2.0 Cr"),
    ("Innovation", "Satisfied", "Scalable model")
]
for i, (label, val, delta) in enumerate(metrics):
    mx = main_x + i * (card_w + 10)
    draw.rectangle([(mx, metric_y), (mx + card_w, metric_y + 55)], fill="#F8FAFC", outline="#E2E8F0", width=1)
    draw.text((mx + 10, metric_y + 6), label, fill="#64748B", font=font_small)
    draw.text((mx + 10, metric_y + 22), val, fill="#16A34A", font=font_bold)
    draw.text((mx + 10, metric_y + 38), delta, fill="#475569", font=font_small)

# Cited DPIIT Statutory Rule Card
rule_y = metric_y + 65
rule_h = 165
draw.rectangle([(main_x, rule_y), (main_x + form_w, rule_y + rule_h)], fill="#EFF6FF", outline="#60A5FA", width=1)
draw.text((main_x + 15, rule_y + 10), "📜 Cited DPIIT Statutory Rule: Gazette Notification G.S.R. 127(E)", fill="#1E40AF", font=font_bold)
draw.text((main_x + 15, rule_y + 30), "Ministry of Commerce and Industry (DPIIT) • Portal: https://www.startupindia.gov.in/", fill="#2563EB", font=font_small)

rules_text = [
    "• Entity Structure: Must be Private Limited Company, LLP, or Registered Partnership (Sole proprietorships excluded).",
    "• Period of Existence: Up to 10 years from the date of incorporation or registration.",
    "• Turnover Cap: Turnover has not exceeded ₹100 Crore for any financial year since incorporation.",
    "• Innovation & Scalability: Working towards innovation or scalable model with potential for employment/wealth generation.",
    "• Reconstruction Exclusion: Entity must not be formed by splitting up or reconstruction of an existing business."
]
rt_y = rule_y + 52
for r in rules_text:
    draw.text((main_x + 20, rt_y), r, fill="#1E293B", font=font_small)
    rt_y += 18

# Government Benefits Row
draw.text((main_x, rule_y + rule_h + 10), "🎁 Available Benefits: Section 80-IAC 3-Year Tax Exemption • 80% Patent Rebate • ₹50L Seed Fund Scheme", fill="#059669", font=font_bold)

img.save(OUTPUT_PATH, "PNG")
print(f"Updated UI screenshot saved to: {OUTPUT_PATH}")
