# RDMS(Relational Database System) Notes about PostgreSQL

## PostgreSQL RDBMS

**PostgreSQL** is an open-source, object-relational database management system (RDBMS) known for its robustness, extensibility, and standards compliance. Developed to handle a wide range of workloads, from small single-machine applications to large-scale web services, PostgreSQL supports advanced data types and performance optimization features.

#### Key Features:

- **ACID Compliance:** Ensures reliable transactions and data integrity.
- **Extensibility:** Supports custom data types, operators, and functions.
- **Advanced Indexing:** Includes B-tree, hash, GiST, GIN, and more for performance optimization.
- **Concurrency Control:** Uses Multi-Version Concurrency Control (MVCC) to handle concurrent transactions smoothly.
- **Rich Data Types:** Supports JSON, XML, hstore, and others, facilitating diverse data handling.
- **PostGIS Extension:** Enables spatial data handling for geographic information systems (GIS).

#### Use Cases:

1. **Web Applications:** PostgreSQL is popular for web development due to its support for complex queries and data integrity. Example: Reddit uses PostgreSQL for its backend.
2. **Data Warehousing:** Its robust performance and ability to handle large datasets make it suitable for data warehousing solutions.
3. **Geospatial Applications:** With PostGIS, it’s widely used for geographic and location-based applications.

#### Pros:

- **Open-Source:** Free to use with an active community providing continuous updates and support.
- **Reliability:** Known for high data integrity and reliable performance.
- **Flexibility:** Extensive support for various data types and custom extensions.
- **Advanced Features:** Includes full-text search, JSON support, and complex queries.

#### Cons:

- **Complexity:** The wide range of features can lead to a steeper learning curve.
- **Performance Tuning:** May require fine-tuning and optimization for high-performance scenarios.
- **Resource Usage:** Can be resource-intensive compared to simpler databases.

#### Impact on Information Technology Industry:

PostgreSQL has significantly impacted the technology industry by providing a powerful and flexible database solution for a wide range of applications. Its open-source nature has lowered costs for businesses and developers, while its advanced features have enabled the development of complex, high-performance applications. PostgreSQL's role in promoting open standards and fostering a collaborative community has further influenced the evolution of modern database technologies.

## Installation and Configuration of PostgreSQL 13 on RHEL 7 with Custom Port and User `postgres` Password

### 1. Prepare the Data Directory

If you want to use a non-default location for the PostgreSQL data directory, ensure the correct permissions are set:

```bash
# Set ownership of the data directory to the postgres user
chown -R postgres:postgres /user/local/poc/software/postgres-13/data

# Set directory permissions
chmod 750 /user/local/poc/software/postgres-13/data
```

### 2. Install PostgreSQL 13

#### a. Add PostgreSQL Repository

