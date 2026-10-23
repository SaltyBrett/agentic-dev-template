---
name: release
description: 'Cut a release of the template: judge the bump, set the version constant, commit, tag annotated with the bump, push, and watch both gates runs. Operator only.'
argument-hint: <vMAJOR.MINOR.PATCH>
disable-model-invocation: true
---

# Release cut

Version: $ARGUMENTS

This runs only in the template. If `.project-profile` exists this is a project, whose baseline tags
are its own (`docs/governance/doc_control_standard.md`); stop and say so.

1. **Judge the bump** by [[reference_template_versioning]]: would a project adopting this release
   have to do something? List the decisions since the last tag (`git describe --tags --abbrev=0`,
   then the index rows added since it) with the bump each implies; the highest wins, and when
   unsure, go up. Put the version and the reasoning to the operator and wait for a yes.
2. **Start clean:** `git status --short` lists nothing and `pre-commit run --all-files` exits 0.
3. **Set the constant before the commit that gets tagged:**
   `python3 scripts/template_version.py --release <version>`.
4. **Commit** with the message `release: <version>` and no AI attribution.
5. **Tag:** `git tag -a <version> -m "<BUMP>: <what changed, by decision ID>"`. The annotation names
   the bump; the version gate refuses a tag whose annotation does not.
6. **Verify:** `pre-commit run template-version --all-files` exits 0.
7. **Push** `git push origin main`, then `git push origin <version>`, and watch both `gates` runs to
   the end with `gh run watch <id> --exit-status` ([[reference_ci_annotated_tags]]).
8. **Report** the tag, the commit it points at, and both run ids with their conclusions.
