# Chapter 6 â€” Design A Key-Value Store

## Q1: When designing a write-heavy, highly scalable distributed key-value store, why is an LSM-Tree (Log-Structured Merge-Tree) based storage engine commonly preferred over a B+Tree?

**Options:**

- LSM-Trees eliminate the need for an append-only write-ahead log file.
- LSM-Trees convert random writes into fast sequential appends by buffering updates in an in-memory MemTable and logging them, deferring sorting to background compaction cycles.
- LSM-Trees eliminate storage space compaction overhead entirely.
- LSM-Trees perform fast, multi-table synchronous joins on the critical read path.

**Answer:** LSM-Trees convert random writes into fast sequential appends by buffering updates in an in-memory MemTable and logging them, deferring sorting to background compaction cycles.

## Q2: According to the CAP theorem, if a multi-datacenter key-value store encounters a network partition, what architectural trade-off is forced upon the system design?

**Options:**

- You must choose between Consistency (CP) by rejecting writes to isolated partitions to prevent split-brains, or Availability (AP) by accepting local writes that cause divergent data states.
- The system can preserve both parameters by moving to a single-node monolithic state.
- The partition tolerance parameter can be disabled dynamically via configuration flags.
- The system must transition all active columns into binary arrays to protect consistency.

**Answer:** You must choose between Consistency (CP) by rejecting writes to isolated partitions to prevent split-brains, or Availability (AP) by accepting local writes that cause divergent data states.

## Q3: How does a distributed key-value store use Vector Clocks to identify data conflicts across multiple replica nodes without a central locking coordinator?

**Options:**

- Vector clocks compare physical system clock times using NTP time stepping rules.
- Each replica node maintains an array of logical clock counters `[node_id: counter]`. By tracking and passing these arrays with updates, the system can systematically deduce if an update causally follows, precedes, or conflicts with another.
- Vector clocks automatically overwrite older updates using a strict first-in, first-out memory queue.
- They force all storage node files to wipe out secondary index metadata parameters.

**Answer:** Each replica node maintains an array of logical clock counters `[node_id: counter]`. By tracking and passing these arrays with updates, the system can systematically deduce if an update causally follows, precedes, or conflicts with another.

## Q4: When configuring a distributed key-value store cluster with a replication factor of $N=3$, which quorum configuration guarantees strict read consistency (Strong Consistency)?

**Options:**

- Setting write quorum $W=1$ and read quorum $R=1$ to optimize connection throughput lanes.
- Ensuring the quorum equation satisfies $W + R > N$ (e.g., $W=2, R=2$), meaning the read and write replica sets will always overlap at least one up-to-date node.
- Moving all replication handling metrics to run over local loopback interfaces exclusively.
- Dropping write quorum variables entirely and relying on client apps to manage version states.

**Answer:** Ensuring the quorum equation satisfies $W + R > N$ (e.g., $W=2, R=2$), meaning the read and write replica sets will always overlap at least one up-to-date node.

## Q5: What performance optimization does a Bloom Filter provide inside the read path of an LSM-Tree based key-value storage engine?

**Options:**

- It compresses cleartext content strings into binary byte representations on disk.
- It acts as a fast, probabilistic in-memory check that can instantly verify if a key does *not* exist in an SSTable, preventing expensive, redundant disk lookups for missing keys.
- It automatically indexes unindexed tables across distributed storage shards.
- It forces client browsers to execute exponential backoff loops during connection drops.

**Answer:** It acts as a fast, probabilistic in-memory check that can instantly verify if a key does *not* exist in an SSTable, preventing expensive, redundant disk lookups for missing keys.

## Q6: In a distributed NoSQL key-value store, what role does the 'Gossip Protocol' play among cluster nodes?

**Options:**

- It manages the two-phase commit locks for transactional table schema migrations.
- It provides a decentralized, peer-to-peer communication model where nodes periodically exchange status information to maintain a shared view of cluster membership and node health.
- It routes real-time telemetry events out to global edge CDN caching networks.
- It forces client application containers to clear out local caching buffers hourly.

