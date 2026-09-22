# Maintainer Runbook

How this repository is actually run. Not learner-facing — it lives here rather than in `docs/` because it is operational, and it changes as the tooling does.

---

## The four surfaces, and what governs each

| Surface | Governed by | Gate |
| --- | --- | --- |
| `modules/` | Review | `Validate` workflow |
| `cheatsheets/` | Review | `Validate` workflow |
| `labs/` | Review + **self-verification** | `L.A.B. Simulator` workflow |
| Discussions | Labels + conventions | Human |

## CI, and what each job protects

| Workflow | Protects against |
| --- | --- |
| **Validate** | Broken notebook JSON, Python syntax errors, broken relative links, leaked secrets/account IDs/local paths, client branding returning |
| **L.A.B. Simulator** | A lab shipping broken: every reference must pass all three phases, every starter must **fail**, the index must be current, no lab may touch the network |
| **Freshness** (weekly) | Link rot — opens or comments on an issue when something breaks |
| **Welcome** | First-contribution friction |

**The account-ID check is the one to never weaken.** It greps for any 12-digit number that is not the placeholder `123456789012`. It has already caught a real leak.

---

## Adding a module

1. `modules/NN-topic/` with `slides/ notebooks/ exercises/ solutions/ activities/ src/`
2. A `README.md` matching the existing shape — objectives, concept table, ordered sequence, recording row, common mistakes, folder map, navigation
3. An LLD at `docs/architecture/lld/NN-topic.md`
4. Rows in the root `README.md` table, `modules/README.md`, and the relevant [learning paths](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/docs/learning-paths)
5. A **Field guide for this module** section linking the relevant frameworks

## Adding a lab

Seven files; `labctl verify` enforces the two rules that matter.

```bash
python labs/runner/labctl.py verify          # references pass, starters fail, DAG acyclic
python labs/runner/labctl.py index --write   # regenerate the catalog table
```

Then mark it ✅ in [`PATHWAY.md`](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/labs/PATHWAY.md). Full guide: [`CONTRIBUTING-A-LAB.md`](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/labs/CONTRIBUTING-A-LAB.md).

> `verify` caught four real bugs in the labs' own reference solutions during authoring. Never bypass it.

## Adding a discussion

Every practice thread needs a **track**, a **level** and a **format** label, and a row in the [index](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/64).

Titles: `<Topic> <N> · <what it teaches>`. No day numbers, no cohort references, no schedule artefacts — discussions are a large part of how people find this repository, and those mean nothing in a search result.

Taxonomy and conventions: [`docs/DISCUSSIONS.md`](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/docs/DISCUSSIONS.md).

---

## Content hygiene — the standing rules

Three things have leaked before and are now checked:

| Never | Placeholder |
| --- | --- |
| Real AWS account IDs | `123456789012` |
| Local filesystem paths | `/workspace/` |
| Client or cohort branding | — |

**Notebook outputs are committed on purpose** — seeing expected output is part of the teaching. That is exactly why they leak. Before committing a notebook you ran:

```bash
grep -rlE '[0-9]{12}' --include='*.ipynb' .
grep -rl "$(whoami)" --include='*.ipynb' .
```

**Discussions are not covered by CI.** They were scrubbed by hand once, after a real account ID was found in a thread. Check any long paste before posting.

---

## Not possible via the API

Save the rediscovery:

