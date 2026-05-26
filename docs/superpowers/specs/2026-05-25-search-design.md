# Search Feature Design

**Date:** 2026-05-25  
**Status:** Approved

## Overview

Add search to the nocp TUI music browser. Press `/` to enter a query, results replace the current view. Songs play immediately on selection; artists and albums navigate to them in the music view.

## Trigger & Input

- `/` key opens a search bar in the footer area (replacing the current footer text with a `urwid.Edit` widget showing `Search: `)
- User types a query and presses Enter to submit
- Esc cancels without running a search, restoring the original footer
- While the search bar is active, all other key bindings are inactive (input is consumed by the Edit widget)

## API

New `search()` method on `Navidrome`:

```python
def search(self, query: str) -> dict:
    return self.request("search3.view", query=query,
                        artistCount=5, albumCount=10, songCount=20)
```

Returns a `subsonic-response.searchResult3` dict with keys `artist`, `album`, `song` (each a list, possibly absent if no results).

## Results View

A new `"search"` mode. On submit:

1. The previous mode name and layout body are saved to `self.pre_search_mode` and `self.pre_search_body`
2. `self.mode` is set to `"search"`
3. A single `ListBox` is built with:
   - Section header rows (`urwid.Text`, non-selectable) for each non-empty group: "Artists", "Albums", "Songs"
   - `PlainButton` rows for each result within the group
4. The layout body is replaced with this `ListBox` wrapped in a `LineBox`
5. The footer is restored to its original widget

Esc from search mode restores `self.mode`, `self.main_layout.body`, and clears saved state.

## Selection Behavior

| Result type | Action |
|-------------|--------|
| Artist | Call `on_artist_selected(None, artist_obj)` then `switch_to_music_view()` |
| Album | Call `on_album_selected(None, album_obj)` then `switch_to_music_view()` |
| Song | Play immediately via existing play logic |

Result objects are constructed as `Artist`, `Album`, and `Song` instances (same classes used elsewhere) so existing callbacks work without modification.

## Keyboard Changes

- `/` added to `handle_input` — activates search bar
- `esc` added to `handle_input` — if `self.mode == "search"`, exits search view
- Search bar `Edit` widget handles all keypresses while active; `handle_input` is not invoked during text entry (urwid routes input to focused widget first)

## Out of Scope

- Live/incremental search (search fires on Enter only)
- Podcast search (podcasts are local RSS, not on the Subsonic server)
- Radio search
- Persisting search history
