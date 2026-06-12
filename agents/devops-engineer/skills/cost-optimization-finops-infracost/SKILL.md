<!--
Source: https://www.infracost.io/docs/ · https://www.opencost.io/ · https://karpenter.sh/ · https://goldilocks.fairwinds.com/ · https://www.finops.org/framework/
Authored: June 2026 for the devops-engineer agent bundle.
-->

# Cost Optimization (Infracost + OpenCost + Karpenter + Goldilocks + FinOps)

PR-time cost diff with **Infracost** (Terraform/OpenTofu/Pulumi), cluster
workload cost with **OpenCost** (CNCF, formerly Kubecost OSS), K8s
autoscaling + spot via **Karpenter** (AWS), right-sizing via **Goldilocks**
(Fairwinds), and FinOps Foundation framework + FOCUS spec for normalized
multi-cloud billing.

## When to use

- "How much will this PR cost?" → Infracost in PR.
- Monthly cloud bill grew 30% — find the culprit.
- K8s cluster over-provisioned — right-size requests/limits.
- Worker nodes idle — switch to Karpenter spot.
- Negotiating with finance — produce cost-by-team report.

Skip when: serverless-only stack (PaaS bills are obvious); pre-revenue (cut
features first, then cost-optimize).

## Setup

```bash
# Infracost
brew install infracost
infracost auth login           # free; needs account at infracost.io
infracost configure set api_key $INFRACOST_API_KEY

# OpenCost (in-cluster)
helm repo add opencost https://opencost.github.io/opencost-helm-chart
helm upgrade --install opencost opencost/opencost -n opencost --create-namespace

# Karpenter (AWS EKS)
helm upgrade --install karpenter oci://public.ecr.aws/karpenter/karpenter \
  -n karpenter --create-namespace --version 1.0.x \
  --set settings.clusterName=prod --set serviceAccount.annotations."eks\.amazonaws\.com/role-arn"=$KARPENTER_ROLE

# Goldilocks
helm repo add fairwinds-stable https://charts.fairwinds.com/stable
helm upgrade --install goldilocks fairwinds-stable/goldilocks -n goldilocks --create-namespace

# Cast.ai (commercial alt to Karpenter — multi-cloud)
# Vantage / Cloudability / Apptio — multi-cloud cost SaaS (paid)
```

## Common recipes

### Recipe 1 — Infracost CLI diff

```bash
# Baseline
git checkout main
infracost breakdown --path . --format json --out-file infracost-base.json

# Diff PR
git checkout my-branch
infracost diff --path . --compare-to infracost-base.json --format table

# GitHub-comment format
infracost diff --path . --compare-to infracost-base.json --format github-comment --out-file pr.md
gh pr comment --body-file pr.md
```

### Recipe 2 — Infracost GitHub Action

```yaml
name: infracost
on: { pull_request: { paths: ['terraform/**', '**.tf'] } }

permissions: { pull-requests: write }

jobs:
  cost:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v5
        with: { ref: ${{ github.event.pull_request.base.ref }} }
      - uses: infracost/actions/setup@v3
        with: { api-key: ${{ secrets.INFRACOST_API_KEY }} }
      - run: infracost breakdown --path=terraform/ --format=json --out-file=/tmp/base.json
      - uses: actions/checkout@v5
      - run: infracost diff --path=terraform/ --compare-to=/tmp/base.json --format=json --out-file=/tmp/diff.json
      - uses: infracost/actions/comment@v3
        with:
          path: /tmp/diff.json
          behavior: update           # update existing comment vs new
```

### Recipe 3 — Infracost policies

```hcl
# infracost.yml — set a cost-delta policy
version: 0.1
projects:
  - path: terraform/
    name: prod-infra

# infracost-policy.rego — OPA policy
package infracost
deny[msg] {
  input.totalMonthlyCost > 5000
  msg := sprintf("Total monthly cost is $%.2f, exceeds $5000 budget", [input.totalMonthlyCost])
}
```

```bash
infracost breakdown --path=terraform/ --format=json --out-file=cost.json
infracost output --path=cost.json --format=table
conftest test cost.json --policy infracost-policy.rego
```

### Recipe 4 — OpenCost queries

```bash
kubectl port-forward -n opencost svc/opencost 9003:9003 &

# Per-namespace cost in last 7d
curl 'http://localhost:9003/allocation?window=7d&aggregate=namespace' | jq .

# Per-deployment, last 24h
curl 'http://localhost:9003/allocation?window=24h&aggregate=controller&filter=controllerKind%3A%22deployment%22'

# Cost rate by pod label
curl 'http://localhost:9003/allocation?window=1d&aggregate=label%3Aapp.kubernetes.io%2Fname'
```

OpenCost UI at https://opencost.io has dashboards.

