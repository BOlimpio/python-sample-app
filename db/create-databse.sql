USE Backoffice;
CREATE TABLE user (
    id integer not null auto_increment,
    is_active boolean not ,
    created_date datetime not null,
    name varchar(200)
);

SET character_set_client = utf8;
SET character_set_connection = utf8;
SET character_set_results = utf8;
SET collation_connection = utf8_general_ci;

INSERT INTO user (is_active, created_date, name) VALUES (1, "2022-05-05", 'Edward Elric');