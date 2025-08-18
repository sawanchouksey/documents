# Microsoft SQL Server DBA(Database Administrator)

## Install and COnfigure MSSQL 2016 Server
- Run **System Configuration Checker** before installing `MS SQL SEREVR`
- Create `folder` as names mentioned below used for **MSSQL SERVER INSTALLATION**

    - Used for **Data root directory** & **System database directory**
    ```
    mkdir SQL_DATA_FILES
    ```

    - Used for **System database log directory**
    ```
    mkdir SQL_LOG_FILES
    ```

    - Used for **Backup directory**
    ```
    MKDIR SQL_BACKUPS
    ```

    - Used for **SQL tempDB data directory**
    ```
    MKDIR SQL_TEMPDB
    ```

- Enable `FileStream` service to store data as `FileService` 
    - ✅Enable FILESTREAM for Transact-SQL access
        - ✅Enable FILESTREAM for file `I/O` access
            - Windows Share Name : **MSSQLSERVER** 

- [Download Link  for Adventure works 2022 Database](https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure?view=sql-server-ver16&tabs=ssms)

## MSSQL Server Operation
- `Stop MSSQL` Server windows command
```
net stop mssqlserver
```

- `Start MSSQL` Server windows command
```
net start mssqlserver /m
```

- - `Start MSSQL` Server windows command for everybody can connect
```
net start mssqlserver
```

## MSSQL Server Data Storage in DISK
- **.mdf** : It is used for store `data` in Disk with thelp of `pages` and `extents` which logically devided in pages from `0 to n`.
- **.ndf** : It is used for store additional data in Disk.
- **.ldf** : It is used for store Server `Transaction log` in a single file.

## MSSQL Log Manager
- Records changes to the database for recovery purpose. 
- Manage locks to control data access

## Enbale Full Recovery model to Take Backup for `Transaction Log`

To **enable the Full Recovery Model** and take a **Transaction Log backup** in **SQL Server Management Studio (SSMS)**, follow these **step-by-step** instructions:

### 🔧 **Part 1: Enable Full Recovery Model**

1. **Open SSMS** and connect to your SQL Server instance.

2. In **Object Explorer**, expand the **Databases** node.

3. Right-click the database you want to configure, then click **Properties**.

4. In the **Database Properties** dialog:

   * Click the **Options** page on the left.
   * Under **Recovery model**, select **Full** from the dropdown.

5. Click **OK** to save the changes.

✅ Your database is now in **Full Recovery Model**.

### 💾 **Part 2: Take a Full Database Backup (Required First)**

> Before taking a transaction log backup, you must take at least one full backup after switching to Full Recovery Model.

1. In **Object Explorer**, right-click the same database > go to **Tasks** > **Back Up…**

2. In the **Back Up Database** dialog:

   * Ensure **Backup type** is set to **Full**.
   * Confirm the **destination** (e.g., disk path like `C:\Backups\YourDB.bak`).

3. Click **OK** to create the full backup.

4. In **Media Option** Click In **reliablity** section and click ✅ `varify backup when finished` option.

### 🧾 **Part 3: Take a Transaction Log Backup**

1. In **Object Explorer**, right-click the database again > **Tasks** > **Back Up…**

2. In the **Back Up Database** window:

   * **Backup type**: Select **Transaction Log**
   * **Backup component**: Database
   * Choose or add a **destination path** (e.g., `C:\Backups\YourDB_Log.trn`)

3. Click **OK** to start the log backup.

### ✅ Summary

| Step | Action                            |
| ---- | --------------------------------- |
| 1    | Change Recovery Model to **Full** |
| 2    | Take a **Full Backup**            |
| 3    | Take a **Transaction Log Backup** |

## In SQL Server, `a copy-only backup` is a type of full backup that is created independently of the standard backup sequence. It doesn't affect the regular backup and restore operations, making it useful for ad-hoc backups or creating a baseline without disrupting the normal backup schedule. 

## Certainly! In SQL Server, you can split a backup into multiple files using the `BACKUP DATABASE` or `BACKUP LOG` commands with multiple `TO DISK` clauses. This allows the backup to be spread across multiple files, which can help with parallel writing and easier management of large backups.

### Command to Split Backup into Multiple Files

```sql
BACKUP DATABASE YourDatabaseName
TO 
    DISK = 'D:\Backup\YourDatabase_backup_1.bak',
    DISK = 'D:\Backup\YourDatabase_backup_2.bak',
    DISK = 'D:\Backup\YourDatabase_backup_3.bak'
WITH 
    FORMAT,     -- Creates a new media set, overwriting existing backups on those files
    INIT,       -- Overwrites existing backup sets on the media
    MEDIANAME = 'YourDatabaseBackupSet',
    NAME = 'Full Backup of YourDatabaseName';
```

### Explanation:

* **`BACKUP DATABASE YourDatabaseName`**: This specifies the database you want to back up.
* **`TO DISK = 'path\file.bak'`**: Specifies each backup file where the backup data will be written. You can add multiple `DISK` targets to split the backup into multiple files.
* **`WITH FORMAT`**: Initializes the backup media by overwriting any existing backups on the specified files.
* **`WITH INIT`**: Overwrites any existing backup sets on the files, so the backup is fresh.
* **`MEDIANAME`**: Logical name for the backup media set.
* **`NAME`**: A friendly name for the backup set.

### Benefits of Splitting Backup Files

* **Improved performance:** SQL Server can write data in parallel to multiple files.
* **Manageability:** Easier to move or store multiple smaller files than a single huge file.
* **Fault tolerance:** If one file is corrupt, sometimes others can still be used (depending on scenario).

## Backup Two Different location simutaneouly using `Mirror` option for same `database`

### What is Mirror Backup in SQL Server?

* **Mirror Backup** means the same backup set is written **at the same time to multiple destinations**.
* This is **not the same as splitting a backup** into parts; instead, the **full backup is written independently to each destination**.
* Useful for redundancy: one backup file on local disk, and another on remote/network drive.

### Syntax for Mirror Backup in SQL Server

You use the `MIRROR TO` clause along with the usual `TO DISK` for the primary backup destination.

Example:

```sql
BACKUP DATABASE YourDatabaseName
TO DISK = 'D:\Backup\YourDatabase_backup.bak'
MIRROR TO DISK = '\\NetworkShare\BackupFolder\YourDatabase_backup.bak'
WITH
    FORMAT,
    INIT,
    STATS = 10,
    PASSWORD = 'YourStrongPassword',
    NAME = 'Mirrored Full Backup of YourDatabaseName';
```

### Explanation of the command:

* **`TO DISK = '...'`**
  Primary backup file (local disk).

* **`MIRROR TO DISK = '...'`**
  Secondary backup file (remote or network location). This is the "mirror" target.

* **`WITH FORMAT`**
  Overwrites any existing backups on the media (creates a new media set).

* **`INIT`**
  Overwrites existing backup sets on the file.

* **`STATS = 10`**
  Shows progress messages every 10% during backup.

* **`PASSWORD = '...'`**
  Encrypts the backup with a password, requiring it for restore.

* **`NAME`**
  Friendly name for the backup set.

### Important Notes:

* Both files get the **full backup independently**.
* The SQL Server service account must have write permissions on **both locations**.
* The **`PASSWORD` option encrypts the backup header** with a password, so to restore you need to supply this password.
* You cannot mirror backup files to **local disk AND split files at the same time** (mirroring is for full backup copies, splitting is for dividing backup data).

### Summary:

| Clause             | Purpose                                  |
| ------------------ | ---------------------------------------- |
| `TO DISK =`        | Primary backup destination               |
| `MIRROR TO DISK =` | Secondary backup destination (mirror)    |
| `STATS = N`        | Show progress every N%                   |
| `PASSWORD = '...'` | Encrypt backup with password             |
| `FORMAT`, `INIT`   | Create new media set, overwrite existing |

### Example for Mirrored Backup with Stats and Password

```sql
BACKUP DATABASE AdventureWorks
TO DISK = 'C:\Backups\AdventureWorks_full.bak'
MIRROR TO DISK = '\\RemoteServer\Backups\AdventureWorks_full.bak'
WITH
    FORMAT,
    INIT,
    STATS = 10,
    PASSWORD = 'MySecureP@ssw0rd',
    NAME = 'Mirrored Full Backup of AdventureWorks';
```

## Differential Backup Explanation

### What is a Differential Backup?

* A **differential backup** captures **only the data that has changed since the last full backup**.
* It is **smaller and faster** than a full backup because it contains only the "delta" changes.
* To restore a database, you first restore the last full backup, then apply the latest differential backup.
* Differential backups help reduce backup time and storage space while still allowing point-in-time recovery between full backups.

### Syntax for Differential Backup

```sql
BACKUP DATABASE YourDatabaseName
TO DISK = 'backup_location\YourDatabase_diff.bak'
WITH DIFFERENTIAL,
     INIT,        -- optional, overwrites existing backup file
     FORMAT,      -- optional, creates new media set
     STATS = 10,  -- optional, shows backup progress every 10%
     NAME = 'Differential Backup of YourDatabaseName';
```

### Explanation of Syntax

* **`BACKUP DATABASE YourDatabaseName`**
  Specifies the database to back up.

* **`TO DISK = '...'`**
  The destination backup file (can be local disk or network share).

* **`WITH DIFFERENTIAL`**
  Tells SQL Server to perform a differential backup, capturing only changes since last full backup.

* **`INIT`**
  Optional. Overwrites the existing backup file if it exists.

* **`FORMAT`**
  Optional. Creates a new media set (usually used with `INIT`).

* **`STATS = 10`**
  Optional. Displays progress updates every 10%.

* **`NAME = '...'`**
  A friendly name for the backup set.

### Example Command: Differential Backup

```sql
BACKUP DATABASE AdventureWorks
TO DISK = 'D:\Backups\AdventureWorks_diff.bak'
WITH DIFFERENTIAL,
     INIT,
     STATS = 10,
     NAME = 'Differential Backup of AdventureWorks';
```

### About `.diff` Extension for Differential Backups

* **File extension like `.diff` is not mandatory or enforced by SQL Server.**
  SQL Server treats backup files as binary blobs; the file extension does **not affect** how the backup works.

* The **default and most common extension is `.bak`**, used for all types of backups (full, differential, log).

* Some DBAs or organizations use **custom extensions** like:

  * `.diff` or `.differential` for differential backups
  * `.full` for full backups
  * `.trn` or `.log` for transaction log backups

* These custom extensions are purely **for organizational clarity** and easier identification of backup types by humans or scripts.

### Example Naming Conventions

| Backup Type            | Typical Extension | Example Filename                  |
| ---------------------- | ----------------- | --------------------------------- |
| Full Backup            | `.bak` or `.full` | `AdventureWorks_full.bak`         |
| Differential Backup    | `.bak` or `.diff` | `AdventureWorks_diff.diff`        |
| Transaction Log Backup | `.trn` or `.log`  | `AdventureWorks_log_20250814.trn` |

### Key points:

* You can **name your differential backup files with `.diff` extension** if you like:

  ```sql
  BACKUP DATABASE AdventureWorks
  TO DISK = 'D:\Backups\AdventureWorks_2025_08_14.diff'
  WITH DIFFERENTIAL, INIT, STATS = 10;
  ```

* SQL Server will back up normally regardless of the file extension.

* When restoring, just reference the file path and name exactly—extension does not matter to SQL Server.

### Why use `.diff`?

* Helps humans quickly identify the backup type by filename.
* Useful in scripts or automation to filter or pick backup files.
* Keeps backups organized when you have many types in the same folder.

### Important Points about Differential Backups

* Differential backups depend on the **most recent full backup**. If the full backup is overwritten or lost, differential backups become useless.
* Each differential backup contains all changes since the last full backup, so differential backup size increases over time until the next full backup.
* Typically, organizations schedule full backups weekly and differential backups daily or more frequently.

### How to restore from Differential Backup?

1. Restore the **full backup** (with `NORECOVERY` to keep the database ready for more restores).
2. Restore the **latest differential backup** (with `RECOVERY` to bring database online).

Example restore commands:

```sql
-- Step 1: Restore full backup
RESTORE DATABASE AdventureWorks
FROM DISK = 'D:\Backups\AdventureWorks_full.bak'
WITH NORECOVERY;

-- Step 2: Restore latest differential backup
RESTORE DATABASE AdventureWorks
FROM DISK = 'D:\Backups\AdventureWorks_diff.bak'
WITH RECOVERY;
```

## **Transaction Log Backups** in SQL Server 

### 1. What is a Transaction Log Backup?

* **Transaction Log backups** capture all the transaction log records that have been generated since the last transaction log backup (or since the full backup if no log backups have been taken).
* They allow **point-in-time recovery** of the database by restoring the full backup and then restoring a sequence of transaction log backups.
* Transaction log backups are **only possible when the database recovery model is FULL or BULK\_LOGGED** (not SIMPLE).
* They help **truncate the log file**, freeing space within the transaction log.

### 2. Importance and Use of Transaction Log Backups

* **Point-in-time recovery:** You can restore your database to any moment between backups.
* **Minimizing data loss:** Regular log backups mean less data loss if the database crashes.
* **Prevent log growth:** Log backups free up space inside the log file, preventing it from growing excessively.
* **Required for databases in FULL or BULK\_LOGGED recovery models** to manage log size and enable restore options.

### 3. File Extension for Transaction Log Backups: `.trn`

* By convention, transaction log backups are saved with a `.trn` extension, but **you can use any extension**.
* Using `.trn` helps differentiate log backups from full (`.bak`) or differential (`.diff`) backups.

### 4. How to Take Transaction Log Backup Using SSMS GUI — Step by Step

1. **Open SQL Server Management Studio (SSMS)** and connect to your SQL Server instance.

2. **Expand the Databases node** in Object Explorer and locate your database.

3. **Right-click on the database**, go to **Tasks > Back Up...**

