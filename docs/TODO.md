# TODO

Remaining work, in order. Not shipped in the submission archive (excluded in
`scripts/package.sh`).

## 1. i18n — language button (3 pts, every page) · not started

- [ ] `web/src/locales/{fr,en}.json`, passed as `messages` to `createI18n` in `main.ts`
- [ ] Language toggle next to `ThemeToggle` in `AppHeader.vue`: persist in
      `localStorage` and keep `<html lang>` in sync (same pattern as `useTheme.ts`)
- [ ] Replace hardcoded strings:
  - [ ] `AppHeader` nav + `PageLayout` titles in every view, `AppFooter`
  - [ ] `Shows` (headings, loading/error/empty) + `ShowDescription` (ticket labels, SOLD OUT)
  - [ ] `Guestbook` + `ShoutoutForm` (labels, placeholders, button, errors, thanks, empty state)
  - [ ] `Contact` + `ContactForm` (labels, placeholders, inquiry options, validation errors, status)
- [ ] Check that `ShowDescription` dates re-render immediately when the language changes

## 2. Responsive + Firefox (4 pts)

- [ ] `App.vue`: `main { width: 70% }` → `width: 100%` + a `max-width`
- [ ] Header below 700px already stacks into one column; check that the nav wraps cleanly
- [ ] In **Firefox**, check every page at 390 / 768 / 1280px (Shows tickets, Guestbook, Contact form)
- [ ] Maybe do specific mobile layouts or rules ? -> In general, let's try to keep it logic and use variables / rules in main.css to avoid redundancy

## 3. Content

- [ ] Home page (empty)
- [ ] About page (empty)

## 4. Submission

- [ ] `docs/RAPPORT.md` (empty) → `just pdf`, ≤ 2 pages: technologies (justify
      `web/src` being over the 15-file limit rather than cutting files), mini user
      manual, 1–2 technical details (e.g. honeypot + rate limit, theme composable)
- [ ] Screenshots: every page × fr/en × day/night (do this after 1–3)
- [ ] Root `README.md` up to date
- [ ] `just release`, archive ≤ 3MB
