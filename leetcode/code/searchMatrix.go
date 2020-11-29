func searchMatrix(matrix [][]int, target int) bool {
    if len(matrix) <=0 {
        return false
    }
    row := len(matrix) - 1
    col := len(matrix[0]) - 1
    i := row
    j := 0
    for ;i>=0 && j<=col;{
         if target == matrix[i][j]{
                return true
            }
            if target > matrix[i][j]{
                j += 1
            }else{
                i -= 1
            }
    }
    return false
}
