// LabelHistory, gorm约定表名模型规则
```
type LabelHistory struct {
	ActionId  int64  `gorm:"AUTO_INCREMENT;primary_key;comment:'自增操作Id'"`
	RequestId string `gorm:"type:varchar(200);comment:'请求ID'"`
	Query     string `gorm:"type:varchar(200);comment:'查询query'"`
	Count     int    `gorm:"type:int;comment:'查询用户数'"`
	Time      string `gorm:"type:varchar(200);comment:'查询时间'"`
	State     string `gorm:"type:varchar(100);comment:'任务执行结束状态'"`
	Remarks   string `gorm:"type:varchar(100);comment:'备注信息'"`
}
```
