# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

Off-campus housing and student living at UC Berkeley. The official housing site tells you application deadlines and dorm rates, but it will never tell you which apartment company has a reputation for ignoring maintenance requests, whether southside actually feels safe at night, how the sublet check scam works, or what a fair price per bed looks like when a "luxury" building advertises $1,400 per bed in a triple. That knowledge lives in r/berkeley threads where students vent, warn each other, and answer each other's questions. My system makes those threads searchable and answerable.

---

## Documents

All documents are threads from the r/berkeley subreddit, pulled through the PullPush archive API (Reddit blocks direct scraping) and saved as plain text files in `documents/`. Each file contains the thread title, URL, date, the original post, and the top replies by score.

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Safe to live alone in southside | Safety experiences and precautions for southside | https://www.reddit.com/r/berkeley/comments/1402pj4/ (`documents/southside_safety_1402pj4.txt`) |
| 2 | AVOID STERLING APARTMENT COLLECTIONS AT ALL COST!!!! | Detailed negative review of a big apartment company | https://www.reddit.com/r/berkeley/comments/10qpclk/ (`documents/avoid_sterling_10qpclk.txt`) |
| 3 | Ace Berkeley apartments DO NOT RENT | Negative review of Ace Berkeley apartments | https://www.reddit.com/r/berkeley/comments/1idyoyy/ (`documents/avoid_ace_berkeley_1idyoyy.txt`) |
| 4 | Thinking about living in Identity Logan Park? Read this. | Long resident review of Identity Logan Park | https://www.reddit.com/r/berkeley/comments/1abwegr/ (`documents/identity_logan_park_1abwegr.txt`) |
| 5 | Subletters, beware for scammers | How the fake check sublet scam works | https://www.reddit.com/r/berkeley/comments/12ew1tz/ (`documents/housing_scams_12ew1tz.txt`) |
| 6 | Lease argument | Deposit and lease transfer dispute, tenant rights advice | https://www.reddit.com/r/berkeley/comments/1580z76/ (`documents/lease_dispute_1580z76.txt`) |
| 7 | Sudden rent hike 15 days before the end of the month? Help? | Rent increase notice rules | https://www.reddit.com/r/berkeley/comments/1kmzn6q/ (`documents/rent_hike_1kmzn6q.txt`) |
| 8 | Thoughts on Housing Costs | Rent levels, luxury buildings, per-bed pricing | https://www.reddit.com/r/berkeley/comments/1c4013y/ (`documents/housing_costs_1c4013y.txt`) |
| 9 | Best neighborhoods to live in | Neighborhood comparison for students | https://www.reddit.com/r/berkeley/comments/vcd6uu/ (`documents/best_neighborhoods_vcd6uu.txt`) |
| 10 | Best neighborhoods for CS major (off campus housing)? | Where to live relative to the CS buildings | https://www.reddit.com/r/berkeley/comments/ne41wq/ (`documents/neighborhoods_cs_ne41wq.txt`) |
| 11 | Best One Bed, One Bath or Solo Rooms on Berkeley | Recommendations for living alone | https://www.reddit.com/r/berkeley/comments/1k6ezhe/ (`documents/solo_rooms_1k6ezhe.txt`) |
| 12 | Grad Students Housing Options | Housing options for grad students | https://www.reddit.com/r/berkeley/comments/1irtkg6/ (`documents/grad_housing_1irtkg6.txt`) |
| 13 | BERKELEY CO OPS | What living in the co-ops is like | https://www.reddit.com/r/berkeley/comments/1koq3t3/ (`documents/coops_1koq3t3.txt`) |
| 14 | when to start looking for apartments of fall 2025 | Apartment search timeline | https://www.reddit.com/r/berkeley/comments/1i3kdjh/ (`documents/when_to_search_1i3kdjh.txt`) |
| 15 | Questions about housing from a new student | General housing Q&A for someone new | https://www.reddit.com/r/berkeley/comments/r01hx/ (`documents/new_student_housing_r01hx.txt`) |
| 16 | International student coming for the Summer | Short-term summer housing advice | https://www.reddit.com/r/berkeley/comments/1dup8e/ (`documents/intl_summer_housing_1dup8e.txt`) |
| 17 | Anchor House roommate | Roommate search post for Anchor House | https://www.reddit.com/r/berkeley/comments/1ko80eo/ (`documents/roommates_1ko80eo.txt`) |

