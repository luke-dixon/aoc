// Advent of Code Day 7 Part 2
let fs = require('fs');

let setDifference = function (set1, set2) {
  // from https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set
  return new Set([...set1].filter(x => !set2.has(x)));
};

let data = fs.readFileSync('input7.txt', 'utf8');
data = data.split('\n');

// Discard entry from trailing \n
data.pop();

let steps = {};
let labels = new Set();
let requirements = new Set();

// Create each step
data.forEach(function (s) {
  if (s.length != 48) {
    return;
  }
  let stepLabel = s[5];
  let requirement = s[36];

  labels.add(stepLabel);
  requirements.add(requirement);

  if (steps[stepLabel] === undefined) {
    steps[stepLabel] = {
      label: stepLabel,
      requiredBy: [],
      requirements: []
    }
  }

  let step = steps[stepLabel];
  step.requiredBy.push(requirement);
});

// One step has no requirements, so wasn't created yet
let firstStepLabel;
for (firstStepLabel of setDifference(requirements, labels)) { break; }
steps[firstStepLabel] = { label: firstStepLabel, requiredBy: [], requirements: [] };

// Find which other steps are required by each step
for (let label of Object.keys(steps)) {
  for (let requirement of steps[label].requiredBy) {
    steps[requirement].requirements.push(label);
  }
}

// The length of the result should only be as long as the number of labels
const resultDoneLength = Object.keys(steps).length;
let stepsInProgress = [];
let result = [];

let minute = 0;

const createWorker = function () {
  return {
    idle: true,
    task: null,
    callback: function () {},
    startTask: function (step, callback) {
      this.idle = false;
      this.task = step.charCodeAt(0) - 4;
      this.callback = callback;
    },
    update: function () {
      if (this.idle) {
        return;
      }
      this.task -= 1;
      if (this.task === 0) {
        this.callback();
        this.idle = true;
      }
    }
  };
};

const workers = [];
for (let i = 0; i < 5; i += 1) {
  workers.push(createWorker());
}

while (result.length < resultDoneLength) {
  // Assign idle workers new steps
  for (let worker of workers) {
    if (!worker.idle) {
      continue;
    }
    // Start a worker on the first step alphabetically that has no requirements
    for (let label of Object.keys(steps).sort()) {
      let step = steps[label];
      if (stepsInProgress.indexOf(label) !== -1) {
        continue;
      }
      //console.log('step: ' + label + ', requirements length: ' + step.requirements.length);
      if (step.requirements.length === 0) {
        stepsInProgress.push(label);
        worker.startTask(label, function () {
          // When the task is done, add the result to the list of results
          result.push(label);
          delete steps[label];
          stepsInProgress.splice(stepsInProgress.indexOf(label), 1);

          // Remove this step as a requirement from other steps
          for (let otherLabel of Object.keys(steps)) {
            let otherStep = steps[otherLabel];
            let stepIdx = otherStep.requirements.indexOf(label);
            if (stepIdx !== -1) {
              otherStep.requirements.splice(stepIdx, 1);
            }
          }
        });
        break;
      }
    }
  }

  for (let worker of workers) {
    worker.update();
  }
  minute += 1;
}

console.log('Day 7 Part 2 Answer: ' + minute);
