# Chapter 11 â€” Design A News Feed System

## Q1: When designing a hybrid Fan-Out engine, how should the system dynamically classify an account as a 'celebrity' or high fan-out target to shift them from a Push to a Pull model?

**Options:**

- By calculating the exact string byte length of the user's display name parameters.
- By applying a dynamic threshold based on raw follower counts and real-time account activity, flagging high-degree graph nodes to bypass the write fan-out queue.
- By running a synchronous full-table scan across the post history database during every write request.
- By forcing all accounts created within the last 30 days to use a pull model exclusively.

**Answer:** By applying a dynamic threshold based on raw follower counts and real-time account activity, flagging high-degree graph nodes to bypass the write fan-out queue.

## Q2: To store a user's pre-compiled news feed timeline in a Redis cluster with maximum memory efficiency and fast pagination support, which data structure represents the best operational choice?

**Options:**

- A standard Redis String containing a large serialized JSON array of all historical posts.
- A Redis Sorted Set (ZSET) using the post creation timestamp as the score and the 'post_id' as the member value.
- A flat Redis Hash mapping sequential integer keys to individual raw text payloads.
- A Redis HyperLogLog structure to maintain chronological appending logic.

**Answer:** A Redis Sorted Set (ZSET) using the post creation timestamp as the score and the 'post_id' as the member value.

## Q3: A user follows 5,000 active accounts, creating a massive fan-out read merge step if they utilize a pull model. How can you mitigate the read latency of merging these timelines during feed generation?

**Options:**

- Execute 5,000 synchronous individual database SELECT queries sequentially in a linear loop.
- Parallelize the timeline fetch operations using a scatter-gather pattern with asynchronous workers, combined with strict max-age time limits to only fetch recent active windows.
- Convert all post timelines into a single unified global monolithic table across one database shard.
- Force the client browser to make individual network calls to each of the 5,000 followed user accounts.

**Answer:** Parallelize the timeline fetch operations using a scatter-gather pattern with asynchronous workers, combined with strict max-age time limits to only fetch recent active windows.

## Q4: How do you enforce a hard ceiling on cache memory consumption for inactive users who haven't logged into the news feed application for months?

**Options:**

- Maintain their feeds permanently in high-cost memory arrays to ensure zero-latency retrieval whenever they return.
- Configure an aggressive Time-To-Live (TTL) on timeline caches, allowing inactive feeds to expire from memory; dynamically reconstruct their feed from cold database storage only when they authenticate again.
- Run a cron job that randomizes the keyspace characters of inactive users to trigger background eviction errors.
- Move the inactive timelines into a high-speed local UDP broadcast buffer ring.

**Answer:** Configure an aggressive Time-To-Live (TTL) on timeline caches, allowing inactive feeds to expire from memory; dynamically reconstruct their feed from cold database storage only when they authenticate again.

## Q5: What is the primary architectural benefit of utilizing 'Feed Pagination' based on a Cursor token (e.g., max_id = post_12345) rather than a simple numeric offset (e.g., LIMIT 10 OFFSET 20)?

**Options:**

- Cursor pagination encrypts the underlying data payloads to defend against interceptors.
- Numeric offsets cause duplicate entries or skipped items if new posts are published while a user is actively scrolling their feed.
- Offset pagination requires more network bandwidth because it expands the underlying TCP window sizes.
- Cursors automatically index unindexed non-relational database tables across distributed shards.

**Answer:** Numeric offsets cause duplicate entries or skipped items if new posts are published while a user is actively scrolling their feed.

## Q6: When a user deletes a published post, how should the Fan-Out engine clean up the pre-compiled timelines cached inside Redis across millions of followers?

**Options:**

- The system runs a synchronous sweep across all cache clusters, deleting the keys completely.
- An asynchronous worker pool consumes a post-deletion event from Kafka and issues optimized background `ZREM` batch updates to remove that specific post_id from active follower sets.
- The system drops all database index metrics to reset the keyspace.
- The system forces client devices to undergo an immediate factory data restore loop.

**Answer:** An asynchronous worker pool consumes a post-deletion event from Kafka and issues optimized background `ZREM` batch updates to remove that specific post_id from active follower sets.

## Q7: What is the core downside of constructing a news feed using a pure client-side pulling structure, where the device merges posts from all creators dynamically at runtime?

**Options:**

