package main

import (
	"fmt"
)

func main() {
	var test int
	fmt.Println("Hello World: Type a Number: ")
	for i := 1; i < 5; i++ {
		fmt.Scanf("%d", &test)
		fmt.Println(test)
	}
}
