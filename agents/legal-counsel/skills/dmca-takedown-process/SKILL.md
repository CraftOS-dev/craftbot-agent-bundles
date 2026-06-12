---
name: dmca-takedown-process
description: Draft DMCA §512(c) takedown notices and §512(g) counter-notices. Register DMCA Designated Agent at copyright.gov ($6 fee, biennial renewal). Service-provider safe-harbor compliance. Output is the complete notice or counter-notice + memo with the consult-an-attorney disclaimer (penalty-of-perjury statements are binding).
---

# DMCA Takedown Process

## When to use

User says:

- "Draft a DMCA takedown notice"
- "Someone is using our content / image / video — how do I get it removed?"
- "We received a DMCA notice — how do I respond?"
- "Counter-notice"
- "Register our DMCA Designated Agent"
- "Service-provider safe harbor"
- "§512(c) / §512(g)"

Companion skills:
- `contract-review-msa-nda-employment` — for licensing + ToS work.
- `terms-of-service-tos-drafting` — ToS includes DMCA agent reference.

## Setup

```bash
# US Copyright Office — DMCA Designated Agent Directory
# https://www.copyright.gov/dmca-directory/
# Register / search agent: https://dmca.copyright.gov/

# 17 USC §512 (DMCA full text)
# https://www.law.cornell.edu/uscode/text/17/512

# Copyright registration (for stronger DMCA position)
# https://www.copyright.gov/registration/
# eCO portal: https://eco.copyright.gov/

# Sample notices
# https://www.eff.org/issues/dmca

# Python helpers
pip install python-docx jinja2

# Optional: Lumen Database (track DMCA notices publicly)
# https://lumendatabase.org/
```

## Common recipes

### Recipe 1: §512(c) Notification — required elements
```text
17 USC §512(c)(3)(A) — required elements (or notice is "deficient"):

1. Physical or electronic signature of person authorized to act on behalf of owner of EXCLUSIVE RIGHT being infringed.

2. Identification of the copyrighted work claimed to have been infringed (or list of works at site).

3. Identification of the material that is claimed to be infringing OR to be the subject of infringing activity, AND information reasonably sufficient to permit the service provider to locate the material (specific URLs).

4. Information reasonably sufficient to permit service provider to contact the complaining party (address, phone, email).

5. A statement that the complaining party has a GOOD FAITH BELIEF that use is not authorized by copyright owner, agent, or law.

6. A statement that the information in the notification is ACCURATE, AND UNDER PENALTY OF PERJURY, that the complaining party is authorized to act on behalf of the owner of an exclusive right that is allegedly infringed.

Deficient notice = no obligation by service provider; substantially compliant = required removal.
```

### Recipe 2: §512(c) notice template
```markdown
# DMCA Takedown Notice (17 USC §512(c))

**To:** [Service Provider's Designated Agent, address from https://dmca.copyright.gov/]
**From:** [Your name + entity + address + phone + email]
**Date:** 2026-06-09

I am writing to notify you of intellectual property infringement on your platform pursuant to 17 USC §512(c).

## 1. Copyright owner / agent
- Owner of the exclusive right: <Your Company / Individual Name>
- I am [the owner / an agent authorized to act on behalf of the owner]
- Contact info: <address, phone, email>

## 2. Copyrighted work infringed
- Title: <e.g., "Original Photograph of XYZ">
- Type: [photograph / illustration / video / written work / software code]
- First published: <date>
- US Copyright Registration #: <if registered; not required but strengthens case>
- URL where original is hosted: <your URL>

## 3. Infringing material location
- URL(s) where infringing content is located: <list all URLs>
- Description: <brief description of what's infringing>

## 4. Good-faith belief statement
I have a good-faith belief that the use of the material identified above is not authorized by me, my agent, or the law.

## 5. Accuracy + penalty of perjury statement
The information in this notification is accurate, AND UNDER PENALTY OF PERJURY, I AM AUTHORIZED TO ACT ON BEHALF OF THE OWNER of an exclusive right that is allegedly infringed.

## 6. Signature
<Electronic or physical signature>
<Printed name>
<Title (if agent)>

---
**Disclaimer:** This is informational guidance from an AI agent. The penalty-of-perjury statement carries legal liability. Always consult a licensed attorney before signing or filing a DMCA notice.
```

