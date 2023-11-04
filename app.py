import gradio as gr
import requests


def submit(text,temperature,frequency_penalty):
    
    if text == "":
        raise gr.Error("Please enter some text to generate")
    data = {
        "model": "HuggingFaceH4/zephyr-7b-beta",
        "prompt": f"<|user|>\n{text}</s>\n<|assissant|>",
        "temperature": temperature,
        "max_tokens": frequency_penalty
    }
    response = requests.post("http://127.0.0.1:8000/v1/submit", json=data)
    if response.status_code == 200:   
        return response.text
    return "Error: Unable to fetch response from server"
    
with gr.Blocks( theme=gr.themes.Soft(primary_hue="violet"), css="""#component-0 {margin : 7vw 17vw;}
                                                                   #title h1{text-align:center;
                                                                           font-size:5vh}""") as demo:
    gr.Markdown("# Hi-NOLIN", elem_id="title")
    Input = gr.Textbox(label="Input", lines=4)
    Output = gr.Textbox(label="Output", lines=8)
    with gr.Accordion(label="Advanced options",open=False):
        temperature = gr.Slider(label="temperature", minimum=0, maximum=1, value=0.7, step=0.1, info="controls randomness")
        frequency_penalty = gr.Slider(label="frequency penalty", minimum=1, maximum=100, value=50, step=1, info="higher means less repetition")
    with gr.Row():
        btn = gr.Button("Submit",variant="primary")
        clear = gr.ClearButton(components=[Input], value="Clear Input")
    btn.click(submit, inputs=[Input, temperature, frequency_penalty], outputs=[Output])
    Input.submit(submit, inputs=[Input, temperature, frequency_penalty], outputs=[Output])



if __name__ == "__main__":
    demo.queue()
    demo.launch(show_api=False) 