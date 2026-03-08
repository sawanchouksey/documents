## HashiCorp Nomad

### Workload Orchestration

##### Q. Is Nomad eventually or strongly consistent?
Uses both:
- **Consensus protocol:** Strongly consistent (state replication, scheduling)
- **Gossip protocol:** Manages server addresses (clustering, federation)

All Nomad-managed data is strongly consistent.

##### Q. Nomad datacenter vs Consul datacenter?
- **Nomad datacenter:** Equivalent to region, can have multiple datacenters
- **Consul datacenter:** More equivalent to Nomad region

Nomad supports two-tier approach; Consul relies on federation.

##### Q. What is bootstrapping a Nomad cluster?
Process of electing first leader and writing initial cluster state. Occurs when `bootstrap_expect` servers connect. Options like `default_scheduler_config` only affect initial bootstrap.

If state destroyed on all servers, cluster re-bootstraps with defaults.

---

