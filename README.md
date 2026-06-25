# 🟧 hn — Hacker News, explained for *you*

A [Claude Code](https://claude.com/claude-code) skill that reads the **top 30 Hacker News
stories**, lets you pick the ones you care about, and builds an **interactive HTML page**
that explains each chosen story **at your personal level** — every piece of jargon decoded,
with simple diagrams and self-check questions.

No API key. No server. No paid services. It runs inside Claude Code, which does the
explaining for you.

```
/hn  →  browse top 30  →  pick the ones you want  →  get a personal, interactive lesson page
```

---

## ✨ Features

- **Top 30, live** — pulls the current front page straight from the public Hacker News API.
- **You choose** — shows all 30 with a one-line summary each; no filtering, you pick.
- **Explained at your level** — reads your `profile.md`, so a beginner and an expert get
  different explanations of the same story.
- **Interactive HTML lesson page** for the stories you picked, with:
  - 📖 deep-dive explanations in plain English
  - 🖍️ **tap-to-reveal jargon** — hard words are highlighted; tap for a simple definition
  - 📊 simple inline diagrams when a concept needs a visual
  - ✅ a self-check question per story (click to reveal the answer)
  - 📚 a key-terms glossary
- **Freshly designed every run** — uses Claude Code's `frontend-design` skill so the page
  looks distinctive, not templated.
- **You name & place the file** — it asks where to save and what to call it (defaults to the
  folder you're in), so you can keep a library.
- **Drill down** — ask "explain #4 more" or "what are the comments saying" and it fetches
  and explains that story's discussion.

---

## 📋 Requirements

- **[Claude Code](https://claude.com/claude-code)** — the skill runs inside it.
- **Python 3** — used by the small fetch script (standard library only, nothing to install).
- *(Optional)* the **`frontend-design`** skill — bundled with Claude Code's official
  plugins. If it's missing the page still builds, just with simpler styling.

---

## 🚀 Install

1. Clone (or download) this repo into your Claude Code skills folder:

   ```bash
   git clone https://github.com/<your-username>/hn.git ~/.claude/skills/hn
   ```

   Or copy the `hn` folder so it lives at `~/.claude/skills/hn/`.

2. Create your personal profile from the template:

   ```bash
   cd ~/.claude/skills/hn
   cp profile.example.md profile.md
   ```

3. Open `profile.md` and fill in your level, what you know, and how deep you want
   explanations. (You can re-edit it anytime.)

That's it — Claude Code picks up the skill automatically.

---

## 🧑‍💻 Usage

In Claude Code, type:

```
/hn
```

1. You'll get the **top 30** with one-line summaries, then it waits for you.
2. Reply with the numbers you want, e.g. `3, 4, 5, 17, 29`.
3. It asks **where to save** the page and **what to name it**, then builds and opens an
   interactive HTML lesson.
4. Want more on a story? Just ask: `explain #4 more` or `what are the comments saying on #17`.

---

## 🗂️ What's in here

```
hn/
├── SKILL.md            # instructions Claude follows for /hn
├── profile.example.md  # template — copy to profile.md and personalize
├── profile.md          # YOUR profile (created by you; git-ignored, stays private)
├── scripts/
│   └── fetch_hn.py      # fetches HN stories + comments (Python stdlib only)
└── README.md
```

## ⚙️ Customizing

Everything is plain text:

- **How explanations feel** → edit `profile.md`.
- **How the page is built / the workflow** → edit `SKILL.md`.
- **How data is fetched** → edit `scripts/fetch_hn.py`.

You can also run the fetcher on its own:

```bash
python3 scripts/fetch_hn.py 10          # top 10 stories
python3 scripts/fetch_hn.py --comments 48669534   # comments on a story
```
