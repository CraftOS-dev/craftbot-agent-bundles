<!--
Source: https://developer.1password.com/docs/cli/ + https://bitwarden.com/help/cli/
-->
# Password Management — 1Password / Bitwarden — SKILL

Vault CRUD + sharing + breach alerts + SSH agent. 1Password owns the best UX + family/team sharing + Watchtower; Bitwarden is open-source + free tier + self-hostable. Both have first-class CLIs. Agent uses `op` (1Password) / `bw` (Bitwarden) for retrieval + injection + rotation.

## When to use this skill

- **"Where's my password for X?"** — retrieval.
- **"Generate a new password for X"** — creation + storage.
- **"Share password with spouse / team member"** — vault sharing.
- **"Check my passwords for breaches"** — Watchtower / Have I Been Pwned scan.
- **"Rotate passwords"** — periodic security hygiene.

**Do NOT use this skill when:**
- Password reset / account recovery — those are per-service flows (e.g., google.com/account).
- 2FA / TOTP secret generation — handled inside vault but separate UX.
- Saving secrets to env for code — use `1password` skill's `op run` for that.

## Pick the right tool

| Need | Tool | Why |
|---|---|---|
| Family + best UX + Watchtower + Developer | **1Password** | $36/yr family; $36/yr individual; SSH agent |
| Open-source + free tier + self-host | **Bitwarden** | Free; Bitwarden Premium $10/yr; Vaultwarden self-host |
| Built into macOS / iOS | **Apple Keychain** | Free; AirDrop sharing; less robust |
| Legacy enterprise | **LastPass** | Avoid for new users (multiple breaches) |
| Specialized | **Dashlane / NordPass / Keeper / Proton Pass** | Niche |

## Setup

### 1Password CLI (`op`)

```bash
# Install
brew install --cask 1password-cli
# OR npm
npm i -g @1password/op

# Sign in (interactive once, then session token)
op signin

# Or biometric (macOS):
# Settings > Developer > Integrate with 1Password CLI
# Then op signin uses Touch ID
```

Docs: https://developer.1password.com/docs/cli/

### Bitwarden CLI (`bw`)

```bash
# Install
brew install bitwarden-cli
# OR npm
npm i -g @bitwarden/cli

# Login
bw login me@email.com
# Unlock per session
export BW_SESSION="$(bw unlock --raw)"
```

Docs: https://bitwarden.com/help/cli/

### MCP wrappers (already in agent.yaml)

- `1password` skill — wraps `op` CLI
- `onepassword-mcp` — read-only MCP
- `bitwarden-mcp` — Bitwarden CRUD MCP

## Common recipes

### Recipe 1: 1Password — retrieve a password

```bash
# Whole item
op item get "GitHub"

# Just the password
op item get "GitHub" --fields password

# JSON
op item get "GitHub" --format json | jq '.fields[] | select(.label=="password") | .value'
```

### Recipe 2: 1Password — create a new login

```bash
op item create \
  --category=login \
  --title="MyService" \
  --vault="Personal" \
  username="me@email.com" \
  --generate-password='letters,digits,symbols,length=20' \
  url="https://example.com" \
  notes="2FA: TOTP via Authy"
```

### Recipe 3: 1Password — update an item

```bash
op item edit "MyService" \
  password="$(op item create --generate-password=letters,digits,length=24 --dry-run)" \
  notes="Rotated 2026-06-10"
```

### Recipe 4: 1Password — list items in a vault

```bash
op item list --vault "Personal"
op item list --categories login,credit_card,document
```

### Recipe 5: 1Password — share vault with family

```bash
# Family vault is a shared vault
op vault create "Family" --description "Shared family logins"

# Add a family member (must already be in family account)
op user list
op group user list  # see members

# Items added to "Family" vault auto-shared
op item create --category=login --vault="Family" --title="Netflix" ...
```

### Recipe 6: 1Password Watchtower — breach scan

```bash
# CLI checks: weak / reused / breached
op item list --categories login \
  | xargs -I {} op item get {} --format json \
  | jq 'select(.fields[] | .label=="password" | .value | length < 10) | .title'
# Returns weak passwords
```

Or use Watchtower in the 1Password app for the full breach + weak + reuse scan.

### Recipe 7: 1Password — inject secrets to env (op run)

```bash
# .env.template file
DATABASE_URL=op://Personal/MyDB/url
API_KEY=op://Personal/MyService/password

# Run with substitution
op run --env-file=.env.template -- python script.py
```

Never expose secrets in shell history; always use `op run`.

### Recipe 8: Bitwarden — retrieve

```bash
# Unlock once per session
export BW_SESSION="$(bw unlock --raw)"

# Get an item
bw get item "GitHub"

# Just password
bw get password "GitHub"

# Username
bw get username "GitHub"
```

### Recipe 9: Bitwarden — create

```bash
bw get template item | jq '.name="MyService" | .login.username="me@email.com" | .login.password=(now|tostring)' \
  | bw encode | bw create item
```

### Recipe 10: Bitwarden — generate password

```bash
bw generate -uln --length 24
# -u uppercase, -l lowercase, -n numbers, -s symbols
```

### Recipe 11: SSH key via 1Password

```bash
# Store SSH key
op item create --category=ssh_key --title="GitHub SSH" \
  privatekey="$(cat ~/.ssh/id_ed25519)" \
  publickey="$(cat ~/.ssh/id_ed25519.pub)"

# Use 1Password SSH agent (replaces ssh-agent)
# https://developer.1password.com/docs/ssh/
```

