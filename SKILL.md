---
name: hn
description: Fetch the top Hacker News stories, let the user pick which to learn, and build an interactive HTML page that explains the chosen stories at the user's personal level (from their profile). Use when the user runs /hn or asks to read, browse, explain, or learn from Hacker News / HN front-page stories.
---

# /hn — Hacker News, explained for you

A multi-step skill that teaches the user the Hacker News stories *they* choose, at the
level described in their profile. No API key needed — you (Claude) do the explaining.

**Skill directory:** `~/.claude/skills/hn/`
- `profile.md` — the user's knowledge profile. **Always read it first.**
- `scripts/fetch_hn.py` — fetches HN data (stdlib only).

Always pause and wait for the user whenever a choice is theirs. Never auto-pick.

---

## Step 1 — Browse (in the terminal)

1. **Read `profile.md`** (in this skill's directory) to learn the user's level and goals.
   If `profile.md` does not exist, read `profile.example.md` instead, and gently tell the
   user to copy it to `profile.md` and personalize it (`cp profile.example.md profile.md`).
2. **Fetch the stories:** run

   ```
   python3 ~/.claude/skills/hn/scripts/fetch_hn.py 30
   ```

   It prints all 30 top stories in rank order with title, points, comments, the HN
   discussion link (`item?id=...`), the article URL (context only), and any self-text.
3. **Print a numbered list of all 30** in rank order. For each, write a **one-line "what
   this is about"** in the simple language the profile asks for. Use the article domain and
   any self-text to get it right. **No filtering** — show every story so the user chooses.
4. **Ask which numbers** they want to learn, then **stop and wait** for their reply. Do not
   continue until they answer.

## Step 2 — Learn (interactive HTML page)

When the user gives their picks:

1. **First invoke the `frontend-design` skill** and follow its guidance, so the page looks
   distinctive and polished — not templated. Do this every time.
2. Build **one self-contained HTML file**. All CSS + JS inline, no JS frameworks; the only
   external load may be web fonts from a CDN (always include a system-font fallback).
3. **Order the cards by increasing rank** (lowest story number first, e.g. #3, #4, #5 …),
   regardless of the order the user typed their picks.
4. For **each** selected story include:
   - **Deep-dive explanation** in plain English, assuming zero prior knowledge (match the
     depth/tone in `profile.md`).
   - **Click-to-reveal jargon** — highlight hard terms; tapping one reveals a simple
     definition.
   - **A simple inline-SVG diagram when a concept benefits from a visual** (e.g. a flow, a
     network, a loop). Keep it deliberately simple, not fancy.
   - **A self-check question** with a click-to-reveal answer.
   - **Only the Hacker News discussion link** (`https://news.ycombinator.com/item?id={id}`).
     **Do not** include the external/original article URL.
5. Add a **key-terms glossary** at the end collecting every term used, defined simply.
6. **Before saving, ask the user where to save it and what to name it — then stop and wait
   for their reply.** Specifically:
   - Run `pwd` to find the folder the user is currently in, and **offer that folder as the
     default** (so the file lands somewhere they can easily find — e.g. if they're in their
     `hn` directory, save it there). Accept any other folder they name.
   - **Ask what to name the file** (suggest a simple default like `hn-today`, but let them
     choose). Add `.html` for them if they leave it off.
   - If a file with that name already exists in that folder, ask whether to overwrite it or
     use a different name. Do not silently overwrite.
7. Save to `<chosen folder>/<chosen name>.html`, then tell the user the full path and open
   it:

   ```
   xdg-open <chosen folder>/<chosen name>.html
   ```

## Step 3 — Drill down (optional)

If the user asks to go deeper on a story (e.g. "explain #4 more" or "what are the comments
saying"), fetch that story's discussion:

```
python3 ~/.claude/skills/hn/scripts/fetch_hn.py --comments STORY_ID
```

(The story id is the number in its HN link.) Then summarize and explain the comments at the
user's level.

---

## Notes
- If `python3` fails, tell the user and stop — don't invent story data.
- Keep all explanations honest; if you're unsure what an article says, say so or fetch the
  HN discussion for context rather than guessing.
- The user can edit `profile.md` anytime; re-read it on every run so changes take effect.
