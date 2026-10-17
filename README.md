# GenAI Application

## Project Information

**Nama Project:**

GenAI Issue Triager API

**Use Case:**

Bug / Issue Report Triager (Mengubah laporan error atau keluhan teknis yang berantakan dari pengguna menjadi catatan berkode JSON yang rapi untuk membantu tim pembuat aplikasi).

**Deskripsi Singkat:**

Aplikasi backend yang dibuat dengan FastAPI dan Groq LLM API untuk memeriksa laporan masalah atau error secara otomatis. Aplikasi ini bisa mencari tingkat bahaya error, ringkasan masalah, cara memicu eror kembali, dan saran perbaikan agar tim QA dan developer bisa bekerja lebih cepat.

------------------------------------------------------

## Tech Stack

Tuliskan teknologi yang digunakan.

- Python 3.12.10
- FastAPI
- Pydantic
- Groq API
- openai/gpt-oss-120b
- python-dotenv

------------------------------------------------------

## Application Flow

Jelaskan menggunakan bahasa kalian sendiri bagaimana aplikasi bekerja dari:

```text
User Input
↓
FastAPI
↓
LLM API
↓
Structured Output
```

Penjelasan kalian:

- Pengguna mengirimkan request lewat `HTTP POST` ke endpoint `/analyze`. Request tersebut dikirim dalam bentuk kode JSON yang isinya teks laporan error dan pilihan `prompt_version` yakni A, B, atau C.
- FastAPI menerima request tersebut lalu memeriksa apakah isinya sudah lengkap dan jumlah hurufnya pas menggunakan aturan dari Pydantic melalui `AnalyzeRequest`. Jika sudah benar, aplikasi akan mengambil `GROQ_API_KEY` dari file `.env` dan menyatukan kalimat perintah sistem sesuai versi yang dipilih dengan teks laporan dari pengguna.
- Aplikasi mengirimkan pesan tersebut secara asynchronous ke server Groq. Model yang digunakan adalah `openai/gpt-oss-120b` dengan tingkat kreativitas yang rendah atau temperature sebesar 0.2 agar hasil pemeriksaannya selalu sama, teratur, dan jujur.
- Setelah mendapat balasan dari LLM, alat pembaca kode berupa `parse_llm_output` akan menghapus tanda ketik yang tidak perlu atau markdown. Teks itu kemudian diubah menjadi kode JSON dan diperiksa kembali agar isinya pas dengan kolom yang sudah ditentukan, yaitu `severity_level`, `summary`, `reproduction_steps`, dan `recommended_action`, sebelum dikirim balik ke pengguna.

------------------------------------------------------

## API Endpoint

Tuliskan endpoint utama aplikasi.

Contoh:

```text
POST /analyze
```

Endpoint kalian:

```text
POST /analyze
```

------------------------------------------------------

## Example Request

Masukkan salah satu request aktual yang digunakan ketika testing.

```json
{
  "text": "Bapak saya selalu mengeluh kalau kuota internetnya habis padahal saat cek di aplikasi MyTelkomsel masih banyak dan bahkan menumpuk kuotanya",
  "prompt_version": "C"
}
```

------------------------------------------------------

## Example Response

Masukkan actual response dari aplikasi.

```json
{
  "prompt_version": "C",
  "is_valid_json": true,
  "structured_data": {
    "severity_level": "MEDIUM",
    "summary": "Pengguna melaporkan kuota internet terlihat habis padahal di aplikasi MyTelkomsel masih ada dan bahkan menumpuk.",
    "reproduction_steps": [
      "Langkah reproduksi tidak disebutkan secara spesifik"
    ],
    "recommended_action": "Lakukan investigasi sinkronisasi data kuota antara sistem penagihan dan aplikasi MyTelkomsel, periksa log penggunaan, validasi algoritma penghitungan kuota, serta pastikan tidak ada delay atau kesalahan pada pembaruan status kuota di perangkat pengguna."
  },
  "raw_output": null
}
```

------------------------------------------------------

# Structured Output

Tuliskan structured output/schema yang digunakan pada aplikasi.

```json
{
  "severity_level": "LOW | MEDIUM | HIGH | CRITICAL",
  "summary": "string",
  "reproduction_steps": [
    "string"
  ],
  "recommended_action": "string"
}
```

