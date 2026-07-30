/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
-- Current Database: `rostek_gateway`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `rostek_gateway` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci */;

USE `rostek_gateway`;

--
-- Table structure for table `call_box_error`
--

DROP TABLE IF EXISTS `call_box_error`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `call_box_error` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device_id` varchar(50) NOT NULL,
  `module` varchar(50) NOT NULL,
  `code` int(11) NOT NULL,
  `desc` varchar(255) NOT NULL,
  `timestamp` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `device_id` (`device_id`),
  CONSTRAINT `call_box_error_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `device` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=795050 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `call_box_error`
--

LOCK TABLES `call_box_error` WRITE;
/*!40000 ALTER TABLE `call_box_error` DISABLE KEYS */;
INSERT INTO `call_box_error` VALUES (792961,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710467511),(792962,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710467511),(793037,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710467522),(793038,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710467522),(793099,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710467532),(793101,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710467532),(793296,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710467547),(793299,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710467548),(793894,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710467601),(793895,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710467606),(793896,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710467628),(793897,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710467633),(793898,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710467639),(793899,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710467644),(793900,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710467649),(793901,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710467654),(793902,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710467680),(793903,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710467685),(793908,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1710468470),(793912,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710468847),(793913,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710468852),(793914,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710468858),(793915,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710468863),(793917,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710468924),(793918,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710468926),(793920,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710468953),(793921,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710468958),(793924,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710468999),(793925,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710469004),(793926,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710469025),(793928,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710469029),(793929,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710469046),(793930,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710469049),(793944,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710469081),(793945,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710469086),(793964,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710469132),(793965,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710469137),(794070,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710469376),(794071,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710469381),(794325,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710470050),(794327,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710470052),(794399,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1401,'Can not call IP to server: 172.21.99.23',1710470200),(794610,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1710554021),(794613,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1710571976),(794614,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1710733252),(794616,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1710811084),(794617,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1710827388),(794623,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1711087461),(794627,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1711336350),(794628,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1711336627),(794629,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1711337625),(794630,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1711346538),(794631,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1711347103),(794632,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1711347124),(794633,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1711347170),(794636,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1711418199),(794638,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1711501638),(794639,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1711502023),(794641,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1712622403),(794642,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1712622832),(794650,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1725522445),(794652,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1725523388),(794653,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1725523429),(794658,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1725591602),(794659,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1725591602),(794660,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1725591603),(794661,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1725591604),(794662,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1725591605),(794663,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1725591606),(794664,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1725591606),(794665,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1725591607),(794666,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1725591607),(794667,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1725591609),(794668,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1725591610),(794672,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1725699793),(794673,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1725699798),(794674,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1725705733),(794675,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1725705736),(794676,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1725705739),(794695,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1726048025),(794696,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1726048108),(794697,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1726100582),(794698,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1726100587),(794700,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1726131096),(794701,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1726131096),(794702,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1726131097),(794703,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1726131098),(794715,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1726339097),(794720,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1726446812),(794721,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1726446815),(794722,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1726447714),(794723,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1726447714),(794724,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1726454654),(794725,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1726469183),(794732,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1726623258),(794733,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1726623348),(794734,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.16',1726623351),(794773,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1728919522),(794776,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1729071395),(794777,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1729071618),(794778,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1729071624),(794779,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1729071629),(794780,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1729071664),(794781,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1729071666),(794782,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1729071680),(794783,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1729071682),(794784,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1729071804),(794785,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1729071806),(794786,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1729071811),(794787,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1729071990),(794788,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1729071993),(794789,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1729072079),(794790,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1729072128),(794791,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1729072190),(794792,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1729072550),(794799,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1729302886),(794800,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1729302888),(794801,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1729302890),(794802,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1729303375),(794803,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1729303424),(794804,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1729303841),(794805,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1729303936),(794806,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1729304185),(794807,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1729304203),(794808,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1729304217),(794809,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1729304227),(794810,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1729316467),(794819,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1729862923),(794820,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1729862925),(794821,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1729862930),(794822,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1729862932),(794826,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1730080321),(794827,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1730080464),(794829,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1730425514),(794833,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1731320010),(794835,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1731468581),(794836,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1731479872),(794847,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1400,'Can not connect device device5489411b-8562-4ac2-826f-e2fccbb142b3 with protocol mc_protocol',1732075423),(794855,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733459594),(794856,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733459643),(794857,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733459669),(794858,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733459674),(794859,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733459725),(794861,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733611445),(794862,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733655259),(794863,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733687663),(794864,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733687670),(794865,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733687719),(794866,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733687729),(794867,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733687732),(794868,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733687773),(794869,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733687776),(794870,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733687941),(794871,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733687943),(794872,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733687985),(794873,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733688017),(794874,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733688047),(794875,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733688152),(794876,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733688173),(794877,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733688268),(794878,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733688279),(794879,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733688401),(794880,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733688528),(794881,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733688607),(794882,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733688752),(794883,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733688763),(794884,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733689011),(794885,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733689013),(794886,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733689020),(794887,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733689022),(794888,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733689054),(794889,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733689074),(794890,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733689076),(794891,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733689085),(794892,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733690015),(794893,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733690034),(794894,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733690036),(794895,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733690039),(794896,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733690045),(794897,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733708746),(794898,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733783155),(794899,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733783313),(794900,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733783393),(794901,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1733783480),(794915,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1400,'Can not connect device device5489411b-8562-4ac2-826f-e2fccbb142b3 with protocol mc_protocol',1734946997),(794916,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1735061215),(794917,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1735069863),(794923,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1400,'Can not connect device device5489411b-8562-4ac2-826f-e2fccbb142b3 with protocol mc_protocol',1735496063),(794929,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1735546687),(794939,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1400,'Can not connect device device5489411b-8562-4ac2-826f-e2fccbb142b3 with protocol mc_protocol',1735934598),(794941,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1400,'Can not connect device device5489411b-8562-4ac2-826f-e2fccbb142b3 with protocol mc_protocol',1736080045),(794946,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1736910908),(794947,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1736963997),(794948,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1736964020),(794949,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1736964027),(794950,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1736964254),(794951,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1737316976),(794952,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1737317194),(794953,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1737317199),(794954,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1737317327),(794955,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1400,'Can not connect device device5489411b-8562-4ac2-826f-e2fccbb142b3 with protocol mc_protocol',1737352724),(794956,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1400,'Can not connect device device5489411b-8562-4ac2-826f-e2fccbb142b3 with protocol mc_protocol',1737357634),(794957,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1737429216),(794958,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1737429821),(794959,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1738570464),(794960,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1738638703),(794961,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1739562766),(794962,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1739563026),(794963,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1739563028),(794964,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1739563065),(794965,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1739563476),(794966,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1739563481),(794967,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1739563484),(794968,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1739563547),(794969,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1739563815),(794970,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1739563826),(794971,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1739563828),(794972,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1739621769),(794973,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1739621891),(794974,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1739621963),(794975,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1739621966),(794976,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1739622129),(794977,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1739622134),(794978,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740458177),(794979,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740458183),(794980,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740458188),(794981,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740458193),(794982,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740465150),(794983,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740480175),(794984,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740480181),(794985,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740486031),(794986,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740486088),(794987,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740486093),(794988,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740486125),(794989,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740486596),(794990,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740486601),(794991,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740486606),(794992,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740486612),(794993,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740486617),(794994,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740488172),(794995,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740488177),(794996,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740488522),(794997,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740488551),(794998,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740488605),(794999,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740488855),(795000,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740490004),(795001,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740490009),(795002,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740490015),(795003,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740490020),(795004,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740490522),(795005,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740490540),(795006,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740490545),(795007,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740490933),(795008,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740491297),(795009,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740491302),(795010,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740492090),(795011,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740492098),(795012,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740492118),(795013,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740492126),(795014,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740492142),(795015,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740492148),(795016,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740492503),(795017,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740492508),(795018,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740492513),(795019,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740492530),(795020,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1740492537),(795021,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1400,'Can not connect device device5489411b-8562-4ac2-826f-e2fccbb142b3 with protocol mc_protocol',1742029882),(795022,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1744416926),(795023,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1744416945),(795024,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1744416950),(795025,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1744437759),(795026,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1744437765),(795027,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1744437773),(795028,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1744437778),(795029,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1744437783),(795030,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1744437788),(795031,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1744437793),(795032,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1744890141),(795033,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1401,'Can not call IP to server: 172.21.99.23',1744890269),(795034,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1400,'Can not connect device device5489411b-8562-4ac2-826f-e2fccbb142b3 with protocol mc_protocol',1746373698),(795035,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1400,'Can not connect device device5489411b-8562-4ac2-826f-e2fccbb142b3 with protocol mc_protocol',1746374380),(795036,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1400,'Can not connect device device5489411b-8562-4ac2-826f-e2fccbb142b3 with protocol mc_protocol',1746806761),(795037,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1400,'Can not connect device deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37 with protocol modbus_rtu',1746861590),(795038,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1400,'Can not connect device deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37 with protocol modbus_rtu',1746861590),(795039,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1400,'Can not connect device deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37 with protocol modbus_rtu',1746861614),(795040,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1400,'Can not connect device deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37 with protocol modbus_rtu',1746861621),(795041,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1400,'Can not connect device deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37 with protocol modbus_rtu',1746861627),(795042,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1400,'Can not connect device deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37 with protocol modbus_rtu',1746861652),(795043,'deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','call_box',1400,'Can not connect device deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37 with protocol modbus_rtu',1746861658),(795044,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1400,'Can not connect device device5489411b-8562-4ac2-826f-e2fccbb142b3 with protocol mc_protocol',1746964603),(795045,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1400,'Can not connect device device5489411b-8562-4ac2-826f-e2fccbb142b3 with protocol mc_protocol',1746965171),(795046,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1400,'Can not connect device device5489411b-8562-4ac2-826f-e2fccbb142b3 with protocol mc_protocol',1746965261),(795047,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1400,'Can not connect device device5489411b-8562-4ac2-826f-e2fccbb142b3 with protocol mc_protocol',1746965356),(795048,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1400,'Can not connect device device5489411b-8562-4ac2-826f-e2fccbb142b3 with protocol mc_protocol',1746965597),(795049,'device5489411b-8562-4ac2-826f-e2fccbb142b3','call_box',1400,'Can not connect device device5489411b-8562-4ac2-826f-e2fccbb142b3 with protocol mc_protocol',1746965763);
/*!40000 ALTER TABLE `call_box_error` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device`
--

DROP TABLE IF EXISTS `device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `device` (
  `id` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `device_type` varchar(50) DEFAULT NULL,
  `group_id` varchar(50) NOT NULL,
  `modified` datetime NOT NULL,
  `protocol_type` varchar(50) NOT NULL,
  `protocol` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`protocol`)),
  `register` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`register`)),
  `device` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`device`)),
  PRIMARY KEY (`id`,`name`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `group_id` (`group_id`),
  CONSTRAINT `device_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `device_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device`
--

LOCK TABLES `device` WRITE;
/*!40000 ALTER TABLE `device` DISABLE KEYS */;
INSERT INTO `device` VALUES ('device5489411b-8562-4ac2-826f-e2fccbb142b3','line tu dong','call_box','4a7a86d1-9e53-4edb-a78e-0a6df1baaf69','2024-03-14 03:09:22','mc_protocol','{\"ip\": \"172.21.99.220\", \"port\": 3000, \"plc_series\": \"Q\", \"comm_type\": \"binary\"}','[{\"name\": \"button_1\", \"addr\": 15}, {\"name\": \"b1_id\", \"addr\": 16}, {\"name\": \"fb1\", \"addr\": 17}, {\"name\": \"button_2\", \"addr\": 11}, {\"name\": \"b2_id\", \"addr\": 12}, {\"name\": \"fb2\", \"addr\": 13}, {\"name\": \"button_3\", \"addr\": 18}, {\"name\": \"b3_id\", \"addr\": 19}, {\"name\": \"fb3\", \"addr\": 20}, {\"name\": \"button_4\", \"addr\": 21}, {\"name\": \"b4_id\", \"addr\": 22}, {\"name\": \"fb4\", \"addr\": 40}, {\"name\": \"button_5\", \"addr\": 23}, {\"name\": \"b5_id\", \"addr\": 24}, {\"name\": \"fb5\", \"addr\": 41}, {\"name\": \"button_6\", \"addr\": 25}, {\"name\": \"b6_id\", \"addr\": 26}, {\"name\": \"fb6\", \"addr\": 43}]','{\"max_retry\": 2, \"enable\": true, \"server_ip\": \"172.21.99.23\", \"server_port\": 8080, \"username\": \"admin\", \"password\": \"admin\", \"uptime_send_time\": 10, \"timeout_call_api\": 5, \"timeout_when_disconnect\": 15, \"number_of_button\": 15, \"auto_feedback\": false}'),('deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37','rostek_callbox','call_box','4a7a86d1-9e53-4edb-a78e-0a6df1baaf69','2024-09-18 02:38:40','modbus_rtu','{\"baudrate\": 9600, \"parity_bit\": \"none\", \"byte_len\": 8, \"stop_bit_len\": 1, \"unit_id\": 4, \"timeout\": 1, \"com\": \"rs485-1\"}','[{\"name\": \"button_1\", \"addr\": 4097}, {\"name\": \"b1_id\", \"addr\": 4098}, {\"name\": \"fb1\", \"addr\": 4099}, {\"name\": \"button_2\", \"addr\": 4100}, {\"name\": \"b2_id\", \"addr\": 4101}, {\"name\": \"fb2\", \"addr\": 4102}, {\"name\": \"button_3\", \"addr\": 4103}, {\"name\": \"b3_id\", \"addr\": 4104}, {\"name\": \"fb3\", \"addr\": 4105}, {\"name\": \"button_4\", \"addr\": 4106}, {\"name\": \"b4_id\", \"addr\": 4107}, {\"name\": \"fb4\", \"addr\": 4108}, {\"name\": \"button_5\", \"addr\": 4109}, {\"name\": \"b5_id\", \"addr\": 4110}, {\"name\": \"fb5\", \"addr\": 4111}, {\"name\": \"button_6\", \"addr\": 4112}, {\"name\": \"b6_id\", \"addr\": 4113}, {\"name\": \"fb6\", \"addr\": 4114}, {\"name\": \"button_7\", \"addr\": 4115}, {\"name\": \"b7_id\", \"addr\": 4116}, {\"name\": \"fb7\", \"addr\": 4117}, {\"name\": \"button_8\", \"addr\": 4118}, {\"name\": \"b8_id\", \"addr\": 4119}, {\"name\": \"fb8\", \"addr\": 4120}, {\"name\": \"button_9\", \"addr\": 4121}, {\"name\": \"b9_id\", \"addr\": 4122}, {\"name\": \"fb9\", \"addr\": 4123}, {\"name\": \"button_10\", \"addr\": 4124}, {\"name\": \"b10_id\", \"addr\": 4125}, {\"name\": \"fb10\", \"addr\": 4126}, {\"name\": \"button_11\", \"addr\": 4127}, {\"name\": \"b11_id\", \"addr\": 4128}, {\"name\": \"fb11\", \"addr\": 4129}, {\"name\": \"button_12\", \"addr\": 4130}, {\"name\": \"b12_id\", \"addr\": 4131}, {\"name\": \"fb12\", \"addr\": 4132}, {\"name\": \"button_13\", \"addr\": 4133}, {\"name\": \"b13_id\", \"addr\": 4134}, {\"name\": \"fb13\", \"addr\": 4135}, {\"name\": \"button_14\", \"addr\": 4136}, {\"name\": \"b14_id\", \"addr\": 4137}, {\"name\": \"fb14\", \"addr\": 4138}, {\"name\": \"button_15\", \"addr\": 4139}, {\"name\": \"b15_id\", \"addr\": 4140}, {\"name\": \"fb15\", \"addr\": 4141}]','{\"max_retry\": 2, \"enable\": true, \"server_ip\": \"172.21.99.23\", \"server_port\": 8080, \"username\": \"admin\", \"password\": \"admin\", \"uptime_send_time\": 10, \"timeout_call_api\": 5, \"timeout_when_disconnect\": 15, \"number_of_button\": 15, \"auto_feedback\": false}');
/*!40000 ALTER TABLE `device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device_group`
--

DROP TABLE IF EXISTS `device_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `device_group` (
  `id` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `modified` datetime NOT NULL,
  PRIMARY KEY (`id`,`name`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device_group`
--

LOCK TABLES `device_group` WRITE;
/*!40000 ALTER TABLE `device_group` DISABLE KEYS */;
INSERT INTO `device_group` VALUES ('4a7a86d1-9e53-4edb-a78e-0a6df1baaf69','Main Group','2024-02-23 12:08:48'),('group96053726-ae87-4c4e-97d2-f77fafc659f8','string','2024-02-28 13:28:39');
/*!40000 ALTER TABLE `device_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `log_table`
--

DROP TABLE IF EXISTS `log_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log_table` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `module` varchar(50) NOT NULL,
  `code` int(11) NOT NULL,
  `log_type` varchar(50) NOT NULL,
  `desc` varchar(255) NOT NULL,
  `date_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_table`
--

LOCK TABLES `log_table` WRITE;
/*!40000 ALTER TABLE `log_table` DISABLE KEYS */;
INSERT INTO `log_table` VALUES (1,'system',200,'update','Add group string success','2024-02-28 13:28:39'),(2,'call_box',200,'add_device','Create call_box with name 456','2024-03-05 07:21:02'),(3,'call_box',200,'add_device','Create call_box with name rostek_callbox','2024-03-05 08:59:46'),(4,'call_box',200,'update','Update call_box with ID deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37 in group 4a7a86d1-9e53-4edb-a78e-0a6df1baaf69','2024-03-05 09:06:22'),(5,'call_box',200,'update','Update call_box with ID deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37 in group 4a7a86d1-9e53-4edb-a78e-0a6df1baaf69','2024-03-06 06:42:42'),(6,'call_box',200,'update','Update call_box with ID deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37 in group 4a7a86d1-9e53-4edb-a78e-0a6df1baaf69','2024-03-07 04:04:22'),(7,'call_box',200,'update','Update call_box with ID deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37 in group 4a7a86d1-9e53-4edb-a78e-0a6df1baaf69','2024-03-07 06:07:57'),(8,'call_box',200,'update','Update call_box with ID deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37 in group 4a7a86d1-9e53-4edb-a78e-0a6df1baaf69','2024-03-07 10:02:08'),(9,'call_box',200,'update','Update call_box with ID deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37 in group 4a7a86d1-9e53-4edb-a78e-0a6df1baaf69','2024-03-07 10:06:23'),(10,'call_box',200,'update','Update call_box with ID deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37 in group 4a7a86d1-9e53-4edb-a78e-0a6df1baaf69','2024-03-07 11:01:28'),(11,'call_box',200,'update','Update call_box with ID device0fc9ab1c-61bd-495e-8a03-1025119376dd in group 4a7a86d1-9e53-4edb-a78e-0a6df1baaf69','2024-03-08 17:37:34'),(12,'call_box',200,'update','Update call_box with ID device0fc9ab1c-61bd-495e-8a03-1025119376dd in group 4a7a86d1-9e53-4edb-a78e-0a6df1baaf69','2024-03-08 17:40:04'),(13,'call_box',200,'update','Update call_box with ID deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37 in group 4a7a86d1-9e53-4edb-a78e-0a6df1baaf69','2024-03-09 07:31:12'),(14,'call_box',200,'update','Update call_box with ID device0fc9ab1c-61bd-495e-8a03-1025119376dd in group 4a7a86d1-9e53-4edb-a78e-0a6df1baaf69','2024-03-09 08:16:33'),(15,'call_box',200,'update','Update call_box with ID device0fc9ab1c-61bd-495e-8a03-1025119376dd in group 4a7a86d1-9e53-4edb-a78e-0a6df1baaf69','2024-03-11 00:53:23'),(16,'call_box',200,'update','Update call_box with ID deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37 in group 4a7a86d1-9e53-4edb-a78e-0a6df1baaf69','2024-03-11 00:54:09'),(17,'call_box',200,'update','Update call_box with ID deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37 in group 4a7a86d1-9e53-4edb-a78e-0a6df1baaf69','2024-03-11 00:54:11'),(18,'call_box',200,'add_device','Create call_box with name line tu dong','2024-03-11 06:58:25'),(19,'call_box',200,'update','Update call_box with ID devicef70aa21c-2a37-4275-88e0-0e2868e8bec1 in group 4a7a86d1-9e53-4edb-a78e-0a6df1baaf69','2024-03-11 07:40:47'),(20,'call_box',200,'update','Update call_box with ID devicef70aa21c-2a37-4275-88e0-0e2868e8bec1 in group 4a7a86d1-9e53-4edb-a78e-0a6df1baaf69','2024-03-11 07:45:55'),(21,'call_box',200,'delete','Delete call_box with ID devicef70aa21c-2a37-4275-88e0-0e2868e8bec1 in group 4a7a86d1-9e53-4edb-a78e-0a6df1baaf69','2024-03-11 07:48:49'),(22,'call_box',200,'add_device','Create call_box with name line tu dong','2024-03-11 07:49:36'),(23,'call_box',200,'update','Update call_box with ID deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37 in group 4a7a86d1-9e53-4edb-a78e-0a6df1baaf69','2024-03-12 06:59:35'),(24,'call_box',200,'update','Update call_box with ID deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37 in group 4a7a86d1-9e53-4edb-a78e-0a6df1baaf69','2024-03-14 03:08:05'),(25,'call_box',200,'update','Update call_box with ID device0fc9ab1c-61bd-495e-8a03-1025119376dd in group 4a7a86d1-9e53-4edb-a78e-0a6df1baaf69','2024-03-14 03:08:33'),(26,'call_box',200,'update','Update call_box with ID device5489411b-8562-4ac2-826f-e2fccbb142b3 in group 4a7a86d1-9e53-4edb-a78e-0a6df1baaf69','2024-03-14 03:09:22'),(27,'call_box',200,'delete','Delete call_box with ID devicef02bc648-4f58-482b-b788-88f377e1f4d4 in group 4a7a86d1-9e53-4edb-a78e-0a6df1baaf69','2024-03-15 01:39:44'),(28,'call_box',200,'update','Update call_box with ID deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37 in group 4a7a86d1-9e53-4edb-a78e-0a6df1baaf69','2024-09-05 08:46:28'),(29,'call_box',200,'update','Update call_box with ID deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37 in group 4a7a86d1-9e53-4edb-a78e-0a6df1baaf69','2024-09-05 08:46:52'),(30,'mqtt',200,'update','Update mqtt broker information [\'host\', \'port\', \'username\', \'password\']','2024-09-05 09:16:30'),(31,'call_box',200,'update','Update call_box with ID deviceb5e4f7ae-60a2-48f1-96c8-068b1cffeb37 in group 4a7a86d1-9e53-4edb-a78e-0a6df1baaf69','2024-09-18 02:38:40'),(32,'call_box',200,'delete','Delete call_box with ID device0fc9ab1c-61bd-495e-8a03-1025119376dd in group 4a7a86d1-9e53-4edb-a78e-0a6df1baaf69','2025-01-08 04:07:38');
/*!40000 ALTER TABLE `log_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oee`
--

DROP TABLE IF EXISTS `oee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oee` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device_id` varchar(50) NOT NULL,
  `machine_status` int(11) NOT NULL,
  `actual` int(11) NOT NULL,
  `running_number` int(11) NOT NULL,
  `timestamp` int(11) DEFAULT NULL,
  `changeover` int(11) DEFAULT NULL,
  `up_time` int(11) DEFAULT NULL,
  `change_type` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `device_id` (`device_id`),
  CONSTRAINT `oee_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `device` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oee`
--

LOCK TABLES `oee` WRITE;
/*!40000 ALTER TABLE `oee` DISABLE KEYS */;
/*!40000 ALTER TABLE `oee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oee_downtime`
--

DROP TABLE IF EXISTS `oee_downtime`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oee_downtime` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device_id` varchar(50) NOT NULL,
  `machine_status` int(11) NOT NULL,
  `timestamp` int(11) NOT NULL,
  `duration` int(11) NOT NULL,
  `end_time` int(11) NOT NULL,
  `running_number` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `device_id` (`device_id`),
  CONSTRAINT `oee_downtime_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `device` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oee_downtime`
--

LOCK TABLES `oee_downtime` WRITE;
/*!40000 ALTER TABLE `oee_downtime` DISABLE KEYS */;
/*!40000 ALTER TABLE `oee_downtime` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oee_production`
--

DROP TABLE IF EXISTS `oee_production`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oee_production` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device_id` varchar(50) NOT NULL,
  `start_time` int(11) NOT NULL,
  `start_production_time` int(11) NOT NULL,
  `end_time` int(11) NOT NULL,
  `actual` int(11) DEFAULT NULL,
  `running_number` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `device_id` (`device_id`),
  CONSTRAINT `oee_production_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `device` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oee_production`
--

LOCK TABLES `oee_production` WRITE;
/*!40000 ALTER TABLE `oee_production` DISABLE KEYS */;
/*!40000 ALTER TABLE `oee_production` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oee_sync`
--

DROP TABLE IF EXISTS `oee_sync`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oee_sync` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device_id` varchar(50) NOT NULL,
  `machine_status` int(11) NOT NULL,
  `actual` int(11) NOT NULL,
  `running_number` int(11) NOT NULL,
  `timestamp` int(11) DEFAULT NULL,
  `changeover` int(11) DEFAULT NULL,
  `up_time` int(11) DEFAULT NULL,
  `change_type` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `device_id` (`device_id`),
  CONSTRAINT `oee_sync_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `device` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oee_sync`
--

LOCK TABLES `oee_sync` WRITE;
/*!40000 ALTER TABLE `oee_sync` DISABLE KEYS */;
/*!40000 ALTER TABLE `oee_sync` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `username` varchar(50) NOT NULL,
  `password` varchar(50) DEFAULT NULL,
  `enterprise` varchar(50) DEFAULT NULL,
  `mqtt_password` varchar(20) DEFAULT NULL,
  `mqtt_username` varchar(20) DEFAULT NULL,
  `mqtt_host` varchar(20) DEFAULT NULL,
  `mqtt_port` int(11) DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('admin','admin','rostek','rostek2019','rostek','172.21.99.23',1883);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Current Database: `mysql`
--

USE `mysql`;

--
-- Final view structure for view `user`
--

/*!50001 DROP VIEW IF EXISTS `user`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`mariadb.sys`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `user` AS select `global_priv`.`Host` AS `Host`,`global_priv`.`User` AS `User`,if(json_value(`global_priv`.`Priv`,'$.plugin') in ('mysql_native_password','mysql_old_password'),ifnull(json_value(`global_priv`.`Priv`,'$.authentication_string'),''),'') AS `Password`,if(json_value(`global_priv`.`Priv`,'$.access') & 1,'Y','N') AS `Select_priv`,if(json_value(`global_priv`.`Priv`,'$.access') & 2,'Y','N') AS `Insert_priv`,if(json_value(`global_priv`.`Priv`,'$.access') & 4,'Y','N') AS `Update_priv`,if(json_value(`global_priv`.`Priv`,'$.access') & 8,'Y','N') AS `Delete_priv`,if(json_value(`global_priv`.`Priv`,'$.access') & 16,'Y','N') AS `Create_priv`,if(json_value(`global_priv`.`Priv`,'$.access') & 32,'Y','N') AS `Drop_priv`,if(json_value(`global_priv`.`Priv`,'$.access') & 64,'Y','N') AS `Reload_priv`,if(json_value(`global_priv`.`Priv`,'$.access') & 128,'Y','N') AS `Shutdown_priv`,if(json_value(`global_priv`.`Priv`,'$.access') & 256,'Y','N') AS `Process_priv`,if(json_value(`global_priv`.`Priv`,'$.access') & 512,'Y','N') AS `File_priv`,if(json_value(`global_priv`.`Priv`,'$.access') & 1024,'Y','N') AS `Grant_priv`,if(json_value(`global_priv`.`Priv`,'$.access') & 2048,'Y','N') AS `References_priv`,if(json_value(`global_priv`.`Priv`,'$.access') & 4096,'Y','N') AS `Index_priv`,if(json_value(`global_priv`.`Priv`,'$.access') & 8192,'Y','N') AS `Alter_priv`,if(json_value(`global_priv`.`Priv`,'$.access') & 16384,'Y','N') AS `Show_db_priv`,if(json_value(`global_priv`.`Priv`,'$.access') & 32768,'Y','N') AS `Super_priv`,if(json_value(`global_priv`.`Priv`,'$.access') & 65536,'Y','N') AS `Create_tmp_table_priv`,if(json_value(`global_priv`.`Priv`,'$.access') & 131072,'Y','N') AS `Lock_tables_priv`,if(json_value(`global_priv`.`Priv`,'$.access') & 262144,'Y','N') AS `Execute_priv`,if(json_value(`global_priv`.`Priv`,'$.access') & 524288,'Y','N') AS `Repl_slave_priv`,if(json_value(`global_priv`.`Priv`,'$.access') & 1048576,'Y','N') AS `Repl_client_priv`,if(json_value(`global_priv`.`Priv`,'$.access') & 2097152,'Y','N') AS `Create_view_priv`,if(json_value(`global_priv`.`Priv`,'$.access') & 4194304,'Y','N') AS `Show_view_priv`,if(json_value(`global_priv`.`Priv`,'$.access') & 8388608,'Y','N') AS `Create_routine_priv`,if(json_value(`global_priv`.`Priv`,'$.access') & 16777216,'Y','N') AS `Alter_routine_priv`,if(json_value(`global_priv`.`Priv`,'$.access') & 33554432,'Y','N') AS `Create_user_priv`,if(json_value(`global_priv`.`Priv`,'$.access') & 67108864,'Y','N') AS `Event_priv`,if(json_value(`global_priv`.`Priv`,'$.access') & 134217728,'Y','N') AS `Trigger_priv`,if(json_value(`global_priv`.`Priv`,'$.access') & 268435456,'Y','N') AS `Create_tablespace_priv`,if(json_value(`global_priv`.`Priv`,'$.access') & 536870912,'Y','N') AS `Delete_history_priv`,elt(ifnull(json_value(`global_priv`.`Priv`,'$.ssl_type'),0) + 1,'','ANY','X509','SPECIFIED') AS `ssl_type`,ifnull(json_value(`global_priv`.`Priv`,'$.ssl_cipher'),'') AS `ssl_cipher`,ifnull(json_value(`global_priv`.`Priv`,'$.x509_issuer'),'') AS `x509_issuer`,ifnull(json_value(`global_priv`.`Priv`,'$.x509_subject'),'') AS `x509_subject`,cast(ifnull(json_value(`global_priv`.`Priv`,'$.max_questions'),0) as unsigned) AS `max_questions`,cast(ifnull(json_value(`global_priv`.`Priv`,'$.max_updates'),0) as unsigned) AS `max_updates`,cast(ifnull(json_value(`global_priv`.`Priv`,'$.max_connections'),0) as unsigned) AS `max_connections`,cast(ifnull(json_value(`global_priv`.`Priv`,'$.max_user_connections'),0) as signed) AS `max_user_connections`,ifnull(json_value(`global_priv`.`Priv`,'$.plugin'),'') AS `plugin`,ifnull(json_value(`global_priv`.`Priv`,'$.authentication_string'),'') AS `authentication_string`,if(ifnull(json_value(`global_priv`.`Priv`,'$.password_last_changed'),1) = 0,'Y','N') AS `password_expired`,elt(ifnull(json_value(`global_priv`.`Priv`,'$.is_role'),0) + 1,'N','Y') AS `is_role`,ifnull(json_value(`global_priv`.`Priv`,'$.default_role'),'') AS `default_role`,cast(ifnull(json_value(`global_priv`.`Priv`,'$.max_statement_time'),0.0) as decimal(12,6)) AS `max_statement_time` from `global_priv` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Current Database: `rostek_gateway`
--

USE `rostek_gateway`;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-19 14:13:31
