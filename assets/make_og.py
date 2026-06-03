#!/usr/bin/env python3
"""사이트 톤에 맞춘 1200x630 OG 미리보기 이미지 생성기."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG = (247, 247, 248)      # --bg
CARD = (255, 255, 255)    # --surface
TEXT = (19, 18, 18)       # --text
SOFT = (90, 92, 98)       # text-soft
FAINT = (130, 132, 138)   # text-faint
BORDER = (225, 226, 228)

FONT_PATH = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
OUT = os.path.dirname(os.path.abspath(__file__))


def font(size, index=0):
    return ImageFont.truetype(FONT_PATH, size, index=index)


def wrap(draw, text, fnt, max_w):
    lines, line = [], ""
    for ch in text:
        test = line + ch
        if draw.textlength(test, font=fnt) <= max_w or not line:
            line = test
        else:
            lines.append(line)
            line = ch
    if line:
        lines.append(line)
    return lines


def make(filename, eyebrow, title, sub):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # inner card
    m = 56
    d.rounded_rectangle([m, m, W - m, H - m], radius=28, fill=CARD, outline=BORDER, width=2)

    pad = m + 64
    # eyebrow (uppercase, faint)
    f_eye = font(26, index=2)
    d.text((pad, pad + 8), eyebrow.upper(), font=f_eye, fill=FAINT)

    # title (big, bold)
    f_title = font(72, index=6)
    lines = wrap(d, title, f_title, W - pad * 2)
    y = pad + 70
    for ln in lines[:3]:
        d.text((pad, y), ln, font=f_title, fill=TEXT)
        y += 92

    # subtitle (soft)
    if sub:
        f_sub = font(30, index=2)
        for ln in wrap(d, sub, f_sub, W - pad * 2)[:2]:
            d.text((pad, y + 16), ln, font=f_sub, fill=SOFT)
            y += 44

    # footer: name + url
    f_foot = font(28, index=4)
    fy = H - m - 84
    d.text((pad, fy), "Subi Cheon", font=f_foot, fill=TEXT)
    f_url = font(26, index=2)
    url = "subi-cheon.github.io"
    uw = d.textlength(url, font=f_url)
    d.text((W - pad - uw, fy + 2), url, font=f_url, fill=FAINT)

    path = os.path.join(OUT, filename)
    img.save(path, "PNG")
    print("saved", filename)


if __name__ == "__main__":
    # 기존 페이지들의 OG 이미지 일괄 재생성
    make("og-default.png", "Product Designer · Builder",
         "디자인과 기술 사이에서 쓸모 있는 경험을 만듭니다.",
         "Subi Cheon의 이력서, 포트폴리오, 그리고 생각을 기록하는 공간.")

    make("og-about.png", "About",
         "천수비 — 만들면서 배우는 프로덕트 디자이너",
         "경력, 일하는 방식, 그리고 지금 하고 있는 일.")

    make("og-good-product-questions.png", "Writing · 2026.05",
         "좋은 제품은 어떤 질문에서 시작되는가",
         "문제를 정의하는 방식이 결과물의 절반을 결정한다고 믿습니다.")

    make("og-designer-who-codes.png", "Writing · 2026.03",
         "디자이너가 코드를 다룬다는 것",
         "직접 만들어 보면 설계의 해상도가 달라집니다.")

    make("og-interface-for-ai-agents.png", "Writing · 2026.01",
         "AI 에이전트와 함께 일하는 인터페이스",
         "사람과 에이전트의 역할을 어떻게 나눌 것인가.")
