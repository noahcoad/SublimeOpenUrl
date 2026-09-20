# Backlog triage — 2026-09-08, re-verified 2026-09-20

**Picking this up mid-stream? Read "Resume here" below first** — it has current state, what's
unposted, and what's waiting on a decision. The tables further down are the standing assessment.

State of the 13 open issues and 11 open PRs, originally checked against `master` at `3.1.1`.
Written as an assessment pending Noah's call on the public actions; since then six issues have
been closed and three PRs commented on — see "Resume here".

**Re-verified 2026-09-20 against `master` at `3.2.0`** (`eda09af`), 317 tests passing. Every
"fixed" row below still holds, exercised through `find_selection` / `find_markdown_link_span` /
`find_scheme_url_span` rather than read off the source. **One row moved: #56 is now fully fixed** —
3.2.0's `find_heading_slug_row` resolves `[x](#heading)`, the one case that was still missing, which
also **supersedes PR #74**. So the close list is **six issues, not five**: #51, #56, #57, #61, #64,
#75. Also newly confirmed: quoted paths with spaces select whole (`"/home/a/my file.pdf"` →
`/home/a/my file.pdf`), which answers @alec1's follow-up on #43, and `run_subprocess` passes an
argument *list*, so spaces never hit a shell.

**The one thing to know about the PRs:** all 11 are by **@eugenesvk**, all from
April 2026, and they are a **stacked chain** — each says "stacked on top of the
previous ones." They branch from pre-`3.0.0` master. Since then `3.0.0` merged a
long-running fork, and `3.0.1`/`3.1.0`/`3.1.1` refactored selection wholesale
(`ENCLOSING_PAIRS`, `find_markdown_link_span`, `find_deep_link_span`,
`find_scheme_url_span`, deep links). **Every one of them will conflict**, and two
are now moot. Do not try to merge the chain as a chain.

**Corollary, verified 2026-09-20 by commit count: the per-PR diff sizes below overstate each PR's
own change.** #62 = 1 commit, #65 = 3, #67 = 5, #76 = 16 (the whole stack). So #62 is genuinely its
own diff; #76's +441 is mostly everything underneath it. **#70 is the exception** — 1 commit, and it
does not appear to be stacked. Read each PR's own commit, not its diff.

## Resume here — session state as of 2026-09-20 (evening)

`master` is at **`1f8f77a`, two commits past `3.2.0` (`eda09af`), unpushed.** 310 tests pass on
`py -m pytest tests -q` and on the ST-3.8 gate
(`uv run --python 3.8 --with pytest --with pyyaml -m pytest -q`). Working tree clean, no branches.
No version bump or release notes written for the two new commits yet.

- `21367ac` — **Run in Terminal removed entirely** (paused 2026-09-02, cut after 18 days unhooked).
  Also deleted the dead root `CODEOWNERS`. Details and the preserved diagnosis in `docs/lessons.md`.
  Kept the `terminal` / `pause` fields on custom commands — different feature, README offers it as
  the replacement.
- `1f8f77a` — **resolved target on every quick-panel input line** (`📄 ~/txt/notes.md:42`, `📁`,
  `◆`, `🔍`). This is PR **#67**'s idea built correctly; see that row below.

### Posted to GitHub

