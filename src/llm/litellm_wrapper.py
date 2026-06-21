"""
LiteLLM wrapper for structured agent calls.

Enforces JSON mode via response_format parameter for agents that expect
structured JSON output (Agents 1, 5, 6, 7, 8).
Includes retry on JSON parse failure (max 3 attempts).

All agents that return JSON MUST use call_structured_agent().
Agent 7 (Answer Synthesizer) returns prose and uses call_prose_agent().
"""

import json

import litellm

from src.utils.logger import setup_logger

logger = setup_logger(__name__)


async def call_structured_agent(
    system_prompt: str,
    user_prompt: str,
    model: str,
    temperature: float = 0.0,
    max_tokens: int = 1000,
) -> dict:
    """
    Wrapper for all agents that return JSON.
    Enforces JSON mode via response_format parameter.
    Includes retry on JSON parse failure (max 3 attempts).

    Args:
        system_prompt: System-level instructions for the agent.
        user_prompt: User query / context for the agent.
        model: LiteLLM model string (e.g., "gemini/gemini-3.1-flash-lite").
        temperature: Sampling temperature (default 0.0 for determinism).
        max_tokens: Maximum output tokens.

    Returns:
        Parsed JSON dict from the agent response.

    Raises:
        ValueError: If agent returns invalid JSON after 3 attempts.
        litellm.exceptions.APIError: On API communication failure.
    """
    for attempt in range(3):
        try:
            logger.info(
                "Calling structured agent",
                extra={
                    "model": model,
                    "attempt": attempt + 1,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                },
            )

            response = await litellm.acompletion(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                response_format={"type": "json_object"},  # Enforces JSON mode
            )

            raw = response.choices[0].message.content
            # Strip accidental markdown fences before parsing
            clean = raw.strip().removeprefix("```json").removesuffix("```").strip()
            parsed = json.loads(clean)

            logger.info(
                "Structured agent call successful",
                extra={
                    "model": model,
                    "attempt": attempt + 1,
                    "response_keys": list(parsed.keys()) if isinstance(parsed, dict) else "non-dict",
                },
            )
            return parsed

        except json.JSONDecodeError as e:
            logger.warning(
                "Agent returned invalid JSON",
                extra={
                    "model": model,
                    "attempt": attempt + 1,
                    "error": str(e),
                    "raw_preview": raw[:200] if raw else "empty",
                },
            )
            if attempt == 2:
                raise ValueError(
                    f"Agent returned invalid JSON after 3 attempts: {e}\nRaw: {raw}"
                )
            continue

        except Exception as e:
            logger.error(
                "Structured agent call failed",
                extra={
                    "model": model,
                    "attempt": attempt + 1,
                    "error": str(e),
                    "error_type": type(e).__name__,
                },
            )
            if attempt == 2:
                raise
            continue

    # Should never reach here due to raises above, but satisfy type checker
    raise ValueError("Unexpected: exhausted all retry attempts without raising")


async def call_prose_agent(
    system_prompt: str,
    user_prompt: str,
    model: str,
    temperature: float = 0.1,
    max_tokens: int = 3000,
) -> str:
    """
    Wrapper for agents that return prose (not JSON).
    Used by Agent 7 (Answer Synthesizer) which returns natural language answers.
    Does NOT enforce JSON mode.

    Args:
        system_prompt: System-level instructions for the agent.
        user_prompt: User query / context for the agent.
        model: LiteLLM model string.
        temperature: Sampling temperature (default 0.1 for slight variety).
        max_tokens: Maximum output tokens (default 3000 for long answers).

    Returns:
        Raw string response from the agent.

    Raises:
        litellm.exceptions.APIError: On API communication failure.
    """
    logger.info(
        "Calling prose agent",
        extra={
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
        },
    )

    response = await litellm.acompletion(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )

    content = response.choices[0].message.content

    logger.info(
        "Prose agent call successful",
        extra={
            "model": model,
            "response_length": len(content) if content else 0,
        },
    )

    return content


async def call_local_agent(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.0,
    max_tokens: int = 1500,
) -> dict:
    """
    Wrapper for local Ollama agents (Agents 4 and 8).
    Always uses the local Qwen2.5:14b model, no budget consumption.
    Enforces JSON mode.

    Args:
        system_prompt: System-level instructions.
        user_prompt: User query / context.
        temperature: Sampling temperature (default 0.0).
        max_tokens: Maximum output tokens (default 1500).

    Returns:
        Parsed JSON dict from the local model.

    Raises:
        ValueError: If model returns invalid JSON after 3 attempts.
    """
    return await call_structured_agent(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        model="ollama/qwen2.5:14b",
        temperature=temperature,
        max_tokens=max_tokens,
    )
