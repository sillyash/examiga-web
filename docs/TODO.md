# TODO

Remaining work, in order. Not shipped in the submission archive (excluded in
`scripts/package.sh`).

## 1. i18n — language button (3 pts, every page) · done

- [x] `locales/{fr,en}.json`, `LanguageToggle.vue` in the header, persisted + `<html lang>`

## 2. Responsive + Firefox (4 pts)

- [ ] `App.vue`: `main { width: 70% }` → `width: 100%` + a `max-width`
- [ ] Header below 700px already stacks into one column; check that the nav wraps cleanly
- [ ] In **Firefox**, check every page at 390 / 768 / 1280px (Shows tickets, Guestbook, Contact form)
- [ ] Maybe do specific mobile layouts or rules ? -> In general, let's try to keep it logic and use variables / rules in main.css to avoid redundancy

## 3. Content

About was merged into Home (hero, next show, who we are, latest shoutouts).

- [ ] Replace the `TODO` placeholders in `home.*` (bio, members, influences) in both
      `locales/fr.json` and `en.json`
- [ ] Band photo → `web/public/band.jpg`, then point `.hero-photo` in `Home.vue` at it
      (it shows the logo for now)

## 4. Submission

- [ ] `npm run build` fails on `main`: `eslint.config.ts` imports `defineConfigWithVueTs` /
      `vueTsConfigs` as named exports that the installed `@vue/eslint-config-typescript`
      doesn't have (also crashes `npm run lint`). `scripts/package.sh` runs the build,
      so this blocks the archive.

- [ ] `docs/RAPPORT.md` (empty) → `just pdf`, ≤ 2 pages: technologies (justify
      `web/src` being over the 15-file limit rather than cutting files), mini user
      manual, 1–2 technical details (e.g. honeypot + rate limit, theme composable)
- [ ] Screenshots: every page × fr/en × day/night (do this after 1–3)
- [ ] Root `README.md` up to date
- [ ] `just release`, archive ≤ 3MB
