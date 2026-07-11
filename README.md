# The Unofficial Guide — Project 1

A RAG system that answers questions about off-campus housing at UC Berkeley using real r/berkeley threads.

**Demo video:** [VIDEO LINK GOES HERE]

## How to run it

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # then paste your Groq key into .env
python collect_documents.py # fetches the 17 threads (already included in documents/)
python ingest.py            # cleans and chunks into chunks.json
python build_index.py       # embeds chunks into ChromaDB
python app.py               # opens the Gradio UI at http://localhost:7860
```

---

## Domain

Off-campus housing and student living at UC Berkeley. The official housing site covers application deadlines and dorm rates, but it will never tell you which apartment company ignores maintenance requests for months, whether southside actually feels safe at night, how the fake check sublet scam works, or that "luxury" buildings advertise $1,400 per bed by planning for triples. That knowledge only exists in r/berkeley threads where students warn each other and answer each other's questions, and it is scattered across years of posts that are hard to search. This system makes it queryable in plain language with citations back to the original threads.

---

## Document Sources

All 17 documents are threads from the r/berkeley subreddit. Reddit blocks direct scraping (I tried both the JSON API and mirror sites and got bot walls), so `collect_documents.py` pulls them through the PullPush archive API instead. Each file in `documents/` contains the thread title, permalink, date, the original post, and up to 20 top-scored replies, with removed/deleted comments, AutoModerator posts, and replies under 40 characters filtered out.

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Safe to live alone in southside | Safety thread | https://www.reddit.com/r/berkeley/comments/1402pj4/ → `documents/southside_safety_1402pj4.txt` |
| 2 | AVOID STERLING APARTMENT COLLECTIONS AT ALL COST!!!! | Building review | https://www.reddit.com/r/berkeley/comments/10qpclk/ → `documents/avoid_sterling_10qpclk.txt` |
| 3 | Ace Berkeley apartments DO NOT RENT | Building review | https://www.reddit.com/r/berkeley/comments/1idyoyy/ → `documents/avoid_ace_berkeley_1idyoyy.txt` |
| 4 | Thinking about living in Identity Logan Park? Read this. | Building review | https://www.reddit.com/r/berkeley/comments/1abwegr/ → `documents/identity_logan_park_1abwegr.txt` |
| 5 | Subletters, beware for scammers | Scam warning | https://www.reddit.com/r/berkeley/comments/12ew1tz/ → `documents/housing_scams_12ew1tz.txt` |
| 6 | Lease argument | Tenant rights Q&A | https://www.reddit.com/r/berkeley/comments/1580z76/ → `documents/lease_dispute_1580z76.txt` |
| 7 | Sudden rent hike 15 days before the end of the month? Help? | Tenant rights Q&A | https://www.reddit.com/r/berkeley/comments/1kmzn6q/ → `documents/rent_hike_1kmzn6q.txt` |
| 8 | Thoughts on Housing Costs | Rent market discussion | https://www.reddit.com/r/berkeley/comments/1c4013y/ → `documents/housing_costs_1c4013y.txt` |
| 9 | Best neighborhoods to live in | Neighborhood advice | https://www.reddit.com/r/berkeley/comments/vcd6uu/ → `documents/best_neighborhoods_vcd6uu.txt` |
| 10 | Best neighborhoods for CS major (off campus housing)? | Neighborhood advice | https://www.reddit.com/r/berkeley/comments/ne41wq/ → `documents/neighborhoods_cs_ne41wq.txt` |
| 11 | Best One Bed, One Bath or Solo Rooms on Berkeley | Living solo advice | https://www.reddit.com/r/berkeley/comments/1k6ezhe/ → `documents/solo_rooms_1k6ezhe.txt` |
| 12 | Grad Students Housing Options | Grad housing advice | https://www.reddit.com/r/berkeley/comments/1irtkg6/ → `documents/grad_housing_1irtkg6.txt` |
| 13 | BERKELEY CO OPS | Co-op living | https://www.reddit.com/r/berkeley/comments/1koq3t3/ → `documents/coops_1koq3t3.txt` |
| 14 | when to start looking for apartments of fall 2025 | Search timeline | https://www.reddit.com/r/berkeley/comments/1i3kdjh/ → `documents/when_to_search_1i3kdjh.txt` |
| 15 | Questions about housing from a new student | General housing Q&A | https://www.reddit.com/r/berkeley/comments/r01hx/ → `documents/new_student_housing_r01hx.txt` |
| 16 | International student coming for the Summer | Short-term housing | https://www.reddit.com/r/berkeley/comments/1dup8e/ → `documents/intl_summer_housing_1dup8e.txt` |
| 17 | Anchor House roommate | Roommate search | https://www.reddit.com/r/berkeley/comments/1ko80eo/ → `documents/roommates_1ko80eo.txt` |

---

## Chunking Strategy

**Chunk size:** up to 800 characters, built by packing whole paragraphs (post paragraphs or individual comments) together until the next one would go over the limit. Paragraphs that are themselves over 800 characters get split on sentence boundaries first. Final chunks run 157 to 1,104 characters, averaging 686.

**Overlap:** when a chunk fills up, the last paragraph carries into the next chunk if it is under 300 characters. So overlap is one short paragraph rather than a fixed character count.

**Why these choices fit your documents:** Reddit threads are made of comments, and a comment is the natural unit of meaning here. A fixed 500-character split would cut comments mid-sentence, and half a comment retrieves nothing useful. Packing whole comments keeps every chunk self-contained, and 800 characters fits about 2 to 4 typical replies, enough to stay on one topic without mixing several. I also prepend the thread title to every chunk (`Thread: Safe to live alone in southside`) because a reply like "it's really not that bad, just lock up" is meaningless without knowing what question it answered. Preprocessing before chunking: unescape HTML entities (`&amp;`, `&#x200B;`), strip markdown links keeping the anchor text, drop bare URLs and reddit image preview links, remove the `[N points]` score markers, and collapse extra whitespace.

