# start

New at CDE? You're in the right place. This gets your Claude set up with CDE's tools, workflows, and client context.

## Before you start

You need three things:

1. **Claude Code installed.** See the CDE Team Toolkit.
2. **git installed.** On a Mac, running `git --version` in Terminal will offer to install it.
3. **A GitHub invite to `Core-Digital-Expansion`, accepted.** Check your email. If you don't have one, ask the account lead before going further, because step 2 below needs it.

## Setup (two commands)

On Windows, type `python` wherever this page says `python3`.

```bash
git clone https://github.com/Core-Digital-Expansion/start.git
```

```bash
python3 start/bootstrap.py
```

That's it. It will:

- put CDE's two shared repos in a permanent folder (`~/CDE` by default)
- install the full CDE protocol library into your Claude, so you can ask for any of our workflows by name
- connect the standard tool set (browser automation, Google Drive, image generation, and so on), pausing to ask for your own logins where a tool needs one
- tell your Claude what CDE is, so it has the context in every folder, not just this one
- keep itself up to date from then on
- finish by printing a checklist of what worked and what still needs your login

You can re-run it any time. It skips whatever is already done.

**Want it somewhere other than `~/CDE`?** `python3 start/bootstrap.py --dir ~/wherever`

**Run ad accounts?** `python3 start/bootstrap.py --role paid-media` adds the Google Ads setup guide. Designers use `--role creative`.

## After setup

Restart Claude Code, then try asking it something like *"what CDE protocols do you have for paid search?"* or *"give me the account guide for Ten Thousand."* If it knows what you're talking about, you're set.

## If something says FAIL

Re-run `python3 ~/CDE/protocols/tools/setup-team-stack.py` first, since that fixes most things. To see the checklist again on its own:

```bash
python3 ~/CDE/protocols/tools/verify-setup.py
```

Still stuck, or a repo wouldn't clone? That's almost always a GitHub access problem. Ask the account lead.

## What's in here

Only this bootstrap script. It holds no credentials and no client information, which is why it can be public. Everything confidential lives in the two private repos it clones for you.
