```
func InitGorm() *OrmDB {
	var user = viper.GetString("Mysql.User")
	var password = viper.GetString("Mysql.Password")
	var host = viper.GetString("Mysql.Host")
	var port = viper.GetInt("Mysql.Port")
	var dbname = viper.GetString("Mysql.Database")
	var err error
	gormDB, err = NewGormDB(user, password, host, dbname, port)
	if err != nil {
		log.Error("connect mysql error", err)
	}
	gormDB.SetLogMode(true)
	return gormDB
}
```
