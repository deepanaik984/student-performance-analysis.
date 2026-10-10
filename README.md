# Student Performance Analysis

An analysis of secondary school student performance using the UCI Student Performance dataset,
done in Python (pandas, Matplotlib) in a Jupyter notebook.

## Dataset

UCI Student Performance (student-mat.csv): 395 secondary school students from two Portuguese
schools, mathematics course. The final grade (G3) is scored from 0 to 20.

## Questions answered

1. Do students with more absences tend to get lower final grades?
2. How does study time relate to the final grade?
3. Do students with past failures perform worse?
4. What share of students pass, and what do students who don't pass have in common?

## Approach

- Checked the data for missing values, duplicates and zero final grades (none missing, none
  duplicated, 38 students with a final grade of 0).
- Defined a pass as a final grade of at least 10. This is my own project rule, not part of the
  dataset, and I tested how the results change with other pass marks.
- Compared groups with groupby, calculated correlations and drew charts with Matplotlib.
- Added a short extra check on whether a low first-period grade flags students who later
  don't pass.

## Key findings

- 67.09% of all 395 students passed; 74.23% when the 38 students with a final grade of 0 are
  excluded.
- All 38 students with a final grade of 0 have 0 recorded absences, which hid the absences
  pattern. The analyses of absences, study time and past failures therefore use the 357
  students with a final grade above 0.
- Among those 357 students, absences show a weak negative association with final grade
  (correlation -0.21).
- Past failures show the strongest pattern: average final grade falls from 11.94 (no past
  failures) to 8.27 (three or more).
- Study time shows only a small, uneven difference in grades.
- Students who did not pass had more past failures and higher absences than those who passed.
- A first-period grade below 10 was an early indicator: 34.2% of those students passed,
  compared with 92.3% of those who scored 10 or above.
- The pass rate depends strongly on the pass mark chosen (about 82% at 8, 67% at 10, 41% at 12).
- ![Absences vs final grade](chart_absences_vs_grade.png)
  ![Study time](chart_study_time.png)
  ![Past failures](chart_past_failures.png)

## Limitations

- The data is observational, so the results show associations, not causes.
- It covers one course (mathematics) in two schools, so it may not apply elsewhere.
- The pass mark of 10 is my own rule.
- The reason for the zero final grades is not documented, and some groups are small (for
  example, 11 and 12 students with two or three past failures).

## Files

- student_performance_analysis_final.ipynb: the analysis notebook
- student-mat.csv: the dataset

## How to run

pip install pandas matplotlib notebook
jupyter notebook student_performance_analysis_final.ipynb

Keep student-mat.csv in the same folder as the notebook. The file uses semicolons as
separators, so it is loaded with sep=";".

## Data source and licence

Cortez, P. (2014). Student Performance. UCI Machine Learning Repository.
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0):
https://creativecommons.org/licenses/by/4.0/legalcode
