LEARNING_RESOURCES = {
    "python": "Python fundamentals and problem solving",
    "sql": "SQL fundamentals, queries, joins, and aggregations",
    "excel": "Excel formulas, pivot tables, and data analysis",
    "pandas": "Pandas DataFrame operations and data cleaning",
    "power bi": "Power BI dashboards, visualization, and DAX",
    "numpy": "NumPy arrays and numerical computing",
    "matplotlib": "Data visualization with Matplotlib",
    "machine learning": "Machine learning fundamentals and model building",
    "scikit-learn": "Scikit-learn preprocessing, training, and evaluation",
    "deep learning": "Neural networks and deep learning fundamentals",
    "tensorflow": "TensorFlow model development",
    "pytorch": "PyTorch tensors and neural networks",
    "nlp": "Natural Language Processing fundamentals",
    "computer vision": "Computer Vision and image processing",
    "opencv": "OpenCV image processing techniques",
    "cnn": "Convolutional Neural Networks",
    "yolo": "Object detection using YOLO",
    "transformers": "Transformer architecture and applications",
    "llm": "Large Language Models and prompt engineering",
    "rag": "Retrieval-Augmented Generation",
    "artificial intelligence": "Artificial Intelligence fundamentals",
    "fastapi": "FastAPI REST API development",
    "django": "Django web application development",
    "flask": "Flask backend development",
    "rest api": "REST API design and development",
    "docker": "Docker containers and deployment",
    "aws": "AWS cloud fundamentals",
    "azure": "Microsoft Azure fundamentals",
    "gcp": "Google Cloud Platform fundamentals",
    "git": "Git version control and branching",
    "github": "GitHub repositories, branches, and collaboration",
}


def generate_roadmap(missing_skills):
    """
    Generate a basic learning roadmap based
    on missing skills.
    """

    roadmap = []

    for index, skill in enumerate(missing_skills):

        skill_key = skill.lower().strip()

        topic = LEARNING_RESOURCES.get(
            skill_key,
            f"{skill} fundamentals and practical applications"
        )

        week = index + 1

        roadmap.append({
            "week": week,
            "skill": skill,
            "topic": topic
        })

    return roadmap