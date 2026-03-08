# Restoring TDE-Encrypted SQL Database Backup

This document outlines the steps to restore a TDE-encrypted SQL database backup using a `.bak` file.

## Prerequisites

Before performing the restoration of a TDE-encrypted SQL database backup, ensure you have the following:

1. **SQL Server Version**: Ensure you are using a version of SQL Server that supports Transparent Data Encryption (TDE), such as SQL Server 2008 Enterprise Edition or later.

2. **Backup Files**:
   - The `.bak` file of the database you wish to restore.
   - The TDE certificate and private key file that were used to encrypt the database.

3. **Permissions**:
   - You must have sufficient permissions to create certificates and master keys. Typically, this requires `sysadmin` or similar roles.

4. **Secure Passwords**: Ensure that you have access to the passwords used during the encryption and backup processes.

5. **SQL Server Management Studio (SSMS)**: It is recommended to perform these operations in SQL Server Management Studio for ease of execution.


## Step 1: Check Database Encryption Status

To verify the encryption status of your databases, execute the following SQL query:

```sql
SELECT 
    db.name, 
    db.is_encrypted, 
    dm.encryption_state, 
    dm.percent_complete, 
    dm.key_algorithm, 
    dm.key_length, 
    db.database_id 
FROM sys.databases db 
LEFT OUTER JOIN sys.dm_database_encryption_keys dm ON db.database_id = dm.database_id;
GO
```

## Step 2: List Certificates

To view the certificates available on the server, run:

```sql
SELECT * FROM sys.certificates;
GO
```

## Step 3: Backup the Server Certificate

Backup the TDE certificate with the following command:

```sql
BACKUP CERTIFICATE MyServerCert 
TO FILE 'D:\Vlog\Azure tutorial\SQL TDE Encryption\TDE_Cert' 
WITH PRIVATE KEY (
    FILE = 'D:\Vlog\Azure tutorial\SQL TDE Encryption\TDE_CertKey.pvk', 
    ENCRYPTION BY PASSWORD = 'mycertificatepassword@12345'
);
GO
```

### Error Handling

If you encounter an error such as:

```
Restore of database "TechKnowledge" failed. 
Additional information: System.Data.SqlClient.SqlError: 
Cannot find server certificate with thumbprint '0x0D1713C54F4BBDECE88617AFC83DBCB247C600'.
```

This indicates that the certificate is not available or not correctly referenced.

## Step 4: Create a Master Key

If necessary, create a master key in the master database:

```sql
USE master;
GO
CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'dontaskmeagain@12345';
GO
```

## Step 5: Restore the Certificate

To restore the previously backed-up certificate, execute:

```sql
CREATE CERTIFICATE BackupEncryptionCert 
FROM FILE = 'D:\Backup\tde_cert' 
WITH PRIVATE KEY (
    FILE = 'D:\Backup\tde_certkey.pvk', 
    DECRYPTION BY PASSWORD = 'mycertificatepassword@12345'
);
GO
```

## Conclusion

After following these steps, you should be able to restore your TDE-encrypted SQL database backup successfully. Ensure that all file paths and passwords are correctly specified and that the necessary certificates are available.

### Support Me

**If you find my content useful or enjoy what I do, you can support me by buying me a coffee. Your support helps keep this website running and encourages me to create more content.**

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sawanchokso)

**Your generosity is greatly appreciated!**