<!--
Sources: https://technologymatch.com/blog/intune-vs-jamf-pro-vs-kandji-the-it-leaders-guide-to-apple-management-in-2026
         https://www.iru.com/compare/kandji-alternatives
         https://www.rippling.com/blog/rippling-mdm-review
Iru = formerly Kandji (rebranded Oct 2025); six-product unified platform.
Jamf = Apple-deep. Intune = mixed fleet + Apple DDM transition. Rippling IT = lifecycle-tied.
-->
# Device Management — Iru (Kandji) / Jamf / Intune / Rippling IT — SKILL

Stand up MDM (Mobile Device Management): enrollment, blueprints (security baselines), OS update enforcement, app deployment, lifecycle hooks (provision-on-hire / wipe-on-offboard), remote wipe, certificate management. Apple-fleet defaults to Iru or Jamf; mixed fleet defaults to Intune; HRIS-tied defaults to Rippling IT.

## When to use

- Provisioning Macs/Windows/iOS/Android.
- Enforcing OS updates / FileVault / Gatekeeper / firewall.
- Pushing apps (1Password, Slack, Zoom, Chrome) on day-1.
- Offboarding remote wipe.
- SOC 2 / ISO 27001 device-controls evidence.
- Trigger phrases: "MDM", "device management", "Kandji", "Iru", "Jamf", "Intune", "Rippling IT", "remote wipe", "blueprint", "FileVault", "BitLocker", "OS update".

## Setup

```bash
export KANDJI_TOKEN="xxx"      # Iru/Kandji bearer; https://<tenant>.api.iru.com
export KANDJI_HOST="<tenant>.api.iru.com"
export JAMF_HOST="<jss>.jamfcloud.com"
export JAMF_USER="apiuser"
export JAMF_PASS="xxx"
export GRAPH_TOKEN="xxx"       # Microsoft Graph for Intune; OAuth client_credentials
export RIPPLING_KEY="xxx"      # Rippling IT
```

## Common recipes

### Recipe 1: Stage / fleet platform selection
```yaml
choose:
  apple_only_under_300_devices:
    primary: Iru (formerly Kandji)
    why: Modern + unified six-product platform; Auto-Apps Library; Library Items
  apple_only_300_plus_devices_deep:
    primary: Jamf Pro
    why: Deepest Apple tooling; Self Service catalog
  mixed_win_mac_ios_android:
    primary: Microsoft Intune
    why: Single console; transitioning to Apple DDM; bundled if M365
  hris_lifecycle_tied:
    primary: Rippling IT
    why: Auto-provision on hire / auto-deprovision on offboard; one platform
  android_dedicated:
    primary: Esper or Scalefusion
    why: Android-first deep tooling
  windows_focused:
    primary: Microsoft Intune or Hexnode
    why: Intune for M365 shops; Hexnode for mixed SMB
```

### Recipe 2: Iru (Kandji) — enroll a device (Auto-enroll via Apple Business Manager)
```bash
# Get authentication token + enrollment profile
curl -s "https://$KANDJI_HOST/api/v1/blueprints" \
  -H "Authorization: Bearer $KANDJI_TOKEN" \
  | jq '.results[] | {id, name, devices_count}'

# Assign new device to blueprint
curl -s -X PATCH "https://$KANDJI_HOST/api/v1/devices/<device_id>" \
  -H "Authorization: Bearer $KANDJI_TOKEN" -H "Content-Type: application/json" \
  -d '{"blueprint_id":"<blueprint_id>"}'
```

### Recipe 3: Iru blueprint — security baseline (Library Items)
```yaml
blueprint:
  name: "Standard Employee Mac — 2026"
  library_items:
    - type: filevault
      enabled: true
      escrow_recovery_key: true
    - type: firewall
      enabled: true
      block_all_incoming: false
      stealth_mode: true
    - type: gatekeeper
      enabled: true
      allowed_sources: "AppStore_and_identified_developers"
    - type: software_update
      auto_install_macos: false   # We push controlled
      auto_install_security_updates: true
      enforce_version: "Sonoma 14.5"
      enforce_after_days: 14
    - type: screen_saver
      idle_time_seconds: 600
      require_password_immediately: true
    - type: ssh
      enabled: false              # ssh off by default
    - type: airdrop
      allowed_for: "contacts_only"
    - type: time_machine
      enabled: false
    - type: app_install
      apps: ["1Password 8", "Slack", "Google Chrome", "Zoom", "Cloudflare WARP"]
```

