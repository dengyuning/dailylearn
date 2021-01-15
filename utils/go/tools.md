```
package tools

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"

	"github.com/spf13/viper"
	"gopkg.in/yaml.v2"
)

// SupportedExts Universally supported extensions.
var SupportedExts []string = []string{"json", "yaml", "yml"}

// UnsupportedConfigError configuration filetype.
type UnsupportedConfigError string

// Returns the formatted configuration error.
func (str UnsupportedConfigError) Error() string {
	return fmt.Sprintf("Unsupported Config Type %q", string(str))
}
func getConfigType() string {
	cf := viper.ConfigFileUsed()
	ext := filepath.Ext(cf)
	if len(ext) > 1 {
		return ext[1:]
	}
	return ""
}

// SaveConfig will store the settings from viper inside the config-file
func SaveConfig() error {
	// Verify if format is accepted
	if !StringContain(getConfigType(), SupportedExts) {
		return UnsupportedConfigError(getConfigType())
	}
	// Open file
	f, err := os.Create(viper.ConfigFileUsed())
	defer f.Close()
	if err != nil {
		return err
	}
	// Switch between formats
	switch getConfigType() {
	case "json":
		b, err := json.MarshalIndent(viper.AllSettings(), "", "    ")
		if err != nil {
			return err
		}
		f.WriteString(string(b))
	case "yaml", "yml":
		b, err := yaml.Marshal(viper.AllSettings())
		if err != nil {
			return err
		}
		f.WriteString(string(b))
	}
	return nil
}

func GoRouting(){
	for i := 0; i < 3; i++ {
		wg := sync.WaitGroup{}
		ch := make(chan int, 5)
		for j:=0;j<5;j++{
			wg.Add(1)
			go func(wg *sync.WaitGroup, i int,  ch chan<- int) {
				log.Printf("i:%d", i)
				ch <- i
				wg.Done()
			}(&wg, j,ch)
		}
		wg.Wait()
		log.Printf("run:i:%d", i)
	}
}

```
