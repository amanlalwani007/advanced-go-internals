# Chapter 10 â€” Design A Notification System

## Q1: When configuring an asynchronous message broker like RabbitMQ to handle high-priority OTP notifications alongside low-priority marketing notifications, which queue topology ensures optimal isolation?

**Options:**

- A single massive queue where messages use an internal priority field to bubble up to the front.
- Physically separate queues for distinct priority levels, with dedicated worker pools scaled independently to ensure high-priority channels always have compute availability.
- A circular ring buffer queue that overwrites older marketing messages when an OTP message enters.
- Routing all messages through a single dead-letter exchange configured with dynamic routing keys.

**Answer:** Physically separate queues for distinct priority levels, with dedicated worker pools scaled independently to ensure high-priority channels always have compute availability.

## Q2: A worker successfully sends an SMS via a third-party gateway, but the gateway's network response drops before the worker can acknowledge it. What mechanism prevents the user from receiving a duplicate SMS upon worker retry?

**Options:**

- The worker performs a hard reboot of its local OS container to clear memory leaks.
- Tracking an atomic 'idempotency_key' in a distributed database or cache layer, forcing workers to verify the key's state before executing outbound gateway requests.
- Relying on standard TCP packet window resizing to drop the duplicate frame.
- Forcing the client UI app to execute a cancellation handshake token.

**Answer:** Tracking an atomic 'idempotency_key' in a distributed database or cache layer, forcing workers to verify the key's state before executing outbound gateway requests.

## Q3: If a downstream provider like SendGrid experiences an extended outage and returns HTTP 503 Service Unavailable, how should your worker pool adjust to protect systemic resource availability?

**Options:**

- Increase thread counts and loop queries continuously to force the data through.
- Implement a Circuit Breaker pattern to fail fast locally, redirecting traffic to a backup provider while using exponential back-off with jitter for retries on the primary channel.
- Drop the notifications entirely and send an execution error back to the client UI.
- Convert all outbound traffic to run over local UDP broadcast paths.

**Answer:** Implement a Circuit Breaker pattern to fail fast locally, redirecting traffic to a backup provider while using exponential back-off with jitter for retries on the primary channel.

## Q4: To track real-time delivery funnels (Sent -> Delivered -> Read) for billions of push notifications without slowing down the core delivery workers, how should the telemetric data flow be structured?

**Options:**

- Have workers write status updates directly to the primary relational user database before pushing to the network.
- Emit delivery tracking telemetry as asynchronous events to a distributed streaming platform like Apache Kafka, allowing downstream analytical consumers to process logs out-of-band.
- Block client device interaction until a complete multi-region database handshake verifies delivery states.
- Store analytics tracking strings inside the local worker container file system logs.

**Answer:** Emit delivery tracking telemetry as asynchronous events to a distributed streaming platform like Apache Kafka, allowing downstream analytical consumers to process logs out-of-band.

## Q5: A user resets their notification settings frequently. How do you prevent race conditions where a worker sends a notification that the user disabled milliseconds prior?

**Options:**

- Run a full database schema lock on the entire users table during every single notification dispatch loop.
- Implement a 'Just-In-Time' (JIT) preference check by querying a low-latency distributed cache (e.g., Redis) right before the worker calls the external gateway API.
- Rely on the third-party provider to know and enforce your user's localized preference state configurations.
- Force the worker to wait 10 seconds before every execution step to let the system settle.

**Answer:** Implement a 'Just-In-Time' (JIT) preference check by querying a low-latency distributed cache (e.g., Redis) right before the worker calls the external gateway API.

## Q6: When designing a user-facing notification rate limiter to prevent spamming individuals with more than 3 marketing pushes per hour, which algorithm represents the best trade-off for low memory footprint and burst protection?

**Options:**

- A strict Distributed Locking loop using explicit database transaction semaphores.
- The Token Bucket or Sliding Window Log algorithm implemented inside a fast distributed cache like Redis.
- A random drop filter that rejects 10% of all marketing notification traffic uniformly.
- A hard-coded counter variable inside the local application memory space of each stateless container.

**Answer:** The Token Bucket or Sliding Window Log algorithm implemented inside a fast distributed cache like Redis.

## Q7: What is the primary benefit of converting raw notification templates (e.g., promotional HTML or SMS texts) to pre-compiled formats at boot time rather than rendering them dynamically on every worker request?

**Options:**

