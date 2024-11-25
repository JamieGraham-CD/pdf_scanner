import PyPDF2
from pathlib import Path

def split_pdf(input_pdf_path, output_folder_path):
    # Create output folder if it doesn't exist
    Path(output_folder_path).mkdir(parents=True, exist_ok=True)

    # Open the PDF file
    with open(input_pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        total_pages = len(pdf_reader.pages)

        for page_num in range(total_pages):
            # Create a new PDF writer for each page
            pdf_writer = PyPDF2.PdfWriter()
            pdf_writer.add_page(pdf_reader.pages[page_num])

            # Save the individual page
            output_file = Path(output_folder_path) / f"page_{page_num + 1}.pdf"
            with open(output_file, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)

            print(f"Saved: {output_file}")

# Path to the input PDF file
input_pdf_path = "./pdfs/nrf_legacy_2022.pdf"  # Replace with your PDF path
# Folder to save the split pages
output_folder_path = "./pdfs/"  # Replace with your desired output folder

# Split the PDF
split_pdf(input_pdf_path, output_folder_path)


