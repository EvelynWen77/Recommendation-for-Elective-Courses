# User Stories & Components


## User Story 1

Tony is a college teacher specializing in Computer Science. He wants to make his class more appealing and attract more students。 Students will interact with the recommendation system through the university’s online portal. By entering their interests, academic progress, and preferences, the system will generate personalized course recommendations. Tony plans to use these recommendations to identify what content or features his class should include to increase enrollment.


## Component: Recommendation Model Interaction Logic

### What it Does:
This component processes user data by passing it to the recommendation model and retrieves recommended course IDs based on the input.

### Inputs:
- **User Data**:
  - **History Course**: *(list of strings)*
  - **Interest**: *(list of string)*
  - **Major**: *(string)*
  - **Grade**: *(int)*

### Outputs:
- **Recommended Course IDs**: *(list of strings)*

### Components Used:
- **Frontend Validation Module:** Ensures input data is complete and valid
- **Database Module:** Queries course and student information
- **Recommendation Engine:** Uses user data to generate recommendations

### Side Effects:
- Logs user input and recommendation results for future analysis
- Schedules retraining tasks based on user interaction data



## User Story 2
 
As a Machine Learning Engineer, Kara needs to develop and maintain a course recommendation system that effectively suggests personalized course options to students. Her responsibilities include Training the Machine Learning Model, Managing External Data Sources, Updating the Model, and Ensuring Model Performance.


## Component: Model Training Module

### What it Does:
Trains the machine learning model using historical data of student enrollments, course information, and other relevant features to learn patterns that improve recommendation accuracy.

### Inputs:
- **training_data (dictionary):** Contains processed student histories, course features, and labels indicating course enrollments
- **hyperparameters (dictionary):** Settings for model training, such as learning rate, number of epochs, and batch size

### Outputs:
- **trained_model (object):** The machine learning model is ready for inference
- **training_logs (dictionary):** Metrics like loss and accuracy recorded during training

### Components Used:
- **Data Loader:** Supplies training data to the model
- **Optimization Algorithm:** Minimizes the loss function to improve model predictions
- **Logging Module:** Records training progress and performance metrics

### Side Effects:
- Writes the trained model to persistent storage
- Updates logs with training information for future reference


## User Story 3

As a System Administrator, Tom needs to monitor and manage the university course recommendation system to ensure its stability and reliability. This includes creating and managing user accounts, updating course and student data, monitoring system performance, and resolving errors in real time to provide a seamless experience for users.

## Component: System Monitoring and Maintenance Module

### What it Does:
This component enables the administrator to monitor the system's health, manage user accounts, and update key datasets to ensure smooth operation of the recommendation system.

### Inputs:
- **Admin Credentials:** Username (string) and Password (string)
- **Action:** User Management Requests and Data Update Requests

### Outputs:
- **Success/Failure Status:** Confirmation message for user account actions and data updates
- **Performance Reports:** Detailed logs of any errors encountered during operation

### Components Used:
- **System Performance Monitoring Module:** Tracks server health, database performance, and error logs
- **Database Update Module:** Processes course and student data uploads and synchronizes with the database

### Side Effects:
- Automatically logs all actions performed by the administrator
