import pandas as pd

df = pd.read_excel("/Users/evelynwen/Desktop/CSE583/UW_Courses_with_keywords.xlsx")
df.to_csv("UW_Courses_with_keywords.csv", index=False, quoting=1)

df = pd.read_excel("/Users/evelynwen/Desktop/CSE583/students_info.xlsx")
df.to_csv("students_info.csv", index=False, quoting=1)

df = pd.read_excel("/Users/evelynwen/Desktop/CSE583/Courses_Enrollment.xlsx")
df.to_csv("Courses_Enrollment.csv", index=False, quoting=1)

df = pd.read_excel("/Users/evelynwen/Desktop/CSE583/students_interest.xlsx")
df.to_csv("students_interest.csv", index=False, quoting=1)