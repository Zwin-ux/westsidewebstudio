"""Render app links from apps.json into the site's HTML.

Usage:
  python scripts/build.py              # update the HTML in place
  python scripts/build.py --out _site  # write a deployable copy to _site
  python scripts/build.py --set masri appstore https://apps.apple.com/app/id123

status is one of:
  testing     private, no public link (stamp opens the app's page)
  testflight  public beta (stamp opens the TestFlight link)
  appstore    released (stamp opens the App Store listing)
"""
import argparse, html, io, json, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATUSES = {"testing": "In testing", "testflight": "TestFlight beta", "appstore": "On the App Store"}
LINK_RULES = {
    "testflight": re.compile(r"^https://testflight\.apple\.com/join/[A-Za-z0-9]+$"),
    "appStore": re.compile(r"^https://apps\.apple\.com/[a-z/]*app/[^\s]*id\d+(\?[^\s]*)?$"),
    "site": re.compile(r"^https://[^\s]+$"),
}
MARKER = re.compile(r"<!-- app:([a-z0-9-]+):([a-z]+) -->.*?<!-- /app -->", re.S)
SKIP = {".git", ".github", "scripts", "_site", "apps.json", "README.md", "DNS.md"}


def validate(data):
    errors = []
    for app in data["apps"]:
        status = app.get("status")
        if status not in STATUSES:
            errors.append(f"{app['id']}: status must be one of {', '.join(STATUSES)}")
        for field, rule in LINK_RULES.items():
            value = app.get(field, "")
            if value and not rule.match(value):
                errors.append(f"{app['id']}: {field} doesn't look right: {value}")
        if status == "testflight" and not app.get("testflight"):
            errors.append(f"{app['id']}: status is testflight but there's no testflight link")
        if status == "appstore" and not app.get("appStore"):
            errors.append(f"{app['id']}: status is appstore but there's no appStore link")
    if errors:
        sys.exit("apps.json:\n  " + "\n  ".join(errors))
    return data


def primary_link(app):
    if app["status"] == "appstore":
        return app["appStore"]
    if app["status"] == "testflight":
        return app["testflight"]
    return app["page"]


def render(app, field, depth):
    """depth: '' for the home page, '../' for a page one folder down."""
    e = html.escape
    if field == "status":
        return e(STATUSES[app["status"]])
    if field == "stamp":
        href = primary_link(app)
        if not href.startswith("https://"):
            href = depth + href
        return f'''<a class="app-stamp" href="{e(href)}">
            <div class="stamp-paper"><div class="stamp-face">
              <span class="stamp-corner">iOS</span>
              <img src="{depth}{e(app['icon'])}" width="84" height="84" alt="">
              <span class="stamp-name">{e(app['name'])}</span>
              <span class="stamp-note">{e(STATUSES[app['status']])}</span>
            </div></div>
          </a>'''
    if field == "cta":
        links = []
        if app["status"] == "appstore":
            links.append(f'<a class="btn" href="{e(app["appStore"])}">Get it on the App Store</a>')
        elif app["status"] == "testflight":
            links.append(f'<a class="btn" href="{e(app["testflight"])}">Join the TestFlight beta</a>')
        if app.get("site"):
            links.append(f'<a class="textlink" href="{e(app["site"])}">{e(app["name"])} site</a>')
        return "\n          ".join(links)
    raise ValueError(f"unknown field {field}")


def render_tree(root, apps):
    for page in root.rglob("*.html"):
        rel = page.relative_to(root)
        if rel.parts[0] in SKIP:
            continue
        depth = "../" * (len(rel.parts) - 1)
        text = page.read_text(encoding="utf-8")

        def sub(m):
            app_id, field = m.group(1), m.group(2)
            if app_id not in apps:
                sys.exit(f"{rel}: no app '{app_id}' in apps.json")
            return f"<!-- app:{app_id}:{field} -->{render(apps[app_id], field, depth)}<!-- /app -->"

        new = MARKER.sub(sub, text)
        if new != text:
            io.open(page, "w", encoding="utf-8", newline="\n").write(new)
            print(f"updated {rel}")


def set_app(data, app_id, status, url):
    app = next((a for a in data["apps"] if a["id"] == app_id), None)
    if not app:
        sys.exit(f"no app '{app_id}' in apps.json")
    app["status"] = status
    if url:
        app["appStore" if status == "appstore" else "testflight"] = url


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--set", nargs="+", metavar=("APP", "STATUS"))
    args = ap.parse_args()
    path = ROOT / "apps.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if args.set:
        set_app(data, args.set[0], args.set[1], args.set[2] if len(args.set) > 2 else "")
    data = validate(data)
    if args.set:
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    apps = {a["id"]: a for a in data["apps"]}
    root = ROOT
    if args.out:
        root = Path(args.out).resolve()
        if root.exists():
            shutil.rmtree(root)
        shutil.copytree(ROOT, root, ignore=lambda d, names: [n for n in names if Path(d) == ROOT and n in SKIP])
    render_tree(root, apps)


if __name__ == "__main__":
    main()
