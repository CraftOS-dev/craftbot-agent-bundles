<!--
Sources: https://docs.snapshot.org/ + https://dev.mirror.xyz/ + https://docs.lens.xyz/ + https://collab.land/ + https://docs.farcaster.xyz/ + https://docs.guild.xyz/
-->
# Web3 Community (Snapshot / Mirror / Lens / Collab.Land) — SKILL

Decentralized community ops: Snapshot for off-chain governance voting; Aragon for on-chain DAOs; Mirror for token-gated content publishing; Lens Protocol for decentralized social graph; Farcaster for crypto-native social; Guild.xyz + Collab.Land for token-/NFT-gated Discord & Telegram roles. Workflow: governance space + voting strategy → publication for token-holder updates → gated channels via wallet-token-presence check.

## When to use

- New Web3 / token-holder community needing governance + gated comms.
- Existing DAO without formal off-chain voting (Snapshot setup).
- NFT project gating Discord channels by holder status (Collab.Land / Guild.xyz).
- Token-holder newsletter / publication launch (Mirror).
- Decentralized social presence (Lens / Farcaster).
- Multi-channel sync: Snapshot vote → community announcement → Mirror post.
- Migration off centralized platforms (legal / sanctions reasons).
- Cross-link to `gated-community-memberstack-outseta-substack` for fiat-paid hybrid.

Trigger phrases: "DAO", "web3 community", "Snapshot vote", "Mirror publication", "Lens protocol", "Farcaster", "Collab.Land", "Guild.xyz", "NFT gated", "token gated Discord", "governance vote", "crypto community", "wallet sign-in".

## Setup

```bash
# Snapshot — no API key for read; signing for write
curl https://hub.snapshot.org/api/spaces/yieldfarm.eth
# GraphQL endpoint for queries
curl -X POST https://hub.snapshot.org/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ space(id:\"yieldfarm.eth\") { name votingPower } }"}'

# Snapshot.js CLI for vote creation (server-side signing wallet)
npx snapshot.js create-proposal --space yieldfarm.eth --signer 0x...

# Mirror — REST + GraphQL (Mirror dev)
curl https://api.mirror.xyz/v0/publications/brand.mirror.xyz

# Lens Protocol — GraphQL
curl -X POST https://api.lens.dev/ \
  -H "Content-Type: application/json" \
  -d '{"query":"{ profile(request:{handle:\"brand.lens\"}) { id name } }"}'

# Farcaster — Hub API
curl https://nemes.farcaster.xyz:2281/v1/userDataByFid?fid=12345

# Collab.Land — admin via Discord bot commands; API in beta
# Install: https://collab.land/invite

# Guild.xyz — REST API
curl -H "Authorization: Bearer $GUILD_TOKEN" \
  https://api.guild.xyz/v2/guilds/brand
```

