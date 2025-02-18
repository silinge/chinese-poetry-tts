import gradio as gr
import json
import os
from TTS.api import TTS

# 加载诗词数据
with open("json/poet.tang.300.json", "r", encoding="utf-8") as f:
    poems = json.load(f)

# 初始化 TTS 模型（此处以多语言模型为例）
tts_model = "tts_models/multilingual/multi-dataset/xtts_v2"
tts = TTS(tts_model)

def generate_audio(poem_index):
    poem = poems[int(poem_index)]
    title = poem["title"]
    author = poem["author"]
    content = "\n".join(poem["paragraphs"])
    text = f"{title}，{author}。\n{content}"
    
    # 保存临时音频文件
    output_path = f"temp_{title}.wav"
    tts.tts_to_file(text=text, file_path=output_path)
    return output_path

# 构建 Gradio 界面
with gr.Blocks() as demo:
    gr.Markdown("# 诗词朗诵生成器")
    poem_index = gr.Dropdown(choices=[str(i) for i in range(len(poems[:50]))], label="选择诗词编号")
    output_audio = gr.Audio(type="filepath")
    generate_button = gr.Button("生成朗诵音频")
    generate_button.click(generate_audio, inputs=[poem_index], outputs=[output_audio])

demo.launch()
