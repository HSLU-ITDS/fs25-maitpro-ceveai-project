from reportlab.pdfgen import canvas
import io

def create_candidates_pdf(candidates):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    for candidate in candidates:
        y = 800  # Start near the top of the page for each candidate

        # Candidate header
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, y, f"Candidate #{candidate.get('index', '')}: {candidate.get('candidate_name', '')}")
        y -= 30

        # Filename
        p.setFont("Helvetica", 12)
        p.drawString(100, y, f"Filename: {candidate.get('filename', '')}")
        y -= 20

        # Total Score
        p.drawString(100, y, f"Total Score: {candidate.get('total_score', '')}")
        y -= 20

        # Summary
        p.drawString(100, y, "Summary:")
        y -= 15
        summary = candidate.get('summary', '')
        # Wrap summary text if it's too long
        for line in split_text(summary, 80):
            p.drawString(120, y, line)
            y -= 15

        y -= 10

        # Scores
        p.setFont("Helvetica-Bold", 12)
        p.drawString(100, y, "Scores:")
        y -= 20
        p.setFont("Helvetica", 12)
        for score in candidate.get("scores", []):
            score_line = f"{score.get('criterion', '')}: {score.get('score', '')}"
            p.drawString(120, y, score_line)
            y -= 15

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