- It prevents the browser from formatting human-readable text layers properly.
- It shifts the heavy computing and network retrieval burden completely to the mobile device, resulting in massive bandwidth consumption, slow loading speeds, and battery drain.
- It automatically transitions low-level network transport loops from HTTPS over to raw SMTP.
- It requires cloud providers to drop multi-region database replication layers entirely.

**Answer:** It shifts the heavy computing and network retrieval burden completely to the mobile device, resulting in massive bandwidth consumption, slow loading speeds, and battery drain.

## Q8: When sharding the primary database that houses historical user posts, which column parameter ensures uniform data scattering across NoSQL cluster rings?

**Options:**

- The raw byte length of the post text payload attributes.
- The unique `post_id` or a composite key of `user_id + post_id`, spreading rows evenly via consistent hashing.
- The global 'created_at' date tracking string values.
- The creator account's public timezone region text block parameters.

**Answer:** The unique `post_id` or a composite key of `user_id + post_id`, spreading rows evenly via consistent hashing.

## Q9: How do social platforms include highly popular 'Sponsored Ad Posts' into a user's pre-compiled timeline cache cleanly?

**Options:**

- Ads are injected into the pre-compiled feed array dynamically by the application layer at retrieval time, separating ad delivery from standard post data.
- Every single advertisement is hard-copied into the timeline sets of all global users permanently.
- Ads are streamed via separate raw UDP broadcast loops to the browser client.
- The cache tier wipes out all standard post items to leave space for ad frames exclusively.

**Answer:** Ads are injected into the pre-compiled feed array dynamically by the application layer at retrieval time, separating ad delivery from standard post data.

## Q10: What performance metrics indicate that your News Feed system cache cluster is suffering from memory fragmentation or key exhaustion?

**Options:**

- A sharp drop in cache hit ratio paired with elevated latency spikes as requests pass through to primary relational storage rings.
- A sudden, automated transition of network proxy endpoints to loopback addresses.
- An immediate expansion of the raw text field lengths inside metadata tables.
- A mandatory hard reboot requirement registering on external firewall setups.

**Answer:** A sharp drop in cache hit ratio paired with elevated latency spikes as requests pass through to primary relational storage rings.

## Advanced (Staff/Principal)

## Q11: Design a feed ranking algorithm that combines recency, relevance, engagement signals, and explicit user preferences at read time without pre-computing all possibilities.

**Answer:** Use a **two-stage ranking pipeline**: (1) **candidate generation** — pre-compute a candidate pool (e.g., 500 most recent posts from followed accounts + sponsored candidates). This pool is assembled at write time for the push model (pre-compiled feed) or at read time for the pull model (scatter-gather from followed accounts). (2) **real-time scoring** — at feed read time, score each candidate using a lightweight **linear model** (or XGBoost model exported as ONNX) with features: `recency_score = decay(time_since_post)`, `engagement_score = likes * w1 + comments * w2 + shares * w3`, `affinity_score = user_embedding · post_author_embedding` (precomputed daily via collaborative filtering), `content_interests = cosine_sim(user_topic_vector, post_topic_vector)`, `explicit_prefs = boost_certain_topics + dedup_past_interactions`. The model runs in under 10ms for 500 candidates using SIMD-optimized dot products (or an ANN index). This avoids pre-computing all ranking combinations — only ~1% of users have their feed fully personalized in real-time; the rest use a cached tiered ranking that is recomputed lazily.

## Q12: How would you implement a real-time "seen state" tracker that shows users which posts they've already viewed across devices without storing per-user-per-post booleans at scale?

**Answer:** Use a **Bloom filter per user** stored in Redis. When a user views a post, add `post_id` to their Bloom filter. On feed render, check each feed item against the filter — if the filter says "seen", hide it (or show a dimmed indicator). Bloom filter parameters: 1% false positive rate → ~10 bits per post → 10,000 viewed posts per user = ~12.5KB per user. For 1B users: ~12.5TB total → sharded across a Redis cluster (~125 nodes × 100GB). Trade-off: false positives (1%) cause some unread posts to appear read — acceptable for UX. For **cross-device sync**, the Bloom filter is a CRDT: merging two filters is a bitwise OR operation. When a user views a post on mobile, the mobile client sends an `OR` delta to the server, which merges into the user's canonical filter. Offline support: the client maintains a local Bloom filter and syncs on reconnect. For **high-value indicators** (e.g., unread count badge), use a precise counter (Redis INCR) alongside the approximate filter.

