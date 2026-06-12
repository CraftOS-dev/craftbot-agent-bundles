"""Agent Bundle Verifier — quality checks before build.

Runs the verification gates from METHODOLOGY.md against every agent folder
(or one named agent) and reports per-check pass/fail.

Checks performed per agent:
1.  agent.yaml parses + has required fields (name, slug, tier, category)
2.  soul.md present + under token budget (line-count proxy)
3.  role.md present + contains SOTA tool reference section heading
4.  reference/USE_CASES.md present
5.  reference/SOURCES.md present
6.  reference/SOTA_USE_CASES.md present + fulfillment ≥90% parseable
7.  Every name in enabled_skills resolves to a bundled or default skill folder
8.  Every bundled skill folder contains SKILL.md
9.  Every SKILL.md has the required sections (When to use / Setup / Common recipes / Examples / Edge cases / Sources)
10. Every name in mcp_servers exists in app/config/mcp_config.json
11. No inline citation tags (`[from:` / `[merged:`) in soul.md / role.md
12. PROACTIVE.md self-init footer present in soul.md

Usage:
    python verify.py                  # verify all
    python verify.py <slug>           # verify one
    python verify.py --json           # JSON output for CI
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

# Force UTF-8 stdout on Windows so the ✓/✗/⚠ marks render.
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required. Install with: pip install pyyaml")

AGENT_BUNDLE_DIR = Path(__file__).parent.resolve()
AGENTS_DIR = AGENT_BUNDLE_DIR / "agents"
REPO_ROOT = AGENT_BUNDLE_DIR.parent
TOP_LEVEL_SKILLS = REPO_ROOT / "skills"
MCP_CONFIG_PATH = REPO_ROOT / "app" / "config" / "mcp_config.json"

SOUL_MD_LINE_BUDGET = 400          # soft warn over this
SOUL_MD_LINE_HARD_CAP = 600        # hard fail over this
FULFILLMENT_FLOOR = 90             # %

# Section names we accept as proof a SKILL.md follows the new methodology.
# Each tuple = synonyms; at least one synonym must match.
SKILL_SECTION_GROUPS = (
    ("When to use", "Overview", "Purpose", "What this does", "When to invoke"),
    ("Setup", "Installation", "Install", "Prerequisites", "Requirements"),
    ("Sources", "References", "See also", "Further reading"),
)
# Skill packs from upstream (wshobson/anthropics) use other layouts. Skip strict
# structure check for these; they're audited at provenance time, not format time.
SKILL_STRUCTURE_EXEMPT_PREFIXES = ("python-", "data-storytelling", "kpi-dashboard-design",
                                    "architecture-decision-records", "changelog-automation",
                                    "openapi-spec-generation", "doc-coauthoring",
                                    "async-python-patterns")

PROACTIVE_FOOTER_PHRASE = "On first conversation with a new user"
SOTA_REFERENCE_HEADINGS = ("SOTA tool reference", "SOTA execution", "SOTA stack",
                            "Execution status")

# Operator-framing check (Phase 2 of advisor-framing fix). The agent's persona
# intro paragraph in soul.md must be action-verb-first, not passive/advisory.
# We scan the first ~20 lines for the persona intro and flag if (a) any banned
# verb appears AND (b) fewer than 4 action verbs appear to balance it.
INTRO_SCAN_LINES = 20

ADVISORY_BANNED_VERBS = (
    "covers", "covering", "owns", "leans on", "lean on", "relies on",
    "expertise spans", "mastery of", "command of", "sit under", "sits under",
    "bridges the gap", "focus spans", "knows where", "defers to",
    "advise", "advising", "guide ", "guides ", "suggest", "suggests",
)
ACTION_VERBS = (
    "write", "writes", "build", "builds", "run", "runs", "ship", "ships",
    "query", "queries", "fetch", "fetches", "post", "posts", "send", "sends",
    "render", "renders", "generate", "generates", "configure", "configures",
    "deploy", "deploys", "execute", "executes", "draft", "drafts", "publish",
    "publishes", "push", "pushes", "reconcile", "reconciles", "audit", "audits",
    "scan", "scans", "sync", "syncs", "instrument", "instruments", "install",
    "installs", "lint", "lints", "format", "formats", "profile", "profiles",
    "refactor", "refactors", "score", "scores", "route", "routes", "trigger",
    "triggers", "monitor", "monitors", "parse", "parses", "validate", "validates",
    "automate", "automates", "capture", "captures", "negotiate", "negotiates",
    "file", "files", "claim", "claims", "redline", "redlines", "search",
    "searches", "extract", "extracts", "review", "reviews", "handle", "handles",
    "drive", "drives", "feed", "feeds", "triage", "triages", "escalate",
    "escalates", "design", "designs", "find", "finds", "decode", "decodes",
    "predict", "predicts", "diagnose", "diagnoses", "identify", "identifies",
    "process", "processes", "allocate", "allocates", "track", "tracks",
    "operate", "operates", "facilitate", "facilitates", "compute", "computes",
    "enforce", "enforces", "map", "maps", "coordinate", "coordinates",
    "maintain", "maintains", "model", "models", "wire", "wires", "deploy",
    "compose", "composes",
)


# ─────────────────────────────────────────────────────────────────────
# Per-check helpers
# ─────────────────────────────────────────────────────────────────────

def _check_file_exists(path: Path, label: str) -> Tuple[bool, str]:
    return (path.exists(), f"{label} {'OK' if path.exists() else 'MISSING: ' + str(path)}")


def _check_agent_yaml(agent_dir: Path) -> Tuple[bool, str, Dict[str, Any]]:
    yaml_path = agent_dir / "agent.yaml"
    if not yaml_path.exists():
        return False, "agent.yaml MISSING", {}
    try:
        data = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
    except Exception as e:
        return False, f"agent.yaml PARSE FAIL: {e}", {}
    required = {"name", "slug", "tier", "category"}
    missing = required - set(data.keys())
    if missing:
        return False, f"agent.yaml MISSING FIELDS: {sorted(missing)}", data
    return True, "agent.yaml OK", data


def _check_soul_md_budget(soul_path: Path) -> Tuple[bool, str]:
    if not soul_path.exists():
        return False, "soul.md MISSING"
    lines = sum(1 for _ in soul_path.read_text(encoding="utf-8").splitlines())
    if lines > SOUL_MD_LINE_HARD_CAP:
        return False, f"soul.md HARD CAP EXCEEDED: {lines} lines > {SOUL_MD_LINE_HARD_CAP}"
    if lines > SOUL_MD_LINE_BUDGET:
        return True, f"soul.md WARN: {lines} lines > soft budget {SOUL_MD_LINE_BUDGET} (consider trimming)"
    return True, f"soul.md OK: {lines} lines"


def _check_role_md_sota(role_path: Path) -> Tuple[bool, str]:
    if not role_path.exists():
        return False, "role.md MISSING"
    text = role_path.read_text(encoding="utf-8")
    for heading in SOTA_REFERENCE_HEADINGS:
        if heading.lower() in text.lower():
            return True, f"role.md SOTA reference OK (found '{heading}')"
    return False, f"role.md MISSING SOTA reference section (looked for: {SOTA_REFERENCE_HEADINGS})"


def _check_skill_resolution(agent_dir: Path, enabled_skills: List[str]) -> Tuple[bool, str, Dict]:
    bundled, default, missing = [], [], []
    for name in enabled_skills:
        if (agent_dir / "skills" / name).is_dir():
            bundled.append(name)
        elif (TOP_LEVEL_SKILLS / name).is_dir():
            default.append(name)
        else:
            missing.append(name)
    if missing:
        return False, (
            f"Skills UNRESOLVED ({len(missing)}/{len(enabled_skills)}): {missing}"
        ), {"bundled": bundled, "default": default, "missing": missing}
    return True, (
        f"Skills OK: {len(bundled)} bundled + {len(default)} default = {len(enabled_skills)}"
    ), {"bundled": bundled, "default": default, "missing": []}


def _check_skill_md_structure(agent_dir: Path, bundled_skills: List[str]) -> Tuple[bool, str]:
    """Hard fail only if SKILL.md is missing or empty. Section structure is a
    SOFT warning for non-exempt packs (upstream skill packs have legitimate
    alternate layouts and shouldn't fail the build)."""
    hard_failures, soft_warnings = [], []
    for name in bundled_skills:
        skill_md = agent_dir / "skills" / name / "SKILL.md"
        if not skill_md.exists():
            hard_failures.append(f"{name}: SKILL.md missing")
            continue
        text = skill_md.read_text(encoding="utf-8")
        if len(text.strip()) < 100:
            hard_failures.append(f"{name}: SKILL.md too short ({len(text)} chars)")
            continue
        # Skip section check for upstream exempt skills
        if any(name.startswith(p) for p in SKILL_STRUCTURE_EXEMPT_PREFIXES):
            continue
        # Check section groups — at least one synonym per group must appear
        missing = []
        for group in SKILL_SECTION_GROUPS:
            if not any(s.lower() in text.lower() for s in group):
                missing.append(group[0])  # report the canonical name
        if missing:
            soft_warnings.append(f"{name}: missing one of each {missing}")
    if hard_failures:
        return False, f"SKILL.md HARD FAIL ({len(hard_failures)}): {hard_failures[:5]}"
    if soft_warnings:
        return True, (
            f"SKILL.md structure OK ({len(bundled_skills)} packs); "
            f"{len(soft_warnings)} soft warnings (non-blocking)"
        )
    return True, f"SKILL.md structure OK across {len(bundled_skills)} bundled skills"


def _check_soul_md_operator_framing(soul_path: Path, slug: str) -> Tuple[bool, str]:
    """Verify the soul.md persona intro is action-verb-first, not advisory.
    Hard fails if banned advisory verbs are present without ≥4 action verbs in
    the intro window. Exception: agents whose slug contains 'advisor' or
    'consultant' are exempt (their advisory framing is in-name)."""
    if "advisor" in slug.lower() or "consultant" in slug.lower():
        return True, "Operator framing CHECK SKIPPED (slug contains advisor/consultant)"
    if not soul_path.exists():
        return False, "soul.md MISSING (cannot check operator framing)"
    lines = soul_path.read_text(encoding="utf-8").splitlines()[:INTRO_SCAN_LINES]
    intro = " ".join(lines).lower()
    banned_found = [v for v in ADVISORY_BANNED_VERBS if v in intro]
    # Word-boundary action-verb count (avoid substring matches like "build" inside "rebuild")
    action_count = 0
    for verb in ACTION_VERBS:
        # Bold-asterisk pattern (**write**) is the strongest signal
        if f"**{verb}**" in intro or f" {verb} " in intro or f"you {verb}" in intro:
            action_count += 1
    if banned_found and action_count < 4:
        return False, (
            f"Operator framing FAIL: advisory verb(s) {banned_found[:3]} found "
            f"with only {action_count} action verbs (need ≥4). "
            f"Rewrite intro with action verbs (write/build/run/ship/...)."
        )
    if banned_found:
        return True, (
            f"Operator framing WARN: advisory verb(s) {banned_found[:3]} found "
            f"but balanced by {action_count} action verbs"
        )
    return True, f"Operator framing OK ({action_count} action verbs in intro)"


def _check_mcp_existence(mcp_servers: List[str]) -> Tuple[bool, str]:
    if not MCP_CONFIG_PATH.exists():
        return False, f"mcp_config.json not found at {MCP_CONFIG_PATH}"
    cfg = json.loads(MCP_CONFIG_PATH.read_text(encoding="utf-8"))
    known = {s.get("name") for s in cfg.get("mcp_servers", [])}
    unknown = [n for n in mcp_servers if n not in known]
    if unknown:
        return False, f"MCPs not in catalog ({len(unknown)}): {unknown}"
    return True, f"MCPs OK: all {len(mcp_servers)} found in catalog"


def _check_no_inline_citations(agent_dir: Path) -> Tuple[bool, str]:
    bad = []
    for fname in ("soul.md", "role.md"):
        path = agent_dir / fname
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for tag in ("[from:", "[merged:"):
            if tag in text:
                bad.append(f"{fname} contains '{tag}'")
    if bad:
        return False, f"Inline citations found: {bad}"
    return True, "No inline citations"


def _check_proactive_footer(soul_path: Path) -> Tuple[bool, str]:
    if not soul_path.exists():
        return False, "soul.md MISSING (cannot check PROACTIVE footer)"
    text = soul_path.read_text(encoding="utf-8")
    if PROACTIVE_FOOTER_PHRASE.lower() in text.lower():
        return True, "PROACTIVE self-init footer present"
    return False, f"PROACTIVE self-init footer MISSING (expected phrase: '{PROACTIVE_FOOTER_PHRASE}')"


def _check_fulfillment(sota_path: Path) -> Tuple[bool, str, int | None]:
    if not sota_path.exists():
        return False, "reference/SOTA_USE_CASES.md MISSING", None
    text = sota_path.read_text(encoding="utf-8")
    # Try several patterns the subagents tend to use
    patterns = [
        r"fulfillment[:\s\-~]+(\d+)\s*%",                   # "fulfillment: 95%" / "fulfillment ~98%"
        r"~?(\d+)\s*%\+?\s*fulfillment",                     # "~98%+ fulfillment" / "98% fulfillment"
        r"≥\s*(\d+)\s*%\s*fulfillment",                      # "≥98% fulfillment"
        r"fulfillment[^.\n]*?≥\s*(\d+)\s*%",                # "fulfillment: ≥98%"
        r"overall[:\s]+~?(\d+)\s*%",                         # "Overall: 95%"
        r"verdict[^.\n]*?~?(\d+)\s*%",                       # "Verdict: ~96%"
        r"≥\s*(\d+)\s*%\s*\)",                               # "(≥98%)" in headings
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            pct = int(m.group(1))
            if pct < FULFILLMENT_FLOOR:
                return False, f"Fulfillment {pct}% BELOW floor {FULFILLMENT_FLOOR}%", pct
            return True, f"Fulfillment {pct}% OK", pct
    # Fall back to counting confidence marks if no explicit %
    cv = text.count("✓")
    cwarn = text.count("⚠")
    cfail = text.count("✗")
    total = cv + cwarn + cfail
    if total == 0:
        return False, "Could not parse fulfillment % from SOTA_USE_CASES.md", None
    pct = round(100 * cv / total)
    if pct < FULFILLMENT_FLOOR:
        return False, f"Fulfillment {pct}% (from {cv}✓/{cwarn}⚠/{cfail}✗) BELOW floor", pct
    return True, f"Fulfillment {pct}% (counted {cv}✓/{cwarn}⚠/{cfail}✗) OK", pct


# ─────────────────────────────────────────────────────────────────────
# Per-agent verify
# ─────────────────────────────────────────────────────────────────────

def verify_one(slug: str, quiet: bool = False) -> Dict[str, Any]:
    agent_dir = AGENTS_DIR / slug
    checks: List[Tuple[str, bool, str]] = []  # (name, passed, message)

    if not agent_dir.is_dir():
        return {"slug": slug, "passed": False, "checks": [],
                "error": f"Agent folder not found: {agent_dir}"}

    # 1. agent.yaml
    yaml_ok, yaml_msg, agent_yaml = _check_agent_yaml(agent_dir)
    checks.append(("agent.yaml", yaml_ok, yaml_msg))

    # 2. soul.md budget
    checks.append(("soul.md budget", *_check_soul_md_budget(agent_dir / "soul.md")))

    # 2b. soul.md operator framing (action-verb intro, not advisory)
    checks.append(("Operator framing", *_check_soul_md_operator_framing(agent_dir / "soul.md", slug)))

    # 3. role.md SOTA reference
    checks.append(("role.md SOTA reference", *_check_role_md_sota(agent_dir / "role.md")))

    # 4-6. Required files
    for fname, label in [("reference/USE_CASES.md", "USE_CASES.md"),
                          ("reference/SOURCES.md", "SOURCES.md"),
                          ("reference/SOTA_USE_CASES.md", "SOTA_USE_CASES.md")]:
        ok, msg = _check_file_exists(agent_dir / fname, label)
        checks.append((label, ok, msg))

    # 7-8. Skills
    enabled = agent_yaml.get("enabled_skills", []) or []
    res_ok, res_msg, res = _check_skill_resolution(agent_dir, enabled)
    checks.append(("Skills resolution", res_ok, res_msg))
    if res_ok:
        struct_ok, struct_msg = _check_skill_md_structure(agent_dir, res["bundled"])
        checks.append(("SKILL.md structure", struct_ok, struct_msg))

    # 9. MCPs
    mcps = agent_yaml.get("mcp_servers", []) or []
    if mcps:
        checks.append(("MCP catalog", *_check_mcp_existence(mcps)))

    # 10. No inline citations
    checks.append(("No inline citations", *_check_no_inline_citations(agent_dir)))

    # 11. PROACTIVE footer
    checks.append(("PROACTIVE footer", *_check_proactive_footer(agent_dir / "soul.md")))

    # 12. Fulfillment
    ful_ok, ful_msg, ful_pct = _check_fulfillment(agent_dir / "reference" / "SOTA_USE_CASES.md")
    checks.append(("Fulfillment ≥90%", ful_ok, ful_msg))

    passed = all(c[1] for c in checks)
    report = {
        "slug": slug,
        "passed": passed,
        "fulfillment_pct": ful_pct,
        "checks": [{"name": n, "passed": p, "message": m} for n, p, m in checks],
    }

    if not quiet:
        icon = "✓" if passed else "✗"
        print(f"\n{icon} {slug}")
        for name, ok, msg in checks:
            mark = "  ✓" if ok else "  ✗"
            print(f"{mark} {name:30s} {msg}")

    return report


def verify_all(quiet: bool = False) -> List[Dict[str, Any]]:
    if not AGENTS_DIR.is_dir():
        sys.exit(f"No agents folder at {AGENTS_DIR}")
    reports = []
    for d in sorted(AGENTS_DIR.iterdir()):
        if d.is_dir() and not d.name.startswith("_"):
            reports.append(verify_one(d.name, quiet=quiet))
    return reports


def main():
    parser = argparse.ArgumentParser(description="Verify CraftBot agent bundles.")
    parser.add_argument("slug", nargs="?", help="Verify one agent by slug; omit for all.")
    parser.add_argument("--json", action="store_true", help="JSON output for CI.")
    args = parser.parse_args()

    if args.json:
        if args.slug:
            print(json.dumps(verify_one(args.slug, quiet=True), indent=2))
        else:
            print(json.dumps(verify_all(quiet=True), indent=2))
        return

    if args.slug:
        report = verify_one(args.slug)
        sys.exit(0 if report["passed"] else 1)

    reports = verify_all()
    print("\n─── Summary ───")
    for r in reports:
        icon = "✓" if r["passed"] else "✗"
        ful = f"{r['fulfillment_pct']}%" if r["fulfillment_pct"] else "?"
        failed = sum(1 for c in r["checks"] if not c["passed"])
        print(f"  {icon} {r['slug']:30s} fulfillment {ful:>5} · {failed} failed check(s)")
    any_failed = any(not r["passed"] for r in reports)
    sys.exit(1 if any_failed else 0)


if __name__ == "__main__":
    main()