### Recipe 5 — Karpenter NodePool (AWS spot + rightsize)

```yaml
apiVersion: karpenter.sh/v1
kind: NodePool
metadata: { name: default }
spec:
  template:
    spec:
      requirements:
        - { key: kubernetes.io/arch, operator: In, values: [amd64, arm64] }
        - { key: kubernetes.io/os, operator: In, values: [linux] }
        - { key: karpenter.sh/capacity-type, operator: In, values: [spot, on-demand] }
        - { key: karpenter.k8s.aws/instance-category, operator: In, values: [c, m, r] }
        - { key: karpenter.k8s.aws/instance-cpu, operator: In, values: ["4","8","16","32"] }
        - { key: karpenter.k8s.aws/instance-generation, operator: Gt, values: ["5"] }
      nodeClassRef:
        name: default
        kind: EC2NodeClass
        group: karpenter.k8s.aws
  limits:
    cpu: 1000
    memory: 1000Gi
  disruption:
    consolidationPolicy: WhenEmptyOrUnderutilized
    consolidateAfter: 30s
---
apiVersion: karpenter.k8s.aws/v1
kind: EC2NodeClass
metadata: { name: default }
spec:
  amiSelectorTerms: [{ alias: "bottlerocket@latest" }]
  subnetSelectorTerms: [{ tags: { karpenter.sh/discovery: prod } }]
  securityGroupSelectorTerms: [{ tags: { karpenter.sh/discovery: prod } }]
  role: KarpenterNodeRole
```

Karpenter:
- Provisions spot when possible (60-90% cheaper than on-demand).
- Consolidates underutilized nodes (deletes empty / packs sparse).
- Pet-vs-cattle scheduling — picks fitting instance type per Pod.

### Recipe 6 — Goldilocks (right-size requests/limits)

```bash
# Goldilocks installs Vertical Pod Autoscaler (recommendation-only mode)
kubectl label namespace prod goldilocks.fairwinds.com/enabled=true

# Wait 24-48h for recommendations
kubectl port-forward -n goldilocks svc/goldilocks-dashboard 8080:80
open http://localhost:8080
```

Goldilocks shows current vs recommended requests + limits per container.
"Burstable QoS" = drop limits; "Guaranteed" = requests = limits.

### Recipe 7 — VPA in recommendation mode

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata: { name: api, namespace: prod }
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  updatePolicy:
    updateMode: "Off"             # recommendation only; don't actually resize
  resourcePolicy:
    containerPolicies:
      - containerName: api
        minAllowed: { cpu: 50m, memory: 128Mi }
        maxAllowed: { cpu: 2, memory: 4Gi }
```

```bash
kubectl describe vpa api -n prod
# Shows: Target, Lower Bound, Upper Bound, Uncapped Target
```

### Recipe 8 — Cluster autoscaler vs Karpenter

| Tool | When | Notes |
|---|---|---|
| Cluster Autoscaler (CA) | Multi-cloud or non-AWS | Fixed ASG node groups |
| Karpenter | AWS EKS | Flexible instance picking; spot; consolidation |
| GKE Autopilot | GCP | Managed; no node mgmt |
| Cast.ai | Multi-cloud | Commercial; works on AKS+EKS+GKE |

### Recipe 9 — Spot interruption handling

```yaml
# Karpenter consumes AWS EventBridge for spot termination notice
# Aws-node-termination-handler (NTH) drains node within the 2-min notice
helm upgrade --install aws-nth eks/aws-node-termination-handler \
  -n kube-system \
  --set enableSqsTerminationDraining=true \
  --set queueURL=$NTH_QUEUE
```

App-level: graceful shutdown on SIGTERM; PDB; multiple replicas.

### Recipe 10 — FOCUS-formatted billing exports

```bash
# AWS CUR (Cost & Usage Report) → S3
aws cur put-report-definition \
  --report-definition '{
    "ReportName":"prod-focus",
    "TimeUnit":"DAILY",
    "Format":"Parquet",
    "Compression":"Parquet",
    "AdditionalSchemaElements":["RESOURCES"],
    "S3Bucket":"myorg-cur",
    "S3Prefix":"focus/",
    "S3Region":"us-east-1"
  }'

# Query with Athena
SELECT "BillingPeriod", "ServiceName", SUM("BilledCost") AS cost
FROM "focus_cur"
WHERE "BillingPeriod" = '2026-05'
GROUP BY 1, 2 ORDER BY 3 DESC;
```

FOCUS spec normalizes cloud bills — same schema across AWS/GCP/Azure.

### Recipe 11 — Reserved Instances / Savings Plans / CUDs

```bash
# AWS — Compute Savings Plans (most flexible)
aws ce get-savings-plans-purchase-recommendation \
  --savings-plans-type COMPUTE_SP \
  --term-in-years ONE_YEAR \
  --payment-option ALL_UPFRONT

