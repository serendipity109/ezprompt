CREATE DATABASE ezprompt;

USE ezprompt;

CREATE TABLE `users` (
  `_id` varchar(24) NOT NULL DEFAULT '',
  `username` varchar(24) NOT NULL DEFAULT '',
  `password` varchar(24) NOT NULL DEFAULT '',
  `credits` int(100) NOT NULL DEFAULT 100,
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP(),
  PRIMARY KEY (`_id`),
  KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `ezprompt`.`users` (`_id`, `username`, `password`, `credits`, `create_time`) VALUES ('1', 'admin', 'wowo0825', '100', '2023-05-12 01:22:07');

CREATE TABLE `trans` (
  `_id` varchar(24) NOT NULL DEFAULT '',
  `username` varchar(100) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `img_url` varchar(100) DEFAULT NULL,
  `elapsed_time` float(50) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`_id`),
  FOREIGN KEY (`username`) REFERENCES users(`username`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
