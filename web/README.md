# BrandBrain — demo (static frontend)

A single self-contained page (`index.html`): React + Babel + Tailwind loaded from CDN.
No build step, no backend needed — the demo runs entirely in the browser on mock data.

## Deploy to Vercel (2 minutes)

**Option A — drag & drop (no CLI):**
1. Go to https://vercel.com/new
2. Drag this `brandbrain-web` folder onto the page (or "Deploy" → upload).
3. Framework preset: **Other**. Build command: none. Output dir: `.` (root).
4. Deploy → you get a public URL like `https://brandbrain-demo.vercel.app`.

**Option B — Vercel CLI:**
```bash
npm i -g vercel        # if you don't have it
cd brandbrain-web
vercel                 # first run: log in + link project (interactive)
vercel --prod          # promote to the public production URL
```

That production URL is shareable with anyone — paste it into another Claude chat, send it to
design partners, or open it on the demo laptop. It needs no login and no server.

## Notes
- Requires internet on first load (React/Tailwind/Babel come from CDN).
- This is the frontend only. The backend (see ../brandbrain) is a stateful FastAPI service and
  should be hosted on Render/Railway/Fly, not Vercel — and its service methods are still stubs.
