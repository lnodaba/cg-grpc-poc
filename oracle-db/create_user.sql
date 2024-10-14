-- Switch to the appropriate container if needed
ALTER SESSION SET CONTAINER=FREEPDB1;

-- Check if the 'oracle' user exists; only create if it doesn't
DECLARE
  user_exists INTEGER := 0;
BEGIN
  SELECT COUNT(*) INTO user_exists FROM dba_users WHERE username = 'ORACLE';
  IF user_exists = 0 THEN
    EXECUTE IMMEDIATE 'CREATE USER oracle IDENTIFIED BY oracle';

    -- Grant necessary privileges to allow the user to connect and perform tasks
    EXECUTE IMMEDIATE 'GRANT CREATE SESSION TO oracle';     -- Allows connection
    EXECUTE IMMEDIATE 'GRANT CREATE TABLE TO oracle';       -- Allows creating tables
    EXECUTE IMMEDIATE 'GRANT CREATE VIEW TO oracle';        -- Allows creating views
    EXECUTE IMMEDIATE 'GRANT CREATE PROCEDURE TO oracle';   -- Allows creating procedures
    EXECUTE IMMEDIATE 'GRANT CREATE SEQUENCE TO oracle';    -- Allows creating sequences
    EXECUTE IMMEDIATE 'GRANT CREATE TRIGGER TO oracle';     -- Allows creating triggers

    -- Grant additional common roles
    EXECUTE IMMEDIATE 'GRANT CONNECT TO oracle';            -- Grants connection privileges
    EXECUTE IMMEDIATE 'GRANT RESOURCE TO oracle';           -- Grants resource creation privileges

    -- Grant quota on USERS tablespace
    EXECUTE IMMEDIATE 'ALTER USER oracle QUOTA UNLIMITED ON USERS';
  END IF;
END;
/
COMMIT;