| Thing | Why |
| --- | --- |
| Creating discussion **categories** | No `createDiscussionCategory` mutation — repo settings only |
| Creating **native polls** | `CreateDiscussionInput` takes only title, body, category. Poll threads here use reactions |
| **Pinning** discussions | No `pinDiscussion` mutation — UI only. Maximum **four**. `pinnedDiscussions` is readable via GraphQL, so you can verify. The wiki [`_Sidebar`](_Sidebar) mirrors the four: change the pins, change the sidebar |
| Setting the **social preview** image | No REST field; the API silently ignores it — Settings → General |
| Creating the **wiki** | No API. The wiki git repo does not exist until the first page is created in the UI |
| Syncing the **boards** from Actions | `GITHUB_TOKEN` cannot access Projects v2, and a fine-grained PAT cannot access *user-owned* projects. Needs a classic PAT, `project` scope only — see [the board sync token](#the-board-sync-token) below |

---

## The board sync token

One secret, `PROJECT_TOKEN`, turns on two of the three boards. It is the only secret this repository
needs, and the only maintenance it asks of you is a rotation when it expires.

| | |
| --- | --- |
| **Powers** | [Hands-on Tracker](https://github.com/users/akash-coded/projects/9) and [Repo Pulse](https://github.com/users/akash-coded/projects/10) |
| **Does not power** | The [Scoreboard](Scoreboard) wiki page, `/leaderboard`, `/progress`, the weekly digest, or the [PDLC board](https://github.com/users/akash-coded/projects/8). All of those work without it |
| **Used by** | [`Pulse & Scoreboard`](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/.github/workflows/pulse.yml) — every six hours, after every Arena run, and on demand |
| **Kind of token** | A **classic** PAT with the **`project` scope only**. Nothing else |
| **First-time setup** | [`docs/setup/project-token.md`](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/docs/setup/project-token.md) |

### Why it cannot be anything else

Two dead ends, both worth remembering so they are not rediscovered:

- **`GITHUB_TOKEN`** — the token Actions provides automatically — has no access to Projects v2 at all.
- **A fine-grained PAT** has no permission that covers **user-owned** Projects. It works for
  organisation-owned projects; these boards belong to a user account, so it does not.

That leaves a classic PAT. Its `project` scope covers *every* project on the account and cannot be
narrowed, which is exactly why the token carries **no other scope** and a short expiry.

### Checking it is working

```bash
gh secret list -R akash-coded/aws-bedrock-agentcore-strands
```

`PROJECT_TOKEN` should be listed. That proves the secret exists, not that the token behind it is still
valid — for that, read the last run:

```bash
gh run view --log $(gh run list --workflow=pulse.yml --limit 1 --json databaseId --jq '.[0].databaseId') | grep -E "tracker board|pulse board|Boards not synced"
```

| You see | Meaning |
| --- | --- |
| `tracker board: N rows` and `pulse board: N live items` | Working |
| `Boards not synced — PROJECT_TOKEN is not set` | The secret is missing or misnamed |
| `Boards not synced — …` with a permission error | The token has expired, been revoked, or lost its scope |

### When it expires

**The run does not fail.** The sync emits a warning annotation, the scoreboard still publishes, and
only the two boards stop refreshing. That is deliberate: an expired token must never be able to take
the scoreboard down with it.

So the failure is quiet. The signal to watch is a board whose rows have stopped moving while the Arena
is still receiving submissions.

### Rotating

Two steps, about two minutes, and nothing to redeploy.

1. Generate a replacement at
   <https://github.com/settings/tokens/new?scopes=project&description=aws-bedrock-agentcore-strands+board+sync>
   — classic token, **`project` scope only**, 90 days. Copy it once.
2. Store it, pasting at the prompt so it never enters shell history:

   ```bash
   gh secret set PROJECT_TOKEN -R akash-coded/aws-bedrock-agentcore-strands
   ```

Then force a run rather than waiting six hours:

```bash
gh workflow run pulse.yml -R akash-coded/aws-bedrock-agentcore-strands
```

Never pass the value with `--body`, and never paste it into a file, an issue or a chat. If it is ever
exposed, revoke it first and rotate second — revoking is instant and the boards degrade gracefully.

### Revoking

```bash
gh secret delete PROJECT_TOKEN -R akash-coded/aws-bedrock-agentcore-strands
```

Then delete the token itself under *Settings → Developer settings → Tokens (classic)*. The workflow
returns to scoreboard-only mode on its own, with a warning on each run.

---

## Release rhythm

No versions — this is teaching material, not a library. Instead:

1. Land the change with CI green
2. Add a `CHANGELOG.md` entry, calling out anything that breaks deep links
3. For anything learner-visible, add a section to the [release notes discussion](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/1)

**Deep links matter more than usual here.** People bookmark specific exercises and modules. Moving a file is a breaking change; say so.

---

## Triage

| Comes in as | Route |
| --- | --- |
| Broken notebook / wrong doc | Issue → fix → note in changelog if learner-visible |
| "AWS changed" | **Highest priority.** Nothing degrades this material faster |
| Question | Q&A. Mark the answer. Add a row to [Community Answers](Community-Answers) |
| Idea | Ideas → [extension board](https://github.com/users/akash-coded/projects/6) if adopted |
| Contact-form message | Arrives by e-mail (reply-to is the sender) and as an issue in the private `inbox` repo. Reply, then close the issue |
| New error | [Error Index](Error-Index); promote to `troubleshooting.md` once seen twice |

---

## The site: the SkyWays playbook

Live at https://akash-coded.github.io/aws-bedrock-agentcore-strands/ · source in [`site/`](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/site)

The written companion is on this wiki, starting at [The Agentic PDLC](The-Agentic-PDLC). When the tool
changes substantively, the wiki pages are what need re-checking — they carry the same numbers.

| Task | How |
| --- | --- |
| Update the tool | Replace `site/app/SkyWays-Architect.html` with the new export and push. The `Pages` workflow builds and deploys |
| Change the footer, disclaimer or links | `site/frame/frame.js` (text) and `site/frame/config.js` (links, contact delivery) |
| Turn the contact relay on | `site/contact-relay/deploy.sh` in your own AWS account → click the SES verification link → paste the Function URL into `site/frame/config.js` |
| Mirror messages into GitHub | Create the `skyways-contact-relay/github` secret in Secrets Manager with a fine-grained token limited to the `inbox` repo (Issues: read/write) |
| Preview locally | `python site/build.py && python -m http.server -d site/_site 8000` |

---

## Quarterly, one minute

- [ ] Is `PROJECT_TOKEN` still alive? Check the last `Pulse & Scoreboard` run for `tracker board: N rows`.
      If it says `Boards not synced`, [rotate it](#rotating) — the run will not fail to tell you

---

## Weekly, five minutes

- [ ] `Freshness` workflow result — any link rot?
- [ ] Open issues labelled `aws-update`
- [ ] Unanswered Q&A older than a week
- [ ] Dependabot alerts
- [ ] New discussions missing labels
