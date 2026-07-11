
#AI Keyword & FAQ Generator

#Overview

AI Keyword & FAQ Generator is a Python CLI application that uses a Large Language Model (LLM) API to analyze input text and automatically generate important keywords along with frequently asked questions (FAQs) and their answers.

#Features

* Accepts long text as input
* Generates important keywords
* Generates FAQs with answers
* Handles invalid input and API errors
* Clean and modular Python code

##Bonus Features

* Custom number of keywords
* Export results to TXT or JSON
* Regenerate keywords and FAQs
* Structured JSON response parsing

#Technologies Used

* Python 3
* Gemini API / Groq API / OpenRouter API
* Requests library

##Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/ai-keyword-faq-generator.git
```

2. Navigate to the project folder:

```bash
cd ai-keyword-faq-generator
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Add your API key in the project configuration.

5. Run the application:

```bash
python main.py
```

##Project Structure

```text
ai-keyword-faq-generator/
│── main.py
│── api.py
│── utils.py
│── requirements.txt
│── sample_input.txt
│── sample_output.txt
│── README.md
│── .gitignore
```

##Sample Input

```
Artificial Intelligence is transforming healthcare by assisting doctors in disease diagnosis, medical image analysis, and patient care.
```

##Sample Output

###Keywords

* Artificial Intelligence
* Healthcare
* Disease Diagnosis
* Medical Imaging
* Patient Care

###FAQs

**Q:** How is AI used in healthcare?

**A:** AI assists healthcare professionals by improving diagnosis, analyzing medical images, and enhancing patient care.

##Prompt Used

The LLM is instructed to:

* Extract important keywords from the provided text.
* Generate relevant FAQs.
* Provide clear and concise answers.
* Return the response in a structured format for easy parsing.

#Error Handling

* Empty input validation
* Invalid API key handling
* Network/connection errors
* API rate limit handling

#Future Improvements

* Web interface
* PDF and DOCX support
* Multiple language support
* Save history of generated results

##License

This project is created for learning and internship purposes.