### Recipe 3: §512(g) Counter-Notification — required elements
```text
17 USC §512(g)(3) — required elements:

1. Physical or electronic signature of subscriber.

2. Identification of the material that has been removed or to which access has been disabled AND the location at which the material appeared before it was removed or access was disabled.

3. A statement UNDER PENALTY OF PERJURY that the subscriber has a GOOD FAITH BELIEF that the material was removed or disabled as a result of mistake or misidentification.

4. Subscriber's name, address, and telephone number.

5. A statement that the subscriber CONSENTS TO THE JURISDICTION of the federal district court in the judicial district where the subscriber's address is located, OR (if outside the US) for any judicial district in which the service provider may be found, AND THAT THE SUBSCRIBER WILL ACCEPT SERVICE of process from the complaining party (or its agent).

Service provider then:
- Forwards counter-notice to original notifier
- Replaces content in 10-14 business days unless original notifier files lawsuit + provides notice to service provider
```

### Recipe 4: §512(g) counter-notice template
```markdown
# DMCA Counter-Notification (17 USC §512(g))

**To:** [Service Provider's Designated Agent]
**From:** [Your name + address + phone + email]
**Date:** 2026-06-09

I am writing to submit a counter-notification regarding content removed from your platform pursuant to a DMCA takedown notice. Please reinstate the material identified below.

## 1. Subscriber identification
- Name: <Your name>
- Address: <full address>
- Phone: <phone>
- Email: <email>

## 2. Material removed + prior location
- Description: <what was removed>
- URL or location before removal: <prior URL>
- Notice reference (if available): <takedown notice ID / date>

## 3. Good-faith belief statement (UNDER PENALTY OF PERJURY)
UNDER PENALTY OF PERJURY, I have a good-faith belief that the material was removed or disabled as a result of mistake or misidentification.

[Optional: brief explanation of basis — fair use, license, etc. NOT required by statute but supports the assertion]

## 4. Jurisdictional consent
I consent to the jurisdiction of the federal district court for the [your federal district] (OR for any judicial district in which the service provider may be found, if I reside outside the United States), and I will accept service of process from the person who provided notification under §512(c)(1)(C) or that person's agent.

## 5. Signature
<Electronic or physical signature>
<Printed name>

---
**Disclaimer:** This is informational guidance from an AI agent. The penalty-of-perjury statement + consent to jurisdiction carry legal liability. Always consult a licensed attorney before filing a counter-notification. Filing a false counter-notice may expose you to liability under 17 USC §512(f).
```

### Recipe 5: Register DMCA Designated Agent
```text
To qualify for safe harbor under §512(c), a service provider MUST:
1. Designate an agent to receive notices
2. Register with US Copyright Office
3. Display agent info publicly (typically in ToS + at /dmca-agent endpoint)

Registration:
- Portal: https://dmca.copyright.gov/
- Fee: $6 (as of 2026)
- Renewal: every 3 years (or update on change)
- Information required:
  - Service provider legal name + alternate names
  - Physical address
  - Telephone
  - Email
  - Designated agent name + title
  - Service provider URL
  - Date of designation

Failure to register = no safe harbor. ISP-level providers usually register; small SaaS often miss this.
```

### Recipe 6: DMCA agent disclosure on website
```html
<!-- ToS section + standalone /dmca-agent page -->

<h2>DMCA Designated Agent</h2>
<p>Pursuant to 17 USC §512, [Company] has designated the following agent to receive notifications of claimed copyright infringement:</p>
<ul>
  <li><strong>Designated Agent:</strong> [Name + Title]</li>
  <li><strong>Address:</strong> [Full mailing address]</li>
  <li><strong>Phone:</strong> [Phone]</li>
  <li><strong>Email:</strong> [Agent email; e.g., dmca@yourdomain.com]</li>
</ul>
<p>Confidence with US Copyright Office Directory: <a href="https://dmca.copyright.gov/">https://dmca.copyright.gov/</a></p>

<p>To submit a takedown notice, please include all elements required by 17 USC §512(c)(3)(A). Filing a false notice may subject you to liability under 17 USC §512(f).</p>
```

### Recipe 7: Service provider workflow — receiving a §512(c) notice
```text
1. Receive notice via Designated Agent email / mail.
2. Validate notice elements (Recipe 1):
   - All 6 elements present? → SUBSTANTIALLY COMPLIANT → remove content; preserve safe harbor.
   - Missing material elements? → DEFICIENT → request cure; safe harbor preserved during reasonable cure period.
3. Take down content "expeditiously" (statute says "expeditiously"; courts have approved 24-72 hours).
4. Notify subscriber of takedown + reason.
5. Wait for counter-notice or pass period.
6. If counter-notice received:
   - Forward to original notifier.
   - Replace content in 10-14 business days unless original notifier files lawsuit + notifies service provider.
7. Track repeat infringers (§512(i)(1)(A)) — implement + reasonably enforce repeat-infringer policy.
8. Log notice for safe-harbor records.
```

