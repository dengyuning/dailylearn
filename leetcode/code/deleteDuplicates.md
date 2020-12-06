#### 删除排序链表中的重复元素 II
给定一个排序链表，删除所有含有重复数字的节点，只保留原始链表中 没有重复出现 的数字。

示例 1:
输入: 1->2->3->3->4->4->5
输出: 1->2->5

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/remove-duplicates-from-sorted-list-ii

func deleteDuplicates(head *ListNode) *ListNode {
	dummyHead := &ListNode{
		Val: -1,
		Next: head,
	}
	pre := dummyHead
	cur := dummyHead.Next
	dup := 0
	for ;cur!=nil && cur.Next !=nil ;{
		if cur.Next.Val != cur.Val{
			pre = pre.Next
			cur = cur.Next
		}else{
			dup = cur.Val
			for ;cur!=nil && cur.Val==dup; {
				cur = cur.Next
			}
			pre.Next = cur
		}
	}
	return dummyHead.Next
}
