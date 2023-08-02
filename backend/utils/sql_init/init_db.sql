CREATE DATABASE ezprompt;

USE ezprompt;

CREATE TABLE `user` (
  `_id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` varchar(50) NOT NULL DEFAULT '',
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `user_info` (
  `_id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` varchar(50) NOT NULL DEFAULT '',
  `password` varchar(10) NOT NULL DEFAULT '',
  `credits` int NOT NULL DEFAULT 0,
  `token` varchar(300) NOT NULL DEFAULT '',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP(),
  `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP(),
  UNIQUE KEY `user_id` (`user_id`),
  FOREIGN KEY (`user_id`) REFERENCES user(`user_id`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `transaction` (
  `_id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` varchar(50) DEFAULT NULL,
  `prompt_id` varchar(20) DEFAULT NULL,
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP(),
  UNIQUE KEY `prompt_id` (`prompt_id`),
  FOREIGN KEY (`user_id`) REFERENCES user(`user_id`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `image` (
  `_id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` varchar(50) DEFAULT NULL,
  `prompt_id` varchar(20) DEFAULT NULL,
  `img` varchar(100) DEFAULT NULL,
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP(),
  FOREIGN KEY (`user_id`) REFERENCES user(`user_id`),
  FOREIGN KEY (`prompt_id`) REFERENCES transaction(`prompt_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE DATABASE requests;

USE requests;

CREATE TABLE `records` (
   `_id` INT AUTO_INCREMENT PRIMARY KEY,
   `user_id` VARCHAR(1000) DEFAULT NULL,
   `prompt` TEXT DEFAULT NULL,
   `mode` VARCHAR(10) DEFAULT NULL,
   `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
