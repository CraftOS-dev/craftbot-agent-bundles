<!--
Source: https://www.pulumi.com/docs/ · https://www.pulumi.com/docs/pulumi-cloud/esc/
Authored: June 2026 for the devops-engineer agent bundle.
-->

# Pulumi IaC (Python / TypeScript)

Real-programming-language infrastructure-as-code using Pulumi 3.130+.
Choose TypeScript for type-safety + npm ecosystem, Python for ML/data
shops, Go for static binaries, C#/Java for enterprise. Pulumi ESC for
secrets and config environments. State in Pulumi Cloud (free for individuals)
or S3 backend.

## When to use

- Team prefers real code over HCL — loops, conditionals, abstractions.
- Reusable abstractions via `ComponentResource` (e.g., "our standard service").
- Mixing imperative logic (read a file, call an API, then provision).
- Cross-language stack imports (TS stack → Python stack outputs).
- Pulumi ESC for centralized secret + config management.

Skip when: team is HCL-fluent (use `terraform-opentofu-iac`); AWS-only
serverless (use `aws-cdk-sst-serverless`); state mgmt budget is zero
(Pulumi Cloud is free for individuals + small teams; S3 backend is free).

## Setup

```bash
# Install
curl -fsSL https://get.pulumi.com | sh
# OR: brew install pulumi/tap/pulumi

# Language runtimes
brew install node@20    # for TS
brew install python@3.12 uv

# Authenticate (Pulumi Cloud — free for personal)
pulumi login              # opens browser; OR `pulumi login s3://myorg-pulumi-state`

# ESC CLI
pulumi org set-default myorg
pulumi env init myorg/prod
```

Auth env vars (for non-interactive CI):
- `PULUMI_ACCESS_TOKEN` — from Pulumi Cloud → Settings → Tokens
- `AWS_PROFILE` / `GOOGLE_APPLICATION_CREDENTIALS` / `AZURE_CLIENT_ID` — cloud creds

## Common recipes

### Recipe 1 — New TypeScript stack on AWS

```bash
mkdir prod-net && cd prod-net
pulumi new aws-typescript --name prod-net --stack prod --description "Prod networking"
```

```typescript
// index.ts
import * as aws from "@pulumi/aws";
import * as awsx from "@pulumi/awsx";

const vpc = new awsx.ec2.Vpc("prod", {
  cidrBlock: "10.0.0.0/16",
  numberOfAvailabilityZones: 3,
  natGateways: { strategy: awsx.ec2.NatGatewayStrategy.OnePerAz },
  tags: { ManagedBy: "pulumi", Env: "prod" },
});

export const vpcId = vpc.vpcId;
export const privateSubnetIds = vpc.privateSubnetIds;
```

```bash
pulumi preview --diff
pulumi up --yes
pulumi stack output vpcId
```

### Recipe 2 — Python stack on GCP

```python
# __main__.py
import pulumi
import pulumi_gcp as gcp

config = pulumi.Config()
project = config.require("gcpProject")

bucket = gcp.storage.Bucket(
    "data",
    name=f"{project}-data",
    location="US",
    uniform_bucket_level_access=True,
    versioning={"enabled": True},
    lifecycle_rules=[{
        "condition": {"age": 90},
        "action": {"type": "SetStorageClass", "storage_class": "NEARLINE"},
    }],
)

pulumi.export("bucket_url", bucket.url)
```

```bash
pulumi config set gcp:project myproject-prod
pulumi config set gcpProject myproject-prod
pulumi up --yes
```

### Recipe 3 — ComponentResource for "standard service"

```typescript
// component.ts
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import * as k8s from "@pulumi/kubernetes";

interface ServiceArgs {
  name: string;
  image: pulumi.Input<string>;     // sha-pinned digest ref
  port: number;
  replicas?: number;
  envFromSecret?: string;
}

export class StandardService extends pulumi.ComponentResource {
  public readonly url: pulumi.Output<string>;

