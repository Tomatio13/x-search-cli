---
name: x-search-skill
description: Search X posts and get Grok-grounded summaries via the local x-search CLI. Use when the user wants X search, summaries of reactions on X, cited X post URLs, or X result filtering by handle, date, image, or video.
compatibility: Requires the x-search command to already be installed and authenticated through Hermes xai-oauth or XAI_API_KEY.
---

# X Search

Use the local `x-search` command when the user specifically needs information from X posts rather than general web results. Assumes `x-search` is already installed and authenticated.

## Trigger conditions

- Use this skill when the user asks for reactions on X, cited X post URLs, or summaries grounded in X search results.
- Use this skill when the user wants X results filtered by handle, date, image, or video.
- Do not use this skill for general web research unless X is the required source.
- If X is the primary source, use this skill first and add non-X sources only when the user needs supplemental context.

## Core workflow

1. Convert the request into one clear X-search prompt with topic, timeframe, and expected deliverable.
2. Pick the output mode first: summary, citations, URLs, or full JSON.
3. Add only the narrowest filters needed: handle, date, image, or video.
4. Run `x-search` once and inspect whether the result is broad, empty, or missing evidence.
5. Tighten the prompt before stacking many flags.
6. If the user needs evidence, rerun with `--mode citations` or `--mode urls`.
7. Verify that the result matches the requested timeframe, topic, and evidence level before answering.

## Mode selection

- Use `--mode answer` for a direct summary.
- Use `--mode citations` for labeled citation URLs.
- Use `--mode urls` for raw source collection.
- Use `--mode json` for debugging or downstream parsing.

## Option rules

- Use `--allowed-handle` for a trusted-account subset.
- Use `--excluded-handle` to remove noisy accounts.
- MUST NOT combine `--allowed-handle` and `--excluded-handle`.
- MUST use `--from-date` and `--to-date` only with `YYYY-MM-DD`.
- Convert relative dates such as `today`, `yesterday`, or `this week` into explicit bounds when feasible.
- Only enable `--image` or `--video` when the request depends on media understanding.
- The default model is `grok-4.3`. Override with `--model` only when the task needs a different tradeoff.

## Prompt rules

- Ask for one concrete deliverable per call.
- Include the topic, timeframe, and angle in the prompt text.
- Prefer prompts such as `Summarize reactions on X`, `Find posts discussing`, or `Compare opinions on X`.
- If recency matters, say so in the prompt even when date filters are present.
- Prompt text may be written in English for consistency with the command examples.

## Failure handling

- If `x-search` is not found, stop and report that the CLI must be installed first.
- If the command fails because of invalid arguments, fix the command shape before retrying.
- If the command exits non-zero, check authentication or Hermes configuration next.
- If the result is empty, too broad, or lacks evidence, refine the prompt and rerun once.
- If citations are required but the summary is not enough, rerun with `--mode citations`, `--mode urls`, or `--mode json`.
- If the query comes from standard input, pipe it into `x-search` instead of rewriting the content by hand.

## References

- For ready-to-run command templates, see [references/COMMANDS.md](references/COMMANDS.md).
