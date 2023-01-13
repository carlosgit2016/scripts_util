package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func Enqueue(element int, queue []int) []int {
	queue = append(queue, element)
	return queue
}

func Dequeue(queue []int) []int {
	var index = 0
	return queue[:index]
}

func PrintElement(queue []int) {
	fmt.Println(queue[0])
}

func Operation(line string, queue []int) []int {
	var operation int
	var value int

	array := strings.Fields(line)
	operation, _ = strconv.Atoi(array[0])

	if len(array) > 1 {
		value, _ = strconv.Atoi(array[1])
	}

	switch operation {
	case 1:
		return Enqueue(value, queue)
	case 2:
		return Dequeue(queue)
	case 3:
		PrintElement(queue)
		return queue
	}

	return queue
}

func main() {
	reader := bufio.NewReader(os.Stdin)
	var queue []int
	var lines string

	for {
		line, _ := reader.ReadString('\n')

		if line == "" {
			break
		}

		lines += line
	}

	array_lines := strings.Split(lines, "\n")
	line_amount, _ := strconv.Atoi(array_lines[0])

	for i := 1; i <= line_amount; i++ {
		Operation(array_lines[i], queue)
	}
}
