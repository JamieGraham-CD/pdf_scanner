from Models.gemini_models import GeminiModel
import vertexai
from vertexai.generative_models import GenerativeModel, Part
import csv

# TODO(developer): Update project_id and location
vertexai.init(project="cd-ds-384118", location="us-south1")


model = GenerativeModel("gemini-1.5-flash-002")


prompt = ''' 
You are a very professional document extractor specialist. Extract all text and tables into a csv format. 
<Rules>
- Interpret headings and make sure to align the rows and columns correctly.
- Remove commas from any numbers in cells in a table. 
- Wrap only the first row of column headers in quotes when saving the csv text.
- If the first row of column headers have commas in them, remove them. 
    - Example: "Apples, Oranges, or Pears" should be "Apples Oranges or Pears"
'''


pdf_file = Part.from_uri(
    uri="gs://data-extraction-services/zeroday/test-pdf/outputs/page_67.pdf",
    mime_type="application/pdf",
)
contents = [pdf_file, prompt]

response = model.generate_content(contents)
csv_text = response.text.replace("csv",'').replace("'''",'')


output_file = "output.csv"

with open(output_file, "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    for row in csv_text.splitlines():
        csv_writer.writerow(row.split(","))
        
print(f"CSV saved to {output_file}")
