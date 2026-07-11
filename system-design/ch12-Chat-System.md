# Chapter 12 â€” Design A Chat System

## Q1: When scale testing stateful WebSocket Gateways to handle 10 million concurrent active user connections, what operating system resource bottleneck is typically encountered first on an individual server node before CPU exhaustion occurs?

**Options:**

- Disk I/O write throughput capacity limits.
- The maximum file descriptor availability limit (C10K/C10M problem) along with kernel memory allocations for socket read/write buffers.
- The local hardware register width bounds.
- DNS resolution throughput limits on the loopback adapter interface.

**Answer:** The maximum file descriptor availability limit (C10K/C10M problem) along with kernel memory allocations for socket read/write buffers.

## Q2: If your chat application uses an active cluster of stateful WebSocket servers, what structural downside occurs if you use a standard Round-Robin Load Balancer without session awareness to distribute fresh socket requests?

**Options:**

- The load balancer automatically converts outbound packet frames into legacy FTP routes.
- Connections distribute uniformly at first, but because sessions are long-lived, server groups can exhibit severe load imbalances over time as users disconnect unevenly.
- The data formatting layer automatically switches to use raw Base16 hex coding blocks.
- Relational query optimizations become invalid across downstream database replica nodes.

**Answer:** Connections distribute uniformly at first, but because sessions are long-lived, server groups can exhibit severe load imbalances over time as users disconnect unevenly.

## Q3: To track a user's real-time online/offline presence status across millions of users, why is using a distributed key-value store with continuous HTTP short-polling heavily discouraged?

**Options:**

- Key-value stores cannot serialize basic character strings efficiently.
- The sheer volume of continuous read queries from millions of clients polling status fields will overwhelm the database clusters, introducing high infrastructure costs and severe read contention.
- Short-polling automatically triggers dynamic table schema rewrites across the storage layer.
- It forces data centers to drop multi-region replication settings to prevent corruption.

**Answer:** The sheer volume of continuous read queries from millions of clients polling status fields will overwhelm the database clusters, introducing high infrastructure costs and severe read contention.

## Q4: When storing chat history messages, why is a wide-column NoSQL database like Apache Cassandra or ScyllaDB often chosen over a traditional relational database model like MySQL at scale?

**Options:**

- Relational systems are unable to manage primary key index models over large datasets.
- Wide-column stores optimize for append-heavy write paths and support linear range scans based on a partition key (chat_id) and clustering column (message_id), matching chat access patterns cleanly.
- Cassandra automatically translates plain text payloads into encrypted bit vectors across the storage nodes.
- NoSQL architectures eliminate the requirement for implementing application rate-limit boundaries.

**Answer:** Wide-column stores optimize for append-heavy write paths and support linear range scans based on a partition key (chat_id) and clustering column (message_id), matching chat access patterns cleanly.

## Q5: In a group chat with 10,000 active participants, a user publishes a message, triggering a 'Fan-Out' write/distribution operation. How do you prevent this single message event from stalling the processing pipeline of the stateful gateway server?

**Options:**

- Force the sender node to block and wait until 10,000 synchronous network confirmations are logged sequentially.
- Publish the message event to an asynchronous message broker (e.g., Kafka or Pulsar) and let distributed consumer workers process fan-out distribution out-of-band, routing payloads to targets via an internal session map.
- Convert the message payload to a compressed binary format and broadcast it over local UDP loopback paths uniformly.
- Instantly disconnect all 10,000 participants to clear out active socket buffer queues.

**Answer:** Publish the message event to an asynchronous message broker (e.g., Kafka or Pulsar) and let distributed consumer workers process fan-out distribution out-of-band, routing payloads to targets via an internal session map.

## Q6: When a client device reconnects after a prolonged network drop, how should the system catch it up on missed chat history efficiently without overloading the database?

**Options:**

- Re-execute a complete full-table scan across the entire historical message database for all chats in system history.
- The client passes its last known, locally saved checkpoint sequence key or timestamp, allowing the message service to perform a highly bounded, indexed range query to fetch only the delta missing from that specific offset.
- Force the client to dump its local cache entirely and rebuild all history records dynamically using random string guesses.
- The server routes the full uncompressed data history cache over a slow single-threaded serial connection bus.

**Answer:** The client passes its last known, locally saved checkpoint sequence key or timestamp, allowing the message service to perform a highly bounded, indexed range query to fetch only the delta missing from that specific offset.

## Q7: What core performance flaw exists if you rely on a centralized relational database's standard auto-incrementing integer key to sequence message order across thousands of independent distributed chat rooms?

**Options:**

