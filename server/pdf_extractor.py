"""
PDF Extractor – Store text and images into variables
Run:  python pdf_extractor_vars.py
Make sure you have:  pip install PyMuPDF
"""

import fitz  
from moviepy.editor import VideoFileClip, concatenate_videoclips, ImageClip, CompositeVideoClip

import os

def extract_text_and_images(pdf_path):
    text_from_pdf = ""
    images_from_pdf = [] 

    with fitz.open(stream=pdf_path.read(), filetype="pdf") as doc:
        print(f"Opened PDF: {pdf_path}")
        print(f"Total pages: {len(doc)}")

        for page_num, page in enumerate(doc, start=1):
            print(f"\n=== Processing Page {page_num} ===")

            page_text = page.get_text()
            text_from_pdf += f"\n--- Page {page_num} ---\n" + (page_text or "")
            # print(f"Extracted {len(page_text)} characters of text")

            image_list = page.get_images(full=True)
            if image_list:
                print(f"Found {len(image_list)} image(s)")
            for img_index, img in enumerate(image_list, start=1):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                images_from_pdf.append({
                    "page": page_num,
                    "index": img_index,
                    "ext": image_ext,
                    "bytes": image_bytes
                })
                # print(f"   Stored image {img_index} from page {page_num} ({image_ext})")
                # print(image_list)

    print("\n Extraction complete!")
    return text_from_pdf, images_from_pdf

def combine_videos(video_files, output_path="videos/final_combined.mp4"):
    video_files = [vf for vf in video_files if os.path.exists(vf)]

    if not video_files:
        print("⚠️ No video clips found to combine.")
        return None  # prevents crash

    clips = [VideoFileClip(vf) for vf in video_files]
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    print(f"✅ Combined {len(clips)} clips → {output_path}")
    return output_path

