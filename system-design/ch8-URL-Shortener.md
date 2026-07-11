# Chapter 8 â€” Design A URL Shortener

## Q1: When serving global redirects from a URL shortener, should you use an HTTP 301 Permanent Redirect or an HTTP 302 Found Redirect if you must capture comprehensive click analytics?

**Options:**

- HTTP 301, because browsers cache the redirect, reducing your egress network bandwidth costs drastically.
- HTTP 302, because browsers will consistently hit your backend infrastructure for every click, allowing you to accurately track click counts and user agent metadata.
- HTTP 301, because modern browsers append downstream analytical tracking tokens automatically to permanent redirect payloads.
- HTTP 307, because it forces the browser to transition from a GET request to a POST request to deliver analytic cookies.

**Answer:** HTTP 302, because browsers will consistently hit your backend infrastructure for every click, allowing you to accurately track click counts and user agent metadata.

## Q2: To scale reads for a viral short link that receives 500,000 requests per second globally, which caching eviction strategy is most appropriate for the distributed Redis layer handling the mapping metadata?

**Options:**

- FIFO (First In, First Out), to ensure stale links are purged strictly based on their creation sequence.
- LRU (Least Recently Used) or LFU (Least Frequently Used), to guarantee that active, high-traffic URL mappings remain hot in memory while dead links naturally phase out.
- Random Eviction, because it reduces the CPU overhead of keeping track of memory key access ordering structures.
- TTL-only eviction with zero memory cap flags configured on the cluster nodes.

**Answer:** LRU (Least Recently Used) or LFU (Least Frequently Used), to guarantee that active, high-traffic URL mappings remain hot in memory while dead links naturally phase out.

## Q3: If you utilize a NoSQL wide-column database like Apache Cassandra to store the short URL data, what should be designated as your Partition Key to achieve uniform data distribution across the ring cluster?

**Options:**

- The target 'long_url' string parameter, to group similar destinations onto identical storage physical nodes.
- The generated 'short_code' token, because its distributed hashing ensures predictable, random, and uniform scattering across the cluster nodes.
- The 'created_at' timestamp field, so that historical queries can scan adjacent rows consecutively.
- The user ID of the link creator, ensuring that corporate accounts have isolated table storage spaces.

**Answer:** The generated 'short_code' token, because its distributed hashing ensures predictable, random, and uniform scattering across the cluster nodes.

## Q4: A Cache Stampede (Thundering Herd) risk occurs when a viral short link's cache key expires, forcing thousands of concurrent app requests to compute or fetch the long URL from the database simultaneously. How do you mitigate this at Staff scale?

**Options:**

- Increase the database pool size to allow unlimited concurrent processing connections.
- Implement probabilistic early expiration (XFetch) or use a mutex lock (single-flight pattern) so only one worker updates the cache while others wait or read old data.
- Convert all database operations to run on synchronous serial read lines.
- Configure the browser clients to run exponential backoff calculations on the client-side UI redirect tier.

**Answer:** Implement probabilistic early expiration (XFetch) or use a mutex lock (single-flight pattern) so only one worker updates the cache while others wait or read old data.

## Q5: Why is Base62 encoding preferred over standard Hexadecimal (Base16) or Base64 encoding for generating public short links?

**Options:**

- Base62 offers more complex encryption parameters to defend against reverse engineering attacks.
- Base62 significantly maximizes character density per bit compared to Base16, while avoiding confusing special characters (like '+' or '/') used in Base64 that can break URL path string parsing.
- Base62 integrates directly with standard hardware register structures to accelerate indexing operations.
- Base64 generation introduces a mandatory network round-trip delay to validate text character mappings.

**Answer:** Base62 significantly maximizes character density per bit compared to Base16, while avoiding confusing special characters (like '+' or '/') used in Base64 that can break URL path string parsing.

## Q6: If your distributed URL shortener deployment must ensure that short code strings are never recycled or overwritten even if they remain dormant for years, which lifecycle parameter should be omitted?

**Options:**

