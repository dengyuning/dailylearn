```
func ParseTimeToString(t time.Time) string {
	timestamp := t.Unix()
	tm := time.Unix(timestamp, 0)
	stime := tm.Format("2006-01-02 15:04:05")
	return stime
}
```
