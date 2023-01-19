package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func Dequeue(queue []int) []int {
	var second_index = 1
	return queue[second_index:int(len(queue))]
}

func PrintElement(queue []int) {
	fmt.Println(queue[0])
}

func Operation(line string, queue []int) []int {
	var value int

	line = strings.TrimSpace(line)
	array := strings.Split(line, " ")

	operation, _ := strconv.Atoi(array[0])

	if len(array) > 1 {
		value, _ = strconv.Atoi(array[1])
	}
	switch operation {
	case 1:
		queue = append(queue, value)
	case 2:
		queue = Dequeue(queue)
	case 3:
		PrintElement(queue)
	}
	return queue
}

func main() {
	reader := bufio.NewReader(os.Stdin)
	var queue []int

	var FirstLine int

	_, err := fmt.Scanf("%d", &FirstLine)
	if err != nil {
		panic(err)
	}

	for i := 0; i < FirstLine; i++ {

		line, _ := reader.ReadString('\n')
		queue = Operation(line, queue)
	}
}