### Recipe 4: Jamf Pro — extension attribute + smart group
```bash
# Get auth token
TOKEN=$(curl -su "$JAMF_USER:$JAMF_PASS" -X POST "https://$JAMF_HOST/api/v1/auth/token" | jq -r .token)

# Create smart group: "Macs with FileVault disabled"
curl -s -X POST "https://$JAMF_HOST/JSSResource/computergroups/id/0" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/xml" \
  -d '<computer_group>
    <name>FileVault disabled</name>
    <is_smart>true</is_smart>
    <criteria>
      <criterion><name>FileVault 2 Status</name><value>Not Encrypted</value></criterion>
    </criteria>
  </computer_group>'
```

### Recipe 5: Intune — compliance policy (Win + Mac)
```bash
# Microsoft Graph — create compliance policy
curl -s -X POST "https://graph.microsoft.com/v1.0/deviceManagement/deviceCompliancePolicies" \
  -H "Authorization: Bearer $GRAPH_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "@odata.type":"#microsoft.graph.windows10CompliancePolicy",
    "displayName":"Windows — Production baseline",
    "passwordRequired":true,
    "passwordMinimumLength":12,
    "passwordRequiredType":"alphanumeric",
    "passwordExpirationDays":null,
    "passwordPreviousPasswordBlockCount":5,
    "bitLockerEnabled":true,
    "secureBootEnabled":true,
    "antiVirusRequired":true,
    "antiSpywareRequired":true,
    "osMinimumVersion":"10.0.22631"
  }'
```

### Recipe 6: Rippling IT — lifecycle hooks
```bash
# Hook: when employee.hired → ship device pre-configured
curl -s -X POST "https://api.rippling.com/platform/api/devices/automations" \
  -H "Authorization: Bearer $RIPPLING_KEY" -H "Content-Type: application/json" \
  -d '{
    "trigger":"employee.hired",
    "device_spec":{"type":"MacBook Pro 14 M4 Pro","ram_gb":24,"ssd_gb":1000},
    "blueprint":"Standard Employee Mac — 2026",
    "auto_ship_address":"home_on_file",
    "deliver_by_days_before_start":3
  }'

# Hook: when employee.terminated → remote wipe + recover device
curl -s -X POST "https://api.rippling.com/platform/api/devices/automations" \
  -H "Authorization: Bearer $RIPPLING_KEY" -H "Content-Type: application/json" \
  -d '{
    "trigger":"employee.terminated",
    "actions":["lock_immediately","wipe_after_hours:24","ship_return_label"]
  }'
```

### Recipe 7: Remote wipe (Iru/Kandji)
```bash
# Self-service / compliance erase
curl -s -X POST "https://$KANDJI_HOST/api/v1/devices/<device_id>/actions/erase" \
  -H "Authorization: Bearer $KANDJI_TOKEN" -H "Content-Type: application/json" \
  -d '{"PIN":"123456"}'

# Lock (recoverable)
curl -s -X POST "https://$KANDJI_HOST/api/v1/devices/<device_id>/actions/lock" \
  -H "Authorization: Bearer $KANDJI_TOKEN" -H "Content-Type: application/json" \
  -d '{"PIN":"123456","message":"Please return this device to IT."}'
```

### Recipe 8: OS update enforcement (Iru)
```yaml
# Library item: deferred-update enforcement
library_item:
  type: managed_os_updates
  major_os_version_deferral_days: 30
  install_action: "InstallLater"
  enforce_after_install_button_taps: 7
  reboot_window: "off_hours_only"
```

### Recipe 9: App deployment fleet-wide
```bash
# Iru — assign Auto-App to a blueprint
curl -s -X POST "https://$KANDJI_HOST/api/v1/library/auto-apps" \
  -H "Authorization: Bearer $KANDJI_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "name":"1Password 8",
    "auto_install":true,
    "blueprint_ids":["<bp1>","<bp2>"],
    "update_policy":"latest_stable"
  }'
```

### Recipe 10: Inventory + drift report (Python)
```python
# Detect drift: devices not on enforced OS version
import requests, os
r = requests.get(f"https://{os.environ['KANDJI_HOST']}/api/v1/devices?limit=300",
    headers={'Authorization': f"Bearer {os.environ['KANDJI_TOKEN']}"}).json()
drift = []
for d in r['results']:
    if d['os_version'] < "14.5":
        drift.append({'user': d['user']['email'], 'os': d['os_version'], 'last_check_in': d['last_check_in']})
print(drift)
```

