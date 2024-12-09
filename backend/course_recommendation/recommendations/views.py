from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import boto3
import tensorflow as tf
import numpy as np
import pandas as pd
import pickle
from .models import Args, SASRecTrainer, process_student_data
import io

s3_client = boto3.client('s3')
bucket_name = 'cs583-source-data'

@csrf_exempt
def recommend_courses(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print(data)
            student_class = data.get("class")  
            student_major = data.get("major")
            student_id = data.get("id")  
            student_interest = data.get("interest", [])  
            courses_taken = data.get("coursesTaken", []) 

            if not isinstance(student_class, int) or not (0 <= student_class <= 4):
                return JsonResponse({"error": "Invalid class value"}, status=400)

            if not isinstance(student_major, int) or not (0 <= student_major < 4):
                return JsonResponse({"error": "Invalid major value"}, status=400)
            elif student_major == 0:
                student_major = 'Applied Mathematics'
            elif student_major == 1:
                student_major = 'Mathematics'
            elif student_major == 2:
                student_major = 'Electrical and Computer Engineering'
            else:
                student_major = 'Computer Science and Engineering'

            if not isinstance(student_interest, list) or len(student_interest) not in [1, 2]:
                return JsonResponse({"error": "Interest must have 1 or 2 items"}, status=400)

            if not isinstance(courses_taken, list):
                return JsonResponse({"error": "coursesTaken should be a list"}, status=400)

            if len(student_interest) == 1:
                student_interest.append('')
            courses_taken = ", ".join(courses_taken)
            print(courses_taken)

            student_data = pd.DataFrame([{
                "StudentID": student_id,
                "Courses": courses_taken, 
                "Interest_1": student_interest[0], 
                "Interest_2": student_interest[1], 
                "Grade": student_class, 
                "Major": student_major
            }])

            def download_from_s3(file_key):
                response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
                return response['Body'].read()
            mapping_data = pickle.loads(download_from_s3('mapping_data.pkl'))

            itemnum = mapping_data["itemnum"]
            gradenum = mapping_data["gradenum"]
            vocab_size = mapping_data["vocab_size"]
            args = Args()
            course_id_to_idx = mapping_data["course_id_to_idx"]
            course_data = mapping_data["course_data"]
            processed_new_students = process_student_data(student_data, course_id_to_idx)
            print(processed_new_students)
            trainer = SASRecTrainer(
                usernum=200, itemnum=itemnum, gradenum=gradenum, vocab_size=vocab_size, args=args, mode="inference"
            )

            # Load pre-trained weights
            trainer.model.load_weights('/home/ubuntu/backend/course_recommendation/recommendations/sasrec_weights')
            recommendations = trainer.recommend(processed_new_students, course_data, num_recommendations=10)

            recommended_course_ids = []
            for student_id, courses in recommendations:
                print(f"Recommendations for student {student_id}:")
                for _, course_id, score in courses:
                    print(f" - Course ID: {course_id}, Score: {score:.4f}")
                    recommended_course_ids.append(course_id)

            return JsonResponse({"recommended_course_ids": recommended_course_ids}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

