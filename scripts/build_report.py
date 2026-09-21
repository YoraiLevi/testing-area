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
    lines = ["### CI Status", ""]
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
    # Notes are deduped by (tool, reason): cells sharing a cause collapse into one
    # numbered note listing every affected cell, not repeated identical text.
    note_num: dict[tuple[str, str], int] = {}
    note_cells: dict[tuple[str, str], list[str]] = {}

    def mark(tool_name: str, cell: str, reason: str) -> int:
        key = (tool_name, reason)
        if key not in note_num:
            note_num[key] = len(note_num) + 1
            note_cells[key] = []
        note_cells[key].append(cell)
        return note_num[key]

    ne_used = False
    for t in tools["tools"]:
        unsupported = t.get("unsupported", {})
        fmts = " · ".join(t.get("formats", []))
        row = [f"[{t['name']}][{t['id']}]<br><sub>{fmts}</sub>", t["family"]]
        for c in cells:
            rec = idx.get((t["id"], c, headline))
            if rec is None:
                # No CI run for this cell: an upstream limit (➖) and simply outside the
                # grid's OS/shell matrix (⬜) are distinct, honest states.
                if c in unsupported:
                    row.append(f"➖<sup>{mark(t['name'], c, unsupported[c])}</sup>")
                else:
                    row.append("⬜")
                    ne_used = True
                continue
            verdict = rec.get("verdict")
            glyph = VERDICT_GLYPH.get(verdict, "⬜")
            run = rec.get("run_url")
            cell_md = f"[{glyph}]({run})" if run else glyph
            # Any cell that ran and did not succeed (hard failure or platform limit) is
            # flagged with its reason in the numbered notes.
            if verdict in ("broken", "skipped", "not-applicable") and rec.get("reason"):
                cell_md += f"<sup>{mark(t['name'], c, rec['reason'])}</sup>"
            row.append(cell_md)
        rows.append("| " + " | ".join(row) + " |")
    legend = ("\nLegend: ✅ working · ❌ broken · ➖ not applicable"
              + (" · ⬜ not evaluated" if ne_used else "") + "\n")
    na_body = "No upstream build, or a platform-only dependency. Numbered notes give the cell's cause."
    block = ["**Grid notes**", "", f"- **➖ not applicable.** {na_body}"]
    if ne_used:
        block.append(
            "- **⬜ not evaluated.** No CI run exists for this OS/shell, so no verdict is claimed."
        )
    if note_num:
        block.append("")
        for (tool_name, reason), num in note_num.items():
            cs = ", ".join(f"`{c}`" for c in note_cells[(tool_name, reason)])
            block.append(f"{num}. **{tool_name} · {cs}**: {reason}")
    block.append("")
    notes_md = "\n".join(block)
    return (
        "### Capability Grid (headline scenario `launch-exit`)\n\n"
        + "\n".join(rows) + "\n" + legend + "\n" + notes_md
    )


def recordings(tools: dict, idx: dict) -> str:
    """Point readers at each tool's asset page instead of embedding GIFs here.

    The samples live in assets/<tool>/README.md (one per output format), so the
    main report stays small and every format is viewable in one place.
    """
    scen = tools["scenarios"]
    pref = ["linux-bash", "linux-zsh", "macos-zsh", "linux-pwsh", "windows-pwsh"]
    have = []  # tools with at least one committed working recording
    for t in tools["tools"]:
        for c in pref + t["cells"]:
            if idx.get((t["id"], c, "launch-exit"), {}).get("verdict") != "working":
                continue
            if any(idx.get((t["id"], c, s), {}).get("verdict") == "working"
                   and idx.get((t["id"], c, s), {}).get("gif") for s in scen):
                have.append(t)
                break
    out = ["### Recordings", ""]
    if not have:
        out.append("_No working recordings committed yet. Trigger the `rec-*` workflows._")
        out.append("")
        return "\n".join(out)
    toc = " · ".join(f"[{t['name']}](assets/{t['id']}/README.md)" for t in have)
    out.append("Each tool's recordings, one sample per output format, live on its asset page.")
    out.append("")
    out.append(f"**Jump to a recording:** {toc}")
    out.append("")
    return "\n".join(out)


