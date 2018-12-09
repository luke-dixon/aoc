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
let result = [];
while (result.length < resultDoneLength) {
  // Add the first step alphabetically that has no requirements
  for (let label of Object.keys(steps).sort()) {
    let step = steps[label];
    if (step.requirements.length === 0) {
      result.push(label);
      delete steps[label];
      break;
    }
  }

  // Remove the step we just added from all the requirements
  let lastStepAdded = result[result.length - 1];
  for (let label of Object.keys(steps)) {
    let step = steps[label];
    let stepIdx = step.requirements.indexOf(lastStepAdded);
    if (stepIdx !== -1) {
      step.requirements.splice(stepIdx, 1);
    }
  }
}

console.log('Day 7 Part 1 Answer: ' + result.join(''));
