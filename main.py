import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from system_prompt import system_prompt
from functions.call_function import available_functions, call_function

parser = argparse.ArgumentParser(description = "Chatbot")
parser.add_argument("user_prompt", type = str, help = "User prompt")
parser.add_argument("--verbose", action="store_true", help= "Enable verbose output")
args = parser.parse_args()

load_dotenv()
api_key= os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("api key not found")

client = genai.Client(api_key = api_key)

def main():
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    for i in range(20):
        response = client.models.generate_content(model = "gemini-2.5-flash", contents = messages, config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions]))
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
        if args.verbose:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")
        function_results = []
        if response.function_calls:
            for function_call in response.function_calls:
                # print(f"Calling function: {function_call.name}({function_call.args})")
                function_call_result = call_function(function_call, verbose=args.verbose)
                if not function_call_result.parts:
                    raise Exception("function call result has no parts")
                if not function_call_result.parts[0].function_response:
                    raise Exception("function call result part has no response")
                if not function_call_result.parts[0].function_response.response:
                    raise Exception("function call result part has no function response")
                
                function_results.append(function_call_result.parts[0])

                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
        else:
            print(response.text)
            break

        messages.append(types.Content(role="user", parts=function_results))   

        if response.usage_metadata == None:
            raise RuntimeError("api request failed")
        
        if i == 19:
            print("Max iterations reached without a final response.")
            sys.exit(1)
    

if __name__ == "__main__":
    main()
