from django.urls import path 
from . import views 

urlpatterns = [
path('aitools/',views.aitools,name='aitools'),
path('lessonplannerdetails/',views.Lesson_Planner_Details,name='lessonplannerdetails'),
path('lessonplanner/',views.Lesson_Planner,name='lessonplanner'),

]