- It completely removes the requirement for multi-channel message routing architectures.
- It drastically cuts worker CPU utilization and processing latency, avoiding repeated disk I/O or tokenizing overhead during high-throughput execution runs.
- It changes the transport protocol from standard HTTPS JSON payloads over to raw binary bits.
- It eliminates the need to track idempotency keys inside the message brokers.

**Answer:** It drastically cuts worker CPU utilization and processing latency, avoiding repeated disk I/O or tokenizing overhead during high-throughput execution runs.

## Q8: When sending iOS Push Notifications via Apple Push Notification service (APNs), which network connection protocol strategy must your workers utilize to maximize throughput?

**Options:**

- Open a new TCP connection and execute a fresh TLS handshake for every single notification payload.
- Maintain persistent HTTP/2 connections to APNs endpoints, multiplexing multiple concurrent notification requests across the same long-lived connection.
- Route payloads through an intermediate SMTP email bridge array.
- Convert all payloads into raw UDP packets to bypass connection-oriented handshakes entirely.

**Answer:** Maintain persistent HTTP/2 connections to APNs endpoints, multiplexing multiple concurrent notification requests across the same long-lived connection.

## Q9: To protect against a single user's device generating millions of duplicate push notifications due to an upstream application bug, which safeguard should be implemented at the gateway tier?

**Options:**

- Enforce a hard rate-limiting filter based on a combination of 'user_id' and 'notification_type' at the API ingestion boundary.
- Dynamically re-route all cluster traffic to the local dev-null storage subsystem.
- Force all worker nodes to poll user devices for authorization signatures prior to fetching tasks.
- Temporarily double the provisioned queue sizing partitions across all data centers.

**Answer:** Enforce a hard rate-limiting filter based on a combination of 'user_id' and 'notification_type' at the API ingestion boundary.

## Q10: If you utilize a relational database to store historical notification logs, what index optimization is required to support fast dashboard queries looking for 'failed' notifications over the last 24 hours?

**Options:**

- A generic single-column index targeting the 'user_payload' JSON blob field text parameters.
- A composite index or partial index covering (status, created_at) where status equals 'failed'.
- A clustered index targeting the client device's MAC address string parameters.
- Dropping all indexes entirely to accelerate write path append execution velocities.

**Answer:** A composite index or partial index covering (status, created_at) where status equals 'failed'.

## Advanced (Staff/Principal)

## Q11: Design a notification deduplication system that guarantees at-most-once delivery across push, SMS, and email channels without a single point of failure. How do you handle idempotency key collisions?

**Answer:** Use a **distributed idempotency ring** backed by Redis Cluster (or DynamoDB with TTL). Each notification event carries an `idempotency_key = hash(recipient_id + notification_type + content_fingerprint + timestamp_window)`. Before sending, the worker attempts a `SET idempotency_key "dispatched" NX EX 86400` (24-hour dedup window). If the key already exists, skip. For SPOF avoidance: use Redis Cluster with replication factor 3 and Raft-based failover (e.g., Redis Enterprise or KeyDB). Handle collisions: if two workers race on the same key, only the first `NX` succeeds — the second returns nil and skips. For **cross-region dedup**, use CRDT-based last-writer-wins counters: each region writes a "consumed" marker with its wall clock. On reconciliation, the highest timestamp wins, so a delivery is never duplicated across regions. Edge case: if the idempotency kv-store is unavailable, fail-open (allow delivery) rather than fail-closed (block all notifications) — duplicate notification is acceptable, missed notification is not.

## Q12: How would you implement delivery receipts and read receipts for push notifications at 1M+ messages per minute? What's the storage and query strategy?

**Answer:** Use a **two-tier storage strategy**: (1) **hot path** — on device receipt/read, the client sends a tiny event to a regional ingestion endpoint that writes to Kafka. A streaming processor (Flink/Kafka Streams) aggregates receipts into a Redis-backed **per-user watermark**: `user:{id}:last_read_timestamp`. This gives O(1) query for "has the user read the latest message?" — critical for read-receipt indicators in chat. (2) **cold path** — the raw receipt events land in a columnar store (ClickHouse) partitioned by `(notification_id, date)`. Query pattern: "did user X read notification Y?" → single-row point lookup → use a secondary index on `(user_id, notification_id)`. Storage: each receipt is ~100 bytes → 1M/min = ~100MB/min = ~144GB/day. Use ClickHouse's built-in compression (ZSTD, ~5:1 ratio) → ~30GB/day. Retention: purge raw events after 90 days; keep aggregated daily rollups for 2 years for compliance.

