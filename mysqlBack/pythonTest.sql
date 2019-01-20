/*
Navicat MySQL Data Transfer

Source Server         : 172.30.34.210
Source Server Version : 50642
Source Host           : 172.30.34.210:3306
Source Database       : pythonTest

Target Server Type    : MYSQL
Target Server Version : 50642
File Encoding         : 65001

Date: 2019-01-19 21:59:39
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for books
-- ----------------------------
DROP TABLE IF EXISTS `books`;
CREATE TABLE `books` (
  `book_Id` varchar(255) NOT NULL COMMENT '书本id',
  `book_name` varchar(255) DEFAULT NULL COMMENT '书本名称',
  `state` varchar(10) DEFAULT '' COMMENT '状态 1：连载 2：完结',
  `author` varchar(255) DEFAULT NULL COMMENT '作者',
  `chan_Id` int(11) DEFAULT NULL COMMENT '分类id',
  `chan_name` varchar(255) DEFAULT NULL COMMENT '分类名',
  `sub_Id` int(11) DEFAULT NULL COMMENT '子分类id',
  `sub_name` varchar(255) DEFAULT NULL COMMENT '子分类',
  `chapter_total_cnt` int(11) DEFAULT NULL COMMENT '章节总数',
  `word_count` int(11) DEFAULT NULL COMMENT '字数',
  `gender` int(1) DEFAULT '0' COMMENT '性别 1:男 2: 女',
  `synoptic` text COMMENT '简介',
  `img_url` varchar(600) DEFAULT NULL COMMENT '图片路径',
  `add_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `nex` int(11) NOT NULL DEFAULT '0' COMMENT '采集次数、被抓取次数',
  PRIMARY KEY (`book_Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for links
-- ----------------------------
DROP TABLE IF EXISTS `links`;
CREATE TABLE `links` (
  `id` int(11) DEFAULT NULL,
  `catalog_Id` varchar(255) DEFAULT NULL COMMENT '章节Id',
  `catalog_name` varchar(255) DEFAULT NULL COMMENT '章节名称',
  `book_Id` varchar(255) DEFAULT NULL COMMENT '书本Id',
  `book_name` text COMMENT '书籍名称',
  `cnt` int(11) DEFAULT NULL COMMENT '章节字数',
  `url` varchar(200) NOT NULL COMMENT 'url',
  `uuid` int(11) DEFAULT NULL COMMENT '排序',
  `fs` int(11) DEFAULT NULL COMMENT '0：免费 1:vip',
  `add_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `nex` int(11) NOT NULL DEFAULT '0' COMMENT '采集次数、被抓取次数',
  `article` longtext COMMENT '文章内容',
  PRIMARY KEY (`url`),
  KEY `index_name` (`book_Id`),
  KEY `index_nex` (`nex`),
  KEY `index_fs` (`fs`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='链接库';