**Answer:** It provides a decentralized, peer-to-peer communication model where nodes periodically exchange status information to maintain a shared view of cluster membership and node health.

## Q7: To resolve data divergence between replica nodes asynchronously during low-traffic windows, what background repair mechanism is used in key-value clusters like DynamoDB or Cassandra?

**Options:**

- Re-executing full disk formatting sequences across all storage cluster machines sequentially.
- Using Merkle Trees (cryptographic tree hashes) to compare data blocks between replicas efficiently, identifying and syncing only the divergent data rows over the network.
- Converting the keyspace array to use random string configurations across regional datacenters.
- Dropping secondary index tracking configurations to reclaim storage spaces.

**Answer:** Using Merkle Trees (cryptographic tree hashes) to compare data blocks between replicas efficiently, identifying and syncing only the divergent data rows over the network.

## Q8: What is the primary operational trade-off of configuring an LSM-Tree storage engine to use 'Size-Tiered Compaction' versus 'Leveled Compaction'?

**Options:**

- Size-tiered compaction eliminates the need to track keyspaces using a write-ahead log.
- Size-tiered compaction optimizes for fast write paths with minimal overhead, but causes high space amplification; leveled compaction reduces space amplification and speeds up reads but incurs a heavy write amplification penalty.
- Leveled compaction mandates the deployment of single-leader replication models exclusively.
- Size-tiered compaction automatically encrypts payload attributes inside disk block boundaries.

**Answer:** Size-tiered compaction optimizes for fast write paths with minimal overhead, but causes high space amplification; leveled compaction reduces space amplification and speeds up reads but incurs a heavy write amplification penalty.

## Q9: When a key-value store encounters a write request while a primary storage replica node is temporarily offline, how does a 'Hinted Handoff' strategy maintain availability?

**Options:**

- The system drops the write event entirely and alerts the edge load balancer gateway tier.
- An alternate healthy node accepts the write and stores a temporary 'hint' record locally, asynchronously delivering the update payload once the primary replica recovers.
- The system blocks all inbound system operations until the dropped server finishes a reboot.
- The data formatting tier converts the record into flat text log directories locally.

**Answer:** An alternate healthy node accepts the write and stores a temporary 'hint' record locally, asynchronously delivering the update payload once the primary replica recovers.

## Q10: What is the architectural purpose of a Write-Ahead Log (WAL) inside a stateful database or key-value store node?

**Options:**

- To provide an indexing structure that accelerates read path wildcard lookups.
- To provide durability by appending incoming transactions sequentially to non-volatile disk before updating in-memory datastores, ensuring data recovery if the node crashes.
- To encrypt database transaction log data arrays before crossing data center networks.
- To throttle incoming client connection queries at the ingress gateway boundary.

**Answer:** To provide durability by appending incoming transactions sequentially to non-volatile disk before updating in-memory datastores, ensuring data recovery if the node crashes.

## Advanced (Staff/Principal)

## Q11: Under what specific workload patterns does an LSM-Tree's read amplification exceed a B-Tree's by an order of magnitude? How would you detect and mitigate this in production?

**Answer:** LSM-Tree read amplification spikes under **write-heavy workloads with high value locality** (e.g., frequent updates to the same set of keys). The same key exists in multiple SSTable generations — a point lookup must check MemTable → immutable MemTable → L0 (many files) → L1...L6. Worst case: 10+ SSTable lookups per read. Detection: monitor `max_sstable_count_per_level` and per-query `read_amplification_factor` (number of files checked). Mitigations: (1) **Bloom filters** on each SSTable (tune to 1% false-positive rate — 10 bits per key); (2) **compaction strategy switch** — if point-read-heavy, use Leveled Compaction (lower read amplification) instead of Size-Tiered; (3) **row cache** in front of LSM (caching hot keys bypasses all SSTable lookups); (4) **monolithic filter** — a single unified Bloom filter across all SSTable generations to short-circuit point lookups after a single probe.

