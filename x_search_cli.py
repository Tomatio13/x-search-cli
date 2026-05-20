import argparse
import json
import sys
from contextlib import contextmanager
from datetime import date
from typing import Callable, Iterable, Iterator, List

import tools.x_search_tool as x_search_tool_module


DEFAULT_MODEL = "grok-4.3"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Call Hermes x_search_tool with a practical CLI interface."
    )
    parser.add_argument(
        "query_parts",
        nargs="*",
        help="Search prompt. If omitted, stdin is used.",
    )
    parser.add_argument(
        "--mode",
        choices=("answer", "json", "citations", "urls"),
        default="answer",
        help="Output mode. Default: answer",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Model for this call. Default: {DEFAULT_MODEL}",
    )
    parser.add_argument(
        "--allowed-handle",
        dest="allowed_handles",
        action="append",
        default=[],
        help="Allow only this X handle. Repeatable. Comma-separated values are also accepted.",
    )
    parser.add_argument(
        "--excluded-handle",
        dest="excluded_handles",
        action="append",
        default=[],
        help="Exclude this X handle. Repeatable. Comma-separated values are also accepted.",
    )
    parser.add_argument(
        "--from-date",
        default="",
        help="Lower date bound in YYYY-MM-DD.",
    )
    parser.add_argument(
        "--to-date",
        default="",
        help="Upper date bound in YYYY-MM-DD.",
    )
    parser.add_argument(
        "--image",
        action="store_true",
        help="Enable image understanding.",
    )
    parser.add_argument(
        "--video",
        action="store_true",
        help="Enable video understanding.",
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="JSON indentation for --mode json. Default: 2",
    )
    return parser.parse_args()


def normalize_handles(values: Iterable[str]) -> List[str]:
    handles: List[str] = []
    for value in values:
        for part in value.split(","):
            handle = part.strip().lstrip("@")
            if handle:
                handles.append(handle)
    return handles


def read_query(query_parts: List[str]) -> str:
    if query_parts:
        return " ".join(part.strip() for part in query_parts).strip()
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    raise SystemExit("query is required")


def validate_date(raw_value: str, option_name: str) -> str:
    value = raw_value.strip()
    if not value:
        return ""
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise SystemExit(f"{option_name} must be YYYY-MM-DD: {value}") from exc
    return value


def parse_response(raw_response: str) -> dict:
    try:
        data = json.loads(raw_response)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid JSON response from x_search_tool: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("x_search_tool returned a non-object JSON response")
    return data


@contextmanager
def override_x_search_model(model: str) -> Iterator[None]:
    normalized_model = model.strip()
    if not normalized_model:
        yield
        return

    original_loader: Callable[[], dict] = x_search_tool_module._load_x_search_config

    def patched_loader() -> dict:
        config = dict(original_loader() or {})
        config["model"] = normalized_model
        return config

    x_search_tool_module._load_x_search_config = patched_loader
    try:
        yield
    finally:
        x_search_tool_module._load_x_search_config = original_loader


def print_citations(data: dict, urls_only: bool) -> None:
    inline_citations = data.get("inline_citations") or []
    citations = data.get("citations") or []

    if inline_citations:
        for index, citation in enumerate(inline_citations, start=1):
            url = str(citation.get("url") or "").strip()
            title = str(citation.get("title") or "").strip() or str(index)
            if not url:
                continue
            if urls_only:
                print(url)
            else:
                print(f"[{title}] {url}")
        return

    for index, citation in enumerate(citations, start=1):
        if isinstance(citation, dict):
            url = str(citation.get("url") or "").strip()
            title = str(citation.get("title") or "").strip() or str(index)
        else:
            url = str(citation).strip()
            title = str(index)
        if not url:
            continue
        if urls_only:
            print(url)
        else:
            print(f"[{title}] {url}")


def main() -> int:
    args = parse_args()
    query = read_query(args.query_parts)
    allowed_handles = normalize_handles(args.allowed_handles)
    excluded_handles = normalize_handles(args.excluded_handles)

    if allowed_handles and excluded_handles:
        raise SystemExit("--allowed-handle and --excluded-handle cannot be used together")

    from_date = validate_date(args.from_date, "--from-date")
    to_date = validate_date(args.to_date, "--to-date")
    model = args.model.strip()

    with override_x_search_model(model):
        raw_response = x_search_tool_module.x_search_tool(
            query=query,
            allowed_x_handles=allowed_handles or None,
            excluded_x_handles=excluded_handles or None,
            from_date=from_date,
            to_date=to_date,
            enable_image_understanding=args.image,
            enable_video_understanding=args.video,
        )
    data = parse_response(raw_response)

    if args.mode == "json":
        print(json.dumps(data, ensure_ascii=False, indent=args.indent))
    elif args.mode == "citations":
        print_citations(data, urls_only=False)
    elif args.mode == "urls":
        print_citations(data, urls_only=True)
    else:
        print(data.get("answer", ""))

    return 0 if data.get("success") else 1


if __name__ == "__main__":
    raise SystemExit(main())
