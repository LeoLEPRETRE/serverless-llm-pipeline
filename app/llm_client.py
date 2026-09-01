import httpx

from app.config import Settings

SYSTEM_PROMPT = (
    "Tu es un reviewer de code senior, bienveillant mais exigeant. "
    "Pour le code fourni : 1) identifie les bugs, 2) signale les failles de sécurité, "
    "3) propose des améliorations de lisibilité et de performance, "
    "4) donne une version corrigée du code. Réponds en français, de façon structurée et concise."
)

class LLMError(Exception):
    """Erreur lors de l'appel au fournisseur LLM."""

async def review_code(code: str, language: str | None, settings: Settings) -> str:
    payload = {
        "model": settings.groq_model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Langage : {language or 'non précisé'}\n\nCode :\n{code}"},
        ],
        "temperature": 0.2,
        "max_tokens": 2048,
        "reasoning_effort": "low",
    }
    headers = {"Authorization": f"Bearer {settings.groq_api_key.get_secret_value()}"}

    try:
        async with httpx.AsyncClient(
            base_url=settings.groq_base_url, timeout=settings.llm_timeout_seconds
        ) as client:
            response = await client.post("/chat/completions", json=payload, headers=headers)
            response.raise_for_status()
    except httpx.TimeoutException as exc:
        raise LLMError("Le fournisseur LLM n'a pas répondu à temps") from exc
    except httpx.HTTPStatusError as exc:
        raise LLMError(
            f"Le fournisseur LLM a renvoyé le statut {exc.response.status_code} : "
            f"{exc.response.text[:500]}"
        ) from exc
    except httpx.RequestError as exc:
        raise LLMError("Impossible de joindre le fournisseur LLM") from exc

    return response.json()["choices"][0]["message"]["content"]