# Secrets Management Standard v1.0

**Version:** 1.0
**Created:** {{DATE}}
**Status:** Active

---

## 1. Purpose

This standard defines how secrets, credentials, and sensitive configuration values are managed. All automation scripts, pipelines, and services MUST follow these practices.

---

## 2. Scope

This standard applies to:
- API tokens and access credentials
- Service Principal client IDs and secrets
- Database connection strings and passwords
- Gateway credentials
- GitHub Personal Access Tokens (PATs)
- Any other sensitive configuration values

---

## 3. Architecture

### 3.1 Central Secrets Store

**Azure Key Vault:** `{{KEYVAULT_NAME}}`

All secrets are stored in a single, centrally-managed Azure Key Vault with:
- RBAC authorization (not access policies)
<!-- profile:gcc -->
- FedRAMP High compliance (GCC-compatible)
<!-- /profile:gcc -->
- Audit logging enabled
- Soft delete and purge protection enabled

### 3.2 Authentication Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    Automation Script                            │
│                  (Python, PowerShell)                           │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│              Azure Key Vault ({{KEYVAULT_NAME}})                │
│                                                                 │
│  ┌─────────────────────┐  ┌─────────────────────┐              │
│  │ SPN Client ID       │  │ SPN Client Secret   │              │
│  └─────────────────────┘  └─────────────────────┘              │
│  ┌─────────────────────┐                                       │
│  │ SPN Tenant ID       │                                       │
│  └─────────────────────┘                                       │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Azure AD / Entra ID                          │
│              (OAuth Client Credentials Flow)                    │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Target API / Service                         │
│                    (Bearer Token Auth)                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Key Vault Inventory

### 4.1 Service Principal Credentials

| Secret Name | Purpose | Created |
|-------------|---------|---------|
| `{{PREFIX}}-spn-client-id` | Service Principal App ID | {{DATE}} |
| `{{PREFIX}}-spn-client-secret` | Service Principal password | {{DATE}} |
| `{{PREFIX}}-spn-tenant-id` | Azure AD Tenant ID | {{DATE}} |

### 4.2 Data Source Credentials

| Secret Name | Purpose | Created |
|-------------|---------|---------|
| `{{PREFIX}}-source-username` | Source system username | {{DATE}} |
| `{{PREFIX}}-source-password` | Source system password | {{DATE}} |

<!-- Add project-specific secrets to this inventory as they are provisioned -->

---

## 5. Service Principal Configuration

### 5.1 Identity

| Property | Value |
|----------|-------|
| Display Name | `{{SPN_NAME}}` |
| Application ID | `{{APP_ID}}` |
| Secret Expiry | 2 years from creation |

### 5.2 Permissions

| Scope | Role/Permission |
|-------|-----------------|
| Azure Subscription | Contributor |
| Key Vault | Key Vault Secrets User |

<!-- Add project-specific permissions as they are granted -->

---

## 6. Usage in Scripts

### 6.1 Python Scripts

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://{{KEYVAULT_NAME}}.vault.azure.net", credential=credential)

secret = client.get_secret("{{PREFIX}}-spn-client-id")
```

### 6.2 PowerShell Scripts

```powershell
# Retrieve secrets from Key Vault (requires az login)
$clientId = az keyvault secret show --vault-name {{KEYVAULT_NAME}} --name {{PREFIX}}-spn-client-id --query value -o tsv
$clientSecret = az keyvault secret show --vault-name {{KEYVAULT_NAME}} --name {{PREFIX}}-spn-client-secret --query value -o tsv
$tenantId = az keyvault secret show --vault-name {{KEYVAULT_NAME}} --name {{PREFIX}}-spn-tenant-id --query value -o tsv
```

### 6.3 GitHub Actions

```yaml
- name: Azure Login
  uses: azure/login@v1
  with:
    client-id: ${{ secrets.AZURE_CLIENT_ID }}
    tenant-id: ${{ secrets.AZURE_TENANT_ID }}
    subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

