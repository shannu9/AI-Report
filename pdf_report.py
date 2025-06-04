from fpdf import FPDF
import matplotlib.pyplot as plt
import os
import uuid

class PDFReport(FPDF):
    def __init__(self, output_path="output"):
        super().__init__()
        self.output_path = output_path
        os.makedirs(output_path, exist_ok=True)

    def save_plot(self, fig, filename):
        path = os.path.join(self.output_path, filename)
        fig.savefig(path, bbox_inches="tight")
        plt.close(fig)
        return path

    def add_watermark(self, text="Shanmukh"):
        # Add a rotated text watermark across the page center
        self.set_text_color(230, 230, 230)
        self.set_font("Arial", "B", 50)
        self.set_xy(0, 0)
        self.rotate(45, x=self.w / 2, y=self.h / 2)
        self.text(self.w / 2 - 30, self.h / 2, text)
        self.rotate(0)

    def rotate(self, angle, x=None, y=None):
        from math import cos, sin, radians
        angle = radians(angle)
        c, s = cos(angle), sin(angle)
        if x is None: x = self.x
        if y is None: y = self.y
        cx, cy = x * self.k, (self.h - y) * self.k
        self._out(f'q {c:.5f} {s:.5f} {-s:.5f} {c:.5f} {cx - c * cx + s * cy:.5f} {cy - s * cx - c * cy:.5f} cm')

    def rotate_end(self):
        self._out('Q')

    def header(self):
        self.add_watermark()

    def create_pdf(self, summary, strategy, insights, plots, table_data):
        self.add_page()
        self.set_font("Arial", "B", 16)
        self.set_text_color(0, 0, 0)
        self.cell(200, 10, "Business Analysis Report", ln=True, align="C")
        self.set_font("Arial", "", 12)

        self.ln(10)
        self.set_font("Arial", "B", 14)
        self.cell(200, 10, "Executive Summary", ln=True)
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 10, summary)

        self.ln(5)
        self.set_font("Arial", "B", 14)
        self.cell(200, 10, "Recommended Strategies", ln=True)
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 10, strategy)

        self.ln(5)
        self.set_font("Arial", "B", 14)
        self.cell(200, 10, "Insights", ln=True)
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 10, insights)

        for plot_path in plots:
            self.add_page()
            self.image(plot_path, x=10, y=30, w=190)

        if table_data:
            self.add_page()
            self.set_font("Arial", "B", 14)
            self.cell(200, 10, "Key Data Table", ln=True)
            self.set_font("Arial", "", 10)
            for row in table_data[:30]:
                line = " | ".join(str(cell) for cell in row)
                self.multi_cell(0, 6, line)

        filename = f"report_{uuid.uuid4().hex[:8]}.pdf"
        filepath = os.path.join(self.output_path, filename)
        self.output(filepath)
        return filepath
