"""
Generate high-fidelity UI screenshot for README documentation.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"
DOCS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH = DOCS_DIR / "ui_chat_screen.png"

# Image dimensions
W, H = 1280, 820
img = Image.new("RGB", (W, H), color="#0F172A")
draw = ImageDraw.Draw(img)

# Try loading standard font or default
try:
    font_title = ImageFont.truetype("arial.ttf", 26)
    font_sub = ImageFont.truetype("arial.ttf", 15)
    font_bold = ImageFont.truetype("arialbd.ttf", 16)
    font_regular = ImageFont.truetype("arial.ttf", 14)
    font_small = ImageFont.truetype("arial.ttf", 12)
    font_code = ImageFont.truetype("consola.ttf", 13)
except Exception:
    font_title = font_sub = font_bold = font_regular = font_small = font_code = ImageFont.load_default()

# App Window Chrome
draw.rectangle([(20, 20), (W - 20, H - 20)], fill="#FFFFFF", outline="#E2E8F0", width=1)
# Window Header Bar
draw.rectangle([(20, 20), (W - 20, 60)], fill="#F8FAFC")
draw.ellipse([(35, 36), (47, 48)], fill="#EF4444")
draw.ellipse([(55, 36), (67, 48)], fill="#F59E0B")
draw.ellipse([(75, 36), (87, 48)], fill="#10B981")
draw.text((W // 2 - 120, 33), "StartupSetu AI Platform — Streamlit Assistant", fill="#475569", font=font_small)

# Sidebar (Left)
sidebar_w = 320
draw.rectangle([(20, 61), (20 + sidebar_w, H - 20)], fill="#F1F5F9")
draw.text((45, 80), "⚙️ System Control", fill="#0F172A", font=font_bold)

# API Status Badge
draw.rectangle([(45, 115), (280, 150)], fill="#DCFCE7", outline="#86EFAC", width=1)
draw.ellipse([(58, 128), (68, 138)], fill="#16A34A")
draw.text((76, 124), "API Online (FastAPI:8000)", fill="#166534", font=font_bold)

# Radio Options
draw.text((45, 175), "Select Processing Engine:", fill="#334155", font=font_bold)
draw.rectangle([(45, 205), (295, 240)], fill="#3B82F6", outline="#2563EB", width=1)
draw.text((60, 215), "● LangGraph Agent (/agent)", fill="#FFFFFF", font=font_bold)

draw.rectangle([(45, 250), (295, 285)], fill="#FFFFFF", outline="#CBD5E1", width=1)
draw.text((60, 260), "○ Direct RAG Pipeline (/ask)", fill="#475569", font=font_regular)

# Sidebar Prompts
draw.text((45, 310), "💡 Quick Inquiries", fill="#334155", font=font_bold)
samples = [
    "What is DPIIT Startup Recognition?",
    "Check eligibility: Pvt Ltd, 2 Cr",
    "Startup India Seed Fund Scheme",
    "Apply for DPIIT Recognition"
]
y_sample = 340
for s in samples:
    draw.rectangle([(45, y_sample), (295, y_sample + 32)], fill="#FFFFFF", outline="#E2E8F0", width=1)
    draw.text((55, y_sample + 7), s, fill="#1E293B", font=font_small)
    y_sample += 40

# Clear Chat Button
draw.rectangle([(45, H - 75), (295, H - 40)], fill="#FEE2E2", outline="#FCA5A5", width=1)
draw.text((95, H - 65), "🗑️ Clear Conversation", fill="#991B1B", font=font_bold)

# Main Area (Right)
main_x = 20 + sidebar_w + 30
draw.text((main_x, 80), "StartupSetu AI Platform", fill="#1E3A8A", font=font_title)
draw.text((main_x, 115), "AI-Powered DPIIT Startup Recognition, Funding Schemes & Official Guidance", fill="#64748B", font=font_sub)

# Chat Message 1: User
y_chat = 155
draw.rectangle([(main_x, y_chat), (W - 50, y_chat + 50)], fill="#EFF6FF", outline="#DBEAFE", width=1)
draw.text((main_x + 15, y_chat + 15), "👤 Check eligibility for my Pvt Ltd company incorporated in 2024 with 2 crore turnover", fill="#1E3A8A", font=font_bold)

# Chat Message 2: Assistant Reply
y_chat += 65
draw.rectangle([(main_x, y_chat), (W - 50, y_chat + 310)], fill="#F8FAFC", outline="#E2E8F0", width=1)
draw.text((main_x + 15, y_chat + 12), "🤖 StartupSetu Agent:", fill="#0F172A", font=font_bold)

res_lines = [
    "Assessment: ELIGIBLE for official DPIIT Startup Recognition.",
    "• Entity Type Valid: True (Private Limited Company)",
    "• Age <= 10 Years: True (2 years active since 2024)",
    "• Annual Turnover <= ₹100 Cr: True (₹2.0 Crore)",
    "• Innovation & Scalability: True",
    "",
    "Available Government Benefits Upon Recognition:",
    "✔ Section 80-IAC 3-Year Income Tax Exemption on profits",
    "✔ 80% Rebate on Patent Filing and 50% on Trademark Fees",
    "✔ Access to Startup India Seed Fund Scheme (up to ₹50 Lakhs)",
    "✔ Self-certification under 6 Labour and 3 Environmental Laws"
]
y_text = y_chat + 38
for line in res_lines:
    draw.text((main_x + 25, y_text), line, fill="#334155", font=font_regular)
    y_text += 20

# Citation Box inside Assistant message
draw.rectangle([(main_x + 25, y_text + 5), (W - 80, y_text + 65)], fill="#EFF6FF", outline="#93C5FD", width=1)
draw.text((main_x + 35, y_text + 12), "📚 Citation: DPIIT Startup Recognition Guidelines [Page 1]", fill="#1E40AF", font=font_bold)
draw.text((main_x + 35, y_text + 34), "Official Portal: https://www.startupindia.gov.in/content/sih/en/startupgov/startup_recognition_page.html", fill="#2563EB", font=font_small)

# Thumbs up / down feedback row
y_fb = y_chat + 320
draw.rectangle([(main_x, y_fb), (main_x + 110, y_fb + 32)], fill="#DCFCE7", outline="#86EFAC", width=1)
draw.text((main_x + 15, y_fb + 7), "👍 Helpful", fill="#166534", font=font_bold)

draw.rectangle([(main_x + 125, y_fb), (main_x + 225, y_fb + 32)], fill="#F1F5F9", outline="#CBD5E1", width=1)
draw.text((main_x + 145, y_fb + 7), "👎 Poor", fill="#475569", font=font_regular)
draw.text((main_x + 245, y_fb + 8), "✓ Feedback saved to data/feedback.json", fill="#059669", font=font_small)

# Approval Required Banner
y_app = y_fb + 45
draw.rectangle([(main_x, y_app), (W - 50, y_app + 80)], fill="#FEF3C7", outline="#FCD34D", width=1)
draw.text((main_x + 15, y_app + 12), "⚠️ Human Approval Required: The agent is preparing to execute 'submit_dpiit_application'", fill="#92400E", font=font_bold)
draw.rectangle([(main_x + 25, y_app + 40), (main_x + 180, y_app + 70)], fill="#16A34A")
draw.text((main_x + 40, y_app + 47), "✅ Approve Action", fill="#FFFFFF", font=font_bold)
draw.rectangle([(main_x + 195, y_app + 40), (main_x + 340, y_app + 70)], fill="#DC2626")
draw.text((main_x + 215, y_app + 47), "❌ Reject Action", fill="#FFFFFF", font=font_bold)

# Chat Input Box at bottom
y_input = H - 85
draw.rectangle([(main_x, y_input), (W - 50, y_input + 45)], fill="#F8FAFC", outline="#CBD5E1", width=1)
draw.text((main_x + 15, y_input + 13), "Ask about DPIIT startup recognition, eligibility, or funding schemes...", fill="#94A3B8", font=font_regular)
draw.rectangle([(W - 110, y_input + 6), (W - 60, y_input + 39)], fill="#2563EB", outline="#1D4ED8", width=1)
draw.text((W - 95, y_input + 13), "Send", fill="#FFFFFF", font=font_bold)

img.save(OUTPUT_PATH, "PNG")
print(f"Screenshot saved to: {OUTPUT_PATH}")
