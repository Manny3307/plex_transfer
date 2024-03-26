select * from tbl_File_Batch_info ORDER BY file_date_time DESC LIMIT 1;

SELECT
DATE_PART('Day', CURRENT_TIMESTAMP - '2024-03-20 21:43:19.258875'::TIMESTAMP) * 24
+ (DATE_PART('min', CURRENT_TIMESTAMP) - DATE_PART('min', '2024-03-20 21:43:19.258875'::TIMESTAMP) 
) AS hour_diff;

SELECT CURRENT_TIMESTAMP - DATE_PART('Hour', '2024-03-20 21:43:19.258875'::TIMESTAMP)

SELECT DATE_PART('min', CURRENT_TIMESTAMP - '2024-03-20 21:43:19.258875') as date_diff

select abs(extract(day from CURRENT_TIMESTAMP - '2024-03-20 21:43:19.258875')) from tbl_File_Batch_info;


TRUNCATE TABLE tbl_File_Batch_info

SELECT * FROM tbl_File_Batch_info


SELECT DATE_PART('min', CURRENT_TIMESTAMP - '2024-03-20 21:43:19.258875') as date_diff
SELECT DATE_PART('min', '2024-03-21 00:10:19.258875'::TIMESTAMP - '2024-03-20 23:43:19.258875'::TIMESTAMP) as date_diff


SELECT file_name FROM tbl_File_Batch_info WHERE file_name NOT IN ('48H with ME.mp4',
'5 orgasm for 10 minutes.mp4',
'BOUND TO PLEASE 05.mp4',
'BOUND TO PLEASE 10.mp4',
'Educating Tricia.mp4',
'faphouse.com-nude-on-the-beach-p1080.mp4',
'Florence Guerin - Le declic.mp4',
'Four College Girls Play a Strip Word Game.mp4',
'Pornoshop della Settima Strada.mp4',
'Retro 208.mp4',
'Rich bitch humiliation.mp4',
'Scream for Vengeance.mp4',
'sex partner decided by bottle spin.mp4',
'slave for couple.mp4',
'X019.mp4', 'test1', 'test2', 'test3', 'test4')

select unnest(array[1, 2, 3, 4, 5, 6, 7, 8, 9]) 
EXCEPT 
select distinct seq_id from my_value;

SELECT UNNEST(ARRAY(['48H with ME.mp4',
'5 orgasm for 10 minutes.mp4',
'BOUND TO PLEASE 05.mp4',
'BOUND TO PLEASE 10.mp4',
'Educating Tricia.mp4',
'faphouse.com-nude-on-the-beach-p1080.mp4',
'Florence Guerin - Le declic.mp4',
'Four College Girls Play a Strip Word Game.mp4',
'Pornoshop della Settima Strada.mp4',
'Retro 208.mp4',
'Rich bitch humiliation.mp4',
'Scream for Vengeance.mp4',
'sex partner decided by bottle spin.mp4',
'slave for couple.mp4',
'X019.mp4', 'test1', 'test2', 'test3', 'test4']))
EXCEPT 
SELECT file_name FROM tbl_File_Batch_info




SELECT 
    v 
FROM
    (
    VALUES
        ('something_a'),
        ('something_b'),
        ('something_c'),
        ('something_d')
    ) AS vs(v)
WHERE
    v NOT IN 
    (SELECT 
        appropriate_column 
    FROM
        some_table
    );
	
SELECT v FROM (
    VALUES
('48H with ME.mp4'),
('5 orgasm for 10 minutes.mp4'),
('BOUND TO PLEASE 05.mp4'),
('BOUND TO PLEASE 10.mp4'),
('Educating Tricia.mp4'),
('faphouse.com-nude-on-the-beach-p1080.mp4'),
('Florence Guerin - Le declic.mp4'),
('Four College Girls Play a Strip Word Game.mp4'),
('Pornoshop della Settima Strada.mp4'),
('Retro 208.mp4'),
('Rich bitch humiliation.mp4'),
('Scream for Vengeance.mp4'),
('sex partner decided by bottle spin.mp4'),
('slave for couple.mp4'),
('X019.mp4'), 
('test1'), 
('test2'), 
('test3'), 
('test4')) AS vs(v)
WHERE
    v NOT IN 
    (SELECT file_name FROM tbl_File_Batch_info)





