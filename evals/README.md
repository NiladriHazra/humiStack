# Skill evaluations

[cases.json](cases.json) contains two realistic tasks per skill, with synthetic
input files and explicit outcome checks. They cover normal edits, an audit-only
boundary, approval/retry exceptions, and different runtime payload paths.

## Reproduce

```sh
python3 evals/prepare.py /absolute/path/to/new-eval-directory
```

The destination's parent must exist. Existing destinations are rejected so a
rerun cannot overwrite earlier evidence. Each case gets identical `with_skill`
and `without_skill` fixture directories and a `case.json` containing its prompt
and assertions.

For each case, use fresh sessions of the same agent/model/settings:

1. **With skill:** give the case prompt, fixture directory, and absolute path to
   the relevant `skills/<name>/SKILL.md`. Have the agent follow that skill.
2. **Without skill:** give the same prompt and corresponding fixture directory,
   without loading either humiStack skill. Disable automatic skill discovery if
   it would load them. Record any unavoidable preloaded guidance.
3. Save outputs and a concise `RESULT.md` inside that run's fixture. Do not let
   runs share memory, modify the collection, or use real customer content.
4. Review assertions against the actual file diff and handoff. Record each as
   passed/failed with concrete evidence; do not grade from the agent's confidence.
5. Compare outcomes before concluding that a skill helps. Record model, settings,
   date, errors, and any provider-reported usage/time. If those counters are not
   available, leave them unknown. A single task pair is not a reliable savings
   benchmark.

When running paired tasks with subagents, launch each with-skill and baseline
pair together. Independent sessions are preferable to role-playing a baseline
inside the same conversation that authored the skill.

The helper unit tests cover deterministic failures. These tasks cover the
instructions' practical use. Neither replaces evaluation on your own repo and
runtime; compatibility with an agent's file format does not prove integration
with every version of that agent.