### Kenapa kalian memilih field-field tersebut?

Jelaskan berdasarkan fungsi aplikasi kalian.

Keempat field ini dipilih agar keluhan awal yang berantakan dari pengguna bisa langsung diubah menjadi catatan tugas yang siap dikerjakan oleh tim QA maupun tim developer:
- `severity_level`: Membantu tim menentukan mana masalah yang harus buru-buru diperbaiki sekarang dan mana yang bisa ditunda nanti.
- `summary`: Memberikan inti masalah secara singkat dengan maksimal 2 kalimat supaya tim tidak perlu membaca cerita pengguna yang panjang lebar.
- `reproduction_steps`: Membantu tim QA untuk mencoba ulang error tersebut secara berurutan, sekaligus melihat apakah cerita dari pengguna sudah jelas atau masih kurang.
- `recommended_action`: Memberikan hipotesis awal dan langkah investigasi pertama yang bisa langsung dicoba oleh tim engineer.

------------------------------------------------------

# Prompt Experiment

Gunakan input yang sama untuk Prompt A, Prompt B, dan Prompt C.

## Input yang Digunakan

```text
Bapak saya selalu mengeluh kalau kuota internetnya habis padahal saat cek di aplikasi MyTelkomsel masih banyak dan bahkan menumpuk kuotanya

```

------------------------------------------------------

## Prompt A

Tuliskan prompt yang digunakan.

```text
Bapak saya selalu mengeluh kalau kuota internetnya habis padahal saat cek di aplikasi MyTelkomsel masih banyak dan bahkan menumpuk kuotanya
```

### Actual Output A

Masukkan actual output dari aplikasi.

```json
{
  "prompt_version": "A",
  "is_valid_json": false,
  "structured_data": null,
  "raw_output": "Ringkasannya: Ayahnya mengeluh kuota internetnya habis, padahal saat dicek di aplikasi MyTelkomsel ternyata masih banyak bahkan ada kuota yang menumpuk."
}
```

------------------------------------------------------

## Prompt B

Tuliskan prompt yang digunakan.

```text
Bapak saya selalu mengeluh kalau kuota internetnya habis padahal saat cek di aplikasi MyTelkomsel masih banyak dan bahkan menumpuk kuotanya
```

### Actual Output B

Masukkan actual output dari aplikasi.

