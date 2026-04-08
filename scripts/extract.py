#!/usr/bin/env python3
"""Extract CZ memoir PDF → Simplified Chinese Markdown chapters."""

import subprocess
import os
import re
import shutil
from pathlib import Path

# Add venv to path
import sys
VENV_SITE = str(Path(__file__).parent.parent / ".venv/lib")
for p in Path(VENV_SITE).glob("python*/site-packages"):
    sys.path.insert(0, str(p))

from opencc import OpenCC
from PIL import Image

PROJECT_DIR = Path(__file__).parent.parent
PDF_FILE = PROJECT_DIR / "cz自传.pdf"
OUTPUT_DIR = PROJECT_DIR / "site" / "chapters"
IMAGES_SRC = Path("/tmp/cz_images")
IMAGES_DST = PROJECT_DIR / "site" / "public" / "images"

cc = OpenCC('t2s')

# Chapter definitions: (filename, traditional_title, start_page, end_page)
# Some chapters start mid-page (marked with split_title for the text that begins the chapter)
CHAPTERS = [
    ("00-recommendations", "推薦語", 5, 5),
    ("01-dedication", "獻詞", 6, 6),
    ("02-preface", "序言（何一）：外面沒有別人", 9, 11),
    ("03-foreword", "前言", 12, 12),
    ("04-binance-launch", "幣安上線，2017年7月14日12點", 13, 14),
    ("05-early-years", "早年歲月", 15, 19),
    ("06-vancouver", "溫哥華，1989-1995", 20, 27),
    ("07-mcgill", "麥基爾歲月，1995-1999", 28, 30),
    ("08-tokyo-years", "東京歲月", 31, 39),
    ("09-bitcoin-2013", "初識比特幣：2013", 40, 51),
    ("10-bijie-tech", "比捷科技", 52, 58),
    ("11-binance-birth", "幣安誕生", 59, 76),
    ("12-china-ban", "中國禁令", 77, 79),
    ("13-tokyo", "東京", 80, 85),
    ("14-number-one", "世界第一", 86, 114),
    ("15-anniversary", "一週年慶典", 115, 118),
    ("16-crypto-winter-2019", "2019加密寒冬", 119, 132),
    ("17-year-2020", "2020", 133, 136),
    ("18-tricky-cases", "棘手案例", 137, 141),
    ("19-year-2021", "2021", 141, 147),
    ("20-roaming-earth-2022", "2022年，漫遊地球", 148, 176),
    ("21-doj-2023", "2023年，司法部談判", 177, 187),
    ("22-flying-to-america", "飛去美國", 188, 221),
    ("23-pro-crypto-era", "美國的「支持加密」時代", 222, 223),
    ("24-pardon", "特赦", 224, 224),
    ("25-epilogue", "結語", 225, 225),
    ("26-cz-principles", "附录：CZ 的原則", 226, 235),
]

# Image page mapping from pdfimages -list (image_index -> page_number)
IMAGE_PAGES = {
    0: 1, 1: 15, 2: 17, 3: 20, 4: 20, 5: 22, 6: 23,
    7: 32, 8: 62, 9: 65, 10: 73, 11: 76, 12: 80, 13: 84,
    14: 85, 15: 89, 16: 91, 17: 92, 18: 94, 19: 96, 20: 97,
    21: 102, 22: 103, 23: 104, 24: 105, 25: 108, 26: 109,
    27: 110, 28: 116, 29: 117, 30: 118, 31: 119, 32: 128,
    33: 133, 34: 134, 35: 146, 36: 150, 37: 154, 38: 155,
    39: 156, 40: 160, 41: 163, 42: 165, 43: 166, 44: 167,
    45: 169, 46: 170, 47: 176, 48: 177, 49: 234, 50: 235,
    51: 240,  # 3px tall separator, skip
}

# Images to skip (too small, decorative, or separator)
SKIP_IMAGES = {51}  # 3px tall separator line


def extract_page_text(page_num):
    """Extract text from a single PDF page."""
    result = subprocess.run(
        ["pdftotext", "-f", str(page_num), "-l", str(page_num), str(PDF_FILE), "-"],
        capture_output=True, text=True
    )
    return result.stdout


