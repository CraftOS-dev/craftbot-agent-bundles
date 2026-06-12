<!--
Source: https://docs.aws.amazon.com/cdk/ · https://sst.dev/docs/ · https://docs.aws.amazon.com/serverless-application-model/
Authored: June 2026 for the devops-engineer agent bundle.
-->

# AWS CDK / SST / SAM (Serverless IaC)

AWS-native infrastructure-as-code: **AWS CDK 2.x** for general AWS infra
in TypeScript/Python (synthesizes CloudFormation), **SST v3** for modern
serverless fullstack apps (built on the Pulumi runtime since v3), and
**AWS SAM** for Lambda-centric workflows (CloudFormation extension).

## When to use

- AWS-only stack with mostly-managed services (Lambda, ECS Fargate, EKS,
  DynamoDB, RDS, API Gateway, EventBridge, Step Functions).
- Serverless fullstack app (Next.js + API + DB) → SST v3.
- Lambda-heavy app with no UI → SAM (lightweight) or CDK (richer).
- Constructs pattern: reusable AWS abstractions library-style.

Skip when: multi-cloud (use `terraform-opentofu-iac` or `pulumi-iac-python-typescript`);
K8s-first (use `kubernetes-deployments-helm-kustomize`); team doesn't speak
TS/Python (CDK and SST require code).

## Setup

```bash
# AWS CDK
npm install -g aws-cdk@2.x
# OR: brew install aws-cdk
cdk --version          # cdk 2.x

# SST v3
npm install -g sst
# new project: npx create-sst@latest

# SAM
brew tap aws/tap && brew install aws-sam-cli
sam --version

# Companion
brew install jq awscli
aws configure sso       # SSO login
```

Bootstrap CDK once per AWS account + region:

```bash
cdk bootstrap aws://123456789012/us-east-1 \
  --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess
```

This creates the `CDKToolkit` stack: S3 staging bucket + ECR repo + IAM
roles for `cdk deploy`.

## Common recipes

### Recipe 1 — CDK TypeScript scaffold

```bash
mkdir prod-app && cd prod-app
cdk init app --language=typescript
# Edit lib/prod-app-stack.ts
```

```typescript
// lib/prod-app-stack.ts
import * as cdk from "aws-cdk-lib";
import * as ec2 from "aws-cdk-lib/aws-ec2";
import * as ecs from "aws-cdk-lib/aws-ecs";
import * as ecsp from "aws-cdk-lib/aws-ecs-patterns";

export class ProdAppStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const vpc = new ec2.Vpc(this, "Vpc", { maxAzs: 3, natGateways: 1 });

    const cluster = new ecs.Cluster(this, "Cluster", { vpc, containerInsights: true });

    new ecsp.ApplicationLoadBalancedFargateService(this, "Api", {
      cluster,
      cpu: 256,
      memoryLimitMiB: 512,
      desiredCount: 3,
      taskImageOptions: {
        image: ecs.ContainerImage.fromRegistry("ghcr.io/myorg/api@sha256:6ba7b810..."),
        containerPort: 8080,
      },
      publicLoadBalancer: true,
    });
  }
}

// bin/prod-app.ts
const app = new cdk.App();
new ProdAppStack(app, "Prod", { env: { account: "123456789012", region: "us-east-1" } });
```

```bash
cdk synth                    # CloudFormation template → cdk.out/
cdk diff Prod                # diff vs deployed
cdk deploy Prod --require-approval=never
```

### Recipe 2 — CDK Python (Lambda + DynamoDB)

```python
# stacks/prod_app.py
from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    aws_dynamodb as dynamodb,
    aws_apigatewayv2 as apigw,
    aws_apigatewayv2_integrations as integrations,
    Duration,
)
from constructs import Construct

class ProdAppStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        table = dynamodb.Table(
            self, "OrdersTable",
            partition_key={"name": "order_id", "type": dynamodb.AttributeType.STRING},
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            point_in_time_recovery=True,
        )

        fn = lambda_.Function(
            self, "OrdersFn",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="app.handler",
            code=lambda_.Code.from_asset("src/orders"),
            memory_size=512,
            timeout=Duration.seconds(10),
            environment={"TABLE_NAME": table.table_name},
            tracing=lambda_.Tracing.ACTIVE,
        )
        table.grant_read_write_data(fn)

        http = apigw.HttpApi(self, "Api")
        http.add_routes(path="/orders/{id}", methods=[apigw.HttpMethod.GET],
                        integration=integrations.HttpLambdaIntegration("OrdersInt", fn))
```