Auth + env:
- `ETHEREUM_RPC_URL` — Alchemy / Infura / public RPC (https://eth.public-rpc.com).
- `SNAPSHOT_HUB_URL=https://hub.snapshot.org` — Snapshot mainnet hub.
- `SNAPSHOT_PROPOSAL_SIGNER_PK` — wallet PK for server-side proposal creation (cold wallet recommended).
- `MIRROR_API_KEY` — Mirror → Settings → API.
- `LENS_BEARER_TOKEN` — Lens login flow.
- `FARCASTER_FID` + `FARCASTER_SIGNER_PK` — Farcaster account.
- `GUILD_API_KEY` — Guild.xyz → Settings.
- `DISCORD_BOT_TOKEN` — for role sync via Collab.Land webhooks.

Workspace prerequisites:
- ENS domain or self-controlled smart contract address for Snapshot space.
- Discord server with role hierarchy (bot above gated roles).
- Telegram chat (optional) with Collab.Land or Guild bot admin.
- Wallet-connect flow on landing page (RainbowKit / WalletConnect / Privy).

## Common recipes

### Recipe 1: Stack picker

| Need | Tool | Why |
|---|---|---|
| Off-chain governance vote | Snapshot | SOTA; gas-free; 1.5M+ DAOs use it |
| On-chain treasury actions | Aragon / Tally / Safe | Execution requires on-chain |
| Token-gated publishing | Mirror | Crypto-native Substack |
| Decentralized social graph | Lens or Farcaster | Lens for protocol; Farcaster for Twitter alt |
| NFT-gated Discord roles | Collab.Land | Bot, point-and-click setup |
| Token + custom rule gated roles | Guild.xyz | More flexible than Collab.Land |
| Telegram-gated | Collab.Land Telegram bot | Same install pattern |

Default Web3 community stack: Snapshot + Mirror + Collab.Land + Discord. Add Farcaster for social-graph presence.

### Recipe 2: Snapshot space setup

```bash
# Create space (admin signs with ENS-controlling wallet)
# Use https://snapshot.org/#/spaces/create UI for first space

# Configuration via space settings (snapshot.org/#/spaces/yieldfarm.eth/settings):
cat <<EOF > snapshot_space.yaml
name: BrandDAO
network: '1'  # Ethereum mainnet
symbol: BRAND
admins:
  - 0xAAAA...
  - 0xBBBB...
strategies:
  - name: erc20-balance-of
    params:
      address: '0xBrandTokenAddress'
      decimals: 18
      symbol: BRAND
voting:
  delay: 0  # hours before vote starts
  period: 168  # hours (7 days)
  type: single-choice  # single-choice|approval|weighted|quadratic|ranked-choice|basic
  quorum: 0
  hideAbstain: false
filters:
  minScore: 100  # min token balance to vote
plugins:
  safeSnap:  # auto-execute via Safe (optional)
    address: 0x...
EOF
```

### Recipe 3: Snapshot create-proposal programmatic

```javascript
// node.js
import snapshot from "@snapshot-labs/snapshot.js";
import { Wallet } from "ethers";

const wallet = new Wallet(process.env.SNAPSHOT_PROPOSAL_SIGNER_PK);
const client = new snapshot.Client712("https://hub.snapshot.org");

const receipt = await client.proposal(wallet, wallet.address, {
  space: "brand.eth",
  type: "single-choice",
  title: "Allocate 100k BRAND to community treasury",
  body: `## Background\nWe propose...\n\n## Vote options\n- Yes — execute\n- No — reject`,
  choices: ["Yes", "No"],
  start: Math.floor(Date.now() / 1000),
  end: Math.floor(Date.now() / 1000) + 7 * 86400,
  snapshot: 19012345,  // block number
  plugins: JSON.stringify({}),
  app: "brand-community-manager",
});
console.log("Proposal id:", receipt.id);
```

### Recipe 4: Snapshot vote results to Discord

```python
# Poll Snapshot GraphQL daily; announce milestones + finals
import requests, datetime

q = """
{ proposals(first: 5, where: {space: "brand.eth"}, orderBy: "created", orderDirection: desc) {
    id title state choices scores scores_total end
}}"""
resp = requests.post("https://hub.snapshot.org/graphql", json={"query": q}).json()
for p in resp["data"]["proposals"]:
    if p["state"] == "closed":
        winner_idx = p["scores"].index(max(p["scores"]))
        discord_full.create_message(
            channel_id=GOVERNANCE_CH,
            content=f":ballot_box: **Proposal closed**: {p['title']}\n"
                    f"Result: **{p['choices'][winner_idx]}** ({p['scores'][winner_idx]:.0f} votes, "
                    f"{p['scores'][winner_idx]/p['scores_total']*100:.1f}%)\n"
                    f"<https://snapshot.org/#/brand.eth/proposal/{p['id']}>"
        )
```

### Recipe 5: Mirror publication for token-holder updates

```bash
# Mirror does not have full programmatic publish API
# Use Mirror UI for first publication, then API for read + cross-post

# Read publication
curl https://api.mirror.xyz/v0/publications/brand.mirror.xyz/entries \
  -H "Authorization: Bearer $MIRROR_API_KEY" \
  | jq '.entries[]'

# Token-gating on publication: set in Mirror UI → Publication settings
# → Token-gating → requires holding 0xBrandToken or 0xBrandNFT
```

Cross-post Mirror entry → Discord:

```python
entries = requests.get(
    "https://api.mirror.xyz/v0/publications/brand.mirror.xyz/entries",
    headers={"Authorization": f"Bearer {MIRROR_API_KEY}"}
).json()["entries"][:1]

for e in entries:
    discord_full.create_message(
        channel_id=ANNOUNCEMENTS_CH,
        content=f":scroll: **New on Mirror**: {e['title']}\n{e['url']}\n"
                f"_Token-holders only._"
    )
```

### Recipe 6: Collab.Land Discord token-gating

```
# Install via https://collab.land/invite/discord → pick guild → authorize

# In Discord, run:
/setup-tgr
# Wizard prompts:
# - Token contract address
# - Network: ETH / Polygon / Base / Arbitrum
# - Min balance: 1
# - Role to grant: "Token Holder"