**Final chunk count:** 112 chunks across 17 documents.

---

## Sample Chunks

Five chunks pulled at random after running `python ingest.py`. Every chunk starts with a `Thread:` header so a comment keeps the context of the question it was answering.

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

**Model used:** all-MiniLM-L6-v2 via sentence-transformers, running locally. Free, no API key, fast enough to embed all 112 chunks in a few seconds on a laptop, and its 256 token input limit fits my chunk sizes.

**Production tradeoff reflection:** For real users I would weigh four things. Accuracy on informal text: student posts are full of slang and local shorthand ("tweaks", "cba", "unit 3", "gourmet ghetto"), and a small general-purpose model embeds those weakly, so a larger model like text-embedding-3-large or BGE-M3 would likely retrieve better on this corpus. Context length: MiniLM truncates at 256 tokens, which capped my chunk size; a longer-context model would let me chunk by whole comment threads. Multilingual support: Berkeley has a huge international population that might query in Chinese or Korean, and MiniLM is English-only. Latency and privacy: a local model keeps queries on device and costs nothing per call, which matters because housing questions can be personal ("can my landlord evict me if..."), while an API model gives better quality at the price of a network hop, a per-query cost, and shipping user queries to a third party.

---

## Retrieval Test Results

Run with `python test_retrieval.py` (top 5 by cosine distance, lower is better; abbreviated to the top 3 here).

**Query 1:** "Is it safe to live alone in southside?"

Top returned chunks:
- (0.263) `southside_safety_1402pj4.txt`: "Get to know your neighbors a little. You can use them for a sense of security... Always lock your doors."
- (0.264) `southside_safety_1402pj4.txt`: "They are all potential acquaintances... knowing some people by sight and name in your building will help if there are any problems"
- (0.273) `southside_safety_1402pj4.txt`: "Get a door lock holder (the type that fit under the handle). Don't turn on lights near your window immediately after getting inside..."

Relevance explanation: all five results came from the one thread that is literally this question, with distances in the 0.26 to 0.35 range. The chunks are the safety precautions students actually recommended (locks, neighbors, window habits), which is exactly the material an answer needs. This is the best case for the system: a query that closely mirrors a thread title plus content.

