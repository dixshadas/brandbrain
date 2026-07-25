# Brainlee — marketing site (`brainlee.tech`)

A single self-contained page (`index.html`): React + Babel + Tailwind loaded from CDN.
No build step, no backend needed.

This is the **public marketing site only**. The interactive product prototype is a
separate, independently-deployed app — see [`../prototype/`](../prototype) and
[`../DEPLOY.md`](../DEPLOY.md) for the two-project (`brainlee.tech` +
`demo.brainlee.tech`) setup. Nothing in this folder links to, references, or ships the
prototype's code.

## Deploy to Vercel

See [`../DEPLOY.md`](../DEPLOY.md) for the full two-project deployment guide. Quick version:

```bash
npm i -g vercel        # if you don't have it
cd web
vercel                 # first run: log in + link project (interactive)
vercel --prod          # promote to the public production URL
```

## "Request a Demo" form → your CRM/sheet

The site has one conversion event: the **Request a Demo** modal (validated, spam-guarded,
keyboard-accessible). Out of the box it runs in demo mode: it validates, shows the
success state, and keeps a local copy in `localStorage` (`brainlee_leads`). To POST
submissions somewhere real, set `window.__LEAD_ENDPOINT` near the top of `index.html` to
any endpoint that accepts a `POST` with a JSON body (first, last, company, email,
jobTitle, phone, useCase, submittedAt, source).

A free, no-server option is a **Google Apps Script Web App**:

1. Open the target Sheet → **Extensions → Apps Script**, paste:

   ```js
   function doPost(e) {
     const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
     const d = JSON.parse(e.postData.contents);
     sheet.appendRow([new Date(), d.first, d.last, d.email, d.company, d.jobTitle, d.phone, d.useCase]);
     return ContentService.createTextOutput(JSON.stringify({ok:true}))
       .setMimeType(ContentService.MimeType.JSON);
   }
   ```
   (Add a header row: `Timestamp | First | Last | Email | Company | Job title | Phone | Use case`.)

2. **Deploy → New deployment → Web app**, Execute as *Me*, Access *Anyone*. Copy the `/exec` URL.
3. In `index.html`, set `window.__LEAD_ENDPOINT = "https://script.google.com/…/exec";`

The form POSTs as `no-cors`, so the row is appended even though the browser can't read the
response — the UI shows success optimistically and always keeps the local fallback copy.

## Product tour video

`window.__VIDEO_URL` (also near the top of `index.html`) gates the Section 2 player: blank
shows a composed poster placeholder (never a broken player), set it to an `.mp4`/`.webm`
URL to enable the real autoplay-on-scroll, pause-off-screen, fullscreen-capable player.

## Notes
- Requires internet on first load (React/Tailwind/Babel come from CDN).
- This is the frontend only. The backend (see `../src`) is a stateful FastAPI service and
  should be hosted on Render/Railway/Fly, not Vercel — and its service methods are still stubs.
