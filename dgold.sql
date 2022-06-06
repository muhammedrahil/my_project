/*
SQLyog Community v13.0.1 (64 bit)
MySQL - 10.4.24-MariaDB : Database - dgold
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
  `department` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`emp_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `employee` */

/*Table structure for table `leaverequest` */

DROP TABLE IF EXISTS `leaverequest`;

CREATE TABLE `leaverequest` (
  `LRid` int(10) NOT NULL AUTO_INCREMENT,
  `reason` varchar(100) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `lg_id` int(10) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `expDate` date DEFAULT NULL,
  `applyDate` date DEFAULT NULL,
  PRIMARY KEY (`LRid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `leaverequest` */

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `loginid` int(10) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `ecode` varchar(50) DEFAULT NULL,
  `usertype` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`loginid`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`loginid`,`username`,`ecode`,`usertype`) values 
(1,'DGOLDCOO','COODGD@916','COO'),
(2,'RMKMNGR','RMKMNGR@916','MANAGER'),
(3,'PMNMNGR','PMNMNGR@916','MANAGER'),
(4,'PTBMNGR','PTBMNGR@916','MANAGER'),
(5,'VLCMNGR','PTBMNGR@916','MANAGER'),
(6,'RMKDIR','RMKDIR@916','DIRECTOR'),
(7,'PMNDIR','PMNDIR@916','DIRECTOR'),
(8,'PTBDIR','PTBDIR@916','DIRECTOR'),
(9,'VLCDIR','VLCDIR@916','DIRECTOR'),
(10,'RMKEMP','RMK@916','EMPLOYEES'),
(11,'PMNEMP','PMN@916','EMPLOYEES'),
(12,'PTBEMP','PTB@916','EMPLOYEES'),
(13,'VLCEMP','VLC@916','EMPLOYEES');

/*Table structure for table `memo` */

DROP TABLE IF EXISTS `memo`;

CREATE TABLE `memo` (
  `memoid` int(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) DEFAULT NULL,
  `memo` longblob DEFAULT NULL,
  `file_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`memoid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `memo` */

/*Table structure for table `pyment` */

DROP TABLE IF EXISTS `pyment`;

CREATE TABLE `pyment` (
  `pid` int(50) NOT NULL AUTO_INCREMENT,
  `catogary` varchar(100) DEFAULT NULL,
  `moneny` varchar(100) DEFAULT NULL,
  `lg_id` int(10) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `pyment` */

/*Table structure for table `target` */

DROP TABLE IF EXISTS `target`;

CREATE TABLE `target` (
  `trid` int(10) NOT NULL AUTO_INCREMENT,
  `gold` varchar(50) DEFAULT NULL,
  `lg_id` int(10) DEFAULT NULL,
  `achive_gold` varchar(100) DEFAULT NULL,
  `Diamond` varchar(100) DEFAULT NULL,
  `achive_diamond` varchar(100) DEFAULT NULL,
  `gold_achive_pers` varchar(15) DEFAULT NULL,
  `dmn__achive_perse` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`trid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `target` */

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