- Enforcing an aggressive Time-To-Live (TTL) expiration configuration on primary database storage records.
- Using consistent hashing to partition the core NoSQL wide-column table keyspaces.
- Enforcing sliding rate limits on incoming API click ingestion proxy endpoints.
- Configuring Bloom Filter bit masks inside the real-time cache cluster lines.

**Answer:** Enforcing an aggressive Time-To-Live (TTL) expiration configuration on primary database storage records.

## Q7: When designing the database schema for a URL shortener in a relational SQL platform at scale, what optimization accelerates pointing lookups based on short code keys?

**Options:**

- Defining the short code field string layout as a unique clustered index on the database partition tables.
- Inlining the raw long destination URL string into a single character binary cell array.
- Dropping table primary keys entirely to speed up horizontal append velocities.
- Enforcing synchronous distributed locks across alternate read replica configurations.

**Answer:** Defining the short code field string layout as a unique clustered index on the database partition tables.

## Q8: What happens if a user submits a long URL destination containing malicious or phishing payload links to your platform's creation endpoint?

**Options:**

- The shortener gateway should pass the target URL through an asynchronous threat intelligence verification API filter before registering the short link in database layers.
- The system should execute a hard container rebuild across the ingress proxy server pool.
- The system automatically transitions all downstream database rows into binary layouts.
- The endpoint blocks all inbound client traffic configurations permanently.

**Answer:** The shortener gateway should pass the target URL through an asynchronous threat intelligence verification API filter before registering the short link in database layers.

## Q9: When scale-testing the short code generation component using a central relational sequence generator, what is the best strategy to maximize write path performance?

**Options:**

- Force each worker container to fetch a block or range of sequential ID numbers into local memory buffers at boot time, reducing point lookups.
- Execute a full table vacuum loop synchronously on every single short link write action.
- Convert the generation algorithm to rely strictly on raw UDP loopback protocols.
- Purge the master database configuration parameters whenever traffic scales past baselines.

**Answer:** Force each worker container to fetch a block or range of sequential ID numbers into local memory buffers at boot time, reducing point lookups.

## Q10: Why is it discouraged to use a simple MD5 or SHA-256 hash of a long URL string directly as its short code parameter value?

**Options:**

- Standard cryptographic hashing algorithms generate values that are too long (e.g., 32+ hex characters), violating short link requirements unless extra compression or truncation step logic is applied.
- Cryptographic hashes lose their character validation properties if they traverse internet proxy routers.
- Hashing long URLs forces relational database layers to discard primary key constraints.
- Cryptographic hashing requires an outbound cross-network round-trip handshake loop.

**Answer:** Standard cryptographic hashing algorithms generate values that are too long (e.g., 32+ hex characters), violating short link requirements unless extra compression or truncation step logic is applied.

## Advanced (Staff/Principal)

## Q11: Design a URL shortener that provides custom aliases while preventing alias squatting and dictionary attacks. How do you handle the trade-off between user freedom and security?

**Answer:** Implement a **three-tier alias allocation**: (1) **random aliases** — default, 7-char base-62, generated server-side with no user input; (2) **semi-custom aliases** — user-suggested but vetted via an automated policy engine (blocklist + pattern matching + Levenshtein distance check against reserved names); (3) **reserved/vanity aliases** — manually reviewed, requiring business approval, for brands/enterprise customers. Anti-squatting: enforce **alias expiration** — if a custom alias receives zero clicks for 90 days, it is released back to the pool. Require **verified ownership** (email or phone) for custom aliases to discourage mass registration. Rate-limit alias creation per account (e.g., 10 custom aliases/day). Dictionary attacks: pre-register a blocklist of the top 100K dictionary words, common brand names, and profanity. Use **probabilistic detection** (Bloom filter) to reject aliases that match blocked patterns at O(1) cost.

## Q12: How would you handle link rotation/migration when a short URL domain changes (e.g., rebranding from bit.ly to bitly.com) without breaking existing links?

