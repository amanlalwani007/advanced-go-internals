# Chapter 9 â€” Design A Web Crawler

## Q1: When designing a large-scale DNS resolver for a web crawler processing 100,000 pages per second, what is the primary architectural bottleneck of relying on the local OS standard getaddrinfo call?

**Options:**

- It lacks support for IPv6 address resolution schemas.
- It is typically a synchronous, blocking network system call that binds an entire application execution thread for the duration of the network lookup.
- It automatically compresses DNS payloads, which corrupts the destination IP parsing masks.
- It forces the crawler to communicate strictly via TCP rather than UDP routes.

**Answer:** It is typically a synchronous, blocking network system call that binds an entire application execution thread for the duration of the network lookup.

## Q2: To effectively minimize space requirements when tracking whether trillions of unique URLs have been visited, which distributed data structure represents the best memory trade-off?

**Options:**

- A globally synchronized relational database index table using B+Trees.
- A Scalable Distributed Bloom Filter or cuckoo filter kept in high-density cluster memory.
- An append-only text file distributed across a Hadoop Distributed File System (HDFS) pool.
- A centralized Radix Tree stored entirely within a single master node's memory space.

**Answer:** A Scalable Distributed Bloom Filter or cuckoo filter kept in high-density cluster memory.

## Q3: A web crawler encounters a 'spider trap' (e.g., a dynamically generated calendar loop that produces infinite paths like /year/2026/month/06/day/23...). What strategy best protects the crawler from resource exhaustion?

**Options:**

- Relying purely on the HTTP timeout layer to break connection sockets automatically.
- Enforcing strict URL length boundaries and tracking structural repetition count anomalies per domain using a combination of page depth constraints and URL structure analytics.
- Clearing the DNS cache every time the crawl path exceeds twenty deep branches.
- Switching the downloader from GET requests to HEAD requests for all subdirectory layers.

**Answer:** Enforcing strict URL length boundaries and tracking structural repetition count anomalies per domain using a combination of page depth constraints and URL structure analytics.

## Q4: To implement strict 'Politeness' compliance across a distributed cluster of independent crawling nodes, how should the URL Frontier be structurally coordinated?

**Options:**

- Each worker node randomizes its execution sleep timings between individual fetch operations globally.
- Map hostnames to specific Back Queues via a hashing mechanism, and use a centralized broker or distributed lock manager to ensure a single Back Queue is only polled by one worker thread at a time.
- Force all worker nodes to route traffic through a shared centralized proxy gateway that drops concurrent packets.
- Implement a distributed two-phase commit across all worker instances before issuing any HTTP request.

**Answer:** Map hostnames to specific Back Queues via a hashing mechanism, and use a centralized broker or distributed lock manager to ensure a single Back Queue is only polled by one worker thread at a time.

## Q5: When extracting hyperlinks from downloaded HTML pages, why is near-duplicate content detection (e.g., using SimHash) performed *before* parsing out the outbound anchor links?

**Options:**

- SimHash requires the raw, unparsed HTML byte stream to compute cryptographic bit patterns.
- If a page is flagged as a near-duplicate of an already processed document, extracting its links is redundant and would pollute the URL Frontier with duplicate crawl paths.
- Parsing anchor links mutates the document structure, which invalidates the underlying TCP socket checksum flags.
- SimHash algorithms automatically fix broken HTML tags to accelerate downstream DOM query processing.

**Answer:** If a page is flagged as a near-duplicate of an already processed document, extracting its links is redundant and would pollute the URL Frontier with duplicate crawl paths.

## Q6: How should a distributed web crawler handle a server's robots.txt file to balance politeness compliance with high-throughput performance?

**Options:**

- Download and parse the robots.txt file for every single URL fetch request to ensure real-time compliance.
- Download the robots.txt file once per domain, parse its rules into an optimal in-memory trie structure, cache it locally with a reasonable TTL, and validate URLs against this cache before fetching.
- Download the file only when the target web server returns an HTTP 403 Forbidden status code response.
- Incorporate robots.txt rules directly into the global DNS resolution packet payload flags.

**Answer:** Download the robots.txt file once per domain, parse its rules into an optimal in-memory trie structure, cache it locally with a reasonable TTL, and validate URLs against this cache before fetching.

## Q7: What is the primary architectural trade-off when configuring your crawler's HTML fetcher to execute client-side JavaScript using headless browser instances (e.g., Playwright or Headless Chrome) versus basic HTTP raw HTML clients?

**Options:**

