-- Create schema if not exists
CREATE SCHEMA IF NOT EXISTS filrouge;

-- Create table for filrouge
CREATE TABLE IF NOT EXISTS filrouge.server (
    userId BIGINT PRIMARY KEY,
    balance BIGINT,
    objects TEXT,
    lastPull BIGINT
);
