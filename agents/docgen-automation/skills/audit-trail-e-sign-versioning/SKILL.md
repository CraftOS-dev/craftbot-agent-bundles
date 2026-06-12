---
name: audit-trail-e-sign-versioning
description: Archive executed contracts with full audit chain — Certificate of Completion (DocuSign / Adobe Sign / PandaDoc), SHA-256 hashing, OpenTimestamps blockchain proof, version history, retention policy. Build evidentiary-grade chains for litigation, audits, and compliance (SOX, 21 CFR Part 11, HIPAA, GDPR). Use when the user says "audit trail", "certificate of completion", "evidence preservation", "OpenTimestamps", "blockchain proof", "envelope archive", "document retention".
---

# Audit trail + e-sign versioning — Certificate + Hash + OpenTimestamps

This skill ships the post-execution evidence preservation pipeline. The e-sign tool produces the envelope + cert; this skill captures, hashes, time-stamps, indexes, and retains it for evidentiary use.

## When to use

User says:

- "Archive this signed envelope"
- "Pull the Certificate of Completion"
- "Hash + timestamp this document"
- "Tamper-evident proof of when this was signed"
- "Document retention policy"
- "OpenTimestamps / blockchain notarization"
- "Build the evidence chain for litigation hold"
- "SOX-grade / 21 CFR Part 11 audit trail"

Companion skills:
- `e-signature-docusign-adobe-sign-pandadoc` — source of envelope + cert.
- `clm-ironclad-contractworks-integration` — push archived envelope into CLM.
- `document-workflow-routing-approval` — preserve approval audit upstream of signing.
- `redaction-automation-pii` — redact before long-term archive if needed.

## Setup

```bash
# Hashing — built-in (Python / Node / sha256sum)
# No install

# OpenTimestamps — blockchain timestamping
pip install opentimestamps-client
# or Node:
npm install opentimestamps

# AWS S3 + Glacier (long-term archival)
pip install boto3
# Required env: AWS credentials + S3 bucket with object lock (WORM)

# Google Drive (alt archive target)
# Default skill: google-drive-mcp
# Required env: GDRIVE_OAUTH_TOKEN

# DocuSign (cert pull)
# See e-signature-docusign-adobe-sign-pandadoc setup

# Notarize.com / Proof.com (formal notary cert)
# Required env: PROOF_API_KEY
```

## Common recipes

### Recipe 1: What to archive (envelope-complete checklist)

For every executed envelope, capture:

| Asset | Source | Format | Retention |
|---|---|---|---|
| Combined signed PDF | DocuSign `/envelopes/{id}/documents/combined` | PDF | 7+ years |
| Certificate of Completion | DocuSign `/documents/certificate` | PDF | 7+ years (match contract retention) |
| Audit Trail JSON | DocuSign `/envelopes/{id}/audit_events` | JSON | 7+ years |
| Original draft PDF (pre-sign) | Filesystem / template engine | PDF | Until executed +1 yr |
| Approval audit (Slack / Linear / etc.) | `document-workflow-routing-approval` log | JSON | 7+ years |
| SHA-256 of combined PDF | `sha256sum` | hex | Forever (index) |
| OpenTimestamps proof | `ots stamp` | .ots | Forever |
| Counterparty identity | DocuSign recipient + IP + auth method | JSON | 7+ years |
| Metadata (deal_id, parties, term, value) | CRM | JSON | 7+ years |

### Recipe 2: Pull DocuSign Certificate of Completion + combined PDF

```python
from docusign_esign import EnvelopesApi
import hashlib, base64

envelopes_api = EnvelopesApi(api_client)

# Combined signed PDF (all docs + cert merged)
combined_bytes = envelopes_api.get_document(
    account_id=ACCT_ID,
    envelope_id=env_id,
    document_id="combined"
)
combined_path = f"archive/{env_id}/combined.pdf"
with open(combined_path, "wb") as f:
    f.write(combined_bytes)

# Just the certificate (audit page) alone
cert_bytes = envelopes_api.get_document(
    account_id=ACCT_ID,
    envelope_id=env_id,
    document_id="certificate"
)
cert_path = f"archive/{env_id}/certificate.pdf"
with open(cert_path, "wb") as f:
    f.write(cert_bytes)
```

