1. import	"github.com/lexkong/log"

```
t0 = time.Now()
log.Infof("初始化完成，总耗时: %v", time.Since(t0))
```

```
package tools

import (
	"encoding/json"
	"os"
	"strings"
	"unicode"

	"github.com/lexkong/log"
)

// StringContain 判断字符串是否存在另一字符串列表中
func StringContain(target string, strings []string) bool {
	for _, str := range strings {
		if target == str {
			return true
		}
	}
	return false
}

// StringsContain 判断字符串列表是否有交集
func StringsContain(targets []string, strings []string) bool {
	for _, target := range targets {
		if StringContain(target, strings) {
			return true
		}
	}
	return false
}

// IsFileExisted 判断文件是否存在
func IsFileExisted(path string) bool {
	_, err := os.Stat(path)
	if err != nil {
		if os.IsExist(err) {
			return true
		}
		return false
	}
	return true
}

// ContainsHanScript 判断是否包含汉字
func ContainsHanScript(str string) bool {
	hanScript := false
	for _, runeValue := range str {
		if unicode.Is(unicode.Han, runeValue) {
			hanScript = true
		} else {
			continue
		}
	}
	return hanScript
}

// ContainsBasicMark 判断是否包含基础标点
func ContainsBasicMark(str string) bool {
	hasMark := false
	basicMark := []string{",", ";", "，", "。", "；", "、"}
	for _, mark := range basicMark {
		if strings.Contains(str, mark) {
			hasMark = true
			break
		}
	}
	return hasMark
}

// ArrayToJSONStr 序列化
func ArrayToJSONStr(arr []string) (string, error) {
	jsonStr, err := json.Marshal(arr)
	if err != nil {
		log.Error("array can't change to json string", err)
		return "", err
	}
	return string(jsonStr), nil
}

// JSONStrToArray 反序列化
func JSONStrToArray(str string) ([]string, error) {
	var arr []string
	err := json.Unmarshal([]byte(str), &arr)
	if err != nil {
		log.Error("json string can't change to array", err)
		return nil, err
	}
	return arr, nil
}

// Contains 判断数值是否存在数值列表
func Contains(s []int, e int) bool {
	for _, a := range s {
		if a == e {
			return true
		}
	}
	return false
}

// DeepCopy 深拷贝
func DeepCopy(value interface{}) interface{} {
	if valueMap, ok := value.(map[string]interface{}); ok {
		newMap := make(map[string]interface{})
		for k, v := range valueMap {
			newMap[k] = DeepCopy(v)
		}

		return newMap
	} else if valueSlice, ok := value.([]interface{}); ok {
		newSlice := make([]interface{}, len(valueSlice))
		for k, v := range valueSlice {
			newSlice[k] = DeepCopy(v)
		}

		return newSlice
	}

	return value
}
```