### Recipe 12: TOTP secret generation

```bash
# 1Password (stores TOTP, generates current code)
op item get "MyService" --otp

# Bitwarden
bw get totp "MyService"
```

### Recipe 13: Audit weak/reused/breached

```bash
# 1Password — using the Watchtower API via CLI
op vault list --format json | jq '.[] | .name' | while read v; do
  op item list --vault "$v" --categories login --format json | jq '.[]' \
    | while read item; do
        # Check via Have I Been Pwned API (k-anonymity)
        pw=$(echo "$item" | jq -r '.fields[] | select(.label=="password") | .value')
        hash=$(echo -n "$pw" | sha1sum | awk '{print $1}' | tr 'a-z' 'A-Z')
        prefix=${hash:0:5}
        suffix=${hash:5}
        curl -s "https://api.pwnedpasswords.com/range/$prefix" | grep -q "$suffix" && \
          echo "BREACHED: $(echo $item | jq -r .title)"
      done
done
```

### Recipe 14: Backup vault

```bash
# 1Password
op item list --format json > vault_backup_$(date +%F).json
# Encrypted; do not commit to public repos

# Bitwarden
bw export --format json --output ~/backups/bw_$(date +%F).json
```

## Examples

### Example 1: Retrieve password for app

**Goal:** User asks "where's my Netflix password?"

**Steps:**
1. Recipe 1: `op item get "Netflix" --fields password`.
2. Surface to user (don't print to terminal).
3. Suggest using `op item get "Netflix" --share` for share-link.

**Result:** Password in clipboard (via `--reveal | pbcopy` chain) or surfaced securely.

### Example 2: New account setup

**Goal:** Sign up for new SaaS; generate + store password.

**Steps:**
1. Recipe 2: create new login with auto-gen password.
2. Surface password to user for paste-into-signup.
3. After signup: Recipe 3 to update with 2FA notes.

**Result:** Login stored from day 1.

### Example 3: Family vault share

**Goal:** Share Netflix login with spouse.

**Steps:**
1. Recipe 5: ensure "Family" vault exists; spouse is member.
2. Move Netflix item to Family vault:
   ```bash
   op item move "Netflix" --to-vault "Family"
   ```
3. Both can access via own 1Password app.

**Result:** Shared without sending password in plaintext.

### Example 4: Quarterly rotation

**Goal:** Rotate all weak passwords.

**Steps:**
1. Recipe 13: identify breached/weak.
2. For each: Recipe 3 to rotate.
3. Recipe 14: backup vault before + after.
4. Surface diff: rotated 5 logins.

**Result:** Hygiene maintained.

### Example 5: SSH key management

**Goal:** Set up 1Password as SSH agent.

**Steps:**
1. Recipe 11: store SSH key in 1Password.
2. Enable 1Password SSH agent in settings.
3. Update `~/.ssh/config` to use agent socket.
4. Verify `ssh -T git@github.com` works.

**Result:** SSH unlocks via biometric/PIN; no exposed key files.

## Edge cases / gotchas

- **`op signin` session expiry**: Session token expires after 30 min default; re-signin. Use biometric integration for smoother UX.
- **CLI vs GUI**: GUI Watchtower has full breach scan UI; CLI Recipe 13 is manual. Recommend GUI for the actual user-facing audit.
- **Vault organization**: Personal / Family / Work as separate vaults. Don't mix.
- **Imported from LastPass**: Migration tools at https://developer.1password.com/docs/cli/import/ — review post-import.
- **Bitwarden free vs Premium**: Free doesn't include TOTP storage; $10/yr Premium does.
- **Self-host Bitwarden / Vaultwarden**: Vaultwarden is the Rust unofficial implementation; lighter. Use Vaultwarden for personal self-host.
- **Apple Keychain**: Built-in, free, integrated. But limited sharing (only via AirDrop) + no breach scan. Don't recommend for users with families.
- **LastPass breaches**: Multiple major breaches 2022-2023. Recommend migration off LastPass to 1P or BW.
- **Hash check via HIBP**: Use k-anonymity (Recipe 13) — never send full hash.
- **Backup encryption**: Vault export is encrypted; backup file is not. Store on encrypted disk; never in iCloud / Drive plaintext.
- **2FA on password manager itself**: Always-on. Hardware key (YubiKey) recommended.
- **Family invite**: Spouse must accept invite + create master password. Walk through if needed.
- **Compromise drill**: If master password compromised, full rotation needed. Have a recovery plan.
- **Shared between work + personal**: Different vault per category; don't mix.
- **CLI history**: `op item get ... --reveal` puts password in shell history. Use `--otp` or pipe-to-clipboard via `pbcopy`.
- **Travel mode**: 1Password has "Travel Mode" — hides Personal vault when crossing borders. Useful for international travelers.

## Sources

- [1Password CLI docs](https://developer.1password.com/docs/cli/)
- [1Password SSH agent](https://developer.1password.com/docs/ssh/)
- [Bitwarden CLI](https://bitwarden.com/help/cli/)
- [Vaultwarden (self-host)](https://github.com/dani-garcia/vaultwarden)
- [Have I Been Pwned API](https://haveibeenpwned.com/API/v3)
- [1Password pricing](https://1password.com/pricing/)
- [Bitwarden pricing](https://bitwarden.com/pricing/)