1. Visit [PostgreSQL Downloads](https://download.postgresql.org) to choose the appropriate repository for your OS. Select the following options:
   
   - **Version**: 13
   - **Platform**: RedHat/CentOS
   - **Architecture**: x86_64

2. Install the PostgreSQL repository RPM:
   
   ```bash
   yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm
   ```

#### b. Install PostgreSQL Server

1. Install the PostgreSQL 13 server package:
   
   ```bash
   yum install -y postgresql13-server
   ```

2. Initialize the PostgreSQL 13 database cluster:
   
   ```bash
   /usr/pgsql-13/bin/postgresql-13-setup initdb
   ```

3. Start the PostgreSQL service:
   
   ```bash
   systemctl start postgresql-13.service
   ```

4. Verify that the PostgreSQL service is running:
   
   ```bash
   ps -ef | grep postmaster
   ```

5. Enable PostgreSQL to start on boot:
   
   ```bash
   systemctl enable postgresql-13.service
   ```

### 3. Manage PostgreSQL Service

- **Start PostgreSQL service**:
  
  ```bash
  systemctl start postgresql-13.service
  ```

- **Stop PostgreSQL service**:
  
  ```bash
  systemctl stop postgresql-13.service
  ```

- **Restart PostgreSQL service**:
  
  ```bash
  systemctl restart postgresql-13.service
  ```

- **Check status of PostgreSQL service**:
  
  ```bash
  systemctl status postgresql-13.service
  ```

### 4. Configure PostgreSQL

#### a. Check Default Port

Check the default port setting in the configuration file:

```bash
cat /var/lib/pgsql/13/data/postgresql.conf | grep port
```

By default, PostgreSQL listens on port 5432.

#### b. Configure PostgreSQL for Remote Connections

1. Edit `postgresql.conf` to set the desired port and listen addresses:
   
   ```bash
   vi /var/lib/pgsql/13/data/postgresql.conf
   ```
   
   - Update the following parameters:
     
     ```plaintext
     # - Connection Settings -
     listen_addresses = '*'          # Listen on all IP addresses
     port = 8114                     # Change port to 8114 or your preferred port
     ```

2. Edit `pg_hba.conf` to configure authentication methods:
   
   ```bash
   vi /var/lib/pgsql/13/data/pg_hba.conf
   ```
   
   - Update the file with the following entries:
     
     ```plaintext
     # TYPE  DATABASE        USER            ADDRESS                 METHOD
     
     # "local" is for Unix domain socket connections only
     local   all             all                                     trust
     # IPv4 local connections:
     host    all             all             0.0.0.0/0               md5
     # IPv6 local connections:
     host    all             all             ::1/128                 md5
     ```

3. Restart PostgreSQL to apply changes:
   
   ```bash
   systemctl restart postgresql-13.service
   ```

### 5. Post-Installation Steps

1. Switch to the `postgres` user:
   
   ```bash
   su - postgres
   ```

2. Connect to PostgreSQL using the new port:
   
   ```bash
   psql -p 8114
   ```

3. Change the default `postgres` user password:
   
   ```sql
   ALTER USER postgres PASSWORD '*********';
   ```

4. Exit the `psql` shell:
   
   ```sql
   \q
   ```

5. Switch back to the root user:
   
   ```bash
   exit
   ```

6. Restart PostgreSQL once more to ensure all changes are effective:
   
   ```bash
   systemctl restart postgresql-13.service
   ```

### 6. Verify Remote Connection

- Test the connection from a remote machine or using a PostgreSQL client such as pgAdmin to ensure that the server is accessible with the new settings.

## Connect `Postgres Server` using `psql`

To connect to a PostgreSQL server using `psql` with specific parameters like host, port, user, and password, you can use the following command-line options:

```sh
psql -h hostname -p port -U username -d database_name
```

Here's what each option means:

- `-h hostname` specifies the server address (e.g., `localhost` or `192.168.1.100`).
- `-p port` specifies the port number on which PostgreSQL is running (default is `5432`).
- `-U username` specifies the user you want to connect as.
- `-d database_name` specifies the name of the database you want to connect to.

### Example

To connect to a PostgreSQL server running on `localhost` at port `5432`, as user `myuser`, and to the database `mydatabase`, you would use:

```sh
psql -h localhost -p 5432 -U myuser -d mydatabase
```

### Password Prompt

When using `psql` from the command line, you will be prompted for the password associated with the specified user. `psql` does not accept passwords directly via command-line arguments for security reasons.

### Alternative: Using Environment Variables

If you prefer not to be prompted for a password each time, you can set the `PGPASSWORD` environment variable in your shell before running the `psql` command:

```sh
export PGPASSWORD='your_password'
psql -h localhost -p 5432 -U myuser -d mydatabase
```

**Note:** Storing passwords in environment variables can have security implications, so be cautious with this approach, especially on shared or insecure systems.

### Example with Environment Variables

```sh
export PGPASSWORD='mysecretpassword'
psql -h localhost -p 5432 -U myuser -d mydatabase
```

### Using a Connection Service File

For more complex connection configurations, you can use a PostgreSQL connection service file. This method allows you to store connection details in a configuration file and then reference this file in your `psql` commands.

1. **Create a `.pg_service.conf` file** in your home directory (or specify a different path with the `PGSERVICEFILE` environment variable):
   
   ```ini
   [myservice]
   host=localhost
   port=5432
   user=myuser
   dbname=mydatabase
   ```

2. **Connect using the service name**:
   
   ```sh
   psql service=myservice
   ```

## `psql` important widely used command and scripts

- We can run this command from `pgAdmin` as well as `psql` command line as well.
1. **Create Database:**
   
   ```sql
   CREATE DATABASE test_db;
   ```
   
   *Creates a new database named `test_db`.*

2. **Create Schema:**
   
   ```sql
   CREATE SCHEMA test_sc;
   ```
   
   *Creates a new schema named `test_sc` within the current database.*

3. **Grant Privileges on Database:**
   
   ```sql
   GRANT ALL PRIVILEGES ON DATABASE test_db TO test;
   ```
   
   *Grants all privileges on the `test_db` database to the user `test`.*

4. **Create Read-Only User:**
   
   ```sql
   CREATE USER testreadonly WITH PASSWORD 'password';
   ```
   
   *Creates a user `testreadonly` with a specified password.*

5. **Grant Connect Privilege to Read-Only User:**
   
   ```sql
   GRANT CONNECT ON DATABASE test_db TO testreadonly;
   ```
   
   *Allows the `testreadonly` user to connect to the `test_db` database.*

6. **Grant Usage on Schema to Read-Only User:**
   
   ```sql
   GRANT USAGE ON SCHEMA test_sc TO testreadonly;
   ```
   
   *Allows the `testreadonly` user to use the `test_sc` schema.*

7. **Grant Select on All Tables to Read-Only User:**
   
   ```sql
   GRANT SELECT ON ALL TABLES IN SCHEMA test_sc TO testreadonly;
   ```
   
   *Grants the `testreadonly` user permission to select (read) from all tables in `test_sc` schema.*

8. **Alter Default Privileges for Read-Only User:**
   
   ```sql
   ALTER DEFAULT PRIVILEGES IN SCHEMA test_sc GRANT SELECT ON TABLES TO testreadonly;
   ```
   
   *Ensures `testreadonly` gets select privileges on new tables created in `test_sc` schema.*

9. **Create Read-Write User:**
   
   ```sql
   CREATE USER testreadwrite WITH PASSWORD 'password';
   ```
   
   *Creates a user `testreadwrite` with a specified password.*

10. **Grant Connect Privilege to Read-Write User:**
    
    ```sql
    GRANT CONNECT ON DATABASE test_db TO testreadwrite;
    ```
    
    *Allows the `testreadwrite` user to connect to the `test_db` database.*

11. **Grant Usage on Schema to Read-Write User:**
    
    ```sql
    GRANT USAGE ON SCHEMA test_sc TO testreadwrite;
    ```
    
    *Allows the `testreadwrite` user to use the `test_sc` schema.*

12. **Grant Full Table Privileges to Read-Write User:**
    
    ```sql
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA test_sc TO testreadwrite;
    ```
    
    *Grants `testreadwrite` user permissions to select, insert, update, and delete from all tables in `test_sc` schema.*

13. **Alter Default Privileges for Read-Write User:**
    
    ```sql
    ALTER DEFAULT PRIVILEGES IN SCHEMA test_sc GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO testreadwrite;
    ```
    
    *Ensures `testreadwrite` gets select, insert, update, and delete privileges on new tables created in `test_sc` schema.*

### SQL Script

- This script ensures that `my_user` can only access the `test` schema and has no visibility or access to other schemas within the database. Adjust schema names and user details as needed.

```sql
-- Assuming you want to manage user 'my_user' and 'test' schema

-- Connect to the appropriate database
\c my_database;

-- Create user (if not already created)
CREATE USER my_user WITH PASSWORD 'secure_password';

-- Grant connect privilege to user (if not already done)
GRANT CONNECT ON DATABASE my_database TO my_user;

-- Revoke all access from user on all schemas (assuming there are multiple schemas)
DO $$
DECLARE
    schema_record RECORD;
BEGIN
    FOR schema_record IN
        SELECT schema_name
        FROM information_schema.schemata
        WHERE schema_name <> 'pg_catalog'
          AND schema_name <> 'information_schema'
          AND schema_name <> 'test'  -- Exclude the schema that should remain accessible
    LOOP
        EXECUTE format('REVOKE ALL ON SCHEMA %I FROM my_user;', schema_record.schema_name);
    END LOOP;
END $$;

-- Ensure user has usage access to the 'test' schema
GRANT USAGE ON SCHEMA test TO my_user;

-- Grant necessary privileges on all tables in 'test' schema (e.g., SELECT, INSERT, UPDATE, DELETE)
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA test TO my_user;

-- Set default privileges for future tables in 'test' schema
ALTER DEFAULT PRIVILEGES IN SCHEMA test GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO my_user;

-- Ensure no default privileges on other schemas (if applicable)
DO $$
DECLARE
    schema_record RECORD;
BEGIN
    FOR schema_record IN
        SELECT schema_name
        FROM information_schema.schemata
        WHERE schema_name <> 'pg_catalog'
          AND schema_name <> 'information_schema'
          AND schema_name <> 'test'
    LOOP
        EXECUTE format('ALTER DEFAULT PRIVILEGES IN SCHEMA %I REVOKE ALL ON TABLES FROM my_user;', schema_record.schema_name);
    END LOOP;
END $$;
```

### Support Me

**If you find my content useful or enjoy what I do, you can support me by buying me a coffee. Your support helps keep this website running and encourages me to create more content.**

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sawanchokso)

**Your generosity is greatly appreciated!**

##### Thank you for your support!💚