"""Agent Bundle Builder — turn agents/<slug>/ into dist/<slug>.craftbot

Reads agent.yaml + soul.md + role.md + reference/SOTA_USE_CASES.md + skills/<bundled>/
and produces a `.craftbot` zip in the same format the existing profile-bundle
importer expects (see app/ui_layer/settings/profile_bundle.py).

Output structure:
    <slug>.craftbot (zip)
    ├── manifest.json
    ├── README.md
    ├── profile/
    │   ├── SOUL.md   (from soul.md)
    │   └── AGENT.md  (from role.md)
    ├── skills/
    │   ├── enabled.json   ({"enabled_skills": [...]})
    │   └── <bundled-skill>/SKILL.md  (each bundled skill folder copied verbatim)
    └── mcp/
        └── servers.json   ({"mcp_servers": [...env values stripped...]})

Default skills (already shipped with CraftBot) are listed by name in enabled.json
but their folders are NOT copied — the recipient already has them.

Usage:
    python build.py                  # build all agents
    python build.py <slug>           # build one agent
    python build.py --verify-only    # run verify.py without building
    python build.py --skip-verify    # build without running verify.py first
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

# Force UTF-8 stdout on Windows so the ✓/✗ marks render.
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

# Paths anchored on this file's location (agent_bundle/build.py)
AGENT_BUNDLE_DIR = Path(__file__).parent.resolve()
AGENTS_DIR = AGENT_BUNDLE_DIR / "agents"
DIST_DIR = AGENT_BUNDLE_DIR / "dist"
REPO_ROOT = AGENT_BUNDLE_DIR.parent
TOP_LEVEL_SKILLS = REPO_ROOT / "skills"
MCP_CONFIG_PATH = REPO_ROOT / "app" / "config" / "mcp_config.json"
SKILLS_CONFIG_PATH = REPO_ROOT / "app" / "config" / "skills_config.json"

BUNDLE_FORMAT_VERSION = "1.0"

# Names in MCP env-var keys that indicate secrets. Keys are kept (so the
# recipient knows what to fill in); values are stripped.
SECRET_ENV_HINTS = ("KEY", "TOKEN", "SECRET", "PASSWORD", "PASS", "CREDENTIAL")

SKIP_DIR_NAMES = {
    "node_modules", "dist", "build", ".next", ".nuxt", ".cache",
    ".turbo", ".vite", ".git", "__pycache__",
}
SKIP_FILE_SUFFIXES = (".db", ".sqlite", ".sqlite3", ".db-journal", ".pyc")


# ─────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────

def _load_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default if default is not None else {}
    return json.loads(path.read_text(encoding="utf-8"))


def _load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing: {path}")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _should_skip(path: Path) -> bool:
    if path.name in SKIP_DIR_NAMES:
        return True
    if path.is_file() and any(path.name.lower().endswith(s) for s in SKIP_FILE_SUFFIXES):
        return True
    return False


def _copy_dir_filtered(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    dst.mkdir(parents=True, exist_ok=True)
    for entry in src.iterdir():
        if _should_skip(entry):
            continue
        target = dst / entry.name
        if entry.is_dir():
            _copy_dir_filtered(entry, target)
        else:
            shutil.copy2(entry, target)


def _strip_mcp_secrets(servers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    cleaned = []
    for server in servers:
        s = dict(server)
        env = dict(s.get("env") or {})
        for key in list(env.keys()):
            if any(hint in key.upper() for hint in SECRET_ENV_HINTS):
                env[key] = ""  # blank — recipient fills in
        s["env"] = env
        cleaned.append(s)
    return cleaned


# ─────────────────────────────────────────────────────────────────────
# Skill resolution
# ─────────────────────────────────────────────────────────────────────

def _resolve_skill(name: str, agent_dir: Path) -> Tuple[str, Path | None]:
    """Return ('bundled', path) | ('default', None) | ('missing', None)."""
    bundled = agent_dir / "skills" / name
    if bundled.is_dir():
        return ("bundled", bundled)
    default = TOP_LEVEL_SKILLS / name
    if default.is_dir():
        return ("default", None)
    return ("missing", None)


# ─────────────────────────────────────────────────────────────────────
# Build one agent
# ─────────────────────────────────────────────────────────────────────

def _build_manifest(agent_yaml: Dict[str, Any], skills_resolution: Dict[str, str],
                    mcp_servers: List[str], fulfillment: str | None) -> Dict[str, Any]:
    return {
        "bundle_format_version": BUNDLE_FORMAT_VERSION,
        "name": agent_yaml.get("name", agent_yaml.get("slug", "Unknown")),
        "slug": agent_yaml.get("slug", ""),
        "description": (agent_yaml.get("description") or "").strip(),
        "tier": agent_yaml.get("tier", ""),
        "category": agent_yaml.get("category", ""),
        "tags": agent_yaml.get("tags", []),
        "source_app_version": "agent-bundle-build",
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "fulfillment": fulfillment,
        "contents": {
            "agent_name": agent_yaml.get("name", ""),
            "md_files": ["SOUL.md", "AGENT.md"],
            "skills": [s for s in skills_resolution.keys()],
            "skills_bundled": [n for n, kind in skills_resolution.items() if kind == "bundled"],
            "skills_default": [n for n, kind in skills_resolution.items() if kind == "default"],
            "mcp_servers": mcp_servers,
            "living_ui_apps": [],
        },
    }


def _build_readme(manifest: Dict[str, Any]) -> str:
    c = manifest["contents"]
    skills_b = "\n".join(f"- {s}" for s in c["skills_bundled"]) or "_(none)_"
    skills_d = "\n".join(f"- {s}" for s in c["skills_default"]) or "_(none)_"
    mcps = "\n".join(f"- {s}" for s in c["mcp_servers"]) or "_(none)_"
    return (
        f"# {manifest['name']} — CraftBot agent bundle\n\n"
        f"{manifest['description'] or '_(no description)_'}\n\n"
        f"**Tier:** {manifest['tier']} · **Category:** {manifest['category']} · "
        f"**Fulfillment:** {manifest['fulfillment'] or 'unknown'}\n\n"
        f"Bundle format: `{manifest['bundle_format_version']}`  "
        f"Created: `{manifest['created_at']}`\n\n"
        f"## Personality\n- SOUL.md (always-on identity)\n- AGENT.md (role/playbooks/SOTA tool reference, grep-only)\n\n"
        f"## Bundled skills (ship inside this .craftbot)\n{skills_b}\n\n"
        f"## CraftBot default skills (already on recipient's install)\n{skills_d}\n\n"
        f"## MCP servers (recipient enables in MCP settings)\n{mcps}\n\n"
        "API keys, OAuth secrets, personal memory, and conversation history "
        "are **not** included in this bundle.\n"
    )


def _read_fulfillment(agent_dir: Path) -> str | None:
    """Parse reference/SOTA_USE_CASES.md for the fulfillment %. Matches the
    same patterns verify.py uses so the two stay consistent."""
    sota = agent_dir / "reference" / "SOTA_USE_CASES.md"
    if not sota.exists():
        return None
    import re
    text = sota.read_text(encoding="utf-8")
    patterns = [
        r"fulfillment[:\s\-~]+(\d+)\s*%",
        r"~?(\d+)\s*%\+?\s*fulfillment",
        r"≥\s*(\d+)\s*%\s*fulfillment",
        r"fulfillment[^.\n]*?≥\s*(\d+)\s*%",
        r"overall[:\s]+~?(\d+)\s*%",
        r"verdict[^.\n]*?~?(\d+)\s*%",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return f"{match.group(1)}%"
    return None


def build_agent(slug: str, verbose: bool = True) -> Dict[str, Any]:
    agent_dir = AGENTS_DIR / slug
    if not agent_dir.is_dir():
        return {"success": False, "slug": slug, "error": f"Agent folder not found: {agent_dir}"}

    # Read agent.yaml
    try:
        agent_yaml = _load_yaml(agent_dir / "agent.yaml")
    except Exception as e:
        return {"success": False, "slug": slug, "error": f"agent.yaml parse failed: {e}"}

    # Resolve enabled_skills
    enabled_skills = agent_yaml.get("enabled_skills", []) or []
    resolution: Dict[str, str] = {}  # name → 'bundled' | 'default'
    missing: List[str] = []
    for name in enabled_skills:
        kind, _path = _resolve_skill(name, agent_dir)
        if kind == "missing":
            missing.append(name)
        else:
            resolution[name] = kind
    if missing:
        return {"success": False, "slug": slug,
                "error": f"Skills not resolved (no folder in agents/{slug}/skills/ or repo skills/): {', '.join(missing)}"}

    # Resolve MCP servers — look up each name in the source mcp_config.json
    mcp_names = agent_yaml.get("mcp_servers", []) or []
    src_mcp_cfg = _load_json(MCP_CONFIG_PATH, {"mcp_servers": []})
    src_by_name = {s.get("name"): s for s in src_mcp_cfg.get("mcp_servers", [])}
    mcp_servers_full: List[Dict[str, Any]] = []
    mcp_unknown: List[str] = []
    for name in mcp_names:
        if name in src_by_name:
            server = dict(src_by_name[name])
            server["enabled"] = True  # recommend enable on import
            mcp_servers_full.append(server)
        else:
            mcp_unknown.append(name)
            # Synthesize minimal stub so the import flow shows it as needs-enable
            mcp_servers_full.append({"name": name, "enabled": True, "env": {},
                                     "_note": "Not found in CraftBot catalog at build time"})
    mcp_servers_full = _strip_mcp_secrets(mcp_servers_full)

    fulfillment = _read_fulfillment(agent_dir)
    manifest = _build_manifest(agent_yaml, resolution, mcp_names, fulfillment)

    # Build staging dir
    staging = Path(tempfile.mkdtemp(prefix=f"craftbot_build_{slug}_"))
    try:
        # manifest.json + README.md
        (staging / "manifest.json").write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
        (staging / "README.md").write_text(_build_readme(manifest), encoding="utf-8")

        # profile/ — SOUL.md from soul.md, AGENT.md from role.md
        profile = staging / "profile"
        profile.mkdir()
        soul_src = agent_dir / "soul.md"
        role_src = agent_dir / "role.md"
        if not soul_src.exists():
            return {"success": False, "slug": slug, "error": "soul.md missing"}
        if not role_src.exists():
            return {"success": False, "slug": slug, "error": "role.md missing"}
        shutil.copy2(soul_src, profile / "SOUL.md")
        shutil.copy2(role_src, profile / "AGENT.md")

        # skills/ — copy bundled folders, write enabled.json
        skills_dir = staging / "skills"
        skills_dir.mkdir()
        (skills_dir / "enabled.json").write_text(
            json.dumps({"enabled_skills": list(resolution.keys())}, indent=2),
            encoding="utf-8")
        for name, kind in resolution.items():
            if kind == "bundled":
                _copy_dir_filtered(agent_dir / "skills" / name, skills_dir / name)

        # mcp/ — servers.json
        mcp_dir = staging / "mcp"
        mcp_dir.mkdir()
        (mcp_dir / "servers.json").write_text(
            json.dumps({"mcp_servers": mcp_servers_full}, indent=2, ensure_ascii=False),
            encoding="utf-8")

        # Zip
        DIST_DIR.mkdir(exist_ok=True)
        ts = time.strftime("%Y%m%d")
        out_path = DIST_DIR / f"{slug}-{ts}.craftbot"
        with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for entry in staging.rglob("*"):
                if entry.is_file():
                    zf.write(entry, entry.relative_to(staging))

        size_kb = out_path.stat().st_size // 1024
        bundled_count = sum(1 for k in resolution.values() if k == "bundled")
        default_count = sum(1 for k in resolution.values() if k == "default")
        result = {
            "success": True, "slug": slug,
            "path": str(out_path),
            "size_kb": size_kb,
            "skills_bundled": bundled_count,
            "skills_default": default_count,
            "mcp_count": len(mcp_servers_full),
            "mcp_unknown": mcp_unknown,
            "fulfillment": fulfillment,
        }
        if verbose:
            note = f" ({len(mcp_unknown)} MCPs not in catalog)" if mcp_unknown else ""
            print(f"  ✓ {slug:30s} → {out_path.name}  "
                  f"{size_kb}KB · {bundled_count}b+{default_count}d skills · "
                  f"{len(mcp_servers_full)} MCPs{note} · fulfillment {fulfillment or '?'}")
        return result
    finally:
        shutil.rmtree(staging, ignore_errors=True)


# ─────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Build CraftBot agent bundles.")
    parser.add_argument("slug", nargs="?", help="Build a single agent by slug; omit to build all.")
    parser.add_argument("--verify-only", action="store_true",
                        help="Run verify.py only; do not build.")
    parser.add_argument("--skip-verify", action="store_true",
                        help="Skip the pre-build verify.py pass.")
    args = parser.parse_args()

    # Run verify first unless skipped
    if not args.skip_verify:
        try:
            from verify import verify_all, verify_one  # local import
        except ImportError:
            print("⚠ verify.py not found; proceeding without verification.")
            verify_all = verify_one = None  # type: ignore

        if verify_all and verify_one:
            print("─── Verification ───")
            verify_failed = False
            if args.slug:
                report = verify_one(args.slug)
                if not report["passed"]:
                    verify_failed = True
            else:
                reports = verify_all()
                if any(not r["passed"] for r in reports):
                    verify_failed = True
            if args.verify_only:
                sys.exit(0 if not verify_failed else 1)
            if verify_failed:
                print("\n✗ Verification failed. Fix issues above or pass --skip-verify.")
                sys.exit(1)

    # Build
    print("\n─── Build ───")
    if args.slug:
        result = build_agent(args.slug)
        sys.exit(0 if result["success"] else 1)
    else:
        if not AGENTS_DIR.is_dir():
            sys.exit(f"No agents folder at {AGENTS_DIR}")
        results = []
        for agent_dir in sorted(AGENTS_DIR.iterdir()):
            if agent_dir.is_dir() and not agent_dir.name.startswith("_"):
                results.append(build_agent(agent_dir.name))
        ok = sum(1 for r in results if r["success"])
        print(f"\nBuilt {ok}/{len(results)} agents into {DIST_DIR}")
        failed = [r for r in results if not r["success"]]
        for r in failed:
            print(f"  ✗ {r['slug']}: {r.get('error', 'unknown error')}")
        sys.exit(0 if not failed else 1)


if __name__ == "__main__":
    main()