### Recipe 3: Pull DocuSign envelope audit events (machine-readable)

```python
audit = envelopes_api.list_audit_events(
    account_id=ACCT_ID,
    envelope_id=env_id
)
with open(f"archive/{env_id}/audit.json", "w") as f:
    json.dump([e.to_dict() for e in audit.audit_events], f, indent=2, default=str)
```

Each event: `name`, `event_fields[]` (user name, IP, timestamp, user agent, etc.).

### Recipe 4: Hash + write fingerprint manifest

```python
def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

manifest = {
    "envelope_id": env_id,
    "completed_at": "2026-06-15T14:32:11Z",
    "files": {
        "combined.pdf": {"sha256": sha256(combined_path), "size": os.path.getsize(combined_path)},
        "certificate.pdf": {"sha256": sha256(cert_path), "size": os.path.getsize(cert_path)},
        "audit.json": {"sha256": sha256(f"archive/{env_id}/audit.json"), "size": os.path.getsize(f"archive/{env_id}/audit.json")}
    },
    "signers": [
        {"name":"Jane Smith", "email":"jane@acme.com", "auth":"email", "signed_at":"2026-06-15T14:31:00Z"}
    ]
}
with open(f"archive/{env_id}/manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)
```

### Recipe 5: OpenTimestamps — blockchain proof of existence

```bash
# Stamp the combined PDF
ots stamp archive/$env_id/combined.pdf
# Produces archive/$env_id/combined.pdf.ots (calendar receipt)

# After ~1-6 hours, OTS aggregator commits to Bitcoin
# Upgrade local file to include blockchain proof
ots upgrade archive/$env_id/combined.pdf.ots

# Verify (anytime, by anyone with the file + ots)
ots verify archive/$env_id/combined.pdf.ots
# Output: "Success! Bitcoin block 875432 attests existence as of <timestamp>"
```

OpenTimestamps is free, no API key, decentralized. Adds tamper-evident timestamp without trusting a single notary.

### Recipe 6: AWS S3 with Object Lock (WORM compliance)

```bash
# Bucket already created with Object Lock enabled (must be enabled at create time)
aws s3api put-object \
  --bucket envelope-archive \
  --key envelopes/$env_id/combined.pdf \
  --body archive/$env_id/combined.pdf \
  --object-lock-mode COMPLIANCE \
  --object-lock-retain-until-date "2033-06-15T00:00:00Z"  # 7-year retention
```

Compliance mode = no one (not even root) can delete before retention; SOX-grade.

### Recipe 7: Upload manifest as YAML on S3 + symlink in CLM

```bash
aws s3 cp archive/$env_id/manifest.json s3://envelope-archive/envelopes/$env_id/
aws s3 cp archive/$env_id/combined.pdf s3://envelope-archive/envelopes/$env_id/
aws s3 cp archive/$env_id/certificate.pdf s3://envelope-archive/envelopes/$env_id/
aws s3 cp archive/$env_id/audit.json s3://envelope-archive/envelopes/$env_id/
aws s3 cp archive/$env_id/combined.pdf.ots s3://envelope-archive/envelopes/$env_id/

# Generate signed URL for CLM linkage (5-year)
aws s3 presign s3://envelope-archive/envelopes/$env_id/combined.pdf --expires-in 157680000
```

### Recipe 8: Append to envelope archive index (markdown / Notion)

```markdown
# Envelope Archive Index — env_abc123

- DocuSign envelope ID: env_abc123
- Document name: MSA — Acme Corp
- Signers: Jane Smith @ jane@acme.com, Bob Rep @ bob@widgetco.com
- Sent: 2026-06-12T09:00:00Z
- Completed: 2026-06-15T14:32:11Z
- Combined PDF SHA-256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- Certificate SHA-256: a1b2c3...
- S3 URI (combined): s3://envelope-archive/envelopes/env_abc123/combined.pdf
- S3 URI (certificate): s3://envelope-archive/envelopes/env_abc123/certificate.pdf
- OpenTimestamps proof: s3://envelope-archive/envelopes/env_abc123/combined.pdf.ots
- Bitcoin block (OTS): 875432
- CLM record: https://ironcladapp.com/records/iwf_xyz...
- Retention until: 2033-06-15
```

