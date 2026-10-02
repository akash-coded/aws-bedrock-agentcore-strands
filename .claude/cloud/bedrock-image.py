#!/usr/bin/env python3
"""Make one image with a Stability AI model on Amazon Bedrock, from a Claude Code cloud session.

The key comes from AWS_BEARER_TOKEN_BEDROCK when the environment's variables set it. Otherwise the
session never holds the key: the cloud environment has an API credential for
bedrock-runtime.us-west-2.amazonaws.com, and Anthropic's proxy adds "Authorization: Bearer <key>"
to each request after it leaves this machine (see .claude/cloud/README.md, "Images").

Each real image is billed to the owner's AWS account. Before the first image of a task, say what
you will make, how many and with which model, and wait for the owner's yes. --check spends nothing.

    python3 .claude/cloud/bedrock-image.py --check
    python3 .claude/cloud/bedrock-image.py --prompt "..." --out picture.png
        [--model core|ultra|sd35] [--aspect 16:9] [--negative "..."] [--seed N]
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ENDPOINT = "https://bedrock-runtime.us-west-2.amazonaws.com"
MODELS = {
    "core": "stability.stable-image-core-v1:1",
    "ultra": "stability.stable-image-ultra-v1:1",
    "sd35": "stability.sd3-5-large-v1:0",
}
ASPECTS = ["16:9", "1:1", "21:9", "2:3", "3:2", "4:5", "5:4", "9:16", "9:21"]


def invoke(endpoint: str, model: str, body: dict) -> tuple[int, dict]:
    """POST the body to InvokeModel. No Authorization header: the environment's proxy adds it."""
    url = f"{endpoint}/model/{urllib.parse.quote(model, safe='')}/invoke"
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), method="POST",
                                 headers=headers())
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
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
    ap.add_argument("--check", action="store_true",
                    help="send a request without a prompt: shows whether the key is attached, makes no image")
    ap.add_argument("--prompt")
    ap.add_argument("--out", help="where to write the picture (.png or .jpg)")
    ap.add_argument("--model", choices=sorted(MODELS), default="core")
    ap.add_argument("--aspect", choices=ASPECTS, default="16:9")
    ap.add_argument("--negative", default="")
    ap.add_argument("--seed", type=int, default=0, help="0 picks one at random")
    ap.add_argument("--endpoint", default=ENDPOINT, help=argparse.SUPPRESS)  # for tests
    a = ap.parse_args()
    model = MODELS[a.model]

    if a.check:
        code, data = invoke(a.endpoint, model, {})
        if code == 400:
            print(f"The key works: Bedrock accepted it and turned down the empty request ({message(data)}). No image was made.")
            return 0
        if code in (401, 403):
            print(f"Not authorised ({code}): {message(data)}")
            print("Set AWS_BEARER_TOKEN_BEDROCK in the environment's variables (a running session sees new variables only after its machine restarts), "
                  "or check the environment's API credential: allowed website bedrock-runtime.us-west-2.amazonaws.com, "
                  "header Authorization, prefix Bearer, and a key that has not expired. A message about AWS Marketplace "
                  "means the model is not yet activated in the account.")
            return 1
        print(f"Unexpected answer {code}: {message(data)}")
        return 1

    if not a.prompt or not a.out:
        ap.error("give --prompt and --out, or --check")
    out = Path(a.out).expanduser()
    fmt = "jpeg" if out.suffix.lower() in (".jpg", ".jpeg") else "png"
    body = {"prompt": a.prompt, "aspect_ratio": a.aspect, "output_format": fmt}
    if a.negative:
        body["negative_prompt"] = a.negative
    if a.seed:
        body["seed"] = a.seed

    code, data = invoke(a.endpoint, model, body)
    if code != 200:
        print(f"Bedrock answered {code}: {message(data)}", file=sys.stderr)
        return 1
    images = data.get("images") or []
    reason = (data.get("finish_reasons") or [None])[0]
    if not images or reason:
        print(f"No image returned (finish reason: {reason})", file=sys.stderr)
        return 1
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(base64.b64decode(images[0]))
    seed = (data.get("seeds") or [a.seed])[0]
    print(f"wrote {out} ({out.stat().st_size:,} bytes), model {model}, seed {seed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
