/*
@Author: github.com/imvast
@Date: 2/5/2023
*/

package main

import (
	"bufio"
	"fmt"
	"math/rand"
	"os"
	"time"
)

func main() {
	rand.Seed(time.Now().UnixNano())
	chars := "abcdefghijklmnopqrstuvwxyz0123456789"

	f, err := os.Create("keys.txt")
	if err != nil {
		panic(err)
	}
	defer f.Close()

	w := bufio.NewWriter(f)
	start := time.Now()
	for i := 0; i < 100_000; i++ {
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
	fmt.Printf("[*] Generated 100,000 keys in %v seconds", elapsed.Seconds())
}