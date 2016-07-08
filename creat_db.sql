create database  users;

USE users;

DROP TABLE ring_users;

CREATE TABLE `users`.`ring_users` (
  `user_id` BIGINT UNIQUE not NULL AUTO_INCREMENT,
  `user_name` VARCHAR(200) UNIQUE NULL,
  `user_username` VARCHAR(200) UNIQUE NULL,
  `user_password` VARCHAR(200) NULL,
  PRIMARY KEY (`user_id`));

use users;
alter TABLE ring_users add COLUMN ihave int;
alter TABLE ring_users add COLUMN ihave_des TEXT(400);


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
SET NAMES 'utf8';
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


#add items

CREATE TABLE `ring_wish` (
  `wish_id` int(11) NOT NULL AUTO_INCREMENT,
  `wish_num` INT,
  `wish_description` varchar(2000) DEFAULT NULL,
  `wish_user_id` int(11) DEFAULT NULL,
  `wish_date` datetime DEFAULT NULL,
  PRIMARY KEY (`wish_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3;



DROP procedure IF EXISTS `users`.`sp_addWish`;

DELIMITER $$
USE `users`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_addWish`(
    IN p_num INT,
    IN p_description varchar(1000),
    IN p_user_id bigint
)
BEGIN

    if  (exists(SELECT 1 FROM  ring_wish WHERE ((wish_user_id = p_user_id) AND (wish_num = p_num)) ))THEN
      SELECT 'Wish number already in wish-list';
    ELSE
      SET NAMES 'utf8';
    insert into ring_wish(
        wish_num,
        wish_description,
        wish_user_id,
        wish_date
    )
    values
    (
        p_num,
        p_description,
        p_user_id,
        NOW()
    );
    END IF;
END$$

DELIMITER ;
;

# add wish list

USE `users`;
DROP procedure IF EXISTS `sp_GetWishByUser`;

DELIMITER $$
USE `users`$$
CREATE PROCEDURE `sp_GetWishByUser` (
IN p_user_id INT
)
BEGIN
    select * from ring_wish where wish_user_id = p_user_id;
END$$



USE `users`;
DROP procedure IF EXISTS `sp_Getallwish`;

DELIMITER $$
USE `users`$$
CREATE PROCEDURE `sp_Getallwish` (
IN p_user_id INT
)
BEGIN
    select distinct user_name,wish_num from ring_users join ring_wish on ring_users.user_id = ring_wish.wish_user_id;
END$$




USE `users`;
DROP procedure IF EXISTS `sp_Getallhave`;

DELIMITER $$
USE `users`$$
CREATE PROCEDURE `sp_Getallhave` (
IN p_user_id INT
)
BEGIN
    select distinct user_name,ihave from ring_users join ring_wish on ring_users.user_id = ring_wish.wish_user_id;
END$$





DELIMITER ;

ALTER DATABASE users CHARACTER SET utf8 COLLATE utf8_unicode_ci;
ALTER TABLE ring_users CONVERT TO CHARACTER SET utf8 COLLATE utf8_unicode_ci;

ALTER TABLE ring_wish CONVERT TO CHARACTER SET utf8 COLLATE utf8_unicode_ci;


DELIMITER $$
 use users;
DROP procedure IF EXISTS `users`.`sp_GetWishById`;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_GetWishById`(
IN p_wish_id INT,
In p_user_id INT
)
BEGIN
select * from ring_wish where wish_id = p_wish_id and wish_user_id = p_user_id;
END $$




DELIMITER $$
 use users;
DROP procedure IF EXISTS `users`.`sp_GetHaveById`;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_GetHaveById`(
In p_user_id INT
)
BEGIN
select ihave,ihave_des from ring_users where user_id = p_user_id;
END $$




DROP  PROCEDURE  if EXISTS `users`.`sp_GetHaveByUser`;

DELIMITER $$
CREATE  DEFINER =`root`@`localhost` PROCEDURE  `sp_GetHaveByUser`(
in p_user_id INT
)
BEGIN
SELECT * FROM  ring_users WHERE  user_id = p_user_id ;
END $$





DROP procedure IF EXISTS `users`.`sp_updateWish`;

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_updateWish`(
IN p_title INT,
IN p_description varchar(1000),
IN p_wish_id INT,
In p_user_id INT
)
BEGIN
update ring_wish set wish_num = p_title,wish_description = p_description where wish_id = p_wish_id and wish_user_id = p_user_id;
END$$

DELIMITER ;



DROP procedure IF EXISTS `users`.`sp_updateHave`;
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_updateHave`(
IN p_title INT,
IN p_description varchar(1000),
In p_user_id INT
)
BEGIN
update ring_users set ihave = p_title,ihave_des = p_description where user_id = p_user_id;
END$$






DELIMITER $$
USE `users`$$
CREATE PROCEDURE `sp_deleteWish` (
IN p_wish_id int,
IN p_user_id int
)
BEGIN
delete from ring_wish where wish_id = p_wish_id and wish_user_id = p_user_id;
END$$

DELIMITER ;

