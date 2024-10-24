from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import os 
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import markdown


def LLM_Setup(prompt):
    load_dotenv()
    key = os.getenv('apikey')
    model = ChatOpenAI(api_key = key, model = 'gpt-4o')
    parser = StrOutputParser()
    output = model | parser
    output = output.invoke(prompt)
    return output





@login_required(login_url='login')
def aitools(request):
    return render(request,'aitools/aitools.html')

@login_required(login_url='login')
def Lesson_Planner_Details(request):
    return render(request,'aitools/lessonplannerdetails.html')

@login_required(login_url='login')
def Lesson_Planner(request):
    output = None 
    if request.method == 'POST':
        subject = request.POST.get('subject')
        topic = request.POST.get('topic')
        grade = request.POST.get('grade')
        duration = request.POST.get('duration')
        learning_objective = request.POST.get('learning_objectives')
        customization = request.POST.get('customization')

        if not customization:
            
            prompt = (
                f"Generate a detailed lesson plan for the subject of {subject} on the topic of {topic}. "
                f"This lesson is intended for {grade} students and will last for {duration}. "
                f"The following are the learning objectives: {learning_objective}. Return the results as Markdown and don't return class size"
            )
            llm_out = LLM_Setup(prompt=prompt)
            output = markdown.markdown(llm_out)

        else:
            prompt = (
                f"Generate a detailed lesson plan for the subject of {subject} on the topic of {topic}. "
                f"This lesson is intended for {grade} students and will last for {duration}. "
                f"The following are the learning objectives: {learning_objective}. Return the results as Markdown and don't return class size"
                f"This is how the user wants the plan to be customized {customization}."
            )

            llm_out = LLM_Setup(prompt=prompt)
            output = markdown.markdown(llm_out)

    return render(request, 'aitools/lessonplanner.html', {'output': output})


