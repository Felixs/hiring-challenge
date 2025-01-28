-- use database
\c ctrchallenge;


-- create table for all ctr winners
DROP TABLE IF EXISTS ctr;
CREATE TABLE IF NOT EXISTS ctr (
    test_id VARCHAR(128) NOT NULL,
    content_id VARCHAR(32) NOT NULL,
    winner_id INT NOT NULL,
    ctr FLOAT NOT NULL,
    margin FLOAT NOT NULL,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (test_id)
);
-- set optional set additional indices to speed search queries
-- CREATE INDEX idx_content_id ON ctr (content_id);
-- CREATE INDEX idx_margin ON ctr (margin);

-- create view with subset of winners by over 20% margin
DROP VIEW IF EXISTS ctr_winners;
CREATE VIEW ctr_winners AS (
    SELECT
        test_id,
        content_id,
        winner_id,
        ctr,
        margin,
        processed_at
    FROM
        ctr
    WHERE 
        margin >= 0.2
);
