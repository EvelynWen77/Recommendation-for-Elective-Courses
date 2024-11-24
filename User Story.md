# User Stories & Components


## User Story 1

Tony is a college teacher specializing in Computer Science. He wants to make his class more appealing and attract more students. To achieve this, Tony plans to use a recommendation system to identify what content or features his class should include to increase enrollment. Being highly technical, Tony is familiar with all aspects of the system.

—

## Component: Recommendation Model Interaction Logic

### What it Does:
This component processes user data by passing it to the recommendation model and retrieves recommended course IDs based on the input.

### Inputs:
- **User Data**:
  - **History Course**: *(string)*
  - **Interest**: *(string)*
  - **Major**: *(string)*
  - **Grade**: *(int)*

### Outputs:
- **Recommended Course IDs**: *(list of strings)*

### Components Used:
- The frontend collects user input data, validates it, and sends the verified data to the recommendation system.

### Side Effects:
- None



—

# User Story 2

**Technician (Machine Learning Engineer):**  
As a Machine Learning Engineer, Kara needs to develop and maintain a course recommendation system that effectively suggests personalized course options to students. Her responsibilities include Training the Machine Learning Model, Managing External Data Sources, Updating the Model, and Ensuring Model Performance.

—

##Component: Model Training

### What it Does:
Trains the machine learning model using historical data of student enrollments, course information, and other relevant features to learn patterns that improve recommendation accuracy.

### Inputs:
- **training_data (dictionary):** Contains processed student histories, course features, and labels indicating course enrollments.
- **hyperparameters (dictionary):** Settings for model training, such as learning rate, number of epochs, and batch size.

### Specify Components:
- **Data Loader:** Manages the loading and batching of training data.
- **Model Architecture Definition:** Specifies the structure of the SASRec model.
- **Optimization Algorithm (e.g., Adam optimizer):** Updates model weights during training.

### Outputs:
- **trained_model (object):** The machine learning model is ready for inference.
- **training_logs (dictionary):** Metrics like loss and accuracy recorded during training.

### How it Uses Other Components:
- **Data Loader:** Supplies training data to the model.
- **Optimization Algorithm:** Minimizes the loss function to improve model predictions.
- **Logging Module:** Records training progress and performance metrics.

### Side Effects:
- Writes the trained model to persistent storage.
- Updates logs with training information for future reference.

——

