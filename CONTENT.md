# Spimov MCP — Content / Listing Kit

Ready-to-use copy for the MCP marketplace, GitHub, PyPI, and launch posts.
Marketing sections sell outcomes; the **Tools** section is the developer-facing
reference. Everything below reflects the actual v0.4.0 capabilities.

---

## Taglines

> **Dub any video into 17 languages — straight from your AI chat.**

- *AI video dubbing for Claude and any MCP client.*
- *Paste a YouTube link, get it dubbed. No dashboard, no downloads.*

---

## Short description (marketplace card / GitHub "About")

> Spimov MCP lets Claude (and any MCP client) dub videos into 17 languages, edit
> translations line-by-line, burn subtitles, and publish straight to YouTube —
> all from natural language. Works locally (file upload) or over the hosted HTTP
> server.

One-line (PyPI / GitHub About):

> MCP server for Spimov — dub videos, generate subtitles, and publish to YouTube
> from Claude Desktop, Claude Code, or Claude web.

---

## Long description (listing body)

### Spimov MCP — AI video dubbing, inside your chat

Spimov MCP connects the [Spimov](https://spimov.com) dubbing engine to Claude and
any Model Context Protocol client. Ask in plain language — *"dub this YouTube
short into German and upload it unlisted to my channel"* — and the whole pipeline
runs server-side: transcription, translation, voice synthesis, lip-sync, and
publishing.

**What you can do**

- 🎬 **Dub from a YouTube link or a local file** — regular videos, Shorts, and YouTube Music all supported.
- 🌍 **17 target languages**, with auto source-language detection.
- 🗣️ **Choose your voice engine** — `xtts` (high-quality, default), `chatterbox` (emotion-aware), or `elevenlabs`.
- ✍️ **Edit before you publish** — list transcript segments and fix any line's text, emotion, or speaker; only that segment is re-synthesized.
- 💬 **Subtitles your way** — fetch SRT/VTT, burn them in, or embed soft tracks in extra languages.
- 🎚️ **Remix without re-dubbing** — adjust the audio mix, subtitle styling, or lip-sync on a finished job.
- 📺 **Publish to YouTube** automatically when the dub finishes.
- 🔗 **Get a shareable download link** for the finished MP4 — works in the browser, no API key needed.

**14 tools** across dubbing, editing, subtitles, and publishing (see below).

**Works everywhere MCP does**

- **Claude Desktop / Claude Code** (stdio) — supports local file upload.
- **Claude web & hosted clients** — connect to the hosted Streamable HTTP server, no install required.

**Setup in 2 minutes** — grab an API key from spimov.com, drop it into your MCP
config, and start dubbing.

---

## Tools (14)

> Developer-facing reference. MCP clients auto-discover these via `list_tools`;
> this table is here so human evaluators can see the full scope at a glance.

**Create**
- `create_dub` — dub a local video file (stdio only)
- `dub_youtube` — dub a YouTube link/Short; optional auto-upload to a channel

**Track**
- `get_job_status` · `list_jobs` · `get_quota` · `cancel_job`

**Edit & refine**
- `list_segments` — inspect transcript (text, speaker, emotion, timing)
- `update_segment` — edit one line's text/emotion/speaker; re-synths just that segment
- `remix_video` — re-render audio mix / subtitle styling / lip-sync, no re-dub

**Get results**
- `get_download_url` — shareable browser download link (use over HTTP/web)
- `download_video` — save the MP4 locally (stdio only)
- `get_subtitles` — fetch SRT/VTT in any embedded language
- `upload_to_youtube` — publish (or retry) a finished job to a connected channel

**Reference**
- `list_languages` — supported source/target languages

---

## Launch / announcement post (X / LinkedIn)

> We just shipped **Spimov MCP** 🎬
>
> Dub any video into 17 languages without leaving your AI chat. Paste a YouTube
> link → Claude transcribes, translates, voices, and can publish it straight to
> YouTube.
>
> • Local file or YouTube URL
> • Edit any line, re-synth just that segment
> • SRT/VTT, burned-in or soft subtitles
> • Works in Claude Desktop, Claude Code & Claude web
>
> `pip install spimov-mcp` → spimov.com
> #MCP #Claude #AIdubbing

---

## Marketplace metadata (fields)

| Field | Value |
|---|---|
| **Name** | Spimov |
| **Category** | Media / Video |
| **Description** | Dub videos into 17 languages, edit translations, generate subtitles, and publish to YouTube — from any MCP client. |
| **Auth** | API key (`spk_live_…`) |
| **Homepage** | https://spimov.com |
| **Install (stdio)** | `pip install spimov-mcp` |
| **Connect (HTTP)** | `https://mcp.spimov.com/mcp` |