- Headless browsers require less network bandwidth because they compress structural style assets naturally.
- Headless browsers enable the crawling of dynamic single-page applications (SPAs), but they increase memory and CPU consumption by orders of magnitude, lowering throughput.
- Raw HTTP clients are incapable of parsing standard text compressions like GZIP or Brotli payloads.
- Headless browsers eliminate the requirement for managing URL Frontier queues due to their internal cache structures.

**Answer:** Headless browsers enable the crawling of dynamic single-page applications (SPAs), but they increase memory and CPU consumption by orders of magnitude, lowering throughput.

## Q8: When storing crawled web page contents across a distributed storage cluster, why are large wide-column stores (like HBase) or object stores (like AWS S3) chosen over standard file systems storing individual raw HTML files?

**Options:**

- Standard file systems lack the cryptographic security protocols necessary to isolate crawled text data partitions.
- Storing billions of tiny individual files creates severe metadata allocation bottlenecks (inode exhaustion) and slows directory listing speeds to a crawl on standard operating systems.
- Object stores automatically execute deep neural net semantic text parsing during the write stream.
- Wide-column stores enforce strict synchronous transactions that lock out web crawler nodes during read operations.

**Answer:** Storing billions of tiny individual files creates severe metadata allocation bottlenecks (inode exhaustion) and slows directory listing speeds to a crawl on standard operating systems.

## Q9: If your distributed web crawler nodes suddenly begin experiencing high rates of HTTP 429 Too Many Requests errors from a target cluster, which architectural adjustments should the URL Frontier immediately implement?

**Options:**

- Double the number of concurrent fetch threads assigned to that host to clear out the queue before it overflows.
- Dynamically increase the back-off delay multiplier (e.g., using exponential back-off) for that specific host's Back Queue and decrease its maximum concurrency limits.
- Immediately pivot all requests to target the system's staging environment servers instead.
- Flush the local Bloom Filter tracking structures to force a complete re-crawl from the root seed node.

**Answer:** Dynamically increase the back-off delay multiplier (e.g., using exponential back-off) for that specific host's Back Queue and decrease its maximum concurrency limits.

## Q10: In a distributed crawler using a master/worker topology, what happens if the master node crashes while managing the URL Frontier allocations?

**Options:**

- The workers will continue fetching data uninterrupted forever by generating random memory link strings.
- A single point of failure (SPOF) condition triggers unless the master state is backed up continuously via distributed consensus logs (e.g., Raft), allowing a standby follower to assume leadership.
- The storage engines will automatically transition into read-only mode across all data center zones.
- The network gateway infrastructure shifts all active worker sockets to target local loopback channels.

**Answer:** A single point of failure (SPOF) condition triggers unless the master state is backed up continuously via distributed consensus logs (e.g., Raft), allowing a standby follower to assume leadership.

## Advanced (Staff/Principal)

## Q11: Design a politeness scheduler that respects robots.txt and crawl-delay while still achieving maximum throughput across a distributed fleet of 10,000 worker nodes.

**Answer:** Use a **two-level scheduler**: (1) **global policy layer** — a centralized service (etcd-backed) stores per-domain politeness configuration: `crawl_delay`, `max_concurrent_requests`, `allowed_paths` (from robots.txt). Workers fetch policy on encountering a new domain and cache it locally with a TTL (e.g., 15 minutes). (2) **local rate limiter per worker** — each worker maintains a token bucket per-domain. But with 10K workers, independent token buckets violate politeness (10K workers × 1 req/10s ≠ 1 req/10s). Solution: **distributed claim-check**. Workers do not directly issue requests. Instead, they submit URL claims to a **per-domain FIFO queue** backed by Kafka (partitioned by `domain_hash`). A small number of **politeness dispatchers** (one per domain partition) pull claims and schedule actual HTTP fetches, enforcing the domain's rate limit exactly. Workers are pure discovery + extraction engines, decoupled from fetch pacing. This gives central control of politeness with massive worker parallelism.

## Q12: How do you detect and handle JavaScript-rendered content that changes on every visit (e.g., dynamic token-based CSRF protection)? What fingerprinting strategy do you use?

**Answer:** Use a **structural fingerprint** rather than a content hash. Compute a **DOM structure signature**: serialize the rendered DOM tree ignoring attribute values, text content, and inline styles that vary per-session. Compare against a **normalized tree hash** (e.g., Merkle tree of tag names + class names + structural positions). If the structural fingerprint matches a previously seen page within a similarity threshold (e.g., 0.8 Jaccard similarity on tag-path sets), treat it as a duplicate — do not extract links from it. For CSRF tokens specifically: implement a **phantom-aware fetcher** that detects anti-bot measures by: (1) checking if the page contains hidden form fields with dynamic values; (2) measuring the execution time of critical JS — if it suspiciously matches a known anti-bot script profile, flag the page. For high-value targets, use a **headless browser snapshot** solution but cache the rendered DOM fingerprints to avoid per-visit headless costs.

