# Chapter 5 â€” Design Consistent Hashing

## Q1: In a standard modular hashing routing design ($hash(key) \pmod N$), what operational disaster occurs across a high-concurrency caching cluster if a single server machine node crashes?

**Options:**

- The remaining nodes automatically flip into an unencrypted data format state.
- The divisor $N$ changes, causing the hash mappings for almost all existing keys to shift, resulting in a massive global cache miss storm that can crash downstream primary databases.
- The cluster locks out all application connections permanently to preserve safety rules.
- The system database rows immediately change their index layouts into binary arrays.

**Answer:** The divisor $N$ changes, causing the hash mappings for almost all existing keys to shift, resulting in a massive global cache miss storm that can crash downstream primary databases.

## Q2: How does introducing 'Virtual Nodes' (vnodes) inside a Consistent Hashing ring topology resolve the statistical problem of non-uniform data distribution?

**Options:**

- Virtual nodes physically duplicate the underlying data blocks across multiple active disks.
- By mapping multiple random hash positions on the ring to a single physical server node, spreading data keys and lookup traffic evenly across the fleet and avoiding hot spots.
- Virtual nodes alter network layer transport systems to use raw UDP broadcast loops.
- They force primary relational databases to execute complete table sweeps hourly.

**Answer:** By mapping multiple random hash positions on the ring to a single physical server node, spreading data keys and lookup traffic evenly across the fleet and avoiding hot spots.

## Q3: When a new physical server node is added to a consistent hashing ring, what is the data movement boundary condition across the surrounding infrastructure?

**Options:**

- Every single key across all nodes in the cluster must be reallocated to a new home node location.
- Only a small fraction of the total keyspaceâ€”specifically the keys that hash into the slice of the ring claimed by the new nodeâ€”must be moved from its immediate clockwise neighbor node.
- Data blocks bypass all index steps and write directly into cold archival systems.
- The system forces all upstream clients to drop active WebSocket connection channels.

**Answer:** Only a small fraction of the total keyspaceâ€”specifically the keys that hash into the slice of the ring claimed by the new nodeâ€”must be moved from its immediate clockwise neighbor node.

## Q4: To route a cache request key to the correct server node inside a consistent hashing ring programmatically, what data structure and lookup logic should the application routing layer use?

**Options:**

- A flat sequential text file scanned linearly from beginning to end on every query.
- A sorted array or Balanced Binary Search Tree (like a Red-Black Tree) containing the hash positions of all nodes, executing a binary search (`ceiling` lookup) to find the first node position $\ge$ hash(key).
- A centralized relational database table performing full-table wildcard scans synchronously.
- A distributed circular ring buffer queue that overwrites older records dynamically.

**Answer:** A sorted array or Balanced Binary Search Tree (like a Red-Black Tree) containing the hash positions of all nodes, executing a binary search (`ceiling` lookup) to find the first node position $\ge$ hash(key).

## Q5: What is the primary architectural downside of configuring a massive number of virtual nodes (e.g., 1,000 vnodes per server node) inside a consistent hashing ring?

**Options:**

- It causes the data structure to lose its cryptographic token verification capabilities.
- It significantly increases the memory footprint of the routing table and slows down the lookup speed (as search time scales logarithmically with the number of ring nodes).
- It limits cluster data layout options to single-tenant monolithic architectures.
- It forces client browsers to execute absolute hardware level factory resets.

**Answer:** It significantly increases the memory footprint of the routing table and slows down the lookup speed (as search time scales logarithmically with the number of ring nodes).

## Q6: How can a Staff Engineer use consistent hashing to optimize edge CDN proxy selections for high-scale video asset caching?

**Options:**

- By routing all global user request targets to a single master origin storage system.
- By hashing the video asset's unique URL path key onto a consistent hash ring shared by edge CDN proxy nodes, ensuring popular videos stick to dedicated cache hosts while scaling smoothly.
- By converting all media files into unindexed binary strings inside relational indexes.
- By dropping edge firewall protective constraints whenever concurrent request counts spike.

**Answer:** By hashing the video asset's unique URL path key onto a consistent hash ring shared by edge CDN proxy nodes, ensuring popular videos stick to dedicated cache hosts while scaling smoothly.

## Q7: When physical server configurations vary widely across a cluster (e.g., Node A has 32GB RAM, Node B has 256GB RAM), how do you adapt consistent hashing to prevent overloading lower-tier nodes?

**Options:**