## Q13: Design a feed system that supports undo/soft-delete: when a user deletes a post, how do you ensure it disappears from all followers' feeds within seconds across a global deployment?

**Answer:** **Fan-out of deletion** must match fan-out of creation. Use a **dedicated deletion queue** in Kafka partitioned by `author_id`. On post deletion, the feed service publishes a `post_deleted(author_id, post_id)` event. Global fan-out: (1) each feed worker consumes from the partition and, for every follower whose pre-compiled feed is in Redis, issues `ZREM(post_id)` on the follower's feed sorted set. (2) for followers whose feeds are not cached (inactive), update a **deleted_posts Bloom filter per user** (same structure as Q12) — the feed is reconstructed from cold storage on next login, and the filter ensures the deleted post is excluded. Targeting sub-second global deletion: use a **multi-region Kafka MirrorMaker** to propagate the deletion event to all regions' feed workers. Each region independently processes `ZREM`. For viral accounts with millions of followers: (1) skip direct fan-out; instead, post a `blocked_posts:{post_id}` entry in Redis (TTL 7 days). Any feed render for any user checks this set for blocked posts — this avoids 10M `ZREM` calls. (2) The blocked post entry is replicated via cross-region Redis replication (CRDT-based) automatically.

## Q14: How do you handle a follower count that swings wildly (e.g., a bot purge removes millions of fake followers)? Design a system that absorbs the feed cache invalidation storm.

**Answer:** **Lazy invalidation with version stamps**: each user has a `follower_set_version` (monotonically increasing integer stored in Redis). When followers are removed (bot purge), increment `follower_set_version` — do NOT immediately rebuild feeds. On the next read of a follower's feed, the feed service checks if the reader's `follower_set_version` for the account matches the cached feed's `version_stamp`. If mismatched, the feed is **stale** and must be rebuilt: remove posts from purged bots from the pre-compiled feed and re-rank. The rebuild is triggered **per-reader, lazily** — the thundering herd is spread out over the natural read pattern of all followers. For high-traffic readers (celebrities), proactively warm: use a background worker that processes the largest fan-out accounts first, with a rate limit (e.g., 100K feed rebuilds per minute). Monitor: track `pending_feed_rebuilds` per account. If a bot purge removes 50M followers from a single account, the rebuild backlog may take hours — this is acceptable because the "follower count" in the UI is detached from feed computation and can be updated instantly.

## Q15: Describe the algorithmic and infrastructure challenges of injecting sponsored content into feeds while maintaining a hard latency SLA of 200ms p99 read time.

**Answer:** Algorithmic challenges: (1) **relevance vs. latency** — the ad selection model (CTR prediction, budget pacing, audience targeting) is computationally expensive. Offload to a separate **ad serving tier** with precomputed ad candidates per user (top 50 ads scored offline). At feed read time, the feed service calls the ad tier in parallel with feed generation, merging sponsored posts at the correct positions (e.g., every 10th organic post). (2) **position smoothing** — the ad must appear at a deterministic rank without re-sorting the entire feed. Use **reservoir sampling** for organic → inline ad at the target position. Infrastructure challenges: (3) **sub-200ms p99** — the feed service must fan-out to both the organic feed cache and the ad tier concurrently (Go goroutines or async Rust). Use a **deadline propagation** pattern: if the ad tier hasn't responded within 150ms, serve the feed without ads (graceful degradation). (4) **global budget pacing** — an ad campaign has a daily budget, but the feed service is distributed across 1000s of nodes. Use a **local token bucket** per node (refreshed every minute from a global Redis counter). The budget sync is eventually consistent; accept small overspend (bounded by 1 minute × provisioned throughput). (5) **auditing** — every ad impression must be logged for billing (Kafka → Flink → hourly aggregated billing). The logging path must not block the user-facing read path; use async writes with a ring buffer.

## Q16: You are designing a news feed for a platform that has both "following" and "friendship" graphs (like Twitter + Facebook combined). A user follows 500 celebrities and has 200 friends. How does the fan-out strategy differ between the two relationship types, and how do you merge the two feed sources into a single ranked timeline?

