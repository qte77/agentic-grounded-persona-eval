# Groundwork (sortmy.london) — Findings

## §Research

Scope per `target.md`: evidence for the four civic-wayfinding workflows only (Sort My
Care, Sort My Wander, Sort My Food Hygiene, Sort My Scam Check) — the bundled Founder's Copilot
workflow is explicitly out of scope for this run. Geographic scope: London/UK, weighted toward
UK-specific general-public sources over generic startup-community sources, per the same file.

### Source coverage

What was tried, and what actually happened — not assumed:

- **Reddit (r/london, r/AskUK, r/CasualUK)** — target.md's *preferred* source set. **Blocked on
  every tier tried, including the method's own designated fetch tool**, ruling out a
  single-tool artifact:
  - `WebFetch` on `www.reddit.com` and `old.reddit.com` (both a subreddit front page and a
    `/search.json` endpoint) returned "Claude Code is unable to fetch from `<host>`" — a
    tool-level refusal for the reddit.com domain, not a 404 or empty result.
  - A direct `python3`/`urllib` request (bypassing the WebFetch tool entirely, run from this same
    runner) to `www.reddit.com`, bare `reddit.com`, and `old.reddit.com` search-JSON endpoints all
    returned `HTTP 403: Blocked`.
  - **`polyfetch-scrape` itself** (used from a local sibling clone via `uv run --directory
    ../polyfetch-scrape polyfetch fetch <url> --json`, its stealth-Patchright tier, the method's
    own designated tool for exactly this situation) was tried against two independent endpoints —
    `old.reddit.com/r/london/search.json?q=NHS+111` and
    `www.reddit.com/r/AskUK/search.json?q=food+hygiene+rating` — and both returned a genuine
    `FingerprintBlock` (`status=403` after 3 internal retries each).
  - Three independent tools, two subreddits, one consistent result: **Reddit's own edge is
    fingerprint-blocking this runner's network specifically**, not any one tool's limitation. This
    is a fact about this runner's network, not evidence that Londoners don't discuss these pain
    points on Reddit. No Reddit content — positive or negative — appears below; treat r/london,
    r/AskUK, r/CasualUK as unsearched, not as searched-and-empty. A future run from a different
    network/residential exit could still reasonably retry them.
- **`polyfetch-scrape`** — the spec's designated fetch tool for anything needing an actual browser
  fetch. Not installed globally on this runner (`which polyfetch` → not found), but a **local
  sibling clone was available at `../polyfetch-scrape/`** and directly usable env-borrowed, per its
  own `USING.md`: `uv run --directory ../polyfetch-scrape polyfetch fetch <url> --json` — no
  install into this repo needed, no network fetch of the tool itself required. This wasn't
  identified until partway through this run; `WebFetch`/`WebSearch` were used as the initial
  substitute for most of Phase 1 (with the paraphrase-risk caveat below), and the sibling clone was
  used directly to re-verify the Reddit block once found (see the Reddit bullet above) and by Phase
  3's live-evaluator runs (which additionally needed `patchright install chromium` inside that
  clone, or reused a venv another instance built, for `render_session()`). For a future run:
  **check for a local sibling clone first** — it's faster and more reliable than installing from
  GitHub into an isolated venv.
- **Hacker News (Algolia search API)** — reachable and queried (`hn.algolia.com/api/v1/search`,
  `tags=story`) for "food hygiene rating london" (0 hits, empty result set — genuinely empty, not
  blocked) and "which NHS service to use" (13 fuzzy/typo-tolerant hits, all irrelevant — hosting,
  DNS, GPU-cluster, YC-launch stories with no connection to this ICP). Confirms target.md's own
  expectation: HN's audience is not this product's ICP. No HN quotes appear below because none
  were on-topic, not because the API failed.
- **ProductHunt GraphQL API** — not attempted. Requires a self-serve `developer_token` from a PH
  account's API dashboard; no such credential is available in this environment/run.
- **Trustpilot** — not queried this run. Groundwork is a new/indie civic tool with no established
  review footprint, and target.md scopes this run to pain-point evidence (how the ICP talks about
  the underlying problems), not product reviews of Groundwork itself, which don't yet exist.
- **UK forums that *did* work** — MoneySavingExpert Forums (`forums.moneysavingexpert.com`) and
  Mumsnet (`mumsnet.com/talk`) were fetchable directly via `WebFetch` and yielded the sourced
  quotes below. These are not in target.md's example list (r/london, r/AskUK, r/CasualUK) but are
  UK-specific, general-public (non-tech) communities squarely on-ICP for "budget-conscious
  Londoners/residents navigating civic and consumer-trust questions" — used as the closest
  available substitute once Reddit proved unreachable.
