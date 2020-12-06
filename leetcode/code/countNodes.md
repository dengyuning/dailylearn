#### 完全二叉树的节点个数
```
func countNodes(root *TreeNode) int {
	if root == nil{
		return 0
	}
	levelLeft := countLevel(root.Left)
	levelRight := countLevel(root.Right)
	if levelLeft == levelRight {
		// 左子树满
		return int(math.Exp2(float64(levelLeft))) -1 + 1 + countNodes(root.Right)
	}else{
		// 右子树满
		return int(math.Exp2(float64(levelRight))) -1 + 1 + countNodes(root.Left)
	}
}

func countLevel(root *TreeNode) int{
    l := 0
    left := root
    for ;left!=nil;{
        left = left.Left
        l += 1
    }
    return l
}
```
