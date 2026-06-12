<!--
Source: https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Dev-Mode-MCP-Server
Figma Dev Mode MCP, GA 2025-2026
-->
# Figma Design Collaboration — SKILL

Figma Dev Mode MCP exposes frames, components, design tokens, and generated code snippets directly. This pack covers reading designs into PRDs, posting frame comments, and pushing handoff notes back to Linear.

## When to use

- Embedding a Figma frame URL into a PRD or Linear issue (handoff).
- Reading frame structure / components to validate design vs. PRD scope.
- Posting comments on specific frames (review feedback, copy edits).
- Extracting design tokens (colors, typography) for cross-team consistency docs.
- Generating component code snippets for engineering handoff.

Trigger phrases: "review this design", "leave feedback on the Figma frame", "extract design tokens", "pull frame for the PRD", "handoff design spec to Linear".

## Setup

```bash
# Figma Dev Mode MCP — connect via the official endpoint
# (Requires Dev Mode seat on Figma Org/Enterprise; Pro can read but limited features.)
npx -y @figma/dev-mode-mcp-server@latest

# Standalone REST fallback
curl -fsSL "https://api.figma.com/v1/me" \
  -H "X-FIGMA-TOKEN: $FIGMA_ACCESS_TOKEN"
```

Auth:
- `FIGMA_ACCESS_TOKEN` — personal access token from https://www.figma.com/settings (Account → Personal access tokens). Scopes: `file_content:read`, `file_comments:write`, `file_dev_resources:read`.

MCP tools available (`figma-mcp`):
- `get_file_frames` — list all top-level frames in a file (filter by page)
- `get_file_nodes` — fetch specific node(s) by ID
- `get_components` / `get_component_set` — component library traversal
- `get_design_tokens` — extract published tokens (colors, type, spacing)
- `get_code_snippet` — Dev Mode code generation per frame (React / Swift / Compose)
- `post_comment_on_frame` — leave threaded comment at node
- `list_comments` / `resolve_comment`

## Common recipes

### Recipe 1: List frames in a file (by page)

```bash
# Get the file_key from the Figma URL: figma.com/file/<file_key>/<title>
mcp tool figma.get_file_frames \
  --fileKey "abc123XYZ" \
  --pageName "Onboarding Revamp"
```

Returns frame IDs + names + URLs you can embed into a PRD.

### Recipe 2: Post a comment on a specific frame

```bash
# Find the node_id from frame URL: figma.com/file/.../?node-id=42%3A100
mcp tool figma.post_comment_on_frame \
  --fileKey "abc123XYZ" \
  --nodeId "42:100" \
  --message "Copy on this CTA reads as too sales-y; suggest 'Get started' over 'Start your free 14-day trial today'. Also: empty-state needs design."
```

### Recipe 3: Extract design tokens for the PRD appendix

```bash
mcp tool figma.get_design_tokens \
  --fileKey "abc123XYZ" \
  --output json \
| jq '{colors: .styles.colors, type: .styles.text, spacing: .styles.spacing}'
```

### Recipe 4: Generate React snippet for a component

```bash
mcp tool figma.get_code_snippet \
  --fileKey "abc123XYZ" \
  --nodeId "42:100" \
  --language "react-tsx" \
  --framework "tailwind"
```

### Recipe 5: Quick PRD-ready embed block

```bash
# Build a markdown table of frame name → URL for the PRD appendix
mcp tool figma.get_file_frames --fileKey "abc123XYZ" --pageName "Onboarding Revamp" \
| jq -r '.frames[] | "| \(.name) | [Frame](\(.url)) |"' \
| sed '1i| Frame | Link |\n|---|---|'
```

### Recipe 6: Audit a Figma file against PRD scope

```python
# Cross-check: does Figma have a frame per PRD acceptance criterion?
import requests
H = {"X-FIGMA-TOKEN": FIGMA_TOKEN}

frames = requests.get(f"https://api.figma.com/v1/files/{file_key}/nodes?ids={page_id}", headers=H).json()
frame_names = {f["name"].lower() for f in frames["nodes"][page_id]["document"]["children"]}

prd_states = {"empty state", "loading state", "error state", "success state"}
missing = prd_states - frame_names
print(f"Missing frames: {missing}")
```

### Recipe 7: Linear-Figma handoff (round-trip)