### Recipe 11: Self-Service catalog (Iru/Jamf)
```yaml
# Apps available on user's Self Service app (don't auto-install)
self_service_catalog:
  - VS Code
  - JetBrains Toolbox
  - Figma desktop
  - Postman
  - Loom
  - Linear
  - Notion desktop
  - Tailscale
  - Cloudflare WARP
```

## Examples

### Example 1: Stand up MDM for 30-person Apple fleet
**Goal:** Day-1 fleet enrollment + security baseline + 1Password push.
**Steps:**
1. Recipe 1: select Iru (Apple-only, modern).
2. Configure Apple Business Manager → Iru token (one-time).
3. Recipe 3: blueprint = baseline.
4. Recipe 9: assign 1Password / Slack / Chrome / Zoom Auto-Apps.
5. Recipe 8: enforce Sonoma 14.5 within 14 days.
6. Recipe 6: tie to Rippling for lifecycle hooks.
7. Recipe 10: weekly drift report → Slack #it-ops.

**Result:** All Macs enrolled with consistent baseline; ABM auto-enroll on first boot; offboarding wipe in one click.

### Example 2: Quick-wipe an exiting employee's Mac
**Goal:** Remote wipe at 17:00 termination day.
**Steps:**
1. HR fires termination in Rippling.
2. Recipe 6 lifecycle hook fires → Recipe 7 lock + scheduled wipe.
3. Return-shipping label emailed to employee.
4. After device received, MDM verifies clean status before recycling.

**Result:** No data on departing device after 24h.

## Edge cases / gotchas

- **PIN for erase/lock.** Iru/Kandji + Jamf both require a PIN to wipe; if lost, device is bricked. Store PINs in vault (1Password / Bitwarden / Vault).
- **Apple Business Manager (ABM) requirement.** Auto-enroll requires ABM token + device purchase via Apple direct / authorized reseller. BYOD doesn't auto-enroll.
- **Apple DDM transition.** Apple moving from MDM commands to Declarative Device Management; Intune + Iru + Jamf all transitioning through 2026-2027. Recipe shapes may shift; check vendor docs.
- **Kandji → Iru rename (Oct 2025).** API hostname and SDK package names change; back-compat aliases exist until ~2027 but plan migration.
- **OS update enforcement vs user trust.** Force-rebooting during work hours destroys trust + work product. Recipe 8 `off_hours_only` is mandatory.
- **FileVault recovery key escrow.** Always escrow to MDM; otherwise lost key = bricked drive. Recipe 3 sets `escrow_recovery_key: true`.
- **Rippling IT scope.** Tied to Rippling subscription; not a standalone MDM. Don't pick if not on Rippling HRIS.
- **Jamf vs Jamf Now.** Jamf Now = SMB-light, Jamf Pro = enterprise. Recipe 4 is Pro API.
- **Mac App Store apps.** Push via Auto-App, but some require Volume Purchase Program (VPP) tokens via ABM.
- **GDPR + remote wipe.** EU employees: wipe must respect personal data per DPA / Works Council. Recipe 7 `erase` includes user data; for BYOD on iOS use selective wipe of company profile only.
- **Battery-low at wipe time.** Wipe command queues; if device offline > 30 days may never execute. Pair with SSO deprovision + cloud-backup expiry.
- **Defer to `legal-counsel` for binding labor / privacy review of remote-wipe + monitoring policies, especially EU / Works Council jurisdictions.**

## Sources

- Technology Match — Intune vs Jamf vs Iru/Kandji 2026: https://technologymatch.com/blog/intune-vs-jamf-pro-vs-kandji-the-it-leaders-guide-to-apple-management-in-2026
- Iru — Kandji Alternatives (rebrand Oct 2025): https://www.iru.com/compare/kandji-alternatives
- Rippling — MDM Review: https://www.rippling.com/blog/rippling-mdm-review
- Iru / Kandji API: https://api.kandji.io/api/v1/docs (legacy) / https://docs.iru.com/
- Jamf Pro API: https://developer.jamf.com/jamf-pro/reference
- Microsoft Graph — Intune: https://learn.microsoft.com/en-us/graph/api/resources/intune-graph-overview
- Apple Declarative Device Management: https://developer.apple.com/documentation/devicemanagement/declarative_device_management