## Q12: Design a hybrid storage engine that dynamically switches between LSM-Tree and B-Tree based on workload characteristics. What metrics trigger the switch?

**Answer:** A **tiered engine** with an LSM-Tree write-optimized front layer and a B-Tree read-optimized back layer. The LSM layer absorbs writes and recent updates. A background migration job moves "cold" data (keys not updated in >N minutes) from LSM to the B-Tree layer, where subsequent point reads are O(log n) with minimal amplification. The B-Tree is stored as a static, read-only, memory-mapped structure with periodic minor compaction (merge small updates). The LSM continues serving writes. Triggers: (1) **read-to-write ratio** crossing a threshold (e.g., >20:1 reads); (2) **compaction stall events** — if LSM compaction cannot keep up and backpressure triggers; (3) **P50/P99 read latency** exceeding a configurable target. When workload shifts back to write-heavy, the B-Tree layer is invalidated and data is absorbed back into LSM.

## Q13: How do you implement transactions and isolation levels in a distributed key-value store without a centralized coordinator? What are the failure modes?

**Answer:** Use **distributed transactions via Calvin-style deterministic ordering** or **Percolator-style two-phase commit with a lock service**. Calvin: a sequencing layer orders all transactions deterministically across all nodes before execution — no locks needed, but throughput is limited by the sequencer's clock rate. Percolator: a centralized timestamp oracle (or HLC) + per-key locks stored in the KV store itself (multi-row transactions via 2PC). Failure modes: (1) **lock holder crash** — resolved by a lease expiry mechanism (lock has a TTL, worker must heartbeat); (2) **prepared transaction never commits** — resolved by a recovery worker that scans prepared-but-incomplete transactions and resolves them (commit or abort) based on the primary key's status; (3) **clock skew** in timestamp oracle — mitigated by using a Hybrid Logical Clock (HLC) that captures causality even with bounded clock drift; (4) **deadlocks** — detected via lock-wait graphs or using a timeout-based fail-fast approach.

## Q14: Describe how you would implement a global secondary index in a Dynamo-style distributed KV store. What are the consistency challenges and how do you resolve them?

**Answer:** Global secondary indexes (GSI) are separate tables keyed by indexed attribute → primary key. Implementation: **eventual-GSI** — an asynchronous log streaming from the base table (via DynamoDB Streams / Kafka) to the GSI table. **Consistent-GSI** — a 2PC transaction updates both base table and GSI atomically, but this doubles write latency. Consistency challenges: (1) **write ordering** — if the base table update succeeds but GSI update fails, the index diverges. Solution: write-ahead-log with exactly-once semantics; (2) **hot partition** — if an indexed attribute has low cardinality (e.g., boolean `is_active`), all rows map to one GSI partition. Solution: add a shard suffix to the index key (e.g., `is_active#<hash_of_pk>`) and merge during query; (3) **backfill** — when adding a new GSI to existing data, must scan the entire base table without impacting production reads. Solution: use a throttled background scan with checkpointing, applying updates to GSI with backpressure.

## Q15: In a multi-tenant KV store, how do you prevent a noisy neighbor from starving other tenants of IOPS and memory? Design the admission control and scheduling mechanism.

**Answer:** Implement a **weighted fair queuing (WFQ) scheduler** at the storage engine level, with per-tenant token buckets for both read and write IOPS. Each tenant is assigned a weight proportional to their provisioned tier (e.g., tenant A: 10K IOPS, tenant B: 1K IOPS). The scheduler maintains a **compensating counter** per tenant — if a tenant exceeds its allocation, future requests are queued with a delay penalty proportional to the overage. For memory fairness, use **tenant-aware LRU eviction** in the page cache: each tenant has a reserved capacity floor and a burstable ceiling. Background compaction/GC runs are throttled per-tenant — if a tenant's write volume triggers compaction, the compaction IOPS are charged to that tenant's budget. Detect noisy neighbor by monitoring **P99 latency divergence** between tenants and **compaction-pending ratios** — alert when a single tenant's pending compaction exceeds 50% of the cluster total.

