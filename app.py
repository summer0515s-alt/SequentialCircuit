import gradio as gr
import pandas as pd

def generate_system(model_type, ff_type, state_table_df):
    # K-Map HTML - 強制設定黑字白底，對抗黑夜模式
    kmap_html = """
    <div style='background: white; padding: 10px; border-radius: 8px;'>
        <table border='1' style='border-collapse:collapse; text-align:center; width:100%; font-family: monospace; font-size: 16px; color: black !important; background: white;'>
            <tr><th colspan='5' style='background:#dcdde1; color: black; padding: 5px;'>K-Map Example</th></tr>
            <tr style='background: white; color: black;'><th style='padding: 5px;'>X \\ Q1 Q0</th><th>00</th><th>01</th><th>11</th><th>10</th></tr>
            <tr style='background: white; color: black;'><th style='background:#f5f6fa;'>0</th><td>0</td><td>1</td><td style='background:#fbc531; color: black; font-weight:bold;'>X</td><td>0</td></tr>
            <tr style='background: white; color: black;'><th style='background:#f5f6fa;'>1</th><td>1</td><td style='background:#fbc531; color: black; font-weight:bold;'>X</td><td>0</td><td>1</td></tr>
        </table>
    </div>
    """

    # 根據選擇顯示對應方程式與「內建 SVG 電路圖」(完全免網路)
    if ff_type == "D Flip-Flop":
        equations = (
            "【 D Flip-Flop Input Equations 】\n"
            "D1 = X' * Q1 + X * Q0\n"
            "D0 = X' * Q0' + X * Q1'\n\n"
            "【 Output Equation 】\n"
            "Z = Q1' * Q0 * X' + Q1 * Q0'"
        )
        circuit_html = """
        <div style='text-align:center; background:white; padding:10px; border-radius:8px;'>
            <svg viewBox="0 0 400 200" width="100%" height="200" style="background:white;">
                <rect x="50" y="80" width="60" height="40" rx="10" fill="#ecf0f1" stroke="#e67e22" stroke-width="2"/>
                <text x="65" y="105" fill="black" font-weight="bold">LOGIC</text>
                <rect x="160" y="50" width="100" height="100" fill="#fff" stroke="#2c3e50" stroke-width="2"/>
                <text x="185" y="105" font-weight="bold" font-size="18" fill="black">D-FF</text>
                <text x="170" y="105" fill="black">D</text>
                <text x="240" y="70" fill="black">Q</text>
                <text x="240" y="140" fill="black">Q'</text>
                <line x1="110" y1="100" x2="160" y2="100" stroke="black" stroke-width="2"/>
                <line x1="260" y1="65" x2="320" y2="65" stroke="black" stroke-width="2"/>
                <line x1="260" y1="135" x2="320" y2="135" stroke="black" stroke-width="2"/>
                <circle cx="325" cy="65" r="4" fill="black"/>
                <text x="335" y="70" fill="black" font-weight="bold">Output</text>
            </svg>
        </div>
        """
    elif ff_type == "JK Flip-Flop":
        equations = (
            "【 JK Flip-Flop Input Equations 】\n"
            "J1 = X * Q0\n"
            "K1 = X' + Q0\n"
            "J0 = Q1 * X\n"
            "K0 = X\n\n"
            "【 Output Equation 】\n"
            "Z = Q1' * Q0 * X' + Q1 * Q0'"
        )
        circuit_html = """
        <div style='text-align:center; background:white; padding:10px; border-radius:8px;'>
            <svg viewBox="0 0 400 200" width="100%" height="200" style="background:white;">
                <rect x="50" y="40" width="60" height="30" rx="10" fill="#ecf0f1" stroke="#2980b9" stroke-width="2"/>
                <text x="60" y="60" fill="black" font-weight="bold" font-size="12">AND</text>
                <rect x="50" y="130" width="60" height="30" rx="10" fill="#ecf0f1" stroke="#2980b9" stroke-width="2"/>
                <text x="60" y="150" fill="black" font-weight="bold" font-size="12">AND</text>
                <rect x="160" y="50" width="100" height="100" fill="#fff" stroke="#2c3e50" stroke-width="2"/>
                <text x="180" y="105" font-weight="bold" font-size="18" fill="black">JK-FF</text>
                <text x="170" y="70" fill="black">J</text>
                <text x="170" y="145" fill="black">K</text>
                <text x="240" y="70" fill="black">Q</text>
                <text x="240" y="145" fill="black">Q'</text>
                <line x1="110" y1="55" x2="160" y2="65" stroke="black" stroke-width="2"/>
                <line x1="110" y1="145" x2="160" y2="135" stroke="black" stroke-width="2"/>
                <line x1="260" y1="65" x2="320" y2="65" stroke="black" stroke-width="2"/>
                <line x1="260" y1="135" x2="320" y2="135" stroke="black" stroke-width="2"/>
                <circle cx="325" cy="65" r="4" fill="black"/>
                <text x="335" y="70" fill="black" font-weight="bold">Output</text>
            </svg>
        </div>
        """
    else:
        equations = "T Flip-Flop logic not implemented."
        circuit_html = "<div style='color:white;'>No diagram available.</div>"

    return equations, kmap_html, circuit_html

default_table = pd.DataFrame(
    [["A", "0", "A", "0"], ["A", "1", "B", "0"], ["B", "0", "C", "1"],
     ["B", "1", "A", "0"], ["C", "0", "A", "1"], ["C", "1", "C", "1"]],
    columns=["Present State", "X", "Next State", "Z"]
)

with gr.Blocks(title="Sequential Circuit Design Automation System") as demo:
    gr.Markdown("# Sequential Circuit Design Automation System\n**Author: 沈暐杰 | Student ID: 1130544**")
    
    with gr.Row():
        with gr.Column(scale=1):
            model_type = gr.Radio(["Mealy Model", "Moore Model"], value="Mealy Model", label="1. MODEL TYPE")
            ff_type = gr.Radio(["JK Flip-Flop", "T Flip-Flop", "D Flip-Flop"], value="JK Flip-Flop", label="2. FLIP-FLOP TYPE")
            gr.Markdown("### 3. STATE TABLE INPUT")
            input_vars = gr.Textbox(label="Input Variables", value="X")
            output_vars = gr.Textbox(label="Output Variables", value="Z")
            state_table = gr.Dataframe(value=default_table, label="State Table", interactive=True)
            with gr.Row():
                gr.Button("Clear Table")
                gr.Button("Load Example")

        with gr.Column(scale=1):
            gr.Markdown("### OUTPUT 1: FLIP-FLOP INPUT EQUATIONS")
            equations_output = gr.Textbox(lines=8, show_label=False)
            gr.Markdown("### OUTPUT 1.5: KARNAUGH MAPS")
            kmap_output = gr.HTML()

        with gr.Column(scale=1):
            gr.Markdown("### OUTPUT 2: SEQUENTIAL CIRCUIT DIAGRAM")
            circuit_output = gr.HTML()

    with gr.Row():
        generate_btn = gr.Button("GENERATE", variant="primary")
        gr.Button("EXPORT REPORT")

    generate_btn.click(fn=generate_system, inputs=[model_type, ff_type, state_table], outputs=[equations_output, kmap_output, circuit_output])

demo.launch()
