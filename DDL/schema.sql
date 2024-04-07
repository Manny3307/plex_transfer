CREATE DATABASE plex_transfer
    WITH
    OWNER = manny
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_AU.UTF-8'
    LC_CTYPE = 'en_AU.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

GRANT TEMPORARY, CONNECT ON DATABASE plex_transfer TO PUBLIC;
GRANT ALL ON DATABASE plex_transfer TO plex_app_user;


CREATE USER plex_app_user WITH PASSWORD 'plexuser';
GRANT ALL PRIVILEGES ON DATABASE plex_transfer to plex_app_user;

CREATE TABLE tbl_File_Batch_Info(
	file_id  		INT	GENERATED ALWAYS AS IDENTITY,
	file_name		VARCHAR(1000) NOT NULL,
	batch_id		VARCHAR(20) NOT NULL,
	file_date_time	TIMESTAMP,
    is_executed     BOOLEAN
)


INSERT INTO tbl_File_Batch_Info (file_name, batch_id, file_date_time, is_executed)
VALUES ('test1','d6btg4cqpb',CURRENT_TIMESTAMP, 0)

INSERT INTO tbl_File_Batch_Info (file_name, batch_id, file_date_time, is_executed)
VALUES('test2','d6btg4cqpb',CURRENT_TIMESTAMP, 0)