## Q13: Design the storage architecture for storing 100 billion crawled pages with compression, deduplication, and near-real-time indexing. Estimate the hardware requirements.

**Answer:** Assume average page size = 50KB uncompressed (HTML + extracted text + metadata). 100B × 50KB = 5 exabytes raw. Compress with Zstandard (dictionary-trained on HTML corpus) → ~5:1 ratio = 1 exabyte compressed. Storage: **object store** (S3-compatible) partitioned by URL hash prefix (e.g., 4096 buckets, 00/00 → ff/ff). Deduplication: use a **distributed Bloom filter** (or Cuckoo filter) across a Redis/Cluster with 10 bits per URL = 100B × 10 bits = 125GB filter — fits in memory on 4 nodes. Near-real-time indexing: stream compressed pages into **Elasticsearch** (or a custom inverted index). With 50:1 compression, 1 exabyte → 20PB for ES. Estimate: ~2000 object storage nodes (4TB each), ~200 ES data nodes, ~32 crawler dispatcher nodes. With erasure coding (12+4) instead of 3x replication, reduce object storage to ~700 raw TB. Power: ~2MW for the storage fleet alone. Given these numbers, most organizations abstract this via cloud object stores (S3, GCS) and managed ES — the operators' job is the ingestion pipeline, not the hardware.

## Q14: How do you handle crawling behind login walls? Design a session management system that can maintain and rotate millions of authenticated sessions without triggering anti-bot systems.

**Answer:** **Credential hierarchy**: (1) seed accounts with verified credentials stored in a **vault** (HashiCorp Vault / AWS Secrets Manager) with automatic rotation; (2) for each target site, maintain a session pool of N concurrent authenticated sessions. Sessions are distributed across workers via consistent hashing on the site's domain. Session lifecycle: login with credentials → extract cookies + tokens → store in a shared Redis cache (encrypted, with a TTL matching the session expiry). Workers pick up sessions from the cache when they need to crawl authenticated pages. Anti-bot evasion: (1) **mimic human behavior** — randomize request intervals (Gaussian distribution around a mean), scroll events, mouse movements via headless browser; (2) **session diversity** — each session uses a distinct user-agent, accept-language, and browser fingerprint; (3) **IP rotation** — route requests through a rotating proxy pool (residential proxies for high-value targets, datacenter proxies for low-value). Monitor **login failure rate** per site — a spike indicates either credential rotation or anti-bot upgrade; automatically pause crawling and alert.

## Q15: Describe how you would implement a priority-based crawl queue that balances freshness (recrawling popular pages) with coverage (discovering new pages) under finite bandwidth.

