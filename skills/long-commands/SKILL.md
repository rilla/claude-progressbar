---
name: long-commands
description: Use before running any Bash command that may take more than about ten seconds — builds, rebuilds, downloads, syncs, test suites, batch loops — and when writing a script or loop that will. The statusline draws one progress bar per running command from the tail of that command's own output (its newest `NN%`, `n/m` or `n of m`), so the command has to run in the background with its output whole, and be judged afterwards by its exit status and the tail of its output file. Loads the rules for running, reading back, picking flags, shaping loops, and staying inside the three-bar budget.
---

# claude-progressbar

The statusline shows one row per Bash command that is still running: a bar,
the elapsed time and the command's last output line. The bar is **parsed**
from the output when the newest line carries `NN%`, `n/m` or `n of m`;
otherwise it is **estimated** from earlier runs of the same command;
otherwise it bounces. Nothing is sent to you; the HUD reads the command's
output file directly. Your job is to leave that file whole and keep it out
of the conversation.

## Run long commands in the background, whole

For anything that may run longer than about ten seconds:

- Run it with `run_in_background`, output unfiltered. Claude Code writes
  the output to the task's output file, the bar reads it from there, and
  none of it lands in the conversation. Do this even when your next step
  needs the result: wait for the completion notice rather than running in
  the foreground, which hands you the whole output when it ends.
- The task's output file is already the log. Do not redirect to your own
  (`> build.log`, `| tee`), and do not pipe through `tail`, `head` or
  `grep`, wrap in `$(…)` or pass `--quiet`: the bar reads only the task's
  output file, and all of those leave it blind. Both streams are
  captured, so progress written to stderr is fine.
- When it ends, judge it by the exit status in the completion notice, then
  read only what you need from the output file the notice names:
  `tail -n 40` for the summary, `grep -n` for the failures. Never read the
  whole file back.
- Ask tools for machine-readable progress: `rsync --info=progress2`,
  `curl -#`, `wget --progress=dot:mega`, `pip --progress-bar on`,
  `docker compose … --progress plain`, `pytest -q` (its `[ 42%]`
  suffix), `cargo build` (`Compiling …` plus `[n/m]`), `git clone
  --progress`.
- Carriage-return redraws are fine: each `\r` segment counts as a line
  and the newest one wins.
- In your own loops print the step on its own line, `printf '%d/%d
  %s\n' "$i" "$n" "$item"`, or a percentage. One line per step is
  enough; more is noise in the output file and no gain on the bar.
- Repeat long commands with the same text. The ETA comes from the median
  of earlier runs of the same normalised command (`cd …`, env
  assignments, `rtk`, `sudo`, `timeout` and `time` are stripped), so a
  random temp path or a changed flag starts a fresh history.

## Stay quiet

- The HUD shows at most three bars (`--max-rows` in the statusLine
  command); extra commands collapse to `+N more running`. Do not fan out
  background commands to get more bars, and do not read a running task's
  output file to report a percentage: the HUD already shows it.
- Do not narrate progress in chat. Say what the command does when you
  start it and what came out when it ends.
- A bar that reads `quiet 45s` means the command has written nothing for
  that long. Decide whether it is stuck before it finishes, not after.
