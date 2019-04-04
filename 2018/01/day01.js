const fs = require('fs');

const dataFromRaw = (rawData) => {
    const data = [];
    rawData.toString().trim().split('\n').forEach((d) => data.push(parseInt(d)));
    return data;
}

const part1 = (rawData) => {
    const data = dataFromRaw(rawData);
    const total = data.reduce((acc, value) => acc + value);
    console.log(`Day 1 Part 1 Answer ${total}`);
};

const part2 = (rawData) => {
    const data = dataFromRaw(rawData);
    const frequencies = new Set();
    let frequency = 0;
    let answer = NaN;

    while (!answer) {
        for (const val of data) {
            frequency += val;
            if (!answer && frequencies.has(frequency)) {
                answer = frequency;
                break;
            }
            frequencies.add(frequency);
        }
    }
    console.log(`Day 1 Part 2 Answer ${answer}`);
}

fs.readFile('input1.txt', (err, rawData) => {
    if (err) {
        throw err;
    }
    part1(rawData);
    part2(rawData);
});
