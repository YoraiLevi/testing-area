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
ASSETS = ROOT / "assets"
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
    # Per-cell reasons collected in grid iteration order (tools in file order,
    # cells sorted); the index becomes the cell's `<sup>N</sup>` marker.
    notes: list[str] = []
    for t in tools["tools"]:
        unsupported = t.get("unsupported", {})
        fmts = " · ".join(t.get("formats", []))
        row = [f"[{t['name']}][{t['id']}]<br><sub>{fmts}</sub>", t["family"]]
        for c in cells:
            rec = idx.get((t["id"], c, headline))
            if rec is None:
                # No CI run for this cell: genuinely unsupported upstream vs. simply
                # outside the sampled matrix are distinct, honest states.
                if c in unsupported:
                    notes.append(f"**{t['name']} · `{c}`** — {unsupported[c]}")
                    row.append(f"➖<sup>{len(notes)}</sup>")
                else:
                    row.append("⬜")
                continue
            verdict = rec.get("verdict")
            glyph = VERDICT_GLYPH.get(verdict, "⬜")
            run = rec.get("run_url")
            cell_md = f"[{glyph}]({run})" if run else glyph
            # Any cell that ran in CI and did not succeed (a hard failure, or a
            # genuine platform limitation) is flagged with its reason in the notes.
            if verdict in ("broken", "skipped", "not-applicable") and rec.get("reason"):
                notes.append(f"**{t['name']} · `{c}`** — {rec['reason']}")
                cell_md += f"<sup>{len(notes)}</sup>"
            row.append(cell_md)
        rows.append("| " + " | ".join(row) + " |")
    legend = "\nLegend: ✅ working · ❌ broken · ➖ not applicable · ⬜ not evaluated\n"
    na_body = (
        "The recorder cannot target this OS/shell: the upstream project publishes no build"
        " for it, or a hard dependency is platform-specific (ttyd and libghostty-vt are"
        " Unix-only; PowerSession-rs is Windows-only). Cells with a specific cause carry"
        " their own numbered note below."
    )
    ne_body = (
        "This OS/shell was outside the sampled matrix for this recorder. The shell axis"
        " (bash/zsh/pwsh) was sampled rather than run exhaustively, so the tool may still"
        " work here; no CI run exists, so no verdict is claimed."
    )
    block = ["**Grid notes**", "",
             f"- **➖ not applicable** — {na_body}",
             f"- **⬜ not evaluated** — {ne_body}"]
    if notes:
        block.append("")
        block.extend(f"{i}. {n}" for i, n in enumerate(notes, 1))
    block.append("")
    notes_md = "\n".join(block)
    return (
        "### Capability Grid — headline scenario `launch-exit`\n\n"
        + "\n".join(rows) + "\n" + legend + "\n" + notes_md
    )


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
        out.append(f"#### {t['name']} (`{chosen}`)")
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


FAMILY_LABEL = {
    "scripted": "scripted (tape / guided)",
    "interactive": "interactive (live TTY session)",
    "hybrid": "hybrid (scripted tape + interactive live capture)",
}


def _modes_str(t: dict) -> str:
    m = t.get("modes", {})
    parts = [name for name, on in (("interactive", m.get("interactive")),
                                   ("scripted", m.get("scripted"))) if on]
    return " + ".join(parts) if parts else "—"


def asset_readmes(tools: dict) -> None:
    """Write assets/README.md (overview) and assets/<tool>/README.md (per format).

    Each recorder exports every format in its tools.json `formats` list, laid out
    as assets/<tool>/<format>/<cell>-<scenario>.<ext>. These indexes are generated
    from whatever files the recorders actually committed, so they never overclaim.
    """
    if not ASSETS.exists():
        return
    overview = [
        "# Recording assets",
        "",
        "Generated by `scripts/build_report.py`. Every recorder exports each output",
        "format it supports; files are laid out hierarchically as",
        "`<tool>/<format>/<cell>-<scenario>.<ext>`.",
        "",
        "| Tool | Family | Modes | Formats | Files |",
        "|------|--------|-------|---------|------:|",
    ]
    for t in tools["tools"]:
        tid = t["id"]
        tdir = ASSETS / tid
        fmt_files = {}
        total = 0
        for fmt in t["formats"]:
            fdir = tdir / fmt
            files = sorted(p.name for p in fdir.glob("*")) if fdir.is_dir() else []
            fmt_files[fmt] = files
            total += len(files)
        fmts_md = " · ".join(t["formats"])
        overview.append(
            f"| [{t['name']}]({tid}/) | {t['family']} | {_modes_str(t)}"
            f" | {fmts_md} | {total} |"
        )
        lines = [
            f"# {t['name']} — recording assets",
            "",
            f"- **Family:** {FAMILY_LABEL.get(t['family'], t['family'])}",
            f"- **Modes:** {_modes_str(t)}",
            f"- **Formats:** {fmts_md}",
            f"- **Converter:** {t['converter'] or 'none (native encoder)'}",
            f"- **Upstream:** {t['url']}",
            "",
            "Files are named `<cell>-<scenario>.<ext>` within each format directory.",
            "",
        ]
        for fmt in t["formats"]:
            files = fmt_files[fmt]
            lines.append(f"## `{fmt}` — {len(files)} file(s)")
            lines.append("")
            if files:
                lines.extend(f"- [`{name}`]({fmt}/{name})" for name in files)
            else:
                lines.append("_No files committed yet (cell broken or not evaluated)._")
            lines.append("")
        tdir.mkdir(parents=True, exist_ok=True)
        (tdir / "README.md").write_text("\n".join(lines), encoding="utf-8")
    (ASSETS / "README.md").write_text("\n".join(overview) + "\n", encoding="utf-8")
    print("build_report: asset READMEs updated")


def build_section(tools: dict, idx: dict) -> str:
    grid_md = grid(tools, idx)
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
    asset_readmes(tools)
    print("build_report: README updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
