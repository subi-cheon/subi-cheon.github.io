#!/usr/bin/env python3
"""
새 글 추가 자동화 스크립트.

하는 일 (한 번에):
  1) posts/<slug>.html 생성 — 메타·Open Graph·Twitter·JSON-LD 전부 포함
  2) assets/og-<slug>.png 생성 — 제목이 들어간 링크 미리보기 이미지
  3) sitemap.xml 에 새 URL 등록
  4) index.html 의 Writing 목록 맨 위에 새 글 추가 + 번호 재정렬

사용 예:
  python3 new_post.py \
    --slug ai-agent-handoff \
    --title "에이전트에게 일을 넘긴다는 것" \
    --desc "사람이 어디까지 개입해야 하는가." \
    --date 2026-07 \
    --read 6 \
    --tags "Agent UX,Process"

생성 후 posts/<slug>.html 의 <div class="prose"> 안 본문만 채우면 끝.
"""
import argparse
import datetime
import os
import re
import sys

BASE = "https://subi-cheon.github.io"
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "assets"))
from make_og import make as make_og  # noqa: E402


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def disp_date(date):  # "2026-07" -> "2026.07"
    return date.replace("-", ".")


def post_html(slug, title, desc, date, read, tags, prev):
    tag_spans = "".join(f"<span>{esc(t)}</span>" for t in tags)
    og = f"{BASE}/assets/og-{slug}.png"
    url = f"{BASE}/posts/{slug}.html"
    article_tags = "\n".join(f'  <meta property="article:tag" content="{esc(t)}" />' for t in tags)
    keywords = ", ".join(f'"{esc(t)}"' for t in tags)
    pubdate = f"{date}-01"

    prev_nav = ""
    if prev:
        prev_nav = f"""
      <a class="article-nav-prev" href="{prev['slug']}.html">
        <span class="article-nav-label">이전 글</span>
        <span class="article-nav-title">{esc(prev['title'])}</span>
      </a>"""

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(title)} — Subi Cheon</title>
  <meta name="description" content="{esc(desc)}" />
  <meta name="author" content="Subi Cheon (천수비)" />
  <link rel="canonical" href="{url}" />

  <!-- Open Graph -->
  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="Subi Cheon" />
  <meta property="og:locale" content="ko_KR" />
  <meta property="og:url" content="{url}" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{esc(desc)}" />
  <meta property="og:image" content="{og}" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="article:published_time" content="{pubdate}" />
  <meta property="article:author" content="Subi Cheon" />
{article_tags}

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{esc(title)}" />
  <meta name="twitter:description" content="{esc(desc)}" />
  <meta name="twitter:image" content="{og}" />

  <!-- Structured data -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "{esc(title)}",
    "description": "{esc(desc)}",
    "image": "{og}",
    "datePublished": "{pubdate}",
    "inLanguage": "ko-KR",
    "keywords": [{keywords}],
    "mainEntityOfPage": "{url}",
    "author": {{ "@type": "Person", "name": "Subi Cheon", "url": "{BASE}/" }},
    "publisher": {{ "@type": "Person", "name": "Subi Cheon", "url": "{BASE}/" }}
  }}
  </script>

  <link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin />
  <link rel="stylesheet" href="../styles.css" />

  <script>
    (function () {{
      var stored = localStorage.getItem('theme');
      var prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      var theme = stored || (prefersDark ? 'dark' : 'light');
      document.documentElement.setAttribute('data-theme', theme);
    }})();
  </script>
</head>
<body>
  <!-- ===== Header ===== -->
  <header class="site-header" id="top">
    <div class="container header-inner">
      <a class="logo" href="../index.html" aria-label="홈으로">
        <span class="logo-text">Subi Cheon</span>
      </a>

      <nav class="nav" aria-label="주요 메뉴">
        <ul class="nav-list" id="navList">
          <li><a href="../about.html">About</a></li>
          <li><a href="../index.html#writing">Writing</a></li>
          <li><a href="../index.html#project">Project</a></li>
          <li><a href="../index.html#contact">Contact</a></li>
          <li>
            <a href="https://www.linkedin.com/in/subicheon/" target="_blank" rel="noopener noreferrer">
              Linkedin
              <svg class="ext-icon" width="12" height="12" viewBox="0 0 24 24" aria-hidden="true">
                <path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M14 4h6v6M20 4l-9 9M19 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h5"/>
              </svg>
            </a>
          </li>
        </ul>

        <button class="theme-toggle" id="themeToggle" type="button" aria-label="라이트/다크 모드 전환">
          <svg class="icon-sun" width="20" height="20" viewBox="0 0 24 24" aria-hidden="true">
            <circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="2"/>
            <path stroke="currentColor" stroke-width="2" stroke-linecap="round" d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>
          </svg>
          <svg class="icon-moon" width="20" height="20" viewBox="0 0 24 24" aria-hidden="true">
            <path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/>
          </svg>
        </button>

        <button class="menu-btn" id="menuBtn" type="button" aria-label="메뉴 열기" aria-expanded="false" aria-controls="navList">
          <span></span><span></span><span></span>
        </button>
      </nav>
    </div>
  </header>

  <main class="article container">
    <a class="back-link" href="../index.html#writing">← Writing</a>

    <header class="article-head">
      <div class="tag-list small">{tag_spans}</div>
      <h1>{esc(title)}</h1>
      <p class="article-meta">
        <time datetime="{date}">{disp_date(date)}</time>
        <span class="dot">·</span>
        <span>{read}분 읽기</span>
      </p>
    </header>

    <div class="prose">
      <!-- ↓↓↓ 여기에 본문을 작성하세요 (h2, p, blockquote, ul 등 자유롭게) ↓↓↓ -->
      <p>{esc(desc)}</p>
      <!-- ↑↑↑ 본문 끝 ↑↑↑ -->
    </div>

    <nav class="article-nav">{prev_nav}
    </nav>
  </main>

  <!-- ===== Footer ===== -->
  <footer class="site-footer">
    <div class="container footer-inner">
      <p class="footer-copy">© 2026 천수비 (Subi Cheon)</p>
      <div class="footer-links">
        <a href="https://www.linkedin.com/in/subicheon/" target="_blank" rel="noopener noreferrer">Linkedin</a>
        <a href="mailto:subi.cheon@gmail.com">subi.cheon@gmail.com</a>
      </div>
    </div>
  </footer>

  <script src="../script.js"></script>