## Q16: A junior engineer proposes using Redis as a primary key-value store for a financial ledger system because "it's fast." As the principal engineer, what concerns do you raise, and under what specific conditions would you approve it?

**Answer:** Concerns: (1) **durability** — Redis is primarily an in-memory store with asynchronous disk persistence (RDB/AOF). A crash before the AOF sync loses up to 1 second of data. Financial ledgers require synchronous durability (fsync before acknowledging writes). (2) **consistency** — Redis replication is asynchronous and uses a weak consistency model. In a failover, the new leader may have stale data, causing ledger entries to vanish. (3) **transactions** — Redis `MULTI/EXEC` transactions are optimistic and do not support rollback on error — a half-applied transaction in a ledger is a compliance nightmare. (4) **compliance** — financial systems require audit logs, point-in-time recovery, and immutable write-ahead logs — Redis provides none natively. Conditions under which I would approve: (a) **non-authoritative cache** — Redis holds a fast copy of ledger data; the authoritative store is a SQL database with WAL. Redis is used only for read-path acceleration. (b) **idempotent writes** — every write is a CRDT (last-writer-wins) with a client-generated idempotency key; if Redis loses data, it can be rebuilt from the WAL. (c) **bounded data loss is contractually acceptable** — the business agrees to tolerate <1 second of data loss in exchange for <1ms read latency. (d) **Redis Cluster with AOF fsync=always and replication factor 3**. Even then, I'd push back on using Redis for ledgers and suggest using FoundationDB or PostgreSQL instead — the engineering cost of making Redis safe for money is higher than using a system designed for it.

## Q17: Your LSM-Tree based KV store's read latency has degraded by 10X over 6 months. After investigation, you find that the compaction strategy is not keeping up with the write rate — pending compaction has grown unboundedly. Design both the immediate mitigation and the long-term fix.

**Answer:** Immediate mitigation: (1) **throttle write traffic** — apply backpressure to write clients (reduce write rate by 50% at the admission controller) to let compaction catch up. (2) **add compaction threads** — temporarily increase compaction parallelism from 4 to 8 (if CPU headroom exists). (3) **offload cold SSTables** — manually force compaction of the largest SSTables (L0 → L1) with a higher priority. (4) **increase Bloom filter false-positive rate** — from 1% to 5% (reduces filter memory, frees compaction cache). This increases read I/O temporarily but may help if compaction is memory-bound. Long-term fix: (1) **switch compaction strategy** — if using Size-Tiered, switch to Leveled Compaction (less space amplification, fewer overlapping SSTables per level → fewer files to check per read). (2) **tiered storage** — write-ahead logs on NVMe, SSTables on SSD, cold data (accessed <1/month) on HDD. This reduces compaction pressure on the hot tier. (3) **compaction-aware admission control** — monitor `compaction_pending_bytes`. When it exceeds a threshold (e.g., 2× the MemTable size), reduce the write rate proportionally (backpressure). (4) **predictive compaction** — use a short-term write rate forecast (exponential smoothing on writes/sec) to pre-schedule compaction during low-write periods. (5) **monitoring SLO** — alert when `read_amplification > 10x` or `compaction_pending_bytes > 100GB`. These must be reviewed weekly in the capacity review.

## Q18: Design a key-value store that supports both strong consistency (linearizability) for some keys and eventual consistency for others, with the consistency level configurable per-operation by the client. How do you prevent clients from accidentally choosing weak consistency for critical operations?

