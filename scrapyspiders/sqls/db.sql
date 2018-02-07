CREATE DATABASE spiders;

USE spiders;

/*jobbole project*/
CREATE TABLE `jobbole_article` (
  `url_object_id` char(32) NOT NULL COMMENT '文章URL的MD5 hash值',
  `title` varchar(200) NOT NULL DEFAULT '' COMMENT '文章标题',
  `create_date` date NOT NULL COMMENT '发表时间',
  `url` varchar(300) NOT NULL DEFAULT '' COMMENT '文章URL',
  `front_image_url` varchar(300) DEFAULT NULL COMMENT '封面URL',
  `front_image_path` varchar(200) DEFAULT NULL COMMENT '图片保存路径',
  `comment_nums` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '评论数',
  `fav_nums` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '收藏数',
  `praise_nums` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '点赞数',
  `tags` varchar(200) NOT NULL DEFAULT '' COMMENT '标签',
  `category` varchar(50) DEFAULT NULL COMMENT '分类',
  `content` longtext NOT NULL COMMENT '文章内容',
  `create_at` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '创建时间',
  PRIMARY KEY (`url_object_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='文章表';

/*获取西刺ip并且插入到数据库*/
CREATE TABLE IF NOT EXISTS `proxy_ip`(
  id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  ip VARCHAR(20) NOT NULL DEFAULT '' COMMENT '代理ip地址',
  port INT UNSIGNED NOT NULL COMMENT '端口',
  speed DECIMAL(10,3) DEFAULT 0.000 NOT NULL COMMENT '连接速度',
  http_type CHAR(10) NOT NULL COMMENT 'http类型',
  PRIMARY KEY(id),
  UNIQUE KEY ip_port_key(ip,port)
)ENGINE=Innodb DEFAULT CHARSET='UTF8' AUTO_INCREMENT=1 COMMENT '代理ip表';