## Q13: Design a notification routing system that selects the optimal channel (push/SMS/email/in-app) based on user preferences, device state, time of day, and message urgency — all evaluated in under 5ms.

**Answer:** Precompute a **routing decision tree** per user and cache it in local memory on each notification worker. The tree is a compact binary structure: (1) branch on user preference tier (all-channels / important-only / off-hours-silent); (2) branch on message priority (critical / high / normal / low); (3) branch on time-of-day bucket (business-hours / evening / sleep); (4) branch on device-last-seen recency (active within 5 min / 1 hour / 24 hours / stale). Cache the tree in local memory (LRU, 1M users ≈ 1GB). The worker evaluates the tree in <1μs — just a series of bitwise operations on precomputed flags. If the user is not in cache, fall back to a faster Redis lookup of their serialized preference bitset (most users will be hot). The 5ms budget includes this cache-miss fallback. Synchronous evaluation: the worker blocks for at most 2ms; if the Redis lookup exceeds 2ms, use a cached default routing (push + email for critical, email-only for normal) and proceed — the correct routing will be applied asynchronously on the next notification.

## Q14: How do you handle provider failover when multiple SMS/email providers are used? Design a circuit breaker with health checking that prevents false positives during transient network issues.

**Answer:** **Closed Circuit** → steady state (primary provider). Configure a **health probe** every 5 seconds: send a test request to the provider's status endpoint (or a synthetic notification). Track success/failure in a **sliding window** of the last 30 probes. When failure rate > 20% in the window, transition to **Half-Open**: (1) immediately route all traffic to a secondary provider (pre-warmed, already provisioned); (2) start probing the primary more aggressively (every 1 second) to detect recovery. **Half-Open → Closed** when 10 consecutive probes succeed. **Half-Open → Open** (dead) if failures continue for 60 seconds. In **Open** state, all primary traffic is blackholed; secondary handles 100%. Alert on any state transition. Prevent false positives: (1) use **triangulated health probes** — check from 3 separate health-check nodes (different AZs). If only 1 node reports failure, it's a network issue, not a provider issue; (2) **jittered retry** — the first failure in a window triggers a retry after 100ms; only count as failure if both attempts fail; (3) **degraded routing** — in Half-Open, send 10% traffic to primary while 90% goes to secondary (canary-style re-entry).

## Q15: Design a compliance system that ensures notification delivery respects regional regulations (GDPR, CAN-SPAM, etc.) including opt-out, data retention, and audit trails at scale.

**Answer:** **Regulatory rules engine**: compile regional regulations into a **decision table** stored in a config store (etcd). For each notification, evaluate: (1) **consent check** — query the user's consent record from a low-latency KV store (Redis); key = `consent:{user_id}:{channel}`; value = `opt_in` / `opt_out` / `not_set`. Default for GDPR region: not_set = cannot send marketing (explicit consent required). (2) **opt-out header** — for email, automatically append an `Unsubscribe` header containing a single-click token; for SMS, include an `STOP` instruction per CTIA guidelines. (3) **retention** — tag all notification records with a `retention_ttl` based on the user's region (e.g., GDPR: 30 days after deletion request; CCPA: 12 months). A background garbage collector scans a time-partitioned table and securely purges expired records (overwrite + drop). (4) **audit trail** — every notification send attempt (success or failure) is logged to an append-only audit table (immutable, backed by object store with WORM policy). Include: user_id, channel, timestamp, content_hash, consent_status_at_time, region, regulation_version. This satisfies regulatory inquiry response SLA (e.g., produce all records for user X within 72 hours). Scale: audit writes are batched (1000 events or 5 seconds) and piped to a compressed columnar store for cost-efficient storage.

## Q16: Your notification system has a critical bug: during a provider outage, the dead-letter queue (DLQ) for failed notifications grew to 50M messages. When the provider recovered, the workers drained the DLQ at full throttle, causing a 10X traffic spike that overwhelmed the provider and triggered a second outage. Design a safe DLQ drain mechanism.