SELECT * FROM tbl_File_Batch_info

DELETE FROM tbl_File_Batch_info WHERE file_id IN (50, 51)



SELECT file_name, COUNT(file_name)
FROM tbl_File_Batch_info
GROUP BY file_name
HAVING COUNT(file_name) > 1


select * from tbl_File_Batch_info WHERE file_name = 'She BEGS me to stop intense female orgasm.mp4'
select * from tbl_File_Batch_info WHERE file_name = 'Tied up teased and made to cum.mp4' LIMIT 2


SELECT DISTINCT(file_name) from tbl_File_Batch_info WHERE file_name IN (
SELECT file_name
FROM tbl_File_Batch_info
GROUP BY file_name
HAVING COUNT(file_name) > 1)


SELECT file_id, file_name FROM tbl_File_Batch_info AS dp_file USING tbl_File_Batch_info AS corr_file
WHERE 
dp_file.file_id = corr_file.file_id
AND dp_file.file_name = corr_file.file_name




SELECT file_name, COUNT(file_name)
FROM tbl_File_Batch_info
GROUP BY file_name
HAVING COUNT(file_name) > 1


SELECT * FROM tbl_File_Batch_info WHERE file_name = 'can she handle this overstimulation     loud intensexa0orgasm.mp4'

SELECT * FROM tbl_File_Batch_info WHERE file_name LIKE 'can she handle%'
SELECT DISTINCT batch_id from tbl_File_Batch_info
can she handle this overstimulation     loud intense orgasm.mp4
can she handle this overstimulation     loud intensexa0orgasm.mp4

DELETE FROM tbl_File_Batch_info WHERE file_id IN (538, 431)

DELETE FROM tbl_File_Batch_info WHERE file_id IN (
SELECT DISTINCT dp_file.file_name, dp_file.file_id, dp_file.batch_id 
	FROM tbl_File_Batch_info AS dp_file 
	INNER JOIN tbl_File_Batch_info AS corr_file ON dp_file.file_name = corr_file.file_name
WHERE 
dp_file.file_id > corr_file.file_id
GROUP BY dp_file.file_name, dp_file.file_id, dp_file.batch_id   
ORDER BY dp_file.file_name)



SELECT * FROM tbl_File_Batch_info WHERE batch_id IN ('rw2db1dgqx', 'bm1hoe4iyp')

BEGIN TRANSACTION

DELETE FROM tbl_File_Batch_info WHERE file_id IN (
SELECT DISTINCT  dp_file.file_id
	FROM tbl_File_Batch_info AS dp_file 
	INNER JOIN tbl_File_Batch_info AS corr_file ON dp_file.file_name = corr_file.file_name
WHERE 
dp_file.file_id > corr_file.file_id
GROUP BY  dp_file.file_id)

COMMIT TRANSACTION


ROLLBACK TRANSACTION


SELECT * FROM tbl_File_Batch_info WHERE file_name = 'Captured Milfs Desperately Ticklish Pussy Part 2.mp4'

SELECT file_name FROM tbl_File_Batch_info WHERE is_executed = False

TRUNCATE TABLE tbl_File_Batch_info

UPDATE tbl_File_Batch_info SET is_executed = False WHERE file_id IN (SELECT file_id FROM tbl_File_Batch_info WHERE file_id NOT IN (533,534))
SELECT file_id FROM tbl_File_Batch_info WHERE file_id NOT IN (533,534)

SELECT * FROM tbl_File_Batch_info
ORDER BY file_date_time DESC

SELECT * FROM tbl_File_Batch_info WHERE is_executed = False

SELECT * FROM tbl_File_Batch_info ORDER BY file_name DESC

UPDATE tbl_File_Batch_info SET is_executed = True WHERE file_id IN (SELECT file_id FROM tbl_File_Batch_info WHERE file_id < 652)

SELECT file_id FROM tbl_File_Batch_info WHERE file_id < 652

SELECT * FROM tbl_File_Batch_info WHERE is_executed = True

UPDATE tbl_File_Batch_info SET file_name = 'UNAID girl flew NY Vegas for THIS   Squirting Massage.. Real Wet Amateur.mp4' WHERE file_id = 652