```bash
cdk deploy --all --require-approval=never
```

### Recipe 3 — SST v3 (Next.js + API + Postgres)

```bash
npx create-sst@latest my-app
cd my-app
```

```typescript
// sst.config.ts
export default $config({
  app(input) {
    return { name: "my-app", removal: input?.stage === "prod" ? "retain" : "remove" };
  },
  async run() {
    const db = new sst.aws.Postgres("Db", { vpc: { az: 3 } });
    const next = new sst.aws.Nextjs("Web", {
      link: [db],
      domain: $app.stage === "prod" ? "myorg.com" : `${$app.stage}.myorg.com`,
    });
    return { url: next.url };
  },
});
```

```bash
sst dev                                # local dev with live Lambda
sst deploy --stage prod                # CFN deploy via Pulumi runtime
sst remove --stage feature-1234        # delete stage
```

### Recipe 4 — SAM Lambda (template + local invoke)

```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    Runtime: python3.12
    MemorySize: 512
    Timeout: 10
    Tracing: Active

Resources:
  OrdersFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/orders/
      Handler: app.handler
      Events:
        Api:
          Type: HttpApi
          Properties: { Path: /orders/{id}, Method: get }
      Policies:
        - DynamoDBCrudPolicy: { TableName: !Ref OrdersTable }

  OrdersTable:
    Type: AWS::DynamoDB::Table
    Properties:
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions: [{ AttributeName: order_id, AttributeType: S }]
      KeySchema: [{ AttributeName: order_id, KeyType: HASH }]
```

```bash
sam validate
sam build --use-container          # build via Docker for parity
sam local invoke OrdersFunction --event events/get.json
sam local start-api                # API Gateway emulator
sam deploy --guided                # first time
sam deploy                          # subsequent
sam delete                          # tear down
```

### Recipe 5 — CDK Constructs Hub patterns

```typescript
import { SecureBucket } from "@cdklabs/cdk-secure-bucket";
import { NextjsSite } from "cdk-nextjs-standalone";

const bucket = new SecureBucket(this, "Logs", { /* encryption + access logs by default */ });
new NextjsSite(this, "Site", { path: "../app" });
```

Constructs Hub: https://constructs.dev/ — community + AWS-supported
re-usable patterns.

### Recipe 6 — Cross-account / cross-region

```typescript
const app = new cdk.App();
new NetworkStack(app, "Network", { env: { account: "111", region: "us-east-1" } });
new AppStack(app, "App-USE1", { env: { account: "222", region: "us-east-1" } });
new AppStack(app, "App-EUW1", { env: { account: "222", region: "eu-west-1" } });
cdk synth        # generates a CloudFormation template per stack
cdk deploy --all
```

### Recipe 7 — Lambda Powertools + Lambda Layers

```typescript
const layer = lambda.LayerVersion.fromLayerVersionArn(
  this, "Powertools",
  `arn:aws:lambda:${this.region}:094274105915:layer:AWSLambdaPowertoolsTypeScript:24`
);

new lambda.Function(this, "Fn", { /* ... */ layers: [layer] });
```

### Recipe 8 — Aspect for security (require encryption)

```typescript
import { Aspects, IAspect } from "aws-cdk-lib";
import { CfnBucket } from "aws-cdk-lib/aws-s3";
import { IConstruct } from "constructs";

class RequireEncryption implements IAspect {
  visit(node: IConstruct): void {
    if (node instanceof CfnBucket && !node.bucketEncryption) {
      throw new Error(`Bucket ${node.node.path} missing BucketEncryption`);
    }
  }
}
Aspects.of(app).add(new RequireEncryption());
```

`cdk synth` fails the build if any S3 bucket lacks encryption.

### Recipe 9 — `cdk-nag` for security checks

```bash
npm install cdk-nag
```

```typescript
import { AwsSolutionsChecks } from "cdk-nag";
Aspects.of(app).add(new AwsSolutionsChecks({ verbose: true }));
```

`cdk synth` annotates each finding; suppress per-resource via
`NagSuppressions.addResourceSuppressions`.

### Recipe 10 — Standard CDK flow

