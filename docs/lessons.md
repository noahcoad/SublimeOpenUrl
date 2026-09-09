# Lessons — open-url

## PAUSED: Run in Terminal (2026-09-02)

The action is **disabled** — code and tests are intact, but the entry points are unhooked:

- `open_url.sublime-commands` — the `Open URL: Run in Terminal` palette entry was removed
- `open_url.sublime-settings` — the `run in terminal` action is commented out in both
  `file_custom_commands` and `folder_custom_commands`

Left in place: `run_in_terminal()`, `_osx_terminal_args()`, `_terminal_launcher_script()`,
`_as_string()`, `RunInTerminalCommand`, the `run_in_terminal` sentinel in `BUILTIN_COMMANDS`,
the `terminal_app` setting, and 12 tests. To resume, re-add the two entry points.

**Symptom:** a new iTerm window opens but the launcher never runs — first an unexecuted path
sitting at the prompt, then (after switching from `write text` to `command`) an empty window.

**What's ruled out:** stale module and wrong argv. Instrumenting `run_in_terminal` proved the
current code ran with exactly the argv that works when pasted into a shell:

```
tag=v3-command app='iTerm' folder='/Users/ncoad/txt/sys'
args=['osascript', '-e', 'tell application "iTerm"\n\tactivate\n\tcreate window with default profile command "…/run-in-terminal.command"\nend tell']
```

Same script + same launcher file → works from a shell, fails from Sublime. So the variable is
**who the caller is**, not what's sent.

**Next lead:** macOS Automation permission — Sublime Text needs to be allowed to control iTerm
(System Settings → Privacy & Security → Automation → Sublime Text). A denied or half-granted
grant can let `activate` through while the rest of the script dies. Check `tccutil`/the console
for a `-1743` error, and try capturing osascript's stderr (the current code throws it away —
`subprocess.Popen(args)` with no pipes; capture it before guessing again).

## Run the test suite against Python 3.8 (2026-09-02)

ST 4's bundled interpreter is Python 3.8; `py` is much newer, so a 3.9+ API passes `pytest`
here and then AttributeErrors in the ST console on first real use. Cost us a
`str.removesuffix()` in `_osx_terminal_args` — 280 tests green, crash on invocation.

```bash
uv run --python 3.8 --with pytest --with pyyaml -m pytest -q
```

There's no CI (see `removed-dev-tooling.md`), so this is a manual step before calling a change
done. Full lesson, including which APIs to watch for: `~/txt/my/sublime.txt` § plugin python version.