**Answer:** Maintain **dual domain resolution** indefinitely for old links. Implementation: (1) keep the old domain's DNS pointing at your edge infrastructure; (2) the old domain's API gateway issues a **301 redirect** to `https://newdomain.com/<code>` (preserving the short code). The 301 tells browsers/clients to cache the redirect permanently, so subsequent hits go directly to the new domain without hitting the old gateway — self-migrating. (3) For clients that ignore 301 (API clients, curl), the old gateway continues to serve 301s indefinitely. (4) For **deep SEO preservation**, use the old domain's `robots.txt` and `sitemap` to point crawlers to the new domain. (5) Monitor **old domain hit rate** — when it drops below a threshold (e.g., 1% of traffic), consider a sunset timeline. Never force a hard cutover — links shared on printed media, email signatures, and embedded in PDFs are permanently immutable.

## Q13: Design a URL shortener analytics system that tracks per-link click geography, device type, and referrer at 500K clicks/sec with sub-second query latency on historical data.

**Answer:** Two-tier architecture: (1) **hot path** — on each redirect, log the click event to Apache Kafka as a structured message (short_code, timestamp, user_agent, referrer, geo from CloudFront/edge headers, device type parsed). Use a custom **Kafka partitioner** keyed by short_code to ensure all clicks for a link land on the same partition, enabling ordered processing. (2) **cold path** — Kafka consumers batch-aggregate data into **pre-aggregated time-series buckets** stored in a columnar store (ClickHouse / Druid). Store pre-joined rollups every 5 minutes: `(short_code, ts_bucket, country, device_type, referrer_domain, count)`. Query: the analytics dashboard queries ClickHouse with a simple `SELECT sum(count) ... WHERE short_code = ? AND ts_bucket > ? GROUP BY country`. Columnar storage allows scanning billions of rows in sub-second. For **real-time counters** (last 5 minutes), maintain a Redis hash per short_code with atomic `HINCRBY` — dashboards poll Redis for the hot data and ClickHouse for historical.

## Q14: How do you handle a malicious user who creates millions of short links pointing to the same destination to exhaust your storage? Design quota and abuse detection.

**Answer:** Implement **content-based deduplication**: hash the destination URL + a canonicalization pass (strip tracking params, normalize protocol/slashes). If the same canonical URL already has a short link from any user, return the existing short code — this prevents storage explosion. However, this leaks info about popularity. Alternative: **per-user dedup** — detect if the same user creates the same destination repeatedly; silently return the existing short code. Combine with **proactive rate limits**: (1) per-user hourly link creation quota (e.g., 1000); (2) per-destination link limit — max 100 short codes per unique destination from the same user; (3) **ML-based abuse detection** — features: creation velocity, destination domain entropy (spam domains have high entropy random subdomains), similarity to known phishing destinations (via threat intel feeds). Store the dedup hash as a secondary index in a separate table (not the main table) to avoid slowing primary writes. When a user hits a soft limit, escalate to CAPTCHA; hard limit triggers account suspension.

## Q15: Describe the CAP trade-offs in a globally distributed URL shortener. What's your replication strategy for the short-to-long mapping and why?

**Answer:** URL shorteners are inherently **AP** workloads — it's better to serve a redirect (possibly stale) than to fail with 503. Downtime breaks billions of existing links. Strategy: **multi-master active-active with conflict-free replicated data types (CRDTs)**. The mapping table uses last-writer-wins (LWW) CRDTs with wall-clock timestamps. Each region accepts writes independently. Replication is asynchronous via Kafka cross-region mirroring. This means: (1) a link created in us-east-1 is not immediately visible in eu-west-1 (~1 second replication lag is acceptable for link creation); (2) during partition, each region continues serving reads and writes independently; (3) conflicts are resolved deterministically by timestamp (or hybrid logical clock). The trade-off: **deletion is problematic** — if a user deletes a link in one region, the deletion may not have propagated when another region serves a stale redirect. Mitigation: tombstone records with a TTL, and a fixed DNS TTL on the short domain so clients don't cache broken redirects indefinitely.

## Q16: Your URL shortener is used to generate links for an email marketing platform. A customer reports that their emails contain broken links because the short URLs expired after 30 days. They expected permanent links. What was the architectural failure, and how do you prevent this class of misunderstanding?