- Assign an equal number of virtual nodes to all physical machines uniformly regardless of hardware.
- Assign a proportional number of virtual nodes to each physical server based on its weight or capacity metric (e.g., allocating more vnodes to the high-RAM host).
- Force the database layer to drop all index tracking parameters to save storage.
- Wipe out local host memory buffers whenever an uneven load skew registers.

**Answer:** Assign a proportional number of virtual nodes to each physical server based on its weight or capacity metric (e.g., allocating more vnodes to the high-RAM host).

## Q8: If your consistent hashing configuration encounters a 'Hotspot' where a single key experiences millions of requests per second, how must the architecture react?

**Options:**

- Consistent hashing cannot solve this key-level hot spot; you must introduce an independent layer like local application memory caches or duplicate key replication with random suffixes.
- Move the entire ring data structure into local text logs inside edge balancer containers.
- Force a complete cluster-wide data vacuum sequence across all storage disks.
- Convert the specific key's text characters to use random string masks across shards.

**Answer:** Consistent hashing cannot solve this key-level hot spot; you must introduce an independent layer like local application memory caches or duplicate key replication with random suffixes.

## Q9: How do you achieve cluster consensus on the current structural layout of a consistent hashing ring across thousands of independent stateless web servers?

**Options:**

- Have each web server execute independent network polls against client devices randomly.
- Use a centralized coordination configuration tier (like Apache ZooKeeper or consul) or a gossip-protocol daemon to distribute active ring layout changes reliably.
- Store the entire ring structure parameters inside a raw text file on a shared network drive.
- Force all application microservices to route transactions through a single-threaded queue.

**Answer:** Use a centralized coordination configuration tier (like Apache ZooKeeper or consul) or a gossip-protocol daemon to distribute active ring layout changes reliably.

## Q10: Which cryptographic or non-cryptographic hashing algorithm is best suited for computing node positions on a consistent hashing ring to balance speed and distribution uniformity?

**Options:**

- A slow, cryptographically secure password hashing algorithm like bcrypt or argon2.
- A fast, high-distribution non-cryptographic hashing algorithm like MurmurHash3, xxHash, or Ketama variants.
- A basic modular division function targeting the server's local rack asset integer ID.
- An append-only character length check algorithm matching host string names.

**Answer:** A fast, high-distribution non-cryptographic hashing algorithm like MurmurHash3, xxHash, or Ketama variants.

## Advanced (Staff/Principal)

## Q11: How does the choice of hash function impact the stability of a consistent hashing ring when servers are repeatedly added and removed? What properties would you test for?

**Answer:** The hash function must produce **uniform distribution** and **low avalanche** sensitivity — small input changes should not produce wildly different outputs (which causes unnecessary key movement). Test for: (1) **load balancing std-dev** across nodes after 1000 random add/remove operations; (2) **key redistribution percentage** per node removal (should approach `1/N`); (3) **collision rate** in the hash space — collisions cause loss of keys unless handled; (4) **performance at scale** — hash speed matters when hashing millions of keys per second. MurmurHash3 and xxHash are preferred over MD5/SHA-1 because they're faster without meaningful distribution quality loss. Avoid using Java's built-in `hashCode()` or similar — they are not designed for ring distribution.

## Q12: Design a strategy for rebalancing data when a new datacenter is added. How do you prevent a thundering herd during simultaneous ring updates?

**Answer:** Use a **two-phase rebalancing** approach: (1) **shadow replication** — add the new datacenter's virtual nodes to the ring but mark them as "draining receivers". Existing nodes begin replicating data to new nodes asynchronously while still serving reads. (2) **atomic switch** — after replication completes, atomically update a **configuration version** in ZooKeeper/etcd that activates the new ring layout. Gateways use a **rate-limited background sync** to pick up the new ring, randomized over a window (e.g., 30–60 seconds with jitter) to prevent thundering herd. During transition, gateways can serve stale reads from the old ring config until they observe the new version. Use **bounded staleness**: any node lagging > TTL (e.g., 5 seconds) is cut out of the active pool.

## Q13: In a system using virtual nodes, how do you dynamically adjust virtual node counts based on real-time load metrics without triggering massive data movement?

**Answer:** Instead of changing vnode count (which triggers key redistribution), use **weighted consistent hashing** with a fixed vnode pool per server (e.g., 256). Adjust the **weight factor** dynamically: each ring position's token stores a weight multiplier. The gateway samples the weight when selecting a node — a node at 80% capacity gets weight 1.0, at 95% gets weight 0.5, effectively shedding traffic. This changes **query distribution** without moving any data. Combine with a **capacity-aware load balancer** that periodically gossips utilization metrics and adjusts weights via a central config store. Data movement is only triggered when crossing a hard threshold (e.g., weight drops below 0.1), at which point you run a controlled rehashing over hours.

