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
keyboard-accessible). `window.__LEAD_ENDPOINT` (top of `index.html`) is live and points at a
**Google Apps Script Web App** bound to
[this spreadsheet](https://docs.google.com/spreadsheets/u/1/d/1_WXGP4Ijn7XM96lTKQJyeFRuyzIrC6N5dAU0DD4wxHY/edit?gid=0#gid=0).
Every real submission is POSTed there as JSON and appends a row; a copy is always kept in
`localStorage` (`brainlee_leads`) as a backstop regardless of network outcome. If
`__LEAD_ENDPOINT` is ever blanked out, the form falls back to demo mode: it still validates
and shows success, just without sending anywhere.

The deployed `doPost(e)` handler is expected to look like this — the client payload's keys
(`first`, `last`, `company`, `email`, `jobTitle`, `phone`, `useCase`, `submittedAt`, `source`)
must match whatever fields it reads off `d`:

```js
function doPost(e) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
  const d = JSON.parse(e.postData.contents);
  sheet.appendRow([
    new Date(), d.first, d.last, d.email, d.company, d.jobTitle, d.phone, d.useCase,
    d.submittedAt, d.source,
  ]);
  return ContentService.createTextOutput(JSON.stringify({ok:true}))
    .setMimeType(ContentService.MimeType.JSON);
}
```
Header row on `Sheet1` (or whichever tab the handler targets):
`Timestamp | First | Last | Email | Company | Job title | Phone | Use case | Submitted At | Source`.

To redeploy the script after edits: **Deploy → Manage deployments → edit (pencil) → New
version → Deploy**. Redeploying as a brand-new deployment instead of a new version changes
the `/exec` URL, which would require updating `window.__LEAD_ENDPOINT` again.

The form POSTs with `mode:"no-cors"` and a `text/plain` `Content-Type` — Apps Script Web
Apps don't send CORS headers back, so a normal `cors` fetch could never read the response
anyway, and an `application/json` header would trigger a CORS preflight Apps Script doesn't
answer. The body is still JSON; `JSON.parse(e.postData.contents)` doesn't care what the
declared content type was. Because the response is opaque, the UI treats a submission that's
still in flight after ~2.5s as successful optimistically — a genuine network failure (offline,
DNS, etc.) that surfaces before then still shows the retry state.

## Page structure

Hero → How Brainlee works → Built for enterprise trust → Final CTA. All sections share the
dark theme; there is no light-background section. The "See Brainlee in Action" product-video
section was removed deliberately: the public site does not show the product running. The
interactive product experience lives only on the private prototype
(see [`../prototype/`](../prototype)).

## Notes
- Requires internet on first load (React/Tailwind/Babel come from CDN).
- This is the frontend only. The backend (see `../src`) is a stateful FastAPI service and
  should be hosted on Render/Railway/Fly, not Vercel — and its service methods are still stubs.
