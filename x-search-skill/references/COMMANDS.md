# x-search Command Patterns

Use these patterns when the base workflow in `SKILL.md` is not enough.

## Basic summary

```sh
x-search 'What are people on X saying about OpenAI this week?'
```

## Model override

```sh
x-search --model grok-4.20-reasoning 'Summarize reactions on X about product launch delays'
```

## Trusted handles only

```sh
x-search \
  --allowed-handle openai \
  --allowed-handle samaltman \
  'Summarize recent posts and reactions on X'
```

## Exclude noisy handles

```sh
x-search \
  --excluded-handle spamaccount \
  --excluded-handle anotheraccount \
  'Find posts discussing the API outage'
```

## Explicit date window

```sh
x-search \
  --from-date YYYY-MM-DD \
  --to-date YYYY-MM-DD \
  'Summarize discussion on X about the latest model release'
```

## Evidence-first output

```sh
x-search --mode citations 'Find posts discussing the benchmark controversy'
x-search --mode urls 'Find posts discussing the benchmark controversy'
```

## JSON output for inspection

```sh
x-search --mode json --indent 2 'Find posts discussing the benchmark controversy'
```

## Media-aware search

```sh
x-search --image --video 'Find posts reacting to the demo video and summarize sentiment'
```

## Query from standard input

```sh
cat prompt.txt | x-search --mode answer
```
