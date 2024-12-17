# Dining Philosophers Problem

## Authors
- Mohamed Tarek Taha Ahmed
- Ahmed Mohamed Maged
- Wesam Ahmed Hassan
- Mahmoud Ahmed AbdelAziz
- Mahmoud Osama Ibrahim

## For
- Helwan University
- Cybersecurity Diploma
- Faculty of Computer and Artificial Intelligence

## Description
This project simulates the Dining Philosophers problem using Python's multithreading. It avoids deadlock and starvation through proper resource management.

## Requirements
- Python 3.x

## How to Run
1. Clone the repository.
2. Run the script using `python dining_philosophers.py`.

## Solution Details
- The philosophers alternate between thinking and eating.
- A priority lock is used to prevent deadlock and starvation.

## Examples
- For deadlock prevention, the priority lock ensures that philosophers cannot hold one chopstick while waiting for another.
- For starvation prevention, philosophers retry eating if they cannot acquire both chopsticks.

## License
This project is licensed under the MIT License.

