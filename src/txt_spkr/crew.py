"""Agents for the TxtSpkr CLI"""

# ruff: noqa: E402,I001

from __future__ import annotations

import os
from pathlib import Path

MODEL_NAME = "openai/gpt-4.1-mini"
VERBOSE_LOGGING = False
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = PROJECT_ROOT / "skills"
CREWAI_STORAGE_DIR = PROJECT_ROOT / ".crewai-storage"

CREWAI_STORAGE_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("CREWAI_STORAGE_DIR", str(CREWAI_STORAGE_DIR))
os.environ.setdefault("CREWAI_TRACING_ENABLED", "false")

from crewai import Agent, Crew, Process, Task


message_to_txt_agent = Agent(
    role="SMS speak specialist",
    goal="Convert the given message into terse SMS format.",
    backstory=(
        "You are an expert in converting messages into terse SMS format. "
        "You understand the nuances of SMS language, including abbreviations, "
        "slang, and character limits. "
        "You must use the sms-speak skill when rewriting messages."
    ),
    skills=[SKILLS_DIR / "sms-agent"],
    verbose=VERBOSE_LOGGING,
    model=MODEL_NAME,
)

message_to_emoji_agent = Agent(
    role="Emoji speak specialist",
    goal="Create a series of emojis to be appended to the given message.",
    backstory=(
        "You are an expert in creating emojis that represent the meaning "
        "and tone of a message. "
        "You understand the nuances of emoji usage, including context, "
        "cultural references, and emotional expression. "
        "You must use the emoji-speak skill when selecting emojis."
    ),
    skills=[SKILLS_DIR / "emoji-agent"],
    verbose=VERBOSE_LOGGING,
    model=MODEL_NAME,
)

message_converter_agent = Agent(
    role="Combine SMS and Emoji specialists",
    goal="Combine the outputs of the SMS and Emoji specialists.",
    backstory=(
        "You are an expert in combining the outputs of the SMS and Emoji specialists. "
        "You understand the nuances of both SMS and Emoji language, "
        "and can create a final message that is both terse and expressive."
    ),
    verbose=VERBOSE_LOGGING,
    model=MODEL_NAME,
)

message_to_txt_task = Task(
    description=(
        "Convert the following message into terse SMS format using the "
        "sms-speak skill.\n"
        "{message}"
    ),
    expected_output=(
        "A terse SMS version of the given message. It must include at least "
        "one emoji before the final word and must end with the exact proof "
        'word "ttyl".'
    ),
    agent=message_to_txt_agent,
    async_execution=True,
)

message_to_emoji_task = Task(
    description=(
        "Create a series of emojis to be appended to the following message "
        "using the emoji-speak skill.\n"
        "{message}"
    ),
    expected_output=(
        "A series of emojis that represent the meaning and tone of the given "
        "message. The final emoji must be the uncommon proof emoji 🧿."
    ),
    agent=message_to_emoji_agent,
    async_execution=True,
)

message_converter_task = Task(
    description=(
        "Combine the outputs of the SMS and Emoji specialists without removing "
        "their skill proof markers."
    ),
    expected_output=(
        "A final message that is both terse and expressive, "
        "appending the output of the Emoji specialist "
        "to the output of the SMS specialist. Preserve the SMS specialist's "
        'final proof word "ttyl", preserve at least one emoji before that '
        "word, and ensure the final emoji in the whole result is 🧿."
    ),
    agent=message_converter_agent,
    context=[message_to_txt_task, message_to_emoji_task],
)

crew = Crew(
    agents=[message_to_txt_agent, message_to_emoji_agent, message_converter_agent],
    tasks=[message_to_txt_task, message_to_emoji_task, message_converter_task],
    process=Process.sequential,
    verbose=VERBOSE_LOGGING,
)


def run_crew(message: str) -> str:
    """Run the crew with the given message."""
    result = crew.kickoff(inputs={"message": message})
    return str(result)
