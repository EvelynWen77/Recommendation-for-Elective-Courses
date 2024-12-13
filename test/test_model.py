"""
Course Recommendation System using SASRec (Self-Attentive Sequential Recommendation) Model

This module provides functionality for generating course recommendations for students
based on their historical course data and interests using a trained SASRec model.

The script loads pre-processed metadata and generates 
personalized course recommendations.

Dependencies:
- pandas
- pickle
- tensorflow (implied by the model)
"""
import pytest
import pandas as pd
import pickle
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from model import SASRecTrainer, process_student_data, Args

# Fixtures for shared setup
@pytest.fixture(scope="module")
def metadata():
    """Fixture to load metadata."""
    test_dir = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.abspath(os.path.join(test_dir, ".."))
    pkl_path = os.path.join(project_root, "src", "mapping_data.pkl")

    if not os.path.exists(pkl_path):
        pytest.fail(f"File not found: {pkl_path}")

    # Load metadata
    with open(pkl_path, "rb") as f:
        metadata = pickle.load(f)

    return metadata

@pytest.fixture(scope="module")
def trainer(metadata):
    """Fixture to initialize SASRecTrainer."""
    args = Args()
    trainer_instance = SASRecTrainer(
        usernum=metadata["usernum"],
        itemnum=metadata["itemnum"],
        gradenum=metadata["gradenum"],
        vocab_size=metadata["vocab_size"],
        args=args,
        mode="inference",
    )

    # Load weights
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    weights_path = os.path.join(project_root, "src", "sasrec_weights.weights.h5")
    if not os.path.exists(weights_path):
        pytest.fail(f"File not found: {weights_path}")

    trainer_instance.model.load_weights(weights_path)
    return trainer_instance

def test_metadata_loading(metadata):
    """Test that metadata values are loaded correctly."""
    assert isinstance(metadata["itemnum"], int)
    assert isinstance(metadata["gradenum"], int)
    assert isinstance(metadata["vocab_size"], int)
    assert isinstance(metadata["course_id_to_idx"], dict)
    assert isinstance(metadata["course_data"], dict)

def test_recommendation_generation(trainer, metadata):
    """Test that recommendations are generated correctly."""
    new_student_data = pd.DataFrame([{
        "StudentID": "S0888",
        "Courses": "MATH 209, MATH 207, MATH 125",
        "Interest_1": "Computer Science",
        "Interest_2": "Mathematics",
        "Grade": "2",
        "Major": "Engineering"
    }])

    processed_new_students = process_student_data(new_student_data, metadata["course_id_to_idx"])
    recommendations = trainer.recommend(processed_new_students, metadata["course_data"], num_recommendations=5)

    assert len(recommendations) > 0