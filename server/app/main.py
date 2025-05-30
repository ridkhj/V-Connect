from services.generate_pdf import PdfGenerator
from app.scripts.data_extractor import SheetDataExtractor
from app.scripts.csv_extractor import CsvExtractor

extrator = CsvExtractor()
extrator.read_csv_in_pattern_folder()


leitorDados = SheetDataExtractor()
leitorDados.select_and_process_sheet_by_type()

geradorPdf = PdfGenerator()
