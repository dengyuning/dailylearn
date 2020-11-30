##### 一、快速排序

1. 核心思想：
         对于数组中的每一个元素，将其放到最终位置上（左边的元素都比他小，右边的元素都比它大）。

2. 算法逻辑：

   2.1 

   > a) 随机挑选基准元素nums[a]，将其放到最右（最左也可以，这里假设放在最右）
   >
   > b) 用两个指针，i和j，j用于从左往右遍历，i用于记录比nums[i]小的元素，初始值设为`l-1`
   >
   > c) 遇到比nums[a]小的元素，则将其与nums[i]交换,i++,j++; 否则j++ 
   >
   > d) 到达数组末尾时，i+1记录的则是基准元素的最终位置
   >
   > e) 对i+1 左边的数组元素进行快速排序
   >
   > f) 对i+1 右边的数组元素进行快速排序

   2.2 

   > a) 随机挑选基准元素nums[a]，将其放到最右nums[r]（最左也可以，这里假设放在最右）
   >
   > b) 用两个指针, i = 0, j = len(nums) - 2，i 从左往右遍历, j 从右往左遍历
   >
   > c) 如果nums[i] > nums[r] , 则交换nums[i]和nums[j]的值, j--
   >
   > d) 如果nums[j] < nums[r], 则交换nums[i]和nums[j]的值, i++
   >
   > e) i==j 的时候 交换nums[i]和nums[r]的值
   >
   > e) 对i+1 左边的数组元素进行快速排序
   >
   > f) 对i+1 右边的数组元素进行快速排序

3. 栗子🌰：

   

4. 代码：

   ```
   func randomPartition(a []int, l, r int) int {
   	i := rand.Int() % (r - l + 1) + l    // 随机挑选基准元素
   	a[i], a[r] = a[r], a[i]
   	return partition(a, l, r)
   }
   
   func partition(a []int, l, r int) int {
   	x := a[r]
   	i := l - 1
   	for j := l; j < r; j++ {
   		if a[j] <= x {
   			i++
   			a[i], a[j] = a[j], a[i]
   		}
   	}
   	a[i+1], a[r] = a[r], a[i+1]
   	return i + 1
   }
   
   ```

   

   