def ledger(tools: dict) -> str:
    out = ["### Skipped Tools", "",
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

    # Per-tool tallies. A not-applicable cell (an upstream limit) is NOT a coverage
    # failure, so it is kept out of the denominator; "attempted" counts only the cells
    # the tool actually ran (working or broken). This stops a Unix-only tool that omits
    # Windows from outscoring one that declares Windows and records it not-applicable.
    tally = {}
    for t in tools["tools"]:
        working = attempted = na = 0
        for c in t["cells"]:
            for s in scen:
                v = idx.get((t["id"], c, s), {}).get("verdict")
                if v == "working":
                    working += 1
                    attempted += 1
                elif v in ("broken", "skipped"):
                    attempted += 1
                elif v == "not-applicable":
                    na += 1
        tally[t["id"]] = (working, attempted, na)

    out = [
        "### What To Use",
        "",
        "Headline `launch-exit` green, ranked by how many of the four tapes landed.",
        "",
        "| Cell | Working recorders (scenarios / 4) |",
        "|------|-----------------------------------|",
    ]
    # Build each cell's listing, then collapse cells that share an identical listing.
    listings = []
    for c in cells:
        ranked = []
        for t in tools["tools"]:
            if idx.get((t["id"], c, headline), {}).get("verdict") != "working":
                continue
            n = sum(1 for s in scen if idx.get((t["id"], c, s), {}).get("verdict") == "working")
            ranked.append((n, t["name"], t["id"]))
        ranked.sort(key=lambda x: (-x[0], x[1].lower()))
        listing = ", ".join(f"[{name}][{tid}] ({n}/4)" for n, name, tid in ranked) or "_none_"
        listings.append((c, listing))
    grouped = []
    for c, listing in listings:
        for g in grouped:
            if g[0] == listing:
                g[1].append(c)
                break
        else:
            grouped.append((listing, [c]))
    for listing, cs in grouped:
        label = " · ".join(f"`{c}`" for c in cs)
        out.append(f"| {label} | {listing} |")
    out.append("")

    def link(t):
        return f"[{t['name']}][{t['id']}]"

    def frag(t):
        w, a, na = tally[t["id"]]
        suffix = f", {na} N/A" if na else ""
        return f"{link(t)} ({w}/{a}{suffix})"

    full = [t for t in tools["tools"]
            if tally[t["id"]][1] > 0 and tally[t["id"]][0] == tally[t["id"]][1]]
    partial = [t for t in tools["tools"] if 0 < tally[t["id"]][0] < tally[t["id"]][1]]
    none = [t for t in tools["tools"] if tally[t["id"]][0] == 0]
    if full:
        out.append("**Green on every cell they target:** "
                   + ", ".join(frag(t) for t in sorted(full, key=lambda t: t["name"].lower())) + ".")
        out.append("")
    if partial:
        out.append("**Attempted and failed at least one cell:** "
                   + ", ".join(frag(t) for t in sorted(partial, key=lambda t: t["name"].lower())) + ".")
        out.append("")
    if none:
        out.append("**No working GIF in CI:** "
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


# Formats GitHub reliably inline-renders in Markdown via ![](path). svg is flaky and
# mp4/webm/avi/cast/svgz/yml never inline, so those are linked with a gif preview instead.
INLINE = {"gif", "webp", "png", "apng", "jpg", "jpeg"}
# Prefer a visually rich scenario for the single representative sample.
_SCENARIO_PREF = ("help-tour", "typing-demo", "tui-splash", "launch-exit")


def _representative(files):
    """Pick one representative file per format, favouring a busy scenario."""
    for pref in _SCENARIO_PREF:
        for name in files:
            if pref in name:
                return name
    return files[0] if files else None


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
            rep = _representative(files)
            if rep and fmt in INLINE:
                lines.append(f"![{t['name']} {fmt} sample: {rep}]({fmt}/{rep})")
                lines.append("")
            elif rep:
                lines.append(
                    f"Sample: [`{rep}`]({fmt}/{rep}) (`{fmt}` does not render inline on GitHub)."
                )
                cell = rep.rsplit(".", 1)[0]
                gif_name = f"{cell}.gif"
                if fmt != "gif" and gif_name in fmt_files.get("gif", []):
                    lines.append("")
                    lines.append(
                        f"![{t['name']} {cell} (gif preview of the same cell)](gif/{gif_name})"
                    )
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
        "_Generated from committed CI results on `testing-vhs`._",
        "",
        grid_md,
        "",
        analysis(tools, idx),
        "",
        recordings(tools, idx),
        "",
        ledger(tools),
        "",
        badges(tools),
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