4. In the **Back Up Database** window:

   * **Backup type:** Select **Transaction Log** from the dropdown.
   * **Backup component:** Leave as **Database**.
   * **Backup set:** Provide a name (e.g., `Log Backup on 2025-08-14`).
   * **Destination:** Remove any existing backup destinations if needed, and click **Add...**.
   * Choose or type the path where you want to save the `.trn` file, e.g., `D:\Backups\YourDatabase_LogBackup_20250814.trn`.
   * Click **OK** to add the destination.

5. Optionally, configure **Options** tab:

   * You can choose to overwrite or append to existing backup sets.
   * Compression (if enabled in your SQL Server edition) can be selected here.

6. Click **OK** to start the transaction log backup.

7. SSMS will show a progress message and confirm once the backup is complete.

### 5. How to Take Transaction Log Backup Using T-SQL Command

```sql
BACKUP LOG YourDatabaseName
TO DISK = 'D:\Backups\YourDatabase_LogBackup_20250814.trn'
WITH INIT, -- overwrites existing backup file
     STATS = 10; -- shows progress every 10%
```

### 6. Important Notes:

* Make sure your database **recovery model** is FULL or BULK\_LOGGED to perform log backups.

Check current recovery model:

```sql
SELECT name, recovery_model_desc 
FROM sys.databases
WHERE name = 'YourDatabaseName';
```

To change recovery model to FULL:

```sql
ALTER DATABASE YourDatabaseName SET RECOVERY FULL;
```

* Log backups can be scheduled frequently (e.g., every 15 minutes) to minimize data loss.
* Full backups and differential backups are still necessary alongside log backups for a complete backup strategy.

### 7. How to Restore Using Transaction Log Backups?

To restore a database to a point in time using transaction log backups:

```sql
-- Step 1: Restore full backup with NORECOVERY
RESTORE DATABASE YourDatabaseName
FROM DISK = 'D:\Backups\YourDatabase_full.bak'
WITH NORECOVERY;

-- Step 2: (Optional) Restore latest differential backup with NORECOVERY if exists
RESTORE DATABASE YourDatabaseName
FROM DISK = 'D:\Backups\YourDatabase_diff.bak'
WITH NORECOVERY;

-- Step 3: Restore transaction log backups in sequence with NORECOVERY
RESTORE LOG YourDatabaseName
FROM DISK = 'D:\Backups\YourDatabase_LogBackup_20250814.trn'
WITH NORECOVERY;

-- Step 4: Final transaction log restore with RECOVERY to bring database online
RESTORE LOG YourDatabaseName
FROM DISK = 'D:\Backups\YourDatabase_LogBackup_Last.trn'
WITH RECOVERY;
```

## Absolutely! Let’s talk about **Transaction Log Backups** in SQL Server — what they are, why they’re important, how to create them both via **SQL Server Management Studio (SSMS) GUI** and with **T-SQL commands**, and their typical file extension `.trn`.

---

# 1. What is a Transaction Log Backup?

* **Transaction Log backups** capture all the transaction log records that have been generated since the last transaction log backup (or since the full backup if no log backups have been taken).
* They allow **point-in-time recovery** of the database by restoring the full backup and then restoring a sequence of transaction log backups.
* Transaction log backups are **only possible when the database recovery model is FULL or BULK\_LOGGED** (not SIMPLE).
* They help **truncate the log file**, freeing space within the transaction log.

---

# 2. Importance and Use of Transaction Log Backups

* **Point-in-time recovery:** You can restore your database to any moment between backups.
* **Minimizing data loss:** Regular log backups mean less data loss if the database crashes.
* **Prevent log growth:** Log backups free up space inside the log file, preventing it from growing excessively.
* **Required for databases in FULL or BULK\_LOGGED recovery models** to manage log size and enable restore options.

---

# 3. File Extension for Transaction Log Backups: `.trn`

* By convention, transaction log backups are saved with a `.trn` extension, but **you can use any extension**.
* Using `.trn` helps differentiate log backups from full (`.bak`) or differential (`.diff`) backups.

---

# 4. How to Take Transaction Log Backup Using SSMS GUI — Step by Step

1. **Open SQL Server Management Studio (SSMS)** and connect to your SQL Server instance.

2. **Expand the Databases node** in Object Explorer and locate your database.

3. **Right-click on the database**, go to **Tasks > Back Up...**

4. In the **Back Up Database** window:

   * **Backup type:** Select **Transaction Log** from the dropdown.
   * **Backup component:** Leave as **Database**.
   * **Backup set:** Provide a name (e.g., `Log Backup on 2025-08-14`).
   * **Destination:** Remove any existing backup destinations if needed, and click **Add...**.
   * Choose or type the path where you want to save the `.trn` file, e.g., `D:\Backups\YourDatabase_LogBackup_20250814.trn`.
   * Click **OK** to add the destination.

5. Optionally, configure **Options** tab:

   * You can choose to overwrite or append to existing backup sets.
   * Compression (if enabled in your SQL Server edition) can be selected here.

6. Click **OK** to start the transaction log backup.

7. SSMS will show a progress message and confirm once the backup is complete.

---

# 5. How to Take Transaction Log Backup Using T-SQL Command

```sql
BACKUP LOG YourDatabaseName
TO DISK = 'D:\Backups\YourDatabase_LogBackup_20250814.trn'
WITH INIT, -- overwrites existing backup file
     STATS = 10; -- shows progress every 10%
```

---

# 6. Important Notes:

* Make sure your database **recovery model** is FULL or BULK\_LOGGED to perform log backups.

Check current recovery model:

```sql
SELECT name, recovery_model_desc 
FROM sys.databases
WHERE name = 'YourDatabaseName';
```

To change recovery model to FULL:

```sql
ALTER DATABASE YourDatabaseName SET RECOVERY FULL;
```

* Log backups can be scheduled frequently (e.g., every 15 minutes) to minimize data loss.
* Full backups and differential backups are still necessary alongside log backups for a complete backup strategy.

---

# 7. How to Restore Using Transaction Log Backups?

To restore a database to a point in time using transaction log backups:

```sql
-- Step 1: Restore full backup with NORECOVERY
RESTORE DATABASE YourDatabaseName
FROM DISK = 'D:\Backups\YourDatabase_full.bak'
WITH NORECOVERY;

-- Step 2: (Optional) Restore latest differential backup with NORECOVERY if exists
RESTORE DATABASE YourDatabaseName
FROM DISK = 'D:\Backups\YourDatabase_diff.bak'
WITH NORECOVERY;

-- Step 3: Restore transaction log backups in sequence with NORECOVERY
RESTORE LOG YourDatabaseName
FROM DISK = 'D:\Backups\YourDatabase_LogBackup_20250814.trn'
WITH NORECOVERY;

-- Step 4: Final transaction log restore with RECOVERY to bring database online
RESTORE LOG YourDatabaseName
FROM DISK = 'D:\Backups\YourDatabase_LogBackup_Last.trn'
WITH RECOVERY;
```

## What is `Page Level Restore / Recovery`

- Page restore is a technique used to replace corrupted pages of information in a database with uncorrupted data
from a backup.

- The intent of the restore is to fix one or more corrupted pages from the available backups.

- To identify corrupted pages, look for pages marked as “suspect” in the table, msdb syspect_pages

- Most of the time, performing a page level restore suffices for database availability.

- A good backup strategy is a key to recovery or restoration, and SQL Server provides us with an option to fix
database pages at a granular level.

- Performing a page level restore in SQL Server is a clever option wherein the restoration of the entire VLDB
database backup is not required.

- Identifying the corruption and finding a solution is the key to successful restoration or recovery of the database.

- If the number of corrupted pages seems too large, and if the administrator feels that restoring the entire database
from the most recent backup is a viable option, only in that case should the option be full restoration.

## Script Explanation: Page-Level Corruption Setup, Detection & Repair

### 1. **Database Creation and Setup**

```sql
USE master;
GO

DROP DATABASE IF EXISTS [CorruptionTest];
GO

CREATE DATABASE [CorruptionTest];
GO

ALTER DATABASE [CorruptionTest] SET RECOVERY FULL;
GO

ALTER DATABASE [CorruptionTest] SET PAGE_VERIFY CHECKSUM;
GO
```

**Explanation:**

* Drops the database if it already exists to ensure a fresh start.
* Creates a new database called `CorruptionTest`.
* Sets the database recovery model to **FULL**, necessary for transaction log backups and point-in-time recovery.
* Sets `PAGE_VERIFY` to **CHECKSUM** to detect page corruption. This option computes a checksum for each page and validates it when the page is read, helping detect corruption early.

### 2. **Creating Tables with Large Columns**

```sql
CREATE TABLE [CorruptionTest].[dbo].[mssqltips_online]
(
    increment INT, 
    randomGUID UNIQUEIDENTIFIER, 
    randomValue INT, 
    BigCol CHAR(2000) DEFAULT 'a',
    INDEX CIX_MSSQLTips_increment1 UNIQUE CLUSTERED (increment)
);
GO

CREATE TABLE [CorruptionTest].[dbo].[mssqltips_corrupt]
(
    increment INT, 
    randomGUID UNIQUEIDENTIFIER, 
    randomValue INT, 
    BigCol CHAR(2000) DEFAULT 'a',
    INDEX CIX_MSSQLTips_increment1 UNIQUE CLUSTERED (increment)
);
GO
```

**Explanation:**

* Creates two tables with identical structure.
* Each has an integer column, a GUID column, an integer, and a big fixed-length column (`CHAR(2000)`).
* Each table has a clustered unique index on `increment` column.
* These tables will be used to insert data and later simulate corruption on one.

### 3. **Inserting Large Volume of Data**

```sql
SET NOCOUNT ON;
DECLARE @counter INT = 1;

BEGIN TRAN
   WHILE @counter <= 250000
   BEGIN
      INSERT INTO CorruptionTest.dbo.mssqltips_online (increment, randomGUID, randomValue) 
      VALUES (@counter, NEWID(), ABS(CHECKSUM(NewId())) % 140000000);

      INSERT INTO CorruptionTest.dbo.mssqltips_corrupt (increment, randomGUID, randomValue)
      VALUES (@counter, NEWID(), ABS(CHECKSUM(NewId())) % 140000000);

      SET @counter += 1;
   END;
COMMIT TRAN;
GO
```

**Explanation:**

* Inserts 250,000 rows into each table inside a single transaction.
* `randomGUID` is generated using `NEWID()`.
* `randomValue` is a random integer value.
* The large column `BigCol` is defaulted to `'a'` (since not explicitly inserted).
* This data will simulate real-world usage for corruption testing.

### 4. **Run DBCC CHECKDB to Validate Integrity**

```sql
DBCC CHECKDB('CorruptionTest') WITH NO_INFOMSGS;
GO
```

**Explanation:**

* Checks database integrity.
* Verifies data and index consistency.
* `NO_INFOMSGS` suppresses informational messages, showing only errors.
* Should report no corruption at this point.

### 5. **Full Backup with Compression**

```sql
BACKUP DATABASE [CorruptionTest] TO DISK = 'C:\SQL_BACKUPS\CorruptionTest_Full.BAK' WITH COMPRESSION;
GO
```

**Explanation:**

* Takes a full backup of the `CorruptionTest` database.
* Compresses the backup to save disk space.
* Good to have a clean backup before corrupting data.

### 6. **Simple Select Queries**

```sql
SELECT * FROM CorruptionTest.dbo.mssqltips;
SELECT * FROM CorruptionTest.dbo.mssqltips_online;
```

**Explanation:**

* Selects all data from two tables.
* Note: `mssqltips` table is not created in the script. Possibly a typo or earlier table.

### 7. **Get Physical Page Location for Corrupt Table Rows**

```sql
SELECT TOP 10
   sys.fn_PhysLocFormatter(%%physloc%%) AS PageId,
   *
FROM [CorruptionTest].[dbo].[mssqltips_corrupt];
GO
```

**Explanation:**

* Retrieves the **physical page location** of rows using the undocumented function `sys.fn_PhysLocFormatter`.
* Useful for identifying exactly which data pages hold the rows for later low-level inspection or corruption simulation.

### 8. **Enable Trace Flag 3604 and Dump Page Contents**

```sql
DBCC TRACEON (3604);
GO

DBCC PAGE ('CorruptionTest', 1, 354, 3);
GO
```

**Explanation:**

* `TRACEON 3604` sends DBCC output to the client instead of the error log.
* `DBCC PAGE` dumps the contents of **file 1**, **page 354**, **dump level 3** (includes header, data, and slot details).
* This allows inspecting the contents of the page before corruption.

### 9. **Convert Page Number for Corruption**

```sql
--66381639

SELECT CONVERT(VARBINARY(8), 95868367);
GO
----------------------------------------------
--Output: 0x05B6D5CF
```

**Explanation:**

* Converts the page number `95868367` into a binary format.
* This binary value is used in the `DBCC WRITEPAGE` command to overwrite part of a page.
* The `DBCC WRITEPAGE` requires a hex value to corrupt specific bytes on the page.

### 10. **Set Database to SINGLE\_USER Mode and Corrupt a Page**

```sql
USE master;
GO  
ALTER DATABASE [CorruptionTest] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
GO

DBCC WRITEPAGE ('CorruptionTest', 1, 354, 2151, 4, 0xCFD5B605, 1);
GO

ALTER DATABASE [CorruptionTest] SET MULTI_USER;
GO
```

**Explanation:**

* Sets the database to `SINGLE_USER` mode to allow exclusive access (needed to use `DBCC WRITEPAGE`).
* `DBCC WRITEPAGE` overwrites **file 1**, **page 354**, **byte offset 2151**, with 4 bytes (`0xCFD5B605`), corrupting the page data.
* This simulates **physical corruption** on the page.
* Restores the database to multi-user mode afterwards.

### 11. **Verify Corruption: Query and Inspect Page**

```sql
SELECT TOP 10
   sys.fn_PhysLocFormatter(%%physloc%%) AS PageId,
   *
FROM [CorruptionTest].[dbo].[mssqltips];
GO

DBCC PAGE ('CorruptionTest', 1, 354, 3);
GO
```

**Explanation:**

* Attempts to query the corrupted table (`mssqltips`).
* Dumps the corrupted page again to see the corruption effect.

### Summary and Context for Page-Level Restore

