```
package set

import "sync"

type Set struct {
	M map[interface{}]bool
	sync.RWMutex
}

/*建立新的set*/
func New() *Set {
	set := Set{M: map[interface{}]bool{}}
	return &set
}

/*从已有的interface{} slice中建立新的set*/
func NewSetFromSlice(init []interface{}) *Set {
	set := Set{M: map[interface{}]bool{}}
	for _, s := range init {
		if set.M[s] == false {
			set.M[s] = true
		}
	}
	return &set
}

/*加入一个新的元素*/
func (s *Set) Add(item interface{}) {
	s.Lock()
	defer s.Unlock()
	s.M[item] = true
}

/*删除一个元素*/
func (s *Set) Remove(item interface{}) {
	s.Lock()
	defer s.Unlock()
	delete(s.M, item)
}

/*查看是否含有一个元素*/
func (s *Set) Has(item interface{}) bool {
	s.RLock()
	defer s.RUnlock()
	_, ok := s.M[item]
	return ok
}

/*检查集合元素的个数*/
func (s *Set) Size() int {
	return len(s.List())
}

/*清空集合*/
func (s *Set) Clear() {
	s.Lock()
	defer s.Unlock()
	s.M = map[interface{}]bool{}
}

/*检查集合是否为空*/
func (s *Set) IsEmpty() bool {
	if s.Size() == 0 {
		return true
	}
	return false
}

/*将集合元素转化为interface{} slice，可用于输出和遍历*/
func (s *Set) List() []interface{} {
	s.RLock()
	defer s.RUnlock()
	list := []interface{}{}
	for item := range s.M {
		list = append(list, item)
	}
	return list
}

/*返回集合的交集*/
func (s *Set) Intersect(s1 *Set) *Set {
	s.Lock()
	defer s.Unlock()
	s2 := New()
	for item := range s.M {
		if s1.M[item] == true {
			s2.Add(item)
		}
	}
	return s2
}

/*返回集合的并集*/
func (s *Set) Union(s1 *Set) *Set {
	s.Lock()
	defer s.Unlock()
	s2 := New()
	for item := range s.M {
		s2.Add(item)
	}
	for item := range s1.M {
		s2.Add(item)
	}
	return s2
}

func NewSetFromStringSlice(init []string) *Set {
	set := Set{M: map[interface{}]bool{}}
	for _, s := range init {
		if set.M[s] == false {
			set.M[s] = true
		}
	}
	return &set
}

```
