import pandas as pd
import random
import re

courses_df = pd.read_excel('/Users/evelynwen/Desktop/CSE583/UW_Courses_with_keywords.xlsx')

# Generate students information
def generate_students(num_students=50):
    majors = courses_df['Major'].unique().tolist()
    students = []
    for i in range(num_students):
        student_id = f"S{i+1:04d}"
        name = f"Student_{i+1}"
        grade = random.randint(1, 5) 
        major = random.choice(majors)
        students.append([name, student_id, grade, major])
    return pd.DataFrame(students, columns=["Name", "ID", "Grade", "Major"])

# Extract the prerequisites
def extract_prerequisites(prereq_str):
    if pd.notna(prereq_str):
        return re.findall(r'[A-Z]+\s*[A-Z]*\s*\d+', prereq_str)
    return []

# Select courses and adjust the quota
def select_courses_for_grade(grade, major, selected_courses, course_quota, student_grade):
    course_pool = courses_df[courses_df['Course ID'].str.contains(rf'\b{grade}\d{{2}}\b')]
    major_courses = course_pool[course_pool['Major'] == major]['Course ID'].tolist()
    non_major_courses = course_pool[course_pool['Major'] != major]['Course ID'].tolist()
    
    while course_quota[grade] > 0:
        # Random choose course with 90% belong to major courses
        if random.random() < 0.9 and major_courses:
            course = random.choice(major_courses)
        elif non_major_courses:
            course = random.choice(non_major_courses)
        else:
            break 
        
        # Already selected, skip
        if course in selected_courses:
            continue
        
        add_course_with_prereqs(course, selected_courses, course_quota, student_grade)
    
    return selected_courses

# Add course with prerequisite and adjust the quota for each grade
def add_course_with_prereqs(course, selected_courses, course_quota, student_grade):
    
    # Get course level
    match = re.search(r'\b(\d)', course)
    if match:
        course_grade = int(match.group(1))
    else:
        print(f"Warning: Could not determine grade for course {course}")
        return

    # Check quota for corresponding level
    if course_quota.get(course_grade, 0) <= 0:
        return

    # Add course and decrease quota
    selected_courses.append(course)
    course_quota[course_grade] -= 1
    
    # Check prerequisite
    prerequisites = courses_df[courses_df['Course ID'] == course]['Prerequisites'].values
    if prerequisites.size > 0:
        prereq_list = extract_prerequisites(prerequisites[0])

        # Special rule for graduate student
        if student_grade == 5:
            prereq_list = [prereq for prereq in prereq_list if re.search(r'\b5\d{2}\b', prereq)]
        
        # Add 1-2 prerequisite courses
        for prereq in prereq_list[:2]:  
            add_course_with_prereqs(prereq, selected_courses, course_quota, student_grade)

# Generate history
def generate_course_history(students_df):
    course_history = []
    for _, student in students_df.iterrows():
        student_id = student['ID']
        grade = student['Grade']
        major = student['Major']
        
        course_quota = {g: 9 for g in range(1, grade + 1)}
        selected_courses = []
        
        for current_grade in range(grade, 0, -1):
            select_courses_for_grade(current_grade, major, selected_courses, course_quota, grade)
        
        final_courses = selected_courses[:9 * grade if grade < 5 else 9]
        course_history.append([student_id, grade, ', '.join(final_courses)])
    
    return pd.DataFrame(course_history, columns=["ID", "Completed Grade", "Courses"])


students_df = generate_students(200)
course_history_df = generate_course_history(students_df)

students_df.to_excel("students_info.xlsx", index=False)
# course_history_df.to_excel("course_history.xlsx", index=False)


# Expanded the History into multiple records
expanded_records = []
for index, row in course_history_df.iterrows():
    student_id = row["StudentID"]
    completed_grade = row["Completed Grade"]
    courses = row["Courses"].split(", ")

    for course in courses:

        match = re.search(r'\b(\d)', course)
        if match:
            course_level = int(match.group(1))
        else:
            continue 

        if completed_grade == 5:
            selection_year = 2023
        else:
            selection_year = 2023 - (completed_grade - course_level)

        expanded_records.append({
            "StudentID": student_id,
            "CourseID": course,
            "SelectionDate": f"{selection_year}-09-26" 
        })

expanded_df = pd.DataFrame(expanded_records)
expanded_df.to_excel("Courses_Enrollment.xlsx")
