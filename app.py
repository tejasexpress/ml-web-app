import gradio as gr
import requests

def generate_messages(messages: list, query: str) -> list:
    formatted_messages = [
        {
            'role': 'system',
            'content': 'You are a helpful assistant.'
        }
    ]
    for m in messages:
        formatted_messages.append({
            'role': 'user',
            'content': m[0]
        })
        formatted_messages.append({
            'role': 'assistant',
            'content': m[1]
        })
    formatted_messages.append(
        {
            'role': 'user',
            'content': query
        }
    )
    return formatted_messages

def submit(query, Chatbot,temperature,frequency_penalty):
    
    if query == "":
        raise gr.Error("Please enter some text to generate")
    formatted_messages = generate_messages(Chatbot, query)
    data = {
        "messages": formatted_messages,
        "temperature": temperature,
        "frequency_penalty": frequency_penalty
    }
    response = requests.post("http://127.0.0.1:8000/v1/submit", json=data, stream=True)
    Chatbot = Chatbot + [[query,""]]
    if response.status_code == 200:
        acc_text = ""
        try:
            for i, chunk in enumerate(response.iter_content(chunk_size=1024)):
                if chunk:
                    text = str(chunk, encoding="utf-8")
                acc_text += text
                last_turn = list(Chatbot.pop(-1))
                last_turn[-1] += acc_text
                Chatbot = Chatbot + [last_turn]
                yield "", Chatbot
                acc_text = ""
        except requests.exceptions.RequestException as e:
            # Handle any exceptions that may occur during the streaming
            print("Error occurred during streaming:", str(e))

        # stripped_text = response.text.strip('"')
        # newline = stripped_text.replace('\\n', '\n')
        # print(newline)
        # Chatbot.append((query, newline)) 
        # return '',Chatbot
    
with gr.Blocks( theme=gr.themes.Soft(primary_hue="violet"), css="""#component-0 {margin : 7vw 17vw;}
                                                                   #title h1{text-align:center;
                                                                           font-size:5vh}""") as demo:
    gr.Markdown("# Hi-NOLIN", elem_id="title")
    Chatbot = gr.Chatbot(height=400)
    Input = gr.Textbox(label="Input", lines=4)
    with gr.Accordion(label="Advanced options",open=False):
        temperature = gr.Slider(label="temperature", minimum=0, maximum=2, value=0.7, step=0.1, info="controls randomness")
        frequency_penalty = gr.Slider(label="frequency penalty", minimum=-2, maximum=2, value=0, step=0.1, info="higher means less repetition")
    with gr.Row():
        btn = gr.Button("Submit",variant="primary")
        clear = gr.ClearButton(components=[Input, Chatbot], value="Clear Input")
    btn.click(submit, inputs=[Input, Chatbot, temperature, frequency_penalty], outputs=[Input, Chatbot])
    Input.submit(submit, inputs=[Input, Chatbot, temperature, frequency_penalty], outputs=[Input, Chatbot])

if __name__ == "__main__":
    demo.queue().launch(show_api=False) 