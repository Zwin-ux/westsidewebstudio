# westsidewebstudio.com

The website of Westside Web Studio, a one-person app studio in Los Angeles. It's a static site with no cookies, analytics or third-party requests. A small Python script fills in the app links from `apps.json`. Fonts are self-hosted.

- `index.html`: home (studio intro and the apps)
- `nursebook/`, `masri/`: app pages
- `contact/`, `privacy/`
- `qr/`: forwards old printed QR codes (`/qr?src=…`) to the home page
- `404.html`

Deployed to GitHub Pages by `.github/workflows/site.yml` on every push to `main`. DNS setup: [DNS.md](DNS.md).

## App links

`apps.json` decides where each app stamp points:

- `testing`: the app's page on this site
- `testflight`: the TestFlight join link
- `appstore`: the App Store listing

To change one, run the workflow. It updates `apps.json`, commits, and deploys:

```bash
gh workflow run site.yml -R Zwin-ux/westsidewebstudio -f app=masri -f status=testflight -f url=https://testflight.apple.com/join/XXXX
```

Or edit `apps.json`, run `python scripts/build.py`, and push.

Preview locally:

```bash
python scripts/build.py && python -m http.server 8765
```

Rules for copy: nothing invented. No testimonials, client logos or usage stats. Every app claim must match the app's current store copy.

© 2026 Westside Web Studio
