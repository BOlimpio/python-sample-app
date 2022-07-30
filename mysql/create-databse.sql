USE db;
CREATE TABLE IF NOT EXISTS products (
    id int not null auto_increment,
    name varchar(200),
    PRIMARY KEY (id)
);

-- SET character_set_client = utf8;
-- SET character_set_connection = utf8;
-- SET character_set_results = utf8;
-- SET collation_connection = utf8_general_ci;

INSERT INTO products (name) VALUES ('Echo dot 2');