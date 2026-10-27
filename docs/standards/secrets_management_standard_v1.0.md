---
authority: secrets management - how credentials are stored, reached by workloads, scripts and agents, and rotated
implements: []
verified: 2026-10-24
---

# Secrets Management Standard v1.0

**Created:** {{DATE}}
**Status:** Active

---

## 1. Purpose

How the project's credentials are held, reached and rotated. A workload authenticates as a security
principal whose credentials live in one secrets store; a person or an agent authenticates each tool
through its own CLI login. Every script, pipeline and service follows this standard, which names no
platform.

---

## 2. Scope

- The credentials of every security principal the project runs as
- API tokens, keys and certificates
- Database connection strings and passwords
- Personal access tokens, which a tool's CLI login replaces wherever it can
- Any other sensitive configuration value

---

## 3. The security principal

A security principal is the identity a workload, service or pipeline authenticates as, distinct
from any person's account. The major platforms call it a service principal or managed identity, an
IAM role, or a service account; this standard uses the generic term throughout.

- **One per workload and environment.** A principal belongs to one workload in one environment, so
  revoking it stops exactly that workload and every log entry names it.
- **Least privilege.** Each role assignment grants the narrowest scope and the fewest actions the
  workload needs, recorded in section 5. Nothing is granted for convenience.
- **Keyless first.** In order of preference: an identity the platform attaches to the workload, with
  no credential to hold; federated sign-in, as a CI job's OpenID Connect token exchanged for
  short-lived credentials; a certificate; a client secret last, and only with an expiry.
- **Owned.** Every principal names an owner who answers for its roles and its rotation.

---

## 4. The secrets store

**Store:** `{{SECRETS_STORE}}`

Every secret lives in the one store the project names, never in code, configuration or a
repository. The store:

- authorizes access by role assignment to principals, never by a shared key;
- logs every read, write and deletion;
- keeps a deleted secret recoverable for a retention period, so a mistaken deletion is undone.

### 4.1 Inventory

| Secret | Purpose | Read by | Created |
|--------|---------|---------|---------|
| `{{PREFIX}}-{{PRINCIPAL}}-credential` | The runtime principal's credential, where it cannot be keyless | `{{PRINCIPAL}}` | {{DATE}} |
| `{{PREFIX}}-source-username` | Source system username | `{{PRINCIPAL}}` | {{DATE}} |
| `{{PREFIX}}-source-password` | Source system password | `{{PRINCIPAL}}` | {{DATE}} |

<!-- Add each secret to this inventory as it is provisioned -->

---

## 5. Principals and their roles

| Principal | Workload and environment | Role and scope | Credential | Owner |
|-----------|--------------------------|----------------|------------|-------|
| `{{PRINCIPAL}}` | The runtime workload, one principal in each environment | Reads its own secrets in `{{SECRETS_STORE}}`; each further role named here as it is granted | Keyless where the platform allows, otherwise a credential with an expiry | The project's platform owner |

<!-- Add each principal and each role as it is granted -->

---

## 6. Reaching a secret

- A workload reads a secret at run time from the store, authenticated as its principal through the
  platform's own SDK or CLI, and holds it in memory only.
- A script reads its credentials the same way. It never takes a secret as a literal, an argument or
  a file in the repository.
- A CI pipeline signs in by federation where the CI provider and the platform support it: the job's
  OpenID Connect token is exchanged for short-lived credentials of the pipeline's principal, so the
  CI provider stores no long-lived secret. Where federation is unavailable, the CI provider's
  encrypted secret store holds the principal's credential, scoped to the job that needs it.

### 6.1 Developer and agent tool authentication

A person or an agent authenticates each tool through its own CLI login, which keeps the token in the
operating system's keyring, never through a personal access token pasted into configuration or an
environment variable. `gh auth login` is the example for GitHub, where the template is hosted; each
other platform's CLI has a login of its own. Claude Code and Codex use the same login, so the tools
stay interchangeable. A token that was ever committed or exported is rotated, and its holder moves to
the CLI login.

### 6.2 Sensitive data in agent context

Never load raw or bulk sensitive data (PII, credentials, full table extracts) into an AI agent's
context window. Treat the context window as an untrusted surface for regulated data: content pasted
into a session may be retained by the tool.

- Query the governed source (a database, a warehouse or an API) and work from aggregated results,
  small samples and schema, never row dumps.
- Prefer an MCP server over ad-hoc CLI access for sensitive data: it gives tighter, auditable control
  over exactly what the agent can reach, consistent with Anthropic's guidance to use MCP, not the
  CLI, for sensitive data.
- This holds under every tool (Claude Code, Codex): it is a data-handling rule, not a tool feature.

---

## 7. Prohibited practices

| Practice | Risk | Instead |
|----------|------|---------|
| A secret in code | Exposure in source control | The secrets store |
| A secret in an environment variable in production | Exposure in process listings | The secrets store, read at run time |
| A secret in a configuration file | Exposure in backups and logs | The secrets store |
| A person's account used by a workload | No audit trail; access ends with the person | A security principal |
| One principal shared by several workloads | Revoking one stops all; logs cannot tell them apart | One principal per workload and environment |
| A long-lived token in a script | Theft | Short-lived credentials from the principal |
| A secret in a commit message or a log | Permanent exposure | Never log a secret |

---

## 8. Rotation

### 8.1 Schedule

| Credential | Rotated | Responsible |
|------------|---------|-------------|
| A principal's client secret | Every 12 months, or at its expiry if sooner | The principal's owner |
| A principal's certificate | Before its expiry | The principal's owner |
| A database password | Every 6 months | The database's owner |
| A personal access token, where no CLI login exists | Every 6 months | Its holder |

A keyless or federated credential has nothing to rotate, which is why section 3 prefers it.

### 8.2 Procedure

1. Create the new credential beside the old, in the store, as a new version.
2. Move every dependent workload to the new version.
3. Verify that each workload works with it.
4. Disable the old version.
5. After 30 days, delete it.

---

## 9. Audit and monitoring

- The store's access log and each principal's sign-in log go to the project's log service and are
  kept as long as the project's handling rules require.
- Alerts fire on a failed secret read, a secret's deletion, a change to a principal's role
  assignments, and a principal signing in from a place it never signs in from.

---

## 10. Emergency procedures

### 10.1 A compromised secret

1. Disable the secret in the store at once.
2. Rotate it: create a new credential and move every dependent workload to it.
3. Review the store's access log for unauthorized reads.
4. Record the incident in the project's security log.

### 10.2 A compromised principal

1. Disable the principal on its platform.
2. Revoke its active sessions and tokens.
3. Rotate every credential it holds.
4. Review its sign-in and activity logs for unauthorized operations.
5. Re-enable it, or replace it, with new credentials and only the roles it needs.

---

## 11. Related documents

- [Constitution](../../CONSTITUTION.md): governance rules
- [Session Handoff Standard](session_handoff_standard_v2.0.md): session continuity

---

## Version log

| Version | Date | Decision | Summary | Commit |
|---------|------|----------|---------|--------|
| 2.1 | 2026-10-25 | template | the template's version 2.1 | template |
