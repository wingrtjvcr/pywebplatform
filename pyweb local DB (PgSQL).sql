/*
Navicat PGSQL Data Transfer

Source Server         : localhost
Source Server Version : 90325
Source Host           : localhost:5432
Source Database       : wingtest
Source Schema         : public

Target Server Type    : PGSQL
Target Server Version : 90325
File Encoding         : 65001

Date: 2019-08-01 11:02:45
*/






-- CREATE DATABASE pyweb WITH OWNER = postgres;





-- ----------------------------
-- Table structure for t1

-- ----------------------------

DROP TABLE IF EXISTS "public"."t1";
CREATE TABLE "public"."t1" (
"id" int4 NOT NULL,
"name" varchar COLLATE "default",
"age" int4
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of t1
-- ----------------------------
INSERT INTO "public"."t1" VALUES ('49653', 'new2', null);
INSERT INTO "public"."t1" VALUES ('60753', 'new1', null);
INSERT INTO "public"."t1" VALUES ('99601', 'heiheihei', null);
INSERT INTO "public"."t1" VALUES ('99602', 'lololo', null);
INSERT INTO "public"."t1" VALUES ('99603', 'yiyiyi', null);

-- ----------------------------
-- Alter Sequences Owned By 
-- ----------------------------

-- ----------------------------
-- Primary Key structure for table t1
-- ----------------------------
ALTER TABLE "public"."t1" ADD PRIMARY KEY ("id");




-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS "public"."users";
CREATE TABLE "public"."users" (
"id" int4 NOT NULL,
"usrname" varchar COLLATE "default",
"pwd" varchar COLLATE "default",
"email" varchar COLLATE "default",
"phone" varchar COLLATE "default",
"joindate" timestamp(6)
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO "public"."users" VALUES ('1', '10120869', 'wing', '77@gmail.com', '11', '2019-03-21 13:33:01');

-- ----------------------------
-- Alter Sequences Owned By 
-- ----------------------------

-- ----------------------------
-- Primary Key structure for table users
-- ----------------------------
ALTER TABLE "public"."users" ADD PRIMARY KEY ("id");
