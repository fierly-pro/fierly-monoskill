# Cloud

> Load: AWS, Azure, GCP, or provider-neutral cloud architecture and deployment.
> Pairs with: `security/infrastructure.md`, `security/supply-chain.md`, `technologies/infrastructure/kubernetes.md`.

## Identity and access

- Least privilege: scoped roles/policies, no wildcard `*` actions/resources in production, no long-lived access keys.
- Use workload identity/OIDC for CI and workloads; rotate any static credentials.
- Separate accounts/subscriptions/projects per environment; guard production with approvals and break-glass procedures.
- Enable MFA for human admin access; audit privileged actions.
- Review unused permissions and stale roles quarterly.

## Network and exposure

- Private-by-default: databases and internal services in private subnets, no public IPs unless required.
- Security groups/firewalls: explicit ingress/egress; restrict management ports to bastion/VPN/identity-aware proxy.
- Use a WAF/CDN for public HTTP; DDoS protection at the edge.
- TLS everywhere; managed certificates with auto-renewal.
- Segment environments and trust zones; log flow logs where available.

## Data

- Encrypt at rest with customer-managed keys where required; encrypt in transit.
- Block public object storage by default; use signed URLs with short TTLs; audit bucket policies.
- Backups: automated, encrypted, cross-region where the RPO/RTO requires; test restore.
- Define data residency, retention, and deletion; classify data before choosing a region/service.
- Managed databases: enable point-in-time recovery, deletion protection, and least-privilege app users.

## Compute and serverless

- Right-size instances/functions from metrics; set autoscaling bounds.
- Serverless: set timeouts, memory, concurrency limits; handle cold starts, retries, and idempotency; keep secrets out of env if the platform exposes them broadly.
- Containers: see `technologies/infrastructure/docker.md` and `kubernetes.md`.
- Patch managed runtimes; track end-of-life versions.

## Infrastructure as Code

- Define all resources in Terraform/CloudFormation/Bicep/Pulumi; review plans before apply.
- Remote state with locking and encryption; restrict access.
- Separate state per environment; avoid manual drift.
- Policy-as-code for public buckets, open security groups, wildcard IAM, unencrypted volumes.
- Tag resources for cost, ownership, and data classification.

## Observability and cost

- Centralize logs/metrics/traces; set retention and access controls.
- Alert on security events, error/latency budgets, saturation, and cost anomalies.
- Budgets and alerts per environment/team; review idle resources and storage lifecycle.
- Define incident response, on-call, and disaster recovery; test failover/restore.

## Provider notes

- **AWS:** IAM roles + OIDC, S3 block public access, KMS, RDS PITR, CloudTrail, GuardDuty, SCPs.
- **Azure:** Entra ID/managed identity, Key Vault, Defender for Cloud, Azure Policy, private endpoints.
- **GCP:** IAM/workload identity, org policies, Cloud KMS, Secret Manager, VPC Service Controls, audit logs.

## Checklist

- [ ] No static cloud keys; least-privilege identities.
- [ ] Private network by default; management access restricted.
- [ ] Storage public access blocked; encryption enabled.
- [ ] IaC reviewed; drift and policy checks in CI.
- [ ] Backups/restore and DR tested.
- [ ] Logging, alerts, budgets, and ownership tags configured.