```json
{
  "prompt_version": "B",
  "is_valid_json": false,
  "structured_data": null,
  "raw_output": "**📝 Ringkasan Laporan**\n\n- **Masalah:** Pengguna (melalui orang tua) mengeluhkan bahwa kuota internet “habis” padahal di aplikasi **MyTelkomsel** masih menunjukkan kuota yang cukup / bahkan menumpuk.\n- **Gejala yang terlihat:**  \n  1. Tidak dapat mengakses internet (browser, aplikasi, dll).  \n  2. Pada pengaturan perangkat (Data Usage) atau notifikasi sistem muncul “kuota habis”.  \n  3. MyTelkomsel app menampilkan sisa kuota yang masih banyak.  \n\n---\n\n## 📊 Tingkat Keparahan (Severity)\n\n| Kriteria | Penilaian |\n|----------|-----------|\n| Dampak pada pengguna | **Tinggi** – layanan data tidak dapat dipakai meski kuota masih ada. |\n| Frekuensi | Dilaporkan secara berulang (setiap kali pakai). |\n| Area yang terdampak | Seluruh layanan data (browsing, streaming, aplikasi). |\n| Risiko bisnis | Potensi churn pelanggan & reputasi operator. |\n| **Severity** | **High (P2)** – harus diprioritaskan untuk investigasi segera. |\n\n---\n\n## 🔍 Analisis Awal & Kemungkinan Penyebab\n\n| Area | Kemungkinan Penyebab | Penjelasan |\n|------|----------------------|------------|\n| **1. Pengaturan Kuota di Device** | *Data limit / warning* di Android/iOS di‑set ke nilai yang lebih rendah daripada kuota sebenarnya. | Sistem akan memblokir data ketika limit tercapai, meski provider masih memberi kuota. |\n| **2. APN / Profil Jaringan** | APN yang tidak cocok atau profil data yang korup. | Data tidak diarahkan ke jaringan yang benar → paket tidak terhitung. |\n| **3. Cache / Sinkronisasi MyTelkomsel** | Aplikasi menampilkan data lama (cached) atau tidak sinkron dengan server. | Bisa menimbulkan “kuota masih ada” padahal di sisi jaringan sudah habis. |\n| **4. Dual‑SIM / Slot SIM** | Pengguna memakai slot SIM yang berbeda (misal SIM cadangan) atau SIM tidak terdeteksi dengan benar. | Sistem menganggap kuota SIM utama habis, padahal kuota di SIM lain masih ada. |\n| **5. Masalah di Backend Telkomsel** | Kesalahan pencatatan penggunaan di server (mis‑match antara OSS/BSS). | Kuota di server masih ada, tapi jaringan menolak paket karena error internal. |\n| **6. Aplikasi/OS Bug** | Bug pada UI atau modul “Data Usage” di OS yang menampilkan status “habis”. | Tidak mempengaruhi jaringan, hanya tampilan. |\n\n---\n\n## 🛠️ Langkah‑Langkah Reproduksi (Untuk QA)\n\n1. **Persiapan**  \n   - Siapkan perangkat Android (atau iOS) dengan SIM Telkomsel aktif.  \n   - Pastikan aplikasi **MyTelkomsel** ter‑install & login.  \n   - Catat versi OS, model perangkat, versi aplikasi MyTelkomsel.\n\n2. **Uji Awal**  \n   - Buka **Pengaturan → Data Usage** (atau **Penggunaan Data Seluler**) dan periksa apakah ada *limit* yang di‑enable.  \n   - Buka **MyTelkomsel** → lihat sisa kuota.\n\n3. **Simulasi Masalah**  \n   - Aktifkan **Data Mobile** dan coba akses internet (browser, YouTube, dll).  \n   - Jika tidak ada koneksi, perhatikan notifikasi sistem (“Kuota habis” atau “Data limit reached”).  \n   - Kembali ke MyTelkomsel, pastikan kuota masih terlihat >0.\n\n4. **Verifikasi APN**  \n   - Masuk ke **Pengaturan → Jaringan Seluler → Nama titik akses (APN)**.  \n   - Pastikan APN sesuai dengan standar Telkomsel (misal: `telkomsel`, `internet`).  \n\n5. **Cek Dual‑SIM**  \n   - Jika perangkat dual‑SIM, pastikan **Data Seluler** diarahkan ke SIM yang memiliki kuota.  \n\n6. **Clear Cache & Sync**  \n   - Pada MyTelkomsel: *Settings → Storage → Clear Cache* → *Force Stop* → *Open kembali*.  \n   - Lakukan **Pull‑to‑Refresh** pada halaman kuota.  \n\n7. **Log & Capture**  \n   - Ambil screenshot notifikasi “Kuota habis”.  \n   - Capture layar MyTelkomsel yang menampilkan sisa kuota.  \n   - Jika memungkinkan, aktifkan **Developer Options → Logcat** (Android) selama percobaan untuk mengumpulkan log jaringan.\n\n---\n\n## 💡 Saran Perbaikan Awal (Tindakan Cepat)\n\n| No | Tindakan | Penanggung Jawab | Prioritas |\n|----|----------|------------------|-----------|\n| 1 | **Matikan/Reset Data Limit** di pengaturan perangkat (Data Usage → Data limit). | QA / Support Frontline | High |\n| 2 | **Periksa & Set Ulang APN** ke nilai default Telkomsel. | Support Teknis | High |\n| 3 | **Bersihkan Cache MyTelkomsel** dan lakukan **re‑login**. | Support / QA | Medium |\n| 4 | **Pastikan SIM yang aktif** adalah SIM dengan kuota (jika dual‑SIM). | Support | Medium |\n| 5 | **Uji pada perangkat lain** (model/OS berbeda) untuk menilai apakah bug device‑specific. | QA | Medium |\n| 6 | **Jika semua di atas tidak menyelesaikan**, buat tiket ke **Tim Backend/OSS** dengan melampirkan: <br> - Screenshot notifikasi “Kuota habis”. <br> - Screenshot kuota di MyTelkomsel. <br> - Log jaringan (jika ada). <br> - Device model, OS version, APN config. | QA → Backend Team | High |\n| 7 | **Monitoring**: Setelah perbaikan, lakukan **smoke test** selama 24‑48 jam untuk memastikan data dapat dipakai kembali. | QA | High |\n\n---\n\n## 📋 Checklist Informasi Tambahan yang Diperlukan\n\n- Model perangkat (misal: Samsung Galaxy S23, Xiaomi Redmi 13, iPhone 15, dll).  \n- Versi sistem operasi (Android 13, iOS 17, dll).  \n- Versi aplikasi MyTelkomsel (nomor build).  \n- Apakah perangkat menggunakan **dual‑SIM**? Jika ya, slot mana yang dipilih untuk data?  \n- Apakah ada **VPN** atau aplikasi pengatur bandwidth yang ter‑install?  \n- Waktu kejadian (jam, zona waktu) – apakah terjadi pada jam sibuk atau setelah reset jaringan?  \n- Apakah masalah terjadi pada **semua jaringan** (3G/4G/5G) atau hanya satu?  \n\n---\n\n### 📌 Ringkasan Tindakan Selanjutnya\n\n1. **Langkah cepat di perangkat** – cek & matikan data limit, reset APN, bersihkan cache.  \n2. **Jika masih gagal**, kumpulkan bukti (screenshot, log) dan eskalasikan ke tim backend/OSS dengan informasi lengkap.  \n3. **Prioritaskan** karena dampak layanan data tinggi (Severity = High).  \n\nSemoga analisis ini membantu tim QA dan developer untuk mengidentifikasi akar masalah dan mempercepat perbaikan. Jika ada data tambahan, silakan kirimkan agar investigasi dapat dipercepat. 🚀"
}
```

