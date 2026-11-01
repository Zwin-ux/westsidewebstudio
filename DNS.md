# Pointing westsidewebstudio.com at GitHub Pages

Only the owner can do this, in IONOS (Domains & SSL → westsidewebstudio.com → DNS). Nothing has been changed at IONOS or Resend.

GitHub values come from GitHub's docs, checked 31 Oct 2026:
https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site

## Before you start: what the domain has now (looked up 31 Oct 2026)

| Host | Type | Value | Action |
|---|---|---|---|
| `@` | MX | `mx00.ionos.com`, `mx01.ionos.com` (priority 10) | **Leave alone.** This is the inbox. |
| `@` | TXT | `v=spf1 include:_spf-us.ionos.com ~all` | **Leave alone.** |
| `send` | MX | `feedback-smtp.us-east-1.amazonses.com` | **Leave alone.** Resend sending. |
| `send` | TXT | `v=spf1 include:amazonses.com ~all` | **Leave alone.** Resend sending. |
| `resend._domainkey` | TXT | `p=MIGf…` (DKIM key) | **Leave alone.** Resend DKIM. |
| `ops` | CNAME | `dtjrawma.up.railway.app` | Leave alone (the old Hermes admin console). |
| `nursebook` | CNAME | `zwin-ux.github.io` (to be added for the Nursebook site, repo `Zwin-ux/nursebook-site`) | **Keep.** Add it if it isn't there yet. |
| `www` | CNAME | `43msm5zv.up.railway.app` | **Change** (step 3). This is the old postcard site. |
| `@` | A / AAAA | none | **Add** (step 3). |

**Do not edit or delete any MX or TXT record.** Email (receiving through IONOS, sending through Resend) depends on them. Every change below is an A, AAAA or CNAME record.

## Step 1. Verify the domain with GitHub (recommended, do first)

This stops anyone else from claiming the domain on GitHub Pages.

1. Go to https://github.com/settings/pages and choose **Add a domain**. Enter `westsidewebstudio.com`.
2. GitHub shows a TXT record with a host like `_github-pages-challenge-Zwin-ux` and a random value.
3. In IONOS, **add** that as a new TXT record. It has its own host name, so it does not touch the existing `@` TXT record.
4. Back on GitHub, click **Verify**. DNS can take a few minutes to an hour.

## Step 2. Say yes to the preview

Once you've approved the screenshots, the custom domain gets set on the repo (Settings → Pages → Custom domain → `westsidewebstudio.com`). That adds a `CNAME` file. From then on the github.io address redirects to westsidewebstudio.com, so steps 2 and 3 should happen close together.

## Step 3. Change the DNS records in IONOS

Add four **A** records for the apex (host `@`):

| Host | Type | Value |
|---|---|---|
| `@` | A | `185.199.108.153` |
| `@` | A | `185.199.109.153` |
| `@` | A | `185.199.110.153` |
| `@` | A | `185.199.111.153` |

Add four **AAAA** records for the apex (host `@`):

| Host | Type | Value |
|---|---|---|
| `@` | AAAA | `2606:50c0:8000::153` |
| `@` | AAAA | `2606:50c0:8001::153` |
| `@` | AAAA | `2606:50c0:8002::153` |
| `@` | AAAA | `2606:50c0:8003::153` |

Edit the existing **www** record:

| Host | Type | Old value | New value |
|---|---|---|---|
| `www` | CNAME | `43msm5zv.up.railway.app` | `zwin-ux.github.io` |

Notes:
- The CNAME target has no repository name in it, just `zwin-ux.github.io`.
- If IONOS says the domain is connected to an IONOS website or parking page, switch its usage to custom DNS records first. Otherwise IONOS may add its own A/AAAA records next to GitHub's.
- Don't add a wildcard (`*`) record. GitHub warns that it allows subdomain takeover.
- Keep the `nursebook` CNAME (`nursebook` → `zwin-ux.github.io`). It serves nursebook.westsidewebstudio.com from the `Zwin-ux/nursebook-site` repo. Verifying the domain in step 1 also protects this subdomain.

## Step 4. HTTPS

When DNS resolves (check with `nslookup westsidewebstudio.com`), GitHub issues a certificate, which can take up to an hour. Then tick **Enforce HTTPS** in the repo's Settings → Pages.

## What this switches off

The `www` record currently serves the old Railway app (repo `Zwin-ux/botbot3`: the postcard page, the $149 audit funnel, `/audit`, and the graffiti wall API). After step 3 those pages no longer load on westsidewebstudio.com.
- Printed QR codes that point at `https://www.westsidewebstudio.com/qr?src=…` still work. The new site has a `/qr/` page that forwards to the home page.
- Any other old path shows the new site's 404 page, which links home.
- The Railway app itself keeps running at its Railway URL and at `ops.westsidewebstudio.com` until you turn it off.
