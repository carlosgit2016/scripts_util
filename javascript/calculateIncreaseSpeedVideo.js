const [actualTime, resizedTime] = process.argv.splice(2);

console.log(calculateResizeVideo(actualTime, resizedTime));

function calculateResizeVideo(actualTime, resizedTime) {

    const actualTimeSeconds = stringToTime(actualTime);
    const resizedTimeSeconds = stringToTime(resizedTime);

    const percentToIncreaseSpeedVideo = calculatePercent(actualTimeSeconds, resizedTimeSeconds);

    return percentToIncreaseSpeedVideo.toFixed(2);
}

function calculatePercent(beforeTime, afterTime) {
    // Receive two times and return the percent of reduction or increse

    const newPercent = beforeTime * 100 / afterTime;

    return newPercent;
}

function stringToTime(time) {
    const splitedTime = time.split(":").map(n => Number(n));
    const newTime = ((splitedTime[0] * 60) * 60) + (splitedTime[1] * 60) + splitedTime[2]
    return newTime;
}

// Input: 
// 00:11:32:02
// 00:05:00:00

// Calculate the total percent of increase speed.
// e.g. docker run --rm calculate-resize-video "00:13:00" "00:05:00"
// 260.00 % you need increase to adjust the time from 13 minutes to 05 minutes
