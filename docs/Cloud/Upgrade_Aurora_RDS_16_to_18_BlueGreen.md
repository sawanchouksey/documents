# Amazon RDS PostgreSQL Upgrade Guide
## Engine Version: 16 → 18 | Strategy: Blue/Green Deployment

---

| Field              | Details                                      |
|--------------------|----------------------------------------------|
| **Document Owner** | Sawan Chouskey                               |
| **Environment**    | Production                                   |
| **Service**        | app-service (app-app-xsp namespace)          |
| **Source Version** | PostgreSQL 16.x (engine family: postgres16)  |
| **Target Version** | PostgreSQL 18.x (engine family: postgres18)  |
| **Target Instance**| db.t4g.micro / gp3 storage                   |
| **Strategy**       | AWS RDS Blue/Green Deployment                |
| **Last Updated**   | 2026-02-26                                   |

> **⚠️ AWS RDS Availability Note:** PostgreSQL 18 was released upstream on 2025-09-25. Verify that your AWS region supports `postgres18` as an RDS engine family before proceeding. Check availability via `aws rds describe-db-engine-versions --engine postgres --query "DBEngineVersions[*].EngineVersion"`.

---

## Quick Reference Guide

| # | Phase | Action | Tool | Est. Time | Risk |
|---|-------|--------|------|-----------|------|
| 1 | **Pre-Upgrade** | Take manual snapshot of PG16 instance | Console / CLI | 5–15 min | None |
| 2 | **Pre-Upgrade** | Review PG17+PG18 breaking changes & parameter impacts | DBA | 30 min | None |
| 3 | **Pre-Upgrade** | Create `postgres18` parameter group | Console / CLI | 2 min | None |
| 4 | **Pre-Upgrade** | Set `rds.force_ssl=0`, `log_connections=all` in PG18 group; remove deprecated params | Console / CLI | 5 min | None |
| 5 | **Deployment** | Create Blue/Green deployment (PG18, db.t4g.micro, gp3) | Console / CLI | 20–60 min | None — blue untouched |
| 6 | **Validation** | Monitor green: replication lag < 1s, status = Available | Console / CLI | 5 min | None |
| 7 | **Validation** | Run SQL validation queries on green instance | pgAdmin / psql | 10–15 min | None |
| 8 | **⚠️ Switchover** | Switch over Blue/Green (30–120s write interruption) | Console / CLI | 2–5 min | **Brief downtime** |
| 9 | **Post-Upgrade** | Validate app health, CloudWatch, Instana, write ops | Console / App | 15–30 min | Low |
| 10 | **Cleanup** | Delete Blue/Green deployment & old PG16 instance | Console / CLI | 5 min | None |

**Total estimated duration:** ~2–3 hours (excluding observation window)
**Maintenance window required:** Yes — for Step 8 (Switchover) only
**Rollback available:** Yes — delete green before switchover, or restore from snapshot after

---

## Table of Contents

