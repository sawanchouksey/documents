# PostgreSQL Database Server Authentication with AWS IAM role instead of using password

## Pre-requisite

1. AWS Cli tool must be installed

2. AWS Account with suitable permission i.e IAM, RDS, EC2 etc.

3. Postgrsql server or psql cli utility 

4. Amazon s3 bucket for SSL certificate 

### Create postgresql RDS server in AWS

```
aws rds create-db-cluster --db-cluster-identifier <cluster-name> --engine aurora-postgresql \
--master-username <user-name> --master-user-password <password> \
--db-subnet-group-name <subnet-name> --vpc-security-group-ids <security-group>
```

```
aws rds create-db-instance --db-instance-identifier <instance-name> \
--db-cluster-identifier <cluster-name> --engine aurora-postgresql --db-instance-class db.r4.large
```

Replace the placeholder with respect to your requirements.

### Enabling IAM authentication

To enable IAM authentication from the command line, you must know your cluster name. You can find the name on the RDS console or in the output values of the describe-db-clusters AWS CLI command. See the following code:

```
aws rds describe-db-clusters \
--query "DBClusters[*].[DBClusterIdentifier]"
```

```
aws rds modify-db-cluster \
--db-cluster-identifier <cluster-name> \
--apply-immediately \
--enable-iam-database-authentication
```

### Create IAM policy

an IAM user or role to connect to your database instance or database cluster, you must create an IAM policy.

You construct the policy document from the following four key pieces of data:

- The Region of your cluster

- Your AWS account number

- The database resource ID or the cluster resource ID

- Your database user name

- Specify an ARN that describes one database user account in one database instance using the following format:
  
  ```
  arn:aws:rds-db:<region>:<account-id>:dbuser:<resource-id>/<database-user-name>
  ```

```
For RDS:

{
  "Version" : "2012-10-17",
  "Statement" :
  [
    {
      "Effect" : "Allow",
      "Action" : ["rds-db:connect"],
      "Resource" : ["arn:aws:rds-db:us-east-1:123456789012:dbuser:db-ABCDEFGHIJKL01234/mydbuser"]
    }
  ]
}
```

### Create IAM user with attach policy

```
aws iam create-user --user-name mydbuser

aws iam attach-user-policy \
--policy-arn arn:aws:iam:123456789012:policy/database-login-mydbuser \
--user-name mydbuser
```

### Create Database User and Grant him permission for IAM authentication

After you create your IAM user and attach your IAM policy to the user, create a database user with the same name that you specified in the policy. To use IAM authentication with PostgreSQL, connect to the database cluster, create the database user, and grant them the `rds_iam` role. You can connect as any user that has `CREATE USER` permissions.

1. Login with master user and password in psql cli to perform action
   
   ```
   psql "host=hostName port=portNumber dbname=DBName user=MasterUserName password=MasterUserPassword
   ```

2. Create Db user and Grant him IAM authentication role from psql cli
   
   ```
   CREATE USER mydbuser; 
   GRANT rds_iam TO mydbuser;
   ```

### Connection with Database with IAM role user

1. With IAM database authentication, you use an authentication token when you connect to your database cluster.

2. An authentication token is a string of characters that you use instead of a password.

3. After you generate an authentication token, it’s valid for 15 minutes before it expires. If you try to connect using an expired token, the connection request is denied.

4. Every IAM authentication token must be accompanied by a valid signature, that uses Signature Version 4.

5. After you have a signed IAM authentication token, you can connect to an Amazon RDS database instance.

### Generating Token with AWS CLI

The authentication token consists of several hundred characters so it can be unwieldy on the command line. One way to work around this is to save the token to an environment variable, and use that variable when you connect. The following example code shows how to use the AWS CLI to get a signed authentication token using the `generated-db-auth-token` command, and store it in a `PGPASSWORD` environment variable.

In the Following example code, the parameters to the `generate-db-auth-token` command are as follows:

- **–hostname**– The host name of the DB cluster (cluster endpoint) that you want to access.
- **–port**– The port number used for connecting to your DB cluster.
- **–region**– The Region in which the DB cluster is running.
- **–username**– The database account that you want to access.

```
export RDSHOST="mypostgres-cluster.cluster-abcdefg222hq.us-east-1.rds.amazonaws.com"

export PGPASSWORD="$(aws rds generate-db-auth-token \
--hostname $RDSHOST \
--port 5432 \
--region us-east-1 \
--username mydbuser)"
```

### Connecting to the cluster using psql with the help of above step to generated token

```
psql "host=hostName port=portNumber sslmode=sslMode sslrootcert=certificateFile dbname=dbName user=userName"
```

The parameters are as follows:

- **host** – The host name of the database cluster (cluster endpoint) that you want to access.
- **port** – The port number used for connecting to your database cluster.
- **sslmode** – The SSL mode to use. For more information, see [Using SSL with a PostgreSQL database Instance](https://www.postgresql.org/docs/9.1/libpq-ssl.html) on the PostgreSQL documentation website.

It is recommended to use `sslmode` to `verify-full` or `verify-ca`. When you use `sslmode=verify-full`, the SSL connection verifies the DB instance endpoint against the endpoint in the SSL certificate.

You can use `verify-full` with RDS PostgreSQL and Aurora PostgreSQL cluster and instance endpoints.

- **sslrootcert** – The SSL certificate file that contains the public key. For more information, see [Using SSL with a PostgreSQL database Instance](https://www.postgresql.org/docs/9.1/libpq-ssl.html).
- Download the SSL/TLS certificates from [Using SSL to Encrypt a Connection to a DB Instance](http://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.SSL.html).
- **dbname** – The database that you want to access.
- **user** – The database account that you want to access.

The following example code shows using the command to connect, uses the environment variables that you set when you generated the token in the previous section.

```
psql "host=$RDSHOST port=5432 sslmode=verify-full sslrootcert=/sample_dir/rds-combined-ca-bundle.pem dbname=dbName user= mydbuser"
```

### References and links:

https://aws.amazon.com/blogs/database/using-iam-authentication-to-connect-with-pgadmin-amazon-aurora-postgresql-or-amazon-rds-for-postgresql/

[Using SSL/TLS to encrypt a connection to a DB instance - Amazon Relational Database Service](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.SSL.html)

### Support Me

**If you find my content useful or enjoy what I do, you can support me by buying me a coffee. Your support helps keep this website running and encourages me to create more content.**

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sawanchokso)

**Your generosity is greatly appreciated!**

##### Thank you for your support!💚
