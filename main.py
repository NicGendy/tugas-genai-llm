import json
import os
from typing import Any, Literal
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from groq import AsyncGroq, GroqError
from pydantic import BaseModel, Field, ValidationError

load_dotenv()

app = FastAPI(
    title="GenAI Issue Triager API",
    description="API berbasis LLM untuk menganalisis laporan bug/issue menjadi structured output.",
    version="1.0.0",
)


# Aturan Pydantic untuk request body dan response model
class AnalyzeRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=10,
        max_length=4000,
        description="Teks laporan issue atau bug dari user.",
        examples=["Aplikasi MyTelkomsel langsung keluar sendiri (force close) tiap kali saya coba ganti foto profil pakai foto resolusi tinggi."]
    )
    prompt_version: Literal["A", "B", "C"] = Field(
        default="C",
        description="Pilih versi prompt untuk eksperimen (A: Simple, B: Role+Task+Context, C: Full Structured)."
    )


class TriageStructuredOutput(BaseModel):
    severity_level: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    summary: str
    reproduction_steps: list[str]
    recommended_action: str


class APIResponse(BaseModel):
    prompt_version: str
    is_valid_json: bool
    structured_data: TriageStructuredOutput | None = None
    raw_output: str | None = None


# Daftar prompt sistem untuk berbagai versi
SYSTEM_PROMPTS: dict[str, str] = {
    "A": "You are a helpful assistant.",
    "B": (
        "Role: Kamu adalah Senior QA Engineer dan Bug Triager.\n"
        "Context: Tim developer menerima banyak laporan masalah teknis dari pengguna aplikasi setiap hari "
        "dengan gaya bahasa yang tidak terstruktur.\n"
        "Task: Analisis laporan masalah dari pengguna, tentukan tingkat keparahannya, rangkum intinya, "
        "dan berikan langkah reproduksi serta saran perbaikan awal."
    ),
    # Sebelum Failure Case
    # "C": (
    #     "Role: Kamu adalah Senior QA Engineer dan Bug Triager.\n"
    #     "Context: Tim engineering membutuhkan sistem otomatis untuk mengubah laporan bug mentah dari user "
    #     "menjadi tiket teknis terstruktur yang siap dimasukkan ke database.\n"
    #     "Task: Analisis teks laporan user dan ekstrak tingkat keparahan, ringkasan teknis, langkah reproduksi, "
    #     "serta rekomendasi tindakan.\n"
    #     "Constraints:\n"
    #     "- Gunakan Bahasa Indonesia yang objektif dan teknis.\n"
    #     "- Jangan mengarang fakta di luar informasi yang diberikan user.\n"
    #     "- Jika langkah reproduksi tidak jelas dari teks, tulis ['Langkah reproduksi tidak disebutkan secara spesifik'].\n"
    #     "- Field severity_level HARUS salah satu dari: LOW, MEDIUM, HIGH, atau CRITICAL.\n"
    #     "Output Format:\n"
    #     "Berikan response HANYA dalam format JSON valid tanpa markdown block (```json) dengan struktur persis berikut:\n"
    #     "{\n"
    #     '  "severity_level": "LOW | MEDIUM | HIGH | CRITICAL",\n'
    #     '  "summary": "string ringkasan masalah maks 2 kalimat",\n'
    #     '  "reproduction_steps": ["langkah 1", "langkah 2"],\n'
    #     '  "recommended_action": "string saran investigasi teknis"\n'
    #     "}"
    # ),
    # Sesudah Failure Case
    "C": (
        "Role: Kamu adalah Senior QA Engineer dan Bug Triager.\n"
        "Context: Tim engineering membutuhkan sistem otomatis untuk mengubah laporan bug mentah dari user "
        "menjadi tiket teknis terstruktur yang siap dimasukkan ke database.\n"
        "Task: Analisis teks laporan user dan ekstrak tingkat keparahan, ringkasan teknis, langkah reproduksi, "
        "serta rekomendasi tindakan.\n"
        "Constraints:\n"
        "- Gunakan Bahasa Indonesia yang objektif dan teknis, serta abaikan nada sarkasme dari user.\n"
        "- Jangan mengarang fakta di luar informasi yang diberikan user.\n"
        "- Ekstrak urutan kejadian atau tindakan yang dilakukan user dari cerita mereka menjadi langkah reproduksi berurutan. "
        "Hanya tulis ['Langkah reproduksi tidak disebutkan secara spesifik'] jika teks sama sekali tidak menceritakan kronologi tindakan.\n"
        "- Field severity_level HARUS salah satu dari: LOW, MEDIUM, HIGH, atau CRITICAL.\n"
        "- Wajib kategorikan severity_level sebagai CRITICAL apabila masalah melibatkan transaksi finansial, saldo terpotong ganda, kegagalan pembayaran, atau kehilangan uang/data.\n"
        "Output Format:\n"
        "Berikan response HANYA dalam format JSON valid tanpa markdown block (```json) dengan struktur persis berikut:\n"
        "{\n"
        '  "severity_level": "LOW | MEDIUM | HIGH | CRITICAL",\n'
        '  "summary": "string ringkasan masalah maks 2 kalimat",\n'
        '  "reproduction_steps": ["langkah 1", "langkah 2"],\n'
        '  "recommended_action": "string saran investigasi teknis"\n'
        "}"
    ),
}


