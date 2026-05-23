<h1 align="center">x-search-cli</h1>

<p align="center">
  A practical CLI wrapper for Hermes x_search_tool
</p>

<p align="center">
  <a href="./README_JP.md">日本語</a> | <strong>English</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/uv-managed-6E56CF" alt="uv">
  <img src="https://img.shields.io/badge/xAI-Responses_API-black" alt="xAI Responses API">
</p>

## Overview

X Premium users can now use X search through [Hermes Agent](https://github.com/nousresearch/hermes-agent).
This CLI reuses Hermes Agent credentials, calls the `x_search` tool through the xAI Responses API,
and returns search results from X with Grok-generated summaries.

## Features

- No need to launch Hermes Agent.
- Changes the default model from `grok-4.20-reasoning` to `grok-4.3`.
  - Faster response times.
  - Shorter answers.
- Can be installed globally and called from any directory.

## Requirements

- `uv`
- Authenticated `xai-oauth` in `hermes-agent`, or `XAI_API_KEY`

If you have not authenticated yet, run the following command first.

Authentication example:

```sh
uvx --from hermes-agent hermes auth add xai-oauth
```

## Setup

Install it so you can use it from any directory:

```sh
./install_x_search.sh
x-search 'What are people saying about xAI on X?'
```

Do the same manually:

```sh
uv tool install --editable /path/to/x-search-cli
x-search 'What are people saying about xAI on X?'
```

Try it only inside this repository:

```sh
uv run x-search 'What are people saying about xAI on X?'
```

Run it once from a Hermes environment:

```sh
uvx --from hermes-agent python x_search_cli.py \
  'What are people saying about xAI on X?'
```

## Agent Skill

This repository also includes an Agent Skills format `SKILL.md`.

- Skill file: [`x-search-skill/SKILL.md`](x-search-skill/SKILL.md)
- Reference file: [`x-search-skill/references/COMMANDS.md`](x-search-skill/references/COMMANDS.md)
- Skill name: `x-search-skill`
- Intended use:
  - Summarize reactions on X
  - Collect X posts with citation URLs
  - Filter X search by handle, date, image, and video
- Operational rules for agents:
  - Treat X as the primary source and add non-X sources only when supplemental context is needed
  - Validate timeframe, topic, and evidence level before answering
  - Distinguish installation, argument, authentication, and empty, too broad, or weak-evidence results

This skill assumes that the `x-search` command is already installed
and serves as an operational guide for agents that call the local `x-search` CLI.

`x-search-skill/SKILL.md` is the primary instruction file. `x-search-skill/references/COMMANDS.md`
is optional command guidance that agents read only when needed. Keep the linked
`references/` directory alongside the skill file.

To use it as a skill, place `x-search-skill/SKILL.md` in your Agent Skills directory
or load this repository in an environment where the file can be referenced.

## Usage

Basic:

```sh
x-search 'What are people saying about xAI on X?'
```

The default model for this CLI is `grok-4.3`.

Specify a model explicitly:

```sh
x-search --model grok-4.20-reasoning 'What are people saying about xAI on X?'
```

Print the full JSON:

```sh
x-search --mode json 'What are people saying about xAI on X?'
```

Print citation URLs only:

```sh
x-search --mode urls 'What are people saying about xAI on X?'
```

Print a numbered citation list:

```sh
x-search --mode citations 'What are people saying about xAI on X?'
```

Filter by handle or date:

Replace `YYYY-MM-DD` with explicit dates before running the command.

```sh
x-search \
  --model grok-4.3 \
  --allowed-handle xai \
  --allowed-handle grok \
  --from-date YYYY-MM-DD \
  --to-date YYYY-MM-DD \
  'Summarize recent reactions on X'
```

Pass the query from standard input:

```sh
cat prompt.txt | x-search --mode answer
```

Enable image or video understanding:

```sh
x-search \
  --image \
  --video \
  'Find posts discussing a demo video and summarize reactions'
```

## Options

- `--mode answer|json|citations|urls`
- `--model MODEL`
- `--allowed-handle` and `--excluded-handle`
- `--from-date YYYY-MM-DD`
- `--to-date YYYY-MM-DD`
- `--image`
- `--video`

## Notes

- `install_x_search.sh` updates an existing installation with `--reinstall`
- The default value for `--model` is `grok-4.3`
- `--model` overrides Hermes `x_search.model` only for that invocation
- This CLI default takes precedence over the Hermes default `grok-4.20-reasoning`
- Model, timeout, and retry behavior follow the Hermes `x_search` settings
- Authentication is resolved automatically from `xai-oauth` or `XAI_API_KEY`

## Acknowledgements

Special thanks to @MtkN1XBt for the X article explaining in detail how to use this from Python.
