from crewai import Agent, Task, Crew
from crewai_tools.tools import tool  # ✅ Correct for Pydantic validation
from euri_llm import EuriLLM  # Your custom LLM wrapper

# ------------------------- Tool Definitions ------------------------- #

symptom_checker_tool = Tool(
    name="Symptom Checker Tool",
    description="Analyzes patient symptoms and suggests possible diagnoses.",
    func=lambda symptoms_text: (
        "🩺 Possible condition: Type 2 Diabetes. Recommended: Blood sugar test and HbA1c evaluation."
        if all(k in symptoms_text.lower() for k in ["thirst", "fatigue", "blurred vision"]) else
        "🧠 Possible condition: Migraine or Hypertension."
        if "headache" in symptoms_text.lower() and "blurred vision" in symptoms_text.lower() else
        "😴 Fatigue-related. Could be anemia or sleep issue."
    )
)

health_advice_tool = Tool(
    name="Health Advice Tool",
    description="Provides basic wellness suggestions based on symptoms and history.",
    func=lambda profile_text: (
        "🥗 Advice:\n"
        "- Maintain a low-sugar, balanced diet.\n"
        "- Stay hydrated (8+ glasses/day).\n"
        "- Regular exercise (30 min/day).\n"
        "- Schedule a physician visit for diagnostics.\n"
        "- Track blood pressure & glucose if there's family history."
    )
)

severity_scoring_tool = Tool(
    name="Severity Scoring Tool",
    description="Scores the severity of symptoms to suggest urgency level.",
    func=lambda text: (
        "🚨 High severity: Seek immediate medical attention."
        if any(x in text.lower() for x in ["chest pain", "shortness of breath"]) else
        "⚠️ Moderate severity: Schedule a clinical check-up soon."
        if sum(1 for kw in ["blurred vision", "thirst", "fatigue", "headache"] if kw in text.lower()) >= 3 else
        "✅ Mild symptoms: Monitor and manage with home care."
    )
)

# ------------------------- Agent Wrapper ------------------------- #

class MedicalAgent:
    def __init__(self, role, goal, backstory, tools=[]):
        self.agent = Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            verbose=True,
            allow_delegation=False,
            llm=EuriLLM(),
            tools=tools
        )

    def get_agent(self):
        return self.agent

# ------------------------- User Input ------------------------- #

user_input = {
    "name": "Sudhanshu Kumar",
    "age": 33,
    "gender": "Male",
    "symptoms": ["frequent headache", "blurred vision", "fatigue", "increased thirst"],
    "medical_history": "Family history of diabetes and hypertension."
}

symptoms_text = f"""
Patient Profile:
- Name: {user_input['name']}
- Age: {user_input['age']}
- Gender: {user_input['gender']}
- Symptoms: {', '.join(user_input['symptoms'])}
- Medical History: {user_input['medical_history']}
"""

# ------------------------- Agents ------------------------- #

diagnosis_agent = MedicalAgent(
    role="AI Medical Diagnostician",
    goal="Analyze symptoms and provide possible health conditions.",
    backstory="An expert medical AI trained to evaluate symptoms and infer likely diseases with high accuracy.",
    tools=[symptom_checker_tool]
).get_agent()

advice_agent = MedicalAgent(
    role="AI Wellness Advisor",
    goal="Give preventive health and lifestyle advice based on user profile.",
    backstory="A health assistant AI that provides daily health advice and preventive strategies based on symptoms and history.",
    tools=[health_advice_tool]
).get_agent()

triage_agent = MedicalAgent(
    role="AI Triage Nurse",
    goal="Determine severity of the patient condition and recommend urgency level.",
    backstory="A virtual triage nurse trained to evaluate symptom severity and urgency using scoring systems.",
    tools=[severity_scoring_tool]
).get_agent()

# ------------------------- Tasks ------------------------- #

tasks = [
    Task(
        description=f"Analyze the patient's symptoms and suggest 2–3 possible conditions.\n{symptoms_text}",
        expected_output="Top 3 likely conditions with medical reasoning.",
        agent=diagnosis_agent
    ),
    Task(
        description=f"Provide health and lifestyle recommendations based on the following input:\n{symptoms_text}",
        expected_output="Diet tips, lifestyle changes, and when to consult a doctor.",
        agent=advice_agent
    ),
    Task(
        description=f"Assess the severity of the symptoms and suggest urgency level.\n{symptoms_text}",
        expected_output="Severity level (Low, Moderate, High) and action to take (e.g., home rest, doctor visit, ER).",
        agent=triage_agent
    )
]

# ------------------------- Crew Execution ------------------------- #

crew = Crew(
    agents=[diagnosis_agent, advice_agent, triage_agent],
    tasks=tasks,
    verbose=True
)

result = crew.kickoff()

print("\n📝 Personalized Medical Report:\n")
print(result)