------------------------------------------------------

## Prompt C

Tuliskan prompt yang digunakan.

```text
Bapak saya selalu mengeluh kalau kuota internetnya habis padahal saat cek di aplikasi MyTelkomsel masih banyak dan bahkan menumpuk kuotanya
```

### Actual Output C

Masukkan actual output dari aplikasi.

```json
{
  "prompt_version": "C",
  "is_valid_json": true,
  "structured_data": {
    "severity_level": "MEDIUM",
    "summary": "Pengguna melaporkan kuota internet terlihat habis padahal di aplikasi MyTelkomsel masih ada dan bahkan menumpuk.",
    "reproduction_steps": [
      "Langkah reproduksi tidak disebutkan secara spesifik"
    ],
    "recommended_action": "Lakukan investigasi sinkronisasi data kuota antara sistem penagihan dan aplikasi MyTelkomsel, periksa log penggunaan, validasi algoritma penghitungan kuota, serta pastikan tidak ada delay atau kesalahan pada pembaruan status kuota di perangkat pengguna."
  },
  "raw_output": null
}
```

------------------------------------------------------

# Prompt Evaluation

### Dari ketiga prompt tersebut, mana yang menurut kalian menghasilkan output paling baik?

Prompt C memberikan hasil yang paling bagus dan paling pas untuk dipasang ke sistem backend

### Kenapa?

1. Mudah dibaca komputer dimana prompt C menghasilkan kode JSON yang benar dan lolos pengecekan aturan Pydantic. Hasilnya, data bisa langsung disimpan ke database atau dipajang di layar pengguna tanpa perlu parsing manual yang rumit.
2. Tidak mengarang cerita dikarenakan laporan dari pengguna sangat pendek dan tidak menceritakan urutan kejadiannya, Prompt C mematuhi aturan dengan menuliskan `["Langkah reproduksi tidak disebutkan secara spesifik"]`. Sistem tidak mengarang-ngarang jawaban sendiri.
3. Singkat dan apa adanya dimana singkat cerita masalah dibatasi paling banyak 2 kalimat saja dan langsung memberikan saran perbaikan yang pas.

### Apa perbedaan paling terlihat antara Prompt A, Prompt B, dan Prompt C berdasarkan hasil testing kalian?

