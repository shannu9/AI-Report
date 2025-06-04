from fpdf import FPDF
import matplotlib.pyplot as plt
import os
import uuid

class PDFReport:
    def __init__(self, output_path="output"):
        self.output_path = output_path
        os.makedirs(output_path, exist_ok=True)

    def save_plot(self, fig, filename):
        path = os.path.join(self.output_path, filename)
        fig.savefig(path, bbox_inches="tight")
        plt.close(fig)
        return path

    def add_watermark(self, pdf, text="Shanmukh"):
        pdf.set_text_color(240, 240, 240)  # Light gray
        pdf.set_font("Arial", "B", 40)

        # Simulate diagonal by placing same text multiple times diagonally
        for i in range(0, 300, 50):
            pdf.set_xy(i - 50, i)
            pdf.cell(200, 10, text, ln=False)

        pdf.set_text_color(0, 0, 0)  # Reset to default

    def create_pdf(self, summary, strategy, insights, plots, table_data):
        pdf = FPDF()
        
        # Page 1: Summary
        pdf.add_page()
        self.add_watermark(pdf)
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, "Business Analysis Report", ln=True, align="C")
        pdf.set_font("Arial", "", 12)

        pdf.ln(10)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, "Executive Summary", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 10, summary)

        pdf.ln(5)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, "Recommended Strategies", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 10, strategy)

        pdf.ln(5)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, "Insights", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 10, insights)

        # Page(s): Plots
        for plot_path in plots:
            pdf.add_page()
            self.add_watermark(pdf)
            pdf.image(plot_path, x=10, y=30, w=190)

        # Page: Data Table
        if table_data:
            pdf.add_page()
            self.add_watermark(pdf)
            pdf.set_font("Arial", "B", 14)
            pdf.cell(200, 10, "Key Data Table", ln=True)
            pdf.set_font("Arial", "", 10)
            for row in table_data[:30]:  # Limit to 30 rows
                line = " | ".join(str(cell) for cell in row)
                pdf.multi_cell(0, 6, line)

        filename = f"report_{uuid.uuid4().hex[:8]}.pdf"
        filepath = os.path.join(self.output_path, filename)
        pdf.output(filepath)
        return filepath