  constructor(name: string, args: ServiceArgs, opts?: pulumi.ComponentResourceOptions) {
    super("myorg:components:StandardService", name, {}, opts);

    const deploy = new k8s.apps.v1.Deployment(name, {
      metadata: { name, labels: { app: name } },
      spec: {
        replicas: args.replicas ?? 3,
        selector: { matchLabels: { app: name } },
        template: {
          metadata: { labels: { app: name } },
          spec: {
            containers: [{
              name,
              image: args.image,
              ports: [{ containerPort: args.port }],
              envFrom: args.envFromSecret ? [{ secretRef: { name: args.envFromSecret } }] : [],
              resources: { requests: { cpu: "100m", memory: "256Mi" }, limits: { cpu: "500m", memory: "512Mi" } },
            }],
          },
        },
      },
    }, { parent: this });

    const svc = new k8s.core.v1.Service(name, {
      metadata: { name, labels: { app: name } },
      spec: { selector: { app: name }, ports: [{ port: 80, targetPort: args.port }] },
    }, { parent: this });

    this.url = svc.metadata.name.apply(n => `http://${n}`);
    this.registerOutputs({ url: this.url });
  }
}
```

```typescript
// index.ts
const api = new StandardService("api", {
  name: "api",
  image: "ghcr.io/myorg/api@sha256:6ba7b810...",
  port: 8080,
  replicas: 5,
});
export const apiUrl = api.url;
```

### Recipe 4 — Pulumi ESC (Environments, Secrets, Config)

```yaml
# myorg/prod environment definition
values:
  aws:
    login:
      fn::open::aws-login:
        oidc:
          duration: 1h
          roleArn: arn:aws:iam::123456789012:role/pulumi-prod
          sessionName: pulumi
  pulumiConfig:
    aws:region: us-east-1
    api-key:
      fn::secret: ${secrets.api-key}
  environmentVariables:
    AWS_ACCESS_KEY_ID: ${aws.login.accessKeyId}
    AWS_SECRET_ACCESS_KEY: ${aws.login.secretAccessKey}
    AWS_SESSION_TOKEN: ${aws.login.sessionToken}
```

```bash
pulumi env set myorg/prod aws.login.oidc.roleArn arn:aws:iam::...
pulumi env set myorg/prod --secret secrets.api-key sk_live_xxx
pulumi env get myorg/prod
# Reference from stack
pulumi config env add myorg/prod
pulumi up
```

ESC injects AWS creds via OIDC for the run; no long-lived creds anywhere.

### Recipe 5 — Stack outputs across stacks

```typescript
// network stack exports vpcId, then app stack reads:
const networkRef = new pulumi.StackReference("myorg/network/prod");
const vpcId = networkRef.requireOutput("vpcId");

const cluster = new aws.eks.Cluster("prod", {
  vpcConfig: { subnetIds: networkRef.requireOutput("privateSubnetIds") as any },
});
```

### Recipe 6 — Secret config + automatic encryption

```bash
pulumi config set --secret db_password "$(openssl rand -base64 32)"
# OR from Pulumi ESC reference
pulumi config set db_password '${esc.secrets.db-password}'
```

```typescript
const dbPassword = config.requireSecret("db_password");
const rds = new aws.rds.Instance("prod", {
  password: dbPassword,
  // ...
});
```

`config.requireSecret` returns `Output<string>` flagged sensitive; never
logged.

### Recipe 7 — Standard plan/apply flow

```bash
pulumi stack select prod          # switch active stack
pulumi preview --diff             # show resource changes
pulumi up --yes --suppress-outputs    # apply, no interactive prompt
pulumi stack export --file backup-$(date +%F).json    # state backup
pulumi cancel                     # if a previous up is stuck
```

### Recipe 8 — Refresh + drift detection

```bash
pulumi refresh --yes              # reconcile state with cloud
pulumi preview                    # show drift as diff
# If drift exists, `pulumi up` re-converges; or run `pulumi refresh` only and reconcile in IaC
```

### Recipe 9 — Automation API (programmatic Pulumi)

```python
# scripts/provision.py
import pulumi
from pulumi import automation as auto

def program():
    bucket = pulumi.ResourceOptions()  # ... your resources

stack = auto.create_or_select_stack(
    stack_name="prod",
    project_name="data-platform",
    program=program,
)
stack.set_config("aws:region", auto.ConfigValue(value="us-east-1"))
stack.preview()
stack.up(on_output=print)
```

Useful for CI orchestrators that need to provision per-tenant infra
without subshelling out.

### Recipe 10 — Convert from Terraform / CDK

```bash
# Terraform → Pulumi
brew install pulumi/tap/pulumi-tf-import
pulumi import tf-state.tfstate --from terraform

