# Shared helper modules, deliberately NOT at the package root.
#
# Sublime Text treats every root-level .py file as an independent plugin: it imports the module and
# scans it for Command/EventListener classes. A root-level helper like url.py therefore got imported
# twice under two names (once as a plugin, once via `from .url import ...`), which duplicates its
# module-level state and is what st_package_reviewer flags as "Do not import root-level plugin
# module". Nothing inside a subpackage is auto-loaded, so this is the correct home for shared code.
