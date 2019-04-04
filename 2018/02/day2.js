const fs = require('fs');

const part1 = (rawData) => {
    let twos = 0;
    let threes = 0;

    for (const d of rawData.toString().trim().split('\n')) {
        const counter = {};
        for (const c of d) {
            if (!counter.hasOwnProperty(c)) {
                counter[c] = 0;
            }
            counter[c] += 1;
        }
        const values = Object.values(counter);
        if (values.includes(2)) {
            twos += 1;
        }
        if (values.includes(3)) {
            threes += 1;
        }
    }
    console.log(`Part 1 Answer: ${twos * threes}`);
};

const part2 = (rawData) => {
    const sortedData = rawData.toString().trim().split('\n').sort();
    for (let i = 0; i < sortedData.length; i += 1) {
        for (let j = i + 1; j < sortedData.length; j += 1) {
            let diff = 0;
            let diffIndex = 0;

            for (let c = 0; c < Math.min(sortedData[i].length, sortedData[j].length); c += 1) {
                if (sortedData[i][c] != sortedData[j][c]) {
                    diff += 1;
                    diffIndex = c;
                }
            }

            if (diff == 1) {
                console.log(`Part 2 Answer: ${sortedData[i].slice(0, diffIndex)}${sortedData[i].slice(diffIndex + 1)}`);
            }
        }
    }
};

fs.readFile('input2.txt', (err, rawData) => {
    if (err) {
        throw err;
    }
    part1(rawData);
    part2(rawData);
});