Six fixed issues closed with comments (#51, #56, #57, #61, #64, #75), plus a repro-request on
**#68** and a reply on **#76**. Noah posted his own comment on **#62**. All logged in
`~/txt/my/forum_threads.txt`.

### Drafted, NOT posted

| For | Where | Gist |
|---|---|---|
| **#70** | `~/prj/desk/openurl-drafts/pr70-comment.md` | Don't drop the `.js` default; do the `//` early-bail + candidate dedup instead. Restates #68's three questions (deliberately — he'll see a PR notification sooner). |
| **#62** | transcript only | Ask for more examples. Probably moot — Noah posted a shorter version himself. |
| **#67** | not written | Close as shipped independently at `1f8f77a`, crediting the idea. |
| **#65** | not written | Explain it targets dead code (see below). |

### Waiting on @eugenesvk

**#66** (he confirmed `//etc/hosts` in comments) and **#76**. **#68** is waiting on the three
repro questions — the answer decides whether #70 or the early-bail is the right fix.

### Bugs found while triaging, not yet filed or fixed

1. **`get_selection` is dead code.** Defined `open_url.py:833`, **zero callers**, no test coverage.
   Cursor expansion goes through `find_selection` → `TOKEN_TERMINATORS` (computed at import from
   `ENCLOSING_PAIRS`, not configurable).
2. **The `delimiters` setting is therefore inert.** Its only read is `self.config["delimiters"]` at
   line 846, inside dead `get_selection` — yet it still ships and is still documented as controlling
   expansion. (`trailing_delimiters` *is* live, via `remove_trailing_delimiters`.) Either rewire
   `find_selection` to honor it or drop the setting and document `TOKEN_TERMINATORS` as fixed.
   **This is also why PR #65 is pointless as written** — it extends the dead path.
3. **A malformed `autoactions` entry silently no-ops.** Schema is
   `{ os?, pattern? | endswith?, label, action }`; `endswith` must be a **list** and `action` must be
   `"auto"` or `"menu"`. Get it wrong and there's no error, just no autoaction. Cost me a failing
   test before I noticed.
4. **`generate_urls` never dedups** (`open_url.py:598`), and `os.path.join("src", "//example.com")`
   discards the `search_paths` prefix, so an absolute-ish selection produces literal duplicate
   candidates — each stat'd separately. See the #68 row.

### Noah's-call items still open

The `file_suffixes` default (#68/#70) — see Open questions. Whether to nudge channel PRs
**#9555** / **#9567**. Whether to disable the `Report unreachable packages` cron on his
`package_control_channel` fork (it re-notifies daily). The two **Wuvist/subl_paste_md** PRs (#1, #2).
The GSC `AGREE` three-state status, and the Package Control channel PR fixing GSC's stale `details`
URL.

## Issues

**Posted and closed 2026-09-20: all six fixed issues — #51, #56, #57, #61, #64, #75.** Each got a
short thank-you, an apology for the delay, one sentence on what fixed it, and an invitation to reopen.
Logged in `~/txt/my/forum_threads.txt`. **7 open issues remain** (#27, #43, #52, #55, #63, #68, #69).
All 11 PRs are still open; #76 has a reply and #62 has one from Noah, none are closed or merged.

### Fixed — closed 2026-09-20

| # | Title | Why it's fixed | Verified |
|---|---|---|---|
| **#64** | Match URL by scope | `find_markdown_link_span` (3.1.0) resolves `[in⎀fo](URL)` to the target from anywhere in the link, including the label. Scope matching isn't needed to get the reported outcome. | ✅ `_expand("[info](https://example.com)", 3)` → `https://example.com` |
| **#57** | Open error with default app on windows | The `system_open` sentinel has run `cmd.exe /c start "" <path>` since 3.0.0 — the empty title argument the reporter asked for. The old `["start"]` settings entry it complains about no longer exists. | ✅ `open_url.py` `system_open()` |
| **#61** | URLs that contain commas | Fixed in **3.1.1** via `find_scheme_url_span`. | ✅ test `test_url_query_string_keeps_commas` |
| **#75** | Opening a folder in Explorer raises an exception | Fixed in **3.1.1** — `run_subprocess` no longer uses `check_call`, so `explorer`'s bogus exit 1 doesn't raise. | ✅ code |
| **#51** | Don't include the whole changelog for each update | Fixed back in 2.8.0 ("individual release file for each plugin version"). `messages.json` now has one file per version, which is exactly the PackageDev layout the reporter asked for. | ✅ `messages.json`, 15 entries |
| **#56** | Relative Markdown links | **Completed by 3.2.0.** All four examples resolve: `[x](foo.md)`, `[x](baz.js)`, `[x](foo)` and — the one that was missing at 3.1.1 — `[x](#heading)`, via `find_heading_slug_row`. | ✅ all four through `find_markdown_link_span`; `find_heading_slug_row` returns the heading row and `None` for an unmatched slug |

### Still open and real

| # | Title | Assessment |
|---|---|---|
| **#68** | Very slow opening of some URLs with `.js` | Real, but **the cross-product theory is wrong** — measured 2026-09-20. `//example.com` yields only **4** candidates with `[".js"]` vs **2** without, and `os.path.isdir("//example.com/")` is 0.000s on macOS, so count can't explain 10s. The likely mechanism: `.js` invents a *second hostname* (`//example.com.js`), and on Windows both are UNC paths whose stat blocks on SMB/DNS until **that name** times out — two names failing independently, where a repeat of one name is cached. Also found: `os.path.join("src", "//example.com")` discards the prefix, so `search_paths` does nothing here and the list holds literal duplicates. **Unverified — no Windows box.** #68 asks the three questions that settle it. |
| **#55** | Cyrillic text in link | Not investigated. Almost certainly percent-encoding of non-ASCII before handoff to the browser. Reproducible from the issue's own URLs. |
| **#63** | Open URL under the cursor | **Partly there** — `Default.sublime-mousemap` binds `alt`+double-click to `open_url`, so click-to-open works. But it uses `press_command: drag_select`, which *does* move the text cursor, and "without changing the text cursor position" was the literal ask. A `context`-guarded binding without `drag_select` would finish it. PR **#73** is the contributor's own version. Missing from the original triage tables — added 2026-09-20. |
| **#69** | Help with settings for open in default application | A support question, now answerable: multi-line selection opens each line as its own target (3.0.0), and `.txt`/`.md` auto-edit via `autoactions` — which is why a list opens straight in Sublime with no menu. Images have no autoaction, so they should menu. Recommend replying with an `autoactions` example, then closing. |

### Stale — recommend closing as unactionable

| # | Title | Why |
|---|---|---|
| **#27** | Fail to open URL (2014) | ST2/ST3-era, `C:/Teradata` vs `C:\Teradata`. Both reported versions are long unsupported. **Verified 2026-09-20:** all four forms now *select* correctly — `C:\Teradata`, `C:/Teradata`, and both with a trailing separator (@mkirzon's variant). The handoff itself is unverifiable without Windows, but nothing in today's selection layer reproduces the report. |
| **#43** | `.pdf` fails to open on linux (2018) | Reporter's `mimeapps.list` / `xdg-open` configuration, not plugin logic. Went quiet in 2019. `system_open` now shells to `xdg-open` by default, so the custom `commands: ["thunar"]` workaround is no longer needed, and the spaces follow-up is handled (quoted paths select whole; args are passed as a list). |
| **#52** | Casing not preserved (2020) | Already labelled `can't repro`. Still can't — `/tmp/TEST_FILE.txt` round-trips through `find_selection` unchanged. |

## PRs

Recommendation for the chain as a whole: **don't merge any of it as-is.** Thank
@eugenesvk, explain that 3.0.0–3.1.1 rewrote the selection layer underneath the
branches, and ask him to rebase the ones still worth having — individually, not
stacked.

| # | Title | Size | Recommendation |
|---|---|---|---|
| **#72** | Fix a doc typo | +1/-1 | **Close as already fixed.** The `</kbd>alt</kbd>` typo is gone; the README was rewritten in 3.0.0. Verified: no match in `README.md`. |
| **#77** | Don't break on spaces on Windows with default application | +1/-1 | **Close as already fixed** — same ground as #57; `system_open` already passes the empty title. The settings line it patches no longer exists. |
| **#70** | Disable potentially pathologically slow suffixes | +2/-2 | **Recommend the narrower fix instead** — draft at `~/prj/desk/openurl-drafts/pr70-comment.md`. Dropping `.js` removes one of two bad hostnames rather than fixing anything; anyone who sets suffixes gets the delay back, including a user following the README's own `[".tsx", ".ts"]` example. Better: (a) bail out of path resolution on a `//` prefix — `handle()` stats candidates *before* deciding whether the selection is a URL, so a protocol-relative URL pays full UNC cost on the way to being recognized; (b) dedup `generate_urls`. Both keep the default. Hold until #68's questions are answered. |
| **#71** | Find URLs based on scope instead of chars | +137/-5 | **Superseded.** Its stated goal (`[handle⎀this](example.com)`) works now via `find_markdown_link_span`, without a scope dependency. Close with that explanation. |
| **#74** | Open markdown heading links | +287/-8 | **Superseded as of 3.2.0** (was "worth having" at 3.1.1). `find_heading_slug_row` + `goto_heading_anchor` shipped the `#heading` case independently. Close crediting the diagnosis — he was right that it was the gap in #56. |
| **#73** | Mouse click enhancements | +239/-8 | **Worth considering** — closes #63. A `Default.sublime-mousemap` with `alt`+double-click already exists, so scope the overlap first. |
| **#67** | Path indicators in the popup panels | +99/-5 | **Shipped independently at `1f8f77a` — close it.** Good idea, three bugs in the execution: it displayed `raw_path` (the selected text) rather than the resolved path, so it answered a question you already knew; it hardcoded `selected_index=-1`, dropping the `autoactions` pre-highlight `file_action`/`folder_action` already set; and its glyph was U+241C (Control Pictures), an empty box in most coding fonts. It also covered two of the four panels. All four points have regression tests now. |
| **#62** | Granular feature flags | +44/-4 | Design decision: how much of the plugin should be switchable off. Noah commented 2026-09-20. **Neither of its two capabilities is expressible in 3.2.0** — `autoactions` covers the menu-noise reading but not the URLs-only reading. (Noah's comment says you can "just run the command on URLs"; not quite — with `web_searchers: []` a non-path still pops a one-item "modify path" panel.) |
| **#65** | Per-scope delimiters | +73/-4 | **Close — it extends dead code.** `delimiters` is read only inside `get_selection`, which has zero callers; real expansion goes through `find_selection` → `TOKEN_TERMINATORS`. Making an inert setting per-scope changes nothing at runtime. Fix the inert setting first (see Resume § bugs), then re-ask whether per-scope is wanted. |
| **#66** | Scope stops | +101/-4 | Same family as #65; depends on it. **Awaiting @eugenesvk** — he replied confirming the `//etc/hosts` case in comments. |
| **#76** | `batch_command` (experimental) | +441/-26 | Largest, self-described experimental. **Replied 2026-09-20 asking for more examples.** The gap is real: `open_url.py:770-771` sets `show_menu = False` once there's more than one URL, because `show_quick_panel` is async and only one panel can be up at a time — so a batch takes default actions with no way to say "reveal all of these." That's also what #69 was asking. The sticking point is his majority-wins rule: 5 files + 3 folders + 3 URLs opens the 5 and **silently drops the other 6**. |

## Open questions for Noah

1. **`file_suffixes` default** — keep `[".js"]` or drop to `[]` (#70)?
   **What the setting is for**, traced 2026-09-20: it's a **module-import resolver for bare names**,
   added in 2.6.0 by @kylebebak (`56023db`) for issue **#50** — SASS partials (`@import 'grid'` →
   `_grid.scss`) and JS imports (`'./search-input.component'` → `.component.js`), strings that are
   deliberately *not* filenames because the language's resolver appends the extension.
   `file_prefixes` (the `_`) and `search_paths` (the `src`) are the other two thirds of that same
   issue — one feature, three settings, one commit. So `[".js"]` is the default only because its
   author worked in JavaScript; it's the one default that encodes a language. For a Python/Go/Rust
   user it adds a wasted stat to every bare-name selection.
   **Recommendation:** keep it, and fix #68 at the `//` instead (see the #70 row). Note
   `tests/test_open_url.py:2194` (`test_file_suffixes_default_preserved`) exists specifically to stop
   this default drifting, so changing it means deleting that test on purpose.
2. **Closing issues and PRs** — six issues closed 2026-09-20. **#67 is now ready to close** (shipped
   at `1f8f77a`), and #65, #71, #72, #74, #77 are ready on the assessments above. Say go.
3. ~~**Root `CODEOWNERS`**~~ — resolved: deleted in `21367ac`. `.github/CODEOWNERS` (`@noahcoad`)
   is the live one; the root file was already dead. The `messages/*.md` release notes still credit
   @kylebebak and stay as-is — published history.
4. **Release for the two new commits** — no version bump or `messages/` entry written yet. The
   terminal removal is a user-visible removal, so it probably wants its own note.