• Prompt A (Perintah Sederhana): Hanya menghasilkan 1 kalimat penjelasan ulang dalam bentuk teks biasa. Hasilnya tidak berwujud kode JSON yang benar. Di dalamnya juga tidak ada pemeriksaan masalah, tingkat bahaya eror, ataupun saran perbaikan.
• Prompt B (Perintah Berperan + Tugas + Situasi): Karena sudah diberi peran sebagai *Senior QA Engineer*, hasil pemeriksaannya menjadi sangat lengkap dan mendalam. Tapi, karena tidak diberi Constraint dan Output Format, sistem malah mengeluarkan tulisan teks panjang yang penuh tabel, emoji, dan 7 cara menguji eror yang dikarang-karang sendiri. Akibatnya, tulisan ini tidak bisa diubah menjadi kode JSON.
• Prompt C (Perintah Lengkap & Teratur): Menyatukan kehebatan pemeriksaan dari Prompt B dengan aturan batasan serta bentuk hasil akhir yang ketat. Hasilnya adalah kode JSON yang pas, selalu teratur, tidak mengarang cerita di luar laporan pengguna, dan langsung lolos pengecekan aturan Pydantic.

------------------------------------------------------

# Failure Case

### Input yang menghasilkan output kurang baik

```json
{
  "text": "Mantap sekali aplikasinya, tadi saya beli paket internet 100 ribu pakai GoPay, saldonya sudah kepotong dua kali sampai 200 ribu tapi paketnya gak aktif sama sekali. Terima kasih sudah bikin saldo saya ludes!",
  "prompt_version": "C"
}
```

### Actual Output

```json
{
  "prompt_version": "C",
  "is_valid_json": true,
  "structured_data": {
    "severity_level": "HIGH",
    "summary": "Pembelian paket internet 100 ribu via GoPay terpotong dua kali hingga 200 ribu, namun paket tidak aktif.",
    "reproduction_steps": [
      "Langkah reproduksi tidak disebutkan secara spesifik"
    ],
    "recommended_action": "Lakukan investigasi pada log transaksi pembayaran dan sistem provisioning: verifikasi duplikasi pemotongan, cek status aktivasi paket di backend, proses refund untuk pemotongan ganda, dan pastikan paket diaktifkan untuk pengguna."
  },
  "raw_output": null
}
```

### Menurut kalian apa masalah dari output tersebut?

Terdapat dua masalah utama pada output sebelum diperbaiki:
1. Penentuan `severity_level` kurang tepat: Laporan dari pengguna ini menyangkut masalah uang yang serius, yaitu saldo GoPay terpotong dua kali sebanyak Rp200.000 tapi paket internetnya tetap tidak aktif. Dalam pembuatan aplikasi, error yang bikin rugi uang secara langsung seperti ini wajib dimasukkan ke dalam kelompok CRITICAL, bukan cuma HIGH.
2. Gagal mencari cara memicu eror pada `reproduction_steps` dari cerita pengguna yang menyindir: Pengguna sebenarnya sudah menceritakan urutan kejadiannya yakni beli paket 100 ribu lewat GoPay lalu saldo kepotong dua kali lalu paket tidak aktif. Tapi, karena aturan pembatasan di awal terlalu kaku, LLM gagal mengubah cerita tersebut menjadi daftar urutan cara memicu eror dan malah menulis "Langkah reproduksi tidak disebutkan secara spesifik".

### Apa yang kalian ubah pada prompt / constraint / kode?

```text
Menambahkan dan memperjelas 3 aturan pada bagian Constraints di System Prompt C:
1. Instruksi untuk mengabaikan nada sarkasme dari pengguna.
2. Aturan yang jelas bahwa semua masalah tentang urusan uang, saldo kepotong dua kali, atau gagal bayar tapi saldo tetap berkurang WAJIB dimasukkan ke kelompok CRITICAL.
3. Instruksi agar LLM mengekstrak urutan kejadian dari cerita pengguna menjadi langkah-langkah memicu eror yang berurutan. Tulisan ['Langkah reproduksi tidak disebutkan secara spesifik'] hanya boleh ditulis kalau pengguna sama sekali tidak menceritakan urutan kejadiannya.
```

### Output setelah diperbaiki

