# Backlog triage — 2026-09-08

State of the 13 open issues and 11 open PRs, checked against `master` at `3.1.1`.
Nothing here has been closed or commented on yet — this is the assessment, pending
Noah's call on the public actions.

**The one thing to know about the PRs:** all 11 are by **@eugenesvk**, all from
April 2026, and they are a **stacked chain** — each says "stacked on top of the
previous ones." They branch from pre-`3.0.0` master. Since then `3.0.0` merged a
long-running fork, and `3.0.1`/`3.1.0`/`3.1.1` refactored selection wholesale
(`ENCLOSING_PAIRS`, `find_markdown_link_span`, `find_deep_link_span`,
`find_scheme_url_span`, deep links). **Every one of them will conflict**, and two
are now moot. Do not try to merge the chain as a chain.

## Issues

### Fixed — recommend closing with a pointer to the release

| # | Title | Why it's fixed | Verified |
|---|---|---|---|
| **#64** | Match URL by scope | `find_markdown_link_span` (3.1.0) resolves `[in⎀fo](URL)` to the target from anywhere in the link, including the label. Scope matching isn't needed to get the reported outcome. | ✅ `_expand("[info](https://example.com)", 3)` → `https://example.com` |
| **#57** | Open error with default app on windows | The `system_open` sentinel has run `cmd.exe /c start "" <path>` since 3.0.0 — the empty title argument the reporter asked for. The old `["start"]` settings entry it complains about no longer exists. | ✅ `open_url.py` `system_open()` |
| **#61** | URLs that contain commas | Fixed in **3.1.1** via `find_scheme_url_span`. | ✅ test `test_url_query_string_keeps_commas` |
| **#75** | Opening a folder in Explorer raises an exception | Fixed in **3.1.1** — `run_subprocess` no longer uses `check_call`, so `explorer`'s bogus exit 1 doesn't raise. | ✅ code |
| **#51** | Don't include the whole changelog for each update | Fixed back in 2.8.0 ("individual release file for each plugin version"). `messages.json` now has one file per version, which is exactly the PackageDev layout the reporter asked for. | ✅ `messages.json`, 12 entries |

### Partially fixed — recommend narrowing, not closing

| # | Title | Where it stands |
|---|---|---|
| **#56** | Relative Markdown links | Of the four examples: `[x](foo.md)` and `[x](baz.js)` now resolve from anywhere in the link (3.1.0). `[x](foo)` (no extension) depends on `file_suffixes` containing `.md`, which it doesn't by default. `[x](#heading)` is **not supported** — no anchor navigation. Recommend narrowing the issue to the heading-anchor case, which is what PR **#74** implements. |

### Still open and real

| # | Title | Assessment |
|---|---|---|
| **#68** | Very slow opening of some URLs with `.js` | Real. Each `file_suffixes` entry multiplies against `aliases` × `search_paths` × `file_prefixes`. 3.1.1 documents the cost in the setting but **keeps `[".js"]`**, because `test_file_suffixes_default_preserved` guards it as a 3.0.0 compatibility promise. **Needs your call** — see Open questions. |
| **#55** | Cyrillic text in link | Not investigated. Almost certainly percent-encoding of non-ASCII before handoff to the browser. Reproducible from the issue's own URLs. |
| **#69** | Help with settings for open in default application | A support question, now answerable: multi-line selection opens each line as its own target (3.0.0), and `.txt`/`.md` auto-edit via `autoactions` — which is why a list opens straight in Sublime with no menu. Images have no autoaction, so they should menu. Recommend replying with an `autoactions` example, then closing. |

### Stale — recommend closing as unactionable

| # | Title | Why |
|---|---|---|
| **#27** | Fail to open URL (2014) | ST2/ST3-era, `C:/Teradata` vs `C:\Teradata`. Both reported versions are long unsupported. |
| **#43** | `.pdf` fails to open on linux (2018) | Reporter's `mimeapps.list` / `xdg-open` configuration, not plugin logic. Went quiet in 2019. |
| **#52** | Casing not preserved (2020) | Already labelled `can't repro`. |

## PRs

Recommendation for the chain as a whole: **don't merge any of it as-is.** Thank
@eugenesvk, explain that 3.0.0–3.1.1 rewrote the selection layer underneath the
branches, and ask him to rebase the ones still worth having — individually, not
stacked.

| # | Title | Size | Recommendation |
|---|---|---|---|
| **#72** | Fix a doc typo | +1/-1 | **Close as already fixed.** The `</kbd>alt</kbd>` typo is gone; the README was rewritten in 3.0.0. Verified: no match in `README.md`. |
| **#77** | Don't break on spaces on Windows with default application | +1/-1 | **Close as already fixed** — same ground as #57; `system_open` already passes the empty title. The settings line it patches no longer exists. |
| **#70** | Disable potentially pathologically slow suffixes | +2/-2 | **Blocked on the `file_suffixes` decision** (Open questions). Its position is correct; the compat test is the obstacle. If you say drop it, this is a 2-line change — no need to merge the PR, but credit him. |
| **#71** | Find URLs based on scope instead of chars | +137/-5 | **Superseded.** Its stated goal (`[handle⎀this](example.com)`) works now via `find_markdown_link_span`, without a scope dependency. Close with that explanation. |
| **#74** | Open markdown heading links | +287/-8 | **Worth having** — implements the `#heading` half of #56, which nothing else covers. Needs a rebase; it's stacked on #71/#73. |
| **#73** | Mouse click enhancements | +239/-8 | **Worth considering** — closes #63. A `Default.sublime-mousemap` with `alt`+double-click already exists, so scope the overlap first. |
| **#67** | Path indicators in the popup panels | +99/-5 | Reasonable UX addition, no issue behind it. Low risk, low urgency. |
| **#62** | Granular feature flags | +44/-4 | Design decision: how much of the plugin should be switchable off. `autoactions` already covers part of the "don't bug me with edit suggestions" complaint. |
| **#65** | Per-scope delimiters | +73/-4 | Design decision. Overlaps heavily with the `ENCLOSING_PAIRS` work in 3.1.0 — the JSON-unfriendly-delimiters problem he describes is largely what bracket pairs solved. Re-evaluate whether it's still needed. |
| **#66** | Scope stops | +101/-4 | Same family as #65; depends on it. |
| **#76** | `batch_command` (experimental) | +441/-26 | Largest, self-described experimental, "a bunch of limitations." Defer. |

## Open questions for Noah

1. **`file_suffixes` default** — keep `[".js"]` (compat, current state) or drop to
   `[]` (@eugenesvk's #70, fixes #68's worst case)? Dropping it means a user who
   relied on bare `users` → `users.js` loses that silently, and
   `test_file_suffixes_default_preserved` has to change. A middle option: keep the
   default but short-circuit suffix expansion when the text looks like a URL,
   which fixes the reported symptom without touching the default.
2. **Closing issues and PRs** — nothing has been closed or commented on. The five
   fixed issues and three PRs above are ready to close whenever you say go.
3. **Root `CODEOWNERS`** — the repo has both `CODEOWNERS` (`@noahcoad @kylebebak`)
   and `.github/CODEOWNERS` (`@noahcoad`). GitHub reads `.github/` first, so the
   root file is dead and @kylebebak is not actually a code owner today. Intended?
   Left untouched because it concerns a person, not a config default.