- name: Get Secret from Key Vault
  run: |
    SECRET=$(az keyvault secret show --vault-name {{KEYVAULT_NAME}} --name {{PREFIX}}-spn-client-id --query value -o tsv)
```

### 6.4 Developer & Agent Tool Authentication (CLI keyring)

For **developer and AI-agent tool auth** (as opposed to runtime/service auth, which uses Key Vault +
SPN above), prefer a **CLI keyring** over Personal Access Tokens or tokens in environment variables:

| Service | Preferred | Avoid |
|---------|-----------|-------|
| GitHub | `gh auth login` (stores creds in the OS keyring) | PAT pasted into config / `GH_TOKEN` env var |
| Azure | `az login` / `DefaultAzureCredential` | Client secret in a dotfile |

Rationale: the CLI keyring keeps tokens out of the repo, out of shell history, and out of process
listings — and both Claude Code and Codex authenticate identically, preserving tool interoperability.
If a PAT was ever committed or exported, **rotate it** and migrate to the CLI keyring.

### 6.5 Sensitive Data in Agent Context

Never load raw or bulk sensitive data (PII, credentials, full table extracts) into an AI agent's context
window. Treat the context window as an untrusted, non-compliant surface for regulated data — content
pasted into a session may be retained by the tool.

- Query the governed source (warehouse / API) and work from **aggregated results, small samples, and
  schema** — not row dumps.
- Prefer an **MCP server over ad-hoc CLI** for sensitive-data access: it gives tighter, auditable control
  over exactly what the agent can reach (consistent with Anthropic's guidance to use MCP, not the CLI,
  for sensitive data).
- This applies equally under any tool (Claude, Codex) — it is a data-handling rule, not a tool feature.

---

## 7. Prohibited Practices

| Practice | Risk | Alternative |
|----------|------|-------------|
| Hardcoded secrets in code | Exposure in source control | Use Key Vault |
| Secrets in environment variables (production) | Exposure in process listing | Use Key Vault |
| Secrets in config files | Exposure in backups/logs | Use Key Vault |
| Shared user account credentials | No audit trail, MFA issues | Use Service Principal |
| Long-lived tokens in scripts | Token theft | Acquire fresh tokens |
| Secrets in commit messages | Permanent exposure | Never log secrets |

---

## 8. Secret Rotation

### 8.1 Rotation Schedule

| Secret Type | Rotation Frequency | Responsible |
|-------------|-------------------|-------------|
| SPN Client Secret | Every 12 months | Platform Admin |
| Database Passwords | Every 6 months | DBA |
| PATs | Every 6 months | Developer |

### 8.2 Rotation Procedure

1. Create new secret in Key Vault with `-v2` suffix
2. Update dependent systems to use new secret
3. Verify all systems work with new secret
4. Disable old secret
5. After 30 days, delete old secret

---

## 9. Audit and Monitoring

### 9.1 Key Vault Diagnostics

Key Vault audit logs should be sent to:
- Azure Monitor Log Analytics workspace
- Azure Storage for long-term retention

### 9.2 Alerts

Configure alerts for:
- Failed secret access attempts
- Secret deletions
- Role assignment changes

---

## 10. Emergency Procedures

### 10.1 Compromised Secret

1. **Immediately disable** the secret in Key Vault
2. Rotate the secret (create new, update systems)
3. Review audit logs for unauthorized access
4. Document incident in security log

### 10.2 SPN Compromise

1. Disable the Service Principal in Entra ID
2. Revoke all active sessions
3. Rotate client secret
4. Review audit logs for unauthorized operations
5. Re-enable SPN with new secret

---

## 11. Related Documents

- [Constitution](../../CONSTITUTION.md) - Governance rules
- [Session Handoff Standard](session_handoff_standard_v2.0.md) - Session continuity

---

## 12. Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | {{DATE}} | — | Initial version |
