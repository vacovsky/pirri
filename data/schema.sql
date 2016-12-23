CREATE DATABASE `pirri` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;
CREATE TABLE `dripnodes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `gph` int(11) NOT NULL DEFAULT '0',
  `sid` int(11) NOT NULL DEFAULT '0',
  `count` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
CREATE TABLE `gpio_pins` (
  `gpio` int(11) NOT NULL,
  `notes` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`gpio`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
CREATE TABLE `history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sid` int(11) NOT NULL DEFAULT '0',
  `schedule_id` int(11) NOT NULL DEFAULT '0',
  `duration` int(11) NOT NULL DEFAULT '0',
  `starttime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=223 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
CREATE TABLE `schedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `startdate` int(11) NOT NULL DEFAULT '18990101',
  `enddate` int(11) DEFAULT NULL,
  `sunday` int(11) NOT NULL DEFAULT '0',
  `monday` int(11) NOT NULL DEFAULT '0',
  `tuesday` int(11) NOT NULL DEFAULT '0',
  `wednesday` int(11) NOT NULL DEFAULT '0',
  `thursday` int(11) NOT NULL DEFAULT '0',
  `friday` int(11) NOT NULL DEFAULT '0',
  `saturday` int(11) NOT NULL DEFAULT '0',
  `station` int(11) NOT NULL DEFAULT '0',
  `starttime` int(11) NOT NULL DEFAULT '0',
  `duration` int(11) NOT NULL DEFAULT '0',
  `repeating` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
CREATE TABLE `settings` (
  `idsettings` int(11) NOT NULL AUTO_INCREMENT,
  `openweather_key` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `zipcode` int(11) DEFAULT NULL,
  `weather_units` varchar(45) CHARACTER SET utf8 NOT NULL DEFAULT 'imperial',
  `rabbitmq_addr` varchar(45) CHARACTER SET utf8 NOT NULL DEFAULT 'localhost',
  `rabbitmq_user` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `rabbitmq_pass` varchar(45) CHARACTER SET utf8 DEFAULT NULL,
  `pirri_admin_pass` varchar(45) CHARACTER SET utf8 NOT NULL DEFAULT 'pirri',
  `pirri_admin_user` varchar(45) CHARACTER SET utf8 NOT NULL DEFAULT 'admin',
  `adjust_for_current_weather` bit(1) NOT NULL DEFAULT b'0',
  `adjust_for_forecase_weather` bit(1) NOT NULL DEFAULT b'0',
  `gpio_onstate` int(11) NOT NULL DEFAULT '0',
  `gpio_offstate` int(11) NOT NULL DEFAULT '1',
  `use_newrelic` bit(1) NOT NULL DEFAULT b'0',
  `utc_offset` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`idsettings`),
  UNIQUE KEY `idsettings_UNIQUE` (`idsettings`),
  UNIQUE KEY `pirri_admin_user_UNIQUE` (`pirri_admin_user`),
  UNIQUE KEY `pirri_admin_pass_UNIQUE` (`pirri_admin_pass`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
CREATE TABLE `stations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `gpio` int(11) NOT NULL DEFAULT '0',
  `notes` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `common` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