**Query 2:** "When should I start looking for an apartment for next year?"

Top returned chunks:
- (0.308) `new_student_housing_r01hx.txt`: original post asking "when the best time to look for housing is" for an August move-in
- (0.327) `when_to_search_1i3kdjh.txt`: "I scope locations in Feb and start touring early March. Ideally have a new lease before dead week"
- (0.521) `intl_summer_housing_1dup8e.txt`: a summer-housing post, loosely related

Relevance explanation: the top two hits are the two threads in my corpus that discuss search timing, and the second one contains the concrete answer (scope in February, tour in early March, sign before dead week). The third hit is a topical neighbor rather than an answer, which is why I keep k at 5 but let the answer lean on the strongest chunks. Semantic search matched "start looking for an apartment" to "best time to look for housing" with no shared phrasing, which keyword search would have missed.

**Query 3:** "Which landlords or property companies should I avoid?"

Top returned chunks:
- (0.558) `solo_rooms_1k6ezhe.txt`: names Premium Properties and North Berkeley Properties as the big management companies
- (0.558) `identity_logan_park_1abwegr.txt`: "Identity Logan Park is pricey. The furnishings are shoddy... beds break, and maintenance charges for replacements"
- (0.561) `avoid_sterling_10qpclk.txt`: the wifi/construction complaints from the Sterling thread

Relevance explanation: the right threads surface (the three building-review rants plus the chunk naming the big property companies), but distances sit around 0.55 to 0.58, noticeably weaker than the other queries. The reason is a vocabulary mismatch: the reviews express "avoid this company" through specific anecdotes about trash valets and broken garages, while the query uses abstract meta-language ("which landlords should I avoid"), so no single chunk matches the phrasing strongly. This weakness shows up again in the evaluation report below.

---

## Grounded Generation

**System prompt grounding instruction:** the exact system prompt in `query.py` is:

> You answer questions about student life at UC Berkeley using only the excerpts from r/berkeley threads provided below. Rules:
> - Use only information that appears in the excerpts. Do not use any outside knowledge about Berkeley or anything else.
> - If the excerpts do not contain enough information to answer, reply exactly: "I don't have enough information on that in my documents."
> - When you make a claim, mention which thread it came from, for example: according to the thread "Safe to live alone in southside".
> - These are student opinions, so present them as what students say, not as verified facts.

Structurally, grounding is enforced in three ways beyond the prompt. First, retrieved chunks with cosine distance above 0.65 are dropped before the prompt is built, and if nothing survives the cutoff the system returns the refusal string without ever calling the LLM. Second, the excerpts are labeled with their source filenames in the prompt, so the model cites real files rather than inventing citations. Third, the source list shown to the user is built programmatically from the retrieval metadata in `ask()`, not extracted from the LLM's text, so attribution cannot be hallucinated even if the model forgets to cite.

**How source attribution is surfaced in the response:** the model names threads inline (according to the thread "..."), and the interface shows a separate "Retrieved from" panel listing each source file with its reddit permalink, populated from the retrieval metadata.

---

## Example Responses

**Grounded response 1**

Query: What do students say about Sterling Apartment Collections?

Response: "According to the thread "AVOID STERLING APARTMENT COLLECTIONS AT ALL COST!!!!", students say that Sterling Apartment Collections have several issues. They mention that the apartments have mandatory trash collection, which they have to pay for, but the trash is not always collected (Excerpt 1 and 4). They also state that the apartments are poorly designed, with small or inconvenient storage areas (Excerpt 1). Additionally, students claim that the management is untrustworthy and has lied to them about amenities, such as fans in the apartments (Excerpt 1). Some students have also experienced issues with security, including bike thefts in the garage (Excerpt 4), and problems with package delivery due to the gated apartment complex (Excerpt 5). Overall, students strongly advise against living in Sterling Apartment Collections, citing their negative experiences with the management and the apartments themselves (Excerpts 1-5)."

