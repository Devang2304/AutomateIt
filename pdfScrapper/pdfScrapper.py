import pymupdf
from langchain_google_genai import GoogleGenerativeAI
import os

class pdfScrapper:
    def __init__(self):
        self.llm = GoogleGenerativeAI(model="gemini-2.0-flash",google_api_key='')
    
    def getPdfText(self, pdf_path: str) -> str:
        print("Getting PDF text...")
        try:
            doc = pymupdf.open(pdf_path)

            extracted_text = ""
            for page in doc:
                extracted_text += page.get_text()
            return extracted_text
        except Exception as e:
            return f"Error getting PDF text: {str(e)}"
    
    def generateQuestions(self,pdf_path: str)->str:
        text = self.getPdfText(pdf_path=pdf_path)
        print("Extracted text: ",text)
        print("Generating questions...")
        prompt = f"""
        text data : {text}
       Given the above text data extracted from a PDF document, 
       identify all key topics discussed within the text. 
       For each identified topic, generate a set of interview 
       questions designed to assess a candidate's knowledge in
       a professional interview setting specific to the topic. Ensure that no significant
       topic from the provided text is omitted and that the questions are relevant, appropriately
       challenging, and diverse in type.
       Return the result in a JSON format.
        """
        response = self.llm.invoke(prompt)
        return response

def main():
    pdfscrapper = pdfScrapper()
    pdfPath = input("Enter the video url: ")
    generatedQuestionsJson = pdfscrapper.generateQuestions(pdfPath)
    if not os.path.exists("generatedQuestions.json"):
        os.makedirs("generatedQuestions.json")
    with open("generatedQuestions.json", "w") as file:
        file.write(generatedQuestionsJson)
    print("Questions generated...")

if __name__ == "__main__":
    main()