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

- Pengguna mengirimkan request lewat HTTP POST ke endpoint /analyze. Request tersebut dikirim dalam bentuk kode JSON yang isinya teks laporan error dan pilihan prompt_version yakni A, B, atau C.
- FastAPI menerima request tersebut lalu memeriksa apakah isinya sudah lengkap dan jumlah hurufnya pas menggunakan aturan dari Pydantic melalui AnalyzeRequest. Jika sudah benar, aplikasi akan mengambil GROQ_API_KEY dari file .env dan menyatukan kalimat perintah sistem sesuai versi yang dipilih dengan teks laporan dari pengguna.
- 

------------------------------------------------------

## API Endpoint

Tuliskan endpoint utama aplikasi.

Contoh:

```text
POST /analyze
```

Endpoint kalian:

```text
[ISI SENDIRI]
```

------------------------------------------------------

## Example Request

Masukkan salah satu request aktual yang digunakan ketika testing.

```json
[ISI SENDIRI]
```

------------------------------------------------------

## Example Response

Masukkan actual response dari aplikasi.

```json
[ISI SENDIRI]
```

------------------------------------------------------

# Structured Output

Tuliskan structured output/schema yang digunakan pada aplikasi.

```json
[ISI SENDIRI]
```

### Kenapa kalian memilih field-field tersebut?

Jelaskan berdasarkan fungsi aplikasi kalian.

[ISI SENDIRI]

------------------------------------------------------

# Prompt Experiment

Gunakan input yang sama untuk Prompt A, Prompt B, dan Prompt C.

## Input yang Digunakan

```text
[ISI SENDIRI]
```

------------------------------------------------------

## Prompt A

Tuliskan prompt yang digunakan.

```text
[ISI SENDIRI]
```

### Actual Output A

Masukkan actual output dari aplikasi.

```json
[ISI SENDIRI]
```

------------------------------------------------------

## Prompt B

Tuliskan prompt yang digunakan.

```text
[ISI SENDIRI]
```

### Actual Output B

Masukkan actual output dari aplikasi.

```json
[ISI SENDIRI]
```

------------------------------------------------------

## Prompt C

Tuliskan prompt yang digunakan.

```text
[ISI SENDIRI]
```

### Actual Output C

Masukkan actual output dari aplikasi.

```json
[ISI SENDIRI]
```

------------------------------------------------------

# Prompt Evaluation

### Dari ketiga prompt tersebut, mana yang menurut kalian menghasilkan output paling baik?

[ISI SENDIRI]

### Kenapa?

[ISI SENDIRI]

### Apa perbedaan paling terlihat antara Prompt A, Prompt B, dan Prompt C berdasarkan hasil testing kalian?

[ISI SENDIRI]

------------------------------------------------------

# Failure Case

### Input yang menghasilkan output kurang baik

```json
[ISI SENDIRI]
```

### Actual Output

```json
[ISI SENDIRI]
```

### Menurut kalian apa masalah dari output tersebut?

[ISI SENDIRI]

### Apa yang kalian ubah pada prompt / constraint / kode?

```text
[ISI SENDIRI]
```

### Output setelah diperbaiki

```json
[ISI SENDIRI]
```

------------------------------------------------------

# Personal Reflection

Jawab menggunakan pendapat dan pengalaman kalian sendiri selama mengerjakan project.

### 1. Menurut kalian, bagian apa yang paling sulit dari project ini?

[ISI SENDIRI]

### 2. Bagian kode mana yang paling banyak dibantu oleh AI?

[ISI SENDIRI]

### 3. Setelah melihat kode tersebut, jelaskan menggunakan bahasa kalian sendiri bagaimana bagian tersebut bekerja.

[ISI SENDIRI]

### 4. Menurut kalian, apa kekurangan terbesar dari aplikasi yang kalian buat jika digunakan oleh user sungguhan?

[ISI SENDIRI]

### 5. Jika provider LLM kalian diganti, misalnya dari Groq ke Gemini atau OpenAI, bagian mana dari project yang menurut kalian perlu diubah?

[ISI SENDIRI]

### 6. Setelah mencoba aplikasi kalian sendiri, apa satu improvement yang menurut kalian paling penting jika project ini dilanjutkan?

[ISI SENDIRI]

------------------------------------------------------

# AI Usage

### AI tools yang digunakan

[ISI SENDIRI]

### AI digunakan untuk membantu bagian apa?

[ISI SENDIRI]

### Bagian apa yang kalian tentukan, perbaiki, atau ubah sendiri setelah melihat hasil dari AI?

[ISI SENDIRI]

------------------------------------------------------

# Checklist

- [ ] Project bisa dijalankan.
- [ ] FastAPI bisa dibuka melalui `/docs`.
- [ ] LLM API berhasil digunakan.
- [ ] Minimal terdapat 1 endpoint `POST`.
- [ ] API Key disimpan menggunakan `.env`.
- [ ] `.env` tidak masuk repository GitHub.
- [ ] Structured output memiliki minimal 3 field.
- [ ] Prompt A sudah diuji.
- [ ] Prompt B sudah diuji.
- [ ] Prompt C sudah diuji.
- [ ] Actual output ketiga prompt sudah dimasukkan ke README.
- [ ] Minimal 1 failure case ditemukan.
- [ ] Failure case sudah dicoba diperbaiki.
- [ ] Personal Reflection sudah dijawab.
- [ ] AI Usage sudah dijelaskan.
- [ ] `requirements.txt` tersedia.
- [ ] Project sudah di-push ke GitHub.
- [ ] Link repository GitHub sudah siap dikumpulkan.