Source attribution: `avoid_sterling_10qpclk.txt` (https://www.reddit.com/r/berkeley/comments/10qpclk/avoid_sterling_apartment_collections_at_all_cost/)

**Grounded response 2**

Query: Can my landlord keep my deposit if someone else takes over my lease?

Response: "According to the thread "Lease argument", students say that a landlord can only keep a deposit if the tenant caused physical damage to the property. If someone else takes over the lease, the landlord is legally required to return the deposit, unless there are damages or other deductions allowed by law, such as the cost of advertising for a new tenant, which must be itemized and reasonable."

Source attribution: `lease_dispute_1580z76.txt` (https://www.reddit.com/r/berkeley/comments/1580z76/lease_argument/)

**Out-of-scope query**

Query: What is the best dining hall on campus?

System response (refusal): "I don't have enough information on that in my documents." (No sources shown. The retriever did return housing chunks under the distance cutoff, but the model correctly recognized none of them mention dining halls and used the refusal string, and the app suppresses the source list when the answer is a refusal.)

---

## Query Interface

**Input fields:** one Gradio textbox for the question, plus an Ask button (pressing Enter also submits).

**Output format:** two text panels. "Answer" shows the LLM's grounded response with inline thread citations. "Retrieved from" lists each source document that survived the distance cutoff, with its reddit permalink. Run with `python app.py` and open http://localhost:7860.

**Sample Interaction Transcript**

> **User:** Is it safe to live alone in southside Berkeley?

> **System:** (Answer) According to the thread "Safe to live alone in southside", some students say it's not that bad and that you can be fine if you take precautions such as locking up, not talking to strangers, and carrying pepper spray. One student mentions that the neighborhood has changed and they've noticed less crime. However, another student expresses concern about safety, especially for women walking alone. Overall, students seem to think that with some caution and preparation, it is possible to live alone safely in southside Berkeley.
> (Retrieved from) southside_safety_1402pj4.txt (https://www.reddit.com/r/berkeley/comments/1402pj4/safe_to_live_alone_in_southside/)

---

## Evaluation Report

Full raw output is in `eval_results.json` (generated by `python evaluate.py`).

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Is it safe to live alone in southside Berkeley? | Generally fine with precautions (locks, awareness, don't walk alone late), though some students report it getting worse | Balanced summary: fine with precautions like locking up and pepper spray, one student notes less crime, another worries about women walking alone | Relevant (all 5 chunks from the right thread, 0.28 to 0.35) | Accurate |
| 2 | When should I start looking for an apartment for the next school year? | Scope in February, tour early March, lease signed before dead week; listings go up about a month before leases start | Cited exactly those two facts from the two timing threads | Relevant (top 2 chunks are the answer; chunks 3 to 5 weaker) | Accurate |
| 3 | Which landlords or property management companies do students say to avoid? | Sterling (trash valet fees, stolen packages, month without hot water), Ace Berkeley, Identity Logan Park (shoddy furnishings, billing issues) | Named Ace and Sterling but gave weak reasons for Sterling (wifi, construction) and never mentioned Identity Logan Park even though a chunk from it was retrieved | Partially relevant (right threads but weakest chunks of them; one off-topic bike parking chunk at 0.543) | Partially accurate |
| 4 | How much should I expect to pay in rent near campus? | Roughly $1,100 to $1,500 for a single room with roommates; luxury buildings charge $1,000 to $1,500 per bed in triples; $1,500 to $1,600 max on Northside | Gave the $1,100 to $1,500 single-room figure correctly, but also presented one poster's personal $2,500 to $3,000 budget as if it were a market price | Relevant (0.43 to 0.44, all four rent threads surfaced) | Partially accurate |
| 5 | What is the best dining hall on campus? | Out of scope, system should refuse | "I don't have enough information on that in my documents." | n/a (retrieval returned housing chunks, none about dining) | Accurate (correct refusal) |

---

## Failure Case Analysis

**Question that failed:** "Which landlords or property management companies do students say to avoid?" (question 3)

**What the system returned:** it named Ace Berkeley and Sterling, but justified Sterling with the least damning complaints (unreliable wifi, construction next door) instead of the core ones (a month without hot water, stolen packages, bike thefts), and it skipped Identity Logan Park entirely even though a chunk from that thread was in the context.

**Root cause (tied to a specific pipeline stage):** this is a retrieval failure caused by a vocabulary mismatch at the embedding stage. The review threads never say "avoid this landlord" in general terms; they express it through concrete anecdotes ("no hot water for a month", "packages stolen in 30 minutes"). The query uses abstract meta-language ("which companies should I avoid"), so no chunk matches it strongly. Every retrieved chunk sat at 0.52 to 0.58 distance, and the specific chunks retrieved from the Sterling thread happened to be its mildest complaints. The generation stage then did its job faithfully on mediocre context: it summarized what it was given, which was the wrong subset of the evidence. An off-topic chunk about bike parking from the grad housing thread (0.543) also made it under my 0.65 cutoff and diluted the context.

**What you would change to fix it:** two options. Hybrid search (adding BM25) would let the literal word "avoid" in two of the thread titles pull those documents up. Alternatively, retrieving at the document level after chunk-level matching (fetching the top chunks from each matched thread rather than the top 5 chunks overall) would have given the model the hot water and package theft chunks alongside the wifi one.

---

## Spec Reflection

**One way the spec helped you during implementation:** writing the chunking strategy before coding forced me to actually look at the document structure first, and that is where the "comments are the unit of meaning" decision came from. When the AI-generated first draft of the chunker was a plain fixed-character splitter, I had a concrete spec to check it against and could immediately say it violated the paragraph-packing rule, instead of only discovering the problem later through bad retrieval results.

**One way your implementation diverged from the spec, and why:** the spec said chunks are capped at 800 characters by packing whole paragraphs, but real documents had single paragraphs up to 2,569 characters (long rants in the original posts), which would silently truncate inside the embedding model's 256 token limit. I added a sentence-boundary split for oversized paragraphs and updated planning.md to record it. Collection also diverged: the plan was keyword search over the archive, but keyword search kept returning high-scoring off-topic threads (a memorial vigil post matched "apartment hunting" because the word "apartments" appeared in the body), so I switched to hand-picking thread IDs after browsing candidate titles.

---

## AI Usage

**Instance 1**

- *What I gave the AI:* my Documents and Chunking Strategy sections from planning.md, and asked it to implement the collection script that pulls r/berkeley threads through PullPush plus the ingest/chunking script.
- *What it produced:* a collector that searched the archive by keyword and took the top-scored matching thread per topic, and a chunker matching my paragraph-packing spec.
- *What I changed or overrode:* the keyword collection was unusable in practice. Sorting by score returned popular threads that merely contained the keyword somewhere (an unrelated campus memorial thread came back for "apartment hunting"), and a title-only filter still let joke threads through ("Is it possible to super commute from the moon 3x a week to save on rent"). I directed it to instead dump candidate titles for a set of queries so I could review them, hand-picked 17 thread IDs myself, and had the script rewritten to fetch that curated list. I also had it add a sentence-boundary split after finding a 2,569-character chunk that would have blown past the embedder's token limit.

**Instance 2**

- *What I gave the AI:* my Retrieval Approach section, the grounding requirement, the Groq model name, and the Gradio skeleton from the project instructions, and asked it to wire retrieval, generation, and the interface together.
- *What it produced:* `build_index.py`, `query.py`, and `app.py`, with the grounding prompt, a 0.65 distance cutoff before the LLM sees any context, and the source list built from retrieval metadata instead of trusting the model to cite.
- *What I changed or overrode:* testing the out-of-scope dining hall question exposed that the app displayed a "Retrieved from" source list even when the model refused to answer, which reads like the system is citing sources for a non-answer. I had `ask()` changed to return an empty source list whenever the response is the refusal string. I also confirmed the $1,100 to $1,500 rent figure in the eval actually appears in a source chunk before marking that answer as grounded, rather than taking the citation at face value.