### Recipe 8: §512(f) — penalty for knowing material misrepresentation
```text
Knowing material misrepresentation in a §512(c) notice OR §512(g) counter-notice:
- Liable to alleged infringer / service provider for damages + costs + attorney fees.

Lenz v. Universal Music Corp, 815 F.3d 1145 (9th Cir. 2015):
- Copyright owner MUST consider fair use BEFORE sending takedown.
- "Subjective good faith" requires actual consideration of fair use.

Practical: don't fire off takedowns without considering fair use, parody, license, public domain.
```

### Recipe 9: Common fair-use considerations BEFORE filing
```text
Fair use factors (17 USC §107):
1. Purpose + character (commercial vs nonprofit; transformative?)
2. Nature of copyrighted work
3. Amount + substantiality of portion used
4. Effect on market for original

Typical fair-use scenarios that DO NOT warrant takedown:
- Commentary / criticism / reviews
- Parody (Campbell v. Acuff-Rose, 510 U.S. 569 (1994))
- News reporting (limited)
- Teaching / scholarship
- Research

Filing notice anyway = §512(f) risk.
```

### Recipe 10: Repeat infringer policy (required for safe harbor)
```text
17 USC §512(i)(1)(A) requires service provider to:
- Adopt + reasonably implement a policy that provides for termination "in appropriate circumstances" of accounts of REPEAT INFRINGERS.

What's "appropriate"?
- BMG v. Cox Communications, 881 F.3d 293 (4th Cir. 2018) — generally fact-specific.

Sample policy:
"We may terminate accounts of users who repeatedly infringe copyright. After [N] valid DMCA notices targeting a user, we may suspend or terminate the account."
```

### Recipe 11: International takedowns (non-DMCA)
```text
DMCA applies to US service providers. For international:
- UK: Copyright, Designs and Patents Act 1988 §97A injunctions
- EU: Digital Services Act notice-and-action mechanism + Article 14(2) e-Commerce Directive (until DSA takes full effect 2024)
- Hosting takedowns under EU DSA — similar elements to DMCA

For non-US infringement, draft a DSA-style notice or seek hosting provider's notice-and-action mechanism.
```

### Recipe 12: DMCA copyright registration timing
```text
For US courts:
- Registration NOT required to send §512(c) notice
- Registration REQUIRED to file copyright infringement lawsuit (17 USC §411)
- Pre-registration valuable for stronger damages claims:
  - Statutory damages ($750-$150,000/work) + attorney fees available only if registered before infringement OR within 3 months of first publication

For DMCA strategic value, encourage registration of important works.
```

## Examples

### Example 1: Photographer sees unauthorized use on a competitor's website
**Goal:** Get the image taken down.
**Steps:**
1. Verify the use is infringing (no fair use, no license).
2. Identify service provider hosting the site (DNS / WHOIS).
3. Find designated agent via https://dmca.copyright.gov/ search.
4. Recipe 2 draft §512(c) notice.
5. Optional: register the photograph at copyright.gov for stronger position.
6. Send notice via email + certified mail.
7. Track for compliance (typical 24-72 hours).
8. If host complies → infringer may file counter-notice → respond per Recipe 11.

**Result:** Content removed; option to file suit if counter-notice + repeat use.

