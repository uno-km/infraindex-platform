import asyncio
import os
import sys

from datetime import date

# Add root to python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from apps.batch.services.reporter.pdf_generator import PDFReporter

async def test():
    reporter = PDFReporter()
    file_path = await reporter.generate_report(date.today(), 'morning')
    print(f'Done: {file_path}')

if __name__ == "__main__":
    asyncio.run(test())
