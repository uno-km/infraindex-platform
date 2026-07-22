import io
from typing import Any
from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import StreamingResponse
import openpyxl
from openpyxl.styles import Font, PatternFill
from docx import Document
from datetime import datetime

from apps.api.core.database import get_db
from apps.api.core.ai_service import generate_market_analysis

router = APIRouter()

@router.get("/excel")
async def export_excel(gpu_model_id: str = "H100", db: AsyncSession = Depends(get_db)) -> Any:
    """
    Exports the time-series pricing data as a beautifully styled Excel file.
    (Requirement: "짜치게 csv 말고 엑셀로 그리고 백엔드 단에서 이쁘게 정리해서")
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "GPU Price Data"
    
    # Headers
    headers = ["Date", "Provider", "GPU Model", "Min Price", "Avg Price", "Max Price"]
    ws.append(headers)
    
    # Styling Headers
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
    for cell in ws[1]:
        cell.font = header_font
        cell.fill = header_fill
        
    # Mock data insertion (In prod, fetch from DB)
    mock_data = [
        ["2026-07-20", "Vast.ai", gpu_model_id, 1.85, 1.95, 2.10],
        ["2026-07-21", "Vast.ai", gpu_model_id, 1.90, 2.05, 2.20],
        ["2026-07-22", "Vast.ai", gpu_model_id, 1.88, 2.00, 2.15],
    ]
    for row in mock_data:
        ws.append(row)
        
    # Auto-adjust column width
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column].width = adjusted_width

    # Save to memory
    stream = io.BytesIO()
    wb.save(stream)
    stream.seek(0)
    
    filename = f"{gpu_model_id}_pricing_{datetime.now().strftime('%Y%m%d')}.xlsx"
    return StreamingResponse(
        stream, 
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.get("/word")
async def export_word(db: AsyncSession = Depends(get_db)) -> Any:
    """
    Exports a Daily Briefing as a Microsoft Word Document.
    (Requirement: "word를 통해서 실시간으로 보고서 작성하게")
    """
    doc = Document()
    doc.add_heading('InfraIndex Daily Macro Briefing', 0)
    
    date_str = datetime.now().strftime('%Y-%m-%d %H:%M')
    doc.add_paragraph(f'Report Generated: {date_str}')
    
    # 1. GPU Price Trend
    doc.add_heading('1. GPU Market Price Trend (H100)', level=1)
    doc.add_paragraph('The average price for H100 on community clouds (Vast.ai) has stabilized around $2.00/hr.')
    
    # Table for GPU
    table = doc.add_table(rows=1, cols=3)
    table.style = 'Table Grid'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Provider'
    hdr_cells[1].text = 'Model'
    hdr_cells[2].text = 'Avg Price ($/hr)'
    
    row_cells = table.add_row().cells
    row_cells[0].text = 'Vast.ai'
    row_cells[1].text = 'H100'
    row_cells[2].text = '$2.00'
    
    # 2. Daily Briefing text generated dynamically by AI
    doc.add_heading('2. AI Macro Insight & Analysis', level=1)
    
    # We fetch the JSON data first
    brief_data = await get_daily_brief_json()
    
    # Call the LLM to generate the report
    ai_text = await generate_market_analysis(
        news_data=brief_data["news"],
        power_data=brief_data["power"],
        memory_data=brief_data["memory"]
    )
    
    # Split the AI text into paragraphs
    for para in ai_text.split('\n\n'):
        doc.add_paragraph(para.strip())

    stream = io.BytesIO()
    doc.save(stream)
    stream.seek(0)
    
    filename = f"InfraIndex_Daily_Brief_{datetime.now().strftime('%Y%m%d')}.docx"
    return StreamingResponse(
        stream,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.get("/daily-brief")
async def get_daily_brief_json() -> Any:
    """
    Returns the Macro Intelligence Briefing as JSON for the web dashboard.
    """
    return {
        "date": datetime.now().strftime('%Y-%m-%d'),
        "news": [
            {"title": "AWS announces $10B investment in Mississippi datacenter campuses", "source": "TechCrunch", "date": "2026-07-22"},
            {"title": "Korean authorities restrict new high-density power permits in Seoul", "source": "Bloomberg", "date": "2026-07-21"},
            {"title": "Liquid cooling standardizations proposed for next-gen AI clusters", "source": "DataCenter Dynamics", "date": "2026-07-20"}
        ],
        "power": [
            {"region": "US - Texas (ERCOT)", "cost_per_kwh_usd": 0.08, "trend": "stable"},
            {"region": "US - Virginia (PJM)", "cost_per_kwh_usd": 0.09, "trend": "rising"},
            {"region": "South Korea (KEPCO)", "cost_per_kwh_usd": 0.12, "trend": "rising"}
        ],
        "memory": [
            {"component": "DDR5 128GB R-DIMM", "price_usd": 320.00, "status": "stable"},
            {"component": "HBM3E (Estimated per stack)", "price_usd": 4500.00, "status": "severe_shortage"},
            {"component": "GDDR6 16GB", "price_usd": 45.00, "status": "stable"}
        ]
    }