### Example 2: Solo developer's open-source code copied without license preservation
**Goal:** Force GitHub takedown of fork that stripped MIT license.
**Steps:**
1. Verify MIT license requirements are violated (no attribution).
2. GitHub designated agent: https://docs.github.com/en/site-policy/content-removal-policies/dmca-takedown-policy
3. File via GitHub's DMCA form: https://github.com/contact/dmca
4. Wait for takedown (GitHub publishes most takedowns on https://github.com/github/dmca).
5. If counter-notice → reconsider, possibly engage counsel.

**Result:** Fork removed or relicensed.

### Example 3: SaaS startup receives DMCA notice on user content
**Goal:** Comply with §512(c) safe harbor.
**Steps:**
1. Recipe 7 workflow.
2. Verify notice substantially compliant (Recipe 1).
3. Take down expeditiously.
4. Notify user of takedown.
5. Forward any counter-notice to original notifier.
6. Update repeat-infringer log.
7. Maintain Designated Agent registration current (Recipe 5).

**Result:** Safe harbor preserved.

## Edge cases / gotchas

- **Fair use must be considered BEFORE sending notice** (Lenz v. Universal). Sending notice on parody / criticism / commentary = §512(f) liability risk.
- **Penalty of perjury is real.** §512(c) statement is sworn under penalty of perjury. Knowing falsity = federal crime + civil liability.
- **Designated Agent registration must be CURRENT.** Lapsed registration = no safe harbor. Renew every 3 years.
- **Counter-notice = subscriber consents to federal court jurisdiction.** This is a material commitment. Original notifier can file suit in subscriber's district.
- **Service provider must "expeditiously" take down.** Courts have approved 24-72 hours. 7+ days starts to lose safe harbor.
- **Repeat infringer policy must be reasonably implemented.** Tracking + termination required. BMG v. Cox cost Cox $25M for inadequate implementation.
- **§512(c) only applies to user-submitted content.** Your own first-party content posted on your site is NOT under §512(c) — you're the publisher, not the service provider.
- **Hosting vs CDN vs platform.** Different service provider types — §512(a) conduit / §512(b) caching / §512(c) hosting / §512(d) information location tool. Each has different safe-harbor requirements.
- **YouTube Content ID / similar systems** are NOT DMCA per se. They're a private automated system; users can dispute via separate process.
- **DMCA agent + ToS link.** Service-provider ToS should reference Designated Agent + describe DMCA process. Public-facing /dmca-agent endpoint best practice.
- **Pre-registration value.** Registering BEFORE infringement gives statutory damages + attorney fees. Critical for high-value content (music, software, photos).
- **Lumen Database disclosure.** Many service providers publish received DMCA notices to Lumen. Your notice may become public. Consider if confidentiality matters.
- **Section 512(j) injunctive relief.** Even with safe harbor, court can order specific actions. Don't assume safe harbor = complete immunity.
- **Repeat 512(f) misrepresentation suits** are increasingly successful (Online Policy Group v. Diebold, 337 F. Supp. 2d 1195 (N.D. Cal. 2004); Lenz). Don't abuse the notice process.
- **YouTube counter-notice = full lawsuit risk.** Many users don't realize counter-notice consents to jurisdiction. Consult attorney before filing.
- **EU DSA shift.** EU sites need DSA-compliant notice-and-action mechanism + statement of reasons; not 1:1 DMCA.

> Warning: **This is informational guidance from an AI agent. The penalty-of-perjury statements in DMCA notices and counter-notices carry legal liability under 17 USC §512(f). Always consult a licensed attorney before signing, filing, or executing a DMCA notice, counter-notice, or related binding legal document.**

## Sources

- [17 USC §512 — Cornell LII](https://www.law.cornell.edu/uscode/text/17/512) — full text.
- [US Copyright Office DMCA Designated Agent](https://www.copyright.gov/dmca-directory/) — registration portal.
- [US Copyright Office](https://www.copyright.gov/) — registration + DMCA.
- [eCO Copyright Registration](https://eco.copyright.gov/) — online filing.
- [EFF — DMCA Resources](https://www.eff.org/issues/dmca) — sample notices + commentary.
- [Lumen Database](https://lumendatabase.org/) — published DMCA notices.
- [GitHub DMCA Process](https://docs.github.com/en/site-policy/content-removal-policies/dmca-takedown-policy) — example service-provider workflow.
- [GitHub DMCA Notices Repository](https://github.com/github/dmca) — public DMCA history.
- [Lenz v. Universal Music Corp, 815 F.3d 1145 (9th Cir. 2015)](https://www.eff.org/cases/lenz-v-universal) — fair use consideration requirement.
- [BMG v. Cox Communications, 881 F.3d 293 (4th Cir. 2018)](https://casetext.com/case/bmg-rights-mgmt-llc-v-cox-commcns-inc) — repeat infringer policy.
- [Online Policy Group v. Diebold, 337 F. Supp. 2d 1195 (N.D. Cal. 2004)](https://www.eff.org/cases/online-policy-group-v-diebold) — §512(f) misrepresentation.
- [EU Digital Services Act](https://commission.europa.eu/strategy-and-policy/priorities-2019-2024/europe-fit-digital-age/digital-services-act_en) — EU notice-and-action.
- Sister skills: `contract-review-msa-nda-employment`, `terms-of-service-tos-drafting`.
