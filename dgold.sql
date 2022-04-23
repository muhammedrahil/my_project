/*
SQLyog Community v13.0.1 (64 bit)
MySQL - 5.5.20-log : Database - dgold
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`dgold` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `dgold`;

/*Table structure for table `employee` */

DROP TABLE IF EXISTS `employee`;

CREATE TABLE `employee` (
  `emp_id` int(10) NOT NULL AUTO_INCREMENT,
  `emp_name` varchar(50) DEFAULT NULL,
  `e-code` varchar(20) DEFAULT NULL,
  `branch` varchar(50) DEFAULT NULL,
  `loginid` int(10) DEFAULT NULL,
  PRIMARY KEY (`emp_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `employee` */

insert  into `employee`(`emp_id`,`emp_name`,`e-code`,`branch`,`loginid`) values 
(1,'Rahil','1234','malapuram',12),
(2,'lalu','234','malapuram',13),
(3,'asdfghh','123','malapuram',14);

/*Table structure for table `leaverequest` */

DROP TABLE IF EXISTS `leaverequest`;

CREATE TABLE `leaverequest` (
  `LRid` int(10) NOT NULL AUTO_INCREMENT,
  `reason` varchar(100) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `lg_id` int(10) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `expDate` date DEFAULT NULL,
  PRIMARY KEY (`LRid`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

/*Data for the table `leaverequest` */

insert  into `leaverequest`(`LRid`,`reason`,`status`,`lg_id`,`date`,`expDate`) values 
(1,'medical','pending',12,'2022-04-26','2022-04-30'),
(3,'medical','pending',12,'2022-04-14','2022-04-21'),
(4,'medical','pending',13,'2022-04-28','2022-04-07'),
(5,'marraige','pending',12,'2022-04-21','2022-04-20'),
(6,'medical','accept',12,'2022-04-15','2022-04-13');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `loginid` int(10) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `ecode` varchar(50) DEFAULT NULL,
  `usertype` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`loginid`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`loginid`,`username`,`ecode`,`usertype`) values 
(1,'admin','123','admin'),
(5,'maneger','123','manager'),
(12,'Rahil','1234','employee'),
(13,'lalu','234','employee'),
(14,'asdfghh','123','employee');

/*Table structure for table `pyment` */

DROP TABLE IF EXISTS `pyment`;

CREATE TABLE `pyment` (
  `pid` int(50) NOT NULL AUTO_INCREMENT,
  `catogary` varchar(100) DEFAULT NULL,
  `moneny` varchar(100) DEFAULT NULL,
  `lg_id` int(10) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`pid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `pyment` */

insert  into `pyment`(`pid`,`catogary`,`moneny`,`lg_id`,`status`) values 
(2,'TA','456',12,'accept'),
(3,'TA','1000',12,'accept');

/*Table structure for table `target` */

DROP TABLE IF EXISTS `target`;

CREATE TABLE `target` (
  `trid` int(10) NOT NULL AUTO_INCREMENT,
  `target` varchar(50) DEFAULT NULL,
  `lg_id` int(10) DEFAULT NULL,
  `achive` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`trid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `target` */

insert  into `target`(`trid`,`target`,`lg_id`,`achive`) values 
(1,'120',12,'100'),
(2,'3445',13,'455'),
(3,'2001',14,'233');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