**Answer:** Architectural failure: the system had a **default TTL** of 30 days on short links (to auto-reclaim storage from unused links), but this was not communicated to customers, and there was no way to opt in to permanent links. The root cause is a **missing storage tier SLA**: the system treated all links as ephemeral, but the customer had an implicit expectation of permanence. Fix: (1) **link durability tiers** — define explicit SLAs: `ephemeral` (30-day TTL, free tier), `standard` (7-year TTL, default for paid accounts), `permanent` (indefinite, with a clause in the ToS allowing removal only for legal/abuse reasons, higher cost). (2) **customer-facing API** — the link creation API must accept a `ttl` parameter (default: 7 years for paid, 30 days for free). The API response includes `expires_at` timestamp. (3) **compliance disclaimer** — for `ephemeral` links, the UI/API displays a clear warning: "This link will expire on {date}." (4) **storage cost modeling** — permanent links require infinite storage growth. Model cost as `total_links × avg_size × (1 + growth_rate)^years`. Fund permanent storage via a separate cost center (charged to the marketing product line). (5) **monitoring** — alert when the ratio of permanent links to total links exceeds 50% (indicates customers are opting up and cost is shifting). The principal engineer's lesson: durability expectations must be explicit in the API contract and reflected in the storage architecture from day one — retroactively adding permanence is expensive.

## Q17: Design a URL shortener where the short code is generated from the destination URL via a deterministic hash, so the same long URL always produces the same short URL (content-addressing). What are the security and operational implications of this design?

**Answer:** Benefits: built-in deduplication — no need for "duplicate link" detection; two users sharing the same long URL get the same short code. Implications: (1) **enumeration attack** — given a short code, an attacker can reverse-engineer which long URLs are popular by brute-forcing short codes (if the hash is predictable). Mitigate by using a **salted hash with a secret key** (HMAC-SHA256 truncated to 64 bits). (2) **link rot amplification** — if the target URL goes down or changes content, every user who shared that short link is affected simultaneously. The short code is permanently tied to the first-seen destination. Mitigation: support **aliasing** — users can create an "update" to the short link that redirects to a new destination, with the hash-based code still resolving to the latest alias via a versioned lookup. (3) **hash collisions** — with 64-bit hash (Base62 encoded to ~11 chars), the probability of collision reaches 50% at ~5 billion entries (birthday paradox). Beyond that, new URLs will produce duplicate codes. Mitigation: use 128-bit hash (extended encoding to 22 chars) or fall back to a collision resolution strategy (append a counter until unique). (4) **operational concern** — hash computation adds CPU cost on the write path (~1μs for HMAC-SHA256), negligible. (5) **storage savings** — the dedup table is `hash → long_url` rather than `short_code → long_url`, which saves storage only if the same URL is shared many times (high dedup ratio). For URLs that are shared only once, the hash table adds overhead. Principal decision: content-addressing is ideal for **immutable content** (e.g., IPFS) but problematic for URLs whose destination may change. Use it only if the business guarantees that short links are permanent.

## Q18: You need to support 10 billion URL creations per month (5,000 new links/second sustained). Design the write path to handle this throughput without hotspotting the ID generator or the database.

**Answer:** Write path: (1) **ID generation** — use a **batched ID dispenser** (Raft-based sequencer allocating ranges of 10K IDs to each application server). 5K links/s × 1 ID per link → allocate 1 range per second per server → trivial. (2) **write buffering** — application workers batch incoming `CreateLink` requests into a buffer. When the buffer reaches 1000 requests or 500ms has elapsed, flush it to the database as a **bulk insert**. This reduces database write IOPS by 1000×. (3) **database** — use a distributed NoSQL store (Cassandra/Scylla) with `short_code` as the partition key. Bulk inserts are routed to the appropriate partition via the driver's token-aware routing. Write throughput of 5K/s is well within a 10-node Scylla cluster's capability (each node handles ~500 writes/s). (4) **avoid hot partition** — the short code is a random string (Base62), so the hash is uniformly distributed — no hot partition. (5) **async validation** — for custom aliases (user-chosen), perform a synchronous `SELECT ... WHERE short_code = ?` to check uniqueness — this is a point lookup, <1ms. For the 99% of auto-generated codes, the probability of collision is negligible (64-bit space with 5K/s = 2.6B/year, collision probability << 0.001%). Skip the uniqueness check for auto-generated codes and rely on the DB unique constraint + retry on conflict. (6) **monitoring** — track `write_latency_p99`, `bulk_insert_batch_size`, and `collision_retry_count`. If collision retries exceed 0.01% of writes, it indicates the ID generation space is too small. (7) **capacity** — 10B creations/month × 1KB per row (short_code + long_url + metadata) = ~10TB/month storage. Ensure the storage cluster auto-scales or provision 100TB/month growth.

