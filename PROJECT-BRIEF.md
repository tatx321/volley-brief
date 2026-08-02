<!-- VOLLEY-STATE v1 -->
BRIEF-VERSION 1
BRIEF-GENERATED 2026-08-02T01:05Z
BRIEF-COMMIT 2c25b3f
BRIEF-BRANCH main
FACT current_build :: 14 :: eng :: 2026-08-01
FACT staged_build :: none — 14 is the current build :: eng :: 2026-08-01
FACT friends_signed_in :: 6 :: eng :: 2026-08-01
FACT items_cataloged :: 123 total / 122 confirmed :: eng :: 2026-08-01
FACT invite_reusability :: reusable and uncapped; 2 durable codes minted, 9 legacy still expiring :: eng :: 2026-08-01
FACT ranks_closed :: through 19 — 18b and 19 shipped in build 14 :: eng :: 2026-08-01
FACT gate_c_build :: 14 :: eng :: 2026-08-01
FACT feedback_pipe :: live, 2 rows :: eng :: 2026-07-31
FACT landing_attribution :: live, 19 arrivals logged :: eng :: 2026-08-01
FACT privacy_lending_amendment :: deployed and verified live :: eng :: 2026-08-01
FACT gate_c_date :: unset :: gtm :: 2026-07-31
FACT marketing_version :: 1.0.0 held :: gtm :: 2026-07-31
FACT landing_lending_first :: shipped :: gtm :: 2026-07-30
FACT landing_imagery :: real wardrobe cutouts :: gtm :: 2026-07-30
FACT gate_a :: closed :: joint :: 2026-07-21
FACT gate_b :: closed :: joint :: 2026-07-28
NOTE staged_build :: build 14 was cut from main at 17:41 on Jul 31 and DOES carry 18b/19 — AtTheNet, FriendCloset and lib/social were all present in the tree at that commit, verified rather than assumed. The moment it clears review and the cohort updates, the 13 waiting shares become visible and gate C is one borrow away
NOTE friends_signed_in :: six, not five — c6 joined by referral from c5 on Jul 30 and was not in the original tier-1 list
NOTE items_cataloged :: c1 is 0 captured / 0 confirmed, opened the app 3 times and never took a photo
NOTE items_cataloged :: c2 is 6 captured / 0 confirmed, stalled at the confirm step — 6 photos taken, confirm never pressed once
NOTE items_cataloged :: c3 is 10 confirmed, all in one sitting, then no return in 3 days
NOTE items_cataloged :: c4 is 0 captured / 0 confirmed and has no display name set, so she is invisible in friend lists by design
NOTE items_cataloged :: c5 is 26 confirmed in a single day and is the most active real account — 52 closet opens, 0 wears logged
NOTE items_cataloged :: c6 is 0 captured / 0 confirmed, 2 opens
NOTE items_cataloged :: every cohort member who catalogued anything did it on exactly one unbroken sitting, and nobody has ever catalogued on a second calendar day. But FOUR of six did return on a later day — they returned without cataloguing. And that sitting is not necessarily the first: c1 signed in 07-28 and took her first photo on 08-01, four days later
NOTE invite_reusability :: migration 0025 is applied in prod and committed; the client half was uncommitted until Jul 31 and is now on main. All 14 existing codes still carry an expiry because get-or-create returns the caller's existing row
NOTE items_cataloged :: 13 item_shares and 6 lendable items now exist, all created by Tate on 2026-08-01 as a deliberate nudge — 3 to c5, 4 to c3, 3 to c2, plus 3 from a demo account. They are real rows and they will appear the moment a build carrying 18b/19 reaches the cohort
NOTE friends_signed_in :: two accounts created 2026-08-01 are Tate's own test rigs on the onvolley.com domain, not cohort members, and are excluded from this count
NOTE current_build :: SETTLED 2026-08-02 by Tate against App Store Connect — build 14 is on ALL SIX cohort phones, not just Tate's. It is the first build ever to carry sharing, lendable and the borrow loop. Every repo-side inference to the contrary (docs/status/2026-08-01.md, docs/build-riders.md, the commit record showing no approval) reasoned from ABSENCE OF DATA and was wrong; no event carries app version, so telemetry could never have settled it and direct observation is the only authority here
NOTE gate_c_build :: CORRECTED — every lendable item belongs to Tate (6) or to Ada, the App Review seed (2). ZERO are owned by a cohort member, and the 13 shares are Tate's outbound nudge. Under Tate's own founder exclusion a borrow he is party to does not close the gate, so gate C is arithmetically impossible today regardless of build state
NOTE gate_c_build :: with build 14 confirmed on all six phones, the zero is now BEHAVIOURAL and readable. No cohort member has ever fired friend_closet_opened, item_shared or lendable_set — all 16, 13 and 8 belong to Tate — and four of the six could have. c1 had 3 shared pieces land 9 minutes before she stopped a 32-minute session; c5 opened the app for 17 seconds with 3 pieces waiting and went to Today's Fit instead. Availability is not adoption, and this is the first metric in the product's life that separates she-does-not-want-to from she-never-looked
NOTE gate_c_build :: build 13 was cut from an off-main staged commit that reverted 18b and 19 thirty-two seconds before the build started. Main carries both in full; no build ever has
NOTE feedback_pipe :: in-app door plus the inbox function, both active in prod
NOTE landing_attribution :: arrivals are logged by tag and referrer host with no identifier of any kind; the first post measured end to end is the Jul 30 story set
NOTE privacy_lending_amendment :: the live policy states that sharing a piece is not built and that a friend cannot see any item, and promises to say so there before it ships. It must deploy in the same motion as the first build carrying lending
NOTE gate_b :: recomputed Jul 31 against live data rather than carried forward
OPEN legacy_invites_expire :: eng :: 9 unredeemed codes still carry an expiry, the earliest on 2026-08-03; two durable codes now exist. Tapping Invite friends promotes the newest to never-expiring
OPEN gate_c_no_eligible_lender :: joint :: gate C cannot close today. No cohort member owns a single lendable item — all 8 belong to Tate or the App Review seed — and a borrow Tate is party to does not qualify. The path is c5 marking one piece lendable and sharing it with c6; it needs a conversation, not code
OPEN cohort_confirm_stall :: eng :: c2 has 6 photos and zero confirms after 3 days, and c1 independently reported the same seam in words — capture to closet takes two screens and she called it unintuitive. Two of six on the same handoff is a pattern, not an anecdote
OPEN feedback_pipe_empty :: eng :: the in-app feedback door has never delivered a real submission; the table holds only two test rows and app_feedback_sent has never fired from any device, including c1 who says she used it
OPEN gate_c_date_unset :: gtm :: no target date is recorded for gate C
SHIPPED 2026-08-01 :: build 14 reached the cohort — sharing, lendable and the borrow loop in a shipped build for the first time
SHIPPED 2026-08-01 :: welcome email v2 deployed the moment build 14 landed, so 'and you can lend now' was never false in an inbox
SHIPPED 2026-08-01 :: tag-items auto-admit — a usable piece enters the closet without a review tap; only a missing cutout or a removal fallback holds one back
SHIPPED 2026-08-01 :: c2's six stranded pieces admitted and a mis-oriented cutout corrected, giving her a working closet and a first outfit
SHIPPED 2026-08-01 :: c1 activated — 13 confirmed pieces in about thirty minutes, camera only, connected mid-session, welcome email delivered at 03:53Z. Third activated member
SHIPPED 2026-08-01 :: privacy lending amendment deployed and verified live, ahead of the first build carrying lending
SHIPPED 2026-08-01 :: ig13-friendsonly posted as a reel and recorded its first tagged arrival, the first slot measured end to end
SHIPPED 2026-07-31 :: todays-fit no longer invents an outfit for a closet that cannot make one, and one-piece garments now count as whole-body
SHIPPED 2026-07-31 :: client half of reusable invites committed, so prod schema and repo agree again
SHIPPED 2026-07-30 :: migration 0025, reusable per-user invites, uncapped and durable
SHIPPED 2026-07-30 :: migration 0024, campaign arrivals logged by tag and referrer host
SHIPPED 2026-07-30 :: landing page relaunched lending-first with real wardrobe cutouts
FACTCOUNT 16
OPENCOUNT 5
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
