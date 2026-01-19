# TOPSIS – CLI, Package & Web Service

This project implements the **TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)** method as:
- A Command Line Tool  
- A Python Package (PyPI)  
- A Web Service with file upload and email delivery  

It helps rank multiple alternatives based on multiple criteria using mathematical decision-making.

---

## What is TOPSIS?

TOPSIS selects the best option which is:
- Closest to the ideal best solution  
- Farthest from the ideal worst solution  

Used in finance, management, engineering, and ranking problems.

---

## Methodology (Short)

1. Take input data (1st column = alternatives, rest = criteria)  
2. Normalize each criterion column  
3. Multiply by weights  
4. Find ideal best and ideal worst  
5. Compute distance from both  
6. Calculate TOPSIS score  
7. Rank alternatives  

Higher score = better rank.

---

## Example Dataset

| Fund | P1 | P2 | P3 | P4 | P5 |
|------|----|----|----|----|----|
| M1 | 0.84 | 0.71 | 6.7 | 42.1 | 12.59 |
| M2 | 0.91 | 0.83 | 7.0 | 31.7 | 10.11 |
| ... | ... | ... | ... | ... | ... |

---

## Example Result (From Output File)

| Fund | Topsis Score | Rank |
|------|--------------|------|
| M5 | 0.972128 | 1 |
| M8 | 0.560092 | 2 |
| M6 | 0.547048 | 3 |
| M3 | 0.496361 | 4 |
| M7 | 0.395015 | 5 |
| M1 | 0.382109 | 6 |
| M2 | 0.366492 | 7 |
| M4 | 0.324792 | 8 |

**Best Option = M5 (Rank 1)**

---

## Result Graph Idea

Bar graph:
- X-axis: Alternatives  
- Y-axis: TOPSIS Score  
Highest bar = best choice.

---

## Features

- CLI with full validation  
- PyPI package installable via pip  
- Web service with email result delivery  
- Supports CSV and Excel  

---

## Author

Simran Kaur  

---

## License

Open-source, for academic use.
nd created for academic learning purposes.