1. [Pre-Upgrade Checklist](#1-pre-upgrade-checklist)
2. [PostgreSQL 17 & 18 Breaking Changes Summary](#2-postgresql-17--18-breaking-changes-summary)
3. [Step 1 — Manual Snapshot (Pre-Upgrade Backup)](#3-step-1--manual-snapshot-pre-upgrade-backup)
4. [Step 2 — Create PostgreSQL 18 Parameter Group](#4-step-2--create-postgresql-18-parameter-group)
5. [Step 3 — Configure Parameter Group for PostgreSQL 18](#5-step-3--configure-parameter-group-for-postgresql-18)
6. [Step 4 — Create Blue/Green Deployment](#6-step-4--create-bluegreen-deployment)
7. [Step 5 — Monitor Green Environment Readiness](#7-step-5--monitor-green-environment-readiness)
8. [Step 6 — Pre-Switchover Validation](#8-step-6--pre-switchover-validation)
9. [Step 7 — Execute Switchover](#9-step-7--execute-switchover)
10. [Step 8 — Post-Switchover Validation](#10-step-8--post-switchover-validation)
11. [Step 9 — Cleanup](#11-step-9--cleanup)
12. [Rollback Plan](#12-rollback-plan)
13. [Reference Commands Summary](#13-reference-commands-summary)

---

## 1. Pre-Upgrade Checklist

Ensure all items below are confirmed before beginning the upgrade window.

| # | Checklist Item | Owner | Status |
|---|----------------|-------|--------|
| 1 | Change request approved and scheduled maintenance window confirmed | Change Manager | ☐ |
| 2 | Stakeholders notified (app teams, on-call engineers) | Team Lead | ☐ |
| 3 | Current RDS instance identifier and ARN documented | DBA | ☐ |
| 4 | Current PG16 parameter group name and settings exported/reviewed | DBA | ☐ |
| 5 | PG17 and PG18 breaking changes reviewed (see Section 2) | DBA | ☐ |
| 6 | Deprecated parameters identified and migration plan confirmed | DBA | ☐ |
| 7 | Application connection pool settings reviewed | App Team | ☐ |
| 8 | SSL settings and `pg_hba.conf` reviewed for PG18 compatibility | DBA | ☐ |
| 9 | Automated backups enabled and latest backup confirmed | DBA | ☐ |
| 10 | Rollback plan reviewed and approved | Architect | ☐ |
| 11 | Monitoring dashboards open (CloudWatch, Instana) | Ops | ☐ |
| 12 | AWS RDS `postgres18` engine family availability confirmed in target region | DBA | ☐ |

---

## 2. PostgreSQL 17 & 18 Breaking Changes Summary

Upgrading from PG16 to PG18 crosses **two major versions** (17 and 18). All breaking changes from both versions apply. This section documents every server parameter (GUC) change relevant to this upgrade path.

---

### 2.1 Removed Parameters (PG17)

These parameters were removed in PostgreSQL 17. **If your PG16 parameter group sets any of these, they must be removed before or during the upgrade — leaving them in the group will cause errors or unexpected behaviour.**

| Parameter | Removed In | Reason | Action Required |
|-----------|-----------|--------|-----------------|
| `old_snapshot_threshold` | PG17 | Feature removed; allowed vacuum to cause "snapshot too old" errors | Remove from parameter group |
| `db_user_namespace` | PG17 | Per-database user simulation feature removed (rarely used) | Remove from parameter group; ensure no DB relies on it |
| `trace_recovery_messages` | PG17 | No longer needed | Remove from parameter group |

---

### 2.2 Changed Parameters (PG17)

| Parameter | PG16 Default | PG17 Change | Action Required |
|-----------|-------------|------------|-----------------|
| `vacuum_buffer_usage_limit` | 256kB | Default increased to **2MB** | Review if custom value is set; the new default is better for most workloads |
| `wal_sync_method` | — | Value `fsync_writethrough` **removed on Windows** | Not applicable on Linux-based RDS |

---

### 2.3 New Parameters Introduced in PG17

These parameters are available in PG17 and forward (including PG18). They use PostgreSQL 17/18 defaults on RDS unless explicitly overridden.

| Parameter | Default | Category | Description |
|-----------|---------|----------|-------------|
| `allow_alter_system` | `on` | Compatibility | Disallow `ALTER SYSTEM` when set to `off` — useful for restricting DBA actions |
| `transaction_timeout` | `0` (disabled) | Client | Restrict maximum duration of any transaction (ms) |
| `huge_pages_status` | — | Preset (read-only) | Reports whether huge pages are active; useful when `huge_pages=try` |
| `event_triggers` | `on` | Client | Allows temporary disabling of event triggers for debugging |
| `commit_timestamp_buffers` | auto | Resource | SLRU cache size for commit timestamps |
| `multixact_member_buffers` | auto | Resource | SLRU cache size for multixact members |
| `multixact_offset_buffers` | auto | Resource | SLRU cache size for multixact offsets |
| `notify_buffers` | auto | Resource | SLRU cache size for NOTIFY |
| `serializable_buffers` | auto | Resource | SLRU cache size for serializable transactions |
| `subtransaction_buffers` | auto | Resource | SLRU cache size for subtransactions |
| `summarize_wal` | `off` | WAL | Enable WAL summarization files (required for incremental backups) |
| `wal_summary_keep_time` | `10d` | WAL | Retention period for WAL summary files |
| `sync_replication_slots` | `off` | Replication | Enable failover logical slot synchronization on standby |
| `synchronized_standby_slots` | `''` | Replication | Specify physical standbys that must be synced before subscriber visibility |
| `enable_group_by_reordering` | `on` | Query Tuning | Allow optimizer to reorder `GROUP BY` columns to match `ORDER BY` |
| `io_combine_limit` | `128kB` | Resource | Maximum size for combining multiple I/O reads into one system call |

---

### 2.4 Removed Parameters (PG18)

No additional server parameters were removed in PG18 beyond those listed in PG17 above.

---

### 2.5 Changed Parameters (PG18) — ⚠️ Action Required

| Parameter | PG16 Type / Value | PG18 Type / Value | Notes |
|-----------|------------------|------------------|-------|
| `log_connections` | **Boolean** (`0`/`1`) | **Enum** (`receipt`, `authentication`, `authorization`, `setup_durations`, `all`) | Old boolean `1` is still accepted as backward compatibility in PG18 but using enum `all` is recommended. RDS parameter group may expose it as enum only. |
| `effective_io_concurrency` | Default: **1** | Default: **16** | Increased to reflect modern hardware. If you had a custom value, re-evaluate. |
| `maintenance_io_concurrency` | Default: **10** | Default: **16** | Increased to reflect modern hardware. If you had a custom value, re-evaluate. |
| `ssl_ecdh_curve` | Configures single ECDH curve | **Renamed** to `ssl_groups`; now accepts multiple colon-separated curves | Old name `ssl_ecdh_curve` still works as an alias. Default now includes `X25519`. |
| `track_wal_io_timing` | Tracks timing in `pg_stat_wal` | Now controls tracking in **`pg_stat_io`** instead | `pg_stat_wal` WAL write/sync columns removed; data now in `pg_stat_io` |

---

### 2.6 New Parameters Introduced in PG18

These parameters are new in PG18 and use PostgreSQL 18 defaults on RDS unless explicitly overridden.

| Parameter | Default | Category | Description |
|-----------|---------|----------|-------------|
| `io_method` | `sync` (Linux: `io_uring` if available) | Resource | Asynchronous I/O subsystem: `sync`, `worker`, `io_uring`. New AIO feature in PG18. |
| `io_max_combine_limit` | `128kB` | Resource | Maximum ceiling for `io_combine_limit`; cannot be set higher at runtime |
| `vacuum_max_eager_freeze_failure_rate` | `0.03` | Vacuum | Rate of page freezing failures that will stop eager freezing during normal vacuums |
| `vacuum_truncate` | `on` | Vacuum | Controls whether VACUUM truncates empty pages from end of table files |
| `log_lock_failures` | `off` | Logging | Log `SELECT ... NOWAIT` lock acquisition failures |
| `track_cost_delay_timing` | `off` | Statistics | Track and report cost-delay timing for VACUUM and ANALYZE operations |
| `oauth_validator_libraries` | `''` | Connection | Shared libraries to load for OAuth token validation |
| `ssl_tls13_ciphers` | `''` | SSL | Colon-separated list of TLSv1.3 cipher suites to allow |
| `autovacuum_worker_slots` | `16` | Vacuum | Maximum slots available to autovacuum workers (allows runtime adjustment of `autovacuum_max_workers` without restart) |
| `autovacuum_vacuum_max_threshold` | `-1` (disabled) | Vacuum | Fixed dead-tuple count that triggers autovacuum, independent of percentage threshold |
| `idle_replication_slot_timeout` | `0` (disabled) | Replication | Automatically invalidate replication slots inactive for this duration |
| `max_active_replication_origins` | `10` | Replication | Maximum number of simultaneously active replication origins (previously controlled by `max_replication_slots`) |
| `extension_control_path` | system default | Client | Path(s) to search for extension control files |
| `file_copy_method` | `copy` | Resource | Controls whether `CREATE DATABASE ... STRATEGY=FILE_COPY` uses file copy or clone |
| `md5_password_warnings` | `on` | Connection | Emit deprecation warnings when MD5 passwords are set via `CREATE/ALTER ROLE` |
| `enable_self_join_elimination` | `on` | Query Tuning | Allow optimizer to eliminate unnecessary table self-joins |
| `enable_distinct_reordering` | `on` | Query Tuning | Allow optimizer to reorder `SELECT DISTINCT` keys to avoid sorting |
| `num_os_semaphores` | — | Preset (read-only) | Reports the number of OS semaphores required; useful for OS tuning |

---

### 2.7 MD5 Password Deprecation (PG18)

> **⚠️ Important:** MD5 password authentication is **deprecated** in PostgreSQL 18. `CREATE ROLE` and `ALTER ROLE` now emit deprecation warnings when setting MD5 passwords. Support for MD5 passwords will be **removed in a future major version**.
>
> **Action:** Migrate all users from MD5 to SCRAM-SHA-256 (`scram-sha-256` in `pg_hba.conf`) before or after this upgrade. Use `SELECT usename, passwd FROM pg_shadow WHERE passwd LIKE 'md5%';` to identify affected users.

---

### 2.8 Data Checksums (PG18 initdb Default)

> **Note:** PostgreSQL 18 now **enables data checksums by default** for new clusters created with `initdb`. AWS RDS Blue/Green upgrade does not re-run `initdb` on the existing data, so this does not affect in-place upgrades. However, new instances restored from PG18 snapshots will have checksum behaviour governed by the source cluster's checksum setting.

---

## 3. Step 1 — Manual Snapshot (Pre-Upgrade Backup)

Take a manual snapshot of the existing PostgreSQL 16 instance as a point-in-time recovery baseline before any changes are made.

### AWS Console

1. Open the [AWS RDS Console](https://console.aws.amazon.com/rds/)
2. In the left navigation pane, click **Databases**
3. Select your PostgreSQL 16 DB instance (blue instance)
4. Click **Actions** → **Take snapshot**
5. Enter Snapshot name: `app-service-pg16-pre-upgrade-YYYYMMDD`
6. Click **Take snapshot**
7. Navigate to **Snapshots** in the left pane and wait until **Status** = `Available`

### AWS CLI

```bash
aws rds create-db-snapshot \
  --db-instance-identifier <blue-db-instance-identifier> \
  --db-snapshot-identifier app-service-pg16-pre-upgrade-$(date +%Y%m%d)
```

**Verify snapshot completion:**
```bash
aws rds describe-db-snapshots \
  --db-snapshot-identifier app-service-pg16-pre-upgrade-$(date +%Y%m%d) \
  --query "DBSnapshots[0].{Status:Status,SnapshotTime:SnapshotCreateTime,Engine:EngineVersion}"
```

> Wait until `Status` = `available` before proceeding.

---

## 4. Step 2 — Create PostgreSQL 18 Parameter Group

Create a new RDS parameter group targeting the `postgres18` family. This group will be applied to the green (upgraded) environment.

### AWS Console

1. Open the [AWS RDS Console](https://console.aws.amazon.com/rds/)
2. In the left navigation pane, click **Parameter groups**
3. Click **Create parameter group**
4. Fill in the form:
   - **Parameter group family:** `postgres18`
   - **Type:** `DB Parameter Group`
   - **Group name:** `tf-parameter-postgres-app-service-18`
   - **Description:** `Custom parameter group for PostgreSQL 18 (blue-green upgrade)`
5. Click **Create**

### AWS CLI

```bash
aws rds create-db-parameter-group \
  --db-parameter-group-name tf-parameter-postgres-app-service-18 \
  --db-parameter-group-family postgres18 \
  --description "Custom parameter group for PostgreSQL 18 (blue-green upgrade)"
```

**Verify creation:**
```bash
aws rds describe-db-parameter-groups \
  --db-parameter-group-name tf-parameter-postgres-app-service-18 \
  --query "DBParameterGroups[0].{Name:DBParameterGroupName,Family:DBParameterGroupFamily,Description:Description}"
```

---

## 5. Step 3 — Configure Parameter Group for PostgreSQL 18

Apply custom parameter overrides required for the green environment. The parameters below must be explicitly set to match the existing PG16 behaviour or adopt PG18 best practices.

### 5.1 Required Parameter Overrides

| Parameter | Value | Apply Method | Reason |
|-----------|-------|--------------|--------|
| `log_connections` | `all` | `immediate` | **PG18 enum value** — equivalent to the old boolean `1`. Enables full connection logging for audit and monitoring. |

> **⚠️ PG18 Breaking Change — `log_connections`:**
> In PostgreSQL 16 and earlier, `log_connections` was a **boolean** (`0`/`1`).
> In **PostgreSQL 18**, it was extended to an **enum** type.
> Allowed values: `receipt`, `authentication`, `authorization`, `setup_durations`, `all`.
> The old boolean `1` is still accepted by PG18 for backward compatibility, but `all` is the canonical equivalent and the recommended value going forward.
>
> | Value | Meaning |
> |-------|---------|
> | `receipt` | Log when a connection packet is received |
> | `authentication` | Log after authentication completes |
> | `authorization` | Log after authorization (role/database checks) |
> | `setup_durations` | Log with timing for each connection setup phase |
> | `all` | Log all connection phases (equivalent to old `1`) |

### 5.2 Parameters to Remove from PG18 Group (Deprecated/Removed)

**Do NOT set these parameters in the `postgres18` group.** If they were present in your PG16 group, omit them entirely:

| Parameter | Removed In | Replacement |
|-----------|-----------|-------------|
| `old_snapshot_threshold` | PG17 | No replacement; feature removed |
| `db_user_namespace` | PG17 | No replacement; feature removed |
| `trace_recovery_messages` | PG17 | No replacement; no longer needed |

### 5.3 Optional New Parameters to Consider

These PG18 parameters are set to RDS defaults but may be worth explicitly configuring:

| Parameter | Recommended Value | Apply Method | Reason |
|-----------|------------------|--------------|--------|
| `log_lock_failures` | `1` | `immediate` | Log `NOWAIT` lock failures — useful for debugging contention |
| `autovacuum_vacuum_max_threshold` | `50000` | `immediate` | Cap autovacuum trigger at 50k dead tuples regardless of table size (prevents delays on very large tables) |
| `idle_replication_slot_timeout` | `86400000` *(24h in ms)* | `pending-reboot` | Auto-invalidate stale replication slots after 24 hours to prevent WAL accumulation |
| `md5_password_warnings` | `on` | `immediate` | Keep enabled to track MD5 password usage during migration to SCRAM |
| `track_cost_delay_timing` | `1` | `immediate` | Enable for enhanced vacuum timing visibility in CloudWatch / logs |

### 5.4 AWS Console Instructions

1. Open the [AWS RDS Console](https://console.aws.amazon.com/rds/)
2. In the left navigation pane, click **Parameter groups**
3. Click on `tf-parameter-postgres-app-service-18`
4. Click **Edit parameters**
5. Search for `rds.force_ssl`:
   - Set **Value** to `0`
   - **Apply method:** `pending-reboot`
6. Search for `log_connections`:
   - Set **Value** to `all` *(PG18 enum — equivalent to the old boolean `1`)*
   - **Apply method:** `immediate`
7. Click **Save changes**

### 5.5 AWS CLI

```bash
aws rds modify-db-parameter-group \
  --db-parameter-group-name tf-parameter-postgres-app-service-18 \
  --parameters \
    "ParameterName=rds.force_ssl,ParameterValue=0,ApplyMethod=pending-reboot" \
    "ParameterName=log_connections,ParameterValue=all,ApplyMethod=immediate"
```

**Verify the parameters were applied:**
```bash
aws rds describe-db-parameters \
  --db-parameter-group-name tf-parameter-postgres-app-service-18 \
  --query "Parameters[?ParameterName=='log_connections' || ParameterName=='rds.force_ssl'].{Name:ParameterName,Value:ParameterValue,ApplyType:ApplyType}"
```

---

## 6. Step 4 — Create Blue/Green Deployment

Create the Blue/Green deployment. AWS will provision a green (replica) environment running PostgreSQL 18, continuously replicating from the blue (existing PG16) instance using logical replication.

### AWS Console

1. Open the [AWS RDS Console](https://console.aws.amazon.com/rds/)
2. In the left navigation pane, click **Databases**
3. Select your PostgreSQL 16 DB instance (blue instance)
4. Click **Actions** → **Create Blue/Green Deployment**
5. Fill in the **Blue/Green deployment identifier**: `app-service-bg-pg16-to-pg18`
6. Under **Green environment settings**, configure:
   - **Engine version:** `18` (select the latest 18.x patch)
   - **DB instance class:** `db.t4g.micro`
   - **Storage type:** `gp3`
   - **DB parameter group:** `tf-parameter-postgres-app-service-18`
7. Leave all other settings as inherited from the blue instance
8. Click **Create Blue/Green Deployment**
9. Monitor the deployment on the **Databases** page — a new instance prefixed with `-green` will appear
10. Wait until the Blue/Green deployment **Status** = `Available` (20–60 minutes)

### AWS CLI

```bash
aws rds create-blue-green-deployment \
  --blue-green-deployment-name app-service-bg-pg16-to-pg18 \
  --source arn:aws:rds:<region>:<account-id>:db:<blue-db-instance-identifier> \
  --target-engine-version 18 \
  --target-db-parameter-group-name tf-parameter-postgres-app-service-18 \
  --target-db-instance-class db.t4g.micro \
  --target-storage-type gp3
```

**Monitor deployment creation:**
```bash
aws rds describe-blue-green-deployments \
  --filters Name=blue-green-deployment-name,Values=app-service-bg-pg16-to-pg18 \
  --query "BlueGreenDeployments[0].{Status:Status,GreenArn:GreenDeployment.DBInstanceArn}"
```

> Deployment typically takes **20–60 minutes** depending on database size. Wait until `Status` = `AVAILABLE` before proceeding.

---

## 7. Step 5 — Monitor Green Environment Readiness

Confirm the green instance is in sync and healthy before proceeding to switchover.

### AWS Console

1. Open the [AWS RDS Console](https://console.aws.amazon.com/rds/)
2. Click **Databases** and locate the green instance (e.g., `<instance-name>-green-xxxxx`)
3. Click on the green instance and go to the **Monitoring** tab
4. Check the following CloudWatch metrics:
   - **ReplicaLag** → should be `< 1 second`
   - **DatabaseConnections** → active and stable
   - **CPUUtilization** → within normal range
5. Confirm **DB instance status** = `Available`
6. Confirm **Engine version** shows `18.x`

### AWS CLI

**Check replication lag:**
```bash
aws cloudwatch get-metric-statistics \
  --namespace AWS/RDS \
  --metric-name ReplicaLag \
  --dimensions Name=DBInstanceIdentifier,Value=<green-db-instance-identifier> \
  --start-time $(date -u -d '5 minutes ago' +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 60 \
  --statistics Average
```

**Check green instance status:**
```bash
aws rds describe-db-instances \
  --db-instance-identifier <green-db-instance-identifier> \
  --query "DBInstances[0].{Status:DBInstanceStatus,Engine:EngineVersion,ParamGroup:DBParameterGroups[0].DBParameterGroupName}"
```

> Replication lag should be **< 1 second** before initiating switchover.

---

## 8. Step 6 — Pre-Switchover Validation

Connect to the **green instance** directly and run validation queries before switching over production traffic.

### AWS Console

1. Open the [AWS RDS Console](https://console.aws.amazon.com/rds/)
2. Click on the green instance and copy its **Endpoint** from the **Connectivity & security** tab
3. Connect via pgAdmin or your preferred SQL client using the green endpoint
4. Run the validation queries below

### Validation SQL Queries

```sql
-- 1. Validate PostgreSQL version (expect 18.x)
SELECT version();

-- 2. Validate all user tables are present
SELECT schemaname, tablename
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY schemaname, tablename;

-- 3. Validate row counts on critical tables (compare with blue)
SELECT relname, n_live_tup
FROM pg_stat_user_tables
ORDER BY n_live_tup DESC
LIMIT 20;

-- 4. Validate installed extensions
SELECT extname, extversion FROM pg_extension;

-- 5. Check for any invalid indexes (expect 0 rows)
SELECT indexrelid::regclass, indisvalid
FROM pg_index
WHERE NOT indisvalid;

-- 6. Check active connections
SELECT count(*), state FROM pg_stat_activity GROUP BY state;

-- 7. Confirm log_connections is set correctly (expect 'all' or enum value)
SHOW log_connections;

-- 8. Confirm removed parameters are no longer present
-- (old_snapshot_threshold, db_user_namespace, trace_recovery_messages should not appear)
SELECT name, setting FROM pg_settings
WHERE name IN ('old_snapshot_threshold', 'db_user_namespace', 'trace_recovery_messages');
-- Expected: 0 rows

-- 9. Check for MD5 passwords (plan migration to SCRAM-SHA-256)
SELECT usename, passwd FROM pg_shadow WHERE passwd LIKE 'md5%';

-- 10. Validate new PG18 defaults are in effect
SELECT name, setting, unit
FROM pg_settings
WHERE name IN (
  'effective_io_concurrency',
  'maintenance_io_concurrency',
  'io_method',
  'autovacuum_worker_slots'
);
```

**Expected:** PostgreSQL version shows `18.x`, all tables present, zero invalid indexes, `log_connections` shows `all`.

---

## 9. Step 7 — Execute Switchover

> ⚠️ **This step causes a brief write interruption (typically 30–120 seconds).** Ensure the application team is on standby and the maintenance window is active.

### AWS Console

1. Open the [AWS RDS Console](https://console.aws.amazon.com/rds/)
2. In the left navigation pane, click **Databases**
3. Select the **blue instance**
4. Click **Actions** → **Switch over or delete Blue/Green Deployment**
5. Select **Switch over**
6. Review the confirmation dialog — note the expected downtime warning
7. Enter the deployment name to confirm: `app-service-bg-pg16-to-pg18`
8. Click **Switch over**
9. Monitor the **Status** column on the Databases page
10. Wait until the Blue/Green deployment status = `SWITCHOVER_COMPLETED`
    - The green instance will take over the original endpoint
    - The blue instance will be renamed with a `-old` suffix

### AWS CLI

```bash
aws rds switchover-blue-green-deployment \
  --blue-green-deployment-identifier <blue-green-deployment-id> \
  --switchover-timeout 300
```

**Monitor switchover progress:**
```bash
aws rds describe-blue-green-deployments \
  --filters Name=blue-green-deployment-name,Values=app-service-bg-pg16-to-pg18 \
  --query "BlueGreenDeployments[0].{Status:Status,SwitchoverDetails:SwitchoverDetails}"
```

> Wait until `Status` = `SWITCHOVER_COMPLETED`.

---

## 10. Step 8 — Post-Switchover Validation

Immediately after switchover, validate that production traffic is routing to the upgraded instance and the application is healthy.

### AWS Console

1. Open the [AWS RDS Console](https://console.aws.amazon.com/rds/)
2. Confirm the primary instance now shows **Engine version** `18.x`
3. Confirm the endpoint DNS is unchanged (same as pre-switchover)
4. Open **Monitoring** tab → verify CloudWatch metrics are within baseline
5. Open **CloudWatch** → check for any RDS error logs or alarms

### Validation Checklist

| Validation | Command / Action | Expected Result |
|------------|-----------------|-----------------|
| Engine version | `SELECT version();` | PostgreSQL 18.x |
| Application health | Check app health endpoints | HTTP 200 |
| Connection pool | Check app logs for connection errors | No errors |
| CloudWatch metrics | CPU, FreeableMemory, DBConnections | Within normal baseline |
| Instana monitoring | Check `instana-monitoring=enabled` tag dashboard | No alerts |
| Write operations | Run a test INSERT/UPDATE/DELETE | Success |
| Endpoint unchanged | Compare DNS endpoint pre/post switchover | Identical |
| log_connections | `SHOW log_connections;` | `all` |
| I/O concurrency defaults | Check `effective_io_concurrency` | `16` |
| No MD5 warnings | Review RDS logs for MD5 deprecation warnings | Plan SCRAM migration if present |

---

## 11. Step 9 — Cleanup

Once post-switchover validation is confirmed stable (recommend **24–48 hour observation window**):

### AWS Console

1. Open the [AWS RDS Console](https://console.aws.amazon.com/rds/)
2. In the left navigation pane, click **Databases**
3. Select the **Blue/Green deployment**
4. Click **Actions** → **Delete Blue/Green Deployment**
5. Check **Delete the blue database instance** to also remove the old PG16 instance
6. Type `delete me` in the confirmation box and click **Delete**

### AWS CLI

```bash
aws rds delete-blue-green-deployment \
  --blue-green-deployment-identifier <blue-green-deployment-id> \
  --delete-target
```

> `--delete-target` removes the old blue (PG16) instance. **Omit this flag** if you want to retain the blue instance as an additional safety net before final decommission.

### Update Terraform State

Update the following in your Terraform configuration to reflect the upgraded environment:
- `postgres_version` variable → `18`
- `aws_db_parameter_group` `family` → `postgres18`
- `aws_db_parameter_group` `name` → `tf-parameter-postgres-app-service-18`

### Post-Cleanup: SCRAM Migration (Recommended)

After validating PG18 stability, migrate users from deprecated MD5 to SCRAM-SHA-256:

```sql
-- Change user passwords to trigger SCRAM re-hash
-- Run for each user identified in the pre-switchover MD5 check
ALTER ROLE <username> WITH PASSWORD '<new-password>';

-- Verify no MD5 passwords remain
SELECT usename FROM pg_shadow WHERE passwd LIKE 'md5%';
```

Also update `pg_hba.conf` (RDS: update the cluster parameter group) to use `scram-sha-256` instead of `md5` for relevant auth entries.

---

## 12. Rollback Plan

### Before Switchover — No Production Impact

If issues are found during green validation, simply delete the Blue/Green deployment:

**AWS Console:**
1. Open [AWS RDS Console](https://console.aws.amazon.com/rds/) → **Databases**
2. Select the blue instance → **Actions** → **Switch over or delete Blue/Green Deployment**
3. Select **Delete** → confirm deletion (blue instance remains untouched)

**AWS CLI:**
```bash
aws rds delete-blue-green-deployment \
  --blue-green-deployment-identifier <blue-green-deployment-id>
```

### After Switchover — Restore from Snapshot

If critical issues are detected after switchover, restore from the pre-upgrade manual snapshot taken in Step 1:

**AWS Console:**
1. Open [AWS RDS Console](https://console.aws.amazon.com/rds/) → **Snapshots**
2. Select `app-service-pg16-pre-upgrade-YYYYMMDD`
3. Click **Actions** → **Restore snapshot**
4. Set **DB instance identifier:** `app-service-pg16-restored`
5. Set **DB parameter group:** `tf-parameter-postgres-app-service` *(PG16 group)*
6. Click **Restore DB instance**
7. Once available, update the socat tunnel Kubernetes deployment to point to the restored endpoint and redeploy

**AWS CLI:**
```bash
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier app-service-pg16-restored \
  --db-snapshot-identifier app-service-pg16-pre-upgrade-<date> \
  --db-parameter-group-name tf-parameter-postgres-app-service
```

---

## 13. Reference Commands Summary

```bash
# 1. Create manual snapshot
aws rds create-db-snapshot \
  --db-instance-identifier <blue-db-instance-identifier> \
  --db-snapshot-identifier app-service-pg16-pre-upgrade-$(date +%Y%m%d)

# 2. Create PG18 parameter group
aws rds create-db-parameter-group \
  --db-parameter-group-name tf-parameter-postgres-app-service-18 \
  --db-parameter-group-family postgres18 \
  --description "Custom parameter group for PostgreSQL 18 (blue-green upgrade)"

# 3. Apply parameter overrides
#    log_connections uses enum 'all' in PG18 (replaces boolean 1 from PG16)
aws rds modify-db-parameter-group \
  --db-parameter-group-name tf-parameter-postgres-app-service-18 \
  --parameters \
    "ParameterName=rds.force_ssl,ParameterValue=0,ApplyMethod=pending-reboot" \
    "ParameterName=log_connections,ParameterValue=all,ApplyMethod=immediate"

# 4. Create Blue/Green deployment
aws rds create-blue-green-deployment \
  --blue-green-deployment-name app-service-bg-pg16-to-pg18 \
  --source arn:aws:rds:<region>:<account-id>:db:<blue-db-instance-identifier> \
  --target-engine-version 18 \
  --target-db-parameter-group-name tf-parameter-postgres-app-service-18 \
  --target-db-instance-class db.t4g.micro \
  --target-storage-type gp3

# 5. Check deployment status
aws rds describe-blue-green-deployments \
  --filters Name=blue-green-deployment-name,Values=app-service-bg-pg16-to-pg18 \
  --query "BlueGreenDeployments[0].{Status:Status,GreenArn:GreenDeployment.DBInstanceArn}"

# 6. Switchover (during maintenance window)
aws rds switchover-blue-green-deployment \
  --blue-green-deployment-identifier <blue-green-deployment-id> \
  --switchover-timeout 300

# 7. Cleanup after validation
aws rds delete-blue-green-deployment \
  --blue-green-deployment-identifier <blue-green-deployment-id> \
  --delete-target

# 8. Verify no MD5 passwords remain post-upgrade (connect via psql)
# psql -h <endpoint> -U <admin-user> -c "SELECT usename FROM pg_shadow WHERE passwd LIKE 'md5%';"
```
