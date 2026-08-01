<!-- VOLLEY-STATE v1 -->
BRIEF-VERSION 1
BRIEF-GENERATED 2026-08-01T02:30Z
BRIEF-COMMIT 4ec69cd
BRIEF-BRANCH main
FACT current_build :: 13 :: eng :: 2026-07-30
FACT staged_build :: none :: eng :: 2026-07-31
FACT friends_signed_in :: 6 :: eng :: 2026-08-01
FACT items_cataloged :: 110 total / 104 confirmed :: eng :: 2026-08-01
FACT invite_reusability :: reusable and uncapped in db, zero durable codes minted :: eng :: 2026-07-31
FACT ranks_closed :: through 18a in a build; 18b and 19 on main, never built :: eng :: 2026-07-31
FACT gate_c_build :: none :: eng :: 2026-07-31
FACT feedback_pipe :: live, 2 rows :: eng :: 2026-07-31
FACT landing_attribution :: live, 11 arrivals logged :: eng :: 2026-08-01
FACT privacy_lending_amendment :: written, not deployed :: eng :: 2026-07-31
FACT gate_c_date :: unset :: gtm :: 2026-07-31
FACT marketing_version :: 1.0.0 held :: gtm :: 2026-07-31
FACT landing_lending_first :: shipped :: gtm :: 2026-07-30
FACT landing_imagery :: real wardrobe cutouts :: gtm :: 2026-07-30
FACT gate_a :: closed :: joint :: 2026-07-21
FACT gate_b :: closed :: joint :: 2026-07-28
NOTE current_build :: this row tracks what the cohort runs, not what exists. Build 13 is 18a-scope — it carries friend connection only, and has no sharing, lendable or borrow controls in it at all
NOTE staged_build :: build 12 was cancelled and never distributed; the next build is the first to carry rank 18b and 19, and has not been cut
NOTE friends_signed_in :: six, not five — c6 joined by referral from c5 on Jul 30 and was not in the original tier-1 list
NOTE items_cataloged :: c1 is 0 captured / 0 confirmed, opened the app 3 times and never took a photo
NOTE items_cataloged :: c2 is 6 captured / 0 confirmed, stalled at the confirm step — 6 photos taken, confirm never pressed once
NOTE items_cataloged :: c3 is 10 confirmed, all in one sitting, then no return in 3 days
NOTE items_cataloged :: c4 is 0 captured / 0 confirmed and has no display name set, so she is invisible in friend lists by design
NOTE items_cataloged :: c5 is 26 confirmed in a single day and is the most active real account — 52 closet opens, 0 wears logged
NOTE items_cataloged :: c6 is 0 captured / 0 confirmed, 2 opens
NOTE items_cataloged :: every cohort member who catalogued anything did it on exactly one day and has not returned to it
NOTE invite_reusability :: migration 0025 is applied in prod and committed; the client half was uncommitted until Jul 31 and is now on main. All 14 existing codes still carry an expiry because get-or-create returns the caller's existing row
NOTE items_cataloged :: 13 item_shares and 6 lendable items now exist, all created by Tate on 2026-08-01 as a deliberate nudge — 3 to c5, 4 to c3, 3 to c2, plus 3 from a demo account. They are real rows and they will appear the moment a build carrying 18b/19 reaches the cohort
NOTE gate_c_build :: NONE OF THE COHORT CAN SEE THOSE SHARES. Build 13 has no FriendCloset screen at all, so a shared piece has no surface to render on. Silence from the cohort is not disinterest, it is an absent screen
NOTE friends_signed_in :: two accounts created 2026-08-01 are Tate's own test rigs on the onvolley.com domain, not cohort members, and are excluded from this count
NOTE gate_c_build :: build 13 was cut from an off-main staged commit that reverted 18b and 19 thirty-two seconds before the build started. Main carries both in full; no build ever has
NOTE feedback_pipe :: in-app door plus the inbox function, both active in prod
NOTE landing_attribution :: arrivals are logged by tag and referrer host with no identifier of any kind; the first post measured end to end is the Jul 30 story set
NOTE privacy_lending_amendment :: the live policy states that sharing a piece is not built and that a friend cannot see any item, and promises to say so there before it ships. It must deploy in the same motion as the first build carrying lending
NOTE gate_b :: recomputed Jul 31 against live data rather than carried forward
OPEN gate_c_build_unshipped :: eng :: no build has ever carried rank 18b or 19, so nothing can be shared or borrowed by anyone; gate C sits behind a build, not behind persuasion
OPEN shares_invisible_to_cohort :: eng :: 13 shares and 6 lendable items exist in prod but no shipped build can display any of them; the nudge cannot land until 18b/19 is in a build
OPEN legacy_invites_expire :: eng :: all 14 invite codes still carry an expiry and the earliest falls on 2026-08-03; 10 are unredeemed and none has been deleted
OPEN invite_page_stale :: eng :: the public invite page still reads that a code works once and expires a week after it was sent, and still has no open-in-app button
OPEN duplicate_migration_0021 :: eng :: two migrations share the number 0021, so ordering is filename luck rather than intent
OPEN privacy_amendment_undeployed :: eng :: the lending amendment is written but not deployed, and the local landing copy is byte-identical to the live page
OPEN cohort_confirm_stall :: eng :: c2 has 6 photos and zero confirms after 3 days; the confirm step is the only place a cohort member has ever stalled
OPEN gate_c_date_unset :: gtm :: no target date is recorded for gate C
SHIPPED 2026-08-01 :: ig13-friendsonly posted as a reel and recorded its first tagged arrival, the first slot measured end to end
SHIPPED 2026-07-31 :: todays-fit no longer invents an outfit for a closet that cannot make one, and one-piece garments now count as whole-body
SHIPPED 2026-07-31 :: client half of reusable invites committed, so prod schema and repo agree again
SHIPPED 2026-07-30 :: migration 0025, reusable per-user invites, uncapped and durable
SHIPPED 2026-07-30 :: migration 0024, campaign arrivals logged by tag and referrer host
SHIPPED 2026-07-30 :: landing page relaunched lending-first with real wardrobe cutouts
FACTCOUNT 16
OPENCOUNT 8
<!-- /VOLLEY-STATE -->

