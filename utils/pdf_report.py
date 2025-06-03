# pdf_report.py

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

    def create_pdf(self, summary, strategy, insights, plots, table_data):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, "Business Analysis Report", ln=True, align="C")
        pdf.set_font("Arial", "", 12)

        # Summary
        pdf.ln(10)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, "Executive Summary", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 10, summary)

        # Strategy Suggestions
        pdf.ln(5)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, "Recommended Strategies", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 10, strategy)

        # Insights
        pdf.ln(5)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, "Insights", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 10, insights)

        # Plots
        for plot_path in plots:
            pdf.add_page()
            pdf.image(plot_path, x=10, y=30, w=190)

        # Data table (as text)
        if table_data:
            pdf.add_page()
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
