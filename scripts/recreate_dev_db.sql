-- run this script as root to drop and recreate the database
-- mysql -u root -p < script/recreate_db.sql
DROP DATABASE IF EXISTS openn;
CREATE DATABASE openn CHARACTER SET utf8 COLLATE utf8_unicode_ci;
GRANT ALL PRIVILEGES ON *.* TO 'openn'@'localhost' IDENTIFIED BY 'openn';
FLUSH PRIVILEGES;
