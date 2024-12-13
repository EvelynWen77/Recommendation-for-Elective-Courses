from setuptools import setup, find_packages

setup(
    name="course_recommendation_system",
    version="1.0.0",
    description="Course Recommendation System using SASRec Model",
    author="Zimo.Wen",
    author_email="zimowen19@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "tensorflow>=2.0",
        "numpy",
        "pandas",
        "scikit-learn"
    ],
    entry_points={
        "console_scripts": [
            "initialize_project=src.model:main",  # Replace `main` with the actual entry point in your file
        ],
    },
)