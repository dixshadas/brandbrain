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

## Landing page — "Request a Demo" form → Google Sheet

The landing page (the first screen) has a **Request a Demo** modal. Out of the box it runs in
demo mode: it validates, shows the success state, and keeps a local copy in `localStorage`
(`brainlee_demo_requests`). To persist submissions to the Google Sheet, wire a **Google Apps
Script Web App** (free, no server) and paste its URL into `window.__DEMO_ENDPOINT` near the top
of `index.html`:

1. Open the target Sheet → **Extensions → Apps Script**, paste:

   ```js
   function doPost(e) {
     const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
     const d = JSON.parse(e.postData.contents);
     sheet.appendRow([new Date(), d.first, d.last, d.email, d.company, d.role, d.phone, d.useCase]);
     return ContentService.createTextOutput(JSON.stringify({ok:true}))
       .setMimeType(ContentService.MimeType.JSON);
   }
   ```
   (Add a header row: `Timestamp | First | Last | Email | Company | Role | Phone | Use case`.)

2. **Deploy → New deployment → Web app**, Execute as *Me*, Access *Anyone*. Copy the `/exec` URL.
3. In `index.html`, set `window.__DEMO_ENDPOINT = "https://script.google.com/…/exec";`

The form POSTs as `no-cors`, so the row is appended even though the browser can't read the
response — the UI shows success optimistically and always keeps the local fallback copy.

## Notes
- Requires internet on first load (React/Tailwind/Babel come from CDN).
- This is the frontend only. The backend (see ../brandbrain) is a stateful FastAPI service and
  should be hosted on Render/Railway/Fly, not Vercel — and its service methods are still stubs.
