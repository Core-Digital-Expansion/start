"""CDE onboarding bootstrap. Public on purpose: contains no secrets.

This is the ONE thing a new team member runs. It clones CDE's two shared repos
into a permanent folder, installs the protocol library and MCP tooling into
YOUR Claude Code, plants the CDE boot loader, and prints a PASS/FAIL checklist.

    python bootstrap.py                 # default location: ~/CDE
    python bootstrap.py --dir ~/work    # somewhere else
    python bootstrap.py --dry-run       # show what would happen, change nothing

Prerequisites you need before running:
  1. Claude Code installed (see the CDE Team Toolkit)
  2. git installed
  3. A GitHub account that has ACCEPTED an invite to the Core-Digital-Expansion
     org. If you haven't got one, ask the account lead first - the clone step
     will fail without it, and this script will tell you so plainly.

Safe to re-run: existing clones are updated, configured tools are skipped.
"""
import argparse
import pathlib
import shutil
import subprocess
import sys

ORG = "Core-Digital-Expansion"
REPOS = ["protocols", "client-state"]
DEFAULT_DIR = pathlib.Path.home() / "CDE"


def say(msg=""):
    print(msg, flush=True)


def die(msg):
    say(f"\nSTOPPED: {msg}")
    sys.exit(1)


def run(args, dry, cwd=None, check_ok=True):
    if dry:
        say(f"  DRY-RUN: {' '.join(str(a) for a in args)}")
        return True
    try:
        p = subprocess.run(args, cwd=cwd, text=True, capture_output=True, timeout=600)
    except Exception as exc:
        if check_ok:
            say(f"  failed: {exc}")
        return False
    if p.returncode != 0 and check_ok:
        tail = (p.stderr or p.stdout or "").strip().splitlines()
        for line in tail[-4:]:
            say(f"    {line}")
    return p.returncode == 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=str(DEFAULT_DIR),
                    help=f"where to put the repos (default: {DEFAULT_DIR})")
    ap.add_argument("--role", default="core", choices=["core", "paid-media", "creative"])
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    dry = args.dry_run

    base = pathlib.Path(args.dir).expanduser().resolve()

    say("== CDE onboarding ==\n")

    # ---- 1. prerequisites --------------------------------------------------
    say("-- Checking prerequisites --")
    if not shutil.which("git"):
        die("git is not installed. Install git, then run this again.")
    say("  ok git")

    if not shutil.which("claude"):
        die("Claude Code is not installed, or not on your PATH.\n"
            "  Install it first (see the CDE Team Toolkit), open a new terminal, "
            "then run this again.")
    say("  ok claude")

    if sys.version_info < (3, 9):
        die(f"Python 3.9+ required (found {sys.version.split()[0]}).")
    say(f"  ok python {sys.version.split()[0]}")

    # ---- 2. clone or update the repos --------------------------------------
    say(f"\n-- Getting the CDE repos into {base} --")
    if not dry:
        base.mkdir(parents=True, exist_ok=True)

    for repo in REPOS:
        target = base / repo
        if (target / ".git").is_dir():
            say(f"  {repo}: already here, updating")
            run(["git", "-C", str(target), "pull", "--ff-only", "-q"], dry, check_ok=False)
            continue
        say(f"  {repo}: cloning")
        url = f"https://github.com/{ORG}/{repo}.git"
        if not run(["git", "clone", "-q", url, str(target)], dry):
            die(f"couldn't clone {repo}.\n"
                f"  This is almost always one of two things:\n"
                f"    1. You haven't accepted a GitHub invite to the {ORG} org yet.\n"
                f"       Ask the account lead to send one, accept the email, re-run this.\n"
                f"    2. Your git isn't signed in to GitHub. Run:  gh auth login\n"
                f"       (or install the GitHub CLI first), then re-run this.")

    protocols = base / "protocols"
    installer = protocols / "tools" / "setup-team-stack.py"
    if not dry and not installer.is_file():
        die(f"expected {installer} but it isn't there. Tell the account lead; "
            "the protocols repo layout may have changed.")

    # ---- 3. hand off to the in-repo installer ------------------------------
    say("\n-- Installing tools, protocols, and the CDE boot loader --")
    verify = protocols / "tools" / "verify-setup.py"
    if dry:
        # Nothing was cloned, so the scripts below don't exist yet. Describe
        # them rather than calling them into a file-not-found error.
        say(f"  DRY-RUN: {installer} --role {args.role}")
        say(f"  DRY-RUN: {verify}")
    else:
        say("   (you may be asked for your own API keys; blank skips any of them)\n")
        subprocess.call([sys.executable, str(installer), "--role", args.role])

        # ---- 4. self-test --------------------------------------------------
        if verify.is_file():
            say("\n-- Checking what worked --")
            subprocess.call([sys.executable, str(verify)])

    say("\n== Done ==")
    say(f"Your CDE repos live in: {base}")
    say("Restart Claude Code, then try:  \"what CDE protocols do you have for paid search?\"")
    say("\nRe-run this any time to update. Ask the account lead if anything above says FAIL.")


if __name__ == "__main__":
    main()