- Relational systems cannot store integer formats inside partitioned tables cleanly.
- The single auto-incrementing counter sequence creates a massive global write lock bottleneck across the database cluster, killing horizontal write scalability.
- It forces all data packet headers to expand past the standard MTU payload boundaries.
- It forces all downstream caching nodes to clear their entire memory contents every millisecond.

**Answer:** The single auto-incrementing counter sequence creates a massive global write lock bottleneck across the database cluster, killing horizontal write scalability.

## Q8: How does implementing an internal 'Session Registry' using a distributed hash ring or consistent hashing protect stateful chat gateway nodes during an unexpected node crash?

**Options:**

- It converts all existing active WebSockets into raw UDP frames automatically.
- It minimizes the impact of node reshuffling, ensuring that only the sessions directly connected to the crashed node must reconnect and re-map their states, leaving the remaining cluster stable.
- It guarantees that database writes skip index operations to save storage spaces.
- It forces client applications to execute complete hard factory resets.

**Answer:** It minimizes the impact of node reshuffling, ensuring that only the sessions directly connected to the crashed node must reconnect and re-map their states, leaving the remaining cluster stable.

## Q9: To track whether a message has been successfully Read by a recipient without introducing a write amplification storm in your database, how should Read Receipts be handled at scale?

**Options:**

- Execute an immediate synchronous row update operation in the database for every single individual message read event.
- Batch read receipt events in memory at the client or gateway layer, and update a single 'last_read_message_id' checkpoint watermark per user session in the database asynchronously.
- Route all read status strings into an alternative local text log directory on the gateway host machine.
- Drop read receipt events completely if concurrent chat room traffic surges past a baseline threshold.

**Answer:** Batch read receipt events in memory at the client or gateway layer, and update a single 'last_read_message_id' checkpoint watermark per user session in the database asynchronously.

## Q10: What is the role of an internal 'Heartbeat' mechanism between a client app and the stateful WebSocket gateway node?

**Options:**

- It forces the application to clear out its local device storage schemas periodically.
- It allows the server to detect dead client connections (zombie connections) caused by silent half-open network drops, enabling the system to reclaim server memory and update user presence accurately.
- It re-encrypts historical message payloads inside the downstream NoSQL column families.
- It synchronizes the absolute physical timezone configuration settings across the router interfaces.

**Answer:** It allows the server to detect dead client connections (zombie connections) caused by silent half-open network drops, enabling the system to reclaim server memory and update user presence accurately.

## Advanced (Staff/Principal)

## Q11: Design a multi-device sync protocol for a chat system that must deliver the same message ordering to web, mobile, and desktop clients simultaneously. How do you handle offline writes?

**Answer:** Use a **unified event log per conversation** (Kafka partition, Pulsar topic, or a replicated log). Each client connects as a consumer of the log. Messages are assigned a **monotonically increasing sequence number** by a sequencer node (or Raft log index) per conversation. All clients see the same sequence order. Offline writes: the mobile client stores outgoing messages in a **local SQLite DB** with a client-generated UUID. On reconnect, the client pushes the UUID-tagged messages to the server, which assigns sequence numbers and appends them to the log. Other clients receive the new messages in sequence order. Conflict resolution: if two offline users reply to the same message, both replies are appended in the order the server receives them. The UI uses the client UUID to deduplicate and mark "sent" status. For **read state sync**: each device's last-read sequence number is stored in Redis (CRDT-based, per-user key). Devices exchange read positions: device A advances from seq 100→120 and propagates to server; device B fetches the max read seq across all devices and updates its UI accordingly.

## Q12: How would you implement end-to-end encryption for a group chat with 10,000 participants? What key management and message encryption scheme do you use, and what are the trade-offs?

**Answer:** Standard approaches (PGP-style per-user keys) require O(n) encryption operations per message — 10,000 encryptions for 10K participants, which is infeasible for interactive chat. Use **MLS (Messaging Layer Security) — RFC 9420** with a **binary tree-based Group Ratchet**. Each member holds a set of "leaf" keys in a binary tree. Message encryption uses a group-level symmetric key (sender key) derived from the tree. When a member joins/leaves, only O(log n) key updates are needed via a procedural "key package" broadcast. For 10,000 members, a key update requires ~14 encrypted messages instead of 10,000. Trade-offs: (1) **external sender bottleneck** — the Delivery Service (server) must be trusted to sequence key updates correctly; a malicious DS can partition the group. Mitigate by using a **publicly verifiable transcript** — any member can audit the key update chain. (2) **out-of-order delivery** — if a member misses a key update (offline), they cannot decrypt subsequent messages until they catch up. The DS must store the last N key epochs and deliver on reconnect. (3) **metadata leakage** — the DS knows who is in the group and when they send messages, even if it cannot read contents. Mitigation: use **private message retrieval** or mix-net techniques at high latency cost.