**Answer:** Model crawl scheduling as a **constrained optimization problem** where bandwidth B must be split between recrawl (freshness) and new discovery (coverage). Implement a **multi-priority queue** in Kafka with 3 tiers: (1) **critical** — pages that change frequently and are popular (high PageRank or high inbound link count), recrawl every 5 minutes; (2) **normal** — pages with moderate change frequency and moderate popularity, recrawl every 24 hours; (3) **background** — new URLs from discovery, long-tail pages, recrawl weekly. Dynamic priority adjustment: a **change detection monitor** tracks `etag`/`last-modified` response headers and content hash differences. If a page changes on two consecutive recrawls, promote it one tier (it's more dynamic than expected). If it hasn't changed in 10 recrawls, demote it. Bandwidth allocation: start with 40% critical, 40% normal, 20% background. Adjust based on backlog depth: if background queue grows > 1M URLs, steal 10% from critical. If critical pending time > 30 min, steal from normal. Publish queue depth metrics to allow operators to adjust allocations during traffic anomalies (e.g., after a major website redesign, many critical pages change simultaneously, requiring temporary bandwidth shift).

## Q16: Your distributed crawler has been running for 3 years, and you notice that the URL Frontier contains 40% dead links (domains that no longer resolve, servers returning 410/404 permanently). These dead links consume Frontier memory and slow down the dispatcher. Design a lifecycle management system for URL health.

**Answer:** **URL health lifecycle**: (1) **state machine** — each tracked URL has a state: `ACTIVE` (last fetch succeeded), `DEGRADED` (last N fetches returned 4xx/5xx), `DEAD` (M consecutive failures or DNS resolution failure). Transition rules: 2 consecutive errors → `DEGRADED`, 5 consecutive errors → `DEAD`, successful fetch from `DEAD` → `ACTIVE` (automatic revival). (2) **DEAD URL eviction** — `DEAD` URLs are retained in the Frontier but with a **backoff multiplier**: if `DEAD`, only recheck every 30 days. After 6 months in `DEAD` state, the URL is moved to a **cold archive** table (S3 + DynamoDB index) and removed from the active Frontier. (3) **probation queue** — when a domain becomes `DEAD` for all its URLs (entire domain unresolvable), move the domain to a **domain probation list**. Do not accept new URLs from this domain until it resolves again. Recheck the domain's DNS monthly. (4) **memory optimization** — the active Frontier stores only `ACTIVE` and `DEGRADED` URLs (compressed as 64-bit hashes, not full URLs). The full URL is resolved from a key-value store (RocksDB) only when it's time to fetch. This reduces Frontier memory footprint by ~60%. (5) **monitoring** — track `dead_url_ratio` (target <10%). If it exceeds 20%, investigate for systemic issues (e.g., a popular domain went permanently offline). (6) **automatic re-discovery** — even after eviction, a URL can re-enter the Frontier if it appears again in a newly crawled page's outbound links. The dedup Bloom filter prevents re-add for 30 days after eviction.

## Q17: You are crawling a site that serves different content based on the user's geographical location, device type, and whether they are logged in. Your crawler only sees one variant. How do you design a crawler that can discover all content variants without maintaining thousands of authenticated sessions?

**Answer:** **Multi-fingerprint crawling**: (1) **parameterized crawl** — for each target domain, define a set of dimensions: `{locale: [en, fr, de, ja], device: [mobile, desktop], auth: [anonymous, logged_in]}`. Dispatch up to M (e.g., 6) parallel fetches for each URL, one per unique fingerprint combination. Use different IPs (via proxy pool), user-agents, and `Accept-Language` headers per variant. (2) **structural diffing** — after fetching all variants, compute a **DOM similarity score** (tree edit distance). If all variants produce identical DOM structures (just translated text), merge them into a single canonical entry with a locale map. Only store the canonical version plus a locale→variant URL suffix map. (3) **logged-in variant** — use a syndicated crawling approach: partner with the site to provide a special crawler API key that returns the full content (including authenticated-only content) as JSON, bypassing the need for session management. Many large sites (YouTube, Twitter, Reddit) provide such APIs. (4) **hidden content discovery** — for sites that reveal content only after JavaScript interaction (infinite scroll, accordion), use a **headless browser with scroll/interaction script** per URL, with a timeout (max 5 seconds of interaction per URL). Cache the rendered DOM per fingerprint. (5) **cost control** — `M=6` means 6x the crawl cost for that domain. Enable multi-fingerprint only for high-value domains (based on PageRank or explicit configuration). For long-tail domains, crawl only the default anonymous variant.

## Q18: Your web crawler has been blocked by a major website that accuses you of violating their ToS. Your legal team needs to prove that your crawler respects robots.txt and crawl-delay. Design an observability and compliance system that produces verifiable evidence.

**Answer:** **Crawler compliance observability**: (1) **fetch log** — every HTTP request is logged to an **immutable append-only log** (Kafka → S3 with WORM lock). Each log entry contains: `timestamp, worker_id, target_url, resolved_ip, request_headers, response_code, robots.txt_sha256_checked, delay_enforced_ms`. The robots.txt_sha256_checked field is the SHA-256 of the robots.txt rules that were applied to this request — proving that the crawler checked the rules before fetching. (2) **robots.txt audit trail** — every time a domain's robots.txt is fetched, the raw content and parsed rule set are stored in a versioned store (DynamoDB, keyed by `domain + fetch_timestamp`). The fetch log references which version was used. (3) **politeness proof** — the fetch log records the actual inter-request interval enforced for that domain. A compliance auditor can query: "for domain X, was the delay at least Y seconds between consecutive requests?" — query: `SELECT timestamp, LAG(timestamp) OVER (PARTITION BY domain ORDER BY timestamp) AS prev_ts FROM fetch_log WHERE domain = ?` — compute `timestamp - prev_ts >= crawl_delay`. (4) **rate limiting proof** — records the per-domain token bucket state snapshot before each fetch, proving the bucket was non-empty. (5) **report generation** — a compliance dashboard allows an auditor (or third-party) to generate a time-bound report for a specific domain: "Show all requests to domain X between Date_A and Date_B, with evidence of robots.txt compliance and crawl-delay enforcement." The report is signed with a private key (HMAC) to prove authenticity. (6) **third-party attestation** — engage a third-party security firm to audit the crawler's code and produce an attestation report that can be shared with blocked websites. This has precedent: Google, Bing, and other major crawlers undergo similar audits.

## Q19: A search engine team asks you to design a "freshness SLA" for their web crawler: any newly published article on a major news site must appear in search results within 5 minutes. Design the architecture to meet this SLA while keeping crawl costs within budget.

**Answer:** **Push-based fresh content pipeline**: (1) **RSS/Atom feed monitoring** — for major news sites, subscribe to their RSS/Atom feeds instead of crawling their homepage every minute. Feed polling: poll every 30 seconds. A feed entry contains the article URL and publication timestamp. This is far more efficient than homepage crawling (one small feed request vs crawling the entire homepage + all article links). (2) **pubsubhubbub (WebSub)** — for sites that support it, use WebSub (formerly PubSubHubbub): the site's server pushes new content to the crawler's callback endpoint in real-time. No polling needed. (3) **prioritized crawl** — when a new article URL is discovered (via feed or WebSub), it enters a **hot crawl queue** — immediate fetch, no scheduling delay. The hot queue has dedicated worker capacity (20% of total) to ensure it is never starved by the background crawl. (4) **index-first architecture** — the article's URL, title, and publication timestamp are indexed immediately (within seconds) from the feed metadata, even before the full content is fetched. The search results show the article immediately with a "snapshot pending" indicator. The full-text index is updated within the 5-minute window. (5) **cost controls** — for non-major sites (long-tail), do not offer the 5-minute SLA. Their content is crawled on the normal schedule (hourly/daily). This focuses budget on the high-value domains where freshness matters most. (6) **SLA monitoring** — for each domain in the "fresh" tier, measure `time_from_publication_to_index`. Alert if p99 exceeds 5 minutes. The SLA is met by 99% of articles; outlier articles (extremely long content) may exceed it. (7) **detect feed delay** — some sites delay their feeds by up to 30 minutes (anti-competitive). Monitor `feed_delay = article_pub_timestamp - feed_entry_received_timestamp`. If > 1 minute, escalate — the site is deliberately slowing down crawlers, and the 5-minute SLA cannot be met without direct crawling of their homepage.

## Q20: Your 10,000-node distributed crawler fleet is running at 40% CPU utilization, but your network bandwidth is fully saturated, and the URL Frontier is growing faster than it can be consumed. The bottleneck is not CPU or memory — it's network egress from your data center. How do you redesign the system to work within a fixed bandwidth budget?

**Answer:** This is a **bandwidth-constrained scheduling problem** — the bottleneck has shifted from computation to network egress. Redesign: (1) **admission control** — implement a **token bucket for bandwidth** at the data center level. Each crawl request must "spend" bandwidth tokens proportional to the expected response size (estimated from the Content-Length header or historical average for the domain). If the bucket is empty, the request is queued. (2) **response size capping** — for large pages (>1MB), truncate to the first 500KB (most inverted-index-relevant content is above the fold). Use `Range: bytes=0-524288` header. This reduces per-request bandwidth by 50% for the heaviest 1% of pages. (3) **binary resource skipping** — skip fetching URLs that are likely binary resources (images, PDFs, .zip, .exe) unless specifically configured. These consume bandwidth but produce no indexable text. Check the Content-Type from a HEAD request before GET (costs one small request but saves huge bandwidth). (4) **delta crawling** — for frequently-recrawled pages, use HTTP ETag / If-Modified-Since. On re-crawl, if the server returns 304 Not Modified (no change), the bandwidth cost is ~500 bytes instead of 50KB. With 40% of pages unchanged on each recrawl, this saves ~40% of bandwidth. (5) **geographic distribution** — deploy crawl workers in multiple data centers closer to the target websites. A crawler in Frankfurt crawling a German site uses less WAN bandwidth than one in us-east-1. Use a **geo-aware scheduler** that assigns crawl jobs to the nearest data center to the target. (6) **compression** — use HTTP/2 or gzip compression. Most servers already compress; configure the client to prefer gzip/brotli and increase the compression window size. (7) **bandwidth monitoring** — per-worker, per-domain, and per-datacenter bandwidth dashboards. Set hard limits: total egress must not exceed 95% of provisioned capacity. When approaching the limit, prioritize high-value domains (by PageRank or user-traffic-weighted importance) and deprioritize long-tail.

