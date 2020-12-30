```
func MathCal(wordList []string) (int, error) {
	// 3 * (23 - 2)
	var res int
	userStack := stack.New()
	opStack := stack.New()

	for _, w := range wordList {
		// 非右括号则入栈
		if w != right {
			if w == "+" || w == "-" || w == "*" || w == "/" {
				opStack.Push(w) // 操作符入栈
			} else {
				userStack.Push(w) // 用户入栈
			}
		}

		// 遇到右括号出栈
		if w == right {
			mergeList := []string{}
			for userStack.Len() != 0 {
				top := userStack.Pop().(string)
				if top == left {
					break
				} else {
					mergeList = append(mergeList, top)
				}
			}
			if opStack.Len() != 0 {
				op := opStack.Pop().(string)
				if len(mergeList) != 2 {
					err := errors.New("parse failed")
					log.Error("", err)
					return -1, err
				}
				tmp, err := calUsers(mergeList[0], mergeList[1], op)
				if err != nil {
					err := errors.New("parse failed")
					log.Error("", err)
					return -1, err
				}
				// 合并完入栈
				tmpStr := strconv.Itoa(tmp)
				userStack.Push(tmpStr)
			} else {
				tmp, err := strconv.Atoi(mergeList[0])
				if err != nil {
					err := errors.New("parse failed")
					log.Error("", err)
					return -1, err
				}
				// 合并完入栈
				tmpStr := strconv.Itoa(tmp)
				userStack.Push(tmpStr)
			}
		}
	}
	if opStack.Len() >= 0 {
		mergeList := []string{}
		for userStack.Len() != 0 {
			top := userStack.Pop().(string)
			if top == left {
				break
			} else {
				mergeList = append(mergeList, top)
			}
		}
		if opStack.Len() != 0 {
			op := opStack.Pop().(string)
			if len(mergeList) != 2 {
				err := errors.New("parse failed")
				log.Error("", err)
				return res, err
			}
			res, err := calUsers(mergeList[0], mergeList[1], op)
			if err != nil {
				err := errors.New("parse failed")
				log.Error("", err)
				return res, err
			}
			return res, nil
		} else {
			res, err := strconv.Atoi(mergeList[0])
			if err != nil {
				err := errors.New("parse failed")
				log.Error("", err)
				return res, err
			}
			return res, nil
		}
	}
	return res, nil
}

func calUsers(user1 string, user2 string, op string) (int, error) {
	var res int
	f1, err := strconv.Atoi(user1)
	if err != nil {
		err := errors.New("parse failed")
		log.Error("", err)
		return res, err
	}
	f2, err := strconv.Atoi(user2)
	if err != nil {
		err := errors.New("parse failed")
		log.Error("", err)
		return res, err
	}
	switch op {
	case "*":
		res = f1 * f2
	case "+":
		res = f1 + f2
	case "/":
		res = f2 / f1
	case "-":
		res = f2 - f1
	}
	return res, nil
}
```
