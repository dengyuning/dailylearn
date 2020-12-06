#### 不同路径

一个机器人位于一个 m x n 网格的左上角。

机器人每次只能向下或者向右移动一步。机器人试图达到网格的右下角。

问总共有多少条不同的路径？

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/unique-paths

```
func uniquePaths(m int, n int) int {
	res := make([]int, n)
	for i:=0;i<n;i++ {
		res[i] = 1
	}
    for j:=1;j<m;j++ {
        for i:=1;i<n;i++{
            res[i] += res[i-1]
        }
    }
	return res[n-1]
}
```