### Recipe 9: Adobe Sign — audit report pull

```python
import requests
# Get agreement audit (similar to DocuSign cert)
r = requests.get(
    f"https://api.na2.adobesign.com/api/rest/v6/agreements/{agr_id}/auditTrail",
    headers={"Authorization": f"Bearer {ADOBE_SIGN_TOKEN}"}
)
with open(f"archive/{agr_id}/audit-trail.pdf", "wb") as f:
    f.write(r.content)
```

### Recipe 10: PandaDoc — pull audit log

```bash
curl https://api.pandadoc.com/public/v1/documents/$DOC_ID/audit_log \
  -H "Authorization: API-Key $PANDADOC_API_KEY"
```

Returns chronological list of view / send / sign / countersign events with IP + user agent.

### Recipe 11: Detect tampering on demand

```python
# Given a manifest + the archived file, verify integrity
def verify(envelope_dir):
    manifest = json.load(open(f"{envelope_dir}/manifest.json"))
    failures = []
    for name, meta in manifest["files"].items():
        computed = sha256(f"{envelope_dir}/{name}")
        if computed != meta["sha256"]:
            failures.append(f"{name}: hash mismatch (expected {meta['sha256']}, got {computed})")
    if not failures:
        # Also verify OpenTimestamps
        subprocess.run(["ots", "verify", f"{envelope_dir}/combined.pdf.ots"], check=True)
        return True, "All hashes + OTS verified."
    return False, failures
```

Run weekly via cron; alert on any failure.

### Recipe 12: Retention policy enforcement (auto-delete after window)

```python
# For non-regulated data (where Object Lock not used) — auto-purge after retention window
import datetime
RETENTION_YEARS = 7
cutoff = datetime.datetime.utcnow() - datetime.timedelta(days=RETENTION_YEARS*365)
for envelope_dir in glob.glob("archive/*"):
    manifest = json.load(open(f"{envelope_dir}/manifest.json"))
    if datetime.datetime.fromisoformat(manifest["completed_at"].rstrip("Z")) < cutoff:
        # Confirm with policy authority before purge
        shutil.rmtree(envelope_dir)
```

### Recipe 13: Litigation hold — pause retention

```python
# Mark envelope dir with HOLD.flag → retention enforcement skips
def litigation_hold(env_id, matter_id, attorney):
    with open(f"archive/{env_id}/HOLD.flag", "w") as f:
        json.dump({
            "matter_id": matter_id,
            "attorney": attorney,
            "hold_at": datetime.datetime.utcnow().isoformat()
        }, f)
```

## Examples

### Example 1: SOX-grade revenue contract archive

**Goal:** Public company needs immutable 7-year archive of revenue contracts.
**Steps:**
1. Recipe 2-4 — pull cert + combined + audit + hash.
2. Recipe 5 — OpenTimestamps proof.
3. Recipe 6 — S3 Object Lock COMPLIANCE mode, 7-year retain.
4. Recipe 7 — manifest stored alongside.
5. Recipe 11 — weekly integrity verification cron.

**Result:** Tamper-evident, immutable, audit-ready chain.

### Example 2: SMB contract archive — Google Drive

**Goal:** Non-regulated startup wants organized executed contracts.
**Steps:**
1. Recipe 2 — DocuSign pull on Connect webhook.
2. Recipe 4 — hash + manifest.json.
3. `google-drive-mcp` uploads to `Executed Contracts/2026/Q2/`.
4. Recipe 8 — append to Notion index DB.

**Result:** Searchable archive without infra.

### Example 3: Litigation discovery prep

**Goal:** Opposing counsel demands "all signed MSAs with Acme between 2024-2026".
**Steps:**
1. Query Recipe 8 index by counterparty + date.
2. For each match, verify integrity via Recipe 11.
3. Bundle into a single tar with manifest of hashes.
4. Hand to outside counsel; integrity attestation by Recipe 5 OTS proof.

