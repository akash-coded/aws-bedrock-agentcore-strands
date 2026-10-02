#!/usr/bin/env python3
"""Ask any Amazon Bedrock model one question (the Converse API), from a Claude Code cloud session.

The key comes from AWS_BEARER_TOKEN_BEDROCK when the environment's variables set it. Otherwise the
session never holds the key: the cloud environment has an API credential for the Bedrock hosts,
and Anthropic's proxy adds "Authorization: Bearer <key>" to each request after it leaves this machine
(see .claude/cloud/README.md, "Bedrock"). Every real call is billed to the owner's AWS account: say
which model, how many calls and why, and wait for the owner's yes. --check spends nothing.

    python3 .claude/cloud/bedrock-ask.py --check [--region us-east-1]
    python3 .claude/cloud/bedrock-ask.py --model <model or inference profile id> "question"
        [--region us-east-1] [--max-tokens 1024] [--system "..."] [--temperature 0.2] [--json]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


def converse(endpoint: str, model: str, body: dict) -> tuple[int, dict]:
    """POST to Converse. No Authorization header: the environment's proxy adds it."""
    url = f"{endpoint}/model/{urllib.parse.quote(model, safe='')}/converse"
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), method="POST",
                                 headers=headers())
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            return e.code, json.loads(raw or b"{}")
        except ValueError:
            return e.code, {"message": raw.decode("utf-8", "replace")[:300]}


def headers() -> dict:
    """With AWS_BEARER_TOKEN_BEDROCK set (the environment's variables), send the key; without it, send none
    and let the environment's API credential add it on the way out."""
    h = {"Content-Type": "application/json", "Accept": "application/json"}
    key = os.environ.get("AWS_BEARER_TOKEN_BEDROCK", "").strip()
    if key:
        h["Authorization"] = f"Bearer {key}"
    return h


def message(data: dict) -> str:
    return str(data.get("message") or data.get("Message") or data)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("question", nargs="?")
    ap.add_argument("--check", action="store_true",
                    help="send an empty conversation: shows whether the key is attached, costs nothing")
    ap.add_argument("--model", help="a model ID or inference profile ID, as Bedrock lists them")
    ap.add_argument("--region", default="us-east-1")
    ap.add_argument("--max-tokens", type=int, default=1024, help="always set: an unset limit reserves the model's maximum")
    ap.add_argument("--system", default="")
    ap.add_argument("--temperature", type=float)
    ap.add_argument("--json", action="store_true", help="print Bedrock's whole answer")
    ap.add_argument("--endpoint", help=argparse.SUPPRESS)  # for tests
    a = ap.parse_args()
    endpoint = a.endpoint or f"https://bedrock-runtime.{a.region}.amazonaws.com"

    if a.check:
        code, data = converse(endpoint, a.model or "amazon.nova-lite-v1:0", {"messages": []})
        if code == 400:
            print(f"The key works in {a.region}: Bedrock accepted it and turned down the empty request "
                  f"({message(data)}). Nothing was billed.")
            return 0
        if code in (401, 403):
            print(f"Not authorised ({code}): {message(data)}")
            print("Set AWS_BEARER_TOKEN_BEDROCK in the environment's variables (a running session sees new variables only after its machine restarts), "
                  f"or check that the environment's API credential lists bedrock-runtime.{a.region}.amazonaws.com "
                  "with header Authorization and prefix Bearer, and that the key has not expired.")
            return 1
        print(f"Unexpected answer {code}: {message(data)}")
        return 1

    if not a.model or not a.question:
        ap.error("give --model and a question, or --check")
    body: dict = {"messages": [{"role": "user", "content": [{"text": a.question}]}],
                  "inferenceConfig": {"maxTokens": a.max_tokens}}
    if a.temperature is not None:
        body["inferenceConfig"]["temperature"] = a.temperature
    if a.system:
        body["system"] = [{"text": a.system}]

    code, data = converse(endpoint, a.model, body)
    if code != 200:
        print(f"Bedrock answered {code}: {message(data)}", file=sys.stderr)
        return 1
    if a.json:
        print(json.dumps(data, indent=2))
        return 0
    parts = (data.get("output") or {}).get("message", {}).get("content", [])
    print("\n".join(p["text"] for p in parts if "text" in p))
    u = data.get("usage") or {}
    print(f"[{a.model} in {a.region}: {u.get('inputTokens', '?')} tokens in, {u.get('outputTokens', '?')} out, "
          f"stop: {data.get('stopReason')}]", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
