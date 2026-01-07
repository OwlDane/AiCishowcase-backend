import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.projects.models import Category, Project
from apps.achievements.models import Achievement
from apps.users.models import StudentProfile

def seed():
    # 1. Categories
    robotics, _ = Category.objects.get_or_create(name='Robotics', defaults={'description': 'Robotics and automation projects.'})
    ai, _ = Category.objects.get_or_create(name='Artificial Intelligence', defaults={'description': 'AI and Machine Learning projects.'})
    smart_city, _ = Category.objects.get_or_create(name='Smart City', defaults={'description': 'Smart City and IoT solutions.'})

    # 2. Student Profile
    profile = StudentProfile.objects.first()

    # 3. Projects
    projects_data = [
        {
            'title': "Autonomous Delivery Drone",
            'description': "This project focuses on building an autonomous delivery drone capable of navigating complex urban environments. It uses computer vision for obstacle avoidance and GPS for route planning. The drone is designed to deliver small medical supplies or packages to remote areas.",
            'category': robotics,
            'thumbnail': 'projects/thumbnails/drone.jpg' # Need to handle images properly later
        },
        {
            'title': "AI-Powered Crop Monitoring",
            'description': "AI-Powered Crop Monitoring is a system that leverages satellite imagery and machine learning to help farmers monitor the health of their crops. It can detect early signs of pest infestations, nutrient deficiencies, and water stress, providing actionable insights to optimize yield.",
            'category': ai,
            'thumbnail': 'projects/thumbnails/crop.jpg'
        },
        {
            'title': "Smart Traffic Management",
            'description': "This project aims to reduce urban traffic congestion by using AI to optimize traffic signal timings. The system analyzes real-time traffic data from cameras and sensors to adjust flow dynamically, reducing wait times and carbon emissions.",
            'category': smart_city,
            'thumbnail': 'projects/thumbnails/traffic.jpg'
        }
    ]

    for p_data in projects_data:
        Project.objects.get_or_create(
            title=p_data['title'],
            defaults={
                'description': p_data['description'],
                'category': p_data['category'],
                'student': profile,
                'status': 'APPROVED'
            }
        )

    # 4. Achievements
    achievements_data = [
        {
            'title': "1st Winner - National Robotics Competition 2023",
            'description': "Our team won first place in the National Robotics Competition 2023, showcasing an innovative autonomous rescue robot.",
            'date': "October 2023",
            'category': 'Competition'
        },
        {
            'title': "Partnership with UMG IdeaLab",
            'description': "AiCi officially partnered with UMG IdeaLab to accelerate AI and robotics research in the region.",
            'date': "January 2024",
            'category': 'Partnership'
        },
        {
            'title': "Outstanding AI Research Center Award",
            'description': "AiCi recognized as the most innovative AI research center in the 2023 Tech Excellence Awards.",
            'date': "December 2023",
            'category': 'Recognition'
        }
    ]

    for a_data in achievements_data:
        Achievement.objects.get_or_create(
            title=a_data['title'],
            defaults={
                'description': a_data['description'],
                'date': a_data['date'],
                'category': a_data['category']
            }
        )

    print("Database seeded successfully!")

if __name__ == "__main__":
    seed()