* This script **creates data**, **backs it up**, then **simulates corruption** on a data page.
* You use `DBCC PAGE` to examine physical page contents.
* `DBCC WRITEPAGE` allows you to **inject corruption at the byte level** on a page.
* After corruption, SQL Server will detect issues on reads or during `DBCC CHECKDB`.
* To recover corrupted pages, you can:

  * Use **Page Restore**: restore only the corrupted pages from a backup without restoring the whole database.
  * Use `DBCC CHECKDB` with repair options like `REPAIR_ALLOW_DATA_LOSS` (last resort).
  * Restore the full database backup or apply transaction log backups if point-in-time recovery is possible.

### How to Perform Page Restore (Conceptual Overview)

1. **Identify corrupted pages** using `DBCC CHECKDB` or errors during query.
2. Use the **backup and restore commands** to restore specific pages:

```sql
RESTORE DATABASE CorruptionTest PAGE = '1:354' 
FROM DISK = 'C:\SQL_BACKUPS\CorruptionTest_Full.BAK'
WITH NORECOVERY;
```

* `PAGE = 'file_id:page_id'` specifies the corrupted page.
* You can restore multiple pages as needed.
* After restoring pages, bring database online with:

```sql
RESTORE DATABASE CorruptionTest WITH RECOVERY;
```

### Final Notes:

* `DBCC WRITEPAGE` is an undocumented, dangerous command — only use in test/dev environments.
* Page-level restore is a powerful feature to fix corruption without restoring the entire database.
* Always have recent full and log backups for recovery scenarios.

## **SQL Server Maintenance Plan** outline that includes:

* **Full Database Backup**
* **Transaction Log Backup**
* **Index Rebuild**
* **Update Statistics**
* **Database Integrity Check**
* **Cleanup Old Backup Files (older than 7 days)**

## Step-by-step Consolidated Maintenance Plan Creation in SSMS

### 1. Create New Maintenance Plan

* In SSMS, expand **Management** → right-click **Maintenance Plans** → **New Maintenance Plan**.
* Name it `Consolidated_Maintenance_Plan`.

### 2. Add Tasks to the Design Surface

Drag and drop the following tasks from the Toolbox (left pane) into the plan design area:

* **Back Up Database Task** (for Full Backup)
* **Back Up Database Task** (for Transaction Log Backup)
* **Rebuild Index Task**
* **Update Statistics Task**
* **Check Database Integrity Task**
* **Maintenance Cleanup Task**

### 3. Configure Each Task

#### A. Full Database Backup

* Double-click **Back Up Database Task**.
* Set **Backup type** to **Full**.
* Select **All user databases** (or specific DBs).
* Set destination folder, e.g., `C:\SQL_BACKUPS\Full`.
* Enable **Backup Compression** (if supported).
* Click OK.

#### B. Transaction Log Backup

* Double-click the second **Back Up Database Task**.
* Set **Backup type** to **Transaction Log**.
* Select **All user databases** (or specific DBs).
* Set destination folder, e.g., `C:\SQL_BACKUPS\Log`.
* Enable **Backup Compression**.
* Click OK.

#### C. Rebuild Index Task

* Double-click **Rebuild Index Task**.
* Choose the databases and tables to rebuild.
* Check options like **Sort results in tempdb**.
* If you have Enterprise Edition, you can check **Keep index online**.
* Click OK.

#### D. Update Statistics Task

* Double-click **Update Statistics Task**.
* Select databases.
* Choose **Sampled** or **Full scan** (Full scan recommended for accuracy).
* Click OK.

#### E. Check Database Integrity Task

* Double-click **Check Database Integrity Task**.
* Choose databases to check.
* Click OK.

#### F. Maintenance Cleanup Task

* Double-click **Maintenance Cleanup Task**.
* Set **Delete files of the following type:** **Backup files**.
* Specify folder(s) where backups are saved, e.g., `C:\SQL_BACKUPS`.
* Set **Include all subfolders** if needed.
* Set **File extension(s):** `.bak,.trn` (to cover full and log backups).
* Set **File age:** 7 (deletes backups older than 7 days).
* Click OK.

### 4. Set Execution Order (Connect Tasks)

* Connect tasks with arrows to define execution flow, e.g.:

```
Full Backup
   ↓
Transaction Log Backup
   ↓
Rebuild Index
   ↓
Update Statistics
   ↓
Check Database Integrity
   ↓
Maintenance Cleanup (Delete old backups)
```

### 5. Schedule the Maintenance Plan

* Click the **Schedule** button (calendar icon) in the toolbar or right-click the plan → **Schedule...**
* Create a new schedule:

  * Frequency: Daily (or as needed)
  * Time: Off-peak hours (e.g., 2 AM)
* Click OK.

### 6. Save and Test

* Save the plan.
* Right-click the plan → **Execute** to test run.

# Summary of Maintenance Plan Features:

| Task                   | Purpose                                           |
| ---------------------- | ------------------------------------------------- |
| Full Backup            | Take full backup of all user databases            |
| Transaction Log Backup | Backup transaction logs for point-in-time restore |
| Rebuild Index          | Improve query performance by rebuilding indexes   |
| Update Statistics      | Help query optimizer by updating table stats      |
| Check DB Integrity     | Detect corruption with DBCC CHECKDB               |
| Cleanup Old Backups    | Delete backup files older than 7 days             |

# Additional Tips

