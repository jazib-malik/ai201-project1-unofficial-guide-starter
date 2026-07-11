import gradio as gr

from query import ask


def handle_query(question):
    if not question.strip():
        return "Type a question first.", ""
    result = ask(question)
    if result["sources"]:
        sources = "\n".join(f"- {s}" for s in result["sources"])
    else:
        sources = "No relevant documents found."
    return result["answer"], sources


with gr.Blocks(title="The Unofficial Guide: UC Berkeley Housing") as demo:
    gr.Markdown("# The Unofficial Guide: UC Berkeley Housing\nAsk about off-campus housing, neighborhoods, landlords, roommates, and renting around campus. Answers come from real r/berkeley threads.")
    inp = gr.Textbox(label="Your question", placeholder="Is it safe to live alone in southside?")
    btn = gr.Button("Ask")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

if __name__ == "__main__":
    demo.launch()