```json
{
  "prompt_version": "C",
  "is_valid_json": true,
  "structured_data": {
    "severity_level": "CRITICAL",
    "summary": "Pembelian paket internet 100 ribu via GoPay terpotong saldo dua kali hingga 200 ribu, namun paket tidak aktif.",
    "reproduction_steps": [
      "Buka aplikasi dan pilih paket internet 100 ribu",
      "Pilih metode pembayaran GoPay dan konfirmasi pembelian",
      "Periksa saldo setelah transaksi (terpotong dua kali)",
      "Cek status paket di aplikasi (paket tidak aktif)"
    ],
    "recommended_action": "Lakukan investigasi pada log pembayaran dan callback GoPay untuk mendeteksi duplikasi transaksi, verifikasi alur aktivasi paket, dan proses refund atau kredit saldo untuk pengguna yang terkena potongan ganda."
  },
  "raw_output": null
}
```

------------------------------------------------------

# Personal Reflection

Jawab menggunakan pendapat dan pengalaman kalian sendiri selama mengerjakan project.

### 1. Menurut kalian, bagian apa yang paling sulit dari project ini?

Bagian yang paling sulit adalah mengatur Constraints pada System Prompt agar seimbang. Jika aturannya terlalu bebas, LLM suka mengarang-ngarang cerita sendiri tentang cara memicu eror yang sebenarnya tidak diceritakan oleh pengguna. Sebaliknya, jika aturannya terlalu kaku, LLM jadi gagal mengambil urutan kejadian dari cerita pengguna yang sifatnya curhat atau menyindir. Selain itu, memastikan hasil ketikan dari LLM selalu rapi mengikuti kode JSON dan lolos pemeriksaan aturan Pydantic juga butuh ketelitian.

### 2. Bagian kode mana yang paling banyak dibantu oleh AI?

Bagian kode yang paling banyak dibantu oleh AI adalah membantu pembuatan boilerplate alamat FastAPI, membantu pembuatan `parse_llm_output()` untuk menghapus tanda ketik yang tidak perlu sekaligus membantu memeriksa kode JSON ke aturan Pydantic, serta pengaturan pilihan `prompt_version` yakni A, B, C di dalam isi data agar ketiga percobaan perintah tersebut bisa langsung dicoba lewat satu endpoint `/analyze`.

### 3. Setelah melihat kode tersebut, jelaskan menggunakan bahasa kalian sendiri bagaimana bagian tersebut bekerja.

1. Ketika pengguna mengirim data ke alamat `POST /analyze`, FastAPI akan memeriksa isi data menggunakan aturan AnalyzeRequest untuk memastikan tulisan tidak kosong dan pilihan versi perintahnya adalah A, B, atau C.
2. `build_messages()` mengambil System Prompt dari daftar kamus perintah sesuai versi yang dipilih, lalu menyatukannya dengan teks laporan dari pengguna.
3. Aplikasi memanggil API Groq secara asynchronous menggunakan model `openai/gpt-oss-120b`, lalu menyimpan teks balasannya ke dalam `raw_result`.
4. `parse_llm_output()` kemudian menghapus tanda ketik yang tidak perlu dari teks tersebut, mengubah teks biasa menjadi bentuk kode JSON dengan perintah `json.loads()`, lalu memasukkannya ke aturan Pydantic `TriageStructuredOutput`.
5. Jika bentuk kode JSON dan keempat kolomnya cocok seperti pada Prompt C, aplikasi akan membalas dengan tulisan `is_valid_json: true` beserta data yang sudah rapi di `structured_data`. Jika hasilnya bukan kode JSON seperti pada Prompt A dan B, aplikasi tidak akan rusak atau Error 500, melainkan membalas dengan tulisan `is_valid_json: false` dan menampilkan teks asli apa adanya di `raw_output`.

### 4. Menurut kalian, apa kekurangan terbesar dari aplikasi yang kalian buat jika digunakan oleh user sungguhan?

1. Belum ada penyaring untuk ketikan yang bukan laporan error dimana pengguna memasukkan tulisan yang bukan masalah komputer seperti ucapan salam, pesan sampah/spam, atau pertanyaan umum, aplikasi tetap memaksa diri untuk memeriksanya sebagai laporan eror.
2. Belum bisa menyimpan data otomatis dimana hasil kode JSON yang sudah rapi hanya dikirim balik saat itu juga. Data tersebut belum disimpan otomatis ke dalam database ataupun ke alat pengatur tugas tim seperti Jira, Linear, atau GitHub Issues.
3. Hanya bisa menerima ketikan tulisan dimana di dunia nyata, laporan eror dari pengguna biasanya butuh bukti gambar berupa screenshot atau file catatan error.

