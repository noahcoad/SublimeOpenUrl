# Lessons — open-url

## REMOVED: Run in Terminal (2026-09-20, paused 2026-09-02)

**Gone.** Paused 2026-09-02, removed outright 2026-09-20 — it never worked from Sublime and
nobody asked for it back. Deleted: `run_in_terminal()`, `show_window()`, `_osx_terminal_args()`,
`_terminal_launcher_script()`, `_as_string()`, `RunInTerminalCommand`, the `run_in_terminal`
sentinel, the `terminal_app` setting, the README section, and 15 tests. Recover from git history
if it's ever wanted.

**Not** removed: the `terminal` / `pause` fields on custom commands (`_wrap_in_terminal`). That's
a different feature — it *runs* a command in a terminal rather than opening an idle shell — and
the README offers it as the replacement.

**Why it died.** A new iTerm window opened but the launcher never ran — first an unexecuted path
sitting at the prompt, then (after switching from `write text` to `command`) an empty window.
Stale module and wrong argv were ruled out by instrumentation: the exact argv that works pasted
into a shell failed when Sublime was the caller. So the variable was **who the caller is**, not
what was sent. The untested lead was macOS Automation permission (System Settings → Privacy &
Security → Automation → Sublime Text) — a half-granted TCC grant can let `activate` through while
the rest of the AppleScript dies with `-1743`. Note for any future attempt: the old code threw
osascript's stderr away, so capture it first.

## Run the test suite against Python 3.8 (2026-09-02)

ST 4's bundled interpreter is Python 3.8; `py` is much newer, so a 3.9+ API passes `pytest`
here and then AttributeErrors in the ST console on first real use. Cost us a
`str.removesuffix()` in `_osx_terminal_args` — 280 tests green, crash on invocation.

```bash
uv run --python 3.8 --with pytest --with pyyaml -m pytest -q
```

There's no CI (see `removed-dev-tooling.md`), so this is a manual step before calling a change
done. Full lesson, including which APIs to watch for: `~/txt/my/sublime.txt` § plugin python version.
