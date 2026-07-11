# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |
| 7 | | | |
| 8 | | | |
| 9 | | | |
| 10 | | | |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Sample Chunks

Five chunks pulled at random after running `python ingest.py` (seeded sample). Every chunk starts with a `Thread:` header so a comment keeps the context of the question it was answering.

**Chunk 1** (source: `identity_logan_park_1abwegr.txt`)

> Thread: Thinking about living in Identity Logan Park? Read this.
> It takes on average an entire business day to fix the parking system which creates two awful scenarios. If your car is in the machine while it's broken, good luck. You won't be able to get your car out until it get's repaired. This sound bad, but if your car isn't in the machine when it breaks is somehow worse. First of all, you aren't allowed to park in the regular spots in the garage as they're reserved for staff and employees at the connected Chase bank. If you do park in these spots, they have all non-registered cars towed at the end of the day and issue a fine of $500 on top of having to get your car from a tow lot. Instead, you have to pay out of pocket for street parking until it gets fixed.

**Chunk 2** (source: `southside_safety_1402pj4.txt`)

> Thread: Safe to live alone in southside
> It sure has changed…gotten worse, I reckon
> They have door jams that you can put on the inside once you're in the house. Easily bought on Amazon.
> Im an incoming transfer and I was planning on getting an apartment on southside too! I'm a 200lbs male bodybuilder tho, but regardless all the robberies and assaults still make me very concerned :(
> It's really not that bad. Just make sure you lock up when ur inside and out. Don't talk to strangers get some pepper spray and stay alert & you'll be fine. Probably won't ever have to use it. The neighborhood in south berkeley has changed a lot and I've noticed less crime

**Chunk 3** (source: `lease_dispute_1580z76.txt`)

> Thread: Lease argument
> How can they having the landlord's contacts be considered they reached out to the landlord first. And then as I was arguing with her, she suddenly said she was busy and told me she didn't want to waste her time on meaningless shit, after which she told me she will withdraw the "little help" she gave me (which is the approval of lease transfer) and let me bear the lease as I have paid the 300 security deposit for dormitory. And then, she just vanished and refused to talk to me again. I am an international student and do not want to risk my student status fighting lawsuits, and my family is not rich and cannot afford me paying double rent. What can I do? Can she even withdraw the approval just like that?

**Chunk 4** (source: `southside_safety_1402pj4.txt`)

> Thread: Safe to live alone in southside
> - Always be aware of your surroundings. Don't walk around with earbuds in looking at your phone--I can't believe how often I see this, and those folks look like walking targets. Don't flash valuables. Walk with purpose. If someone seems sketchy, avoid them but don't run (unless you have to).
> - Get to know your neighbors. They can be a great resource if you need help of any kind, and it will probably give you a good deal of psychological reassurance to know who's around you.
> - Take a self-defense class. A lot of people will tell you to get pepper spray or whatnot, but getting some real training in how to use it and other defense techniques will make it much more likely that you'll use it effectively.
> It sure has changed…gotten worse, I reckon

**Chunk 5** (source: `southside_safety_1402pj4.txt`)

> Thread: Safe to live alone in southside
> Not sure if you're living in an apartment or a room in a house...but I'll assume apartment for the moment.
> Regarding locks, Berkeley law, I believe, requires all rental apartments to have deadbolt locks (in addition to any lock that's on the door handle. The deadbolt is the separate lock, usually placed in the door above the handle, that has its own key and is operated from the inside by a little lever). If yours doesn't have one, you can check with the Rent Stabilization Board online or by email for the exact information on what's required of the owner.
> In addition to the other good advice, I would emphasize *get to know your neighbors*. So many people in apartment buildings in Berkeley live in isolation, both from others in their building and others who live nearby.

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Retrieval Test Results

<!-- Run these 3 queries through your retrieval system and record the top returned chunks.
     For at least 2 of the 3, explain why the returned chunks are relevant to the query.
     Results must be text — not screenshots. -->

**Query 1:**

Top returned chunks:
-
-
-

Relevance explanation:

---

**Query 2:**

Top returned chunks:
-
-
-

Relevance explanation:

---

**Query 3:**

Top returned chunks:
-
-
-

Relevance explanation:

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Example Responses

<!-- Provide at least 2 grounded responses (query + response + source attribution)
     and 1 out-of-scope query showing your system's refusal.
     All entries must be text — not screenshots. -->

**Grounded response 1**

Query:

Response:

Source attribution:

---

**Grounded response 2**

Query:

Response:

Source attribution:

---

**Out-of-scope query**

Query:

System response (refusal):

---

## Query Interface

<!-- Describe your query interface: what are the input fields, what does the output look like?
     Then provide a complete sample interaction transcript showing a real exchange. -->

**Input fields:**

**Output format:**

---

**Sample Interaction Transcript**

<!-- Show a complete query → response exchange as it actually appears in your interface.
     Must be text — not a screenshot. -->

> **User:** 

> **System:** 

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
