# Pembacaan Formulir dengan Gemini

## 1. Instalasi

1. Install the environment
   1. Opsi 1 : pakai `virtualenv`
      1. Install `virtualenv` library to create the isolated environment: `python -m pip install virtualenv`
      2. Bikin virtual environent-nya: `python -m virtualenv .venv`
      3. Aktivasi environemnt-nya dengan command: `./venv/Script/activate`
   2. Opsi 2: pakai `conda`
      1. Bikin virtual environent-nya: `conda create --name ocr_gemini python=3.12`
      2. Aktifkan environment baru dengan: `conda activate ocr_gemini`
2. Install library-nya: `pip install -r requirements.txt`
3. Dapatkan API key buat Gemini dari Google AI Studio. Dan masukkan key tersbut ke dalam file `.env`

## 2. Jalankan server-nya

Aktifkan environment-nya sebelum mulai menjalankan server.

```
conda activate ocr_gemini
```

Jalankan command berikut untuk memulai server.

```
python app.py
```

## 3. Uji Coba

Jalankan simulasi client yang ada di `client_example.py`. Silahkan ganti file gambar di script tersebut dengan mengganti variabel `IMAGE_PATH`

```
python client_example.py
```