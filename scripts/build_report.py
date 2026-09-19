#!/usr/bin/env python3
"""Assemble the README report from CI evidence.

Reads scripts/tools.json (tool metadata + skip ledger) and results/**/*.json (per-cell
trial records produced by the recorder workflows), then rewrites README.md between the
<!-- REPORT:START --> and <!-- REPORT:END --> markers with:
  - per-tool CI status badges,
  - a capability grid (headline launch-exit scenario) linking each cell to its run,
  - embedded GIFs (minimal + 3 creative) for every working tool,
  - the honest skipped/not-evaluated ledger.

This script is the SOLE writer of README's report section (avoids cross-workflow races).
"""
import json
import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
README = ROOT / "README.md"
TOOLS_JSON = ROOT / "scripts" / "tools.json"
START = "<!-- REPORT:START -->"
END = "<!-- REPORT:END -->"

REPO = os.environ.get("GITHUB_REPOSITORY", "YoraiLevi/testing-area")
SERVER = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
BRANCH = "testing-vhs"

VERDICT_GLYPH = {
    "working": "✅",
    "broken": "❌",
    "not-applicable": "➖",
    None: "⬜",
}


def load_tools() -> dict:
    return json.loads(TOOLS_JSON.read_text(encoding="utf-8"))


def load_results() -> list[dict]:
    out = []
    if not RESULTS.exists():
        return out
    for path in sorted(RESULTS.rglob("*.json")):
        try:
            out.append(json.loads(path.read_text(encoding="utf-8")))
        except (ValueError, OSError):
            continue
    return out


def index(results: list[dict]) -> dict:
    """(tool, cell, scenario) -> record ; cell = '<os>-<shell>'."""
    idx = {}
    for r in results:
        cell = f"{r.get('os')}-{r.get('shell')}"
        idx[(r.get("tool"), cell, r.get("scenario"))] = r
    return idx


def badges(tools: dict) -> str:
    lines = ["### CI Status (per tool)", ""]
    for t in tools["tools"]:
        wf = f"rec-{t['id']}.yml"
        url = f"{SERVER}/{REPO}/actions/workflows/{wf}"
        badge = f"{url}/badge.svg?branch={BRANCH}"
        lines.append(f"[![{t['name']}]({badge})]({url})")
    return "\n".join(lines) + "\n"


def grid(tools: dict, idx: dict) -> str:
    headline = tools["headline_scenario"]
    cells = []
    for t in tools["tools"]:
        for c in t["cells"]:
            if c not in cells:
                cells.append(c)
    cells.sort()
    header = "| Tool | Family | " + " | ".join(cells) + " |"
    sep = "|------|--------|" + "|".join([":--:"] * len(cells)) + "|"
    rows = [header, sep]
    for t in tools["tools"]:
        row = [t["name"], t["family"]]
        for c in cells:
            rec = idx.get((t["id"], c, headline))
            if rec is None:
                row.append(VERDICT_GLYPH[None])
                continue
            glyph = VERDICT_GLYPH.get(rec.get("verdict"), "⬜")
            run = rec.get("run_url")
            row.append(f"[{glyph}]({run})" if run else glyph)
        rows.append("| " + " | ".join(row) + " |")
    legend = "\nLegend: ✅ working · ❌ broken · ➖ not applicable · ⬜ not yet run\n"
    return "### Capability Grid — headline scenario `launch-exit`\n\n" + "\n".join(rows) + "\n" + legend


def recordings(tools: dict, idx: dict) -> str:
    scen = tools["scenarios"]
    out = ["### Recordings (per tool: minimal + creative)", ""]
    any_gif = False
    for t in tools["tools"]:
        # pick a representative cell that has a working launch-exit, prefer linux-bash
        pref = ["linux-bash", "linux-zsh", "macos-zsh", "linux-pwsh", "windows-pwsh"]
        chosen = None
        for c in pref + t["cells"]:
            if idx.get((t["id"], c, "launch-exit"), {}).get("verdict") == "working":
                chosen = c
                break
        if chosen is None:
            continue
        gifs = []
        for s in scen:
            rec = idx.get((t["id"], chosen, s))
            if rec and rec.get("verdict") == "working" and rec.get("gif"):
                gifs.append((s, rec["gif"]))
        if not gifs:
            continue
        any_gif = True
        out.append(f"#### {t['name']} (`{chosen}`)")
        out.append("")
        for s, gif in gifs:
            out.append(f"**{s}**")
            out.append("")
            out.append(f"![{t['name']} {s}]({gif})")
            out.append("")
    if not any_gif:
        out.append("_No working recordings committed yet. Trigger the `rec-*` workflows._")
        out.append("")
    return "\n".join(out)


def ledger(tools: dict) -> str:
    out = ["### Skipped / Not Evaluated (honest coverage)", "",
           "| Tool | Reason skipped for CI-GIF evaluation |",
           "|------|--------------------------------------|"]
    for s in tools["skipped"]:
        out.append(f"| {s['name']} | {s['reason']} |")
    out.append("")
    out.append("_Tools discovered beyond the original list and evaluated:_ "
               + ", ".join(t["name"] for t in tools["tools"] if t.get("discovered"))
               + ".")
    out.append("")
    return "\n".join(out)


def build_section(tools: dict, idx: dict) -> str:
    parts = [
        "_Generated by `scripts/build_report.py` from CI evidence. Verdicts come only from"
        " green runs on `testing-vhs` (constitution Principles I & II)._",
        "",
        badges(tools),
        "",
        grid(tools, idx),
        "",
        recordings(tools, idx),
        "",
        ledger(tools),
    ]
    return "\n".join(parts)


def main() -> int:
    tools = load_tools()
    idx = index(load_results())
    section = build_section(tools, idx)
    text = README.read_text(encoding="utf-8") if README.exists() else ""
    if START in text and END in text:
        pre = text.split(START)[0]
        post = text.split(END)[1]
        new = pre + START + "\n\n" + section + "\n" + END + post
    else:
        new = text.rstrip() + "\n\n" + START + "\n\n" + section + "\n" + END + "\n"
    README.write_text(new, encoding="utf-8")
    print("build_report: README updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
