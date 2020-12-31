```
  fs, err = os.Open(filePath + "special_words.txt")
	if err != nil {
		return err
	}
	defer fs.Close()
	
	scanner = bufio.NewScanner(fs)
	scanner.Split(bufio.ScanLines)
	for scanner.Scan() {
		items := strings.Split(scanner.Text(), ",")
	}
```
