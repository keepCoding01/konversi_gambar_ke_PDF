import streamlit as st
import requests
import os
from PIL import Image
from io import BytesIO

def uploadAndConvert():
    st.title("🖼️ Konversi Gambar ke PDF Gratis")
    st.write("Unggah gambar dan konversikan ke PDF dalam satu klik!")
    
    uploadedFiles = st.file_uploader("Pilih gambar", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    st.write("Jumlah file yang diunggah:", len(uploadedFiles))

    
    orientation = st.radio("Pilih orientasi halaman:", ["Potret", "Lanskap"])
    pageSize = st.selectbox("Pilih ukuran halaman:", ["Sama dengan gambar", "A4", "Letter"])
    marginSize = st.radio("Pilih ukuran margin:", ["Tidak ada margin", "Kecil", "Besar"])
    
    if uploadedFiles:
        st.subheader("Preview Gambar")
        cols = st.columns(3)
        images = []
        for idx, file in enumerate(uploadedFiles):
            img = Image.open(file).convert("RGB")
            images.append(img)
            cols[idx % 3].image(img, caption=file.name, use_container_width=True)
        
        if st.button("Konversi ke PDF ✨"):
            if images:
                pdfBytes = convertImagesToPdf(images, orientation, pageSize, marginSize)
                st.success("✅ PDF berhasil dibuat!")
                st.download_button("📥 Download PDF", pdfBytes, "gambar_ke_pdf.pdf", "application/pdf")
            else:
                st.error("⚠️ Tidak ada gambar yang dapat dikonversi!")

def convertImagesToPdf(images, orientation, pageSize, marginSize):
    sizes = {"A4": (595, 842), "Letter": (612, 792)}
    margins = {"Tidak ada margin": 0, "Kecil": 10, "Besar": 30}
    margin = margins[marginSize]
    
    processedImages = []
    for img in images:
        if pageSize == "Sama dengan gambar":
            newSize = img.size
        else:
            newSize = sizes[pageSize]
        
        if orientation == "Lanskap":
            newSize = (newSize[1], newSize[0])
        
        newImg = Image.new("RGB", newSize, "white")
        imgResized = img.resize((newSize[0] - 2*margin, newSize[1] - 2*margin))
        newImg.paste(imgResized, (margin, margin))
        processedImages.append(newImg)
    
    # Menyimpan semua gambar ke dalam satu PDF tanpa terpisah
    pdfBuffer = BytesIO()
    processedImages[0].save(pdfBuffer, save_all=True, append_images=processedImages[1:], resolution=100.0, quality=95, optimize=True, format="PDF")
    pdfBuffer.seek(0)
    return pdfBuffer

if __name__ == "__main__":
    st.set_page_config(page_title="Konversi Gambar ke PDF", page_icon="📄", layout="wide")
    uploadAndConvert()
    