## Q13: Design a message retention and compliance archive system that stores all chat history for 7 years while keeping hot storage costs under control. How do you handle legal holds and e-discovery?

**Answer:** **Tiered storage lifecycle**: (1) **hot tier** (first 90 days) — messages stored in Cassandra/DynamoDB (conversation_partition_key + message_timestamp). Fast point queries for recent history. (2) **warm tier** (90 days — 2 years) — older data auto-archived to compressed Avro/Parquet files in object storage (S3/GCS). A metadata index in DynamoDB maps (conversation_id, time_range) → S3 file path. Queries for this range fetch the file and scan — acceptable latency (seconds) for infrequent access. (3) **cold tier** (2 — 7 years) — further compressed with ZSTD (dictionary-trained on chat text, ~8:1 ratio), stored in **Glacier/Archive storage**. Access time: minutes to hours. **Legal holds**: when a legal hold is placed on a user or conversation, move all associated data from the tiered lifecycle into a dedicated **hold bucket** with immutable object lock (WORM) and indefinite retention. The hold bucket is indexed in a separate DB, exempt from all purge routines. **E-discovery**: a search interface over the warm + cold tiers using a custom inverted index built during archiving (word → conversation + timestamp). For compliance, the archive is append-only and checksum-verified. A background auditor scans the archive for bit-rot and repairs via erasure-coded parity shards.

## Q14: How do you design a chat system that gracefully degrades when the backend is partially partitioned? What features remain available and what falls back?

**Answer:** **Degradation tiers** based on partition severity: (1) **mild partition** (e.g., single Redis node down) — rate limiting and presence heartbeat checks fall back to a slower secondary store. Message sending continues normally. Some presence indicators may be stale (last-seen instead of real-time online). (2) **moderate partition** (e.g., loss of a Kafka broker) — message ordering degrades: new messages are stored directly in the database with a local timestamp and backfilled to Kafka when the partition heals. Clients may see slightly out-of-order messages. Group creation and admin operations are degraded to a synchronous DB write (slower, ~200ms). (3) **severe partition** (e.g., loss of primary database region) — **offline mode**. The client caches the last N messages locally (local SQLite). Users can read cached history and compose messages. Composed messages are queued locally with a status indicator ("sending…"). When connectivity is restored, the client pushes the queued messages with idempotency keys via a **delta sync** mechanism. The server accepts out-of-order messages by their client-generated UUID and inserts them into the conversation log at the appropriate position (using clock-skew-bounded timestamps). **Always-available features**: message composition, reading local cache, profile viewing. **Degraded features**: search, link preview, file upload. **Unavailable features**: real-time typing indicators, read receipts, admin controls.

## Q15: Describe a strategy for migrating 500 million chat users from a monolithic database to a distributed NoSQL system with zero downtime and no message loss.

**Answer:** **Dual-write + backfill strategy** (proven at WhatsApp/Discord scale): (1) **dual-write phase** — modify the chat service to write every incoming message to BOTH the legacy monolith AND the new NoSQL store (e.g., Cassandra or ScyllaDB). Reads still come from the monolith. Any NoSQL write failure is logged but does not block the write path. Deploy in canary (1% → 10% → 50% → 100% of traffic). Duration: 2 weeks to soak and monitor. (2) **backfill phase** — a background MapReduce job reads historical data from the monolith in bulk (partitioned by date range + shard) and inserts into NoSQL. Use **checkpointing** to resume from failures. Each batch is verified by comparing count + checksum against the source. (3) **verify phase** — compare a sample of reads from both systems (e.g., for every 1000th message, read from both and diff). Fix inconsistencies via a repair worker that re-reads from the monolith. (4) **cutover phase** — flip the read path from monolith to NoSQL for a small percentage of users (0.1% canary). Monitor P99 latency, error rate, and data freshness. Gradually increase to 100% over a week. Keep the monolith running in read-only shadow mode for another month — if any data inconsistency is found, the repair worker can fetch from the monolith. Only decommission the monolith after one month of zero shadow-mode divergences.

## Q16: Your chat system uses WebSockets. A production incident reveals that a single misbehaving client is sending 100,000 messages per second, causing the WebSocket gateway to consume 100% CPU and drop connections for all other users on that server. Design a per-connection isolation mechanism.

