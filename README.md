# 🎮 Flappy Bird - Tugas Besar Pengolahan Citra Digital

Game ini dibuat untuk memenuhi tugas besar mata kuliah **Pengolahan Citra Digital** yang dikembangkan menggunakan **Python**, **Pygame**, dan **MediaPipe**.  
Kontrol permainan dilakukan menggunakan **gerakan wajah melalui webcam**, tanpa keyboard atau mouse.

## 👩‍💻 Identitas Mahasiswa
- Nama: Salwa  
- NIM: 4.33.23.2.25  
- Kelas: TI-2C  
- Prodi: D4 Teknologi Rekayasa Komputer  
- Mata Kuliah: Pengolahan Citra Digital  
- Dosen Pengampu: Prayitno, S.ST., M.T., PH.D.

## 📌 Fitur Game
- Kontrol burung menggunakan gerakan wajah (MediaPipe + OpenCV)
- Sistem skor dan high score tersimpan otomatis (`high_score.txt`)
- Level meningkat setiap 10 detik (rintangan makin cepat)
- Tampilan skor dan level real-time
- Tampilan Game Over lengkap dengan tombol "Try Again" dan "Exit"
- Efek suara (mulai, tabrakan, skor, game over) dan musik latar

## ▶️ Cara Menjalankan
1. Pastikan Python 3.7+ sudah terinstal di perangkat
2. Install dependency dengan perintah:
    pip install pygame opencv-python mediapipe
3. Jalankan game dengan:
    python main.py
4. Pastikan webcam aktif dan wajah terlihat jelas

## 📁 Struktur Folder

📁 assets/
│ ├── bird_sprite.png
│ ├── canonical_face_model_uv_visualization.png
│ ├── game-over.mp3
│ ├── game-start.mp3
│ ├── pipe_sprite_single.png
│ ├── point.mp3
│ ├── PressStart2P.ttf
│ ├── punch-impact.mp3
│ └── sneaky-guitar-loop.mp3
.gitignore
high_score.txt
main.py
README.md


## 💡 Catatan
- Game **tidak bisa dijalankan di Google Colab** karena Colab tidak mendukung webcam dan audio interaktif.
- Disarankan dijalankan langsung di komputer lokal melalui terminal atau VSCode.
- Gunakan pencahayaan yang cukup agar deteksi wajah berjalan lancar.
- Musik latar dan efek suara otomatis aktif. Pastikan volume perangkat tidak dalam keadaan mute.

## 🎥 Inspirasi Proyek
Proyek ini terinspirasi dari video YouTube berjudul  
**[Head-Tracking Flappy Bird](https://www.youtube.com/watch?v=Tm7Iy6_YW1w)**  
yang memanfaatkan pelacakan wajah untuk mengontrol permainan secara hands-free.

---

Dikembangkan sebagai bagian dari tugas besar semester 4.  
Terima kasih telah mencoba dan bermain 🎉