**Answer:** **Rate-limited DLQ replay**: (1) **DLQ with per-provider token bucket** — each provider gets a DLQ replay rate limit (e.g., 1000 msgs/sec for SendGrid, 500 msgs/sec for Twilio). The replay worker checks the bucket before each retry. This prevents overwhelming a recovering provider. (2) **tiered replay** — prioritize DLQ messages by creation time or priority: replay the most recent messages first (users waiting for a password reset are more urgent than marketing emails from 2 days ago). Use a priority queue in the DLQ: `priority = f(age, message_type, user_tier)`. (3) **manual gating** — for large DLQs (>1M), require manual approval before replay. The operator can configure the replay rate via a UI knob (e.g., "replay at 10% → 50% → 100% over 30 minutes"). (4) **circuit breaker on the DLQ reader** — if the provider returns >5% error rate during replay, pause the DLQ drain and back off exponentially. (5) **prevent DLQ accumulation** — add a **DLQ alert** when queue depth exceeds 10K (trigger incident response) and 100K (auto-pause the primary channel to prevent further failures). (6) **idempotent replay** — each DLQ message carries an idempotency key. The provider's API is idempotent (if the same message was already delivered, the provider returns a "duplicate" response, and the worker does not send it again). This ensures safe retry even if the DLQ is replayed multiple times.

## Q17: Design a notification system that supports "priority boosting" — a user's critical notifications (password reset, payment confirmation) must always be delivered within 10 seconds, even if the system is under 10X normal load. How do you ensure high-priority messages are never starved by low-priority bulk traffic?

**Answer:** **Strict priority isolation**: (1) **separate queues per priority** — physical Kafka topics or RabbitMQ exchanges: `notifications.critical`, `notifications.high`, `notifications.normal`, `notifications.bulk`. Each queue has **dedicated consumer pools** with hard resource reservations. For the critical queue, provision 10% of total worker capacity even though it carries <0.1% of messages. (2) **priority-aware admission control** — at the API gateway, classify incoming notifications into priority tiers. Critical messages bypass all rate limiters (except a very high "abuse" limit). If the critical queue is backlogged (>1000 messages), preempt normal/bulk workers (Kubernetes priority class: critical workers have `priorityClassName: system-cluster-critical` and cannot be evicted). (3) **provider channel reservation** — maintain a reserved pool of provider connections (e.g., 2 Twilio connections reserved for critical SMS; the other 8 shared among normal/bulk). The reserved pool is never borrowed by lower-priority traffic. (4) **graceful degradation under overload** — if the system cannot keep up with aggregate traffic, apply backpressure to **bulk** first (delay by up to 1 hour), then **normal** (delay by up to 5 minutes), but **critical** is never delayed. (5) **monitoring** — critical SLA: `P99_delivery_time < 10s`. Alert if exceeded. Track `priority_boost_count` — how many times critical messages preempted lower-priority workers. If this happens >0.1% of the time, the system is over-provisioned for critical and needs more dedicated capacity. (6) **degradation test** — run a monthly chaos experiment where bulk traffic is injected at 20X normal rate. Verify that critical SLA remains <10s. If not, adjust resource reservations.

## Q18: Your company sends 500M push notifications per day across iOS and Android. The VP of Product wants to add in-app notifications (shown inside the mobile app when the app is foregrounded) with a delivery SLA of <200ms. The push notification pipeline currently runs on Kafka with a typical end-to-end latency of 30 seconds. How do you retrofit the system to meet the in-app SLA without rebuilding the entire pipeline?

**Answer:** **Bypass the async pipeline for in-app**: (1) **dual path** — in-app notifications follow a **synchronous path** that bypasses Kafka entirely. When a user performs an action that triggers an in-app notification (e.g., "You received a new message" badge update), the backend service writes the notification directly to Redis (keyed by `user_id` with a TTL of 5 minutes) and returns immediately. The mobile app polls Redis (or subscribes via a WebSocket) for in-app notifications. This path has <200ms end-to-end latency. (2) **background sync** — the same notification is ALSO published to the Kafka async pipeline for push (normal latency, 30s). The mobile app deduplicates by `notification_id`: if the in-app notification was already displayed, the push notification is suppressed (or shown as a summary). (3) **WebSocket gateway** — deploy a WebSocket gateway (or use an existing one if your chat system has it). When a notification is created, the producing service publishes to a Redis PubSub channel `notifications:user:{id}`. The WebSocket gateway subscribes to Redis PubSub and pushes the notification to the user's connected device in real-time (<50ms). This replaces polling. (4) **data model** — in-app notifications are stored in a lightweight KV store (Redis) with `ZADD user:{id}:inapp timestamp notification_json`. The app fetches the list with `ZREVRANGEBYSCORE`. This avoids database load. (5) **fallback** — if the WebSocket is disconnected, fall back to a short-poll of Redis every 5 seconds (still <200ms effective latency on reconnect). (6) **monitoring** — track `in_app_delivery_latency` (median <50ms, p99 <200ms) and `in_app_vs_push_duplicate_rate` (target <1% of in-app notifs having a corresponding push notif that the user also opens — indicates too much duplication).

