# Chapter 13 â€” Design A Search Autocomplete System

## Q1: When storing a massive Trie structure containing billions of search phrases across a distributed Redis cluster, which sharding strategy prevents severe hotspots when a letter like 'c' or 't' starts a disproportionate number of English queries?

**Options:**

- Shard the cluster based strictly on the first character of the search phrase.
- Use consistent hashing on a fixed-length prefix string (e.g., the first two or three characters) or compute a hash of the entire phrase to distribute lookup roots uniformly across the cluster.
- Store the entire Trie on a single monolithic master node using virtual memory paging structures.
- Partition the Trie layers based on the total character length of the complete text phrase.

**Answer:** Use consistent hashing on a fixed-length prefix string (e.g., the first two or three characters) or compute a hash of the entire phrase to distribute lookup roots uniformly across the cluster.

## Q2: To meet a strict sub-10ms read latency budget for autocomplete suggestions on mobile network connections, which client-side browser optimization reduces redundant API round-trips?

**Options:**

- Forcing the client app to run a full Trie construction loop locally using raw server data dumps.
- Implement Debouncing on keypress events paired with a short-lived client-side memory cache (e.g., LocalStorage) to store suggestions for recently typed prefixes.
- Convert all mobile client traffic to communicate via synchronous single-threaded REST channels.
- Configure the client application to poll the server gateways using raw UDP broadcast frames.

**Answer:** Implement Debouncing on keypress events paired with a short-lived client-side memory cache (e.g., LocalStorage) to store suggestions for recently typed prefixes.

## Q3: What is the primary performance downside of computing the top 5 most popular suggestions dynamically using a standard Trie traversal algorithm on the real-time query path?

**Options:**

- Standard Tries lose the ability to store alphanumeric character types inside terminal leaf blocks.
- Traversing down all possible child nodes from a given prefix and sorting them by frequency at runtime introduces a time complexity of O(V + E), creating high latency blocks under heavy concurrent traffic.
- It automatically shifts the transport protocol infrastructure from HTTPS over to raw SMTP tunnels.
- It causes immediate data block fragmentation across your persistent object storage buckets.

**Answer:** Traversing down all possible child nodes from a given prefix and sorting them by frequency at runtime introduces a time complexity of O(V + E), creating high latency blocks under heavy concurrent traffic.

## Q4: When a user types a search query and hits 'Enter', how should the phrase's popularity frequency be recorded to ensure the system is durable without slowing down the critical user search path?

**Options:**

- Execute an immediate synchronous write statement to update an auto-increment counter row in a core SQL cluster table.
- Asynchronously emit the search log event to a message broker like Apache Kafka, allowing decoupled downstream analytics pipelines to process and aggregate logs out-of-band.
- Force the client browser to keep the socket open until the master database flushes its cache disks.
- Save the data directly into temporary local system files inside the edge load balancer's host OS containers.

**Answer:** Asynchronously emit the search log event to a message broker like Apache Kafka, allowing decoupled downstream analytics pipelines to process and aggregate logs out-of-band.

## Q5: How does an analytics engine like Apache Flink blend real-time trending topics with the historical popularity scores stored inside a master Autocomplete Trie database?

**Options:**

- By executing a full database re-indexing script every 10 seconds across the global shards.
- Flink monitors short sliding windows of incoming search logs to compute velocity scores for surging keywords, pushing immediate micro-updates to override or blend with the cache tier's historical Top-K arrays.
- By dropping all historical data records automatically to make space for the fresh live parameters.
- It converts all text query fields into flat, unindexed Base64 string arrays.

**Answer:** Flink monitors short sliding windows of incoming search logs to compute velocity scores for surging keywords, pushing immediate micro-updates to override or blend with the cache tier's historical Top-K arrays.

## Q6: Why is it structurally critical to limit the maximum character depth of the distributed Autocomplete Trie (e.g., capping prefix tracking at 20 characters)?

