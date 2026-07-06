# 🤖 AI / ML (Entry) — Baby Style (8 weeks)

**For:** Some Python basics. Want to work with AI. Heard it pays well.

**Time:** 3-4 hrs/day | **Goal:** Junior ML Engineer / AI Engineer

**Pay:** $70-100k | **Difficulty:** Medium-Hard

---

## Real Talk

- "AI Engineer" at entry level is actually: use APIs (OpenAI), clean data, run existing models, evaluate results
- You DON'T need a PhD. You DO need Python + SQL + basics of ML.
- Most entry AI jobs = "ML Engineer" where you run models other people designed
- Hot in 2026. Good pay. Less entry-level jobs than web dev but growing fast.

---

## 🗓️ Week 1 — Python + Math Refresher

### Day 1-2: Python for ML
- numpy: arrays, math operations, broadcasting
- `np.array()`, `.mean()`, `.std()`, `.reshape()`

**Do:** Create arrays. Add them. Multiply. Get mean and standard deviation.

### Day 3-4: pandas for ML
- Load data, clean, explore
- `df.describe()`, `df.corr()`, `df.groupby()`

**Do:** Load a dataset. Find correlations. Visualize with a heatmap.

### Day 5: Math basics (just enough)
- Linear algebra: vectors, matrices, dot product
- Calculus: derivative = slope of a line
- Statistics: mean, variance, normal distribution

**Do:** Multiply 2 matrices with numpy. Understand what each number means.

### Day 6-7: Jupyter notebooks
- Notebooks = code + text + charts in one file
- Used by every ML engineer

**Do:** Set up Jupyter. Create a notebook with code, markdown, and a chart.

---

## 🗓️ Week 2 — Machine Learning Basics

### Day 1: What is ML?
- Instead of writing rules, you show the computer examples
- It learns patterns from data
- Supervised = has labels (spam/not spam). Unsupervised = no labels (group customers).

**Do:** Watch "Machine Learning in 5 min" on YouTube.

### Day 2: scikit-learn
- The most popular ML library
- `from sklearn.linear_model import LinearRegression`
- Fit model → predict → evaluate

**Do:** Load a dataset. Train a linear regression model. Predict values.

### Day 3: Classification
- Predict a category (spam/not spam, cat/dog, yes/no)
- Logistic Regression, Decision Trees, Random Forest

**Do:** Train a classifier on the Iris dataset. Predict flower types.

### Day 4: Train/test split
- Don't test on the same data you trained on
- Split: 80% train, 20% test
- `from sklearn.model_selection import train_test_split`

**Do:** Split your data. Train on 80%. Test on 20%. Check accuracy.

### Day 5: Evaluation metrics
- Accuracy = correct / total
- Precision = of predicted positive, how many were right?
- Recall = of actual positive, how many did we catch?
- Confusion matrix = shows true/false positives/negatives

**Do:** Calculate accuracy, precision, recall for your model. Understand each.

### Day 6-7: ML project
**Do:** Build a classifier that predicts something:
- Titanic: survived/died
- Housing: price > median or not

---

## 🗓️ Week 3 — Deep Learning Basics

### Day 1: What is deep learning?
- Neural networks = layers of math that learn patterns
- More data + more layers = better results (usually)
- Used for: images, text, audio, complex patterns

**Do:** Watch "Neural Networks in 5 min" (3Blue1Brown or similar).

### Day 2: TensorFlow / PyTorch
- Two main frameworks. PyTorch is more popular in 2026.
- `import torch`
- Tensors = like numpy arrays but for GPU

**Do:** Install PyTorch. Create tensors. Add, multiply.

### Day 3: Simple neural network
- Input layer → hidden layers → output layer
- Forward pass = data goes in, prediction comes out

**Do:** Build a simple neural network. Train it on a small dataset.

### Day 4: Training loop
- Loss = how wrong is the prediction?
- Optimizer = adjusts weights to reduce loss
- Epoch = one pass through all data

**Do:** Write a training loop. Watch the loss go down. See accuracy go up.

### Day 5: Overfitting + regularization
- Overfitting = model memorizes instead of learning (good on train, bad on test)
- Fix: dropout, early stopping, more data, simpler model

**Do:** Intentionally overfit a model. Then apply techniques to fix it.

### Day 6-7: Practice
- Train a neural network on MNIST (handwritten digits)
- Goal: 90%+ accuracy

---

## 🗓️ Week 4 — LLMs + OpenAI API (💰 Most Valuable Skill)

### Day 1: What are LLMs?
- LLM = Large Language Model (GPT, Claude, Llama)
- Trained on massive text. Can write, summarize, answer questions.
- You don't train them. You USE them via API.

