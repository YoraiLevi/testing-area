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
    "skipped": "➖",
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


def grid(tools: dict, idx: dict, footnotes: dict) -> str:
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
        row = [f"[{t['name']}][{t['id']}]", t["family"]]
        for c in cells:
            rec = idx.get((t["id"], c, headline))
            if rec is None:
                # A cell the tool never declared is not-applicable, not merely un-run.
                row.append("➖" if c not in t["cells"] else VERDICT_GLYPH[None])
                continue
            verdict = rec.get("verdict")
            glyph = VERDICT_GLYPH.get(verdict, "⬜")
            run = rec.get("run_url")
            cell_md = f"[{glyph}]({run})" if run else glyph
            # A cell the tool was actually exercised on but could not produce a GIF
            # carries its own footnote with the exact CI reason.
            if verdict in ("skipped", "not-applicable") and rec.get("reason"):
                fid = f"na-{t['id']}-{c}"
                footnotes[fid] = f"**{t['name']} — `{c}`:** {rec['reason']}"
                cell_md += f"[^{fid}]"
            row.append(cell_md)
        rows.append("| " + " | ".join(row) + " |")
    footnotes["na"] = (
        "**Not applicable (➖).** Either the recorder does not target that OS/shell combination, so"
        " no cell was declared for it (for example EVP and Terminalizer are Linux-only, and Demo"
        " Tape, termsvg, Foley, and Betamax publish no Windows build), or the recorder was exercised"
        " on that platform in CI but cannot produce a GIF headlessly — those cells carry their own"
        " footnote with the exact CI reason."
    )
    legend = "\nLegend: ✅ working · ❌ broken · ➖ not applicable[^na] · ⬜ not yet run\n"
    return "### Capability Grid — headline scenario `launch-exit`\n\n" + "\n".join(rows) + "\n" + legend


def recordings(tools: dict, idx: dict) -> str:
    scen = tools["scenarios"]
    pref = ["linux-bash", "linux-zsh", "macos-zsh", "linux-pwsh", "windows-pwsh"]
    # First resolve which tools have an embeddable recording set and where.
    sections = []  # (tool, chosen_cell, [(scenario, gif), ...])
    for t in tools["tools"]:
        chosen = None
        for c in pref + t["cells"]:
            if idx.get((t["id"], c, "launch-exit"), {}).get("verdict") == "working":
                chosen = c
                break
        if chosen is None:
            continue
        gifs = [
            (s, idx[(t["id"], chosen, s)]["gif"])
            for s in scen
            if idx.get((t["id"], chosen, s), {}).get("verdict") == "working"
            and idx.get((t["id"], chosen, s), {}).get("gif")
        ]
        if gifs:
            sections.append((t, chosen, gifs))

    out = ["### Recordings (per tool: minimal + creative)", ""]
    if not sections:
        out.append("_No working recordings committed yet. Trigger the `rec-*` workflows._")
        out.append("")
        return "\n".join(out)
    # Table of contents so readers can jump straight to a tool's GIFs.
    toc = " · ".join(f"[{t['name']}](#rec-{t['id']})" for t, _c, _g in sections)
    out.append(f"**Jump to a recording:** {toc}")
    out.append("")
    for t, chosen, gifs in sections:
        out.append(f'<a id="rec-{t["id"]}"></a>')
        out.append("")
        out.append(f"#### [{t['name']}]({t['url']}) (`{chosen}`)")
        out.append("")
        for s, gif in gifs:
            out.append(f"**{s}**")
            out.append("")
            out.append(f"![{t['name']} {s}]({gif})")
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


def analysis(tools: dict, idx: dict) -> str:
    """Data-driven recommendations: which tools produce working GIFs in each cell."""
    scen = tools["scenarios"]
    headline = tools["headline_scenario"]
    cells = []
    for t in tools["tools"]:
        for c in t["cells"]:
            if c not in cells:
                cells.append(c)
    cells.sort()

    # Per-tool: how many (cell, scenario) pairs are working.
    tool_working = {}
    for t in tools["tools"]:
        n = sum(
            1
            for c in t["cells"]
            for s in scen
            if idx.get((t["id"], c, s), {}).get("verdict") == "working"
        )
        tool_working[t["id"]] = (n, len(t["cells"]) * len(scen))

    out = [
        "### Analysis & Recommendations",
        "",
        "Reader: an engineer choosing a terminal recorder to capture `omp` in CI. Question: which"
        " tool reliably produces a GIF on each OS/shell? Every claim below is counted from committed"
        " CI result records, not reputation.",
        "",
        "**Per-cell recommendation** — tools whose headline `launch-exit` GIF is green in that cell,"
        " ordered by how many of the four scenarios they land:",
        "",
        "| Cell | Working recorders (working scenarios / 4) |",
        "|------|-------------------------------------------|",
    ]
    for c in cells:
        ranked = []
        for t in tools["tools"]:
            if idx.get((t["id"], c, headline), {}).get("verdict") != "working":
                continue
            n = sum(1 for s in scen if idx.get((t["id"], c, s), {}).get("verdict") == "working")
            ranked.append((n, t["name"], t["id"]))
        ranked.sort(key=lambda x: (-x[0], x[1].lower()))
        listing = ", ".join(f"[{name}][{tid}] ({n}/4)" for n, name, tid in ranked) or "_none_"
        out.append(f"| `{c}` | {listing} |")
    out.append("")

    # Full-house tools (every declared cell x scenario working).
    def link(t):
        return f"[{t['name']}][{t['id']}]"
    full = [t for t in tools["tools"] if tool_working[t["id"]][0] == tool_working[t["id"]][1] and tool_working[t["id"]][1] > 0]
    partial = [t for t in tools["tools"] if 0 < tool_working[t["id"]][0] < tool_working[t["id"]][1]]
    none = [t for t in tools["tools"] if tool_working[t["id"]][0] == 0]
    if full:
        out.append("**Green on every declared cell and scenario:** "
                   + ", ".join(link(t) for t in sorted(full, key=lambda t: t["name"].lower())) + ".")
        out.append("")
    if partial:
        frag = ", ".join(f"{link(t)} ({tool_working[t['id']][0]}/{tool_working[t['id']][1]})"
                         for t in sorted(partial, key=lambda t: t["name"].lower()))
        out.append("**Partial coverage (working / declared cell-scenarios):** " + frag + ".")
        out.append("")
    if none:
        out.append("**No working GIF in CI (honest skip/broken):** "
                   + ", ".join(link(t) for t in sorted(none, key=lambda t: t["name"].lower())) + ".")
        out.append("")
    return "\n".join(out)


def refs(tools: dict) -> str:
    """Named reference-link definitions for tool homepages, used across the report."""
    return "\n".join(f"[{t['id']}]: {t['url']}" for t in tools["tools"])


def footnote_defs(footnotes: dict) -> str:
    # `na` (the general legend note) first, then per-cell reasons in stable order.
    order = ["na"] + sorted(k for k in footnotes if k != "na")
    return "\n".join(f"[^{k}]: {footnotes[k]}" for k in order if k in footnotes)


def build_section(tools: dict, idx: dict) -> str:
    footnotes: dict = {}
    grid_md = grid(tools, idx, footnotes)
    parts = [
        "_Generated by `scripts/build_report.py` from CI evidence. Verdicts come only from"
        " green runs on `testing-vhs` (constitution Principles I & II)._",
        "",
        badges(tools),
        "",
        grid_md,
        "",
        analysis(tools, idx),
        "",
        recordings(tools, idx),
        "",
        ledger(tools),
        "",
        footnote_defs(footnotes),
        "",
        refs(tools),
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
