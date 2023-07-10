CREATE DATABASE ezprompt;

USE ezprompt;

CREATE TABLE `users` (
  `_id` varchar(10) NOT NULL DEFAULT '',
  `user_id` varchar(30) NOT NULL DEFAULT '',
  `password` varchar(24) NOT NULL DEFAULT '',
  `credits` int NOT NULL DEFAULT 100,
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP(),
  PRIMARY KEY (`_id`),
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `ezprompt`.`users` (`_id`, `user_id`, `password`, `credits`, `create_time`) VALUES ('1', 'admin', 'wowo0825', 100, '2023-05-12 01:22:07');

CREATE TABLE `trans` (
  `_id` varchar(10) NOT NULL DEFAULT '',
  `user_id` varchar(30) DEFAULT NULL,
  `prompt_id` varchar(10) DEFAULT NULL,
  `img1` varchar(1000) DEFAULT NULL,
  `img2` varchar(1000) DEFAULT NULL,
  `img3` varchar(1000) DEFAULT NULL,
  `img4` varchar(1000) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`_id`),
  UNIQUE KEY `prompt_id` (`prompt_id`),
  FOREIGN KEY (`user_id`) REFERENCES users(`user_id`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `imgs` (
  `_id` varchar(10) NOT NULL DEFAULT '',
  `user_id` varchar(30) DEFAULT NULL,
  `prompt_id` varchar(10) DEFAULT NULL,
  `img` varchar(1000) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`_id`),
  FOREIGN KEY (`user_id`) REFERENCES users(`user_id`),
  FOREIGN KEY (`prompt_id`) REFERENCES trans(`prompt_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