## Q14: How would you modify consistent hashing to support data replication (each key stored on N nodes) while maintaining the ring's efficiency?

**Answer:** Two approaches: (1) **Replication via successor nodes** — hash the key to a ring position, then store the data on the next N distinct physical nodes clockwise. Simple but creates uneven replication when a node holds keys for multiple predecessors, causing cascading storage pressure. (2) **Separate replication ring** — maintain a secondary ring offset by a constant (`hash(key + "replica-1")`, `hash(key + "replica-2")`, etc.). This distributes replicas more uniformly because each replica uses a different hash seed. Both approaches benefit from **consistent hash rings** for each replica set. For production (e.g., Dynamo-style systems), prefer the separate ring method combined with preference lists to achieve sloppy quorums and hinted handoff without coupling replication to the primary ring's topology.

## Q15: What happens to in-flight requests during a ring structure change? Design a failover mechanism that guarantees at-least-once delivery without split-brain.

**Answer:** In-flight requests can fail in three ways: (1) request routed to a node that no longer owns the key; (2) request acknowledged to the client but not yet persisted; (3) duplicate routing to multiple nodes. Solution: implement a **version-vector ring** where each ring update increments a global epoch. Every request carries the epoch it was routed under. The receiving node checks if it owns the key under both its current epoch and the request's epoch. If not, it **proxies** the request to the correct owner or returns a **redirect** (HTTP 307). For at-least-once guarantee: the client uses **idempotency keys** with a bounded dedup window (e.g., 30 seconds). The server deduplicates based on `(key, idempotency_key, epoch)`. Split-brain is prevented by requiring **N/2+1 consensus** (Raft) before activating a new ring layout — a stale leader cannot install a conflicting ring version.

## Q16: Your team proposes replacing a simple `hash(key) % N` sharding scheme with consistent hashing to reduce reshuffling during cluster resizes. What hidden costs and failure modes would you raise in the design review before approving?

**Answer:** Hidden costs: (1) **implementation complexity** — consistent hashing requires a ring data structure (sorted array + binary search), client-side routing logic, and a coordination mechanism (ZooKeeper/etcd) for ring membership. `hash % N` is 3 lines of code. (2) **client driver upgrade** — every client library must be updated to support the ring; during a rolling upgrade, old and new clients may route differently, causing temporary data inconsistency. (3) **test burden** — ring changes during add/remove must be tested for correctness, performance, and race conditions. (4) **operational overhead** — adding/removing nodes requires updating the ring in the coordination store, which is an operational step that can fail. Failure modes: (5) **ring inconsistency** — if clients disagree on the ring state (partial ZooKeeper watch delivery), requests route to wrong nodes. (6) **hotspotting with non-uniform key distribution** — consistent hashing's "uniform" distribution is probabilistic; with a small number of vnodes, some nodes may get 20% more traffic than others. (7) **cascading failure on ring rebuild** — when a node is marked dead, the ring rebuild triggers a thundering herd of cache misses. Mitigation: the principal engineer should insist on a **side-by-side benchmark** showing the latency/reshuffling improvement justifies the complexity, and approve only with a documented runbook for ring-related incidents.

## Q17: How does consistent hashing interact with multi-tenancy? Design a strategy that ensures a tenant with 1000× the data of another does not cause storage imbalance, even though consistent hashing distributes by key hash, not by data volume.

**Answer:** Consistent hashing distributes by **key count**, not by **data size**. A tenant with 1B keys (each 1KB) will occupy ~1TB spread across all nodes uniformly if their keys are uniformly distributed. However, if the tenant's keys share a common prefix (e.g., `tenant_12345:order:*`), hashing the full key still produces uniform distribution — consistent hashing is key-aware, not prefix-aware, so this case is handled. The real problem is **uneven key distribution per tenant**: if Tenant A has 1B keys and Tenant B has 1K keys, Tenant A consumes 99.9% of storage but is spread across all nodes — this is actually fine for load balancing. The concern is **hot partitions**: if Tenant A's traffic is 100K req/s and concentrated on a single key (e.g., a counter), consistent hashing routes that key to one node, overloading it. Solution: (1) **key-level sharding** — for hot keys, split them with a suffix (`counter_1`, `counter_2`, ... `counter_N`) and merge during read (reduce+aggregate). (2) **tenant-aware capacity planning** — provision nodes such that the largest tenant's data fits with 2X headroom on the smallest node. (3) **weighted vnodes** — assign more vnodes to nodes with larger disk capacity, so data volume naturally skews toward higher-capacity nodes. (4) **rebalance alerting** — monitor per-node disk utilization std-dev; if > 20%, trigger investigation even if the ring is logically balanced.