- **FCA (fca.org.uk)** — the UK financial regulator's own press release on "clone firm" investment
  scams was fetched directly as a primary corroborating source for the scam-check pattern (not a
  forum, but a first-party account of the exact problem, including a named victim's direct quote).
- **Caveat on all quotes below:** they were extracted via `WebFetch`, which runs a small model over
  each page rather than returning raw HTML/JSON. The prompt in every case explicitly requested
  verbatim text, and quotes came back inside quotation marks with matching usernames/timestamps —
  but this is a paraphrase-risk substitute for a raw fetch, not raw HTML captured directly. If a
  reader needs byte-exact text, re-fetch the URL directly.

---

### Pattern 1 — Non-emergency NHS routing is genuinely unclear, and the "safe" answer (111) is
distrusted for over-referring

Relevant to: **Sort My Care**.

> "Don't personally need to go but like to know these things just in case as I have accidents
> prone relatives."
> — Coldnights, opening post of thread titled "Do you need to ring the gp or 111 to go to a&e",
> [Mumsnet](https://www.mumsnet.com/talk/_chat/4037500-Do-you-need-to-ring-the-gp-or-111-to-go-to-a-e), 29 Sep 2020

> "In some areas there's a pilot trialling phoning 111 before going to a and e. If you're not in
> one of those areas and you need to go to a and e, you just go."
> — PurpleDaisies, reply on the same thread, [Mumsnet](https://www.mumsnet.com/talk/_chat/4037500-Do-you-need-to-ring-the-gp-or-111-to-go-to-a-e), 29 Sep 2020

> "I know they need to stay on the safe side but i feel like it's their response to everything,
> which sort of defeats the purpose a little bit."
> — riotlady, [Mumsnet — "Has anyone ever called 111 and NOT been told to go to A and E?"](https://www.mumsnet.com/talk/am_i_being_unreasonable/3476795-Has-anyone-ever-called-111-and-NOT-been-told-to-go-to-A-and-E), 12 Jan 2019

**What this means for the product:** the pattern isn't just "people don't know the routing rules"
(111 vs. GP vs. A&E) — it's that the rules themselves are inconsistently applied by region and the
routing service's own advice is seen as reflexively over-cautious ("their response to everything").
A tool like Sort My Care has to both explain the *stated* pathway and be honest that real-world
practice varies — a single confident answer that doesn't acknowledge that variance risks reading as
naive to exactly the users who've been burned by it. Caveat: this pattern's evidence is 2019–2020
vintage (one thread references a since-possibly-changed COVID-era 111-before-A&E pilot) while the
other three patterns draw on 2021–2025 evidence — the underlying confusion is plausibly still
current, but the specific routing mechanics described may have shifted since these threads were
posted; treat the mechanics as illustrative, not as a current NHS-pathway reference.

---

### Pattern 2 — Visitors and budget-conscious residents default to asking a community for a
curated "free things to do" list rather than researching solo

Relevant to: **Sort My Wander**.

> "We're finally taking the kids (13 & 9) to London for a few nights, but our budget isn't as
> healthy as our enthusiasm! We're staying in a hostel in Bayswater and we'll do plenty of
> wandering and looking at the obvious sites, but I'm hoping for recommendations for cheap or free
> things to do that may be a little different."
> — HowManyMoreTimes, [Mumsnet — "London on a budget"](https://www.mumsnet.com/talk/_chat/4558161-london-on-a-budget), 28 May 2022

> "You're in luck because all the major galleries and museums are free."
> — BigGreen, reply on the same thread, [Mumsnet](https://www.mumsnet.com/talk/_chat/4558161-london-on-a-budget), 28 May 2022

> "My brother and I (20s) are going to London in November to watch the football...we need
> something free to do on the Saturday afternoon."
> — itwasnevermine, [Mumsnet — "Free things to do in London?!"](https://www.mumsnet.com/talk/_chat/5180051-free-things-to-do-in-london), 4 Oct 2024

**What this means for the product:** the recurring behavior is *asking a community for a
pre-filtered shortlist* rather than searching an official listings site — the same few answers
(free museums, markets) get re-supplied thread after thread by other users, years apart, which
suggests the official "what's free in London" information exists but isn't the first
place people look. Sort My Wander's opportunity is being the thing people ask instead of posting a
new thread — but it's competing with "just ask a forum," which costs nothing and gets a
human-vetted answer.

---

### Pattern 3 — Real, financially-costly anxiety about whether an unfamiliar firm is a scam or a
clone of a legitimate one, checked *before* — and sometimes only discovered *after* — money moves

Relevant to: **Sort My Scam Check**.

> "Ive just received 2 texts in quick succession from M&S Bank giving me 2 different 6 digit
> security codes. However I don't have any bank or credit card accounts with M&S. Should I be
> concerned? I tried to ring them but because I don't have any account number I just keep going
> round in circles...."
> — topcat105, [MoneySavingExpert Forum — thread on suspicious M&S Bank texts](https://forums.moneysavingexpert.com/discussion/6652245/is-this-a-scam), 26 Jan, year unconfirmed — this thread's timestamps show no year (just "26 January at H:MMPM"), unlike a separately-checked, lower-numbered thread on the same forum (discussion 6637969) which does show a full year ("4 November 2025"). Two independent signals both point to this being the more recent of the two — the higher discussion ID, and forums commonly dropping the year only for current-year posts — consistent with Jan 2026, but neither is a page-confirmed date for this specific thread

> "So I just wanted to share my experiance, regarding a scale that has been started with payday
> loan companies and to warn people in the future about the signs. ... I signed up for a payday
> loan about a month ago... requested a chargeback of 14p through my banking app, which I thought
> was to verify what was needed. ... Fast forward a month and I have a payment of £29.50 taken out
> of my account from a company called onsavings, never heard of them... I called them and before I
> could even say anything the agent started with 'I assume you are here to cancel?'... They are
> praying on vulnerable people who are desperate."
> — Huhcally, [MoneySavingExpert Forum — "Onsavings.co.uk - Scam"](https://forums.moneysavingexpert.com/discussion/6450280/onsavings-co-uk-scam), 1 Jun 2023 3:32PM (sic on "experiance"/"scale" — reproduced as posted, not corrected)

> "Clone investment scams can look real and sophisticated but anyone can spot them by following our
> advice... When it comes to clones, I cannot emphasise enough how important it is to double check
> every detail."
> — Mark Steward, FCA Executive Director of Enforcement and Market Oversight, [FCA — "FCA issues warning over 'clone firm' investment scams"](https://www.fca.org.uk/news/press-releases/fca-scamsmart-warning-clone-firm-investment-scams), 27 Jan 2021

> "I really thought I'd be able to spot a scam, but now I know they can be far more sophisticated
> than I had ever imagined."
> — Janet from Chester (scam victim quoted in the release), [FCA press release, same URL](https://www.fca.org.uk/news/press-releases/fca-scamsmart-warning-clone-firm-investment-scams), 27 Jan 2021

**What this means for the product:** this is the strongest-evidenced pattern of the four — it spans
a real forum poster unable to verify a text message through official channels, a real poster who
was charged after the fact by a firm they didn't realize they'd agreed to pay, and the UK's own
financial regulator confirming the mechanism (clone firms convincingly imitating real ones) at
scale (the FCA release states "consumers reported losses of more than £78 million between
January-December 2020," averaging £45,242 per victim). The felt need is a
*quick, low-friction check before proceeding* — topcat105 gave up trying to verify through the
official channel because it required information they didn't have. A tool that turns "is this
legit" into one input, one official-source-backed answer, is answering a need that currently ends
in "I tried to ring them... I just keep going round in circles" or discovering the charge a month
later.

---

### Pattern 4 — Food hygiene ratings matter enough to set a personal cutoff, but checking them
"before, not after" is inconsistent and access is a known blocker for a meaningful minority

Relevant to: **Sort My Food Hygiene**.

> "I'm bemused by a Facebook thread where locals have recommended restaurants which I know to have
> a food hygiene rating of 3. Do they not know? Do they not care? Is 3 good enough? AIBU to eat
> only from restaurants with a rating of 5?"
> — Urchinn, [Mumsnet — "To avoid restaurants with food hygiene rating below 5?"](https://www.mumsnet.com/talk/am_i_being_unreasonable/4274778-To-avoid-restaurants-with-food-hygiene-rating-below-5), 19 Jun 2021

> "I always check online. Sometimes the hygiene is fine but something like paperwork is
> incomplete. Your local council hold the details and they are public information."
> — CuriousaboutSamphire, reply on the same thread, [Mumsnet](https://www.mumsnet.com/talk/am_i_being_unreasonable/4274778-To-avoid-restaurants-with-food-hygiene-rating-below-5), 19 Jun 2021

> "Definitely look at hygiene rating! When ordering takeaway, I won't order from anywhere with less
> than 4 star."
> — Teapleasebobb, [Mumsnet — "Do you care about hygiene rating?"](https://www.mumsnet.com/talk/am_i_being_unreasonable/4802234-do-you-care-about-hygiene-rating), 8 May 2023

> "Only one fifth of British people always check the hygiene rating of a takeaway restaurant before
> ordering."
> — national headline finding, [Food Safety News, summarizing a Furniture Choice survey of 1,000 UK adults](https://www.foodsafetynews.com/2020/09/most-people-in-uk-dont-check-takeaway-hygiene-ratings/), 12 Sep 2020

> "In Edinburgh: 36 percent admitting that they do not check the rating of their favorite takeaways
> because they don't know where to find this information."
> — city-level breakdown in the same survey writeup, [Food Safety News](https://www.foodsafetynews.com/2020/09/most-people-in-uk-dont-check-takeaway-hygiene-ratings/), 12 Sep 2020 (this 36% figure is
> Edinburgh-specific, not a national number — a separate, differently-worded 36% figure is also
> reported for Bristol in the same piece, for a different reason: not being bothered by the
> outcome, not not knowing where to look)

**What this means for the product:** people who care about this set a personal, opinionated
threshold ("won't order from anywhere with less than 4 star") and are willing to publicly judge
others who don't check — but the Edinburgh figure is an important counterweight, even though it's
one city's number, not a UK-wide one: over a third of people there who might want to check say they
simply don't know *where* to look, and display of the rating sticker itself is only mandatory in
Wales/Northern Ireland, voluntary in England. That's exactly the gap a single-input "type the
restaurant, get the official FHRS answer" tool closes — the barrier evidenced here isn't
indifference, for a meaningful share it's not knowing the lookup exists.

---

## §Personas

Four personas, one per §Research pattern. This is not a mechanical "one persona per pattern"
default — it's what the evidence actually supports: each pattern's speakers are a distinct,
non-overlapping group talking about an unrelated civic workflow (a parent worrying about A&E vs. a
20-something planning a football weekend vs. someone mid-anxiety over a bank text vs. a takeaway
customer with a ratings cutoff). Nothing in the transcripts links these voices to each other, so
merging any two into one persona would mean inventing a connection the sources don't make. Checked
*after* drafting, this happens to line up 1:1 with `target.md`'s four assumed ICPs — that's
a confirmation the evidence and the product's own targeting agree, not something engineered in
advance.

Each card below also carries its own grounding-strength flag where the evidence is uneven, per the
method's honesty discipline — Phase 3 must inherit these, not let them decay.

### The "Just-In-Case" Carer

Relevant to: **Sort My Care** (Pattern 1).

**Voice:** Not in crisis — thinking ahead. "Don't personally need to go but like to know these
things just in case as I have accidents prone relatives" (Coldnights). Wants the plain mechanics —
who do you actually ring, GP or 111 or just turn up — stated procedurally, the way PurpleDaisies
answers on the same thread ("If you're not in one of those areas and you need to go to a and e, you
just go"). But carries a live grievance against the "safe" official answer: 111 is felt to
over-refer reflexively rather than triage honestly — "I know they need to stay on the safe side but
i feel like it's their response to everything, which sort of defeats the purpose a little bit"
(riotlady).

**Grounded in:** Pattern 1 — Coldnights (opening post), PurpleDaisies (reply), riotlady (separate
thread, same pattern), all Mumsnet.

**Skeptical of:** A tool that just repeats the official "always call 111 / when in doubt go to A&E"
line without acknowledging that the official routing is inconsistent by area and is itself
distrusted for being reflexively risk-averse. To this persona, a confident single answer that
doesn't admit that variance reads as naive, not authoritative.

**What would convince them:** Explaining the *stated* pathway clearly, but being honest that
real-world practice varies by region/pilot and that "the safe answer" isn't always the useful one —
i.e., not defeating the purpose the way riotlady describes 111 doing.

**Grounding-strength flag (carry forward to Phase 3):** §Research flags this pattern's evidence as
2019–2020 vintage — one thread references a since-possibly-changed COVID-era "111-before-A&E"
pilot — while the other three patterns draw on 2021–2025 evidence. The underlying *confusion and
distrust of over-referral* is plausibly still current, but the specific routing mechanics this
persona would cite (which pilots are live, what 111 currently says) may have shifted since these
threads were posted. Treat this persona's factual routing claims as illustrative of the *feeling*,
not as a current NHS-pathway reference — this is a real, moderate-confidence caveat, not a
full-blown thin-grounding case, but it must not disappear by Phase 3.

---

### The Budget Wanderer

Relevant to: **Sort My Wander** (Pattern 2).

**Voice:** Practical about money without being joyless about it. "Our budget isn't as healthy as
our enthusiasm! We're staying in a hostel in Bayswater and we'll do plenty of wandering and looking
at the obvious sites, but I'm hoping for recommendations for cheap or free things to do that may be
a little different" (HowManyMoreTimes) — note the explicit ask for something *beyond* the obvious
sites, not instead of them. Sometimes the ask is narrower and more time-boxed: "we need something
free to do on the Saturday afternoon" (itwasnevermine, visiting for a football match). Either way,
the instinct is to ask a community for a shortlist rather than search official listings solo — and a
generic "here's what's free" answer (like BigGreen's reply, "all the major galleries and museums are
free," to HowManyMoreTimes' thread) reads as the correct-but-obvious answer they were already
half-expecting, not the "a little different" one they actually asked for.

**Grounded in:** Pattern 2 — HowManyMoreTimes and itwasnevermine (both original posters, Mumsnet).
BigGreen's reply is used only as evidence of what the *generic, unsatisfying* answer sounds like,
not as a persona voice — BigGreen is the community answering, not the person with the need.

**Skeptical of:** A tool that just resurfaces the same "free museums and markets" list every other
forum reply already gives. That's the correct answer, but it's the one they were already
half-expecting — it doesn't feel like it was worth asking for.

**What would convince them:** Something that reads as curated and "a little different," the way a
good human forum reply does, rather than a generic listings page — specific enough to feel
hand-picked for a tight, time-boxed window (an afternoon, a weekend with kids on a hostel budget),
not just a re-list of the five free museums everyone already names.

---

### The Circling-Back Verifier

Relevant to: **Sort My Scam Check** (Pattern 3).

**Voice:** Anxious in the moment, and specific about *why* the official channel failed them: "I
tried to ring them but because I don't have any account number I just keep going round in
circles...." (topcat105, mid-incident, about unexplained M&S Bank security-code texts). Sometimes
the anxiety is retrospective and turns into a public warning to others once the damage is done: "I
signed up for a payday loan about a month ago... Fast forward a month and I have a payment of
£29.50 taken out of my account from a company called onsavings, never heard of them... They are
praying on vulnerable people who are desperate" (Huhcally). And sometimes it's a flatly stated loss
of confidence in their own judgment: "I really thought I'd be able to spot a scam, but now I know
they can be far more sophisticated than I had ever imagined" (Janet from Chester, a named victim).

**Grounded in:** Pattern 3 — topcat105 and Huhcally (MoneySavingExpert Forum posters describing
their own experiences), Janet from Chester (a real victim, quoted by name in an FCA press release —
her words, not the regulator's). This is §Research's strongest-evidenced pattern.

**Skeptical of:** Any verification path that demands information they don't have (topcat105 couldn't
verify via the bank's own line *because* they lacked an account number) or that arrives too late to
matter (Huhcally, Janet from Chester — both found out after money had already moved). A tool that
requires the same kind of friction the official channels already failed on won't be trusted more
than those channels were.

**What would convince them:** A fast, low-friction, single-input check they can run *before*
proceeding — not one gated behind information only an existing customer would have. Because the
mechanism here is convincing impersonation ("clone investment scams can look real and
sophisticated," per the FCA's Mark Steward) rather than obviously bad grammar or design, the check
needs to be backed by an official/authoritative source to be worth more than their own judgment,
which Janet from Chester's quote says plainly is not enough on its own.

**Grounding-strength flag (carry forward to Phase 3):** This persona's voice is built entirely from
the three individuals' own words (topcat105, Huhcally, Janet from Chester). Mark Steward's FCA
quote and the £78m/£45,242-average loss figures in §Research are used above only as *institutional
corroboration* of scale and mechanism — they are not persona voice, and this persona would not
naturally speak in that register. If Phase 3 evaluates messaging that leans on official/regulatory
framing, note that as testing the corroborating layer, not this persona's own words.

---

### The Threshold-Setter

Relevant to: **Sort My Food Hygiene** (Pattern 4).

**Voice:** Opinionated and willing to judge others by a number. "I'm bemused by a Facebook thread
where locals have recommended restaurants which I know to have a food hygiene rating of 3. Do they
not know? Do they not care? Is 3 good enough? AIBU to eat only from restaurants with a rating of 5?"
(Urchinn). The check is habitual, not occasional: "I always check online. Sometimes the hygiene is
fine but something like paperwork is incomplete. Your local council hold the details and they are
public information" (CuriousaboutSamphire). And the cutoff is a firm, stated number: "Definitely
look at hygiene rating! When ordering takeaway, I won't order from anywhere with less than 4 star"
(Teapleasebobb).

**Grounded in:** Pattern 4 — Urchinn, CuriousaboutSamphire, Teapleasebobb (all Mumsnet, all
describing their own checking habit and threshold).

**Skeptical of:** Being told to just trust a place's reputation or a friend's recommendation instead
of the official number — Urchinn's whole post is suspicion of exactly that ("locals have
recommended restaurants which I know to have a food hygiene rating of 3"). A tool that can't
surface the *specific* official rating, fast, isn't offering anything this persona doesn't already
do manually.

**What would convince them:** A single-input lookup that returns the official FHRS-style rating
directly — matching CuriousaboutSamphire's own framing that the council already holds this as
public information, just not always easy to find *before* ordering rather than after.

**Grounding-strength flag (carry forward to Phase 3):** This persona is built entirely from
*checkers* — people who already look up ratings and have a threshold. §Research's other data point
for this pattern — "36 percent [of an Edinburgh sample] admitting that they do not check the rating
of their favorite takeaways because they don't know where to find this information" — describes a
different, non-checking segment, but that figure has **no directly quoted voice** behind it; it's a
third-party survey statistic (Food Safety News, summarizing a Furniture Choice survey), not a
forum post in this person's own words. Building a fifth persona on that stat alone would mean
inventing a voice the evidence doesn't contain, so it is deliberately *not* spun into its own
persona. If Phase 3 wants to test the product against the "doesn't know where to look" segment, that
test is evaluating a real but thinly-evidenced audience — flag any such verdict as resting on
survey-only grounding, not a quoted individual.

---

## §Verdicts

All four personas actually drove `render_session()` against the live product — three via a
`polyfetch-scrape` instance one persona's run installed into an isolated venv (`uv pip install
--python <venv> "git+https://github.com/qte77/polyfetch-scrape"` + `python -m patchright install
chromium`, kept entirely outside this repo's own `pyproject.toml`/`uv.lock`), reused by the other
runs once confirmed working via `polyfetch doctor`. All four runs are **complete, not partial** —
zero console errors and zero network failures across every session. Every finding below is a
scope/UX/positioning finding, not a reliability one.

**Tooling note, kept separate from the product verdicts (a runner-environment fact, not a product
fact):** the initial parallel attempt at three of these four runs stalled for 10 minutes each and
had to be killed and retried. The fix that unblocked them was installing `polyfetch-scrape` into an
isolated project-local venv via `uv pip install --python <venv> "git+https://github.com/qte77/
polyfetch-scrape"` rather than a global/system install (plausibly the actual stall cause — a
global install attempting to resolve a permission prompt with no one present to approve it, in this
unattended context). That worked, but was slower than necessary: a **local sibling clone of
`polyfetch-scrape` already existed at `../polyfetch-scrape/`** the entire time, directly usable via
its own env-borrowing contract (`uv run --directory ../polyfetch-scrape polyfetch ...`, per its
`USING.md`) with no install step and no network fetch of the tool itself at all. This wasn't
discovered until after Phase 3 had already completed. **For a future run of this method: check for
a local sibling clone of `polyfetch-scrape` first**, before installing from GitHub into an isolated
venv — it is both faster and avoids this exact stall.

### Persona 1 — "The Just-In-Case Carer" (Sort My Care)

**What was captured:** A full session — landing page, `?usecase=sort-my-care`, the info modal, and
roughly eight free-text submissions through the real input, including a two-step follow-up flow.

**First impression:** "'Ask in your own words' — alright, let's see if it actually listens." Typed
her real question (who to call for an accident-prone relative — 111, GP, or A&E) and the page
correctly tagged it "Showing: Sort My Care." So far so good.

**What's confusing or off-putting:** It never answers the question at all, despite every visible
signal implying it understood it — it asks a clarifying follow-up ("which part of London?") the way
a real assistant would, then returns homecare agencies and dentists sorted by walking distance from
the given postcode. Nothing about 111 vs. GP vs. A&E. Three different phrasings, including the
site's own homepage example ("GP near E8 3GT"), returned the byte-identical five results — pure
proximity ranking over CQC-registered locations, not semantic matching on the question asked (the
literal "GP near E8 3GT" example itself returned zero GPs). A reproducible conversational break: answering
the app's own clarifying question with just a postcode resets it to "I didn't understand that" plus
the full workflow menu — it performs a conversation without holding one. In the product's favor: the
info modal and every results screen are explicit that this is "not advice, a referral, or a
booking" — it never claims to triage her, even though its own copy implies otherwise.

**Would they actually use it:** No, for the need §Research actually grounds her in (which service to
call). She might use the CQC-directory lookup for a different, narrower need, but that's not what
Pattern 1 evidences.

**One-line review:** "It understood the question well enough to ask me for my postcode — then
answered a completely different one."

**Pattern tags:** Pattern 1 is **untested, not contradicted** — the product never gives a routing
answer of any kind, so her stated skepticism (a confident answer that doesn't admit real-world
variance reads as naive) never gets a chance to be confirmed or disproven. What this run does
confirm as a fresh finding is a positioning gap against this file's own assumed-ICP #1 ("finding the
right NHS service for a non-emergency need") — the shipped workflow is a CQC-proximity directory,
adjacent to but not the same as "which service is right for this need."

**Not sure about:** Per her inherited grounding flag, Pattern 1's 2019–2020 evidence may describe
routing mechanics that have since shifted, even though the underlying distrust is plausibly still
current — unresolved by this run either way. The "no subtype filtering" finding is confirmed at one
postcode across three phrasings, not swept across locations. Whether a borough name instead of a raw
postcode survives the follow-up step (unlike the postcode case) wasn't tested.

---

### Persona 2 — "The Budget Wanderer" (Sort My Wander)

**What was captured:** A complete session — landing page, info modal, natural-phrasing queries with
no location, "Bayswater" attempts (bare and embedded), then resolved queries via "Camden," "King's
Cross," the app's own "SW9 9SL" example, and the outward postcode "W2."

**First impression:** "Oh, this is clean — no sign-up, no cookies pop-up, just a box." Typed a real
Mumsnet-style ask ("cheap or free things to do... staying in a hostel... a bit different") and was
asked to clarify location — fair, since none was given.

**What's confusing or off-putting:** "Bayswater" — the actual place she'd be staying — never
resolves, alone or embedded in a full sentence, with no diagnostic (just the same generic prompt
repeated), while "Camden" (the app's own suggested example) and "King's Cross" work immediately. The
outward postcode "W2" (Bayswater's own postcode district) does resolve — so a visitor who has her
postcode is rescued, one who only knows the area name she'd say out loud is not, and the UI's own
copy ("a place like Camden or Hackney") implies area names generally work. Once a location resolves,
every query returns a flat "nearest 5 · from 35,938 official records" list of Grade-II-listed
buildings with identical boilerplate copy — for Camden this surfaced a pet shop and an anonymous
terrace; for the app's own "parks to wander" example, 4 of 5 results were still listed buildings, not
parks. None of "with kids," "budget," or "a little different" changed the output once a location was
recognized — the free text appears to do nothing beyond triggering a category match; ranking is pure
proximity.

**Would they actually use it:** No. The product is honest about what it is (a snapshot, not advice),
and she'd respect that framing, but what she wants is a shortlist that feels hand-picked, and this
returns un-curated nearest-registry rows with no editorial judgment about whether a place is worth
visiting.

**One-line review:** "It's not lying to me, it's just showing me the nearest five things whether or
not they're worth seeing — my mate's forum reply was more useful than this, and that took her thirty
seconds to type."

**Pattern tags:** **Confirms Pattern 2, more sharply than the persona card's own stated skepticism
anticipated.** The card worried the product might resurface the same generic "free museums" list a
forum already gives — that would at least match the forum's baseline. This run found a step below
that baseline: a real forum reply names actual worthwhile destinations; this tool's un-curated
nearest-N surfaced a pet shop and anonymous terraces with identical boilerplate. Pattern 2's own
framing — competing with "just ask a forum," which is human-vetted even in its genericness — is
exactly the gap this exposes.

**Not sure about:** Only four resolved locations were sampled (Camden, King's Cross, SW9 9SL, W2)
against a 35,938-record dataset — "it's always mostly buildings" held in every case tried, but isn't
fully swept. The exact boundary of which area names resolve (beyond confirming "Bayswater" fails and
"W2"/"Camden"/"Hackney"/"King's Cross" succeed) wasn't mapped.

---

### Persona 3 — "The Circling-Back Verifier" (Sort My Scam Check)

**What was captured:** A complete run — landing page, info modal, five free-text queries (the
persona's own real M&S-text scenario, the product's own seeded example "Thames Capital Partners,"
`onsavings.co.uk` from Huhcally's own §Research quote, bare "M&S Bank," and a link-extraction pass),
plus an attempted independent cross-check against the real FCA register.

**First impression:** "Fine, plain page, no sign-up wall, and it's telling me straight off it's 'not
a live search' — a snapshot, weekly refresh, dated results. Good, that's the kind of thing I actually
check for."

**What's confusing or off-putting:** Her own real scenario, typed in her own words, returned "No firm
matches" — it tried to parse the whole sentence as a company name. Narrowing to just "M&S Bank" (a
real, well-known UK bank) failed the same way. `onsavings.co.uk` — the actual scam firm from
Huhcally's own §Research quote — also came back "no firm matches," indistinguishable from the bank's
non-hit. Only the product's own pre-loaded demo example, "Thames Capital Partners," returned a
result — and returned it well: two similarly-named firms, one FCA-authorised, one not, with an
explicit clone-name warning. But the "confirm you're dealing with the real firm" link on that result
doesn't deep-link to the firm's actual register entry — it routes to the FCA register's plain
homepage, the same "back to square one" friction the persona's grounding quotes describe. The result
shown was dated "2026-05-20" against a same-page "refreshed weekly" claim, roughly 14 weeks stale as
of this run. A direct attempt to verify the Thames Capital record against the real FCA register was
itself blocked by a Cloudflare bot challenge (HTTP 403) — a fact about this runner hitting the FCA's
own site, not a finding about the product, and it leaves unresolved whether that record is genuine
FCA data or demo content.

**Would they actually use it:** Unconfirmed, leaning no for now. When it works, it's genuinely the
right shape of answer — fast, official-source-backed, addressing the clone-firm mechanism directly.
But two of three firm-name-shaped attempts (a real bank, a real scam firm from actual evidence) came
back empty with no distinction from "not registered" versus "not in our sample."

**One-line review:** "Nice idea, and when it hits it's exactly what I needed — but the one firm it
found was the one they picked to show me, and the two firms I actually cared about weren't in there
at all."

**Pattern tags:** **Confirms Pattern 3 directly.** The successful demo query is close to a textbook
implementation of the pattern's felt need. The natural-language failure and its "check the FCA
register directly" fallback reproduce topcat105's own complaint almost exactly — "I tried to ring
them... I just keep going round in circles" — and the non-deep-linked "confirm" button adds a second
instance of the same friction. The `onsavings.co.uk` miss is a direct, in-character test against
Huhcally's own real scam experience, and it registered as noise. Nothing observed contradicts Pattern
3; the gap between "ask in your own words" and what the parser needs sharpens the persona's stated
skepticism into a witnessed instance.

**Not sure about:** Sample size — three firm-name queries tested, not a survey of the underlying
data's actual scope. Whether "Thames Capital Partners LLP" is genuine FCA data or demo content is
unresolved (the verification attempt was blocked, not negative). Per this persona's inherited
grounding flag, the product's FRN/Companies-House-number framing is institutional-corroboration
language (from Mark Steward's FCA quote), not this persona's own natural register — this run tests
that corroborating layer, not confirmed "the product speaks like this persona" evidence.

---

### Persona 4 — "The Threshold-Setter" (Sort My Food Hygiene)

**What was captured:** A complete run — landing page, info modal, three name+area queries ("Dishoom
Shoreditch," "Dishoom" alone, "Nando's Brixton"), a full link enumeration, and two independent
verifications (following a captured FSA deep link, and loading the FSA's own site directly).

**First impression:** "Free, no sign-up, and it links straight to the actual FSA page — fine, that's
the right instinct. But it wants a postcode or an area from me, not a place name."

**What's confusing or off-putting:** Typing "Dishoom Shoreditch food hygiene rating" returned "5
venues near Shoreditch" — none of them Dishoom, with no acknowledgment the named place wasn't found,
just a silent substitution. "Nando's Brixton" produced the identical pattern. "Dishoom" alone (no
area) triggered the location-clarification prompt, confirming the parser extracts a location token
but never attempts to match the business name itself — by design, per the info modal's own framing
("type what you need and a place... we show the nearest official records," never "type a business").
A stale-data catch: one Brixton result was dated 2019-11-21 — roughly seven years old, not the "6–18
months old" the site's own footer claims. The product's own "search official ratings" link points
to the FSA's real site, which was independently confirmed to have a dedicated business-name search
field — exactly what this persona wants, and something the product's own escape hatch leads straight
to without offering it directly.

**Would they actually use it:** No, for her actual habitual behavior (checking a specific named
place someone recommended or she's about to order from). The workflow is structurally a "what's
nearby" tool, not a "look up this place" tool, confirmed by two convergent query failures and the
product's own stated input model.

**One-line review:** "Free and official — good instinct — but it can't tell me if the place someone
just recommended is actually a 4, it just shows me whatever's nearby instead, so I'm back on the FSA
site doing the name search myself."

**Pattern tags:** **Confirms the sourcing half of Pattern 4, contradicts/exposes a gap on the
audience-fit half.** The official, dated, single-source-backed number CuriousaboutSamphire describes
wanting is genuinely delivered (verified: one card's link correctly resolves to a real FSA business
page). But the three quoted voices this persona is built from (Urchinn, Teapleasebobb,
CuriousaboutSamphire) all verify a specific known place — behavior the product cannot serve. What the
product's nearest-N mechanic actually fits is Pattern 4's *other*, unquoted segment (the
survey-only "doesn't know where to look" figure) — a read this persona's own Phase 2 card already
flagged as resting on survey grounding, not a quoted individual, so it's carried forward as an
inference, not an equally-weighted finding next to the name-lookup gap itself.

**Not sure about:** Three query shapes tested (name+area ×2, name alone); the info modal's explicit
framing makes a different phrasing unlikely to change the result, but this wasn't exhaustively
swept. The "header date matches the oldest card" observation is n=2, not a confirmed mechanism. A
sibling run's scam-check workflow appeared to accept bare business names without a location — noted
but not independently verified in this session, so not treated as established fact here.

---

## §Cross-persona synthesis

All four personas — spanning four unrelated workflows and four unrelated real needs (a worried
relative-carer, a budget trip-planner, a scam-anxious verifier, a ratings-obsessed diner) —
independently converge on the same underlying mechanism gap: **the product's "ask in your own
words" framing extracts a location and a coarse category from free text, and discards everything
else the user actually said.** The qualitative content of each query — which routing question was
asked, which specific firm was named, what kind of experience was wanted, which specific business
was named — never shapes the answer, even when the UI performs comprehension it doesn't have (Persona
1's clarifying-question theater; Persona 4's silent substitution of an unrelated list for a named
business). Three of four verdicts (Wanderer, Verifier, Threshold-Setter) confirm this directly
against their own grounding pattern; the fourth (Carer) couldn't test its pattern at all, because the
product never engages with the actual question asked, which is itself a version of the same gap —
the free text is read for its shape, not its content.

This is the single highest-leverage finding for anyone iterating on the product: the marketing
promise ("ask in your own words") and the underlying mechanism (postcode/area + category lookup over
an open-data register) are two different products, and every persona that tested this gap tripped
over it independently, from a different angle, without prompting from each other.

A secondary, consistent finding: technical robustness and product honesty are not the problem. Zero
console errors, zero network failures across all four full runs, and every session surfaced explicit,
prominent copy that the product is a signpost, not advice, and that its data is a periodic snapshot
— the disclaimers are real and visible. The gap is entirely between what the free-text input implies
it can do and what the underlying lookup actually does, plus, in two of four workflows (Scam Check,
Wander), evidence of coverage/curation gaps (real firms/places absent or under-curated) layered on
top of that same core mismatch.

**Confirmed but unresolved, flagged honestly rather than left implicit:** whether the "Thames Capital
Partners" scam-check result reflects genuine FCA register data or seeded demo content could not be
settled — the FCA's own register blocked this run's verification attempt with a Cloudflare challenge,
a runner-environment fact, not evidence either way.