## Q19: A customer reports that their short links are being used in a phishing campaign targeting their brand. They want the ability to take down specific short links within 5 minutes globally. Design the takedown system, including propagation guarantees.

**Answer:** **Global takedown system**: (1) **takedown API** — authenticated endpoint `POST /admin/takedown` with parameters `short_code` (single or batch) and `reason_code`. The API writes the takedown event to a **global append-only log** (Kafka with cross-region mirroring). (2) **hot blocklist** — the takedown log feeds a **distributed blocklist** stored in Redis (or Global Data Store). Key: `blocked:{short_code}`, value: `{reason, timestamp, region}`. Each region's edge gateway checks the blocklist BEFORE returning the redirect. Blocklist replication: use Redis CRDTs (Active-Active Geo-Distribution with conflict-free replication) — a takedown in one region propagates to all others within <1 second. (3) **5-minute guarantee** — the blocklist check at the edge is a local Redis lookup (<1ms). Propagation across regions takes <1s. The 5-minute SLA allows for: API authentication (10s), manual review if needed (2-4 minutes), and safety buffer. (4) **override for abuse** — if the takedown is for phishing/malware, bypass the manual review queue and immediately write to the blocklist. (5) **audit trail** — every takedown event is logged (who, when, why, which short_code). The log is immutable and stored for 7 years (compliance requirement). (6) **fallback** — if the Redis blocklist is unavailable, the edge gateway falls back to a local on-disk blocklist (updated every 30 seconds from S3). This adds 30-second latency to takedown propagation but ensures the blocklist is never bypassed. (7) **deceptive redirection** — instead of returning 410 Gone, redirect the takedown links to a **warning page** (hosted on a different domain): "This link has been disabled for security reasons." This prevents phishing while informing the user.

## Q20: Your URL shortener platform is acquired by a larger company. The CTO demands a migration from your custom stack to the acquirer's existing URL shortener infrastructure. They have 50 billion existing links; you have 10 billion. Design the migration with zero downtime and zero broken links for both sets of users.

**Answer:** **Unified routing layer** with a **read-through proxy**: (1) **proxy deployment** — deploy a new global routing layer (Nginx/Envoy) in front of both systems. The proxy holds no data — it's a smart redirector. (2) **mapping table** — for every incoming `GET /{short_code}`, the proxy checks: (a) Redis cache (pre-warmed with both systems' active links); (b) if cache miss, query an **orchestrator** that fans out to both systems in parallel: "does system A have this code?" + "does system B have this code?"; (c) if exactly one returns a result, respond with that redirect; (d) if both return, use the timestamp of last update (newer wins); (e) if neither, return 404. (3) **bulk import** — export all 10B links from your system as compressed Parquet files. Write a **parallel import job** (Spark, 2000 workers) that inserts into the acquirer's system with a flag `origin: "acquired"` and a `preferred` ranking (so the proxy prefers your system's data during the overlap period). (4) **consistent hash ring unification** — if the acquirer's system uses consistent hashing for sharding, allocate a new partition prefix for your data (e.g., all your codes start with a specific fingerprint bit pattern) to avoid reshuffling their existing data. (5) **cutover** — once all 10B links are imported and verified (checksum reconciliation, Merkle tree comparison), switch the proxy to query only the acquirer's system for both old and new links. Keep your old system running as read-only backup for 1 month. (6) **DNS cutover** — the short domain's DNS already points to the proxy, so no DNS change needed. The entire migration is transparent to end-users. (7) **rollback** — if the acquirer's system has higher latency or errors, flip the proxy back to dual-read mode. The proxy exposes a `system_a_traffic_share` feature flag (0-100%) for gradual rollback.

