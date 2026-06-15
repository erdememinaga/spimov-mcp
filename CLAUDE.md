# spimov-mcp – AI Kılavuzu

Bu repo, eski `spimov` monorepo'sundan ayrılan **MCP server** parçasıdır (2026-06 split). PyPI paketi: `spimov-mcp`.

## Amaç
Spimov'u MCP üzerinden kullandıran sunucu. Backend'in **public v1 API**'sini API key ile tüketir; kendi başına iş mantığı barındırmaz.

## Yapı
- `src/spimov_mcp/server.py` — 13 araç tanımı
- `src/spimov_mcp/stdio_main.py` — stdio transport (yerel dosya upload destekler)
- `src/spimov_mcp/http_main.py` — HTTP/SSE transport (`mcp.spimov.com/sse`, URL-only)
- `pyproject.toml`, `build_and_publish.py`

## Transport kararı
- **stdio:** local dosya upload var → `create_dub` stdio-only. `SPIMOV_API_KEY` env var.
- **HTTP/SSE:** hosted, sadece URL tabanlı işler (dosya upload yok).

## Kardeş repolar
- `spimov-backend-dubbing` — public v1 API'yi sağlar (mcp onu tüketir)
- `spimov-frontend`, `spimov-lipsync`

## Sürüm & yayın
Sürüm artırırken: `pyproject.toml` bump → build → `twine upload`. **PyPI publish dışa dönük + geri alınamaz → önce insana sor.**

## Repo-arası seam (KIRMA)
- Backend public v1 API kontratı (`spk_live_*` Bearer)
- Araç imzaları = istemci kontratı; geriye dönük uyumu koru

## Rol
`.claude/agents/mcp.md` — **mcpçi**. PyPI publish öncesi insana sorar.

---

## Dosya Haritası (AI için)
- `src/spimov_mcp/server.py` — `build_server()` + 12 araç (`mcp_tools_definitions`). Tüm araçlar `https://spimov.com/api/v1/*` çağırır (`SPIMOV_API_BASE` ile değişir).
- **Araçlar:** create_dub, get_job_status, list_jobs, download_video, get_subtitles, cancel_job, list_languages, get_quota, dub_youtube, upload_to_youtube, list_segments, update_segment, remix_video.
- `stdio_main.py` — stdio transport, `SPIMOV_API_KEY` env (yerel dosya upload destekler).
- `http_main.py` — HTTP/SSE, Bearer header / `?api_key=`, port 8001, `/sse`.
- Sürüm: `src/spimov_mcp/__init__.py` + `pyproject.toml` (senkron tut). Yayın: `build_and_publish.py` (twine). **PyPI publish öncesi İNSANA SOR.**