# Multi-contract config (advanced)
/tgr-config add
# - 0xToken1 → "Token1 Holder" role
# - 0xNFT1 → "NFT1 Holder" role (min 1)
# - 0xToken2 ≥ 100 → "Big Holder" role
```

Members run `/login` with Collab.Land bot → Connect wallet → bot verifies + assigns role automatically.

### Recipe 7: Guild.xyz advanced gating

Guild allows logical AND/OR + custom rules:

```bash
curl -X POST https://api.guild.xyz/v2/guilds \
  -H "Authorization: Bearer $GUILD_TOKEN" \
  -d '{
    "name": "BrandDAO Members",
    "urlName": "branddao",
    "platforms": [{"platformName": "DISCORD", "platformGuildId": "GUILD_ID"}],
    "roles": [
      {
        "name": "Genesis Holder",
        "requirements": [
          {"type": "ERC721", "chain": "ETHEREUM", "address": "0xGenesisNFT", "data": {"minAmount": 1}}
        ],
        "rolePlatforms": [{"platform":"DISCORD","platformRoleId":"GENESIS_ROLE_ID"}]
      },
      {
        "name": "OG Voter",
        "requirements": [
          {"type": "SNAPSHOT", "data": {"space":"brand.eth","minVotes":3}},
          {"type": "ERC20", "chain":"ETHEREUM", "address":"0xBRAND", "data":{"minAmount":1000}}
        ],
        "logic": "AND",
        "rolePlatforms": [{"platform":"DISCORD","platformRoleId":"OG_ROLE_ID"}]
      }
    ]
  }'
```

Guild auto-refreshes member status hourly; revokes Discord roles when wallet no longer qualifies.

### Recipe 8: Farcaster cast to community

```bash
# Cast via Neynar API (most common Farcaster client API)
curl -X POST https://api.neynar.com/v2/farcaster/cast \
  -H "api_key: $NEYNAR_API_KEY" \
  -d '{
    "signer_uuid": "'$SIGNER_UUID'",
    "text": "New Snapshot vote live: '$PROPOSAL_TITLE' — '$VOTE_URL'",
    "embeds": [{"url":"'$VOTE_URL'"}]
  }'

# Listen for replies + mentions
curl -H "api_key: $NEYNAR_API_KEY" \
  "https://api.neynar.com/v2/farcaster/feed?fid=$YOUR_FID&filter_type=notifications"
```

### Recipe 9: Lens publication

```javascript
// Lens GraphQL via lens.dev
const mutation = `
mutation CreatePostTypedData($request: CreatePublicPostRequest!) {
  createPostTypedData(request: $request) {
    id
    typedData { types domain value }
  }
}`;
const { createPostTypedData } = await graphql(mutation, {
  request: {
    profileId: "0xPROFILE_ID",
    contentURI: "ipfs://bafy...",  // upload content to IPFS first
    collectModule: { revertCollectModule: true },
    referenceModule: { followerOnlyReferenceModule: false },
  },
});
// Sign typed data with wallet; relay to Lens
```

### Recipe 10: Vote → multi-platform announcement orchestration

```python
# On vote close, fan out:
def announce_vote_close(proposal):
    text = f"Vote closed: **{proposal['title']}** — Winner: {winner(proposal)}"
    url = f"https://snapshot.org/#/brand.eth/proposal/{proposal['id']}"

    # Discord
    discord_full.create_message(channel_id=GOV_CH, content=f"{text}\n{url}")
    # Mirror publication (UI-driven, or queue draft)
    # Farcaster cast
    requests.post(NEYNAR_CAST, json={"text": f"{text} {url}", "signer_uuid": SIGNER_UUID})
    # Slack #governance channel for ops team
    slack_mcp.chat_postMessage(channel="#governance", text=f"{text}\n{url}")
    # Email to off-chain stakeholders
    gmail.send(to="stakeholders@brand.com", subject=f"Vote closed: {proposal['title']}", body=...)
