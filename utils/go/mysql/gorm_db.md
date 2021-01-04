```
package mysql

import (
	"fmt"
	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/mysql"
	"github.com/lexkong/log"
)

var DefaultMaxIdleConns = 0
var DefaultMaxOpenConns = 100

type OrmDB struct {
	DB *gorm.DB
}

func NewGormDB(userName, password, host, dbName string, port int) (*OrmDB, error) {
	var err error
	url := fmt.Sprintf("%s:%s@tcp(%s:%d)/%s?charset=utf8&parseTime=true&loc=Local",
		userName, password, host, port, dbName)
	log.Infof(url)
	GormDB := &OrmDB{}
	GormDB.DB, err = gorm.Open("mysql", url)
	if err != nil {
		return nil, err
	}
	//全局禁用表名复数
	GormDB.DB.SingularTable(true)
	GormDB.DB.DB().SetMaxIdleConns(DefaultMaxIdleConns)
	GormDB.DB.DB().SetMaxOpenConns(DefaultMaxOpenConns)
	err = GormDB.DB.DB().Ping()
	if err != nil {
		return nil, err
	}
	return GormDB, nil
}

func (db *OrmDB) SetMaxOpenConns(maxOpenConns int) *OrmDB {
	db.DB.DB().SetMaxOpenConns(maxOpenConns)
	return db
}

func (db *OrmDB) SetMaxIdleConns(maxIdleConns int) *OrmDB {
	db.DB.DB().SetMaxOpenConns(maxIdleConns)
	return db
}

// 设置数据库表前缀
func (db *OrmDB) SetPrefixTableName(prefixTableName string) *OrmDB {
	gorm.DefaultTableNameHandler = func(db *gorm.DB, defaultTableName string) string {
		return prefixTableName + defaultTableName
	}
	return db
}

// 设置debug模式，可以打印出sql语句,默认为false
func (db *OrmDB) SetLogMode(logMode bool) *OrmDB {
	db.DB.LogMode(logMode)
	return db
}

```
