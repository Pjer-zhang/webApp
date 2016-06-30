create database  users;

USE users;

DROP TABLE ring_users;

CREATE TABLE `users`.`ring_users` (
  `user_id` BIGINT UNIQUE not NULL AUTO_INCREMENT,
  `user_name` VARCHAR(200) UNIQUE NULL,
  `user_username` VARCHAR(200) UNIQUE NULL,
  `user_password` VARCHAR(200) NULL,
  PRIMARY KEY (`user_id`));


DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
    IN p_name VARCHAR(20),
    IN p_username VARCHAR(20),
    IN p_password VARCHAR(20)
)
BEGIN
    if ( select exists (select 1 from ring_users where user_username = p_username) ) THEN

        select 'Username Exists !!';
      ELSEIF ( select exists (select 1 from ring_users where user_name = p_name) ) THEN

        select 'UserNeckname Exists !!';

    ELSE

        insert into ring_users
        (
            user_name,
            user_username,
            user_password
        )
        values
        (
            p_name,
            p_username,
            p_password
        );

    END IF;
END$$
DELIMITER ;


DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_validateLogin`(
IN p_username VARCHAR(200)
)
BEGIN
    select * from ring_users where user_username = p_username;
END$$
DELIMITER ;