# GCP — Committed Use Discounts
gcloud compute commitments create my-cud --plan TWELVE_MONTH --resources vcpu=100,memory=400 --region us-central1

# Azure — Reserved Instances
az reservations reservation-order purchase \
  --reservation-order-id $ORDER_ID \
  --sku Standard_D2s_v3 --term P1Y --quantity 10
```

Target: 60-70% of baseline coverage with commitments; remainder on
spot/on-demand. Avoid 100% commitment (no flexibility for downscale).

### Recipe 12 — Cost reports

```bash
# Per-team chargeback (OpenCost CSV)
curl 'http://localhost:9003/allocation?window=30d&aggregate=label%3Ateam&format=csv' > team-cost.csv

# Top-10 most expensive services
curl 'http://localhost:9003/allocation?window=30d&aggregate=controller' | \
  jq -r '[.data[0] | to_entries | .[] | [.key, .value.totalCost] | @csv]' | sort -t, -k2 -nr | head -10
```

## Examples

### Example 1 — Cut $30k/mo EKS bill by 40%

**Goal:** Right-size + spot via Karpenter + delete unused.

1. Install OpenCost (Recipe 4); identify top spenders.
2. Install Goldilocks (Recipe 6); discover 80% of pods over-request memory by 2-3×.
3. PR right-sized requests/limits across services.
4. Install Karpenter (Recipe 5); deprecate ASG node groups.
5. Tag NodePool to allow spot for stateless workloads.
6. After 30 days: bill drops from $30k → $18k.

**Result:** 40% savings, fewer nodes (consolidation), better packing.

### Example 2 — Block expensive Terraform PRs

**Goal:** PRs adding > $500/mo require approval.

1. Add Infracost Action (Recipe 2) to CI.
2. Use OPA/conftest policy (Recipe 3) requiring `<$500` delta for auto-merge.
3. Above threshold → CI fails; requires `/cost-approved` label from FinOps.
4. Block merge via Branch Protection on the `infracost-policy` check.

**Result:** No silent infra-spend creep.

## Edge cases / gotchas

- **Infracost free tier**: full Terraform breakdown is free; advanced
  features (private cloud, custom pricing) need paid plan.
- **OpenCost vs Kubecost**: OpenCost is the CNCF OSS engine; Kubecost is
  the commercial product built on top. OpenCost gives you allocation;
  Kubecost adds savings recommendations + multi-cluster UI.
- **Spot interruption rate** varies by instance type / region — m5.large
  in us-east-1 ~3%/mo; rare ones (r5d.24xlarge) >30%. Diversify NodePools.
- **Karpenter cold start**: provisioning a new node takes ~30-90s. For
  burst traffic, pre-warm with min replicas on a dedicated NodePool.
- **VPA + HPA conflict**: don't use VPA on a workload that's HPA-managed
  on CPU (they fight). HPA on RPS / custom metric is OK with VPA.
- **Reserved Instance lock-in**: pre-paying $$ for 1y/3y limits flexibility.
  Use Savings Plans (more flexible) over RIs where available.
- **Tag enforcement** for cost allocation: untagged resources go to
  "unallocated" bucket. Use Kyverno to require `cost-center` label on every
  resource.
- **Multi-cloud cost dashboards**: Vantage, CloudHealth, Apptio Cloudability
  unify AWS+GCP+Azure spending. Paid SaaS.
- **Egress costs** are often the surprise — AWS egress to internet $0.09/GB.
  Move heavy egress to Cloudflare R2 (free egress).
- **Idle development clusters**: schedule scale-down at night via Karpenter
  `consolidationPolicy: WhenEmptyOrUnderutilized` + `kube-downscaler`.
- **GP3 vs GP2 EBS**: GP3 is 20% cheaper for same perf. Always GP3 in new
  workloads.
- **FinOps maturity**: Crawl → Walk → Run. Start with visibility (OpenCost);
  then allocation (tags); then optimization (rightsizing + RIs).

## Sources

- https://www.infracost.io/docs/ — Infracost
- https://www.opencost.io/ — OpenCost
- https://karpenter.sh/ — Karpenter
- https://goldilocks.fairwinds.com/ — Goldilocks
- https://www.finops.org/framework/ — FinOps Foundation framework
- https://focus.finops.org/ — FOCUS billing spec
- https://kubernetes.io/docs/tasks/run-application/vertical-pod-autoscaler/ — VPA
- https://aws.amazon.com/savingsplans/ — AWS Savings Plans
- https://cloud.google.com/docs/cuds — GCP CUDs
- https://www.cast.ai/ — Cast.ai (commercial K8s cost)
- https://kubecost.com/blog/ — Kubecost blog (OpenCost upstream)