**Answer:** **Dual-graph fan-out**: (1) **following graph (asymmetric, many-to-many)** — use **pull model** for high-follower accounts (celebrities with >10K followers). When the user opens their feed, scatter-gather the latest 50 posts from each followed celebrity (capped at 200 followed accounts → 200 * 50 = 10K posts to rank). For the 500 celebrities the user follows, but 300 have <10K followers, use push for those (pre-compile feed into Redis sorted set). (2) **friendship graph (symmetric, dense)** — use **push model** for friends (typically <500 friends). When a friend posts, fan-out to all their friends' pre-compiled timelines. (3) **merge strategy** — the feed display is a **blended timeline**: interleave friend posts and celebrity posts according to a ranking score. Use a **weighted interleaving algorithm**: every 3rd position in the timeline is reserved for friends (to prevent celebrity content drowning out personal updates). The ranking model assigns a `relationship_type` feature: friend posts get a +0.2 boost to the base relevance score, ensuring they are not deprioritized by high-engagement celebrity content. (4) **control knobs** — user can toggle "show friends first" (chronological friends-only section at the top) or "show best of both" (blended ranked). (5) **monitoring** — track `friend_post_visibility_rate` (are friend posts appearing in the top 20?). If it drops below 10% for a user, they are likely experiencing "celebrity drowning" — adjust the blend ratio for that user.

## Q17: Your news feed system uses a machine learning model to rank posts. A bug in the feature engineering pipeline causes all posts from a particular political party to be systematically suppressed. The bug is discovered by a journalist 3 months later. Design a monitoring and auditing system that detects this class of algorithmic bias within hours, not months.

