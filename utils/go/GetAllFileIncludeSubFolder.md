```
func GetAllFileIncludeSubFolder(folder string) (*set.Set, error) {
	fmt.Print(folder)
	files := set.New()

	_ = filepath.Walk(folder, func(path string, fi os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		if !fi.IsDir() {
			files.Add(path)
		}
		return nil
	})
	return files, nil
}
```
