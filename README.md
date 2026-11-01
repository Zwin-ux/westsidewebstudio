# westsidewebstudio.com

The website of Westside Web Studio, a one-person app studio in Los Angeles. It's a static site with no build step, no cookies, no analytics and no third-party requests. Fonts are self-hosted.

- `index.html`: home (studio intro and the apps)
- `nursebook/`, `masri/`: app pages
- `contact/`, `privacy/`
- `qr/`: forwards old printed QR codes (`/qr?src=…`) to the home page
- `404.html`

Hosted on GitHub Pages from `main` (root). DNS setup for the custom domain: [DNS.md](DNS.md).

Preview locally:

```bash
python -m http.server 8765
```

Rules for copy: nothing invented. No testimonials, client logos or usage stats. Every app claim must match the app's current store copy.

© 2026 Westside Web Studio
