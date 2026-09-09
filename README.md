# Open URL

Open files, folders, web URLs, and search queries from anywhere in Sublime Text — and a lot more besides.

- **Open URL** — the original: open the file/folder/URL under the cursor.
- **Select URL** — expand the cursor to a URL/path region and copy it to the clipboard.
- **Copy Deep Link** — copy a `path:line:/regex/` link pointing at the cursor.
- **Copy Transformed Path** — copy the current file path through a user-supplied shell transform (clipboard normalizers, anonymizers, etc.).
- **Paste Relative Path** — paste a clipboard path as the shortest of relative / `~/...` / absolute, with markdown backtick wrapping.
- **System Open this File** — hand the file you're editing to the OS default opener, no cursor target needed.
- **Run in Terminal** — open a terminal window in the folder of the file you're editing. *(Currently disabled — see [Run in Terminal](#run-in-terminal).)*

## Install

Look for **Open URL** in [Package Control](http://wbond.net/sublime_packages/package_control).

## Quick start

Put the cursor inside a file path, folder path, URL, or word and run **Open URL**:

- <kbd>ctrl+u</kbd> on macOS
- <kbd>ctrl+alt+u</kbd> on Linux/Windows
- right-click → **Open URL**
- <kbd>alt</kbd> + double-click
- <kbd>shift+cmd+p</kbd> → **Open URL**

Try it on these:

```
$HOME/Desktop
https://news.ycombinator.com
google.com
search_for_me
```

## How **Open URL** resolves what you select

### Paths with spaces

Put the cursor anywhere inside a path wrapped in **any** matched delimiter pair and the whole path is selected, spaces and all. All seven pairs behave identically:

```
'~/OneDrive/Q CST - ALL/Customers/3M'
"~/OneDrive/Q CST - ALL/Customers/3M"
`~/OneDrive/Q CST - ALL/Customers/3M`
(~/OneDrive/Q CST - ALL/Customers/3M)
[~/OneDrive/Q CST - ALL/Customers/3M]
{~/OneDrive/Q CST - ALL/Customers/3M}
<~/OneDrive/Q CST - ALL/Customers/3M>
```

Details:

- The wrapper is stripped before resolution, so the path itself is what gets opened.
- A deep-link suffix after the closing delimiter stays attached — `[my file.py]:42` opens `my file.py` at line 42.
- When pairs nest, the innermost one wins: in `<a href='~/a b.txt'>` the cursor selects `~/a b.txt`.
- A pair that opens *and* closes before the cursor isn't treated as a wrapper, so a Markdown checkbox (`- [ ] visit google.com`) still resolves `google.com` normally.
- `${VAR}` braces are part of the path, never a delimiter pair — `${HOME}/Desktop` selects whole.
- Backslash-escaped spaces (`~/a\ b.txt`) also work, unwrapped.

#### Wrapped path *plus* prose

When the quotes wrap a path **and** a comment, the whole thing isn't a path — so the wrapper is ignored and the token under the cursor is used instead:

```
  - "~/txt/aws/qcst/prj_wbr_weekly_customer_project_status.txt — project notes / reference for this prompt"
```

Cursor anywhere in the path opens the file; a `:42` deep-link suffix on it still works. This only kicks in when the wrapped text doesn't resolve *and* the bare token does resolve — on disk, or as a URL with an explicit scheme — so a genuine spaced path (`"~/Q CST - ALL/3M"`) still selects whole. Put the cursor in the prose half instead and you get the whole quoted string (which then falls through to a web search).

### Markdown links

The cursor can sit **anywhere** inside an inline markdown link — on either bracket, inside the label, on the paren, or in the target — and Open URL resolves the *target*:

```
[bits - OneDrive](https://amazon-my.sharepoint.com/shared?id=%2Fsites%2FQCST)
[my notes](~/txt/Q CST - ALL/notes.txt)
[docs](<~/txt/a b.txt>)
[wiki](https://en.wikipedia.org/wiki/Rust_(programming_language))
[foo](~/txt/f.py:12:/^def foo/)
```

Details:

- Targets may contain spaces, with or without an angle wrapper — the whole target is taken.
- A `"title"` after the target is dropped, as are surrounding whitespace and the `<...>` wrapper.
- Parens nest one level, so `Rust_(programming_language)` survives; a deep-link suffix in the target still works.
- A link with an empty target (`[a]()`) falls back to normal expansion, so the label is what resolves.
- Reference-style links (`[a][b]`) aren't followed — only inline `[label](target)`.

### URLs with a scheme

A `scheme://...` URL is matched as one unit from any cursor position inside it, so a **comma in a query string no longer truncates it**:

```
https://www.google.com/search?q=one,two
```

(A comma is otherwise a delimiter, which is what splits `notes.txt,other.txt` into two paths — that still works.)

Details:

- Trailing sentence punctuation (`.,;:!?`) is trimmed, so `see https://example.com.` opens without the period.
- Parens are kept when balanced (`Foo_(bar)`) and dropped when they're a wrapper (`(https://example.com)`).
- A quote, angle, square, or curly wrapper is never part of the URL.
- Two URLs on one line are separate spans; the one under the cursor wins.

### Resolution order

After expanding the selection (using `delimiters`), Open URL tries the following in order. The first match wins.

1. **File** — opens it in Sublime, or shows a menu (edit / reveal / new window / run in terminal / system open).
2. **Folder** — shows a menu (new window / reveal / run in terminal / add to project).
3. **Web URL** (e.g. `google.com` or `https://example.com`) — opens in your browser.
4. **`other_custom_commands` match** — passes the text to whatever shell command you've configured.
5. **Fallback** — show the modify-or-search panel, populated from `web_searchers`.

Paths can be **absolute**, **relative to the current file**, or **relative to the project root**. Env vars and `~` are expanded. The selection can be tweaked further with [URL/Path Transforms](#url--path-transforms).

## Commands

| Command | macOS | Linux/Windows |
|---|---|---|
| **Open URL** | <kbd>ctrl+u</kbd> · <kbd>alt</kbd>+double-click | <kbd>ctrl+alt+u</kbd> · <kbd>alt</kbd>+double-click |
| **Open URL: Select URL** | <kbd>ctrl+shift+u</kbd> | <kbd>ctrl+alt+shift+u</kbd> |
| **Open URL: Copy Deep Link** | <kbd>ctrl+alt+shift+u</kbd> | <kbd>ctrl+alt+shift+d</kbd> |
| **Open URL: Copy Transformed Path** | <kbd>ctrl+alt+shift+c</kbd> | <kbd>ctrl+alt+shift+c</kbd> |
| **Open URL: Paste Relative Path** | <kbd>ctrl+alt+v</kbd> | <kbd>ctrl+alt+v</kbd> |
| **Open URL: System Open this File** | <kbd>ctrl+alt+o</kbd> | <kbd>ctrl+alt+shift+o</kbd> |
| **Open URL: Run in Terminal** | *(disabled — see [Run in Terminal](#run-in-terminal))* | *(disabled)* |
| **Open URL: Skip Menu** | (palette only) | — |
| **Open URL: Use Input** | (palette only) | — |

All default keybindings can be silenced by setting `open_url.disable_default_key_bindings: true` in your User `Preferences.sublime-settings`.

### Open URL: Skip Menu

Looks for **Open URL: Skip Menu** in the Command Palette, or bind it directly:

```json
{ "keys": ["your+key+binding"], "command": "open_url", "args": { "show_menu": false } }
```

This opens files for editing, or reveals folders, without showing the action menu.

### Open URL: Use Input

Prompts for a path or URL, then runs Open URL on whatever you type. Handy when nothing's selected and you want to navigate by name.

The panel is prefilled (and preselected, so typing replaces it) with the clipboard when the clipboard looks like a path or URL — anything that resolves on disk, including a deep link like `~/txt/notes.md:85` or a path with spaces, plus single tokens that merely look path-ish (`~/…`, `./…`, `/…`, `C:\…`, `://`, a bare domain) so you can edit a path that doesn't exist yet. A `file://` URI is converted to a plain path, and a surrounding quote/bracket pair is stripped. Prose, multi-line, and oversized clipboards leave the panel empty.

## Deep Links

Open URL recognizes "deep link" suffixes attached to a path with a colon, so you can jump to a specific spot inside a file. All forms work both ways: **Open URL** navigates to them, and **Open URL: Copy Deep Link** generates them for the cursor or selection.

| Suffix form | Example | What it does |
|---|---|---|
| `:LINE` | `notes.md:42` | Open `notes.md` at line 42. |
| `:START-END` | `notes.md:120-180` | Open `notes.md` and select lines 120–180 (inclusive). |
| `:"text"` | `notes.md:"hello world"` | Open `notes.md`; jump to the first case-insensitive match of `hello world`. |
| `:/regex/` | `notes.md:/^\s*http/` | Open `notes.md`; jump to the first match of the regex. |
| `:LINE:"text"` | `notes.md:11:"hello"` | Like `:"text"`, but among multiple matches prefer the one nearest line 11. If nothing matches, fall back to line 11. |
| `:LINE:/regex/` | `notes.md:11:/^\s*http/` | Same idea with regex. Robust to file edits — the line anchors the location even when the regex is loose or the line moved. |

The combined `:LINE:/regex/` form is what **Copy Deep Link** generates by default. The line number anchors the navigation; the regex (or quoted text) is a hint that improves precision when lines have shifted.

In generated regexes, words are joined by a literal space for readability. Leading indentation becomes `^\s*` (so re-indenting the line doesn't break the anchor), and a gap that isn't a single plain space — a tab, or a run of spaces — becomes `\s+`.

### Copy Deep Link output

| Cursor / selection state | Copies |
|---|---|
| Empty cursor on a blank line | `path:LINE` |
| Empty cursor on a non-blank line | `path:LINE:/^first five words/` |
| Text selected | `path:LINE:"selected text"` |

Set `deep_link_line_number_only: true` in your settings to drop the regex/search part and emit (and parse) line-number-only deep links — useful if you find loose regex anchors more annoying than helpful.

### Pasting deep links

**Open URL: Paste Relative Path** preserves the suffix when pasting a clipboard path. So if your clipboard contains `/abs/path/notes.md:11:/^foo/`, pasting from a file in the same project yields `../notes.md:11:/^foo/` (with the suffix intact).

## Multiple cursors and multi-line selections

Open URL works with multiple cursors — every cursor is processed in parallel and the menu is skipped (treated like **Skip Menu**).

It also works with a single selection that spans multiple non-empty lines: each non-empty line is opened independently. So selecting

```
https://example.com/a
https://example.com/b
~/notes.md:42
```

and running **Open URL** opens all three.

## Custom commands

Open URL has three settings that drive the action menus:

- **`file_custom_commands`** — actions when the resolved path is a file.
- **`folder_custom_commands`** — actions when the resolved path is a folder.
- **`other_custom_commands`** — actions for text that's neither a file/folder nor a web URL.

Each entry is an object with these fields:

| Field | Required | Notes |
|---|---|---|
| `label` | yes | Shown in the quick panel. |
| `commands` | yes | Either a string (run via `shell=True`), an array (argv), or a reserved built-in name (see below). The path is appended unless the string/array contains `$url`, in which case `$url` is substituted. |
| `os` | no | `"osx"` / `"windows"` / `"linux"`. Entry only shows on this OS. |
| `pattern` | no | Regex matched against the path. Entry only shows when it matches. |
| `kwargs` | no | Passed through to [`subprocess.Popen`](https://docs.python.org/3.5/library/subprocess.html#popen-constructor). Two magic `cwd` values are supported: `"project_root"` and `"current_file"`. |
| `terminal` | no | Wrap the command in a terminal window (xterm on macOS/Linux, `cmd.exe` on Windows). |
| `pause` | no | Append a "press ENTER" prompt after the command exits. Pairs with `terminal`. |
| `pre_command` | no | String prepended to the command (e.g. `"sh"` for `"sh script.sh"`). |

Example: copy a file's path to the clipboard.

```json
"file_custom_commands": [
  { "label": "copy path", "commands": "printf '$url' | pbcopy" }
]
```

Example: open a folder in iTerm.

```json
"folder_custom_commands": [
  { "label": "open in iTerm", "os": "osx", "commands": ["open", "-a", "iTerm"] }
]
```

Example: run a shell script in a paused terminal window.

```json
"file_custom_commands": [
  {
    "label": "run",
    "pattern": "\\.sh$",
    "commands": ["sh"],
    "terminal": true,
    "pause": true
  }
]
```

### Built-in command sentinels

Sometimes the right action is in-process (no subprocess). Use one of these reserved strings for `commands`:

| Sentinel | What it does |
|---|---|
| `"edit_in_sublime"` | Open the file in Sublime. Honors any deep-link suffix on the path. |
| `"open_in_new_window"` | Open the path in a new Sublime window using the running ST instance. (On macOS this dispatches via the bundled `subl` binary so project events fire reliably for plugins like AutoOpenNotes.) |
| `"system_open"` | Hand off to the OS — `open` on macOS, `xdg-open` on Linux, `cmd /c start` on Windows. |
| `"add_to_project"` | Append the folder to the current Sublime window's project. |
| `"run_in_terminal"` | Open a terminal window with its cwd at the path — the folder itself, or a file's containing folder. Nothing is executed; you land in an interactive shell. See [Run in Terminal](#run-in-terminal). |

The shipped defaults use these for **edit** (synthesized at runtime), **reveal**, **new window**, **run in terminal**, **system open**, and **add to project**.

### Run in Terminal

> **Currently disabled** (2026-09-02). The palette entry and both menu actions are unhooked
> because the new iTerm window comes up empty when Sublime is the caller — see
> [`docs/lessons.md`](docs/lessons.md). The code and settings below are intact; re-adding the two
> entry points turns it back on.

**Open URL: Run in Terminal** opens a terminal window in the folder of the file you're editing — the terminal-side sibling of [System Open this File](#system-open-this-file), no cursor target needed. The same thing is available as a **run in terminal** action in both the file and folder menus, for a path under the cursor. Nothing is executed either way: you land in an interactive shell at that folder, ready to type.

(To *run* a script in a terminal instead, use a custom command with the [`terminal`](#custom-commands) field.)

With `terminal_app` unset the OS default terminal is used:

- **macOS** — the command is staged in a throwaway `.command` launcher and handed to `open`, so whichever app claims shell scripts takes it (check yours with `duti -x command`). That app decides window vs. tab.
- **Linux** — the `x-terminal-emulator` alternatives symlink, falling back to `xterm`.
- **Windows** — a new `cmd.exe` window (`start cmd /k`).

Set `terminal_app` to pick the app explicitly:

```json
"terminal_app": "iTerm"
```

On macOS, `"iTerm"` and `"Terminal"` are driven via AppleScript, which **guarantees a new window** (plain `open` gives iTerm a tab, since iTerm honors its own preference). Any other value — an app name or an `.app` path — goes to `open -a`. On Linux it's the emulator binary, e.g. `"gnome-terminal"`.

The launcher is handed to iTerm as the new session's `command`, never typed in with `write text`: writing text into a just-created session races the shell's startup, and on a cold iTerm the line lands at the prompt without ever running. One caveat outside our control — a **cold Terminal.app** also opens its own window at launch, so you briefly get two windows; iTerm doesn't.

## `autoactions` — pre-select an action by file type

Sometimes you want certain extensions to open without showing the menu. The `autoactions` setting matches files by `endswith` or `pattern` and pre-selects an action label from your `*_custom_commands` lists, either firing it immediately or pre-highlighting it in the menu.

Each entry:

| Field | Notes |
|---|---|
| `label` | Matches the `label` of an entry in `file_custom_commands`/`folder_custom_commands`, or one of the built-in sentinels. |
| `action` | `"auto"` skips the menu and runs the action immediately. `"menu"` shows the menu but pre-highlights the label. |
| `endswith` | Array of extensions, e.g. `[".sh", ".bash"]`. |
| `pattern` | Alternative to `endswith`: a regex on the resolved path. If both are set, `pattern` wins. |
| `os` | Optional OS filter. |

Defaults shipped with Open URL:

```json
"autoactions": [
  { "os": "windows", "endswith": [".exe", ".com"], "label": "run",  "action": "auto" },
  { "os": "windows", "endswith": [".bat", ".cmd"], "label": "run",  "action": "menu" },
  { "endswith": [".sublime-project"],              "label": "edit", "action": "auto" },
  { "endswith": [".txt", ".md", ".log", ".config", ".sublime-settings"],
    "label": "edit", "action": "auto" }
]
```

So a `.md` link auto-edits, a `.sh` link shows the menu pre-highlighting "run", and `.exe` files on Windows just run.

## URL / Path Transforms

Open URL applies these transforms to the selection before checking the file system:

- `aliases` — `{}` — string substitutions, applied first. Example: `{ "@db": "src/db/models" }` lets you type `@db/users` and have it resolve to `src/db/models/users`.
- `search_paths` — `["src"]` — directories prepended to the path.
- `file_prefixes` — `[]` — prefixes added to the basename.
- `file_suffixes` — `[".js"]` — suffixes (extensions) appended to the basename.

One path is generated for each combination of `search_paths × file_prefixes × file_suffixes`. The first one that resolves to an existing file or folder wins.

So with the defaults, typing `users` resolves to (in order): `users`, `users.js`, `src/users`, `src/users.js`. First file or folder that exists is opened.

## Web search

If the selection isn't a file, folder, or URL, Open URL shows a panel of search engines, populated from the `web_searchers` setting. The first entry in the panel is always **modify path**, which lets you tweak the term and try resolving it again.

```json
"web_searchers": [
  { "label": "google search", "url": "http://google.com/search?q=", "encoding": "utf-8" },
  { "label": "github code",   "url": "https://github.com/search?type=code&q=" }
]
```

Set `web_searchers` to `[]` if you'd rather have no search engines (only the modify-path entry remains).

## Copy Transformed Path

If you set `copy_path_transform` to a shell command, **Open URL: Copy Transformed Path** pipes the current file's path through that command and copies the result. **Copy Deep Link** uses the same transform on the path portion.

`{path}` in the template is replaced with the shell-quoted file path; the command's stdout becomes the new path. If the command exits non-zero, Open URL shows the error in the status bar and doesn't touch the clipboard.

```json
"copy_path_transform": "/opt/homebrew/bin/python3 ~/scripts/shortpath.py {path}"
```

The **Copy Transformed Path** palette entry is hidden when `copy_path_transform` is unset, so it doesn't clutter the palette unless you've configured it.

### Wrapping copied paths

`copy_path_wrap_char` (default `` ` ``) is the copy-side mirror of `plain_text_path_wrap_char` — same rules, applied when the link is put on the clipboard rather than when it's pasted. So `~/notes.txt:42:/^first five words/` gets copied as `` `~/notes.txt:42:/^first five words/` ``, and lands as one re-selectable token wherever you paste it, not just via **Paste Relative Path**.

- A deep link (`:42`, `:"text"`, `:/regex/`) is always enclosed.
- A plain path (from **Copy Transformed Path**) is enclosed only when it contains a space or another char that would break token re-selection.
- If the wrap char already appears in the path, the next available quote (`"`, `'`, `` ` ``) is used.
- Set it to `""` to copy bare, as before.

**Paste Relative Path** strips one enclosing pair off the clipboard, so a wrapped link round-trips without doubling up.

## System Open this File

**Open URL: System Open this File** hands the file in the active view to the OS default opener — `open` on macOS, `xdg-open` on Linux, `cmd /c start` on Windows. It's the `system_open` menu action, but targeting the file you're editing rather than a path under the cursor, so there's nothing to select first. Handy for previewing a markdown file, HTML page, image, or CSV in its registered app.

The command is disabled for unsaved buffers, since there's no path to hand off.

## Paste Relative Path

**Open URL: Paste Relative Path** turns a clipboard path into the shortest of:

- a path relative to the currently open file (with symlinks resolved on both sides, so symlinks-into-Dropbox don't produce huge `../../../`-chains)
- a `~/...`-shortened absolute path
- the absolute path itself

Behavior:

- Web URLs (containing `://`) are pasted as-is.
- `file://...` URIs are stripped first.
- Deep-link suffixes (`:42`, `:/regex/`, etc.) are preserved.
- One enclosing pair of quotes or brackets around the clipboard text is stripped first, so a link copied with `copy_path_wrap_char` doesn't get double-wrapped.
- In Markdown views, the result is wrapped in backticks (controlled by `paste_relative_path_markdown_backticks`).
- In non-Markdown views (`.txt`, plain text, code), the result is wrapped in `` ` `` — the `plain_text_path_wrap_char` setting — when it contains chars that would break re-selection (spaces, apostrophes, brackets, angle brackets, commas) or carries a deep-link suffix, so the pasted link re-selects as one token. If that char already appears in the path, the next available quote (`"`, `'`, `` ` ``) is used. Set the setting to `""` to only wrap on re-selection-breaking chars, with `"` preferred.

## Settings reference

Open with **Preferences → Package Settings → Open URL → Settings**.

| Setting | Default | Purpose |
|---|---|---|
| `delimiters` | `" \t\n\r\"'`` `,*<>[](){}` ` | Selection-expansion terminators (Markdown-friendly defaults). Text wrapped in any matched pair — `""` `''` ` `` ` `()` `[]` `{}` `<>` — selects whole, so paths with spaces work. |
| `trailing_delimiters` | `";.:"` | Recursively stripped from the end of the URL/path. |
| `web_browser` | `""` | Browser name (from [Python's `webbrowser` list](https://docs.python.org/3.3/library/webbrowser.html)). Empty = system default. |
| `web_browser_path` | `""` | Explicit browser executable path. Overrides `web_browser`. |
| `web_searchers` | `[google search]` | List of search engines shown in the modify-or-search panel. |
| `aliases` | `{}` | String substitutions applied to the selection. |
| `search_paths` | `["src"]` | Directory roots tried as prefixes. |
| `file_prefixes` | `[]` | Prefixes added to the basename. |
| `file_suffixes` | `[".js"]` | Extensions tried on bare names. |
| `file_custom_commands` | (6 entries) | Action menu for files. |
| `folder_custom_commands` | (6 entries) | Action menu for folders. |
| `other_custom_commands` | `[]` | Action menu for non-file/non-folder text. |
| `autoactions` | (4 entries) | Per-extension auto-action rules. |
| `deep_link_line_number_only` | `false` | When true, deep links are line numbers only (no `:"text"` or `:/regex/`). |
| `copy_path_transform` | `""` | Shell command for transforming file paths in Copy Deep Link / Copy Transformed Path. |
| `paste_relative_path_markdown_backticks` | `true` | Wrap pasted paths in backticks in Markdown views. |
| `plain_text_path_wrap_char` | `` "`" `` | Char enclosing a pasted path in non-Markdown views when it has a space (or other re-selection breaker) or a deep-link suffix. `""` = old behavior (quote only on breaking chars). |
| `copy_path_wrap_char` | `` "`" `` | Char enclosing a path or deep link copied by **Copy Deep Link** / **Copy Transformed Path**. Deep links always; plain paths only on re-selection-breaking chars. `""` = copy bare. |
| `terminal_app` | `""` | Terminal app for **Run in Terminal** and the **run in terminal** action. Empty = the OS default terminal. |

### Project-specific settings

Any of these settings can be overridden per project via the project file:

```json
{
  "folders": [{ "path": "." }],
  "settings": {
    "open_url": {
      "search_paths": ["src", "lib"],
      "file_suffixes": [".tsx", ".ts"]
    }
  }
}
```

Project settings completely replace user settings for the keys they specify (no array deep-merge).

### Disable default key bindings

Add `"open_url.disable_default_key_bindings": true` to your User `Preferences.sublime-settings`. All five Open URL bindings will become inactive; rebind them yourself in your User `Default.sublime-keymap` if you like.

## Release notes

[See version history.](https://github.com/noahcoad/SublimeOpenUrl/tree/master/messages)

## Development

Tests run in plain Python (no Sublime Text instance required):

```sh
py tests/test_open_url.py
py -m pytest tests/test_open_url.py -q
```

They live in `tests/` rather than the package root because Sublime Text loads every top-level `.py` as a plugin, which made it log `reloading plugin open-url.test_open_url` on every change.

The test suite is the only check. Lint and type-check tooling (`isort`, `flake8`, `pyright`) and the `pre-push` hook that ran them were removed — see [docs/removed-dev-tooling.md](docs/removed-dev-tooling.md) to restore them.

If you use `pyenv`, [the `3.8` version](https://www.sublimetext.com/docs/api_environments.html) in `.python-version` won't match a real `pyenv` version directly. Install some `3.8.X` and symlink: `ln -s ~/.pyenv/versions/3.8.X ~/.pyenv/versions/3.8`.

## Credits

Author: [@noahcoad](http://twitter.com/noahcoad). Long-time maintainer: [@kylebebak](https://github.com/kylebebak).

Inspired by [peterc's forum thread](http://www.sublimetext.com/forum/viewtopic.php?f=2&t=4243) and [KatsuomiK's gist](https://gist.github.com/3542836).

See also: Noah's other [Sublime Text packages](https://gist.github.com/noahcoad/712ba4e38467f5126eb8cedd9ecbc842).