# CDK → Pulumi (via crosscode)
npx crosscode-cli cdk-to-pulumi <cdk-app>
```

### Recipe 11 — S3 backend (no Pulumi Cloud)

```bash
pulumi login s3://myorg-pulumi-state?region=us-east-1
pulumi stack init prod --secrets-provider="awskms://alias/pulumi-secrets?region=us-east-1"
```

### Recipe 12 — CI integration (GitHub Actions OIDC)

```yaml
# .github/workflows/pulumi.yml
permissions: { id-token: write, contents: read, pull-requests: write }
jobs:
  preview:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v5
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/gh-pulumi
          aws-region: us-east-1
      - uses: pulumi/actions@v6
        with:
          command: preview
          stack-name: myorg/prod
          comment-on-pr: true
        env:
          PULUMI_ACCESS_TOKEN: ${{ secrets.PULUMI_ACCESS_TOKEN }}
```

## Examples

### Example 1 — Greenfield TS stack: VPC + EKS + ArgoCD

**Goal:** Provision prod cluster with `pulumi up`.

1. `pulumi new aws-typescript --name prod-cluster --stack prod`.
2. Author VPC (Recipe 1), then `@pulumi/eks` for the cluster.
3. Install ArgoCD via `@pulumi/kubernetes-cert-manager` chart.
4. `pulumi config set aws:region us-east-1`.
5. `pulumi preview --diff` — review additions.
6. `pulumi up --yes`.
7. `pulumi stack output kubeconfig --show-secrets > ~/.kube/config-prod`.

**Result:** EKS cluster with ArgoCD bootstrapped, kubeconfig exported.

### Example 2 — Migrate Terraform networking stack to Pulumi

**Goal:** Keep AWS resources; switch IaC tool.

1. `pulumi import tf-state.tfstate --from terraform` — converts state.
2. Review generated `__main__.py` / `index.ts` — clean up names, extract constants.
3. `pulumi refresh && pulumi preview` — expect no changes.
4. Decommission Terraform: archive the `terraform/` folder; remove from CI.

**Result:** Same cloud state, now managed by Pulumi.

## Edge cases / gotchas

- **`pulumi.Output<T>` is async-ish** — to use in template literals, call
  `.apply(v => ...)`. Direct `\`${output}\`` interpolation works in
  `Output<string>` to `Output<string>` chains only.
- **`pulumi.all([a, b]).apply(([x, y]) => ...)`** is the equivalent of
  `Promise.all` for multiple Outputs.
- **`pulumi destroy` is fast and total.** Always `pulumi preview --json |
  jq .changes` before. No `--target` in older versions; use
  `--target-dependents=false` to limit.
- **Stack references read at preview time.** If the upstream stack hasn't
  been deployed, `requireOutput` errors. Run `pulumi stack output` in CI
  to verify.
- **Secret values in state** are encrypted with `pulumi config set
  --secret`. Default Pulumi Cloud encryption; or `awskms://` /
  `azurekeyvault://` providers. Without `--secret`, they're plaintext.
- **Provider plugins are versioned**. Pin in `package.json` /
  `requirements.txt`; `pulumi plugin install` resolves at install time.
- **State locking is automatic on Pulumi Cloud** (and S3 backend with
  `?lock=true`).
- **TypeScript: `noEmit: false`** in `tsconfig.json` — Pulumi runs `tsx` /
  `ts-node` at runtime; emitted JS is optional.
- **`pulumi up --yes`** is the non-interactive flag; without it CI hangs.
- **`pulumi cancel`** if `up` deadlocks; state stays at last successful
  update (Pulumi is transactional per resource).
- **Resource renames need `aliases`** — otherwise Pulumi destroys + recreates:
  `new aws.s3.Bucket("data", {...}, { aliases: [{ name: "old-name" }] })`.

## Sources

- https://www.pulumi.com/docs/ — Pulumi docs
- https://www.pulumi.com/docs/iac/concepts/resources/components/ — ComponentResource
- https://www.pulumi.com/docs/pulumi-cloud/esc/ — Pulumi ESC
- https://www.pulumi.com/docs/iac/using-pulumi/extending-pulumi/automation-api/ — Automation API
- https://www.pulumi.com/blog/iac-recommended-practices-structuring-pulumi-projects/ — project structuring
- https://www.pulumi.com/docs/iac/adopting-pulumi/import/ — import from Terraform/CDK
- https://www.pulumi.com/registry/ — provider registry
- https://www.pulumi.com/blog/pulumi-esc-ga/ — ESC GA announcement (2024)
