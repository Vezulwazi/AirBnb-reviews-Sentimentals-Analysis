# Airbnb Reviews Sentiment Analysis

A multi-stage sentiment analysis project that classifies Airbnb user reviews into sentiment categories using classical machine learning, deep learning, and LLM-based approaches. The project also includes an interactive dashboard for exploring results and visualizations.

---

## Dataset

The dataset consists of Airbnb user reviews:

- Raw Data: `Dataset/User Review/User_reviews.csv`
- Cleaned Data: `Dataset/Cleaned Data/reviews.csv`

The dataset contains textual user reviews used for sentiment classification after preprocessing and cleaning.

---

## Project Overview

This project implements a complete sentiment analysis pipeline:

- Data preprocessing and text cleaning
- Feature extraction using TF-IDF
- Classical machine learning models
- Deep learning-based sentiment classification
- LLM-based sentiment analysis comparison
- Interactive dashboard for visualization and insights

---

## Tech Stack

- Python
- Pandas
- NumPy
- Scikit-learn:
  - Logistic Regression
  - Random Forest
  - Decision Tree
  - KNN
  - AdaBoost
  - Gradient Boosting
  - Support Vector Machine (SVM)
- TF-IDF Vectorization
- Deep Learning (Notebook-based implementation)
- LLM-based classification
- Plotly & Dash (Interactive dashboard)
- Joblib / Pickle (Model persistence)

---

## Results

Multiple approaches were evaluated for sentiment classification:

- Classical ML models using TF-IDF features
- Deep learning models for improved representation learning
- LLM-based sentiment classification for comparison

Overall, the project demonstrates the trade-offs between traditional machine learning, deep learning, and LLM-based approaches for text sentiment analysis. Detailed performance metrics and comparisons are available in the notebooks.

---

## Project Structure

```text id="ai7k3m"
Airbnb Reviews Sentiment Analysis/
│
├── Dataset/
│   ├── User Review/
│   │   └── User_reviews.csv
│   └── Cleaned Data/
│       └── reviews.csv
│
├── 1_dataPreprocessing.ipynb
├── 2_machineLearning.ipynb
├── 3_deepLearning.ipynb
├── 4_LLM.ipynb
├── dashboard.py
├── requirements.txt
└── README.md
