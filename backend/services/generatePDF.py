from reportlab.pdfgen import canvas
import io
import datetime

LEFT_MARGIN = 60
RIGHT_MARGIN = 60
TOP_MARGIN = 780
BOTTOM_MARGIN = 60
PAGE_HEIGHT = 842
LINE_HEIGHT = 15
ROW_HEIGHT = 22

def create_candidates_pdf(candidates):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    # Title page
    p.setFont("Helvetica-Bold", 28)
    p.setFillColorRGB(0.07, 0.18, 0.36)
    ceveai_header = "CEVEAI"
    ceveai_width = p.stringWidth(ceveai_header, "Helvetica-Bold", 28)
    p.drawString((595 - ceveai_width) / 2, PAGE_HEIGHT - 80, ceveai_header)
    p.setFillColorRGB(0, 0, 0)  

    # Title 
    p.setFont("Helvetica-Bold", 32)
    title = "CV ANALYSIS REPORT"
    title_y = (PAGE_HEIGHT // 2) + 60  
    p.drawString(LEFT_MARGIN, title_y, title)

    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    p.setFont("Helvetica", 14)
    bottom_y = BOTTOM_MARGIN + 60
    p.drawString(LEFT_MARGIN, bottom_y + 40, f"Date: {date_str}")
    p.drawString(LEFT_MARGIN, bottom_y + 20, f"Time: {time_str}")
    p.drawString(LEFT_MARGIN, bottom_y, "Generated by CeVeAI")
    p.showPage()

    def check_page_break(y, needed_space=LINE_HEIGHT):
        if y - needed_space < BOTTOM_MARGIN:
            p.showPage()
            y = TOP_MARGIN
        return y

    for candidate in candidates:
        y = TOP_MARGIN

        p.setFont("Helvetica-Bold", 20)
        candidate_name = str(candidate.get('candidate_name', ''))
        total_score_str = f"{candidate.get('total_score', '')}/10"
        
        p.drawString(LEFT_MARGIN, TOP_MARGIN, candidate_name)
      
        score_width = p.stringWidth(total_score_str, "Helvetica-Bold", 20)
        p.drawString(595 - RIGHT_MARGIN - score_width, TOP_MARGIN, total_score_str)
        y = TOP_MARGIN - 20

        p.setFont("Helvetica", 12)
        p.drawString(LEFT_MARGIN, y, candidate.get('filename'))
        y -= 18

      
        p.setFont("Helvetica-Bold", 30)
        total_score_str = f"{candidate.get('total_score', '')}/10"
       
        score_width = p.stringWidth(total_score_str, "Helvetica-Bold", 30)
        p.drawString(PAGE_HEIGHT - RIGHT_MARGIN - score_width, TOP_MARGIN, total_score_str)

        y -= 20

        p.setFont("Helvetica", 10)
        summary = candidate.get('summary', '')
        for line in split_text(summary, 100):
            y = check_page_break(y)
            p.drawString(LEFT_MARGIN, y, line)
            y -= LINE_HEIGHT

        y -= 40

        p.setFont("Helvetica-Bold", 10)
        p.drawCentredString(LEFT_MARGIN + 50, y, "Criteria")
        p.drawCentredString(LEFT_MARGIN + 120 + 40, y, "Score")
        p.drawString(LEFT_MARGIN + 200, y, "Reasoning")
        y -= LINE_HEIGHT
        p.setFont("Helvetica", 10)
        p.line(LEFT_MARGIN, y + 5, 595 - RIGHT_MARGIN, y + 5)
        y -= 5
        y -= 5

        for score in candidate.get("scores", []):
            y = check_page_break(y, needed_space=ROW_HEIGHT)
            p.drawCentredString(LEFT_MARGIN + 50, y, str(score.get('criterion', '')))
            p.drawCentredString(LEFT_MARGIN + 120 + 40, y, str(score.get('score', '')))
            explanation = score.get('explanation', '')
            explanation_lines = split_text(explanation, 60)
            if explanation_lines:
                p.drawString(LEFT_MARGIN + 200, y, explanation_lines[0])
                for expl_line in explanation_lines[1:]:
                    y -= LINE_HEIGHT
                    y = check_page_break(y, needed_space=ROW_HEIGHT)
                    p.drawString(LEFT_MARGIN + 200, y, expl_line)
            y -= ROW_HEIGHT

        p.showPage()  # Page break after each candidate

    p.save()
    buffer.seek(0)
    return buffer

def split_text(text, max_length):
    # Helper to split long text into lines of max_length
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 <= max_length:
            current_line += (" " if current_line else "") + word
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

def check_page_break(p, y, needed_space=LINE_HEIGHT):
    if y - needed_space < BOTTOM_MARGIN:
        p.showPage()
        y = TOP_MARGIN
    return y
