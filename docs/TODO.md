# TODO — later

Work parked for later. Not shipped in the submission archive (excluded in
`scripts/package.sh`).

## i18n (language button = 3 pts, required on every page)

- [ ] `web/src/locales/fr.json` + `en.json`, loaded as `messages` in `main.ts`'s `createI18n`
- [ ] Language toggle button next to `ThemeToggle` in `AppHeader.vue`
- [ ] Persist the choice in `localStorage` (same pattern as `composables/useTheme.ts`)
      and keep `<html lang>` in sync
- [ ] Translate every hardcoded string:
  - [ ] nav links + page titles (`AppHeader.vue`, `PageLayout` titles in each view)
  - [ ] footer (`AppFooter.vue`)
  - [ ] Shows: "Upcoming", "Past shows", loading/error/empty messages
  - [ ] Tickets (`ShowDescription.vue`): "more info", "add to calendar", "get tickets",
        "tix at the door", "no more tix, sorry", "see you next time", "SOLD OUT"
  - [ ] Guestbook: form labels, placeholders, button, errors, thank-you, empty state
- [ ] Dates/times already follow `$i18n.locale` in `ShowDescription.vue`, check
      they update live when switching

## Responsive / adaptive styling

- [ ] Horizontal scrollbar on every page (seen at both 390px and 1000px wide)
- [ ] `main { width: 70% }` in `App.vue` squeezes content on phones (use `max-width` instead)
- [ ] Header/nav at phone width (nav wraps onto 2 lines, theme toggle on its own row)
- [ ] Re-check tickets and guestbook at 390 / 768 / 1280px
- [ ] Test everything in **Firefox** specifically (4 pts)

## Polish

- [ ] `~` around the city name renders as `ᴺ` in VT323, pick another glyph
- [ ] Address `geo:` link does nothing on desktop Firefox / iOS: switch to plain
      text or a web map link
- [ ] Calendar events hard-code a 2h duration (no end time in the API)
- [ ] `Contact.vue`: `id="#socials"` (the `#` means the `#socials` CSS never applies),
      images missing `alt`, links missing `rel="noopener noreferrer"`
- [ ] Home and About pages are empty
- [ ] Guestbook spam protection (honeypot field) if it gets spammed

## Submission

- [ ] `docs/RAPPORT.md` → `rapport.pdf` (≤ 2 pages): technologies (justify file counts:
      client is over the 15-file limit), mini user manual, 1–2 technical details
- [ ] Screenshots of every page × fr/en × day/night in the report
- [ ] Root README up to date
- [ ] `scripts/package.sh`, check archive ≤ 3MB
