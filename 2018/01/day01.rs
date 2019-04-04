use std::fs::File;
use std::io::Read;
use std::io::BufReader;
use std::collections::HashSet;

fn raw_data_to_numbers(raw_data: &String) -> Vec<i32> {
    let split_data: Vec<&str> = raw_data.trim().split('\n').collect();
    let mut number_list: Vec<i32> = Vec::new();
    for element in split_data.iter() {
        let number: i32 = element.parse().unwrap();
        number_list.push(number);
    }
    return number_list;
}

fn part1(raw_data: &String) {
    let number_list: Vec<i32> = raw_data_to_numbers(raw_data);
    let answer: i32 = number_list.iter().sum();
    println!("Part 1 Answer: {:?}", answer);
}

fn part2(raw_data: &String) {
    let number_list: Vec<i32> = raw_data_to_numbers(raw_data);
    let mut found = false;
    let mut frequency = 0;
    let mut frequencies = HashSet::new();
    frequencies.insert(frequency);

    while !found {
        for element in number_list.iter() {
            frequency += element;
            if frequencies.contains(&frequency) {
                found = true;
                break;
            }
            frequencies.insert(frequency);
        }
    }
    println!("Part 2 Answer: {}", frequency);
}

fn main() -> std::io::Result<()> {
    let file = File::open("input1.txt")?;
    let mut buf_reader = BufReader::new(file);
    let mut contents = String::new();
    buf_reader.read_to_string(&mut contents)?;
    part1(&contents);
    part2(&contents);
    Ok(())
}
