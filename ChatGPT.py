import sys
import os
import openai
from openai.error import InvalidRequestError

class ChatGPT:
  def __init__(self,mission,chat_history_max=4):
    self.total_tokens=0
    self.chat_history=[]
    self.chat_history_max=chat_history_max
    self.mission= {"role": "system", "content": mission}


  def generate_answer(self,prompt):
    self.chat_history.append( {"role":"user","content": prompt})
    messages=[ self.mission ] + self.chat_history

    while 1:
        try:
            #print(messages)
            #print(self.chat_history_max)
            answer,response=self.ChatGPT3(messages)
            #answer,response=self.Davinci(messages)
            #print(response)
            self.total_tokens+=int(response.usage.total_tokens)
            self.chat_history.append( {"role":"assistant","content": answer})
            self.chat_history = self.chat_history[-self.chat_history_max:]
            return answer
        except InvalidRequestError as e:
            print("例外が発生しました:", e)
            print(messages)
            return ""
        except:
            print("error")
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("例外が発生しました:", exc_type)
            print("エラーメッセージ:", exc_value)

  def ChatGPT3(self,messages):
      openai.api_key = os.environ["CUSTOMCONNSTR_OPENAI_API_KEY"]
      response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          max_tokens=3000,
          temperature= 0, # max=2 random, 0 fix
          messages=messages,
          timeout = 5
          )

      answer = response.choices[0]["message"]["content"].strip()
      #print(response)
      return answer,response

  def Davinci(self,messages):
      prompt=""
      messages.insert(1,{"role": "assistant", "content": "[Forget the conversation we've had so far.] No problem! What would you like to talk about?"})
      messages.insert(1,{"role": "user", "content": "Forget the conversation we've had so far."})
      messages.insert(1,{"role": "assistant", "content": "[I ate sushi.] Great!"})
      messages.insert(1,{"role": "user", "content": "I eated sushi."})
      messages.insert(1,{"role": "assistant", "content": "[Can you recommend me some anime?] Sure! What kind of anime do you like?"})
      messages.insert(1,{"role": "user", "content": "recommend me something anime?"})
      for line in messages:
        if line["role"]=="system":
          prompt+="Conversation Rules: "+line["content"]+"\n"
        if line["role"]=="user":
          prompt+="User: "+line["content"]+"\n"
        if line["role"]=="assistant":
          prompt+="Assistant: "+line["content"]+"\n"

      response = openai.Completion.create(
          model="text-davinci-002",
          prompt=prompt,
          max_tokens=5000,
          n=1,
          stop=None,
          temperature=0.7,
      )
      #print(prompt)
      answer = response.choices[0].text.strip()
      prefix = "Assistant: "
      if answer.startswith(prefix):
        answer = answer[len(prefix):]


      return answer,response