</body>
</html>
"""


def update_sitemap(slug, date):
    path = os.path.join(ROOT, "sitemap.xml")
    xml = open(path, encoding="utf-8").read()
    url = f"{BASE}/posts/{slug}.html"
    if url in xml:
        print("• sitemap: 이미 등록됨, 건너뜀")
        return
    entry = f"""  <url>
    <loc>{url}</loc>
    <lastmod>{date}-01</lastmod>
    <changefreq>yearly</changefreq>
    <priority>0.7</priority>
  </url>
</urlset>"""
    xml = xml.replace("</urlset>", entry)
    open(path, "w", encoding="utf-8").write(xml)
    print("• sitemap.xml 업데이트 완료")


def detect_newest_post(index_html):
    """Writing 목록의 첫 글(현재 최신)을 prev 링크용으로 추출."""
    m = re.search(r'writing-item">\s*<a href="posts/([^"]+)\.html">.*?<h3>(.*?)</h3>',
                  index_html, re.S)
    if m:
        return {"slug": m.group(1), "title": m.group(2).strip()}
    return None


def update_index(slug, title, desc, date, tags):
    path = os.path.join(ROOT, "index.html")
    html = open(path, encoding="utf-8").read()
    tag_spans = "".join(f"<span>{esc(t)}</span>" for t in tags)
    new_li = f"""        <li class="writing-item">
          <a href="posts/{slug}.html">
            <span class="writing-no">00</span>
            <div class="writing-body">
              <h3>{esc(title)}</h3>
              <p>{esc(desc)}</p>
              <div class="tag-list small">{tag_spans}</div>
            </div>
            <span class="writing-date">{disp_date(date)}</span>
          </a>
        </li>
"""
    marker = '<ul class="writing-list">\n'
    if marker not in html:
        print("⚠ index.html 의 writing-list 를 찾지 못했습니다. 수동으로 추가하세요.")
        return
    html = html.replace(marker, marker + new_li, 1)
    # writing-no 번호 01,02,03... 재정렬
    counter = {"n": 0}
    def renum(_):
        counter["n"] += 1
        return f'<span class="writing-no">{counter["n"]:02d}</span>'
    html = re.sub(r'<span class="writing-no">\d+</span>', renum, html)
    open(path, "w", encoding="utf-8").write(html)
    print("• index.html Writing 목록 추가 + 번호 재정렬 완료")


def main():
    p = argparse.ArgumentParser(description="새 글 추가 자동화")
    p.add_argument("--slug", required=True, help="URL 슬러그 (영문/하이픈). 예: ai-agent-handoff")
    p.add_argument("--title", required=True, help="글 제목")
    p.add_argument("--desc", required=True, help="한 줄 설명 (검색/미리보기에 사용)")
    p.add_argument("--date", required=True, help="발행 연월 YYYY-MM. 예: 2026-07")
    p.add_argument("--read", default="5", help="예상 읽기 시간(분). 기본 5")
    p.add_argument("--tags", required=True, help="쉼표로 구분. 예: \"Agent UX,Process\"")
    a = p.parse_args()

    if not re.match(r"^\d{4}-\d{2}$", a.date):
        sys.exit("✗ --date 는 YYYY-MM 형식이어야 합니다. 예: 2026-07")
    tags = [t.strip() for t in a.tags.split(",") if t.strip()]
    post_path = os.path.join(ROOT, "posts", f"{a.slug}.html")
    if os.path.exists(post_path):
        sys.exit(f"✗ 이미 존재합니다: posts/{a.slug}.html")

    index_html = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    prev = detect_newest_post(index_html)

    # 1) 글 HTML
    open(post_path, "w", encoding="utf-8").write(
        post_html(a.slug, a.title, a.desc, a.date, a.read, tags, prev))
    print(f"• posts/{a.slug}.html 생성 완료")

    # 2) OG 이미지
    make_og(f"og-{a.slug}.png", f"Writing · {disp_date(a.date)}", a.title, a.desc)

    # 3) sitemap
    update_sitemap(a.slug, a.date)

    # 4) index 목록
    update_index(a.slug, a.title, a.desc, a.date, tags)

    print("\n✅ 완료! 다음만 하면 됩니다:")
    print(f"   1. posts/{a.slug}.html 의 <div class=\"prose\"> 안에 본문 작성")
    print("   2. git add -A && git commit -m \"Add post: " + a.slug + "\" && git push")


if __name__ == "__main__":
    main()