def build_messages(text: str, version: Literal["A", "B", "C"]) -> list[dict[str, str]]:
    """Menyusun payload messages berdasarkan versi prompt yang dipilih."""
    user_content = f"Summarize this text:\n\n{text}" if version == "A" else text
    return [
        {"role": "system", "content": SYSTEM_PROMPTS[version]},
        {"role": "user", "content": user_content},
    ]


# Fungsi Alat Bantuan untuk parsing dan inisialisasi client
def get_groq_client() -> AsyncGroq:
    """Inisialisasi client Groq dengan pengecekan API key eksplisit."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="GROQ_API_KEY tidak ditemukan di file .env.",
        )
    return AsyncGroq(api_key=api_key)


def parse_llm_output(raw_text: str) -> tuple[bool, TriageStructuredOutput | None]:
    """Mencoba mem-parsing output LLM ke Pydantic schema secara aman."""
    cleaned_text = raw_text.strip()
    if cleaned_text.startswith("```"):
        lines = cleaned_text.splitlines()
        cleaned_text = "\n".join(lines[1:-1]).strip()

    try:
        parsed_json: dict[str, Any] = json.loads(cleaned_text)
        validated_data = TriageStructuredOutput(**parsed_json)
        return True, validated_data
    except (json.JSONDecodeError, ValidationError):
        return False, None


# FastAPI Endpoints
@app.get("/")
def home() -> dict[str, str]:
    return {"message": "GenAI Issue Triager API is running. Buka /docs untuk menguji endpoint."}


@app.post("/analyze", response_model=APIResponse)
async def analyze_issue(request: AnalyzeRequest) -> APIResponse:
    client = get_groq_client()
    messages = build_messages(request.text, request.prompt_version)

    try:
        response_format = {"type": "json_object"} if request.prompt_version == "C" else None

        completion = await client.chat.completions.create(
            # model="llama-3.3-70b-versatile", -- gagal akses
            model="openai/gpt-oss-120b",
            messages=messages,
            temperature=0.2,
            response_format=response_format,
        )
    except GroqError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Gagal menghubungi LLM provider: {str(exc)}",
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Terjadi kesalahan internal: {str(exc)}",
        ) from exc

    raw_result = completion.choices[0].message.content or ""
    is_valid, structured_data = parse_llm_output(raw_result)

    if request.prompt_version == "C" and not is_valid:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": "Output LLM tidak sesuai dengan skema JSON yang diharapkan.",
                "raw_output": raw_result,
            },
        )

    return APIResponse(
        prompt_version=request.prompt_version,
        is_valid_json=is_valid,
        structured_data=structured_data,
        raw_output=None if is_valid else raw_result,
    )