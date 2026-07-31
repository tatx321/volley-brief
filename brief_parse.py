#!/usr/bin/env python3
"""
brief_parse.py — read a VOLLEY-STATE block and diff it against volley_state.json.

The block is defined by volley_sync_contract.md v1. This script is the enforcing half:
it refuses a read that cannot be trusted rather than absorbing it silently.

Usage:
    python3 brief_parse.py PROJECT-BRIEF.md
    python3 brief_parse.py PROJECT-BRIEF.md --apply     # write eng-owned facts into state
    python3 brief_parse.py PROJECT-BRIEF.md --guard-only   # PRE-PUSH check, no state file needed

--guard-only is the important one for the publishing side: it runs every structural and
secret check and nothing else, so Claude Code can gate the push on it. A leak caught after
the fetch is already public; caught here, it never leaves the machine.

Exit codes:  0 clean · 1 deltas found (informational) · 2 read REFUSED

THIS FILE IS SAFE TO PUBLISH. The cohort first names it checks for are NOT in it —
they live in a sidecar, .cohort_names, which is gitignored and must never be
committed anywhere. A script that carries the denylist inline puts the exact strings
it is defending into the repo it is defending. So: the check ships, the list does not.

The sidecar is mandatory. If it is missing or empty the script refuses rather than
running a name check that silently passes on everything — a guard that cannot fail is
not a guard, and this one runs on a file that is about to become public.
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

STATE = "volley_state.json"
SIDECAR = ".cohort_names"
REQUIRED = {
    "current_build": "eng", "staged_build": "eng", "friends_signed_in": "eng",
    "items_cataloged": "eng", "invite_reusability": "eng", "ranks_closed": "eng",
    "gate_c_build": "eng", "feedback_pipe": "eng", "landing_attribution": "eng",
    "privacy_lending_amendment": "eng",
    "gate_c_date": "gtm", "marketing_version": "gtm",
    "landing_lending_first": "gtm", "landing_imagery": "gtm",
    "gate_a": "joint", "gate_b": "joint",
}
# Patterns that must never appear in a public brief. Detection is coarse on purpose:
# a false positive costs one question, a false negative costs a leaked credential.
FORBIDDEN = [
    # Invite codes are mixed-case alphanumeric, 10-14 chars. Requiring all three of
    # lower/upper/digit is what separates a code from a word like UNCOMMITTED.
    (r"\b(?=[A-Za-z0-9]{10,14}\b)(?=[A-Za-z0-9]*[a-z])(?=[A-Za-z0-9]*[A-Z])"
     r"(?=[A-Za-z0-9]*\d)[A-Za-z0-9]{10,14}\b", "something that looks like an invite code"),
    # Body allows - and _ so sk-live-xxxx and ghp_xxx-yyy are both caught.
    (r"\b(?:sk|pk|ghp|gho|xox[bpa])[-_][A-Za-z0-9_-]{8,}", "something that looks like an API key or token"),
    (r"REVIEW_CODE", "the review-signin bypass code"),
    (r"\b[\w.+-]+@(?!onvolley\.com)[\w-]+\.[\w.]+\b", "a personal email address"),
]
BEGIN, END = "<!-- VOLLEY-STATE v1 -->", "<!-- /VOLLEY-STATE -->"


class Refused(Exception):
    pass


def load_denylist():
    """Read the cohort first names from the gitignored sidecar.

    Looked for beside this script first, then in the working directory. One name per
    line; blank lines and # comments ignored; case is irrelevant at match time.

    Fails closed on purpose. A missing sidecar is not 'no names to check' — it is 'the
    name check did not run', and the two are indistinguishable from the exit code
    unless we refuse. On the publishing side that distinction is the whole ballgame.
    """
    here = Path(__file__).resolve().parent
    looked = list(dict.fromkeys([here / SIDECAR, Path.cwd().resolve() / SIDECAR]))
    for cand in looked:
        if cand.is_file():
            names = []
            for raw in cand.read_text(encoding="utf-8").splitlines():
                line = raw.split("#", 1)[0].strip()
                if line:
                    names.append(line.lower())
            if not names:
                raise Refused(
                    f"{cand} is present but empty — the cohort name check cannot run. "
                    "Populate it (one first name per line) or the guard is decorative")
            return names
    raise Refused(
        f"no {SIDECAR} sidecar (looked in {', '.join(str(p.parent) for p in looked)}) — the "
        f"cohort name check cannot run, so this file is unverified. Create {SIDECAR} (one first "
        f"name per line, gitignored, never committed) and re-run")


def extract(text):
    if BEGIN not in text or END not in text:
        raise Refused("no VOLLEY-STATE v1 block found — the brief does not follow the contract")
    return text.split(BEGIN, 1)[1].split(END, 1)[0]


def parse(block):
    head, facts, notes, opens, shipped = {}, {}, {}, [], []
    for raw in block.splitlines():
        line = raw.strip()
        if not line:
            continue
        key, _, rest = line.partition(" ")
        if key in ("BRIEF-VERSION", "BRIEF-GENERATED", "BRIEF-COMMIT", "BRIEF-BRANCH",
                   "FACTCOUNT", "OPENCOUNT"):
            head[key] = rest.strip()
        elif key == "FACT":
            p = [x.strip() for x in rest.split("::")]
            if len(p) != 4:
                raise Refused(f"malformed FACT line (want 4 fields, got {len(p)}): {line[:70]}")
            facts[p[0]] = {"value": p[1], "owner": p[2], "as_of": p[3]}
        elif key == "NOTE":
            i, _, t = rest.partition("::")
            notes.setdefault(i.strip(), []).append(t.strip())
        elif key == "OPEN":
            p = [x.strip() for x in rest.split("::")]
            if len(p) != 3:
                raise Refused(f"malformed OPEN line (want 3 fields, got {len(p)}): {line[:70]}")
            opens.append({"id": p[0], "owner": p[1], "text": p[2]})
        elif key == "SHIPPED":
            d, _, t = rest.partition("::")
            shipped.append({"date": d.strip(), "text": t.strip()})
    return head, facts, notes, opens, shipped


def verify(head, facts, opens, block):
    """Every check here is a refusal, not a warning. A brief we half-trust is worse than none."""
    if head.get("BRIEF-VERSION") != "1":
        raise Refused(f"unknown BRIEF-VERSION {head.get('BRIEF-VERSION')!r} — this parser speaks v1")
    for need in ("BRIEF-GENERATED", "BRIEF-COMMIT", "FACTCOUNT", "OPENCOUNT"):
        if need not in head:
            raise Refused(f"missing {need} — cannot establish provenance or completeness")

    # Self-verifying payload: the fetch path may silently drop lines.
    if int(head["FACTCOUNT"]) != len(facts):
        raise Refused(f"FACTCOUNT says {head['FACTCOUNT']}, {len(facts)} arrived — the read is lossy, "
                      "ask for a paste instead")
    if int(head["OPENCOUNT"]) != len(opens):
        raise Refused(f"OPENCOUNT says {head['OPENCOUNT']}, {len(opens)} arrived — the read is lossy")

    missing = [k for k in REQUIRED if k not in facts]
    if missing:
        raise Refused("required fact ids absent (a missing row is an unknown, not 'no news'): "
                      + ", ".join(missing))
    for fid, spec in facts.items():
        want = REQUIRED.get(fid)
        if want and spec["owner"] != want:
            raise Refused(f"{fid} is declared owner={spec['owner']} but the contract says {want}")

    for pat, why in FORBIDDEN:
        m = re.search(pat, block, re.I)
        if m:
            raise Refused(f"the brief contains {why} ({m.group(0)[:14]}…) — "
                          "this file is public; strip it before pushing")
    for name in load_denylist():
        if re.search(rf"\b{re.escape(name)}\b", block, re.I):
            raise Refused(f"a cohort member is named in a public brief ('{name}') — use opaque ids")


def freshness(head, state):
    """A brief older than what we already hold is not an update; reading it would move us backwards."""
    try:
        gen = datetime.fromisoformat(head["BRIEF-GENERATED"].replace("Z", "+00:00"))
    except ValueError:
        raise Refused(f"BRIEF-GENERATED {head['BRIEF-GENERATED']!r} is not ISO 8601 UTC")
    if gen > datetime.now(timezone.utc):
        raise Refused("BRIEF-GENERATED is in the future — the clock or the stamp is wrong")
    return gen


def diff(facts, state):
    local = {f["id"]: f for f in state["facts"]}
    changed, unknown = [], []
    for fid, spec in facts.items():
        if fid not in local:
            unknown.append(fid)
        elif str(local[fid].get("value", "")).strip() != spec["value"]:
            changed.append((fid, str(local[fid].get("value", "")), spec["value"], spec["owner"]))
    absent = [k for k in local if k not in facts]
    return changed, unknown, absent


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    path = args[0] if args else "PROJECT-BRIEF.md"
    apply_ = "--apply" in sys.argv
    guard_only = "--guard-only" in sys.argv

    # --guard-only runs on the publishing side, where volley_state.json does not exist.
    if guard_only:
        try:
            # Sidecar first: if the name check can't run, don't bother reading the file.
            names = load_denylist()
            block = extract(open(path, encoding="utf-8").read())
            head, facts, notes, opens, shipped = parse(block)
            verify(head, facts, opens, block)
            freshness(head, None)
        except Refused as e:
            print(f"BLOCKED — {e}")
            print("do not push. this file would be public.")
            return 2
        print(f"guard ok · {len(facts)} facts · {len(opens)} open · {len(names)} cohort names "
              "checked · no names, codes or keys found · safe to push")
        return 0

    try:
        state = json.load(open(STATE))
    except FileNotFoundError:
        print(f"READ REFUSED — no {STATE} here, so there is nothing to diff against. Run this "
              f"beside local state, or use --guard-only if you meant the pre-push check.")
        return 2

    try:
        block = extract(open(path, encoding="utf-8").read())
        head, facts, notes, opens, shipped = parse(block)
        verify(head, facts, opens, block)
        gen = freshness(head, state)
    except Refused as e:
        print(f"READ REFUSED — {e}")
        print("state untouched. do not propagate; ask for a paste or a corrected push.")
        return 2

    print(f"brief ok · {head['BRIEF-COMMIT']} on {head.get('BRIEF-BRANCH','?')} · "
          f"generated {gen:%Y-%m-%d %H:%MZ} · {len(facts)} facts · {len(opens)} open")
    print(f"local state as_of: {state.get('as_of','?')}\n")

    changed, unknown, absent = diff(facts, state)
    if not (changed or unknown or absent):
        print("no deltas — local state already agrees with the repo.")
    for fid, old, new, owner in changed:
        arrow = "brief wins" if owner == "eng" else "CONFLICT — surface, do not auto-resolve"
        print(f"  ~ {fid} [{owner}] {arrow}\n      local: {old[:88]}\n      brief: {new[:88]}")
    for fid in unknown:
        print(f"  + {fid} — in the brief, not tracked locally")
    for fid in absent:
        print(f"  ? {fid} — tracked locally, absent from the brief")

    if shipped:
        print("\nshipped since last brief:")
        for s in shipped:
            print(f"  · {s['date']} {s['text']}")
    if opens:
        print("\nopen:")
        for o in sorted(opens, key=lambda x: x["owner"]):
            print(f"  · [{o['owner']}] {o['id']} — {o['text']}")

    if apply_:
        # Only eng-owned rows are written. gtm rows are decisions of record and are
        # never overwritten by a fetch — a disagreement there is reported, not resolved.
        local = {f["id"]: f for f in state["facts"]}
        n = 0
        for fid, old, new, owner in changed:
            if owner == "eng":
                local[fid]["value"] = new
                n += 1
        state["facts"] = list(local.values())
        state["as_of"] = f"{gen:%b %d} (fetched from {head['BRIEF-COMMIT']})"
        json.dump(state, open(STATE, "w"), indent=1, ensure_ascii=False)
        print(f"\napplied {n} eng-owned facts to {STATE}. now edit artifacts, then run sync_check.py.")

    return 1 if (changed or unknown or absent) else 0


if __name__ == "__main__":
    sys.exit(main())