## Q19: Your notification system uses a monolithic message template rendering engine. Each notification requires rendering a Go template with user-specific data (name, order details, etc.). At 50K notifications/sec, template rendering consumes 60% of CPU. How do you optimize the rendering path without changing the template language?

**Answer:** (1) **Pre-compile templates at boot** — parse all Go templates at application startup (not on each render). Store the parsed `*template.Template` in a sync.Map. This eliminates the parsing cost (~5ms per template → 0μs). (2) **Template caching with locality** — pre-render the static parts of each template at deploy time. For example, `"Hello {{.Name}}, your order {{.OrderID}} has shipped!"` → cache the prefix `"Hello "` and suffix `", your order has shipped!"` as constants. Only concatenate the dynamic parts at runtime. This reduces string allocation by ~70%. (3) **string interning** — user names, product names, and other high-cardinality strings that repeat across notifications are interned (sync.Map or a flyweight pool). Reuse the same string object across templates instead of allocating new ones. (4) **byte buffer pool** — use a `sync.Pool` of `bytes.Buffer` for template output. Each template render acquires a buffer from the pool, writes to it, and returns it. This eliminates per-render GC pressure from buffer allocations. (5) **batch rendering** — if multiple notifications share the same template and differ only in data (e.g., 1000 users all getting "your order has shipped"), render the template once per unique data set and broadcast the rendered output. This is a **1:N template fan-out**: render once, deliver to N recipients. (6) **hardware acceleration** — if template rendering remains CPU-bound, move it to a separate service written in a faster language (Rust or Go with the same template engine), deployed on compute-optimized instances (C-series). The main notification service offloads rendering via gRPC. (7) **monitoring** — `template_render_p50/p99` and `template_render_cpu_percent`. Target: render time <100μs per template. If exceeded, investigate which templates are slow (nested loops, complex logic) and refactor them.

## Q20: A regulator demands that your notification system must have a "kill switch" that can immediately stop ALL outbound notifications (push, SMS, email, in-app) within 60 seconds of a legal order. Design the kill switch architecture, ensuring it cannot be accidentally triggered and works even if the primary control plane is down.

**Answer:** **Multi-layer kill switch**: (1) **hardware-level cut** — at the network layer, the kill switch can **null-route** the outbound IP ranges of all notification provider gateways (Twilio, SendGrid, APNs, FCM). This is done via BGP announcement change: advertise a more specific route for the provider IPs to a blackhole next-hop. BGP propagation takes ~30 seconds globally. This layer works even if all servers are compromised. (2) **application-level cut** — a **global kill switch config** stored in etcd (multi-region replicated). Key: `global/killswitch/enabled = true|false`. All workers watch this key. When set to `true`, workers refuse to send any notification. Default watch timeout is 10 seconds, so within 10 seconds of the etcd write, all workers stop. (3) **circuit breaker at gateway** — each notification provider gateway has a circuit breaker that checks the kill switch before each batch send. The check is a local memory read (updated via etcd watch), so it adds <1μs overhead. (4) **fail-safe design** — the kill switch defaults to **off** (normal operation). If etcd is unreachable, the worker caches the last known kill switch state. If the last known state was `true` (kill active), it remains active until connectivity is restored and the switch is explicitly turned off. If the last known state was `false`, the worker continues sending (assuming no kill order). This prevents a network partition from accidentally disabling the kill switch. (5) **accidental trigger prevention** — require **two-person authentication** (2PA) to toggle the kill switch. The etcd key has a `modify` permission restricted to a security team's IAM role. Toggling requires a JWT signed by two separate approvers. (6) **audit log** — every toggle of the kill switch is logged to an immutable audit store (including who, when, and the legal order ID). (7) **testing** — test the kill switch quarterly. During the test, verify that all notification channels are blocked within 60 seconds and that the audit log captures the event. The test should include a recovery procedure: "verify no notifications were lost during the test window" (they were queued and should be released after the test).

