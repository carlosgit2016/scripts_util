package main

import (
    "bufio"
    "fmt"
    "io"
    "os"
    "strconv"
    "strings"
)

/*
 * Complete the 'queensAttack' function below.
 *
 * The function is expected to return an INTEGER.
 * The function accepts following parameters:
 *  1. INTEGER n
 *  2. INTEGER k
 *  3. INTEGER r_q
 *  4. INTEGER c_q
 *  5. 2D_INTEGER_ARRAY obstacles
 */

func queensAttack(n int32, k int32, r_q int32, c_q int32, obstacles [][]int32) int32 {
    // Write your code here
    var qPosition int32 = 1
    //diagonals := 4
    var sides int32 = 2
    sideMovements := (n - qPosition) * sides

    var leftToRightDiagonal int32
    // calc left to right diagonal
    if (r_q <= c_q) {
        leftToRightDiagonal = (n - r_q) + (r_q -1)
    } else {
        leftToRightDiagonal = (n - (r_q + (c_q - r_q))) + c_q -1
    }

    return sideMovements + leftToRightDiagonal
}

func main() {
    reader := bufio.NewReaderSize(os.Stdin, 16 * 1024 * 1024)

    firstMultipleInput := strings.Split(strings.TrimSpace(readLine(reader)), " ")

    nTemp, err := strconv.ParseInt(firstMultipleInput[0], 10, 64)
    checkError(err)
    n := int32(nTemp)

    kTemp, err := strconv.ParseInt(firstMultipleInput[1], 10, 64)
    checkError(err)
    k := int32(kTemp)

    secondMultipleInput := strings.Split(strings.TrimSpace(readLine(reader)), " ")

    r_qTemp, err := strconv.ParseInt(secondMultipleInput[0], 10, 64)
    checkError(err)
    r_q := int32(r_qTemp)

    c_qTemp, err := strconv.ParseInt(secondMultipleInput[1], 10, 64)
    checkError(err)
    c_q := int32(c_qTemp)

    var obstacles [][]int32
    for i := 0; i < int(k); i++ {
        obstaclesRowTemp := strings.Split(strings.TrimRight(readLine(reader)," \t\r\n"), " ")

        var obstaclesRow []int32
        for _, obstaclesRowItem := range obstaclesRowTemp {
            obstaclesItemTemp, err := strconv.ParseInt(obstaclesRowItem, 10, 64)
            checkError(err)
            obstaclesItem := int32(obstaclesItemTemp)
            obstaclesRow = append(obstaclesRow, obstaclesItem)
        }

        if len(obstaclesRow) != 2 {
            panic("Bad input")
        }

        obstacles = append(obstacles, obstaclesRow)
    }

    result := queensAttack(n, k, r_q, c_q, obstacles)

    fmt.Println(result)
}

func readLine(reader *bufio.Reader) string {
    str, _, err := reader.ReadLine()
    if err == io.EOF {
        return ""
    }

    return strings.TrimRight(string(str), "\r\n")
}

func checkError(err error) {
    if err != nil {
        panic(err)
    }
}