**Answer:** **Per-connection resource sandboxing**: (1) **connection-level rate limiting** — each WebSocket connection has a local token bucket (1,000 msg/min for regular users, 10,000 for bots). If exceeded, the gateway sends a `WS_CLOSE` with a custom code `PAYLOAD_TOO_LARGE` and drops the connection. This is enforced entirely in the gateway process (no external Redis call) to avoid CPU spikes. (2) **message size limit** — cap incoming message size at 64KB. Larger messages are rejected with a `CLOSE` frame. This prevents a single connection from flooding the gateway's receive buffer. (3) **goroutine/event-loop isolation** — each connection runs in its own goroutine (or event-loop handle). If a connection's goroutine blocks or spins, it does not affect other connections. Use a **connection-level context with a hard deadline** for each message processing step (e.g., 500ms per message). If exceeded, the connection is forcefully closed. (4) **memory isolation** — each connection has a bounded send buffer (max 256KB). If the client is not reading from the socket and the buffer fills up, the gateway closes the connection (backpressure propagation). This prevents a slow consumer from consuming all gateway memory. (5) **CPU monitoring** — the gateway tracks CPU time per connection (via `/proﬁle` or OS-level cgroups). If a single connection uses >10% of a core, it is suspended and disconnected. (6) **admission control** — if the gateway's CPU usage exceeds 80%, it stops accepting new connections (sends a 503 to the load balancer health check). The load balancer routes new connections to healthy gateways. (7) **defense in depth**: even with all these protections, a DDoS attack could overwhelm the gateway. Deploy a **WebSocket proxy** (e.g., HAProxy with per-connection rate limits) in front of the gateway as the first line of defense.

## Q17: Your chat application needs to support message editing and deletion. Edited messages should show an "edited" indicator, and deleted messages should disappear from all recipients' devices within 5 seconds. How do you propagate these mutations efficiently?

**Answer:** **Mutation log with CRDT-based overwrite**: (1) **message mutations as separate events** — editing a message generates a `MessageEdited` event with `(message_id, new_content, edit_timestamp, edit_count)`. Deleting generates a `MessageDeleted` event with `(message_id)`. These events are appended to the conversation's event log (Kafka partition). (2) **client-side conflict resolution** — each client maintains a local map of `message_id → latest_edit`. When a new `MessageEdited` event arrives, the client checks: if `edit_timestamp > current_edit_timestamp`, apply the edit; otherwise, ignore (stale update). This is a last-writer-wins CRDT. (3) **propagation** — already-delivered messages are updated via a **gap-free backfill**: each client receives a `last_event_sequence_number` on reconnect. The client requests all events after that sequence. For `MessageDeleted`, the client removes the message from the local UI state. (4) **5-second deletion SLA** — when a `MessageDeleted` event is published to Kafka, it has an in-memory **fast path**: the gateway's session map directly delivers the deletion event to all connected clients in the conversation (fan-out via the gateway's connection registry). This bypasses Kafka consumer lag. Offline clients receive the deletion when they reconnect and catch up on missed events. (5) **server-side enforcement** — even if a client ignores the deletion event (malicious client), the server refuses to serve the deleted message via the history API. The server deletes the message from the database (soft-delete with `deleted_at` timestamp). (6) **edited indicator** — the `MessageEdited` event includes `edit_count`. `edit_count > 0` triggers the "(edited)" label in the UI. Clients display the latest `new_content` from the last-applied edit.

## Q18: You are building a chat system for a healthcare application where messages must be retained for 7 years for compliance, but also must be immediately deletable if a patient revokes consent. How do you reconcile immutable retention with the right to deletion ("right to be forgotten")?

**Answer:** **Immutable retention with logical deletion**: (1) **immutable event log** — all messages are written to an append-only, immutable event log (Kafka → S3 with WORM lock). This satisfies the retention requirement — the data physically exists and cannot be altered. (2) **logical deletion layer** — the queryable database (the "read model") is a separate store (DynamoDB or Cassandra) that reflects the current visible state. When a patient revokes consent, the system (a) writes a `PatientDataSuppression` event to the immutable log (for audit purposes) and (b) deletes the patient's messages from the read model database. (3) **access control enforcement** — the API layer checks a **suppression list** (Redis Bloom filter of suppressed patient IDs) before serving any message. If the patient is suppressed, the API returns "no messages found" even though the data exists in the immutable store. (4) **data retention for compliance** — the immutable log is kept for 7 years but is **only accessible via a compliance API** with two-person authentication (legal + compliance officer). The customer-facing chat UI can never access the immutable log. (5) **audit trail** — the `PatientDataSuppression` event includes: `patient_id, admin_id who initiated, timestamp, legal_basis`. This proves to the regulator that the right to deletion was honored. (6) **physical deletion after retention period** — after 7 years + a safety margin (30 days), a background job reads the immutable log, identifies messages belonging to suppressed patients, and overwrites the S3 objects with zeros (or deletes them). The WORM policy is lifted for these specific objects via a legal hold release workflow. (7) **principal-level consideration**: the system must be designed from the start with this dual-layered approach — adding "right to deletion" to an immutable system retroactively is extremely difficult. The cost of immutable storage is justified by the regulatory penalty for non-compliance (up to 4% of global revenue under GDPR).

## Q19: A user reports that their chat messages are appearing out of order on their desktop app but correctly ordered on mobile. Investigation reveals the desktop client uses a different WebSocket gateway that processes messages slightly faster, causing a race condition. How do you guarantee cross-device message ordering?

**Answer:** Root cause: the desktop and mobile clients connect to different gateway nodes. Messages published to Kafka are consumed by both gateways independently. If gateway A processes the event and pushes to the desktop client before gateway B processes and pushes to the mobile client, but the desktop's clock is slightly ahead or the processing pipeline has more parallelism, the desktop may render a reply before the original message — ordering is violated. Fix: (1) **sequence numbers per conversation** — the event log assigns a monotonically increasing sequence number to each message within a conversation (via a Raft-based sequencer or a Kafka partition's offset per conversation). (2) **client-side ordering** — the client renders messages sorted by sequence number, NOT by arrival time. If a message with sequence 100 arrives before sequence 99, the client holds it in a buffer until 99 arrives (or for max 5 seconds; if 99 never arrives, request a gap-fill from the server). (3) **server-side ordering guarantee** — the gateway buffers outgoing messages per connection. It sends messages in sequence order, waiting for the previous message's ACK before sending the next (if ordered delivery is required). For unordered delivery (e.g., typing indicators), bypass the sequence buffer. (4) **cross-device sync** — when a device reconnects, it requests all messages after its last known sequence number. The server responds with an ordered list (sorted by sequence number). The client inserts them into the local store in order. (5) **monitoring** — track `out_of_order_message_count` and `sequence_gap_count`. If >0.1% of messages are rendered out of order, investigate the gateway's ordering guarantee. (6) **principal insight**: ordering is a fundamental distributed systems problem — it requires a **single authoritative order** (the sequence number) that all clients agree on, regardless of which gateway or device they use. Without a centralized ordering mechanism, "correct ordering" is impossible in a distributed chat system.