**Options:**

- Memory caches are fundamentally unable to parse string attributes longer than 20 characters.
- It places a strict upper bound on the tree depth, ensuring the maximum search time complexity remains constant at O(1) relative to total database phrase counts, while protecting memory assets from long tail pollution.
- It changes the network transport framing structures to run over raw UDP broadcast formats.
- Longer character configurations automatically invalidate edge load balancer proxy routing configurations.

**Answer:** It places a strict upper bound on the tree depth, ensuring the maximum search time complexity remains constant at O(1) relative to total database phrase counts, while protecting memory assets from long tail pollution.

## Q7: When a business requirement demands the immediate censorship or removal of offensive suggestions from the autocomplete system, how should this be executed without introducing read-latency overhead?

**Options:**

- Rebuild the entire multi-terabyte master Trie database from scratch immediately.
- Maintain a highly optimized, bloom-filter or in-memory hash set of blocked phrases at the API Gateway or Service tier to filter out matched suggestions on the read path instantly.
- Force all client browser applications to purge their hardware local memory files every minute.
- Convert all text query fields into flat, unindexed binary rows inside relational databases.

**Answer:** Maintain a highly optimized, bloom-filter or in-memory hash set of blocked phrases at the API Gateway or Service tier to filter out matched suggestions on the read path instantly.

## Q8: If your search autocomplete service is deployed globally across multiple regions, how do you minimize lookup latency for international users while keeping suggestion metrics accurate?

**Options:**

- Route all international lookups to a single master database cluster in a single region.
- Deploy read-only replicas of the aggregated Trie cache cluster locally in each geographic region, routing user queries to the nearest region via Anycast or GeoDNS.
- Force all international user queries to run over slow, single-threaded serialized network connection lines.
- Convert the Trie cache keyspace to use random string sequences across regions.

**Answer:** Deploy read-only replicas of the aggregated Trie cache cluster locally in each geographic region, routing user queries to the nearest region via Anycast or GeoDNS.

## Q9: What is the primary trade-off when configuring your offline aggregation batch workers to run every 1 hour instead of every 24 hours?

**Options:**

- Hourly runs completely eliminate the need for rate limiters at the edge gateway tier.
- It keeps historical suggestions fresher, but massively increases compute costs and database write contention due to continuous, resource-intensive MapReduce loops.
- Hourly batch updates automatically compress text files into raw binary streaming formats.
- It forces downstream memory caches to use single-leader configuration models exclusively.

**Answer:** It keeps historical suggestions fresher, but massively increases compute costs and database write contention due to continuous, resource-intensive MapReduce loops.

## Q10: When storing pre-compiled Top-K suggestion lists inside individual Trie nodes, what happens to memory consumption compared to a standard baseline Trie data structure?

**Options:**

- Memory consumption drops significantly because child node pointers are removed.
- Memory footprint increases because each prefix node duplicates and houses string arrays of its top completions, trading RAM capacity for ultra-fast lookups.
- The memory cache automatically shifts its storage footprint onto external cold object storage disk drives.
- The total bit width of individual character fields compresses down to a single bit footprint.

**Answer:** Memory footprint increases because each prefix node duplicates and houses string arrays of its top completions, trading RAM capacity for ultra-fast lookups.

## Advanced (Staff/Principal)

## Q11: Design a trending search detection system that identifies and surfaces rapidly rising queries within minutes, not hours, without false positives from bot traffic or coordinated campaigns.