## Q18: In a production incident, a brief network partition caused two zones to independently update the consistent hashing ring, resulting in a split-brain where each zone had a different membership view. How do you detect this post-fact and recover without data loss?

**Answer:** Detection: (1) **ring epoch divergence** — each ring update carries an epoch number (monotonically increasing). If two zones have different epoch numbers for the same logical ring, split-brain occurred. Expose epoch in a metrics endpoint; compare across zones in monitoring. (2) **cross-zone read-repair mismatch** — when a key is read from a node in zone A and the response includes the ring epoch, if zone B's epoch differs, log a split-brain alarm. Recovery: (3) **pause all ring updates** — prevent further divergence. (4) **determine authoritative ring** — the ring with the higher epoch number wins (or the ring that has majority consensus). (5) **reconcile data** — for every key owned by a node in the losing ring but not in the winning ring, that node's data is now orphaned. Scan the losing ring's nodes and re-insert orphaned keys into the winning ring's owners (background reconciliation job). (6) **data integrity check** — for overlapping keys (present in both rings), compare versions via vector clocks or last-write-wins timestamps; pick the latest. (7) **replay missed mutations** — replay the mutation log from the losing ring's epoch to the winning ring, filtering out already-applied mutations via idempotency keys. Prevention: use a **lease-based ring management** — each zone must hold a lease from a majority-quorum store (etcd) to modify the ring. A partitioned zone cannot obtain a lease, preventing split-brain updates entirely.

## Q19: Your system uses consistent hashing for cache node routing. You notice that after a node failure and recovery, the cache hit ratio drops from 90% to 40% and takes 30 minutes to recover. Diagnose the root cause and design a fix.

**Answer:** Root cause: when the failed node re-joins the ring, it is **cold** — it has no cached data. Consistent hashing correctly routes 1/N of all keys to the recovered node, but for those keys, the cache misses and the request passes through to the origin database. This is the **cold-start thundering herd**: the recovered node receives 1/N of all read traffic, all resulting in origin DB queries, potentially overwhelming it. The hit ratio stays low because the node must gradually warm up (LRU fills as users request different keys). Mitigation: (1) **staggered re-join** — when a node recovers, initially assign it only 10% of its normal vnodes. Gradually increase to 100% over 5 minutes. This spreads the cache-fill load over time. (2) **peer seeding** — before the failed node returns, have its neighbor(s) dump their top-hot keys to a shared Redis/s3 manifest. The recovering node reads this manifest and pre-fetches the hot keys from the origin before accepting traffic — it arrives "pre-warmed". (3) **reserved capacity** — over-provision the cluster by 1/N (e.g., N+1 nodes for N-way sharding). When a node fails, the extra node absorbs the slack with minimal per-node overload. (4) **read-through cache with rate-limited fill** — the origin DB uses a connection pool limiter; even if all cache fills hit it, the DB is protected.

## Q20: You are designing a global data store that uses consistent hashing across 10 datacenters. Read latency must be <5ms p99 globally. Write latency must be <50ms p99. How do you configure the ring and replication to meet both SLAs while maintaining strong consistency for critical keys?

**Answer:** This requires **latency-aware consistent hashing** with a **tunable consistency model**: (1) **ring topology** — each datacenter is a "super-node" on the ring, containing a local cluster of physical nodes. The ring is replicated across all datacenters (full replication, not sharding). Reads go to the **nearest datacenter** via GeoDNS → local replica → <5ms p99. (2) **strong consistency for critical keys** — use **consensus-based writes** (Raft) within a datacenter for durability, then **async cross-datacenter replication** for availability. For the subset of keys that need strong consistency (e.g., account balances), use a **leader lease per key**: the write must be acknowledged by a quorum of nodes across 3 datacenters (the key's "preference list" from the ring). Use **Paxos over WAN** with optimistic execution (speculate the write will succeed, roll back if not). (3) **latency optimization** — co-locate the ring's preference list members within a region where possible. Use **edge compute** to terminate the Paxos round within the same continent (e.g., us-east-1 + us-west-1 + eu-west-1 → 80ms inter-DC latency, still within 50ms for writes). (4) **fallback** — for non-critical keys, use eventual consistency: write locally, replicate async, and serve reads from any replica. The 5ms read SLA is met by serving from local replicas (which may be stale by seconds). The principal engineer's call: define which keys are critical, enforce strong consistency there (with the latency tax), and default to eventual for everything else. Do not apply the strong-consistency cost to the entire dataset.