**Answer:** **Consistency-level-per-operation API**: `Get(key, consistency_level: STRONG|EVENTUAL|CAUSAL)`, `Put(key, value, consistency_level: STRONG|EVENTUAL)`. Strong: routes to a Raft leader for the key's range (uses a multi-Raft group scheme like CockroachDB's ranges). Eventual: routes to the nearest replica, returns immediately without waiting for consensus. Causal: uses HLC timestamps; returns values with `hlo > last_seen_hlc`. Prevention of misconfiguration: (1) **schema-level default** — the KV store schema defines a default consistency level per key prefix (e.g., `accounts:*` defaults to STRONG, `sessions:*` defaults to EVENTUAL). This is set at deployment time and cannot be overridden by client code. (2) **runtime enforcement** — the server validates each operation's requested consistency level against the schema default. If a client requests EVENTUAL for a STRONG-default key, the server overrides to STRONG and logs a warning (alert if >0.1% of ops are overridden). (3) **dashboard + alert** — report `consistency_override_count` per service per key prefix. A spike indicates a client bug or a schema misconfiguration. (4) **audit log** — log every operation with its effective consistency level. During incident review, filter by `level=EVENTUAL` to identify operations that may have observed stale data.

## Q19: Your distributed KV store experiences a 10-minute full outage because a metadata operation (table creation) blocked all read/write operations across the cluster. This is the third such incident this year. Design a control plane architecture that makes metadata operations fully non-blocking.

**Answer:** Root cause: metadata operations (schema changes, splitting ranges, adding nodes) acquire a cluster-wide lock or barrier that stalls data-plane operations. Fix: **separate control plane from data plane** with **async schema versioning**: (1) **multi-version metadata** — the metadata store (etcd) maintains a versioned schema catalog. Each node holds a local cache of the current schema version (read from etcd at startup, refreshed via watches). Data-plane operations use their locally cached schema — they never contact the metadata store synchronously. (2) **non-blocking schema changes** — a schema change (e.g., `CREATE TABLE`) writes a new schema version to etcd. The change is applied **lazily** on each node: the node's background metadata sync worker picks up the new version, validates it, and updates the local cache. Data-plane requests continue using the old schema version until the sync completes. (3) **range splits** — splitting a hot range does NOT block operations. The split is planned by the control plane, which marks the range as `splitting`. The original range continues serving reads and writes. The two child ranges are created in `offline` state and pre-populated with a snapshot of the original range's data. Only after the pre-population completes (and the children are caught up via a change log) are they transitioned to `active`, at which point the original range is atomically retired via a versioned config update. (4) **testing** — use **deterministic simulation** (foundationdb-style) to verify that no sequence of control-plane operations can block data-plane operations. The key principle: the data plane must never make a synchronous RPC to the control plane.

## Q20: You need to migrate 10PB of data from a legacy DynamoDB-style KV store to a new Cassandra-based store with zero downtime and no meaningful latency increase. Design the migration plan, including how you validate data completeness after cutover.

**Answer:** **Trickle migration with double-write + shadow-read**: (1) **Phase 0: Shadow-write** — deploy a proxy in front of the legacy store that writes every mutation to BOTH systems (legacy + new). The proxy does not wait for the new store's ack — it fires and forgets. This warms the new store without affecting write latency. (2) **Phase 1: Backfill** — a MapReduce job reads all 10PB from the legacy store in parallel (1000 workers, each reading 10GB batches). For each item, it writes to the new store with a flag `migration_source: "backfill"`. The shadow-writer writes with `migration_source: "live"`. The new store uses LWW CRDTs: the `live` timestamp always wins over `backfill` (since `live` is chronologically newer). (3) **Phase 2: Shadow-read validation** — the proxy routes 1% of read traffic to both stores and compares results. Differences are logged and fixed via a repair worker (reads from legacy, overwrites new). Run until 0 divergence for 24 hours. (4) **Phase 3: Cutover** — route 100% of reads to the new store, but keep the legacy store live and dual-writing for 1 week. (5) **Phase 4: Tear-down** — stop dual-writes; keep legacy as read-only backup for another month. Validation at cutover: run a **checksum reconciliation** — for every partition, compute a Merkle tree checksum over all key-value pairs in both stores (background job, throttled to 10% of cluster IO). The Merkle trees must match within 0.001% divergence (allowing for in-flight mutations). If not, roll back by flipping the read path to legacy. The rollback plan: the proxy has a feature flag `use_new_store`. If p99 latency on the new store exceeds the legacy by >20% for 5 minutes, auto-rollback.