**Answer:** Use a **two-window velocity counter** in a stream processor (Flink): (1) **short window** (last 1 minute) — count query frequency via a sliding window; (2) **long window** (last 24 hours) — baseline frequency. Compute a **velocity score** = `rate_short / rate_long * entropy_factor`. The entropy factor penalizes queries with low source diversity (same IP, same user-agent, same session pattern) — bot attacks show high volume but low entropy. Implementation: each query event carries a session fingerprint (hash of IP + user-agent + a device ID if available). The stream processor maintains a HyperLogLog per query per minute to estimate unique session cardinality. The `entropy_factor = min(unique_sessions_in_minute / 10, 1.0)` — a query with 10K requests but only 5 unique sessions gets entropy_factor = 0.5, halving its velocity score. Surface the top-100 queries by velocity score every minute, updated in Redis. The autocomplete tier reads this list as a boost factor: a trending query gets a temporary popularity multiplier even if its historical absolute frequency is low.

## Q12: How would you implement multilingual autocomplete for languages with complex morphology (Arabic, German compounds, CJK) where standard prefix-based Trie lookup fails?

**Answer:** Standard prefix Tries fail because: (1) Arabic / Hebrew — right-to-left text, prefix lookup needs to start from the first character of the word, which for RTL is the visually rightmost character; (2) German — compound words like "Donaudampfschifffahrtsgesellschaft" make prefix trees deep and memory-heavy; (3) CJK (Chinese, Japanese, Korean) — no spaces between words; characters form multi-character tokens. Solution: (1) for RTL — store the string in its logical order (not display order). A Trie works fine if the client sends the typed prefix in logical order. Alternatively, store a **reverse Trie** keyed by reversed string for RTL client preprocessing. (2) for German compounds — use a **segmentation-aware Trie**: during indexing, segment compound words into their constituent parts using a language-specific compound splitter (e.g., Google's "Morphy" or CC-CEDICT for CJK). The Trie stores both the full word and the segments as separate entries. For autocomplete, if a user types half a compound, suggest the full compound. (3) for CJK — implement a **character n-gram index** (2-grams or 3-grams of characters) stored in a Bloom filter-backed lookup table. On user input, break the input into overlapping n-grams, query the index, and return completion candidates. This trades memory for high recall. For all languages, deploy **per-language Trie shards** (separate Redis instances) and route based on the client's `Accept-Language` header or keyboard locale.

## Q13: Design a personalization layer for autocomplete that blends global popularity with user-specific search history without doubling cache storage.

**Answer:** Use a **blended ranking** at read time: the autocomplete response is a merge of (1) a global popularity list (Top-K from the master Trie) and (2) a user-specific recent search list (stored in a small per-user Redis list, last 200 searches). The merge is done by interleaving: position 1 = user's top match, positions 2-3 = global top-2, position 4 = user's 2nd match, etc. This avoids storing a personalized Trie per user. Storage: the global Trie is a single instance (or sharded by prefix). The per-user recent searches list is `key: user:{id}:recent_searches` stored as a Redis List with LTRIM to cap at 200. For 1B users, this is `200 items × ~50 bytes × 1B = 10TB` — too large for Redis. Optimize: only store per-user lists for **active users** (logged in within 7 days). For cold users, serve global-only suggestions. Active users are ~10% of total → ~1TB → feasible with Redis Cluster (~20 nodes × 50GB). Use **Redis on Flash** (or Dragonfly) for cost-efficient memory. Blend weights: `score = 0.7 * global_score + 0.3 * user_afﬁnity_score`. The user affinity score decays by session recency (last 10 searches weighted 5x older ones).

## Q14: How do you handle profanity, hate speech, and NSFW suggestions in autocomplete while maintaining low false-positive rates? Design the real-time filtering pipeline.

**Answer:** **Multi-stage filter**: (1) **pre-filter** — a Bloom filter of blocked exact phrases (tens of thousands of entries, <1MB). Any autocomplete candidate matching a phrase in the filter is rejected in O(1). (2) **regex classifier** — a compiled set of regex patterns for variants (leetspeak, character substitution: "h4t3", "f*ck"). This catches intentional obfuscation. (3) **ML semantic classifier** — a lightweight ONNX model (DistilBERT distilled to 10MB) that scores each candidate for toxicity. Score > 0.5 → blocked. Run on the top-100 global candidates every batch update cycle (not per-query). Cache the classification result alongside the candidate in the Trie. (4) **override list** — a manually curated allowlist for false-positive terms that are valid in context (e.g., "cock" in "cocktail recipe", "bastard" in legitimate cooking content). Maintained by a moderation team with an audit trail. At query time, the stack runs in sequence: Bloom filter (sub-μs) → regex (μs) → skip ML because result is cached. Total filter overhead per candidate: <5μs. For high-traffic prefixes, the filtered results are pre-cached: the Trie node's top-K list excludes blocked terms entirely, so the read path never even encounters them.

## Q15: Describe how you would A/B test different ranking algorithms for autocomplete suggestions without disrupting the live serving path or requiring a shadow deployment.

**Answer:** **Layer-based A/B testing** built into the serving stack: (1) each autocomplete request carries a `test_bucket` header (set by a deterministic hash of user_id, enabling consistent routing). (2) The serving layer processes all ranking algorithms (control + variants) in parallel for a single request. The variant's results are logged (Kafka) but NOT returned to the user — only the control (current production) is returned. This is called **inference-only shadow mode**. (3) Compare metrics: control vs. variant on identical request logs. Key metrics: **selection rate** (did the user click a suggestion?), **zero-input rate** (did they ignore suggestions and type the full query?), **best-prefix match** (was the top suggestion the one the user ultimately searched?). (4) safety checks — if the variant's results contain toxic/sensitive content that the control filtered, trigger an alert. (5) gradual rollout — when the variant shows statistically significant improvement (p < 0.01, measured over 1M requests), flip the serving path to return the variant to 5% of users via a feature flag. Monitor p99 latency (variant must not degrade beyond +2ms), error rate, and business metrics. Fully roll out after 1 week of stable data. **Rollback**: flip the feature flag off — the control algorithm is always deployed and ready to serve 100%.

## Q16: Your autocomplete service uses a Trie stored in Redis. During a traffic spike, a single hot prefix (e.g., "a") receives 1M queries/sec. The Redis node serving this shard becomes CPU-bound and latency spikes to 500ms p99. How do you shard a Trie by prefix without breaking prefix scanning?

**Answer:** **Prefix-based Trie sharding with query routing**: (1) **static prefix split** — shard the Trie by the first N characters. For example, 26 shards for first character (a-z), or 676 shards for first two characters (aa-zz). The hot prefix "a" maps to shard "a". (2) **hot shard splitting** — when a shard ("a") exceeds a CPU/latency threshold, split it into sub-shards: "aa", "ab", ... "az". Each sub-shard is stored on a separate Redis node. The routing layer maintains a mapping: `prefix_pattern → shard_id`. Queries for "a" are **fanned out to all sub-shards** and merged. Since "a" would fan out to 26 sub-shards, this increases query latency by ~1ms (parallel, not sequential). (3) **two-level routing** — the API gateway has a local cache of the routing table: `shard_map = {"a*": ["redis-a"], "b*": ["redis-b"], ...}`. On cache miss, query a routing service (etcd). (4) **bloom filter per shard** — each sub-shard maintains a Bloom filter of top-100K queries it contains. For a prefix query, the gateway first checks the Bloom filters to determine which sub-shards have relevant completions, skipping empty shards. For single-character queries ("a"), only 20% of sub-shards may have data → 80% reduction in fan-out. (5) **precomputed top-K per shard** — for each sub-shard, precompute the top-100 completions and cache them in the gateway. 80% of queries for "a" can be served from the local cache without hitting Redis. (6) **principal insight**: Tries are fundamentally hard to shard because prefix relationships create cross-shard dependencies. Accept that a single-character prefix will always require fan-out. The solution is to (a) minimize fan-out with Bloom filters, (b) cache aggressively, and (c) throw more CPU at the hot shards via further sub-sharding.

## Q17: You discover that your autocomplete system is being gamed by SEO spammers: they search for trending queries repeatedly, artificially inflating their frequency and causing their spam sites to appear as suggestions. How do you design a spam-resistant frequency counter?

**Answer:** **Anomaly-resistant frequency counting**: (1) **per-session deduplication** — count each query at most once per user session (bounded by a 5-minute sliding window). A spammer running 10K queries from one session only increments the counter once. (2) **IP diversity requirement** — a query's frequency is weighted by the number of distinct IPs (/24 subnet) that submitted it. If 10K queries come from the same /24 subnet, they count as 1 "vote" for frequency purposes. Use HyperLogLog to estimate distinct IPs per query per window efficiently. (3) **velocity anomaly detection** — track the `frequency_velocity` (queries per minute) for each query. If the velocity exceeds 5σ (standard deviations) from the historical baseline for that query, apply a **discount factor**: `count *= 0.1` for the current window. This prevents sudden spam spikes from affecting the autocomplete ranking. (4) **manual blocklist override** — maintain a blocklist of queries that are known spam (updated by the moderation team, deployed as a Bloom filter). Blocklisted queries never appear as suggestions. (5) **temporal decay** — even legitimate trending queries decay rapidly. Use an exponential decay function: `score = sum(e^(-λ * (now - t_i)))` where λ is chosen such that a query from 24 hours ago has 10% weight. This prevents spam that happened yesterday from lingering. (6) **audit** — daily report of the top-100 queries by `velocity_score`. Review manually for anomalies. If a query looks suspicious, investigate the top contributing sessions/IPs. (7) **monitoring** — `spam_detection_alert_count`. If >10 queries per day are flagged as spam velocity anomalies, the anti-spam parameters need tuning.

## Q18: You are asked to build an autocomplete system that supports "did you mean?" spelling correction for misspelled queries. How do you implement this without adding >5ms p99 latency to the autocomplete response?

**Answer:** **Precomputed spelling correction index**: (1) **offline dictionary** — at build time, generate a **spelling correction map** from your query log: for each correctly spelled query, precompute its **noisy variants** (edit distance 1 and 2: insertions, deletions, substitutions, transpositions). Map each variant → original query. This is a massive but offline operation. (2) **index in Redis** — store the map in Redis as a hash: `spelling:{variant} → original_query`. The map only needs to cover the top-1M queries (which cover 95% of search traffic). For queries outside the top-1M, skip spelling correction. (3) **read path** — when a query is typed, the autocomplete service: (a) first checks the Trie for completions on the raw prefix; (b) simultaneously checks the spelling correction map for the full typed string (if the user has paused >200ms, indicating they finished typing). If a correction is found AND the original prefix has 0 completions (no matches), return the corrected suggestion as a "did you mean?" item. (4) **latency control** — both lookups are parallel. Trie lookup: ~1ms. Spelling hash lookup: single Redis GET (<1ms). The combined latency is <2ms — well within the 5ms budget. (5) **false positive mitigation** — only suggest a correction if the original query has zero results. If "amazon" is a valid query with results, never correct it even if the spelling map suggests "amazon → amazon.com" (irrelevant). (6) **performance monitoring** — track `spelling_correction_latency_p99` and `spelling_correction_acceptance_rate` (how often users click the "did you mean?" suggestion). If acceptance rate < 1%, the spelling map is noisy and needs tuning.

## Q19: Your autocomplete Trie is 500GB in memory and growing 10% monthly. You need to keep the entire index in memory for latency SLA. The infrastructure budget is fixed. Design a memory reduction strategy that cuts the footprint by 50% without changing the data structure fundamentally.

**Answer:** **Trie compression techniques**: (1) **static dictionary encoding** — replace common substrings (word stems, suffixes) with 2-byte dictionary tokens. For example, "ing", "tion", "ment", "pre" appear in many English queries → encode them as single 2-byte references instead of repeating the characters. This compresses Trie nodes by ~30%. (2) **prefix deduplication** — in a standard Trie, nodes for "app", "apple", "application" share the "app" path, but each node stores a child pointer array (26 or 52 slots). Use a **compressed Trie (Radix Tree)** : merge single-child nodes into a single node with a label. For example, "a-p-p" are 3 separate nodes with single children; compress into one node "app". This alone reduces node count by 40-60%. (3) **variable-length node encoding** — instead of storing a 256-entry array per node (for ASCII/Unicode), store only a sorted list of existing children (2-4 bytes per child). Use a custom binary format: `child_count (1 byte) + [(char, pointer)]*N`. For nodes with <10 children (which is >90% of Trie nodes), this uses ~30 bytes vs 256 bytes — ~8× savings. (4) **off-heap storage** — store the Trie in **memory-mapped files** (off-heap) rather than in Go heap / Redis Strings. This avoids GC pressure and allows the OS to page out cold Trie branches under memory pressure. Use `mmap` with `MADV_RANDOM` for the cold regions and `MADV_WILLNEED` for hot prefixes. (5) **frequency-triggered pruning** — if a query has zero frequency for 90 days, remove it from the Trie. This cuts ~20% of stale queries annually. Retain only the top-5M queries (covers 98% of search traffic). (6) **compression results** — Radix Tree + variable-length encoding + static dictionary: total compression ~3.5:1. 500GB → ~143GB. Combined with frequency pruning: ~115GB. Under budget. (7) **monitoring** — track `trie_memory_bytes` and `trie_node_count`. Alert if compression ratio drops (e.g., more multi-byte Unicode queries from international users).

## Q20: Your autocomplete service is deployed globally. A user in Japan types "東" (the first character of "Tokyo" in Japanese). The autocomplete should suggest "東京", "東京都", "東日本", etc. However, your Trie is built from English queries and does not cover CJK characters well. Design a multilingual autocomplete that handles CJK, Arabic, and emoji input gracefully.

**Answer:** **Unicode-aware Trie with character n-gram index**: (1) **CJK challenge** — CJK characters represent whole words, not letters. A prefix Trie on individual characters works, but the branching factor is huge (50K+ CJK characters). A Trie node for "東" would have thousands of children → memory explosion. Solution: use a **bigram/trigram index** instead of a character Trie. For each CJK query, break it into overlapping 2-grams: "東京" → ["東京", "京都"]. Store 2-grams as keys in a hash map, each pointing to a sorted set of completions. (2) **read path** — for input "東", the system queries `2-gram_index["東"]` (all 2-grams starting with 東). This returns ["東京", "東京都", "東日本", ...] sorted by frequency. Performance: single hash lookup + ZRANGE → <2ms. (3) **Arabic/Farsi** — Arabic joins characters contextually (initial, medial, final forms). Normalize input by converting to Unicode NFC normalization (decomposed form) and strip diacritics. Use the same n-gram index approach. (4) **emoji** — emoji are multi-byte Unicode sequences. Store them as-is in a separate **emoji index** (a smaller hash map keyed by complete emoji or emoji sequences). On input, if the character is classified as an emoji (Unicode block `Emoticons`, `Miscellaneous Symbols`, etc.), query the emoji index instead of the Trie. (5) **language detection** — at the API gateway, classify the input's script via Unicode block detection (CJK: `\p{Han}`, Arabic: `\p{Arabic}`, Latin: `\p{Latin}`). Route to the appropriate index. For mixed input (e.g., "東京 2024"), query both CJK and Latin indices and merge results. (6) **storage** — CJK n-gram index: ~50GB (compressed). Arabic index: ~10GB. Emoji index: <1GB. Latin Trie: ~150GB. Total: ~210GB — feasible for a single Redis Cluster. (7) **monitoring** — track `autocomplete_p99_by_language`. CJK and Arabic should be <10ms. If not, the n-gram index may need optimization (more shards for hot CJK prefixes).