**Do:** Use ChatGPT. Try: summarize, write code, explain concept, translate.

### Day 2: OpenAI API
- `pip install openai`
- `client.chat.completions.create(model="gpt-4", messages=[...])`
- Send prompt → get response

**Do:** Write Python code that asks GPT to write a poem about cats.

### Day 3: Prompt engineering
- How you ask = what you get
- Be specific. Give examples. Set format.

**Do:** Write prompts that: extract names from text, classify sentiment, summarize articles.

### Day 4: Structured output
- Get JSON back from LLM (not plain text)
- Easy to use in your code

**Do:** Ask GPT to return JSON: `{"name": "...", "age": ..., "city": "..."}`

### Day 5: RAG (Retrieval Augmented Generation)
- Problem: GPT doesn't know YOUR data
- Solution: give it relevant context before asking
- "Here are my docs. Answer based on them."

**Do:** Build a simple RAG: load a PDF, split into chunks, find relevant chunks, ask GPT with context.

### Day 6-7: LLM project
**Do:** Build a "Chat with your data" app:
- Upload a document
- Ask questions about it
- GPT answers based on the document

---

## 🗓️ Week 5 — More ML Projects

### Day 1-2: Regression project
**Do:** Predict house prices:
- Dataset: California housing or Kaggle house prices
- Features: bedrooms, sqft, location, year
- Evaluate: RMSE, MAE, R²

### Day 3-4: Classification project
**Do:** Predict customer churn:
- Dataset: Telco customer churn (Kaggle)
- Features: contract type, tenure, charges
- Evaluate: accuracy, precision, recall, ROC curve

### Day 5-6: NLP project
**Do:** Sentiment analysis:
- Dataset: movie reviews (IMDB)
- Classify positive/negative
- Use TF-IDF + logistic regression, then compare with neural network

### Day 7: Deploy a model
- Save model: `pickle.dump(model, file)`
- Load it in a FastAPI app
- Create API endpoint: POST review → return sentiment

**Do:** Deploy your sentiment model as a web API.

---

## 🗓️ Week 6 — ML Engineering Skills

### Day 1: Feature engineering
- Good features = good model
- Create features from existing data (day of week, ratio, rolling average)
- Handle categorical data (one-hot encoding)
- Scale numerical data (StandardScaler)

**Do:** Take a raw dataset. Create 5 new features. See if accuracy improves.

### Day 2: Model selection
- Try multiple models: Logistic Regression, Random Forest, XGBoost, Neural Network
- Compare results. Pick the best.

**Do:** Train 4 models on the same data. Compare accuracy + training time.

### Day 3: Hyperparameter tuning
- Parameters you set before training (learning rate, tree depth)
- GridSearchCV = try all combinations automatically

**Do:** Use GridSearchCV to find best parameters for Random Forest.

### Day 4: ML pipelines
- `sklearn.pipeline.Pipeline` = chain steps together
- Scale → encode → train → predict
- One object handles everything

**Do:** Build a pipeline. Train. Save. Load. Predict.

### Day 5-6: MLOps basics
- MLflow = track experiments (what model, what params, what accuracy)
- Version control for models

**Do:** Set up MLflow. Log 5 experiments. Compare results.

### Day 7: Full pipeline
**Do:** Build end-to-end:
1. Load data
2. Feature engineering
3. Train model
4. Log with MLflow
5. Save model
6. Deploy with FastAPI

---

## 🗓️ Week 7 — Portfolio + Resume

### Day 1-3: Portfolio projects
- GitHub with 3 projects:
  1. ML model (classification + evaluation)
  2. LLM app (chat with your data / RAG)
  3. Deployed model (FastAPI + endpoint)

### Day 4-5: Resume
- 1 page. Keywords: Python, scikit-learn, PyTorch, LLMs, OpenAI API, RAG, MLflow, FastAPI, SQL, data cleaning

### Day 6-7: LinkedIn
- Headline: "Junior ML Engineer" or "AI Engineer"
- Add projects. Write about what you built.

---

## 🗓️ Week 8 — Job Hunt

- Roles: Junior ML Engineer, AI Engineer, Data Scientist (entry), ML Engineer
- LinkedIn, Indeed — 10 apps/day
- Also apply to "AI/ML" roles at startups (less strict on experience)

**Interview prep:**
- "Explain overfitting and how to prevent it"
- "What's the difference between supervised and unsupervised learning?"
- "Walk me through an ML project from start to finish"
- "How would you evaluate a classification model?"
- "What experience do you have with LLMs?"

---

> ✅ **AI/ML = hottest field but hardest entry.** Focus on LLM skills (RAG, API, prompt engineering) — that's where entry jobs are in 2026. Traditional ML roles want more experience. AI Engineer is the new entry point.