# Volley — project brief

Generated by Claude Code from the repository and the production database. The
block above is the machine-readable half and is defined by the sync contract v1;
everything below it is prose and is ignored by the parser.

## Where things actually stand

**Gate C is behind a build, not behind behaviour.** Rank 18b and 19 — sharing,
lendable, and the borrow loop — are complete on main and self-proven, but no
build has ever carried them. The cohort build was cut from a staged commit that
reverted both, half a minute before the build started, and that revert was never
merged. So the reading that the cohort "won't lend" is unsupported: they have
never had the controls. Zero shares and zero loans is the expected value for a
feature that has not shipped, not a signal about willingness.

**The cohort is engaged, and stops at the same place.** Every member who
catalogued anything did it in one sitting and did not come back to it. One member
has taken photographs and never once pressed confirm. Another has no display name
and is therefore invisible in friend lists — that is the database failing closed
rather than falling back to an email address, which is correct, but it does mean
she cannot be seen by the friend who invited her.

**Two dated hazards.** Every invite code in the system still carries an expiry and
the earliest lands on 2026-08-03; ten of them are unredeemed. And the public
invite page still tells people a code works once and expires in a week, which
stopped being true when reusable invites went in.

**The privacy page has to move with the build.** The live policy does not merely
omit lending — it states that a friend cannot see a single item, and promises to
say so there before it ships rather than after. The amendment is written and not
deployed, and the local copy of the landing page is byte-identical to what is
live, so a deploy today would publish nothing.

## Reading this file

Fetch the raw URL rather than the blob view. Verify both counts before trusting
the contents: the payload declares how many facts and open items it carries, and
a mismatch means the read was lossy and should be refused rather than absorbed.

Cohort members appear only as opaque ids. No name, invite code, key or personal
address appears in this file, and a pre-commit guard blocks the commit if one
ever does.