```bash
cdk list                      # stack names
cdk synth Prod                # emit CFN template
cdk diff Prod                 # diff vs deployed
cdk deploy Prod --require-approval=never \
  --outputs-file outputs.json \
  --rollback false             # disable rollback for fast iteration in dev
cdk destroy Prod
```

### Recipe 11 — CDK Pipelines (self-mutating CI)

```typescript
import { CodePipeline, ShellStep } from "aws-cdk-lib/pipelines";

new CodePipeline(this, "Pipeline", {
  synth: new ShellStep("Synth", {
    input: CodePipelineSource.gitHub("myorg/infra", "main"),
    commands: ["npm ci", "npm run build", "cdk synth"],
  }),
}).addStage(new AppStage(this, "Prod", { env: prodEnv }));
```

Self-mutating: pipeline updates itself when its definition changes.

## Examples

### Example 1 — Lambda + DynamoDB + API Gateway via SAM

**Goal:** Ship a CRUD API with local-test-first workflow.

1. `sam init` → choose Python 3.12 + HelloWorld template.
2. Edit `template.yaml` (Recipe 4) — add DynamoDB table + policies.
3. `sam build --use-container` — parity with Lambda runtime.
4. `sam local start-api` — `curl localhost:3000/orders/abc` works.
5. `sam deploy --guided` — first time; stack params saved to `samconfig.toml`.
6. `sam logs -n OrdersFunction --tail` — live tail prod logs.

**Result:** API live at API Gateway URL; iteration loop is `sam build && sam deploy`.

### Example 2 — Migrate CDK app to SST v3

**Goal:** Drop CloudFormation; use SST's Pulumi-based engine.

1. `npx create-sst@latest` in a new directory.
2. Translate each CDK construct to its SST equivalent (`new aws.s3.Bucket` etc.).
3. `sst dev` — runs local with live Lambda backed by SST runtime.
4. `sst deploy --stage prod` — Pulumi-driven, no CFN.

**Result:** Faster deploys (Pulumi vs CFN), same AWS resources.

## Edge cases / gotchas

- **`cdk bootstrap` must be re-run after a CDK major version bump.** Old
  bootstrap stack may lack permissions for newer asset types.
- **CFN has a 500-resource limit per stack.** Split into nested stacks or
  multiple stacks via CDK Pipelines.
- **`cdk deploy --hotswap`** skips CFN for Lambda code / ECS task def
  changes — instant deploys in dev but bypasses CFN drift detection.
- **CDK asset bundling** uses Docker by default. CI without Docker needs
  `bundling: { local: ... }` or pre-bundled assets.
- **SAM `local invoke`** uses Docker images mirroring Lambda runtimes —
  exact runtime parity but `import` errors at deploy time still possible if
  layers differ.
- **`cdk destroy`** doesn't delete retained resources (`removalPolicy:
  RETAIN`). Default for RDS, DynamoDB unless overridden.
- **SST v3 ≠ SST v2.** v3 uses Pulumi; v2 uses CDK. Migration is non-trivial;
  follow https://sst.dev/docs/migrate-from-v2.
- **CFN stack stuck in `UPDATE_ROLLBACK_FAILED`:** `aws cloudformation
  continue-update-rollback --stack-name <s> --resources-to-skip <r>`.
- **Lambda layer ARN region-specific.** Hard-code by region or use
  `arn:aws:lambda:${this.region}:...`.
- **`cdk diff`** shows IAM diffs in red even when policies haven't materially
  changed — read it carefully before assuming a regression.
- **SAM `sam sync`** is the SAM equivalent of `cdk deploy --hotswap` —
  fast inner loop for Lambda code-only changes.

## Sources

- https://docs.aws.amazon.com/cdk/v2/guide/ — CDK v2 guide
- https://docs.aws.amazon.com/cdk/api/v2/ — CDK API reference
- https://constructs.dev/ — Constructs Hub
- https://github.com/cdklabs/cdk-nag — cdk-nag security checks
- https://sst.dev/docs/ — SST v3 docs
- https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/ — SAM
- https://github.com/aws-powertools — Lambda Powertools
- https://aws.amazon.com/blogs/devops/cdk-pipelines-continuous-delivery-for-aws-cdk-applications/ — CDK Pipelines
- https://sst.dev/blog/sst-v3 — SST v3 announcement
