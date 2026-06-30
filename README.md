# TxtSpkr

TxtSpkr is a small Python command-line workbench for exploring skills in
CrewAI. It accepts a short natural-language message, runs it through a small
crew of agents, and prints a terse SMS-style version with emoji decoration.

> [!WARNING]
> This is an experimental project and should not be considered production-ready.

The project was created to take first steps with CrewAI skills. The domain is
intentionally silly and narrow so the effect of each skill stays visible: one
agent learns how to rewrite text as SMS speak, another learns how to choose
emojis, and a final agent combines their outputs.

## What It Does

The CLI accepts a message such as:

```powershell
.\.venv\Scripts\python.exe -m txt_spkr "Thank you. I'll see you later."
```

The crew then:

- asks an SMS specialist to convert the message into terse txtspk
- asks an emoji specialist to choose emojis for the original message
- asks a combiner agent to merge the SMS and emoji outputs
- prints the final result

The specialist agents use CrewAI skill directories under `skills/`. The SMS
specialist receives the `sms-speak` skill, and the emoji specialist receives
the `emoji-speak` skill. The skills include obvious proof markers, such as the
SMS proof word `ttyl` and an uncommon final emoji, so it is easier to see when
the skills were used.

## Requirements

- Python 3.11.
- PowerShell on Windows.
- An `OPENAI_API_KEY` environment variable for OpenAI model calls.

## Setup

Create the virtual environment and install the project with development
dependencies:

```powershell
.\scripts\setup-dev.ps1
```

The setup script expects Python 3.11 at the path configured in
`scripts\setup-dev.ps1`.

## Running

Run the workbench from the repository root:

```powershell
.\.venv\Scripts\python.exe -m txt_spkr "Thank you. I'll see you later."
```

Example output:

```text
Thx :) c u l8r ttyl :) [uncommon emoji]
```

Actual wording and emoji choices can vary between runs because the output is
model-driven.

## Development Checks

Run formatting, linting, type checking, and tests:

```powershell
.\scripts\check.ps1
```

This runs:

- `ruff format .`
- `ruff check .`
- `pyright`
- `pytest`

## Project Structure

```text
src/txt_spkr/
  __main__.py  Package entry point for python -m txt_spkr
  cli.py       Command-line argument handling and console output
  crew.py      CrewAI agents, tasks, skills wiring, and crew runner

skills/
  sms-agent/
    sms-speak/
      SKILL.md
  emoji-agent/
    emoji-speak/
      SKILL.md

tests/
  test_smoke.py

scripts/
  setup-dev.ps1
  check.ps1
```

## Notes

This project is a CrewAI skills learning exercise, not a general-purpose text
message converter. The skills are written as Markdown `SKILL.md` files so their
effect can be edited and observed without changing much Python code.

CrewAI discovers skills from directories. Each specialist agent is pointed at a
dedicated parent directory so unrelated skills are not given to the wrong
agent.

CrewAI runtime storage is directed to `.crewai-storage/`, which is ignored by
Git. OpenAI API calls may incur usage costs.

## Third-Party Notices

This project has a direct runtime dependency on the `crewai` Python package.
See the package's PyPI license metadata for full license and notice terms.

## License

GNU General Public License v3.0. See the `LICENSE` file for details.
