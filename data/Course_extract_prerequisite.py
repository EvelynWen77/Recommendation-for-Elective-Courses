import pandas as pd
import re
from sentence_transformers import SentenceTransformer, util

df = pd.read_excel('/Users/evelynwen/Desktop/CSE583/UW_Courses.xlsx') 

def extract_course_ids(prerequisite, course_id_list):
    valid_course_ids = set(course_id_list)
    course_ids = re.findall(r'[A-Z]+\s*[A-Z]*\s*\d+', str(prerequisite))
    valid_ids = [course_id for course_id in course_ids if course_id in valid_course_ids]
    return ', '.join(valid_ids)

df['Prerequisites'] = df['Detailed Course Prerequisite'].apply(lambda x: extract_course_ids(x, df['Course ID']))
prerequisite_col_index = df.columns.get_loc("Credits") + 1
df.insert(prerequisite_col_index, 'Prerequisites', df.pop('Prerequisites'))


keywords = [
    'Computation & Scientific Computing', 
    'Differential Equations & Dynamical Systems', 
    'Optimization', 
    'Algebra & Abstract Algebra', 
    'Probability & Stochastic Processes', 
    'Topology & Geometry', 
    'Analysis & Real Analysis', 
    'Complex Analysis & Complex Variables', 
    'Mathematical Modeling', 
    'Mathematical Biology', 
    'Numerical Analysis', 
    'Combinatorics & Discrete Mathematics', 
    'Computer-Aided Mathematics', 
    'Discrete Mathematics & Graph Theory', 
    'Mathematics Education & Career Development',
    'Computer Hardware & Architecture', 
    'Signal Processing & Communication', 
    'Control Systems & Optimization', 
    'Embedded & Real-Time Systems', 
    'Bioengineering & Neural Engineering', 
    'Quantum Computing & Information', 
    'Computer Vision & Image Processing', 
    'Artificial Intelligence & Machine Learning', 
    'Data Science & Data Engineering', 
    'Human-Computer Interaction & UI/UX', 
    'Computer Networks & Security', 
    'Software Development & Engineering', 
    'Database & Data Management', 
    'Robotics & Automation', 
    'Power Systems & Energy Engineering'
]

# Use Bert for Keywords align
model = SentenceTransformer('paraphrase-MiniLM-L6-v2') 

keyword_embeddings = model.encode(keywords, convert_to_tensor=True)

def match_keywords(course_name, course_description):
    
    # Align based on course_name and description
    full_text = f"{course_name} {course_description}"
    course_embedding = model.encode(full_text, convert_to_tensor=True)
    cosine_scores = util.cos_sim(course_embedding, keyword_embeddings).flatten()
    
    # Choose the most 3 rerelevant keywords
    top_indices = cosine_scores.argsort(descending=True)[:3]
    matched_keywords = [keywords[i] for i in top_indices]
    return ', '.join(matched_keywords)


df['Key Words'] = df.apply(lambda row: match_keywords(row['Course Name'], row['Course Description']), axis=1)

df.to_excel('/Users/evelynwen/Desktop/CSE583/UW_Courses_with_keywords.xlsx', index=False)