**Result:** Chain-of-custody-ready document production.

## Edge cases / gotchas

- **DocuSign `combined` vs individual docs.** `combined` includes the cert; if you store both `combined` + `certificate.pdf` separately, you're storing the cert twice. Pick one canonical form.
- **DocuSign audit events vs Certificate of Completion.** Cert is a human-readable PDF; audit events are machine-readable JSON. Store both.
- **Object Lock COMPLIANCE vs GOVERNANCE mode.** COMPLIANCE: no override ever (use for SOX/regulated). GOVERNANCE: root can override (use for non-regulated retention).
- **S3 Object Lock requires bucket creation flag.** Cannot be enabled retroactively — verify before sending to existing bucket.
- **OpenTimestamps upgrade window.** Stamp is instant but Bitcoin commitment takes 1-6 hours. Always run `ots upgrade` after a delay before treating as proof.
- **OpenTimestamps verification needs internet.** Verification queries calendar + Bitcoin headers; offline-only environments need self-hosted calendar.
- **Sandbox cert ≠ legal cert.** Sandbox DocuSign envelopes produce certs that explicitly state "test"; don't archive as production evidence.
- **PII in audit logs.** Audit events include signer IPs + user agents — qualifying PII under GDPR Art. 4; subject to data subject rights.
- **Retention conflict (GDPR vs SOX).** GDPR may require deletion; SOX requires retention. For mixed: keep encrypted + access-controlled; deletion = obfuscation of personal identifiers, not the cert.
- **Adobe Sign agreement IDs are region-bound.** `na1` agreement won't resolve at `eu1` API.
- **PandaDoc audit log granularity.** Less detailed than DocuSign; pair with PandaDoc Forensic Signature option for higher evidence value.
- **Hash algorithm.** SHA-256 is standard; SHA-512 for higher assurance. Never MD5 / SHA-1.
- **Index DB durability.** If index DB is lost, recovery means re-reading every file — keep separate backup.
- **Email proof vs e-sign cert.** Email confirmations ≠ legally robust evidence; always pair with cert.
- **WORM does not mean unbreakable.** Cosmic rays, S3 multi-AZ failures rare but possible — keep cross-region replication on critical archives.
- **Time-stamping authority alternatives.** OpenTimestamps is free; for stronger non-repudiation, use a qualified Time-Stamping Authority (eIDAS Art. 42) like Sectigo / GlobalSign.

## Sources

- [DocuSign Audit + Certificate of Completion](https://support.docusign.com/s/document-item?bundleId=ulp1643236876813&topicId=zwq1578456355001.html) — official cert.
- [DocuSign Envelopes API — get_document](https://developers.docusign.com/docs/esign-rest-api/reference/envelopes/envelopedocuments/get/) — pull combined + cert.
- [DocuSign Audit Events](https://developers.docusign.com/docs/esign-rest-api/reference/envelopes/envelopeauditevents/) — machine-readable audit.
- [Adobe Sign Audit Trail](https://developer.adobe.com/document-services/apis/sign-api/) — agreement audit pull.
- [PandaDoc Audit Log](https://developers.pandadoc.com/reference/get-document-audit-log) — chronological events.
- [OpenTimestamps](https://opentimestamps.org/) — free Bitcoin timestamping.
- [AWS S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-overview.html) — WORM retention.
- [Sectigo Qualified Time-Stamping](https://sectigo.com/resource-library/what-is-a-qualified-timestamp) — eIDAS qualified TSA.
- [21 CFR Part 11](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/part-11-electronic-records-electronic-signatures-scope-and-application) — FDA audit trail requirements.
- [eIDAS Time-Stamping](https://eur-lex.europa.eu/eli/reg/2014/910/oj) — Art. 42 qualified time stamps.
- Sister skills: `e-signature-docusign-adobe-sign-pandadoc`, `clm-ironclad-contractworks-integration`, `document-workflow-routing-approval`, `redaction-automation-pii`.
