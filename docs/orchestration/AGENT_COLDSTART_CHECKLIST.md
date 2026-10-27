# Agent Cold-Start Checklist

The by-hand preconditions of the cold start in `AGENTS.md`: what no script in this repository
proves. Everything else the cold start needs is a gate it runs.

- [ ] **Auth:** the service and tool auth the task needs is present through the sanctioned path:
      the workload's security principal and the project's secrets store for runtime, each tool's
      CLI login (`gh auth status`) for tools. No inline PATs
      (`docs/standards/secrets_management_standard_v1.0.md`).
- [ ] **Every hook type installed in this clone:** `ls .git/hooks/` shows `pre-commit`,
      `commit-msg` and `pre-push`. If one is missing, run `pre-commit install`, which installs the
      types the config names. A type not installed leaves its gates inert, and CI reports it only
      after the push.
