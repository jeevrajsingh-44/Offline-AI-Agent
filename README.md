# Offline AI Agent

A simple autonomous question-answering web application built with Python and Flask.

The system answers questions using a growing local dataset.  
If a question already exists in the dataset, the stored answer is returned immediately.  
If the question is not found, the system searches the internet, retrieves relevant information, and stores the new answer in the dataset.

Over time, the dataset grows, allowing the application to answer more questions directly from its local knowledge base.

---

# Benefits

This project provides several practical benefits:

1. **Automatic Knowledge Growth**  
   The system learns from new questions and stores answers for future queries, building its own knowledge base over time.

2. **Reduced Internet Dependency**  
   Frequently asked questions are answered locally, reducing repeated web searches and saving bandwidth.

3. **Hands-on Experience with AI Concepts**  
   Demonstrates memory layers (dataset), fuzzy matching for approximate reasoning, and tool-augmented intelligence using web search and Wikipedia.

4. **Prototype for Real-World Applications**  
   Can be extended for internal Q&A bots, automated FAQ systems, or as a base for more advanced AI assistants.

---

# How It Works

The system workflow is simple:

1. User enters a question through the web interface.
2. The application checks the local dataset (`qa_dataset.csv`).
3. If a similar question is found:
   - The stored answer is returned immediately.
4. If no match is found:
   - The system searches the internet using DuckDuckGo.
   - If needed, Wikipedia is used as a fallback source.
5. The retrieved answer is stored in the dataset.
6. Future queries for the same or similar question are answered directly from the dataset.

This creates a **self-growing knowledge base**, gradually reducing dependence on web searches.

---

# Key Features

- Local dataset knowledge base using CSV  
- Fuzzy matching to detect similar questions  
- Internet search using DuckDuckGo  
- Wikipedia fallback for additional reliability  
- Automatic dataset expansion  
- Flask-based web interface  

---

# Project Structure
