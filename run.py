import pandas as pd
from model import SASRecTrainer, process_student_data, Args
import pickle
import os


with open("mapping_data.pkl", "rb") as f:
    metadata = pickle.load(f)

itemnum = metadata["itemnum"]
gradenum = metadata["gradenum"]
vocab_size = metadata["vocab_size"]
course_id_to_idx = metadata["course_id_to_idx"]
course_data = metadata["course_data"]
usernum = metadata["usernum"]
args = Args()
# upload new
new_student_data = pd.DataFrame([{
    "StudentID": "S0888",                        
    "Courses": "MATH 209, MATH 207, MATH 125, MATH 124, MATH 208, MATH 126, MATH 125, MATH 124, MATH 134, E E 241, CSE 122, CSE 123, E E 280, E E 215, MATH 136, E E 242, MATH 207, MATH 282",        
    "Interest_1": " Computer-Aided Mathematics",                
    "Interest_2": " Mathematics Education & Career Development",            
    "Grade": "2",                        
    "Major": "Computer Science and Engineering"                
}])

processed_new_students = process_student_data(new_student_data, course_id_to_idx)

# initialize
trainer = SASRecTrainer(
    usernum=usernum, itemnum=itemnum, gradenum=gradenum, vocab_size=vocab_size, args=args, mode="inference"
)

# Load pre-trained weights
trainer.model.load_weights("sasrec_weights.weights.h5")

# generate rec
recommendations = trainer.recommend(processed_new_students, course_data, num_recommendations=10)

recommended_course_ids = []
for student_id, courses in recommendations:
    print(f"Recommendations for student {student_id}:")
    for _, course_id, score in courses:
        print(f"  - Course ID: {course_id}, Score: {score:.4f}")
        recommended_course_ids.append(course_id)
print(recommended_course_ids)
print(max_text_len)