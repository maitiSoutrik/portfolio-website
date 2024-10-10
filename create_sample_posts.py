from app import app, db
from models import BlogPost

def create_sample_posts():
    with app.app_context():
        # Create sample blog posts
        post1 = BlogPost(
            title="Introduction to Embedded Systems",
            content="Embedded systems are computer systems designed for specific control functions within a larger system. They are found in a wide range of devices, from simple appliances to complex industrial machines. These systems combine hardware and software components to perform dedicated functions, often with real-time computing constraints."
        )
        post2 = BlogPost(
            title="The Importance of RTOS in Embedded Development",
            content="Real-Time Operating Systems (RTOS) play a crucial role in embedded systems development. They provide a framework for managing tasks, scheduling, and resource allocation in time-critical applications. RTOS ensures that time-sensitive tasks are executed within their specified time constraints, which is essential for many embedded systems applications."
        )
        
        # Add posts to the database
        db.session.add(post1)
        db.session.add(post2)
        db.session.commit()

        print("Sample blog posts added successfully.")

if __name__ == "__main__":
    create_sample_posts()