def extract_chapter_text(start_page, end_page, title):
    """Extract and join text for a chapter's page range."""
    pages_text = []
    for p in range(start_page, end_page + 1):
        pages_text.append(extract_page_text(p))

    full_text = "\n".join(pages_text)

    # For chapters that share a page with the previous chapter,
    # split at the chapter title
    # Normalize the title for matching (remove spaces that pdftotext might add)
    title_variants = [
        title,
        title.replace("，", "， "),
        title.replace("：", "： "),
        " ".join(title),  # spaced out
    ]

    for variant in title_variants:
        # Try to find title and take everything from it onward
        idx = full_text.find(variant)
        if idx > 0 and idx < 200:  # Only split if title is near the start
            full_text = full_text[idx:]
            break

    return full_text


def process_text(text, title):
    """Process extracted text into clean Markdown paragraphs.

    pdftotext breaks lines at column width but doesn't always insert blank lines
    between paragraphs. Paragraph boundaries are detected by:
    1. Empty lines (always a break)
    2. Previous line ends with sentence-ending punctuation (。！？」）》) AND is reasonably long
    """
    SENTENCE_ENDERS = set("。！？」）》")
    lines = text.split('\n')

    # Remove the chapter title from the first line(s)
    title_normalized = title.replace(" ", "")
    cleaned_lines = []
    title_found = False
    for line in lines:
        stripped = line.strip()
        if not title_found and stripped:
            if title_normalized in stripped.replace(" ", ""):
                title_found = True
                continue
        cleaned_lines.append(line)

    if not title_found:
        cleaned_lines = lines

    # Build paragraphs with proper detection
    paragraphs = []
    current_para = []

    for line in cleaned_lines:
        stripped = line.strip()

        # Empty line = definite paragraph break
        if not stripped:
            if current_para:
                paragraphs.append("".join(current_para))
                current_para = []
            continue

        # Check if this is a list item
        if stripped.startswith(("●", "•", "○")):
            if current_para:
                paragraphs.append("".join(current_para))
                current_para = []
            paragraphs.append("- " + stripped.lstrip("●•○ ").strip())
            continue

        # If current_para has content and previous line ended with sentence punctuation,
        # this line starts a new paragraph
        if current_para:
            prev_text = current_para[-1]
            if prev_text and prev_text[-1] in SENTENCE_ENDERS:
                # Previous line ended a sentence -> start new paragraph
                paragraphs.append("".join(current_para))
                current_para = []

        current_para.append(stripped)

    if current_para:
        paragraphs.append("".join(current_para))

    # Post-process: detect sub-section headers
    # Must be: 4+ chars, no ending punctuation, surrounded by longer paragraphs,
    # and not a single word / table cell
    TABLE_CELL_WORDS = {"高", "低", "中", "无", "是", "否", "好", "差", "有", "大", "小"}
    processed = []
    for i, para in enumerate(paragraphs):
        # Remove empty list items
        if para.strip() == "-" or para.strip() == "- ":
            continue
        if para.startswith("- "):
            processed.append(para)
            continue

        # Skip empty paragraphs
        if not para.strip():
            continue

        # Detect sub-section headers: strict criteria
        stripped = para.strip()
        is_header_length = 4 <= len(stripped) <= 30  # min 4 chars to avoid table cells
        no_end_punct = stripped[-1] not in SENTENCE_ENDERS if stripped else True
        not_quote = not stripped.startswith(("\u300c", "\u300e", "\u300a", "\u201c"))
        has_content_around = (i > 0 and i < len(paragraphs) - 1)
        not_table_cell = stripped not in TABLE_CELL_WORDS
        # Require neighbors to be actual paragraphs (>20 chars)
        prev_is_para = i > 0 and len(paragraphs[i-1]) > 20
        next_is_para = i < len(paragraphs) - 1 and len(paragraphs[i+1]) > 20

        if (is_header_length and no_end_punct and not_quote and
                has_content_around and not_table_cell and
                (prev_is_para or next_is_para) and
                not any(c in stripped for c in "，、；：（）")):
            processed.append(f"\n## {stripped}\n")
            continue

        processed.append(para)

    # Join paragraphs with double newlines
    result = "\n\n".join(processed)

    # Convert footnote references [1] -> [^1]
    result = re.sub(r'\[(\d+)\]', r'[^\1]', result)

    # Clean up excessive whitespace
    result = re.sub(r'\n{3,}', '\n\n', result)

    return result.strip()


