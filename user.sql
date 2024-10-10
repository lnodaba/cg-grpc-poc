sqlplus sys as sysdba

-- Switch to the appropriate container if needed (for PDBs)
ALTER SESSION SET CONTAINER=FREEPDB1;

-- Create the user 'default_user' with a specified password
CREATE USER default_user IDENTIFIED BY default_password;

-- Grant necessary privileges to allow the user to connect and perform tasks
GRANT CREATE SESSION TO default_user;     -- Allows connection
GRANT CREATE TABLE TO default_user;       -- Allows creating tables
GRANT CREATE VIEW TO default_user;        -- Allows creating views
GRANT CREATE PROCEDURE TO default_user;   -- Allows creating procedures
GRANT CREATE SEQUENCE TO default_user;    -- Allows creating sequences
GRANT CREATE TRIGGER TO default_user;     -- Allows creating triggers

-- Grant additional common roles
GRANT CONNECT TO default_user;            -- Grants connection privileges
GRANT RESOURCE TO default_user;           -- Grants resource creation privileges

-- Commit the changes
COMMIT;

-- Verify the privileges granted to 'default_user'
SELECT * FROM USER_SYS_PRIVS WHERE USERNAME = 'DEFAULT_USER';



CREATE PLUGGABLE DATABASE ORACLE 
ADMIN USER oracle IDENTIFIED BY oracle 
FILE_NAME_CONVERT = ('pdbseed', 'ORACLE');
