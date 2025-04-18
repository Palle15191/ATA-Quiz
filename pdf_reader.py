import fitz  # PyMuPDF
import json
import os

def extract_pdf_data(pdf_path, output_dir="data"):
    doc = fitz.open(pdf_path)
    full_text = ""
    images = []

    if not os.path.exists(f"{output_dir}/bilder"):
        os.makedirs(f"{output_dir}/bilder")

    for i, page in enumerate(doc):
        full_text += page.get_text()

        img_list = page.get_images(full=True)
        for img_index, img in enumerate(img_list):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n < 5:  # RGB oder Graustufen
                img_path = f"{output_dir}/bilder/page_{i+1}_img_{img_index+1}.png"
                pix.save(img_path)
                images.append({"page": i+1, "path": img_path})
            pix = None

    with open(f"{output_dir}/extracted_text.json", "w", encoding="utf-8") as f:
        json.dump({"text": full_text, "images": images}, f, ensure_ascii=False, indent=2)

    print(f"✅ Text & Bilder gespeichert unter {output_dir}/")

# ==== Hier startest du das Script direkt ====
if __name__ == "__main__":
    extract_pdf_data(r"G:\KI-Quiz2\data\ebook.pdf")  # <--- Dein Pfad zur PDF