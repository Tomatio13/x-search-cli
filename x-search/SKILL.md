---
name: x-search
description: Search X posts and get Grok-grounded summaries via the local x-search CLI. Use when the user wants X search, summaries of reactions on X, cited X post URLs, or X result filtering by handle, date, image, or video.
compatibility: Requires the x-search command to already be installed and authenticated through Hermes xai-oauth or XAI_API_KEY.
---

# X Search

## When to use

- MUST use `x-search` when the user explicitly wants X posts, reactions on X, or cited X post URLs.
- Do not use this skill for general web research unless X is the required source.
- If the user asks for recent or time-bounded X discussion, prefer `x-search` over broader search tools.

## Workflow

1. Translate the user request into a single search prompt that is explicit about topic, timeframe, and desired output.
2. Choose the output mode before adding optional filters.
3. Choose the narrowest flags that satisfy the request.
4. Run `x-search` and inspect the returned answer or citations.
5. If the result is too broad, tighten the prompt first, then add handle or date filters.
6. If the user needs raw evidence, rerun with `--mode citations` or `--mode urls`.

## Quick mode selection

- Use `--mode answer` for a direct summary.
- Use `--mode citations` for title-plus-URL evidence.
- Use `--mode urls` for source collection only.
- Use `--mode json` for debugging or downstream parsing.

## Command patterns

Basic summary for recent reactions:

```sh
x-search 'What are people on X saying about OpenAI this week?'
```

Model override for deeper reasoning:

```sh
x-search --model grok-4.20-reasoning 'Summarize reactions on X about product launch delays'
```

Handle filter for trusted accounts:

```sh
x-search \
  --allowed-handle openai \
  --allowed-handle samaltman \
  'Summarize recent posts and reactions on X'
```

Date filter for explicit bounds:

```sh
x-search \
  --from-date 2026-05-01 \
  --to-date 2026-05-20 \
  'Summarize discussion on X about the latest model release'
```

Evidence-first output for citations:

```sh
x-search --mode citations 'Find posts discussing the benchmark controversy'
x-search --mode urls 'Find posts discussing the benchmark controversy'
```

Media-aware search for demo reactions:

```sh
x-search --image --video 'Find posts reacting to the demo video and summarize sentiment'
```

## Option selection

- Use `--allowed-handle` for a trusted-source subset.
- Use `--excluded-handle` to remove a noisy account set.
- Never combine `--allowed-handle` and `--excluded-handle` in the same call.
- Use `--from-date` and `--to-date` only with `YYYY-MM-DD`.
- When the user gives relative dates such as `today`, `yesterday`, or `this week`, convert them to explicit `YYYY-MM-DD` bounds when feasible.
- Enable `--image` or `--video` only when the request depends on media understanding.
- Prefer repeated handle flags over comma-separated lists for readability.

## Prompt writing rules

- Ask for one concrete deliverable per call.
- Include the target topic, timeframe, and angle in the prompt.
- Prefer "summarize reactions", "find posts discussing", or "compare opinions" over vague prompts.
- If the user wants recency, say it in the prompt even when date filters are also used.

## Failure handling

- If `x-search` exits non-zero, first check for authentication or configuration issues, then report the stderr or returned error clearly.
- Do not retry until authentication or configuration issues are fixed.
- If the command shape is valid but the answer is empty or obviously underspecified, retry with a more precise prompt before changing many flags.
- If citations are required but missing from `answer`, rerun with `--mode citations` or `--mode json`.
- Treat authentication or configuration failures separately from search-quality failures.
- If the user omits a query but provides stdin content, pipe that content into `x-search`.

## Practical defaults

- The CLI default model is `grok-4.3`.
- `--mode json` pretty-prints JSON with indent `2` unless overridden.