```

## Examples

### Example 1: New DAO launch (Snapshot + Mirror + Collab.Land)

**Goal:** New token launch + DAO with Discord community.

**Steps:**
1. ENS domain registered (Recipe 2 prerequisite).
2. Snapshot space created with ERC20 strategy (Recipe 2).
3. Mirror publication set up + token-gated (Recipe 5).
4. Collab.Land installed in Discord → `/setup-tgr` for `BRAND ≥ 1` → "Token Holder" role (Recipe 6).
5. First governance proposal: "Treasury allocation" (Recipe 3 programmatic OR Snapshot UI).
6. Daily vote-results cron → Discord announcements (Recipe 4).

**Result:** Day 1: 800 wallets connected via Collab.Land. Vote 1: 60% turnout, passed 78% Yes. Mirror publication: 2k subscribers.

### Example 2: NFT project Discord gating

**Goal:** 10k NFT collection wants to gate Discord channels for holders only.

**Steps:**
1. Collab.Land installed.
2. `/setup-tgr` → 0xNFT contract → "Holder" role (Recipe 6).
3. Permission overrides: #holder-chat visible only to "Holder" role.
4. `/setup-tgr` rare-trait gating (Recipe 7 via Guild.xyz for custom traits).
5. Member onboarding: pin "Run /login in #verify to claim role" in #welcome.

**Result:** Verified holder count matches on-chain ownership snapshot ±1% drift (transfers).

### Example 3: Hybrid Web3 + fiat-paid community (Snapshot + Whop)

**Goal:** Some members hold token, others pay $9/mo USD. Both get access.

**Steps:**
1. Collab.Land for token-holders (Recipe 6).
2. Whop for fiat-paid (cross-link: `gated-community-memberstack-outseta-substack` Recipe 5).
3. Both pathways grant same Discord "Member" role.
4. Daily reconciliation: holders + Whop active → expected role count; alert on drift > 2%.

**Result:** Hybrid model serves crypto-native + fiat-native audiences. Cross-tier comms via single Discord.

### Example 4: Decentralized social presence (Farcaster + Lens)

**Goal:** Brand wants persistent Web3 social presence without depending on Twitter.

**Steps:**
1. Farcaster account + signer setup (Recipe 8).
2. Lens profile + handle (Recipe 9).
3. Auto-cross-post: blog post → Farcaster cast + Lens publication via Recipe 10.
4. Engagement monitoring via Neynar / Lens GraphQL for replies + reactions.
5. Sentiment scoring via `sentiment-monitoring-in-community` Recipe 4.

**Result:** 3.2k Farcaster follows, 1.8k Lens follows; meta-analytics across both via custom dashboard.

## Edge cases / gotchas

- **Snapshot block snapshot** — voting power calculated at proposal `snapshot` block. Late-bought tokens don't vote.
- **Snapshot strategy gotchas** — `erc20-balance-of` ignores Uniswap LP / staked / wrapped tokens. Use `multichain` strategy.
- **Quorum vs minScore** — quorum requires X total votes (often unachievable); most DAOs use minScore only.
- **Mirror token-gating bypass** — UI-only; raw entries are publicly indexed via IPFS. Soft gate only.
- **Collab.Land hourly refresh delay** — role revoke takes up to 1 hour after sell.
- **Guild.xyz role-hierarchy** — bot must be above gated roles. Common cause of "Guild isn't assigning role".
- **Lens v3 migration** — Lens migrated v2 → v3 in 2026. Re-verify URLs.
- **Farcaster signer rotation** — signers can be revoked. Periodically verify; rotate as needed.
- **Wallet sign-in UX** — first-timers get confused; pin step-by-step guide in #verify.
- **Multi-chain support** — Polygon/Base/Arbitrum need explicit chain selection in Snapshot + Collab.Land + Guild.
- **Snapshot signing wallet PK** — server-side PK must be cold + access-controlled.
- **Sanctions screening** — OFAC sanctions some wallets. Use Chainalysis/TRM at sign-in.
- **Cross-chain bridged tokens** — snapshot may miss bridged balance. Use multichain strategy.
- **Token volatility** — minScore=100 BRAND varies $10-$1000 across cycles. Recalibrate quarterly.

## Sources

- [Snapshot docs](https://docs.snapshot.org/)
- [Snapshot.js library](https://github.com/snapshot-labs/snapshot.js)
- [Snapshot strategies](https://github.com/snapshot-labs/snapshot-strategies)
- [Mirror dev docs](https://dev.mirror.xyz/)
- [Lens Protocol docs](https://docs.lens.xyz/)
- [Lens API reference](https://docs.lens.xyz/docs/api)
- [Farcaster docs](https://docs.farcaster.xyz/)
- [Neynar API](https://docs.neynar.com/)
- [Collab.Land docs](https://docs.collab.land/)
- [Guild.xyz docs](https://docs.guild.xyz/)
- [Aragon DAO framework](https://aragon.org/)
- [SafeSnap (Snapshot + Gnosis Safe)](https://docs.snapshot.org/plugins/safesnap)