## Q20: Your chat platform is acquired by a company that uses a completely different protocol (Matrix instead of your proprietary protocol). They demand interoperability — users from either system must be able to message each other seamlessly. Design a federation bridge that handles identity mapping, protocol translation, and end-to-end encryption compatibility.

**Answer:** **Bidirectional federation bridge**: (1) **protocol translator** — deploy a bridge service that connects to both systems as a regular client. For your proprietary protocol → Matrix: the bridge logs into a Matrix account (e.g., `@bridge:yourdomain.com`), creates Matrix rooms mirroring your conversations, and relays messages. For Matrix → your protocol: the bridge opens a WebSocket connection to your gateway on behalf of the Matrix user. (2) **identity mapping** — maintain a `user_id → matrix_id` mapping in a consistent KV store (DynamoDB). When a user from your system sends a message to a Matrix user, the bridge looks up the Matrix user's ID, creates a portal room (if not exists), and relays the message with the sender's display name mapped. (3) **E2EE compatibility** — this is the hardest part. If your system uses E2EE and Matrix uses Olm/Megolm (double ratchet), the bridge must be an **E2EE termination point** — it decrypts from one side and re-encrypts for the other. This means the bridge sees plaintext (known as "trusted bridge" model). For higher security, use **transparent relay**: the bridge does not decrypt; instead, it passes the encrypted payload as an attachment in the Matrix room, and a custom Matrix client plugin decrypts it using the original keys. This requires both parties to use a shared key exchange mechanism (e.g., a QR code scanned at pairing time). (4) **presence sync** — the bridge subscribes to presence events from both systems and relays them (online/offline/last_seen). (5) **rate limiting** — the bridge enforces per-user rate limits to prevent a flood from one system overwhelming the other. (6) **monitoring** — track `bridged_messages_per_minute`, `bridge_latency_p99`, and `bridge_failure_rate`. Alert if >1% of bridged messages fail to deliver. (7) **graceful degradation** — if the bridge is overloaded, queue messages and deliver them later (best-effort). Never drop messages. The bridge exposes health endpoints for both systems' monitoring.