* Make sure SQL Server Agent is running; it executes maintenance plans.
* Adjust backup paths and database selection as needed.
* Monitor job history for failures or warnings.
* Consider differential backups if full backups are large.
![CreateMaintenancePlanForDBBackup](https://github.com/sawanchouksey/documents/blob/main/docs/DevOps/CreateMaintenancePlanForDBBackup.png?raw=true)

## **`REPAIR_REBUILD`** option in `DBCC CHECKDB`.

### What is `REPAIR_REBUILD` in `DBCC CHECKDB`?

* `REPAIR_REBUILD` is an option used with the `DBCC CHECKDB` command to **fix minor, non-destructive errors** in the database.
* It performs **online, no-data-loss repairs**, such as:

  * Rebuilding **missing or corrupted nonclustered indexes**
  * Fixing metadata inconsistencies that don’t require data removal
* It **does NOT** fix severe corruption or issues that require deleting data.

### When to Use `REPAIR_REBUILD`

* When you want to fix **minor corruption** found by `DBCC CHECKDB`.
* When you want to avoid any risk of data loss.
* Useful if the problem is limited to things like index corruption.

### Syntax

```sql
DBCC CHECKDB ('DatabaseName', REPAIR_REBUILD);
```

### Important Notes

* **Must run in SINGLE\_USER mode** when using repair options.
* It’s recommended to run this only **after full backups** are taken.
* If `REPAIR_REBUILD` cannot fix the issue, more aggressive options or restore from backup might be needed.
* For serious corruption, `REPAIR_ALLOW_DATA_LOSS` exists but **can delete data** — use with extreme caution.

### Example Usage

```sql
USE master;
GO
ALTER DATABASE YourDatabase SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
GO

DBCC CHECKDB ('YourDatabase', REPAIR_REBUILD);
GO

ALTER DATABASE YourDatabase SET MULTI_USER;
GO
```

### Summary

| Option                   | Repair Type                              | Risk of Data Loss |
| ------------------------ | ---------------------------------------- | ----------------- |
| `REPAIR_REBUILD`         | Fixes minor errors (e.g., index rebuild) | No                |
| `REPAIR_ALLOW_DATA_LOSS` | Fixes major errors, may delete data      | Yes               |

## 🔁 How to Switch SQL Server Authentication Mode via SSMS Server Properties

### ✅ Prerequisites:

* SQL Server Management Studio (SSMS) installed
* Windows account with administrative access to SQL Server
* Access to SQL Server Configuration Manager (to restart the service)

## 🔧 Step-by-Step Guide

### 🔹 **Step 1: Open SSMS and Connect to SQL Server**

1. Open **SQL Server Management Studio (SSMS)**.
2. In the **Connect to Server** dialog:

   * **Server Type**: Database Engine
   * **Server Name**: (e.g., `localhost\SQLEXPRESS`)
   * **Authentication**: Windows Authentication
3. Click **Connect**.

### 🔹 **Step 2: Open Server Properties**

1. In **Object Explorer**, **right-click** the connected server name (top of the tree).

2. Select **Properties**.

### 🔹 **Step 3: Change Authentication Mode**

1. In the **Server Properties** dialog, click on the **Security** page from the left menu.

2. Under **Server authentication**, choose one of the following:

   * **Windows Authentication mode** *(default)*
     → Only Windows users can log in.

   * ✅ **SQL Server and Windows Authentication mode** *(Mixed Mode)*
     → Enables both Windows accounts and SQL Server logins like `sa`

3. After selecting **SQL Server and Windows Authentication mode**, click **OK**.

### 🔹 **Step 4: Restart SQL Server for Changes to Take Effect**

You must restart the SQL Server instance to apply the new authentication setting.

#### ✔ Option A: Use SSMS

1. In **Object Explorer**, right-click the server name.
2. Click **Restart**.

   OR

#### ✔ Option B: Use SQL Server Configuration Manager

1. Open **SQL Server Configuration Manager**.
2. Click on **SQL Server Services**.
3. Right-click your SQL Server instance (e.g., `SQL Server (MSSQLSERVER)`).
4. Choose **Restart**.

### 🔹 **Step 5: Enable and Set Password for `sa` Login (Optional but Recommended for SQL Auth)**

1. In SSMS, expand:

   ```
   Security → Logins
   ```
2. Right-click on `sa` → **Properties**.
3. Under the **General** tab:

   * Set a **strong password**.
4. Under the **Status** tab:

   * Set **Login: Enabled**
   * Click **OK**.

### 🔹 **Step 6: Test SQL Server Authentication**

1. In SSMS, go to **File > Connect Object Explorer**.
2. In the **Connect to Server** dialog:

   * **Authentication**: SQL Server Authentication
   * **Login**: `sa`
   * **Password**: \[your password]
3. Click **Connect**.

If successful, the authentication mode switch was successful!

### ✅ Summary Table

| Step | Action                                                 |
| ---- | ------------------------------------------------------ |
| 1    | Connect using Windows Authentication                   |
| 2    | Open Server Properties                                 |
| 3    | Change to "SQL Server and Windows Authentication mode" |
| 4    | Restart SQL Server instance                            |
| 5    | Enable and set password for `sa` login                 |
| 6    | Test using SQL Authentication                          |


## Switching the **authentication mode** in **SQL Server** between **Windows Authentication** and **Mixed Mode (SQL Server + Windows Authentication)** involves a few steps in **SQL Server Management Studio (SSMS)**.

### 🔄 Goal: Change SQL Server Authentication Mode

* **Windows Authentication**: Only allows Windows user accounts.
* **Mixed Mode Authentication**: Allows both Windows accounts **and** SQL Server logins (like `sa`).

### ✅ Prerequisites

* You must be logged into SQL Server as a **Windows Administrator**.
* You should have **SSMS (SQL Server Management Studio)** installed.

### 🛠️ Steps to Change Authentication Mode in SSMS

### 🔹 Step 1: Open SSMS and Connect

1. Launch **SQL Server Management Studio (SSMS)**.
2. In the **Connect to Server** window:

   * **Server type**: Database Engine
   * **Server name**: \[your server name]
   * **Authentication**: Windows Authentication
   * Click **Connect**

✅ You're now connected to SQL Server.

### 🔹 Step 2: Check Current Authentication Mode

1. In **Object Explorer**, right-click the **server name** at the top.
2. Select **Properties**.

3. In the left pane, select **Security**.
4. Under **Server authentication**, check the selected option:

   * **Windows Authentication mode**
   * **SQL Server and Windows Authentication mode**

### 🔹 Step 3: Change to Mixed Mode (if needed)

1. Select **SQL Server and Windows Authentication mode**.
2. Click **OK**.

> Note: This change does **not** take effect immediately. You must restart the SQL Server service.

### 🔹 Step 4: Restart SQL Server Service

1. In SSMS, open **Object Explorer**.
2. Click the **New Query** button and run:

```sql
SHUTDOWN WITH NOWAIT;
```

> 🔥 This immediately shuts down SQL Server — use carefully. Alternatively:

#### 🧠 Recommended Way (via SQL Server Configuration Manager):

1. Open **SQL Server Configuration Manager**.
2. Go to **SQL Server Services**.
3. Right-click your SQL Server instance.
4. Click **Restart**.

### 🔹 Step 5: Enable `sa` Login (Optional, for SQL Auth)

1. In **SSMS**, expand:

   ```
   Security → Logins
   ```
2. Right-click `sa` → **Properties**.
3. In **General** tab:

   * Set a strong password.
4. In **Status** tab:

   * **Login**: Enabled
   * Click **OK**.

✅ Now, you can log in using `sa` and the password.

### 🔹 Step 6: Test SQL Server Authentication

1. Disconnect your current connection (top-left menu → Disconnect).
2. Click **Connect** → Database Engine
3. Choose:

   * **Authentication**: SQL Server Authentication
   * Login: `sa`
   * Password: \[your password]
4. Click **Connect**

✅ If successful, SQL Authentication is now working.

### 📝 Summary

| Step | Description                                       |
| ---- | ------------------------------------------------- |
| 1    | Open SSMS and connect using Windows Auth          |
| 2    | Check authentication mode under Server Properties |
| 3    | Switch to Mixed Mode (if needed)                  |
| 4    | Restart SQL Server to apply changes               |
| 5    | Enable and configure `sa` login (optional)        |
| 6    | Test SQL Authentication                           |


## 🔐 SQL Server Security Components (Principals Part-1: Server Logins and Server Roles)

SQL Server uses **three key security components** to manage **who** can access it and **what** they can do:

### 🔧 1. SQL Server Security Components Overview

| Component       | Description                                                                                                         |
| --------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Principals**  | These are **users or groups** that request access to SQL Server resources. Examples: logins, database users, roles. |
| **Securables**  | These are **objects that need protection** — like servers, databases, schemas, tables, etc.                         |
| **Permissions** | Define **what actions** a principal can perform on a securable — such as `SELECT`, `INSERT`, `ALTER`, etc.          |

> ✅ **To allow access**, you must grant the correct **permissions** to each **principal** on specific **securables**.

#### 🔸 Example:

If a user named `sqluser01` needs to **query tables** inside the `Sales` schema:

* Grant them `SELECT` permission on the **Sales schema**.
* That will allow them to query **all tables and views** in that schema.

### 👤 2. Principals: Server Logins

A **Login** is a type of **principal** that allows a user to **connect to SQL Server**. Logins exist at the **server level** and must be created in the **master database**.

#### ✅ Types of Server Logins:

1. **Windows Logins**
2. **SQL Server Logins**
3. **Certificate-Mapped Logins**
4. **Asymmetric Key-Mapped Logins**

#### 🔹 A. Windows Logins

* Tied to a **Windows account or group** (either local or domain).
* Format:

  ```
  [DomainName\Username] or [ComputerName\Username]
  ```

##### 🔧 Syntax:

```sql
USE master;
CREATE LOGIN [win10b\winuser01] FROM WINDOWS 
WITH DEFAULT_DATABASE = master, DEFAULT_LANGUAGE = us_english;
```

> * `FROM WINDOWS`: Specifies it's a Windows login
> * `DEFAULT_DATABASE`: The database SQL Server connects to by default
> * `DEFAULT_LANGUAGE`: Preferred language (e.g., `us_english`)

#### 🔹 B. Windows Group Logins

* Create a login for a **Windows group**, which allows all group members to connect with the same permissions.

```sql
CREATE LOGIN [win10b\wingroup01] FROM WINDOWS 
WITH DEFAULT_DATABASE = master, DEFAULT_LANGUAGE = us_english;
```

> ✅ Easier to manage many users by assigning permissions at the group level.

#### 🔹 C. SQL Server Logins (Non-Windows)

* SQL-based logins are **independent of Windows**.
* You must set a **password** and optionally configure password policies.

```sql
CREATE LOGIN sqluser01 
WITH PASSWORD = 'tempPW@56789' MUST_CHANGE,
CHECK_EXPIRATION = ON,
DEFAULT_DATABASE = master,
DEFAULT_LANGUAGE = us_english;
```

> ⚠️ `MUST_CHANGE`: Forces user to change password at first login
> 🔐 `CHECK_EXPIRATION`: Enforces password expiration policy

#### 🛡️ Granting Permissions to Logins

Once a login is created, you can **grant permissions** using the `GRANT` statement:

```sql
GRANT IMPERSONATE ANY LOGIN TO [win10b\winuser01], sqluser01;
```

This permission allows the login to impersonate other logins.

#### 🔍 View Server Logins and Their Permissions

Use system views to inspect permissions:

```sql
SELECT 
    pr.principal_id,
    pr.name,
    pe.state_desc,
    pe.permission_name
FROM sys.server_principals pr
INNER JOIN sys.server_permissions pe
    ON pr.principal_id = pe.grantee_principal_id
WHERE pr.principal_id = SUSER_ID('win10b\winuser01') 
   OR pr.principal_id = SUSER_ID('sqluser01');
```

### 👥 3. Server Roles

SQL Server offers **server-level roles** to simplify permission management:

#### 🔹 What are Server Roles?

* **Security principals** that group other logins.
* Permissions apply at the **server level**, not the database level.
* Assigning logins to server roles grants them predefined **capabilities**.

#### 🔸 Types of Server Roles:

| Type                          | Description                                                                                                        |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **Fixed Server Roles**        | Built-in roles with predefined permissions (e.g., `sysadmin`, `securityadmin`). Permissions **cannot be changed**. |
| **User-Defined Server Roles** | Custom server roles you create, where **permissions can be modified** and customized.                              |

#### 🔹 Examples of Fixed Server Roles

| Role Name       | Description                                    |
| --------------- | ---------------------------------------------- |
| `sysadmin`      | Full control of the entire SQL Server instance |
| `securityadmin` | Manage logins and their permissions            |
| `serveradmin`   | Configure server-wide settings                 |
| `setupadmin`    | Manage linked servers and replication          |
| `processadmin`  | Kill processes                                 |
| `dbcreator`     | Create, alter, drop databases                  |
| `bulkadmin`     | Run bulk insert operations                     |

#### 🔧 Add a Login to a Server Role:

```sql
ALTER SERVER ROLE sysadmin ADD MEMBER sqluser01;
```

> This gives `sqluser01` full administrative privileges on the server.

#### 🔧 Add a Login to a user defined Server Role:

```sql
CREATE SERVER ROLE devops;
GRANT ALTER ANY DATABASE TO devops; 
ALTER SERVER ROLE devops ADD MEMBER [win10b\winuser01];
```

### 📌 Summary

| Component       | Description                                                           |
| --------------- | --------------------------------------------------------------------- |
| **Principal**   | A user, login, or role that can request access                        |
| **Login**       | A server-level principal (can be Windows or SQL-based)                |
| **Securable**   | An object that access can be controlled for (e.g., databases, tables) |
| **Permission**  | Defines what a principal can do (e.g., SELECT, EXECUTE)               |
| **Server Role** | A grouping of permissions at the server level (fixed or user-defined) |

## `Database Users, Database Roles`

### `Database Users`
- After you’ve set up your server-level logins, you can create database users that map back to those logins, whether 
they’re Windows or SQL Server logins.

- can also create database users that do not map to logins.

- These types of logins are generally used for contained databases, impersonation, or development and testing.

- SQL Server provides the CREATE USER statement for creating database users. You must run this statement within 
the context of the database in which the user is being defined.

```sql
USE Adventureworks;
CREATE USER [win10b\winuser01];
GRANT ALTER ON SCHEMA::Sales TO [win10b\winuser01]; 
```

- The winuser01 user is based on the win10b\winuser01 login.

- When you create a database user that has the same name as a login, you do not need to specify the login.

- If you want to create a user with a different name, you must include the FOR LOGIN or FROM LOGIN clause.

```sql
CREATE USER winuser03 FOR LOGIN [win10b\winuser01];
GRANT ALTER ON SCHEMA::Sales TO winuser03; 
```

- You can create only one user in a database per login.

- If you want to try out both these statements, you’ll need to drop the first user before creating the second.

- The two preceding examples also include a GRANT statement that assigns the ALTER permission to the user on the 
Sales schema. As a result, the user will be able to alter any object within that schema.

- When you grant a permission on a specific object, you must specify the type of object and its name, separated by 
the scope qualifier (double colons).

- In some GRANT statements, the securable is implied, so it does not need to be specified.

- Creating a database user that’s associated with a SQL Server login is just as simple as creating a user based on a 
Windows login, especially when you use the same name

```sql
CREATE USER sqluser01;
```

- The CREATE USER statement creates the sqluser01 user, but this time, the example grants no permissions.

- the user receives only the CONNECT permission, which you can verify by running the following SELECT statement:

```sql
SELECT pe.state_desc, pe.permission_name FROM sys.database_principals pr INNER JOIN sys.database_permissions pe
ON pr.principal_id = pe.grantee_principal_id WHERE pr.principal_id = USER_ID('sqluser01');
```

## `User defined Database Roles`
- To set up a user-defined database role, you must create the role, grant permissions to the role, and add members to 
the role (or add members and then grant permissions).

```sql
CREATE ROLE dbdev;
GRANT SELECT ON DATABASE::WideWorldImporters TO dbdev;
ALTER ROLE dbdev ADD MEMBER [win10b\winuser01];
ALTER ROLE dbdev ADD MEMBER sqluser01;
```

## Fixed Database Roles 
- ![Fixed database Roles](https://github.com/sawanchouksey/documents/blob/main/docs/DevOps/FixedDataBaseRoles.png?raw=true)

## Database Level Roles and Permissions
- ![Database Level Roles and Permissions](https://github.com/sawanchouksey/documents/blob/main/docs/DevOps/dbrolesPermission.png?raw=true)

## **step-by-step explanation** on how to **create a user and assign a role to that user** in **SQL Server Management Studio (SSMS)** for a specific database.

### ✅ Prerequisites:

- You must be logged in with an account that has permission to create logins and users (e.g., `sa` or another admin).
- SSMS is installed and connected to your SQL Server instance.

### 🎯 GOAL:

1. **Create a login** at the server level (if needed).
2. **Create a database user** for that login.
3. **Assign a role** to that user in the database.

### 🔹 Step 1: Create a Login (Server-Level)

#### 📍Purpose:

A **login** allows access to the SQL Server **instance**.

#### 🧭 Steps:

1. Open **SSMS** and connect to your SQL Server instance.
2. In **Object Explorer**, expand the server node.
3. Right-click on **Security > Logins** → click **New Login…**
4. In the **Login – New** dialog:
- **General Page**:
  - **Login name**: Type a name (e.g., `myuser`).
  - Select **SQL Server authentication** (if not using Windows).
  - Set a **password** and uncheck “Enforce password policy” if needed.
  - **Default database**: Choose your target database (e.g., `MyDatabase`).
5. Click **OK**.

### 🔹 Step 2: Create a Database User (Database-Level)

#### 📍Purpose:

A **database user** maps to the login within a specific **database**.

#### 🧭 Steps:

1. In **Object Explorer**, expand **Databases > YourDatabase > Security > Users**.
2. Right-click **Users** → Click **New User…**
3. In the **Database User – New** dialog:
   - **User name**: e.g., `myuser`
   - **Login name**: Click the ellipsis `[...]` → select the login you created.
   - **Default schema**: Optional (you can enter `dbo`).
4. Click **OK**.

### 🔹 Step 3: Add the User to a Role

#### 📍Purpose:

**Roles** define the permissions that a user has in the database.

#### 🧭 Steps:

1. In **Object Explorer**, expand **Databases > YourDatabase > Security > Roles > Database Roles**.
2. Right-click on the role you want (e.g., `db_datareader`, `db_datawriter`, `db_owner`) → Click **Properties**.
3. In the **Role Properties** dialog:

   - Go to **Members** page.
   - Click **Add** → Select the user (`myuser`) → Click **OK**.
4. Click **OK** to close Role Properties.

### 🔐 Common Database Roles:

| Role Name      | Description                             |
| -------------- | --------------------------------------- |
| db\_datareader | Can read all data in the database       |
| db\_datawriter | Can write to all tables in the database |
| db\_owner      | Full control of the database            |
| db\_ddladmin   | Can create/modify schema objects        |

### 🧪 Optional: Test Access

You can test login using `myuser`:

1. Disconnect from current connection in SSMS.
2. Reconnect using:

   - **Authentication**: SQL Server Authentication
   - **Login**: `myuser`
   - **Password**: your password

Try running a query like `SELECT * FROM YourTable;` to confirm access.

## SQL Server **`GRANT`**, **`REVOKE`**, and **`DENY`** permission statements, using your provided examples as references. This will help you understand **how permissions are applied**, **checked**, and **removed** on a **schema** and its objects (like tables).

### 🔑 Key Permission Commands in SQL Server

| Command  | Meaning                                                                               |
| -------- | ------------------------------------------------------------------------------------- |
| `GRANT`  | Gives permission to perform an action (e.g., SELECT, INSERT, CONTROL).                |
| `REVOKE` | Removes a previously granted or denied permission. Does **not** deny — just removes.  |
| `DENY`   | Explicitly prevents the action, even if it was granted through a role or other means. |

### 🔍 Understanding the Examples (Step-by-Step)

### 🧪 **Example 1: CONTROL on Schema**

```sql
GRANT CONTROL ON SCHEMA::Sales TO sqluser01;

EXECUTE AS USER = 'sqluser01';
SELECT * FROM fn_my_permissions ('Sales', 'SCHEMA');
REVERT;
GO

REVOKE CONTROL ON SCHEMA::Sales TO sqluser01;
DENY EXECUTE ON SCHEMA::Sales TO sqluser01;
```

#### 📝 Explanation:

* `GRANT CONTROL`: Gives **full control** over the `Sales` schema to `sqluser01`. This includes permission to read, write, modify, and manage objects within the schema.
* `EXECUTE AS USER`: Simulates actions as if you're logged in as `sqluser01`.
* `fn_my_permissions`: Returns the permissions that `sqluser01` has on the `Sales` schema.
* `REVERT`: Returns you to your original context.
* `REVOKE CONTROL`: Removes the CONTROL permission.
* `DENY EXECUTE`: Explicitly **blocks the ability to execute** stored procedures or functions within the `Sales` schema — even if a role grants it.

### 🧪 **Example 2: CONTROL and SELECT on a Table in the Schema**

```sql
GRANT CONTROL ON SCHEMA::Sales TO sqluser01;

EXECUTE AS USER = 'sqluser01';
-- SELECT * FROM fn_my_permissions ('Sales', 'SCHEMA');

SELECT * FROM [Sales].[CreditCard];
REVERT;
GO

REVOKE UPDATE ON SCHEMA::Sales TO sqluser01;
DENY EXECUTE ON SCHEMA::Sales TO sqluser01;
```

#### 📝 Explanation:

* `GRANT CONTROL`: Again gives full control over `Sales` schema, so user can SELECT, INSERT, DELETE, UPDATE, etc.
* Inside `EXECUTE AS`, the user tries to access the table `Sales.CreditCard`.
* `REVOKE UPDATE`: Removes ability to update data (if it was previously granted). But this only removes the grant — it doesn’t deny.
* `DENY EXECUTE`: Prevents executing stored procedures/functions inside `Sales` schema.

🧠 **Note**: Since CONTROL includes UPDATE permission, unless it's **DENIED**, it would still be allowed. So using only REVOKE may not be enough to block UPDATE — use DENY if you want to *prevent* it.

### 🧪 **Example 3: SELECT Only, then Deny SELECT**

```sql
GRANT SELECT ON SCHEMA::Sales TO sqluser01;

EXECUTE AS USER = 'sqluser01';
SELECT * FROM fn_my_permissions ('Sales', 'SCHEMA');
REVERT;
GO

REVOKE UPDATE ON SCHEMA::Sales TO sqluser01;
DENY SELECT ON SCHEMA::Sales TO sqluser01;
```

#### 📝 Explanation:

* `GRANT SELECT`: Allows the user to **read** data from any object in `Sales` schema.
* `fn_my_permissions`: Lists SELECT among the allowed permissions.
* `REVOKE UPDATE`: Has no effect unless UPDATE was previously granted.
* `DENY SELECT`: Explicitly blocks SELECT, overriding any GRANTs the user might have via roles or CONTROL.

📌 **Important**:

* `DENY` always wins over `GRANT`.
* `REVOKE` only **removes** permission — it doesn’t block it if inherited through roles.

### 🎓 Summary of Concepts

| Action                                            | Effect                                                             |
| ------------------------------------------------- | ------------------------------------------------------------------ |
| `GRANT <permission> ON <schema/object> TO <user>` | Enables user to perform the specified action.                      |
| `REVOKE <permission>`                             | Removes previously granted (or denied) permission.                 |
| `DENY <permission>`                               | Explicitly blocks the action, even if other roles grant it.        |
| `CONTROL`                                         | Full control over a schema (implies all object-level permissions). |

## 🔐 Best Practices

* Use `GRANT` to assign the minimum required permissions.
* Use `REVOKE` to clean up old permissions.
* Use `DENY` carefully — especially when dealing with roles, as it overrides grants from any other source.

## `SQL Server Agent`

### Why we `need` SQL Server Agent?
- In this era of automation, it is often required that we execute multiple scripts repeatedly in a timely fashion

- These scripts can be used to back up an existing database, delete extra log files, process data from a table, drop and
rebuild indexes on a table, or running an ETL job etc

- All these tasks are repetitive and can be automated using the SQL Server Agent

- This gives us the flexibility that the job will be executed as per the rules defined in the schedule and there is minimal
human intervention required in order to execute these jobs

- Once the jobs are executed, you can view the history if the execution was successful or failed

- In case of a failure, there is an option to restart the job manually.

- SQL Server Agent can run a job on a schedule, in response to a specific event, or on demand.

- By default, the SQL Server Agent service is disabled when SQL Server is installed unless the user explicitly chooses
to autostart the service.

### SQL Server Agent `Components`
- **Jobs** : A job is a specified series of actions that SQL Server Agent performs.

- **Schedules** : A schedule specifies when a job runs.

- **Alerts**: An alert is an automatic response to a specific event.

- **Operators** : An operator defines contact information for an individual responsible for the maintenance of one or more
instances of SQL Server.

### `Security` for SQL Server Agent Administration
- SQL Server Agent uses the **SQLAgentUserRole** **SQLAgentReaderRole** , and **SQLAgentOperatorRole** fixed
database roles in the msdb database to control access to SQL Server Agent for users who aren't members of
the **sysadmin** fixed server role

- In addition to these fixed database roles, subsystems and proxies help database administrators ensure that each job
step runs with the minimum permissions required to perform its task

- **Roles** : Members of the SQLAgentUserRole SQLAgentReaderRole , and SQLAgentOperatorRole fixed database
roles in msdb , and members of the sysadmin fixed server role have access to SQL Server Agent

- **Subsystems** : A subsystem is a predefined object that represents functionality that is available to a job step

- **Proxies** : SQL Server Agent uses proxies to manage security contexts. A proxy can be used in more than one job
step. Members of the sysadmin fixed server role can create proxies.

### SQL Server Agent `Jobs and Schedules`

#### SQL Server Agent Jobs
- A job is a specified series of actions that SQL Server Agent performs

- Use jobs to define an administrative task that can be run one or more times and monitored for success or failure

- A job can run on one local server or on multiple remote servers

- You can run jobs in several ways:
   - According to one or more schedules.
   - In response to one or more alerts.
   - By executing the **sp_start_job stored procedure**.

- Each action in a job is a job step.

- For example, a job step might consist of running a Transact SQL statement, executing an SSIS package, or issuing a
command to an Analysis Services server.

- Job steps are managed as part of a job.

- Each job step runs in a specific security context

- For job steps that use **Transact SQL**, use the **EXECUTE AS** statement to set the security context for the job step

- For other types of job steps, use a proxy account to set the security context for the job step.

#### Schedules
- A schedule specifies when a job runs

- A schedule specifies when a job runs

- more than one schedule can apply to the same job

- A schedule can define the following conditions for the time when a job runs:
   - Whenever SQL Server Agent starts.
   - Whenever CPU utilization of the computer is at a level you've defined as idle.
   - One time, at a specific date and time.
   - On a recurring schedule.

### SSIS Package with SQL Server Agent

**SSIS (SQL Server Integration Services)** is a powerful data integration and workflow platform that comes with Microsoft SQL Server. It is primarily used for data extraction, transformation, and loading (ETL), data migration, and workflow automation.

#### 🔷 What is an SSIS Package?

An **SSIS package** is a collection of control flow elements, data flow elements, variables, event handlers, and configurations that define a workflow. It can:

* Extract data from various sources
* Transform the data (clean, merge, convert)
* Load the data into destination systems (like databases, files, cloud)

Think of an SSIS package as a *script* or *task* that moves and transforms data between systems in an automated way.

#### 🔷 Why SSIS is Needed? Purpose:

| **Need**            | **Purpose**                                             |
| ------------------- | ------------------------------------------------------- |
| Data migration      | Move data from legacy systems to SQL Server             |
| Data transformation | Clean, aggregate, filter, and reshape data              |
| Data warehousing    | Load data into data warehouses                          |
| Automation          | Run scheduled ETL processes without manual intervention |
| Integration         | Connect to flat files, Excel, Oracle, APIs, etc.        |

#### 🔷 How to Install SSIS:

##### ✅ 1. **Install SQL Server Data Tools (SSDT)**

* Required to create and develop SSIS packages.
* SSDT is a Visual Studio extension.
* Download from: [https://learn.microsoft.com/en-us/sql/ssdt/download-sql-server-data-tools](https://learn.microsoft.com/en-us/sql/ssdt/download-sql-server-data-tools)

##### ✅ 2. **Enable Integration Services in SQL Server Installation**

* During SQL Server setup:

  * Choose `Integration Services` under `Features`.
  * This installs the SSIS runtime engine required to run packages.

##### ✅ 3. **Install SSIS Extension in Visual Studio**

* In Visual Studio:

  * Go to `Extensions` → `Manage Extensions` → Search for **SSIS**
  * Install **SQL Server Integration Services Projects**

#### 🔷 Create and Deploy an SSIS Package (Overview):

##### Step-by-step (Basic):

1. **Open Visual Studio** → Create new SSIS Project
2. In `Control Flow` tab, drag a `Data Flow Task`
3. Inside `Data Flow`, add:

   * Source (e.g., OLE DB Source, Flat File Source)
   * Transformations (optional)
   * Destination (e.g., SQL Server Destination)
4. Configure connections (Connection Managers)
5. Debug & Test the package
6. Deploy using:

   * **Project Deployment Model** (SSISDB)
   * **File System Deployment**

### 🔷 Use Case Example: Automate SSIS Package with SQL Server Agent

### Scenario:

### 🔷 SQL Server Agent: Run SSIS Package Automatically

##### 🛠 Step-by-Step Guide:

##### ✅ Step 1: Ensure SQL Server Agent is Running

* In SSMS → Object Explorer → SQL Server Agent → Start it (if not running)

##### ✅ Step 2: Deploy the SSIS Package

* Deploy package to:

  * **SSISDB (Integration Services Catalog)** – recommended
  * OR the **File System**

##### ✅ Step 3: Create a SQL Server Agent Job

1. In SSMS → Expand `SQL Server Agent` → Right-click **Jobs** → `New Job`

2. **General Tab**:

   * Name: `Load Sales Data`
   * Description: `ETL job to load sales from flat file`

3. **Steps Tab**:

   * Click `New...`
   * Step Name: `Run SSIS Package`
   * Type: `SQL Server Integration Services Package`
   * Run As: `SQL Server Agent Service Account` or proxy
   * Package Source: `SSIS Catalog` or `File System`
   * Browse and select the deployed package

4. **Set Execution Options**:

   * Optionally set logging, fail conditions, retry attempts

5. **Schedules Tab**:

   * Add a new schedule
   * Frequency: Daily, Time: e.g., 2:00 AM

6. Save the job

##### ✅ Common Use Cases of SSIS:

| **Use Case**           | **Description**                                                |
| ---------------------- | -------------------------------------------------------------- |
| ETL for Data Warehouse | Extract from OLTP, transform, and load into dimensional models |
| Data Migration         | Move data between systems (e.g., Oracle → SQL Server)          |
| Daily Reporting Loads  | Automate refresh of reports                                    |
| File Processing        | Load data from Excel, CSV, or XML into DB                      |
| Data Cleansing         | Validate and clean inconsistent data                           |

## SQL Server Agent `Alerts`, `Operators` , `Database Mail` and `Activity Monitor`

### SQL Server Agent Alerts
- An alert is an automatic response to a specific event

- For example, an event can be a job that starts or system resources that reach a specific threshold

- You define the conditions under which an alert occurs

- An alert can respond to one of the following conditions:
   - SQL Server events
   - SQL Server performance conditions
   - Microsoft Windows Management Instrumentation (WMI) events on the computer where SQL Server Agent is
   running

- An alert can perform the following actions:
   - Notify one or more operators
   - Run a job

- Events are generated by SQL Server and entered into the Microsoft Windows application log.

- SQL Server Agent reads the application log and compares events written there to alerts that you have defined.

- When SQL Server Agent finds a match, it fires an alert, which is an automated response to an event.

- In addition to monitoring SQL Server events, SQL Server Agent can also monitor performance conditions and
Windows Management Instrumentation (WMI) events

- To define an alert, you specify:
   - The name of the alert.
   - The event or performance condition that triggers the alert.
   - The action that SQL Server Agent takes in response to the event or performance condition.

### SQL Server Agent Operators
- An operator defines contact information for an individual responsible for the maintenance of one or more instances of
SQL Server

- In some enterprises, operator responsibilities are assigned to one individual

- In enterprises with multiple servers, many individuals can share operator responsibilities

- An operator doesn't contain security information, and doesn't define a security principal.
   - SQL Server can notify operators of alerts through...
   - E mail
   - Pager (through e mail)
   - net send

- To send notifications to operators by using e mail or pagers, you must configure SQL Server Agent to use Database
Mail

- The primary attributes of an operator are:
   - Operator name
   - Contact information

### Database Mail
- Database Mail is an enterprise solution for sending e mail messages from the SQL Server Database Engine.

- Using Database Mail, your database applications can send e mail messages to users. The messages can contain
query results, and can also include files from any resource on your network

- Benefits of using Database Mail
   - Reliability
   - Scalability
   - Security
   - Supportability

#### Database Mail Architecture

- ![DBMailArchitecture](https://github.com/sawanchouksey/documents/blob/main/docs/DevOps/DBMailArchitecture.png?raw=true)

#### Database Mail Components
- **Configuration and security** components
   - Database Mail stores configuration and security information in the *msdb* database. Configuration and security objects create profiles and accounts used by Database Mail.

- **Messaging** components
   - The msdb database acts as the mail host database that holds the messaging objects that Database Mail uses to send e mail.
   - These objects include the *sp_send_dbmail* stored procedure and the data structures that hold information about messages.

- **Database Mail executable**
   - The Database Mail executable is an external program that reads from a queue in the msdb database and sends messages to email servers.

- **Logging and auditing** components
   - Database Mail records logging information in the *msdb* database and the Microsoft Windows application event log.

#### Configuring Agent to use Database Mail
- SQL Server Agent can be configured to use Database Mail

- This is required for alert notifications and automatic notification when a job completes

- Individual job steps within a job can also send e mail without configuring SQL Server Agent to use Database Mail.
   - For example, a Transact SQL job step can use Database Mail to send the results of a query to a list of recipients

- You can configure SQL Server Agent to send e mail messages to predefined operators when:
   - An alert is triggered. Alerts can be configured to send e mail notification of specific events that occur. For
   example, alerts can be configured to notify an operator of a particular database event or operating system
   condition that may need immediate action. For more information about configuring alerts.
   - A scheduled task, such as a database backup or replication event, succeeds or fails. For example, you can use
   SQL Server Agent Mail to notify operators if an error occurs during processing at the end of a month.

### SQL Server Agent `Job Activity Monitor`
- The Job Activity Monitor allows you to view the *sysjobactivity* table by using SQL Server Management Studio

- You can view all jobs on the server, or you can define filters to limit the number of jobs displayed. You can also sort
the job information by clicking on a column heading in the Agent *Job Activity grid*.

- For example, when you select the *Last Run* column heading, you can view the jobs in the order that they were last
run. Clicking the column heading again toggles the jobs in ascending and descending order based on their last run
date.

- Using the Job Activity Monitor you can perform the following tasks:
   - Start and stop jobs.
   - View job properties.
   - View the history for a specific job.

- Refresh the information in the *Agent Job Activity* grid manually or set an automatic refresh interval by clicking *View
refresh settings*

- Use the Job Activity Monitor when you want to find out what jobs are scheduled to run, the last outcome of jobs that
have run during the current session, and to find out which jobs are currently running or idle.

- If the SQL Server Agent service fails unexpectedly, you can determine which jobs were in the middle of being executed by looking at the previous session in the Job Activity Monitor.

- You can also view job activity for the current session by using the *stored procedure sp_help_jobactivity*

## 🔍 What is **Service Broker** in SQL Server (`msdb`)?

**Service Broker** is a **message-based communication platform** in SQL Server. It allows database applications to communicate **asynchronously**, reliably, and in a **transactional** manner within a SQL Server instance or between instances.

### 📦 Purpose of **Service Broker** in `msdb`

In the **`msdb`** database specifically, **Service Broker** is often used internally by SQL Server for tasks like:

* Database Mail
* SQL Agent notifications
* Event notifications
* Query notifications
* System alerts

You typically don't manage Service Broker in `msdb` directly unless you're troubleshooting or developing solutions that rely on these features.

### ✅ How to Check if Service Broker is Enabled

Use this query to check if **Service Broker** is enabled for a database:

```sql
SELECT name, is_broker_enabled 
FROM sys.databases 
WHERE name = 'msdb';
```

* `is_broker_enabled = 1` → Enabled
* `is_broker_enabled = 0` → Disabled

### 🚀 How to Enable Service Broker (if needed)

⚠️ **Note**: For system databases like `msdb`, be cautious when enabling/disabling Service Broker. You generally **should not** need to do this manually unless directed by Microsoft support or you're troubleshooting a specific issue.

- Still, here's the general syntax:

```sql
ALTER DATABASE msdb SET ENABLE_BROKER;
```

- But this can hang if there are open connections to the database.

To **force it**, use:

```sql
ALTER DATABASE msdb SET NEW_BROKER WITH ROLLBACK IMMEDIATE;
```

> ⚠️ `NEW_BROKER` will generate a **new Service Broker identifier**, invalidating existing conversations. Avoid this on production systems unless necessary.

### 🔧 Installing or Using Service Broker

There’s no separate "installation" of Service Broker — it's a built-in feature of SQL Server. You **enable**, **configure**, and **use** it via T-SQL.

If you're building a custom solution using Service Broker:

1. **Create message types**
2. **Create contracts**
3. **Create queues**
4. **Create services**
5. **Begin conversations and send messages**

Example setup (simplified):

```sql
-- Message Type
CREATE MESSAGE TYPE [MyMessage] VALIDATION = NONE;

-- Contract
CREATE CONTRACT [MyContract] ([MyMessage] SENT BY INITIATOR);

-- Queue
CREATE QUEUE [MyQueue];

-- Service
CREATE SERVICE [MyService]
    ON QUEUE [MyQueue]
    ([MyContract]);
```

### 🧠 Summary

| Feature              | Description                                                        |
| -------------------- | ------------------------------------------------------------------ |
| **Service Broker**   | Messaging system in SQL Server                                     |
| **Used in `msdb`**   | For Database Mail, notifications, etc.                             |
| **Check if Enabled** | `SELECT is_broker_enabled FROM sys.databases WHERE name = 'msdb';` |
| **Enable it**        | `ALTER DATABASE msdb SET ENABLE_BROKER;` (Use caution!)            |
| **Custom Use**       | Create message types, contracts, queues, services                  |

## **configure Database Mail** using the **SQL Server Management Studio (SSMS) GUI** — no T-SQL required.

### ✅ **Step-by-Step: Configure Database Mail in SSMS GUI**

> ⚠️ **Prerequisite**: You must be a member of the **sysadmin** role to configure Database Mail.

#### 🔹 Step 1: Open SSMS and Connect to SQL Server

1. Launch **SQL Server Management Studio (SSMS)**.
2. Connect to your SQL Server instance.

#### 🔹 Step 2: Enable Database Mail Feature (if disabled)

1. In **Object Explorer**, expand **Management**.
2. Right-click on **Database Mail** and select **Configure Database Mail**.
3. If this is your first time, a message will prompt:
   🛠️ *"Database Mail is not enabled. Would you like to enable it?"*
   Click **Yes**.

#### 🔹 Step 3: Launch Database Mail Configuration Wizard

1. In the **Welcome screen**, choose:

   * **Set up Database Mail by performing the following tasks**
2. Click **Next**.

#### 🔹 Step 4: Create a New Profile

1. Enter a **Profile Name** (e.g., `DefaultMailProfile`).
2. Optionally, provide a **Description**.
3. Click **Add** to add a new SMTP account.

#### 🔹 Step 5: Configure the SMTP Account

Fill in the details for your SMTP mail server:

| Field                    | Description                                      |
| ------------------------ | ------------------------------------------------ |
| **Account Name**         | e.g., `SQLMailAccount`                           |
| **Description**          | Optional                                         |
| **Email Address**        | The sender's email (e.g., `sql@yourdomain.com`)  |
| **Display Name**         | Friendly name (e.g., `SQL Server Alerts`)        |
| **Reply Email**          | Address for replies                              |
| **Server Name**          | SMTP server address (e.g., `smtp.office365.com`) |
| **Port Number**          | Usually `587` for TLS, or `25` or `465`          |
| **SSL**                  | Check if SSL/TLS is required                     |
| **Basic Authentication** | Provide SMTP username and password               |

> Make sure you have SMTP credentials from your email provider (e.g., Office365, Gmail, or internal mail server).

- Click **OK** when done.

#### 🔹 Step 6: Assign the Account to the Profile

- The new account will appear in the list.
   - Click **Next**.

#### 🔹 Step 7: Set the Profile as Public (Optional)

- You can make the profile:

   * **Public**: Usable by all users.
   * **Private**: Restricted to specific users.

- Check **Public** if you want general use (e.g., SQL Agent Jobs).
   - Click **Next**.


#### 🔹 Step 8: Configure System Parameters (Optional)

- You can set limits like:

   * Max email size
   * Max retries
   * Retry interval

- Default settings are usually fine. Click **Next**.

#### 🔹 Step 9: Complete the Wizard

- Review the summary, then click **Finish**.

#### ✅ Step 10: Send a Test Email

1. In **Object Explorer**, right-click **Database Mail**.
2. Choose **Send Test E-Mail...**
3. Fill in:

   * **To**: Your email address
   * **Subject/Body**: Anything you like
4. Click **Send Test E-Mail**

- You should receive an email within a minute or two.

### 🧪 Troubleshooting Tips

* Check **SQL Server Agent** is running — it's often required for automated notifications.
* If mail fails, check:

```sql
EXEC msdb.dbo.sysmail_event_log_sp;
```

* View logs in:

  * SSMS → Management → Database Mail → **View Database Mail Log**

* If emails are queued but not sent, restart the **SQL Server Agent** and check again.

### 📬 Example SMTP Server Settings

| Email Provider | SMTP Server           | Port | SSL/TLS |
| -------------- | --------------------- | ---- | ------- |
| Gmail          | `smtp.gmail.com`      | 587  | Yes     |
| Outlook/365    | `smtp.office365.com`  | 587  | Yes     |
| Yahoo          | `smtp.mail.yahoo.com` | 465  | Yes     |

> For Gmail, you'll need to enable **App Passwords** or use **OAuth** (T-SQL scripting only).

## Set up a **SQL Server Alert** for **fatal errors** (like severity 20-25 errors) using the **SSMS GUI** — which will send an **email via Database Mail** when a fatal error occurs.

### 🛑 What Are Fatal Errors?

In SQL Server, **fatal errors** are typically severity **level 20–25**, which indicate serious problems like:

* Hardware failures
* Corruption
* System resource failures
* SQL Server internal bugs

- These are rare but **critical**, and it’s good practice to set up alerts for them.

### ✅ Prerequisites

- Before you begin:

| Requirement                       | Details                                             |
| --------------------------------- | --------------------------------------------------- |
| **Database Mail**                 | Must be configured and working (as you already did) |
| **SQL Server Agent**              | Must be **running**                                 |
| **SQL Server Agent Mail Profile** | Must be set to use your Database Mail profile       |

### 🔹 Step-by-Step: Setup Alert for Fatal Errors

#### **Step 1: Ensure SQL Server Agent Uses Database Mail**

1. In SSMS, right-click **SQL Server Agent** → **Properties**.
2. Go to **Alert System** tab.
3. Check **Enable mail profile**.
4. Select your **Database Mail profile** (e.g., `DefaultMailProfile`).
5. Click **OK**.
6. Restart **SQL Server Agent** to apply changes.

#### **Step 2: Create a SQL Server Alert**

1. In SSMS, under **SQL Server Agent**, expand **Alerts**.
2. Right-click **Alerts** → **New Alert...**

#### **Step 3: Fill in General Settings**

| Field             | What to Enter                                     |
| ----------------- | ------------------------------------------------- |
| **Name**          | `Fatal Errors Alert` (or anything descriptive)    |
| **Type**          | `SQL Server event alert`                          |
| **Database name** | `All Databases`                                   |
| **Severity**      | Choose `20` (or create multiple alerts for 20–25) |

> You can only pick **either severity or error number**, not both.

#### **Step 4: Configure Response (Send Email)**

1. Go to the **Response** tab.
2. Check **Notify Operators** → Click **New Operator...**

#### **Step 5: Create an Operator**

1. Enter an **Operator Name** (e.g., `DBA Operator`).
2. Enter **E-mail name** (the email where alerts should be sent).
3. Click **OK**.

- Back in the Alert screen, check the box next to the new operator’s name under **E-mail**, and make sure it’s using your mail profile.

#### **Step 6: Optional – Include Job Execution**

- In the **Response** tab, you can also choose to **execute a job** when a fatal error occurs — e.g., backup logs, collect diagnostics, etc.

#### **Step 7: Finish**

- Click **OK** to save the alert.

- Repeat steps to create alerts for **severities 21–25** if desired, since each severity level may need a separate alert.

### 🧪 Test the Alert

- Unfortunately, **fatal errors** are not easy (or safe) to simulate. But you can:

1. **Create a test alert** with severity **16** (common error level).
2. Raise an error manually:

   ```sql
   RAISERROR('Test alert', 16, 1) WITH LOG;
   ```
3. Wait a few moments to see if the alert sends an email.

### 🔎 View Alert History & Troubleshoot

* Go to: **SQL Server Agent** → **Error Logs** → Right-click → **View Agent Log**
* Or check:

  ```sql
  EXEC msdb.dbo.sysmail_event_log_sp;
  ```

### 🧠 Summary

| Step | Task                                           |
| ---- | ---------------------------------------------- |
| ✅    | Configure Database Mail (done)                 |
| ✅    | Set SQL Server Agent to use mail               |
| ✅    | Create alert for severity 20–25                |
| ✅    | Create Operator with valid email               |
| ✅    | Set alert to notify via email                  |
| ✅    | (Optional) Attach a job for automated response |


## 1️⃣ What is **Job Activity Monitor**?

**Job Activity Monitor** is a built-in tool in SSMS that lets you **view the status and history** of SQL Server Agent jobs.

- You can quickly see:

   * Which jobs are running, idle, or failed
   * Last run status and time
   * Next scheduled run
   * Job history (success, failure, retry info)

### How to Open and Use **Job Activity Monitor**

1. Open **SSMS** and connect to your SQL Server instance.

2. In **Object Explorer**, expand **SQL Server Agent**.

3. Right-click **Job Activity Monitor** → Click **View Job Activity**.

4. The window lists all jobs with columns like:

   * **Name**
   * **Status** (Idle, Running, Succeeded, Failed)
   * **Last Run Outcome** (Succeeded, Failed, Cancelled)
   * **Last Run Date/Time**
   * **Next Run Date/Time**

5. Right-click any job to:

   * Start or stop the job
   * View job history (detailed run logs)
   * Enable or disable the job

### 2️⃣ Configuring Alerts & Notifications for an Existing Job

- You can configure a job to **notify operators** by email, pager, or net send when it completes or fails.

#### Step-by-Step: Configure Notifications for a Job

> **Pre-requisite:** You must have **Database Mail** configured and operators created. SQL Server Agent must be running and linked to Database Mail (as described earlier).

##### Step 1: Open Job Properties

1. In **Object Explorer**, expand **SQL Server Agent** → **Jobs**.
2. Right-click the existing job → Click **Properties**.

##### Step 2: Go to Notifications Page

1. In the job properties window, select the **Notifications** page (on the left panel).
2. Here you will see options to notify an operator via:

   * **Email**
   * **Pager**
   * **Net send**

##### Step 3: Configure When to Notify

- You can choose to notify on:

* **When the job succeeds**
* **When the job fails**
* **When the job completes (success or failure)**

- Check the box for the desired notification, then choose the **Operator** from the dropdown list.

##### Step 4: Save and Close

- Click **OK** to save changes.

##### Step 5: (Optional) Test Notification

- You can:

   * Manually run the job by right-clicking and choosing **Start Job**.
   * Check if the operator receives the email or other notifications on completion/failure.

### Summary Table

| Task                       | How to Access                                                          | Description                                    |
| -------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------- |
| Open Job Activity Monitor  | SQL Server Agent → Right-click → Job Activity Monitor                  | View status and history of jobs                |
| Configure Job Notification | SQL Server Agent → Jobs → Right-click job → Properties → Notifications | Set email/pager notifications for job outcomes |


## Step-by-Step Guide to Setup SQL Server Replication (Publication & Subscription)

### 🔹 Prerequisites & Preparations

- Before starting replication setup:

| Requirement                  | Details                                                        |
| ---------------------------- | -------------------------------------------------------------- |
| **SQL Server Edition**       | Replication is supported in Standard, Enterprise editions      |
| **SQL Server Agent**         | Must be running on both Publisher and Subscriber servers       |
| **Permissions**              | User must be a member of `sysadmin` role or `db_owner`         |
| **Network connectivity**     | Between Publisher and Subscriber (TCP/IP open)                 |
| **Databases**                | Database must be in **FULL** or **Bulk-Logged** recovery model |
| **Database Mail (optional)** | Useful for replication alerts                                  |
| **No active transactions**   | Clean database state for initial snapshot                      |

### 🔹 Step 1: Enable SQL Server Replication Features

1. Open **SQL Server Management Studio (SSMS)**.
2. Connect to the **Publisher SQL Server instance**.
3. Expand **Management** → Right-click **Replication** → Select **Configure Distribution**.
4. This launches the **Configure Distribution Wizard**.

#### In Configure Distribution Wizard:

* Choose to configure the server as a **Distributor** (can be the same as Publisher).
* Specify the **distribution database** name (default: `distribution`).
* Set the folder for snapshot files (default is fine).
* Finish the wizard — this sets up the Distributor.

### 🔹 Step 2: Configure Publisher

1. In SSMS, expand **Replication** → Right-click **Local Publications** → **New Publication**.
2. Select the **publication database** (the database you want to replicate).
3. Choose the type of replication:

* For High Availability and data synchronization, **Transactional Replication** is commonly used.
* Alternatively, **Merge Replication** for bidirectional sync or if offline changes are expected.

4. Choose articles (tables, stored procedures, etc.) you want to publish.
5. Configure **article properties** if needed (filter rows, columns, etc.).
6. Specify **Snapshot Agent** schedule (when initial snapshot is created).
7. Name the publication (e.g., `MyPublication`).
8. Finish to create the publication.

### 🔹 Step 3: Configure Subscriber

1. On the **Subscriber SQL Server instance**, open SSMS and connect.
2. Expand **Replication** → Right-click **Local Subscriptions** → **New Subscription**.
3. Select the **Publisher** and the **publication** created in Step 2.
4. Choose the **Subscriber** and the **subscription database**:

   * Can be an existing database or create a new one.
5. Select **Subscription Type**:

   * **Push Subscription**: The Publisher pushes data to Subscriber.
   * **Pull Subscription**: The Subscriber pulls data from Publisher.
6. Configure the **distribution agent** schedule.
7. Finish creating the subscription.

### 🔹 Step 4: Initial Snapshot and Synchronization

* The **Snapshot Agent** generates a snapshot of published data.
* The **Distribution Agent** applies the snapshot and then continuous changes.

### Replication Monitoring

#### 🔹 Launch Replication Monitor

1. In SSMS, expand **Replication**.
2. Right-click **Replication** → Select **Launch Replication Monitor**.
3. In Replication Monitor, expand your Publisher to view publications.
4. You can monitor:

* **Status** (Running, Idle, Failed)
* **Latency**
* **Transactions**
* **Agents** status (Snapshot, Log Reader, Distribution agents)

### 🔹 Check Replication Status

* Look at **Agent Status** for errors.
* Check **Latency** values; high latency means delayed replication.
* See **Undistributed Commands** — if high, snapshot/log reader may be stuck.
* Check **Delivery Latency** at subscriber.

### 🔹 Troubleshooting & Debugging Replication

| Issue                         | Action                                                              |
| ----------------------------- | ------------------------------------------------------------------- |
| Agents not running            | Start agents manually via Replication Monitor or Agent Jobs         |
| Snapshot not generated        | Check Snapshot Agent history/log; ensure snapshot folder accessible |
| Distribution Agent failure    | Check job history, error messages in Replication Monitor            |
| Log Reader Agent stuck        | Confirm SQL Server Agent running; check database log usage          |
| Permissions errors            | Ensure agent service accounts have correct rights                   |
| Network errors                | Confirm network connectivity and firewall settings                  |
| Conflicts (Merge Replication) | Use conflict viewer or resolve conflicts manually                   |

### Summary Table of Key Components

| Component              | Purpose                                                                    |
| ---------------------- | -------------------------------------------------------------------------- |
| **Distributor**        | Manages data distribution, stores snapshots                                |
| **Publisher**          | Source database with published articles                                    |
| **Subscriber**         | Destination database receiving data                                        |
| **Snapshot Agent**     | Creates initial snapshot of published data                                 |
| **Log Reader Agent**   | Moves transactions from log to distribution DB (Transactional Replication) |
| **Distribution Agent** | Applies snapshot and transactions to subscriber                            |

## Detailed GUI Walkthrough: Setup Transactional Replication in SSMS

### Step 1: Configure Distribution

1. **Open SSMS** and connect to your SQL Server instance (this will be the Publisher).

2. In **Object Explorer**, expand **Management** → right-click **Replication** → select **Configure Distribution**.

3. **Configure Distribution Wizard** opens:

   * **Welcome Page:** Click **Next**.

4. **Distributor Selection:**

   * Choose **“Configure the SQL Server instance as its own Distributor”** (unless you have a separate Distributor server).
   * Click **Next**.

5. **Snapshot Folder:**

   * By default, a folder path for snapshot files will be shown (e.g., `C:\Program Files\Microsoft SQL Server\MSSQL15.MSSQLSERVER\MSSQL\ReplData`).
   * You can change this if needed but keep it accessible by all involved servers.
   * Click **Next**.

6. **Distribution Database Configuration:**

   * Leave default name `distribution`.
   * Adjust size and growth options if needed.
   * Click **Next**.

7. **Publishers to Use this Distributor:**

   * Your current server should be listed as Publisher.
   * Click **Next**.

8. **Complete the Wizard:**

   * Review summary and click **Finish**.
   * The wizard configures the distribution database and related agents.
   * Click **Close** when done.

### Step 2: Create a New Publication

1. In **Object Explorer**, expand **Replication** → right-click **Local Publications** → **New Publication**.

2. **New Publication Wizard** starts:

   * Click **Next** on the welcome screen.

3. **Select Publication Database:**

   * Choose the database you want to replicate (e.g., `AdventureWorks`).
   * Click **Next**.

4. **Choose Publication Type:**

   * Select **Transactional publication** (best for near real-time high availability).
   * Click **Next**.

5. **Articles Selection:**

   * Select the tables, stored procedures, or other objects to publish.
   * You can expand tables and select specific columns or filter rows (click **Article Properties** to do advanced filtering).
   * Click **Next**.

6. **Filter Rows (Optional):**

   * If you want to replicate a subset of data, configure row filters here.
   * Otherwise, click **Next**.

7. **Snapshot Agent Schedule:**

   * Choose to run immediately or schedule snapshots periodically.
   * Usually, “Run continuously” for real-time replication.
   * Click **Next**.

8. **Agent Security:**

   * Configure the security context under which the Snapshot Agent will run.
   * Usually use a SQL Server Agent service account or specify credentials.
   * Click **Next**.

9. **Publication Name:**

   * Enter a name for your publication (e.g., `AdventureWorks_TransactionalPub`).
   * Click **Next**.

10. **Wizard Summary:**

    * Review settings.
    * Click **Finish** to create the publication.

### Step 3: Create a New Subscription

1. In **Object Explorer** of the **Subscriber server**, expand **Replication** → right-click **Local Subscriptions** → **New Subscription**.

2. **New Subscription Wizard** opens:

   * Click **Next**.

3. **Publication Selection:**

   * Connect to the Publisher server.
   * Select the publication you created.
   * Click **Next**.

4. **Subscriber Selection:**

   * Select your Subscriber server.
   * Choose the subscription database:

     * Existing database or
     * Create a new database.
   * Click **Next**.

5. **Subscription Type:**

   * Choose **Push Subscription** (Publisher initiates data transfer) or **Pull Subscription** (Subscriber requests data).
   * Click **Next**.

6. **Agent Schedule:**

   * Choose how often the Distribution Agent runs.
   * For near real-time replication, set continuous schedule.
   * Click **Next**.

7. **Agent Security:**

   * Configure Distribution Agent’s security context.
   * Usually the SQL Server Agent service account or a proxy account.
   * Click **Next**.

8. **Wizard Summary:**

   * Review.
   * Click **Finish**.

### Step 4: Launch Replication Monitor

1. In SSMS, expand **Replication**.
2. Right-click **Replication** → select **Launch Replication Monitor**.
3. **Replication Monitor** window opens.
4. Expand the Publisher → expand your publication.
5. You can see:

   * Agent status (Running, Idle, Failed)
   * Latency information
   * Transaction counts
   * Detailed agent history by clicking on each agent type (Snapshot, Log Reader, Distribution).

### Step 5: Check Replication Status & Troubleshoot

* In **Replication Monitor**, check if agents show **Failed** status.
* Right-click failed agents → View **Agent History** for error messages.
* Common errors:

  * Network connectivity issues
  * Permissions problems on snapshot folder or database
  * SQL Server Agent not running
* Resolve errors based on agent log messages.
* Restart failed agents if needed from Replication Monitor.

### Bonus Tips

* Ensure **SQL Server Agent** is running on all servers.
* Check permissions for SQL Server Agent accounts to access snapshot folders.
* Use **sp\_help\_replication** stored procedure to get replication status.
* Regularly monitor latency to ensure replication health.


### Sample T-SQL Script: Transactional Replication Setup

```sql
-- Step 1: Enable the Distributor (on Publisher server)
EXEC sp_adddistributor @distributor = 'YourPublisherServerName', @password = 'StrongPassword';

-- Step 2: Configure distribution database and snapshot folder
EXEC sp_adddistributiondb 
    @database = 'distribution', 
    @data_folder = 'C:\ReplData',  -- change as needed
    @log_folder = 'C:\ReplData',   -- change as needed
    @log_file_size = 2;

-- Step 3: Link the Distributor to the Publisher
EXEC sp_adddistpublisher 
    @publisher = 'YourPublisherServerName', 
    @distribution_db = 'distribution', 
    @working_directory = 'C:\ReplData', 
    @security_mode = 1;

-- Step 4: Enable the database for publishing
EXEC sp_replicationdboption 
    @dbname = 'YourPublicationDB', 
    @optname = 'publish', 
    @value = 'true';

-- Step 5: Create a new publication
EXEC sp_addpublication 
    @publication = 'YourPublicationName', 
    @status = 'active', 
    @allow_push = 'true', 
    @allow_pull = 'true', 
    @publication_type = 0,  -- 0 = Transactional
    @description = 'Transactional publication on YourPublicationDB';

-- Step 6: Add articles (tables) to publication
EXEC sp_addarticle 
    @publication = 'YourPublicationName', 
    @article = 'YourTableName', 
    @source_owner = 'dbo', 
    @source_object = 'YourTableName', 
    @type = 'logbased', 
    @description = 'Table replication';

-- Step 7: Create push subscription (run on Subscriber server)
EXEC sp_addsubscription 
    @publication = 'YourPublicationName', 
    @subscriber = 'YourSubscriberServerName', 
    @destination_db = 'YourSubscriberDB', 
    @subscription_type = 'Push', 
    @sync_type = 'automatic', 
    @status = 'active';

-- Step 8: Start the Snapshot Agent job to generate initial snapshot
EXEC sp_startpublication_snapshot @publication = 'YourPublicationName';
```

#### Notes:

* Replace `'YourPublisherServerName'`, `'YourPublicationDB'`, `'YourPublicationName'`, `'YourTableName'`, `'YourSubscriberServerName'`, and `'YourSubscriberDB'` with your actual names.
* Snapshot folder paths (`C:\ReplData`) must exist and be accessible to SQL Server Agent service accounts on both Publisher and Distributor.
* Security settings are minimal here; for production, you need to configure appropriate security contexts and proxy accounts.
* After running, monitor agent jobs in SSMS → SQL Server Agent → Jobs.

Absolutely! Here’s a **complete guide to SQL Server Log Shipping for High Availability**, including:

* What it is
* Prerequisites
* Step-by-step configuration with SSMS GUI
* T-SQL script examples
* Monitoring & troubleshooting tips

---

# **SQL Server Log Shipping for High Availability**

---

## What is Log Shipping?

Log Shipping is a disaster recovery solution that automatically sends transaction log backups from a **primary (source) database** to one or more **secondary (standby) databases** on separate SQL Server instances. The secondary databases are kept nearly synchronized by restoring the transaction logs.

It provides:

* Near real-time failover support
* Offsite or onsite secondary copies
* Simplicity and minimal impact on primary server

---

# Prerequisites

| Requirement             | Details                                                       |
| ----------------------- | ------------------------------------------------------------- |
| SQL Server editions     | Standard and Enterprise editions support Log Shipping         |
| SQL Server Agent        | Must be running on both Primary and Secondary servers         |
| Database Recovery Model | Primary database must use **FULL** recovery model             |
| Network connectivity    | Open between Primary and Secondary servers                    |
| Backup folder           | Shared network folder accessible by both servers (read/write) |
| Permissions             | SQL Server Agent service accounts must have access to folders |

## Step-by-Step Guide to Configure Log Shipping via SSMS

### Step 1: Prepare Primary Database

1. **Set Database to Full Recovery Model**:

   * Open SSMS → Connect to Primary server.
   * Expand **Databases**, right-click your database → **Properties**.
   * Go to **Options**, set **Recovery Model** to **Full**.
   * Click **OK**.

### Step 2: Configure Log Shipping on Primary Server

1. Right-click the **database** you want to configure → **Properties**.
2. Go to **Transaction Log Shipping** page (left pane).
3. Check **Enable this as a primary database in a log shipping configuration**.
4. Configure **Backup Settings**:

   * Click **Backup Settings** button.
   * Specify **Backup folder** (a shared folder accessible by primary and secondary).
   * Set **Backup job schedule** (e.g., every 15 minutes).
   * Click **OK**.

### Step 3: Configure Secondary Server and Restore Settings

1. Click **Add** under **Secondary Server Instances**.
2. In the **Secondary Database Settings** window:

   * Specify **Secondary server name**.
   * Specify **Secondary database name** (can be new or existing database).
   * Choose **Initialize Secondary Database**:

     * **No** (if you already have a backup restored)
     * **Yes** (to have log shipping copy and restore a full backup)
   * Configure **Copy Files** settings (folder where transaction log backups will be copied).
   * Configure **Restore Settings**:

     * Specify restore mode:

       * **No recovery** (database stays in restoring state - ideal for automatic failover)
       * **Standby mode** (database readable but no writes allowed)
     * Configure **Restore job schedule**.
   * Click **OK**.

### Step 4: Configure Monitor Server (Optional)

1. You can specify a monitor server and alert settings on the **Transaction Log Shipping** page:

   * Enter monitor server name and configure alert thresholds.
2. Alerts can be sent via Database Mail for failures.

### Step 5: Save and Enable Log Shipping

1. Click **OK** to close the database properties window.
2. Log Shipping jobs (backup, copy, restore) will be created and started automatically.
3. Verify that jobs appear under **SQL Server Agent → Jobs** on primary and secondary servers.

### Step 6: Verify Log Shipping Status

* Right-click the database → **Transaction Log Shipping Status**.
* A dashboard shows:

  * Last backup, copy, and restore times.
  * Status of jobs.
  * Alerts or errors if any.

### T-SQL Script Example for Log Shipping Setup

- Here is a simplified script to configure log shipping backup on primary database:

```sql
-- Enable FULL recovery
ALTER DATABASE YourDB SET RECOVERY FULL;
GO

-- Create a shared backup folder (ensure accessible)

-- Backup job on primary (run this as a job step)
BACKUP LOG YourDB 
TO DISK = '\\YourSharedFolder\YourDB_LogBackup.trn'
WITH INIT, NORECOVERY;
GO

-- On secondary server, restore full backup and log backups as per schedule
RESTORE DATABASE YourDB 
FROM DISK = '\\YourSharedFolder\YourDB_FullBackup.bak' 
WITH NORECOVERY;
GO

RESTORE LOG YourDB 
FROM DISK = '\\YourSharedFolder\YourDB_LogBackup.trn' 
WITH NORECOVERY;
GO
```

> **Note:** The full log shipping automation requires SQL Server Agent jobs and jobs to run backup, copy, and restore tasks in scheduled order.

### Monitoring and Troubleshooting Log Shipping

#### How to Monitor:

* Use **Transaction Log Shipping Status** window in SSMS (right-click database).
* Check SQL Server Agent jobs on both primary and secondary servers.
* Use Replication Monitor for replication errors if configured.
* Query log shipping system tables:

```sql
USE msdb;
GO
SELECT primary_database, secondary_database, backup_finish_date, last_copied_file, last_restored_file, restore_lsn
FROM dbo.log_shipping_monitor_primary;
GO
```

#### Common Issues & Fixes:

| Issue                          | Possible Cause                      | Fix                                          |
| ------------------------------ | ----------------------------------- | -------------------------------------------- |
| Backup job failing             | Permission issue on backup folder   | Check SQL Server Agent account access        |
| Copy job failing               | Network or folder permissions issue | Verify network path and shared folder access |
| Restore job failing            | Database in use or restore error    | Ensure no connections, check restore mode    |
| Log shipping lag or latency    | Schedule too long or jobs failing   | Shorten schedule, check job statuses         |
| Secondary database not in sync | Missing backups or copy errors      | Check job history, restore latest backups    |

### Summary Workflow Diagram (Conceptual)

```
Primary DB (Full Recovery)
        |
   Backup Log (SQL Agent Job)
        |
Shared Network Folder (copy location)
        |
Secondary Server (Copy Job copies files)
        |
Secondary DB (Restore Log job applies changes)
```

### Bonus: Automate Alerts with Database Mail

* Configure Database Mail.
* Setup SQL Server Agent alerts on log shipping jobs.
* Get email notifications on job failures.

Got it! Here’s a **full T-SQL script** that automates the basic setup of **Log Shipping** on the primary server side — including enabling full recovery, creating backup jobs, and configuring the log shipping primary database.

You will still need to configure the secondary server and the copy/restore jobs similarly on that server.

---

## T-SQL Script: Automate Log Shipping Primary Configuration

```sql
USE master;
GO

-- Variables - Change these to your environment
DECLARE @PrimaryServer SYSNAME = 'PrimaryServerName';
DECLARE @SecondaryServer SYSNAME = 'SecondaryServerName';
DECLARE @PrimaryDB SYSNAME = 'YourDatabase';
DECLARE @SecondaryDB SYSNAME = 'YourDatabase_Secondary';
DECLARE @BackupShare NVARCHAR(255) = '\\YourBackupShare\LogShipping';
DECLARE @BackupJobName NVARCHAR(128) = 'LSBackup_YourDatabase';

-- Step 1: Set the database to FULL recovery model
ALTER DATABASE [@PrimaryDB] SET RECOVERY FULL;
GO

-- Step 2: Create backup job for log shipping (runs every 15 minutes)
EXEC msdb.dbo.sp_add_job
    @job_name = @BackupJobName,
    @enabled = 1,
    @description = 'Log Shipping Backup Job for ' + @PrimaryDB,
    @owner_login_name = 'sa';
GO

EXEC msdb.dbo.sp_add_jobstep
    @job_name = @BackupJobName,
    @step_name = 'Backup Transaction Log',
    @subsystem = 'TSQL',
    @command = '
    BACKUP LOG [' + @PrimaryDB + '] TO DISK = ''' + @BackupShare + '\' + @PrimaryDB + '_log.trn'' WITH INIT, NOFORMAT, NO_TRUNCATE, NAME = ''' + @PrimaryDB + ' Transaction Log Backup'';
    ',
    @database_name = 'master',
    @on_success_action = 1,
    @on_fail_action = 2;
GO

EXEC msdb.dbo.sp_add_schedule
    @schedule_name = 'LSBackupSchedule_' + @PrimaryDB,
    @freq_type = 4, -- daily
    @freq_interval = 1,
    @freq_subday_type = 4, -- minutes
    @freq_subday_interval = 15, -- every 15 minutes
    @active_start_time = 0;
GO

EXEC msdb.dbo.sp_attach_schedule
    @job_name = @BackupJobName,
    @schedule_name = 'LSBackupSchedule_' + @PrimaryDB;
GO

EXEC msdb.dbo.sp_add_jobserver
    @job_name = @BackupJobName,
    @server_name = @@SERVERNAME;
GO

PRINT 'Log Shipping Backup Job created and scheduled every 15 minutes';
```

### Notes:

* Replace `'PrimaryServerName'`, `'SecondaryServerName'`, `'YourDatabase'`, and `\\YourBackupShare\LogShipping` with your real server names, database names, and backup share.
* This script only creates the **log backup job** on the primary.
* You’ll need to configure the **copy** and **restore jobs** on the secondary server (can also be scripted).
* Also, you need to set up the log shipping configuration tables and metadata, which is easier done via SSMS or extended scripts.

## What is an Execution Plan?

An **Execution Plan** is a graphical or textual representation that shows how SQL Server executes a query. It details the sequence of operations, data access methods, join algorithms, and the cost of each step.

### Why Use Execution Plans?

* **Performance Tuning:** Identify slow parts of a query and optimize them.
* **Understanding Query Behavior:** See how SQL Server processes your SQL statements.
* **Detecting Inefficiencies:** Spot missing indexes, table scans, excessive sorts, or joins.
* **Troubleshooting:** Analyze why a query is taking longer than expected or consuming excessive resources.

### Where to Find Execution Plan in SSMS?

1. **Icons and Menu:**

   * **Display Estimated Execution Plan:**

     * Icon: A graphical query plan icon (like a query with a flowchart).
     * Shortcut: Press `Ctrl + L` or click the toolbar button with a small flowchart-like icon labeled **"Display Estimated Execution Plan"**.
   * **Include Actual Execution Plan:**

     * Icon: A similar icon, but usually in the toolbar or in the **Query** menu, labeled **"Include Actual Execution Plan"**.
     * Shortcut: Press `Ctrl + M`.
2. **Location:**

   * Found on the SSMS toolbar (near the Execute button).
   * Under the **Query** menu → **Include Actual Execution Plan** or **Display Estimated Execution Plan**.

### Types of Execution Plans

* **Estimated Execution Plan:**
  Generated without executing the query, based on statistics and query optimizer’s prediction.

* **Actual Execution Plan:**
  Captured after query execution, contains runtime information like actual row counts, IO, CPU usage.

### How to Use Execution Plan in SSMS?

1. **Generate Estimated Execution Plan:**

   * Open a query window.
   * Write your query.
   * Click **Display Estimated Execution Plan** (or `Ctrl + L`).
   * The plan appears in a tab below the query.

2. **Generate Actual Execution Plan:**

   * Click **Include Actual Execution Plan** (or `Ctrl + M`).
   * Run the query (press **Execute** or `F5`).
   * After execution, an **Execution Plan** tab appears showing detailed info.

### Understanding the Execution Plan

* **Operators:**
  Each icon in the plan represents an operator (e.g., Index Seek, Table Scan, Nested Loop Join).

* **Cost %:**
  Relative cost of each operator, showing where SQL Server spends most resources.

* **Data Flow:**
  Arrows between operators indicate data flow and row counts.

* **Warnings:**
  Icons like a yellow triangle indicate warnings (e.g., missing indexes, spills to tempdb).

* **Tooltips:**
  Hover over operators to see detailed stats like estimated rows, actual rows, CPU time, IO cost.

### How Execution Plans Help You

* Identify **table scans** that might need indexes.
* Spot **expensive operators** (like sorts or hash joins) that can be optimized.
* Understand **join order** and methods to optimize query logic.
* Detect **parameter sniffing issues** or outdated statistics.
* Optimize queries by rewriting SQL or adding indexes based on plan insights.

### Bonus Tips

* Use **Query Store** (in newer SQL Server versions) to capture and compare execution plans over time.
* Save execution plans (`.sqlplan` files) to share with DBAs or developers.
* Use **SET STATISTICS XML ON** to get execution plans in XML format.

## What is Transparent Data Encryption (TDE)?

TDE encrypts the **data at rest** in the database files and backups. It helps protect sensitive data from unauthorized access if the files or backups are stolen. It performs real-time I/O encryption and decryption of data and log files.

### Why Use TDE?

* Protects data files and backups from unauthorized access.
* Helps meet compliance standards (e.g., GDPR, HIPAA).
* Transparent to applications—no need to change your queries or apps.
* Prevents reading data directly from the file system.

### High-Level Components of TDE

1. **Service Master Key (SMK)** – Root key of SQL Server instance.
2. **Database Master Key (DMK)** – Protects the certificate.
3. **Certificate** – Used to protect the Database Encryption Key.
4. **Database Encryption Key (DEK)** – Symmetric key used to encrypt the database.
5. **TDE** – Encrypts data files and backups with DEK.

### Step-by-Step Guide to Configure TDE in SSMS

#### Step 1: Create a Master Key in the Master Database

1. Connect to your SQL Server instance in SSMS.
2. Open a new query window and run:

```sql
USE master;
GO
CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'StrongMasterKeyPassword!';
GO
```

#### Step 2: Create a Certificate Protected by the Master Key

```sql
CREATE CERTIFICATE MyTDECert WITH SUBJECT = 'TDE Certificate';
GO
```

#### Step 3: Backup the Certificate and Private Key

* Right-click on the **Certificates** folder under **Security > Certificates** in SSMS.
* Find your certificate (`MyTDECert`), right-click → **All Tasks** → **Export**.
* Save the certificate `.cer` file and the private key `.pvk` file securely.
* Or use T-SQL:

```sql
BACKUP CERTIFICATE MyTDECert
TO FILE = 'C:\Backup\MyTDECert.cer'
WITH PRIVATE KEY (
    FILE = 'C:\Backup\MyTDECert.pvk',
    ENCRYPTION BY PASSWORD = 'StrongCertPassword!'
);
GO
```

**Important:** Keep this backup safe. You’ll need it to restore or attach the encrypted database on another server.

#### Step 4: Create Database Encryption Key (DEK) in the User Database

```sql
USE YourDatabase;
GO
CREATE DATABASE ENCRYPTION KEY
WITH ALGORITHM = AES_256
ENCRYPTION BY SERVER CERTIFICATE MyTDECert;
GO
```

#### Step 5: Enable Encryption on the Database

```sql
ALTER DATABASE YourDatabase
SET ENCRYPTION ON;
GO
```

* Encryption runs in the background; you can check encryption state:

```sql
SELECT name, is_encrypted
FROM sys.databases
WHERE name = 'YourDatabase';
GO
```

### Step-by-Step: Restoring a TDE-Enabled Database

#### Step 1: Backup the Certificate and Keys from Source Server

- Make sure you have the `.cer` and `.pvk` files from the source server.

#### Step 2: Create Master Key on Target Server (if not exists)

```sql
USE master;
GO
CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'StrongMasterKeyPassword!';
GO
```

#### Step 3: Create Certificate on Target Server from Backup

```sql
CREATE CERTIFICATE MyTDECert
FROM FILE = 'C:\Backup\MyTDECert.cer'
WITH PRIVATE KEY (
    FILE = 'C:\Backup\MyTDECert.pvk',
    DECRYPTION BY PASSWORD = 'StrongCertPassword!'
);
GO
```

#### Step 4: Restore the TDE-Encrypted Database

- Now, you can restore the database backup normally:

```sql
RESTORE DATABASE YourDatabase
FROM DISK = 'C:\Backups\YourDatabase.bak'
WITH MOVE 'YourDatabase_Data' TO 'C:\Data\YourDatabase.mdf',
     MOVE 'YourDatabase_Log' TO 'C:\Data\YourDatabase_log.ldf';
GO
```

### Configuring TDE via SSMS GUI

1. **Create Master Key and Certificate:**

   * Expand **Security** → **Master Keys** (right-click to create if not exists).
   * Expand **Security** → **Certificates** → right-click → **New Certificate**.
   * Fill in certificate details.

2. **Backup Certificate:**

   * Right-click the certificate → **All Tasks** → **Export**.
   * Follow the wizard to export certificate and private key.

3. **Enable Encryption:**

   * Right-click your database → **Properties** → **Options**.
   * Scroll to **Encryption Enabled** → check **True**.
   * Click **OK**.

### Why TDE Is Important for Your Environment

* Protects sensitive data from theft/loss of physical media.
* Ensures compliance with legal and regulatory requirements.
* Does not affect query performance significantly.
* Works seamlessly with backups — backup files are encrypted.

### Monitoring TDE

- Check encryption state:

```sql
SELECT db.name, dek.encryption_state, dek.key_algorithm, dek.key_length
FROM sys.dm_database_encryption_keys dek
JOIN sys.databases db ON dek.database_id = db.database_id;
GO
```

- Encryption\_state values:

| Value | Meaning                |
| ----- | ---------------------- |
| 0     | No encryption          |
| 1     | Unencrypted            |
| 2     | Encryption in progress |
| 3     | Encrypted              |
| 4     | Key change in progress |
| 5     | Decryption in progress |

### Summary

| Step                           | Purpose                                 |
| ------------------------------ | --------------------------------------- |
| Create Master Key              | Root key for encryption                 |
| Create Certificate             | Used to encrypt database encryption key |
| Backup Certificate             | Needed to restore encrypted database    |
| Create Database Encryption Key | Encrypts the database                   |
| Enable Encryption              | Turns on TDE for database               |


## `SQL Queries`

- Know about Database date

```sql
select getdate()
```

- Delete only 1 row of the table

```sql
delete top(1) from <tableName>
```
