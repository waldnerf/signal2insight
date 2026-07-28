# CLAUDE.md — signal2insights (Research Pipeline)

Applies to all work in this repository.

## Why this file exists

This pipeline has two coupled scoring systems, a two-phase discovery flow, one shared config file every skill reads, and scripts that hardcode their own root path depth. A change made without first checking current state breaks something else more often than not in a system like this. During the build of this pipeline, an archiving script silently reversed a deliberate scoring decision mid-session because two scoring systems disagreed and nobody checked for that before shipping the second one. That is the failure mode this file exists to prevent.

## Rule 1: Validate understanding, then plan, before building

Do not start editing config, scripts, or SKILL.md files from a request alone. First:

1. **State in one line what you understand the request to be.** If it is ambiguous which file, which threshold, or which skill is affected, say so before touching anything.
2. **Read the current state of what you are about to change**, every time, even if you described that file earlier in the same conversation. Do not edit from memory of what a script used to say.
3. **Name every file the change touches before starting**, not as you discover them. A rubric change usually touches: `config/editorial-profile.yaml`, the owning skill's `SKILL.md`, its backing script, and any other script that reads the same field (check `research-librarian/scripts/build_index.py` in particular, since it reads scores written by editorial-triage).
4. **Present a short plan and wait for explicit approval** before writing anything, unless the user's own message already is the plan: a numbered, specific instruction list leaves nothing to validate and can be executed directly.
5. **If the change surfaces an inconsistency (stale data, a schema mismatch, records on a retired rubric), ask a direct question about fixing it.** Don't mention it in a trailing flag and move on, and don't stay silent about it either — "don't do more than asked" is about not taking unrequested action, not about staying quiet. Scale the directness to the size of the decision: an unambiguous doc fix, just fix it and say so; anything with real cost or scope (re-screening the whole queue, re-deriving 250 records), ask before doing it.

"I forgot to check the other file" has already caused a real bug once in this pipeline — this rule exists because of that, not as a generic precaution.

## Rule 2: Collecting reviews and inputs — explain once, then one at a time

Whenever a task needs more than one decision from the user (a new scoring rubric, config threshold changes, which papers to prioritize, a structural choice):

1. **Explain the whole shape of what's being decided first**, in a sentence or two, so the user has context before answering anything. Do not lead with the first question cold.
2. **Then collect each input one at a time.** Ask, wait for the answer, ask the next one. Do not send a wall of five unrelated questions in one message and ask the user to answer all of them at once.
3. **Independent, genuinely unrelated yes/no confirmations** can be grouped in a single structured question set (e.g. `AskUserQuestion`) — that tool already presents them as discrete choices, not prose. The one-at-a-time rule is about not burying the user in unstructured prose questions, not about banning structured multi-question tools.
4. If the user answers three questions in one message before you asked them, that's fine — follow their lead. The rule is about how *you* present the questions, not about forcing a rigid back-and-forth when the user has already volunteered the answers.

## Where this applies most

| Change | Check before writing |
|---|---|
| Any edit to `config/editorial-profile.yaml` | `editorial-strategist` proposes, never writes directly, even on a direct user request — restate current value vs. proposed value first. |
| Scoring rubric changes | The rubric (`editorial-triage/SKILL.md`'s Sections A-F) drives every downstream gate through `screening.recommendations` in the config. Changing a dimension or a recommendation's `download_eligible`/`extract_eligible` flags without checking every script that reads that mapping (`download_top.py`, `build_index.py`, `knowledge-extraction`) is how the archiving bug happened the first time, when two separate scoring systems disagreed. |
| Records on a retired schema | A rubric rewrite doesn't retroactively re-score existing `metadata/scores/*.yaml` records. Scripts should treat "no `recommendation` field" as *not yet screened*, not as a failure — but flag the gap to the user as a real decision (re-screen? how much?), not a silent no-op. |
| Folder or path changes | Every backend script hardcodes `ROOT` via `Path(__file__).resolve().parents[N]`. A folder move breaks every script assuming the old depth. Grep for the old path across every `*.py` and `*.md` before calling a restructuring done, and re-run the affected scripts for real, not just `py_compile`. |
| Full-text reassessment of a score | Never silently overwrite an abstract-only score. Use `reassess_fulltext.py` so the old value, the new value, and the delta are all preserved in `metadata/scores/<id>.yaml`. |
| Anything touching `papers/pdf/` | PDFs are grouped by ISO year-week (`<year-week>/<id>.pdf`), and that week is the *download* week, not `discovery_date`. Don't assume a flat layout; glob for the file if the week isn't already known. |

## Definition of done

A change in this pipeline is not done until:

- The relevant script(s) compile clean **and** have been run for real against the actual `papers/` data (not just a synthetic smoke test) whenever the change touches file I/O.
- Every `SKILL.md` documenting a path, script, or workflow the change touched matches the new behavior, not the old one.
- `README.md`'s folder map and data-flow diagram are updated if the change touched paths, not just the individual skill's own doc.
- Canonical knowledge lives in the file the code actually reads (`config/editorial-profile.yaml`, `papers/metadata/scores/*.yaml`, `papers/metadata/extractions/*.yaml`), never only in a generated artifact, a heatmap, or a conversation. If a scoring decision only exists in something you showed the user, it isn't persisted yet.