---

## Chunking Strategy

**Chunk size:** up to 800 characters per chunk, built by packing whole paragraphs (post paragraphs or individual comments) together until the next one would push past 800.

**Overlap:** when a chunk fills up, the last paragraph carries over into the next chunk if it is under 300 characters. So overlap is one short paragraph, not a fixed character count.

**Reasoning:** My documents are Reddit threads, which means each unit of meaning is a comment or a paragraph of the original post. A fixed character split would cut comments in half, and half a comment is useless for retrieval (a chunk that ends mid-sentence like "the landlord refused to" cannot answer anything). Packing whole comments keeps every chunk self-contained. 800 characters fits roughly 2 to 4 typical comments, which is enough context to be meaningful but small enough that a chunk stays on one topic. I also prepend the thread title to every chunk (like "Thread: Safe to live alone in southside") because a comment like "yes it is fine, just don't walk alone at 3am" only makes sense if you know what question it was answering. The carry-over rule handles cases where a short comment is a reply that continues the previous thought.

Update during implementation: a few original posts turned out to have single paragraphs way over 800 characters (one was 2,569), which would get cut off by the embedding model's 256 token limit. I added a rule that splits an oversized paragraph on sentence boundaries before packing. Final chunk sizes run from 157 to 1,104 characters with an average of 686.

If chunks were too small (single short comments), the embeddings would carry almost no signal and retrieval would match on stray words. If they were too large (a whole thread), one chunk would mix safety talk with rent talk and dilute the match for any specific query. Bad retrieval in the first case looks like random one-liners; in the second case it looks like the same giant chunk coming back for every question.

---

## Retrieval Approach

**Embedding model:** all-MiniLM-L6-v2 via sentence-transformers, running locally. It is free, fast on a laptop, and its 256 token limit fits my 800 character chunks fine.

**Top-k:** 5. With 2 to 4 comments per chunk, 5 chunks gives the LLM roughly 10 to 20 student opinions to work from, which is enough to see agreement or disagreement without stuffing the prompt with weak matches. I will also drop any retrieved chunk with cosine distance above 0.65 before it reaches the LLM, so an off-topic question does not get answered from junk context. Too few chunks and one weird comment dominates the answer; too many and loosely related chunks pull the answer off topic.

**Production tradeoff reflection:** If this were a real product I would weigh: accuracy on informal slang-heavy text (student posts say "tweaks", "cba", "unit 3", which small general models may embed poorly, so a larger model or one fine-tuned on social text could retrieve better), context length (MiniLM truncates at 256 tokens, so longer chunks would need something like OpenAI text-embedding-3 or BGE-M3), multilingual support (Berkeley has many international students who might query in Chinese or Korean, MiniLM is English-only), and latency plus privacy (local models keep queries on device and cost nothing per call, API models are better quality but add a network hop and a per-query cost, and housing questions can be personal enough that I would rather not ship them to a third party).

---

