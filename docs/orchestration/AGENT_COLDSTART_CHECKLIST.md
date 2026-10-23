# Agent Cold-Start Checklist

The by-hand preconditions of the cold start in `AGENTS.md`: what no script in this repository
proves. Everything else the cold start needs is a gate it runs.

- [ ] **Auth:** the service and tool auth the task needs is present through the sanctioned path —
      Key Vault + service principal for runtime, the CLI keyring (`gh auth status`, `az login`) for
      tools. No inline PATs (`docs/standards/secrets_management_standard_v1.0.md`).
- [ ] **Both hook types installed in this clone:** `ls .git/hooks/` shows `pre-commit` *and*
      `commit-msg`. If either is missing, run
      `pre-commit install --hook-type pre-commit --hook-type commit-msg`. With only `pre-commit`
      installed every commit-msg-stage gate is inert, and CI reports it only after the push
      (decision 2026-09-20-001, [[reference_commit_attribution_gate]]).
