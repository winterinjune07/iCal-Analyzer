# ICal Financial Planner

*Now a full-fledged program that imports a work schedule from an ics link and converts it into a data set including net pay, hours, and projected taxation*

---

*For something more like a template look through the commit history!*

## How it works

1. Run the init.sh file to setup the virtual environment.

2. In the .env file you add your ICS link, your payroll info, and your timezone and the program takes care of it.

3. It imports the ICS link and saves it as a standardized CSV file.

4. The main program takes that CSV file and analyzes its data using the payroll info you provided.

5. It outputs real info that you can use to begin to budget specific amounts of hours for work for certain objectives, and so much more!

6. It uses both an estimate based on previous hours worked per week and upcoming scheduled time off to forecast future paychecks!

### *Example Data*

| Period Start | Period End | Check Day  | Hours | Gross Pay | Net Pay |
| ------------ | ---------- | ---------- | ----- | --------- | ------- |
| 09-02-2026   | 09-15-2026 | 09-22-2026 | 75    | 1650      | 1368.74 |
| 09-16-2026   | 09-29-2026 | 10-06-2026 | 50    | 1100      | 912.49  |
| 09-30-2026   | 10-13-2026 | 10-20-2026 | 63    | 1386      | 1149.74 |

## **Caveat**

> **I only have it set to use tax info relevant for a Cincinnati resident**  

## Future Plans

- **Evantually I want to get enough time to make it able to pull tax info for more people, and have it more compatible with more forms of revenue / projections.**