### 5. Jika provider LLM kalian diganti, misalnya dari Groq ke Gemini atau OpenAI, bagian mana dari project yang menurut kalian perlu diubah?

Bagian yang perlu diganti hanya pada bagian penghubung LLM seperti:
1. Mengubah groq menjadi google-genai untuk memakai Gemini atau openai untuk memakai OpenAI.
2. Mengganti kode `GROQ_API_KEY` dan cara memanggilnya dengan kode kunci baru misalnya `OPENAI_API_KEY` dengan aturan `AsyncOpenAI()`.
3. Mengubah cara aplikasi memanggil server dari model `openai/gpt-oss-120b` ke model baru dari perusahaan penyedia yang dipilih misalnya memakai `gemini-4-argon` atau `gpt-6-astra`).

### 6. Setelah mencoba aplikasi kalian sendiri, apa satu improvement yang menurut kalian paling penting jika project ini dilanjutkan?

Menambahkan field validasi awal seperti True atau False dari `is_valid_bug_report` dan `issue_category` seperti contoh Urusan Uang, Jaringan Internet, Tampilan Aplikasi, atau Akun pada bentuk output. Selain itu, membuat sistem pengiriman pesan otomatis atau webhook ke grup komunikasi tim pembuat aplikasi seperti Slack, Discord, atau Telegram. Pesan otomatis ini akan langsung dikirim jika ada laporan masuk yang terdeteksi memiliki `severity_level: "CRITICAL"`, supaya masalah uang seperti saldo yang terpotong dua kali bisa langsung diperbaiki saat itu juga.

------------------------------------------------------

# AI Usage

### AI tools yang digunakan

Google Gemini

### AI digunakan untuk membantu bagian apa?

• Membantu susunan dasar untuk aplikasi FastAPI yakni `main.py` dan aturan pengecekan data Pydantic seperti `AnalyzeRequest`, `TriageStructuredOutput`, `APIResponse`.
• Membantu `parse_llm_output()` untuk mengatur pembacaan hasil akhir, baik yang berbentuk kode JSON maupun yang berupa teks biasa selama percobaan perintah A, B, dan C.

### Bagian apa yang kalian tentukan, perbaiki, atau ubah sendiri setelah melihat hasil dari AI?

1. Saat kode awal dari AI dijalankan, muncul `error 404 model_not_found` karena model `llama-3.3-70b-versatile` sudah tidak bisa dipakai lagi. Saya memperbaikinya dengan menggantinya ke `openai/gpt-oss-120b` dan menyesuaikan aturan cara memanggilnya.
2. Saya menentukan sendiri teks laporan yang akan dicoba berdasarkan masalah nyata pengguna di Indonesia, yaitu masalah kuota MyTelkomsel yang tidak sama (tidak sinkron) serta kasus keluhan sindiran tentang saldo GoPay yang terpotong dua kali.
3. Setelah melihat bahwa hasil awal pada kasus GoPay hanya memberikan tingkat bahaya HIGH dan gagal mencari langkah-langkah memicu error, saya mengubah bagian Constraints pada SYSTEM_PROMPTS["C"]. Saya atur agar masalah uang langsung dimasukkan ke kelompok CRITICAL dan menyuruh sistem mengambil langkah memicu error dari cerita curhat si pengguna.

------------------------------------------------------

# Checklist

- [x] Project bisa dijalankan.
- [x] FastAPI bisa dibuka melalui `/docs`.
- [x] LLM API berhasil digunakan.
- [x] Minimal terdapat 1 endpoint `POST`.
- [x] API Key disimpan menggunakan `.env`.
- [x] `.env` tidak masuk repository GitHub.
- [x] Structured output memiliki minimal 3 field.
- [x] Prompt A sudah diuji.
- [x] Prompt B sudah diuji.
- [x] Prompt C sudah diuji.
- [x] Actual output ketiga prompt sudah dimasukkan ke README.
- [x] Minimal 1 failure case ditemukan.
- [x] Failure case sudah dicoba diperbaiki.
- [x] Personal Reflection sudah dijawab.
- [x] AI Usage sudah dijelaskan.
- [x] `requirements.txt` tersedia.
- [x] Project sudah di-push ke GitHub.
- [x] Link repository GitHub sudah siap dikumpulkan.