def convert_to_simplified(text):
    """Convert Traditional Chinese to Simplified Chinese."""
    return cc.convert(text)


def get_chapter_images(start_page, end_page):
    """Get list of images that belong to this chapter's page range."""
    images = []
    for img_idx, page in IMAGE_PAGES.items():
        if img_idx in SKIP_IMAGES:
            continue
        if start_page <= page <= end_page:
            src_file = IMAGES_SRC / f"img-{img_idx:03d}.jpg"
            if src_file.exists():
                images.append((img_idx, page, src_file))
    return sorted(images, key=lambda x: x[1])


def optimize_image(src_path, dst_path, max_width=1200):
    """Optimize image: resize if too large, save as JPEG."""
    img = Image.open(src_path)

    # Convert grayscale to RGB for consistent output
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # Resize if wider than max_width
    if img.width > max_width:
        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((max_width, new_height), Image.LANCZOS)

    img.save(dst_path, 'JPEG', quality=85, optimize=True)


def generate_markdown(filename, title, text, images):
    """Generate final Markdown file with frontmatter and images."""
    # Convert title to simplified
    title_sc = convert_to_simplified(title)

    # Build frontmatter
    md = f"""---
title: "{title_sc}"
---

# {title_sc}

"""

    # If there are images, insert them
    # Strategy: place images at the beginning of the chapter or find caption text
    image_refs = []
    for img_idx, page, src_path in images:
        img_name = f"img-{img_idx:03d}.jpg"
        image_refs.append(f"![](/images/{img_name})")

    # For the text, insert image references at appropriate positions
    # Simple strategy: insert images between paragraphs near where they appear
    if image_refs and len(image_refs) <= 3:
        # Few images: place them after the first paragraph
        paras = text.split("\n\n", 1)
        if len(paras) > 1:
            text = paras[0] + "\n\n" + "\n\n".join(image_refs) + "\n\n" + paras[1]
        else:
            text = "\n\n".join(image_refs) + "\n\n" + text
    elif image_refs:
        # Many images: distribute them evenly through the text
        paras = text.split("\n\n")
        interval = max(1, len(paras) // (len(image_refs) + 1))
        for i, ref in enumerate(image_refs):
            insert_pos = min((i + 1) * interval, len(paras))
            paras.insert(insert_pos + i, ref)  # +i to account for previous insertions
        text = "\n\n".join(paras)

    md += text + "\n"

    return md


def main():
    # Create output directories
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DST.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("CZ Memoir PDF → Simplified Chinese Markdown")
    print("=" * 60)

    # Process each chapter
    for filename, title, start_page, end_page in CHAPTERS:
        print(f"\n📖 Processing: {title} (pages {start_page}-{end_page})")

        # Extract text
        raw_text = extract_chapter_text(start_page, end_page, title)

        # Process text (clean up, merge paragraphs)
        processed_text = process_text(raw_text, title)

        # Convert to Simplified Chinese
        simplified_text = convert_to_simplified(processed_text)

        # Get and process images for this chapter
        chapter_images = get_chapter_images(start_page, end_page)
        for img_idx, page, src_path in chapter_images:
            dst_path = IMAGES_DST / f"img-{img_idx:03d}.jpg"
            if not dst_path.exists():
                optimize_image(src_path, dst_path)
                print(f"  🖼️  Image: img-{img_idx:03d}.jpg (page {page})")

        # Generate Markdown
        md_content = generate_markdown(filename, title, simplified_text, chapter_images)

        # Write file
        output_file = OUTPUT_DIR / f"{filename}.md"
        output_file.write_text(md_content, encoding='utf-8')
        print(f"  ✅ Written: {filename}.md ({len(simplified_text)} chars)")

    # Copy cover image separately (high quality)
    cover_src = IMAGES_SRC / "img-000.jpg"
    cover_dst = IMAGES_DST / "cover.jpg"
    if cover_src.exists() and not cover_dst.exists():
        shutil.copy2(cover_src, cover_dst)
        print(f"\n🖼️  Cover image copied")

    print(f"\n{'=' * 60}")
    print(f"✅ Done! {len(CHAPTERS)} chapters extracted to {OUTPUT_DIR}")
    print(f"📸 Images saved to {IMAGES_DST}")


if __name__ == "__main__":
    main()
