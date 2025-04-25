from django_ai_assistant import AIAssistant, method_tool, BaseModel, Field
from openai import OpenAI
from django.conf import settings
from typing import List, Dict


class WorkoutAIAssistant(AIAssistant):
    id = "workout_assistant"
    name = "Workout Assistant"
    instructions = (
        "You are an expert fitness assistant specializing in creating personalized workout plans. "
        "Generate science-based workout routines tailored to the user's specific goals, fitness level, "
        "and available equipment. Provide detailed instructions for each exercise."
    )
    model = "gpt-4o"

    def __init__(self):
        super().__init__()
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    class WorkoutPlanInput(BaseModel):
        goals: str = Field(description="Primary fitness goals (weight loss, muscle gain, cardio, etc.)")
        activity_level: str = Field(description="Current fitness level (beginner, intermediate, advanced)")
        days_per_week: int = Field(
            default=3,
            description="Number of available workout days per week",
        )

    class ExerciseDetail(BaseModel):
        name: str
        muscle_group: str
        sets: int
        reps: str
        instructions: str

    class WorkoutDay(BaseModel):
        day_number: int
        focus: str
        exercises: List[ExerciseDetail]

    @method_tool(args_schema=WorkoutPlanInput)
    def generate_workout_plan(self, goals: str, activity_level: str, **kwargs) -> Dict:
        """
        Generate a comprehensive workout plan based on user parameters using OpenAI's API.
        Returns a structured plan with exercise details, progression, and recommendations.
        """
        input_data = self.WorkoutPlanInput(goals=goals, activity_level=activity_level, **kwargs)

        response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self.instructions
                    },
                    {
                        "role": "user",
                        "content": self._build_prompt(input_data)
                    }
                ],
                temperature=0.7,
                response_format={"type": "json_object"},
                max_tokens=1500
            )
            
            plan_json = response.choices[0].message.content
            plan = json.loads(plan_json)
            return self._validate_plan(plan)
    
    
    def _build_prompt(self, input_data: WorkoutPlanInput) -> str:
        prompt = f"""
        Create a {input_data.activity_level} level workout plan for someone who wants to {input_data.goals}.
        
        Parameters:
        - Workout days per week: {input_data.days_per_week}
        - Preferences: {input_data.focus or 'None specified'}
        
        Output format (JSON):
        {{
            "data": {{
                "goal": "[user goal]",
                "level": "[fitness level]",
                "duration_weeks": 4,
                "equipment_used": ["list of equipment"]
            }},
            "weekly_schedule": [
                {{
                    "day": 1,
                    "focus": "[primary muscle group/focus]",
                    "exercises": [
                        {{
                            "name": "[exercise name]",
                            "muscle_group": "[targeted muscles]",
                            "sets": [number],
                            "reps": "[rep range]",
                            "rest": "[rest period]",
                            "instructions": "[detailed form instructions]",
                            "progression": "[how to progress this exercise]"
                        }}
                    ],
                    "total_duration": "[estimated duration]",
                    "notes": "[any additional notes]"
                }}
            ],
            "general_recommendations": {{
                "nutrition": "[brief nutrition tips]",
                "recovery": "[recovery advice]",
                "progression_strategy": "[how to progress the program]"
            }}
        }}
        """

        ai_response = self._call_ai_api(prompt)
        plan = json.loads(ai_response)
        return plan
        
      
    

    