**Answer:** **Algorithmic fairness monitoring**: (1) **distributional parity monitoring** — for every sensitive attribute (political affiliation, race, gender, age group), track `exposure_distribution` — the proportion of feed impressions that contain content from each group. Compare against the **baseline distribution** (the proportion of content created by each group in the user's follow graph). If `exposure_distribution` diverges from `baseline_distribution` by >5% for any group, trigger an alert. (2) **counterfactual logging** — for every feed request, log the **top-50 ranked candidates BEFORE the ML model reranks them** (the raw recall set). Also log the **top-20 after reranking**. Store both sets in a log (compressed, daily partitioned in S3). This allows post-hoc analysis: "Did the model demote content from group X between recall and ranking?" (3) **automated bias audit** — a daily batch job reads the counterfactual logs and computes: `demotion_rate(group) = (count_in_recall - count_in_final) / count_in_recall`. Alert if `demotion_rate` for any group is >2× the average demotion rate. (4) **holdout set** — maintain a set of **audit users** (1% of traffic) who receive an **unbiased ranking** (random order or chronological). Compare their engagement metrics against the ML-ranked users. If the ML-ranked users show systematically lower engagement with content from certain groups, the model has bias. (5) **external audit API** — provide a secure API where trusted third-party auditors can run their own fairness analysis on anonymized log data. Publish a bi-annual transparency report with aggregate fairness metrics. (6) **incident response** — when a bias alert triggers, automatically pause the model and fall back to a simple recency-based ranking. Investigate the feature pipeline, fix the bug, and re-deploy. The model must pass a fairness validation gate before being re-enabled.

## Q18: You notice that a user's news feed takes 5 seconds to load because they follow 50,000 accounts. Most accounts produce <1 post per day, but the scatter-gather fan-out must query 50K recent-post lists. How do you reduce this to <500ms without changing the pull model?

**Answer:** **Hierarchical aggregation with bloom filters**: (1) **interest clustering** — group the followed accounts into topics (using a precomputed account→topic mapping, e.g., "tech", "sports", "news"). The user follows 50K accounts, but these map to ~100 topics. Query the topic-level recent post lists instead (100 queries instead of 50K). At read time, fetch the latest 20 posts from each of the 100 topics, then deduplicate and rank. (2) **bloom filter dedup at query time** — before scatter-gathering, get the user's last-seen-post-IDs (a Bloom filter of the last 5000 seen post IDs). The scatter-gather queries include this Bloom filter; the storage layer pre-filters out already-seen posts, reducing the result set size by ~70%. (3) **cached feed for heavy users** — for users who follow >10K accounts, proactively maintain a pre-compiled feed (push model) for the top-1000 most recently active followed accounts, and only scatter-gather the remaining 49K lazily. The pre-compiled portion covers 80% of fresh content with 2% of the queries. (4) **parallelism + deadline** — issue all 100 topic-level queries concurrently (goroutines / async). Set a strict deadline of 300ms for all queries. If any query exceeds the deadline, return the partial results (the user sees "loading more..." for the rest). (5) **materialized view in Cassandra** — store each account's recent posts in a Cassandra table with `(account_id, post_timestamp)` as the clustering key. A query for "latest 20 posts from account X" is a single Cassandra range query (very fast). With 100 concurrent queries, total latency is dominated by the slowest query (~100ms at p99). (6) **monitoring** — `feed_load_time_per_user_follow_count`. If the 50K-follower user's load time exceeds 500ms, apply one of the above optimizations retroactively via feature flags.

## Q19: Your news feed platform is growing 10% MoM. At current growth rates, the Redis cluster storing pre-compiled feeds will run out of memory in 6 months. You cannot reduce TTLs or drop features. Design a capacity scaling plan that costs <2× current spend.

**Answer:** **Tiered memory architecture**: (1) **hot/warm split** — move pre-compiled feeds from Redis (RAM) to **Redis on Flash** (or **Dragonfly with SSD tiering**). Active users (logged in within 24 hours, ~20% of all users) stay in RAM. Inactive users (80%) have their feeds stored on SSD with a RAM cache for recently accessed items. This reduces RAM requirement by 60% (20% of users × 100% RAM + 80% of users × 10% RAM = 28% of current RAM). (2) **feed compression** — pre-compiled feeds are sorted sets of `(post_id, score)`. Instead of storing the full feed, store a **delta-encoded bitmask** of post IDs relative to a baseline. Use variable-length integer encoding (Varint). This compresses the feed representation by 4:1. A feed of 500 posts goes from ~8KB to ~2KB. (3) **incremental feed building** — instead of maintaining a complete pre-compiled feed for every user, maintain only the **delta log** (new posts since last access). On user login, merge the baseline feed (last full snapshot) + delta log = fresh feed. The delta log is much smaller (only posts from last 24 hours). (4) **per-user memory budget** — enforce a maximum feed size of 1000 posts per user. Beyond that, truncate the oldest entries. Most users never scroll past 200 posts anyway. (5) **cost projection** — current spend: $X/month on Redis. With tiered storage (Redis on Flash is ~3× cheaper per GB than RAM): $X × 0.28 (RAM reduction) × 0.33 (flash cost factor) + $X × 0.72 (flash at 0.33 cost) ≈ $0.43X. Combined with compression (4:1) → $0.11X. Total: ~$0.54X. Well under the 2× budget constraint. (6) **monitoring** — track `redis_memory_usage_growth_rate` monthly. If it exceeds 5%, review whether compression ratios are degrading (more image-heavy feeds) or user growth is accelerating.

## Q20: A user reports that their feed shows a post from an account they explicitly blocked 2 years ago. Investigation reveals that the post was "re-shared" by a friend, and the feed ranking model boosted it because of high engagement from the friend's network. The block was bypassed. How do you enforce hard privacy boundaries without degrading the ranking model's effectiveness?

**Answer:** **Hard block filter at the retrieval layer**: (1) **blocklist check before ranking** — the user's blocklist (stored in Redis as a Bloom filter for fast lookup) is checked against every candidate post's author_id BEFORE the post enters the ranking model. If `author_id` is in the blocklist, the post is **removed from the candidate set entirely**. This is non-negotiable — the ranking model never sees blocked accounts, even in re-shared form. (2) **re-share propagation check** — when a friend re-shares a blocked account's post, the system must detect the **original author**. Store the `original_author_id` in the post metadata (even for re-shares). The blocklist check includes both `author_id` and `original_author_id` — if either is blocked, suppress the post. (3) **user-facing feedback** — when a suppressed re-shared post is relevant to the explanation, show the user: "[Friend] shared a post, but it was hidden because it originated from an account you blocked." This builds trust in the block feature. (4) **testing** — add a unit test: "FeedForUserWithBlocklist: given a re-shared post from blocked original author, verify it is excluded from the candidate set." Also a regression test: if an account is newly blocked, verify that all posts from that account (including past re-shares) are removed from the user's pre-compiled feed within 60 seconds. (5) **privacy audit** — quarterly, randomly sample 10K users and verify that their feed contains zero posts from their blocklisted accounts. If any violation is found, escalate to the engineering director. (6) **principal-level insight**: blocklists are a **hard privacy boundary**, not a ranking signal. They must be enforced before the ranking model, not within it. The ranking model should never be allowed to "overrule" a block — that breaks user trust fundamentally.

