
## Oracle Database User Setup via Docker Compose

The Docker Compose setup is configured to automatically create a user in the Oracle database during startup using the `create_user.sql` script. However, if for any reason the user is not created successfully, you can manually create the user following the steps outlined below.

### Automatic User Creation with Docker Compose

When you run the Docker Compose setup, the `create_user.sql` script located at `./oracle-db/create_user.sql` is executed automatically. This script contains the necessary SQL commands to create the user `oracle` and grant appropriate privileges.

**To start the Oracle database with Docker Compose:**

1. Ensure your `docker-compose.yml` file is set up correctly with the Oracle service, including the volume mount for the SQL script:
   ```yaml
   oracle-db:
     image: container-registry.oracle.com/database/free:23.4.0.0
     container_name: oracle-db
     ports:
       - "1521:1521"
     environment:
       - ORACLE_ALLOW_REMOTE=true
       - ORACLE_ENABLE_XDB=true
       - ORACLE_CHARACTERSET=AL32UTF8
       - ORACLE_PDB=FREEPDB1
     networks:
       - my-network
     volumes:
       - ./oracle-db/create_user.sql:/opt/oracle/scripts/startup/create_user.sql
   ```

2. Run the following command to start the services:
   ```bash
   docker-compose up
   ```

3. Monitor the logs to ensure that the database starts correctly and that the user is created:
   ```bash
   docker-compose logs -f oracle-db
   ```

### Manual User Creation

If the user `oracle` is not created automatically, you can manually create the user by following these steps:

1. **Connect to the Oracle Database**:
   Open your terminal and connect to the Oracle database using the following command:
   ```bash
   sqlplus sys/oracle as sysdba
   ```

2. **Switch to the Appropriate Container (if using PDBs)**:
   If your database setup uses Pluggable Databases (PDBs), switch to the appropriate PDB (in this case, `FREEPDB1`):
   ```sql
   ALTER SESSION SET CONTAINER=FREEPDB1;
   ```

3. **Create a New User**:
   Run the following SQL command to create a user named `oracle` with the password `oracle`:
   ```sql
   CREATE USER oracle IDENTIFIED BY oracle;
   ```

4. **Grant Necessary Privileges**:
   To allow the user to connect and perform tasks, execute the following commands:
   ```sql
   GRANT CREATE SESSION TO oracle;     -- Allows connection
   GRANT CREATE TABLE TO oracle;       -- Allows creating tables
   GRANT CREATE VIEW TO oracle;        -- Allows creating views
   GRANT CREATE PROCEDURE TO oracle;   -- Allows creating procedures
   GRANT CREATE SEQUENCE TO oracle;    -- Allows creating sequences
   GRANT CREATE TRIGGER TO oracle;     -- Allows creating triggers
   GRANT CONNECT TO oracle;            -- Grants connection privileges
   GRANT RESOURCE TO oracle;           -- Grants resource creation privileges
   ```

5. **Commit the Changes**:
   After granting the privileges, commit the changes to make them permanent:
   ```sql
   COMMIT;
   ```

6. **Verify the Privileges**:
   To verify that the privileges were granted successfully, run the following command:
   ```sql
   SELECT * FROM USER_SYS_PRIVS WHERE USERNAME = 'ORACLE';
   ```