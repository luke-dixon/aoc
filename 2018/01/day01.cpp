#include <fstream>
#include <iostream>
#include <numeric>
#include <set>
#include <string>
#include <vector>

using namespace std;

void part1(vector<int> numbers) {
    cout << "Part 1 Answer: " << accumulate(numbers.begin(), numbers.end(), 0, plus<int>()) << endl;
}

//fn part2(raw_data: &String) {
//    let number_list: Vec<i32> = raw_data_to_numbers(raw_data);
//    let mut found = false;
//    let mut frequency = 0;
//    let mut frequencies = HashSet::new();
//    frequencies.insert(frequency);
//
//    while !found {
//        for element in number_list.iter() {
//            frequency += element;
//            if frequencies.contains(&frequency) {
//                found = true;
//                break;
//            }
//            frequencies.insert(frequency);
//        }
//    }
//    println!("Part 2 Answer: {}", frequency);
//}
void part2(vector<int> numbers) {
    bool found = false;
    int frequency = 0;
    set<int> frequencies;
    frequencies.insert(frequency);

    while (!found) {
        for (vector<int>::iterator it = numbers.begin(); it != numbers.end(); ++it) {
            frequency += *it;
            if (frequencies.find(frequency) != frequencies.end()) {
                found = true;
                break;
            }
            frequencies.insert(frequency);
        }
    }
    cout << "Part 2 Answer: " << frequency << endl;
}

int main(int argc, char *argv[]) {
    int rc = 0;

    ifstream file("input1.txt");
    if (file.is_open()) {
        string line;
        vector<int> numbers = {};
        while (getline(file, line)) {
            numbers.push_back(stoi(line));
        }
        part1(numbers);
        part2(numbers);
    } else {
        cerr << "Unable to open file" << endl;
        rc = -1;
    }

    return rc;
}
