1. 从已有分支新建一个分支：

   `git checkout -b name`

2. 在B分支上merge A分支

   ```bash
   git checkout B
   git merge A
   ```

3. 更新远程分支

   ```bash
   git remote update origin --prune
   git remote update origin -p
   ```

4. Git add 添加多余文件，如何撤销？

   ```bashrc
   Git status 先看一下add中的文件
   Git reset HEAD 如果后面什么都不跟的话，就是上一次add里面的全部撤销了。
   Git reset HEAD xx/xx.java 就是对某个文件进行撤销了
   ```

5. 删除本地分支

   `$ git branch -d <BranchName>`

6. 删除远程分支

   `git push origin --delete <BranchName>`

7. 批量删除本地分支

   git branch | grep -v 'tbp' | xargs git branch -D

8. 把项目A(git)的某个分支内容拷贝到一个新的项目B(git仓库)

   ```进入项目A
   1. cd 项目A
   2. git checkout branchName
   3. git remote add origin2 master
   4. git remote set-url origin2 B.git
   5. git checkout -b branchB1(如果不需要修改分支名，当前步骤可以跳过)
   6. git push origin2
   ```

9. git 开发规范：	https://juejin.im/post/5b4328bbf265da0fa21a6820

10. git 删除远端文件（不删除本地）

    ```
    git rm -r --cached A
    git commit -m "ignore A"
    git push　
    ```

11. 删除本地及远程的master分支

    git branch -D master         //删除本地master分支

    git push origin :master     //删除远程master分支

12. 打tag

13. go fmt 格式化整个工程的go文件

    ```
    gofmt -w src
    ```
14. 撤销上一次commit
    
   ```
   git reset --soft HEAD^
   ```