```bash
# 1. Create the Linear issue with the Figma frame link
mcp tool linear.create_issue \
  --teamKey "PROD" \
  --title "Onboarding step 2 — UI" \
  --description "Design spec: https://figma.com/file/abc123XYZ?node-id=42%3A100\n\n## AC\n- [ ] Empty state implemented\n- [ ] Loading state implemented"

# 2. Post a back-link comment on the Figma frame
mcp tool figma.post_comment_on_frame \
  --fileKey "abc123XYZ" \
  --nodeId "42:100" \
  --message "Engineering tracking: https://linear.app/team/issue/PROD-1234"
```

### Recipe 8: Resolve a comment thread when shipped

```bash
mcp tool figma.list_comments --fileKey "abc123XYZ" \
| jq '.[] | select(.message | contains("CTA copy"))'

mcp tool figma.resolve_comment --fileKey "abc123XYZ" --commentId "<id>"
```

### Recipe 9: Pull component set for a design-system PRD

```bash
mcp tool figma.get_component_set \
  --fileKey "design-system-file-key" \
  --setId "<Button-component-set-id>" \
| jq '.variants[] | {name, props}'
```

### Recipe 10: Export frame to PNG for the all-hands deck

```bash
# Export a frame as a 2x PNG for use in pptx
curl -fsSL "https://api.figma.com/v1/images/abc123XYZ?ids=42:100&scale=2&format=png" \
  -H "X-FIGMA-TOKEN: $FIGMA_ACCESS_TOKEN" \
| jq -r '.images["42:100"]' \
| xargs curl -o onboarding-step2.png
```

## Examples

### Example 1: Design review packet for the PRD
**Goal:** Build a "designs" section in the PRD that links the right frames.

**Steps:**
1. `get_file_frames` to list all frames on the "Onboarding Revamp" page.
2. Filter for ones that map to PRD user stories.
3. Build a markdown table (Recipe 5) and append to the Notion PRD via `notion-mcp` `append_block_children`.
4. Run a frame-coverage audit (Recipe 6) — any PRD AC without a frame becomes an open question.

**Result:** PRD has a "Design" section with frame links + a list of frames still owed by design.

### Example 2: Async design critique
**Goal:** Leave structured feedback without scheduling a meeting.

**Steps:**
1. Walk through Figma frames in the file (`get_file_frames`).
2. For each problematic frame, `post_comment_on_frame` with feedback (be specific: cite the user story or AC).
3. Post a single summary comment on the page-level frame (call out top-3 blockers).
4. Notify the designer in Slack with the file link.

**Result:** Threaded comments at the relevant node = preserved context; no synchronous review needed.

## Edge cases / gotchas

- **Dev Mode seat requirement.** `get_code_snippet` and `get_design_tokens` require Dev Mode (Org/Enterprise plan). Personal/Pro plan returns a 403.
- **Token scopes.** Personal tokens default to read-only; comments require `file_comments:write` checked at token-create time.
- **File key vs node ID confusion.** `file_key` is in the URL `figma.com/file/<key>`. Node IDs use `:` (e.g., `42:100`) but URL-encoded `%3A`. The MCP normalizes both, raw REST does not.
- **Rate limits.** Figma REST: 100 req/min per token; bulk node fetches via `?ids=` are much cheaper than N separate calls.
- **Comments don't tag people automatically.** Mention with `@figma_user_id` syntax (look up via `/v1/users`).
- **Image exports** (`/v1/images`) return temporary CDN URLs valid ~30 min; download immediately.
- **Component changes break references.** Embedded frame URLs to a component variant break if the designer renames the variant; prefer node-ID references over name-based.
- **No write access to frames.** The API is read + comment; you cannot create/edit nodes programmatically (except via the Figma plugin SDK, separate surface).
- **File permissions cascade.** A file you can read might be in a project where you cannot list other files; scope token narrow.

## Sources

- [Figma Dev Mode MCP guide](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Dev-Mode-MCP-Server)
- [Figma REST API reference](https://www.figma.com/developers/api)
- [Comments endpoint](https://www.figma.com/developers/api#comments-endpoints)
- [Design tokens via Variables API](https://www.figma.com/developers/api#variables)
- [Code Connect (Dev Mode → code)](https://help.figma.com/hc/en-us/articles/26956746233623-Code-Connect)
