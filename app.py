from pathlib import Path
import hashlib
from tkinter import filedialog as file
import google.generativeai as genai
import time
import os

genai.configure(api_key="AIzaSyDW9iq9jwbSE5Q2PlYCeWrGxn8KO4HE5hY")

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

uploaded_files = []
def upload_if_needed(pathname: str) -> list[str]:
  path = Path(pathname)
  hash_id = hashlib.sha256(path.read_bytes()).hexdigest()
  try:
    existing_file = genai.get_file(name=hash_id)
    return [existing_file]
  except:
    pass
  uploaded_files.append(genai.upload_file(path=path, display_name=hash_id))
  return [uploaded_files[-1]]

prompt_parts_master = [
  "input: ",
  *upload_if_needed("imagem_gato_ia_1.jpeg"),
  "input 2: essa imagem foi gerada por IA?",
  "output: sim",
  "input: ",
  *upload_if_needed("imagem_gato_ia_4.jpeg"),
  "input 2: essa imagem foi gerada por IA?",
  "output: sim",
  "input: ",
  *upload_if_needed("imagem_gato_real_2.jpg"),
  "input 2: essa imagem foi gerada por IA?",
  "output: não",
  "input: ",
  *upload_if_needed("imagem_gato_real_3.jpg"),
  "input 2: essa imagem foi gerada por IA?",
  "output: não",
  "input: ",
  *upload_if_needed("imagem_gato_ia_5.jpeg"),
  "input 2: essa imagem foi gerada por IA?",
  "output: sim",
  "input: ",
  *upload_if_needed("imagem_gato_ia_6.jpeg"),
  "input 2: essa imagem foi gerada por IA?",
  "output: sim",
  "input: ",
]

def adiciona_prompt_parts(prompt_parts, caminho): 
  for lst in upload_if_needed(caminho):
    prompt_parts.append(lst) 
  prompt_parts.append("input 2: essa imagem foi gerada por IA?")  
  prompt_parts.append("output: ")  

  return prompt_parts

def gera_conteudo():
  imagem = file.askopenfilename(filetypes=(("Arquivo de Imagem", "*.jpg"),("Arquivo de Imagem", "*.jpeg"),("Arquivo de Imagem", "*.png")))

  response = model.generate_content(adiciona_prompt_parts(prompt_parts_master,imagem))
  
  print(f'A imagem {imagem} foi gerada por IA? (sim ou não)\nResposta: {response.text}\n')
  
def main():
  os.system('cls' if os.name == 'nt' else 'clear')
  print('Verificação de Imagem Gerada por IA\n')  
  print('1. Verificar Imagem: ')
  print('2. Sair:\n')
  opcao = input('Digite a opção: ')
    
  if opcao == '1':
    try:
      gera_conteudo()  
      os.system('pause') 
      main()    
    except Exception as e:
      print(f'\n Ocorre um erro na geração do conteúdo: {e}\n')
      os.system('pause') 
      main()
  elif opcao == '2':
    for uploaded_file in uploaded_files:
      genai.delete_file(name=uploaded_file.name)     
    quit()
  else:
    print('\nOpção Inválida!')
    time.sleep(2)
  
  main()
  
if __name__ == '__main__':
  main()