## Evaluation Plan

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Is it safe to live alone in southside Berkeley? | Students say southside is generally fine if you take normal precautions; it is crowded with students, but don't walk alone late at night and be aware of package theft and occasional incidents. |
| 2 | What do students say about Sterling Apartment Collections? | Avoid them: mandatory paid trash valet service that is unreliable, packages stolen despite cameras, broken garage door leading to bike thefts, almost a month without hot water with only $125 compensation, unresponsive management. |
| 3 | How does the sublet check scam work and how do I avoid it? | A fake subletter sends a check for more than agreed, then pressures you to wire back the difference before the check bounces. Avoid it by never wiring money back, not cashing overpayment checks, and asking for references and contact info. |
| 4 | Can my landlord keep my deposit if someone else takes over my lease? | No. Students citing California law say the landlord must return the deposit within about 30 days regardless of who found the replacement tenant, and can only deduct documented damage or itemized advertising costs. Small claims court and tenant groups are the recourse. |
| 5 | What is the best dining hall on campus? | Out of scope on purpose. My documents are about housing, so the system should say it doesn't have enough information rather than making something up. |

---

## Anticipated Challenges

1. Reddit threads are noisy. Jokes, sarcasm, and rants sit next to genuinely useful advice, and the LLM cannot always tell them apart. A sarcastic "yeah totally safe, nothing ever happens here" could get quoted as a real safety assessment. My cleaning step strips images and links but it cannot strip sarcasm.

2. Comments lose their context when separated from the thread. A reply like "definitely the second one" is meaningless without the parent comment, and my flat comment list does not preserve reply structure. I am mitigating this by prepending the thread title to every chunk and by filtering out comments under 40 characters, but some retrieved chunks will still be answers to questions the chunk does not contain.

3. Coverage gaps. Ten-ish threads cannot cover every housing question, and the danger is the model filling gaps with training knowledge (it definitely knows things about Berkeley). The grounding prompt plus the distance cutoff should make the system decline instead, and question 5 in my eval plan tests exactly this.

---

## Architecture

```
 documents/*.txt          ingest.py                build_index.py
+----------------+     +------------------+     +----------------------+
| r/berkeley     |     | clean text,      |     | embed chunks with    |
| threads via    | --> | strip links and  | --> | all-MiniLM-L6-v2,    |
| PullPush API   |     | markdown, pack   |     | store in ChromaDB    |
| (collect_      |     | comments into    |     | with source metadata |
| documents.py)  |     | ~800 char chunks |     | (cosine space)       |
+----------------+     +------------------+     +----------------------+
                                                          |
                                                          v
       app.py (Gradio)              query.py         query.py
+----------------------+     +-----------------+     +------------------+
| textbox in, answer   |     | Groq            |     | embed query,     |
| + sources out at     | <-- | llama-3.3-70b   | <-- | top-5 chunks,    |
| localhost:7860       |     | grounded prompt |     | drop dist > 0.65 |
+----------------------+     +-----------------+     +------------------+
        Interface               Generation               Retrieval
```

---

## AI Tool Plan

**Milestone 3 — Ingestion and chunking:** I will give Claude Code my Documents and Chunking Strategy sections and ask it to implement `collect_documents.py` (fetch threads from PullPush and save as text files) and `ingest.py` (clean the text and produce chunks with the paragraph-packing rule above). I will verify by printing 5 random chunks and checking they are self-contained, have the thread title header, and contain no leftover markdown or URLs. I expect to have to correct the collection step, since keyword search over Reddit archives returns a lot of off-topic threads.

**Milestone 4 — Embedding and retrieval:** I will give Claude Code my Retrieval Approach section and the architecture diagram and ask for `build_index.py` (embed all chunks with all-MiniLM-L6-v2 into a persistent ChromaDB collection using cosine distance, with source filename, thread title, URL, and position as metadata) and a `retrieve()` function in `query.py`. I will verify by running 3 of my eval questions through `test_retrieval.py` and checking top distances are under 0.5 and the chunks visibly relate to the question.

**Milestone 5 — Generation and interface:** I will give Claude Code the grounding requirement (answer only from retrieved excerpts, refuse when context is insufficient, cite the thread), the Groq model name, and the Gradio skeleton from the project instructions, and ask it to wire `ask()` plus `app.py`. I will verify grounding by asking question 5 from my eval plan (dining halls) and checking the system refuses, and by checking the source list is built from retrieval metadata in code rather than trusting the LLM to cite honestly.
