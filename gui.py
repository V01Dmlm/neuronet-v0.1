import sys
import threading
from collections import deque

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel,
    QTextEdit, QLineEdit, QPushButton, QSpinBox, QDoubleSpinBox, QComboBox
)
from PyQt6.QtCore import Qt

from generate_pubmed_dataset import generate_dataset as scrape_main
from finetune import main as train_main
from generate_summary import load_model, generate_summary
from pubmed_fetcher import fetch_top_abstract 

def apply_dark_theme(app):
    dark_stylesheet = """
        QWidget {
            background-color: #121212;
            color: #ffffff;
            font-size: 14px;
        }

        QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox, QComboBox {
            background-color: #1e1e1e;
            color: #ffffff;
            border: 1px solid #444;
        }

        QPushButton {
            background-color: #2e2e2e;
            color: #fff;
            border: 1px solid #555;
            padding: 6px;
        }

        QPushButton:hover {
            background-color: #444;
        }

        QTabWidget::pane {
            border-top: 2px solid #444;
        }

        QTabBar::tab {
            background: #1e1e1e;
            padding: 6px;
            color: #aaa;
        }

        QTabBar::tab:selected {
            background: #2e2e2e;
            color: #fff;
        }

        QLabel {
            color: #ccc;
        }
    """
    app.setStyleSheet(dark_stylesheet)

MAX_HISTORY = 6
chat_history = deque(maxlen=MAX_HISTORY)

class PubMedSummarizerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧠 NeuroNet - PubMed Research Assistant")
        self.setGeometry(100, 100, 800, 600)

        self.tabs = QTabWidget()
        self.tabs.addTab(self.dataset_tab(), "📄 Generate Dataset")
        self.tabs.addTab(self.train_tab(), "🛠️ Train Model")
        self.tabs.addTab(self.chat_tab(), "🤖 Research Chatbot")

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    # ===================== Dataset Tab =====================
    def dataset_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.query_input = QLineEdit("Alzheimer OR Cancer OR Diabetes")
        self.max_results_input = QSpinBox()
        self.max_results_input.setMaximum(10000)
        self.max_results_input.setValue(1000)

        self.prompt_input = QTextEdit()
        self.prompt_input.setPlainText("Summarize the following abstract:\n{abstract}\nAnswer:")

        self.dataset_log = QTextEdit()
        self.dataset_log.setReadOnly(True)

        scrape_btn = QPushButton("Download & Generate Dataset")
        scrape_btn.clicked.connect(self.run_scraper_thread)

        layout.addWidget(QLabel("Query:"))
        layout.addWidget(self.query_input)
        layout.addWidget(QLabel("Max Results:"))
        layout.addWidget(self.max_results_input)
        layout.addWidget(QLabel("Prompt Template:"))
        layout.addWidget(self.prompt_input)
        layout.addWidget(scrape_btn)
        layout.addWidget(QLabel("Log:"))
        layout.addWidget(self.dataset_log)

        tab.setLayout(layout)
        return tab

    def run_scraper_thread(self):
        def scraper_task():
            query = self.query_input.text()
            max_results = self.max_results_input.value()
            prompt_template = self.prompt_input.toPlainText()
            output_file = "neuronet_data.jsonl"

            self.dataset_log.append(f"🔍 Starting scrape for: {query} ...")

            try:
                scrape_main(
                    query=query,
                    max_results=max_results,
                    output_file=output_file,
                    prompt_template=prompt_template
                )
                self.dataset_log.append(f"✅ Done! Dataset saved to {output_file}")
            except Exception as e:
                self.dataset_log.append(f"❌ Error: {e}")

        threading.Thread(target=scraper_task).start()

    # ===================== Train Tab =====================
    def train_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.epochs_input = QSpinBox()
        self.epochs_input.setMinimum(1)
        self.epochs_input.setValue(5)

        self.lr_input = QDoubleSpinBox()
        self.lr_input.setDecimals(6)
        self.lr_input.setValue(3e-5)
        self.lr_input.setSingleStep(1e-5)

        self.train_log = QTextEdit()
        self.train_log.setReadOnly(True)

        train_btn = QPushButton("Train model")
        train_btn.clicked.connect(self.run_training_thread)

        layout.addWidget(QLabel("Epochs:"))
        layout.addWidget(self.epochs_input)
        layout.addWidget(QLabel("Learning Rate:"))
        layout.addWidget(self.lr_input)
        layout.addWidget(train_btn)
        layout.addWidget(QLabel("Training Log:"))
        layout.addWidget(self.train_log)

        tab.setLayout(layout)
        return tab

    def run_training_thread(self):
        def train_task():
            self.train_log.append("🚀 Starting training...")
            try:
                train_main()
                self.train_log.append("✅ Training complete!")
            except Exception as e:
                self.train_log.append(f"❌ Error: {e}")
        threading.Thread(target=train_task).start()

    # ===================== Chatbot Tab (Auto-fetch Abstract) =====================
    def chat_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Ask a medical research question...")

        self.style_map = {
            "🧠 Researcher Mode": (
                "You are NeuroNet, a smart and curious medical research assistant.\n\n"
                "Abstract:\n{abstract}\n\n"
                "User: {user_question}\nNeuroNet:"
            ),
            "🩺 Clinical Summary": (
                "Summarize this clinical abstract clearly, with focus on results.\n\n"
                "Abstract:\n{abstract}\n\n"
                "Summary:"
            ),
            "👨‍🏫 Professor Mode": (
                "You're a professor. Explain this abstract to a curious med student.\n\n"
                "Abstract:\n{abstract}\n\n"
                "Student: {user_question}\nProfessor:"
            ),
            "💬 Casual Explainer": (
                "Explain the abstract in simple language.\n\n"
                "Abstract:\n{abstract}\n\n"
                "User: {user_question}\nYou:"
            )
        }

        self.selected_style = QComboBox()
        self.selected_style.addItems(self.style_map.keys())

        ask_btn = QPushButton("Send")
        ask_btn.clicked.connect(self.chatbot_answer)

        layout.addWidget(QLabel("Choose Chatbot Style:"))
        layout.addWidget(self.selected_style)
        layout.addWidget(QLabel("Conversation:"))
        layout.addWidget(self.chat_display)
        layout.addWidget(self.user_input)
        layout.addWidget(ask_btn)

        tab.setLayout(layout)
        return tab

    def chatbot_answer(self):
        user_msg = self.user_input.text().strip()
        if not user_msg:
            return

        selected_style_name = self.selected_style.currentText()
        template = self.style_map[selected_style_name]

        self.chat_display.append(f"👤 You: {user_msg}")
        self.user_input.clear()

        def generate():
            try:
                self.chat_display.append("📡 Fetching related abstract from PubMed...")
                abstract = fetch_top_abstract(user_msg)

                if not abstract:
                    self.chat_display.append("❌ No abstract found for that topic.")
                    return

                full_prompt = (
                    template.replace("{abstract}", abstract)
                            .replace("{user_question}", user_msg)
                )

                model, tokenizer, device = load_model()
                answer = generate_summary(model, tokenizer, device, full_prompt)
                self.chat_display.append(f"🤖 NeuroNet:\n{answer}")
                chat_history.append(f"User: {user_msg}")
                chat_history.append(f"NeuroNet: {answer}")
            except Exception as e:
                self.chat_display.append(f"[Error] {e}")

        threading.Thread(target=generate).start()


# ===================== App Entry Point =====================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_dark_theme(app)

    window = PubMedSummarizerGUI()
    window.show()

    sys.exit(app.exec())

