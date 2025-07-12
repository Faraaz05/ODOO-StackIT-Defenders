from django.core.management.base import BaseCommand
from accounts.models import User
from questions.models import Question, Answer, Vote
from django.utils import timezone
from datetime import timedelta
import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.db.models.manager import Manager
    from django.db.models.query import QuerySet

class Command(BaseCommand):
    help = 'Populate database with mock data for presentation'

    def handle(self, *args, **options):
        self.stdout.write('Creating mock data...')
        
        # Create mock users
        users = []
        user_data = [
            {'username': 'alice_dev', 'email': 'alice@example.com', 'first_name': 'Alice', 'last_name': 'Developer'},
            {'username': 'bob_coder', 'email': 'bob@example.com', 'first_name': 'Bob', 'last_name': 'Coder'},
            {'username': 'charlie_tech', 'email': 'charlie@example.com', 'first_name': 'Charlie', 'last_name': 'Tech'},
            {'username': 'diana_programmer', 'email': 'diana@example.com', 'first_name': 'Diana', 'last_name': 'Programmer'},
            {'username': 'eric_engineer', 'email': 'eric@example.com', 'first_name': 'Eric', 'last_name': 'Engineer'},
            {'username': 'fiona_frontend', 'email': 'fiona@example.com', 'first_name': 'Fiona', 'last_name': 'Frontend'},
            {'username': 'george_backend', 'email': 'george@example.com', 'first_name': 'George', 'last_name': 'Backend'},
            {'username': 'hannah_data', 'email': 'hannah@example.com', 'first_name': 'Hannah', 'last_name': 'Data'},
            {'username': 'ivan_devops', 'email': 'ivan@example.com', 'first_name': 'Ivan', 'last_name': 'DevOps'},
            {'username': 'julia_ml', 'email': 'julia@example.com', 'first_name': 'Julia', 'last_name': 'ML'},
        ]
        
        for user_info in user_data:
            user, created = User.objects.get_or_create(
                username=user_info['username'],
                defaults={
                    'email': user_info['email'],
                    'first_name': user_info['first_name'],
                    'last_name': user_info['last_name'],
                    'is_staff': False,
                    'is_superuser': False
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            users.append(user)
            self.stdout.write(f'Created user: {user.username}')
        
        # Sample questions data
        questions_data = [
            {
                'title': 'How to implement authentication in Django?',
                'description': 'I\'m building a web application and need to implement user authentication. What\'s the best way to handle login, registration, and password reset in Django? I\'ve heard about Django\'s built-in auth system but I\'m not sure how to customize it for my needs.',
                'tags': 'django,authentication,web-development,python',
                'author': users[0],
                'created_at': timezone.now() - timedelta(days=5),
                'upvotes': 15,
                'downvotes': 2
            },
            {
                'title': 'Best practices for React state management?',
                'description': 'I\'m working on a large React application and struggling with state management. Should I use Redux, Context API, or Zustand? What are the pros and cons of each approach?',
                'tags': 'react,javascript,state-management,frontend',
                'author': users[1],
                'created_at': timezone.now() - timedelta(days=3),
                'upvotes': 23,
                'downvotes': 1
            },
            {
                'title': 'Docker vs Kubernetes for deployment?',
                'description': 'I need to deploy my microservices application. Should I use Docker containers with a simple orchestration tool, or go full Kubernetes? What\'s the learning curve and complexity difference?',
                'tags': 'docker,kubernetes,deployment,devops,containers',
                'author': users[2],
                'created_at': timezone.now() - timedelta(days=2),
                'upvotes': 8,
                'downvotes': 3
            },
            {
                'title': 'SQL vs NoSQL for e-commerce database?',
                'description': 'I\'m designing a database for an e-commerce platform. Should I use a relational database like PostgreSQL or a NoSQL solution like MongoDB? What factors should I consider?',
                'tags': 'database,sql,nosql,e-commerce,postgresql,mongodb',
                'author': users[3],
                'created_at': timezone.now() - timedelta(days=1),
                'upvotes': 12,
                'downvotes': 0
            },
            {
                'title': 'How to optimize Python code performance?',
                'description': 'My Python application is running slowly. What are the best tools and techniques for profiling and optimizing Python code? I\'ve heard about cProfile and line_profiler.',
                'tags': 'python,performance,optimization,profiling',
                'author': users[4],
                'created_at': timezone.now() - timedelta(hours=12),
                'upvotes': 6,
                'downvotes': 1
            },
            {
                'title': 'Git workflow for team collaboration?',
                'description': 'My team is growing and we need a better Git workflow. Should we use Git Flow, GitHub Flow, or trunk-based development? What are the best practices for code reviews and CI/CD?',
                'tags': 'git,version-control,teamwork,ci-cd',
                'author': users[0],
                'created_at': timezone.now() - timedelta(hours=6),
                'upvotes': 18,
                'downvotes': 2
            },
            {
                'title': 'Machine Learning model deployment strategies?',
                'description': 'I\'ve trained a machine learning model and need to deploy it in production. What are the best practices for model serving, monitoring, and versioning? Should I use TensorFlow Serving, Flask, or cloud services?',
                'tags': 'machine-learning,deployment,mlops,tensorflow,python',
                'author': users[1],
                'created_at': timezone.now() - timedelta(hours=3),
                'upvotes': 9,
                'downvotes': 0
            },
            {
                'title': 'Web security best practices for developers?',
                'description': 'I\'m building a web application and want to ensure it\'s secure. What are the most important security practices I should implement? How do I protect against SQL injection, XSS, and CSRF attacks?',
                'tags': 'security,web-development,owasp,authentication',
                'author': users[2],
                'created_at': timezone.now() - timedelta(hours=1),
                'upvotes': 14,
                'downvotes': 1
            },
            {
                'title': 'TypeScript vs JavaScript for large projects?',
                'description': 'I\'m starting a new large-scale JavaScript project. Should I use TypeScript? What are the benefits and trade-offs? How does it affect development speed and code quality?',
                'tags': 'typescript,javascript,frontend,development',
                'author': users[5],
                'created_at': timezone.now() - timedelta(hours=4),
                'upvotes': 11,
                'downvotes': 2
            },
            {
                'title': 'Microservices vs Monolith architecture?',
                'description': 'I\'m designing a new system architecture. Should I go with microservices or a monolithic approach? What are the trade-offs in terms of complexity, scalability, and maintenance?',
                'tags': 'architecture,microservices,monolith,scalability',
                'author': users[6],
                'created_at': timezone.now() - timedelta(hours=2),
                'upvotes': 7,
                'downvotes': 1
            },
            {
                'title': 'Data visualization best practices?',
                'description': 'I need to create data visualizations for my application. What are the best libraries and practices for creating interactive charts and dashboards? Should I use D3.js, Chart.js, or Plotly?',
                'tags': 'data-visualization,charts,d3js,frontend',
                'author': users[7],
                'created_at': timezone.now() - timedelta(hours=30),
                'upvotes': 5,
                'downvotes': 0
            },
            {
                'title': 'CI/CD pipeline optimization?',
                'description': 'My CI/CD pipeline is taking too long to run. What are the best practices for optimizing build times and deployment processes? How can I implement parallel testing and caching?',
                'tags': 'ci-cd,devops,automation,testing',
                'author': users[8],
                'created_at': timezone.now() - timedelta(hours=45),
                'upvotes': 8,
                'downvotes': 1
            },
            {
                'title': 'Natural Language Processing with Python?',
                'description': 'I want to build an NLP application. What are the best libraries and approaches for text processing, sentiment analysis, and language modeling? Should I use spaCy, NLTK, or transformers?',
                'tags': 'nlp,python,machine-learning,text-processing',
                'author': users[9],
                'created_at': timezone.now() - timedelta(hours=15),
                'upvotes': 6,
                'downvotes': 0
            },
            {
                'title': 'API design best practices?',
                'description': 'I\'m designing a REST API for my application. What are the best practices for endpoint design, authentication, versioning, and documentation? How should I handle errors and rate limiting?',
                'tags': 'api,rest,design,backend',
                'author': users[5],
                'created_at': timezone.now() - timedelta(hours=8),
                'upvotes': 13,
                'downvotes': 1
            },
            {
                'title': 'Mobile app development with React Native?',
                'description': 'I want to build a mobile app using React Native. What are the pros and cons compared to native development? How do I handle platform-specific features and performance optimization?',
                'tags': 'react-native,mobile,development,cross-platform',
                'author': users[6],
                'created_at': timezone.now() - timedelta(hours=5),
                'upvotes': 9,
                'downvotes': 2
            }
        ]
        
        # Create questions
        questions = []
        for q_data in questions_data:
            question = Question.objects.create(  # type: ignore
                title=q_data['title'],
                description=q_data['description'],
                tags=q_data['tags'],
                author=q_data['author'],
                created_at=q_data['created_at']
            )
            questions.append(question)
            self.stdout.write(f'Created question: {question.title}')
        
        # Sample answers data
        answers_data = [
            {
                'question': questions[0],  # Django auth question
                'description': 'Django provides excellent built-in authentication. Start with `django.contrib.auth` and use the `@login_required` decorator. For customization, you can extend the User model or create a custom user model. Use Django\'s password reset views for password recovery.',
                'author': users[1],
                'upvotes': 8,
                'downvotes': 0
            },
            {
                'question': questions[0],
                'description': 'I recommend using Django REST Framework with JWT tokens for API authentication. It\'s more flexible than session-based auth and works well with modern frontend frameworks.',
                'author': users[2],
                'upvotes': 5,
                'downvotes': 1
            },
            {
                'question': questions[0],
                'description': 'Don\'t forget to implement proper password hashing and use HTTPS in production. Also consider using Django\'s built-in user groups and permissions for role-based access control.',
                'author': users[5],
                'upvotes': 3,
                'downvotes': 0
            },
            {
                'question': questions[1],  # React state management
                'description': 'For most applications, start with React Context API and useState/useReducer. Only move to Redux if you have complex state that needs to be shared across many components. Zustand is a great middle ground.',
                'author': users[3],
                'upvotes': 12,
                'downvotes': 0
            },
            {
                'question': questions[1],
                'description': 'Redux is overkill for most apps. Use Context API for simple state sharing and consider Zustand for more complex cases. The Redux Toolkit makes Redux easier, but it\'s still complex for beginners.',
                'author': users[4],
                'upvotes': 7,
                'downvotes': 2
            },
            {
                'question': questions[1],
                'description': 'Consider using React Query for server state management. It handles caching, background updates, and error states automatically. Combine it with Context API for client state.',
                'author': users[6],
                'upvotes': 6,
                'downvotes': 0
            },
            {
                'question': questions[2],  # Docker vs Kubernetes
                'description': 'Start with Docker Compose for development and simple deployments. Only use Kubernetes if you have multiple services, need auto-scaling, or have a team that can manage the complexity. The learning curve is steep.',
                'author': users[0],
                'upvotes': 6,
                'downvotes': 1
            },
            {
                'question': questions[2],
                'description': 'Consider managed Kubernetes services like EKS, GKE, or AKS if you go the K8s route. They handle the control plane management for you and provide better security defaults.',
                'author': users[8],
                'upvotes': 4,
                'downvotes': 0
            },
            {
                'question': questions[3],  # SQL vs NoSQL
                'description': 'For e-commerce, I\'d recommend PostgreSQL. You need ACID compliance for transactions, and relational databases handle complex queries better. NoSQL is great for specific use cases but not ideal for e-commerce.',
                'author': users[1],
                'upvotes': 9,
                'downvotes': 0
            },
            {
                'question': questions[3],
                'description': 'Consider using a hybrid approach. Use PostgreSQL for transactional data and MongoDB for product catalogs or user preferences. This gives you the best of both worlds.',
                'author': users[7],
                'upvotes': 5,
                'downvotes': 1
            },
            {
                'question': questions[4],  # Python performance
                'description': 'Use cProfile to identify bottlenecks, then optimize with Cython, Numba, or PyPy. Profile memory usage with memory_profiler. Consider using NumPy for numerical operations.',
                'author': users[2],
                'upvotes': 4,
                'downvotes': 0
            },
            {
                'question': questions[4],
                'description': 'Don\'t forget about async programming with asyncio for I/O-bound operations. Also consider using multiprocessing for CPU-intensive tasks. The concurrent.futures module is great for this.',
                'author': users[9],
                'upvotes': 3,
                'downvotes': 0
            },
            {
                'question': questions[5],  # Git workflow
                'description': 'I recommend GitHub Flow for most teams. Keep it simple: main branch is always deployable, create feature branches, submit PRs, merge after review. Avoid Git Flow unless you have complex release cycles.',
                'author': users[3],
                'upvotes': 11,
                'downvotes': 1
            },
            {
                'question': questions[5],
                'description': 'Set up branch protection rules and require code reviews. Use conventional commits for better changelog generation. Consider using semantic-release for automated versioning.',
                'author': users[8],
                'upvotes': 7,
                'downvotes': 0
            },
            {
                'question': questions[6],  # ML deployment
                'description': 'Use TensorFlow Serving for production ML model serving. It provides model versioning, A/B testing, and high-performance inference. For simpler cases, Flask with gunicorn works well.',
                'author': users[9],
                'upvotes': 8,
                'downvotes': 0
            },
            {
                'question': questions[6],
                'description': 'Consider using cloud ML services like AWS SageMaker or Google AI Platform. They handle infrastructure management and provide built-in monitoring and scaling capabilities.',
                'author': users[8],
                'upvotes': 6,
                'downvotes': 1
            },
            {
                'question': questions[7],  # Web security
                'description': 'Always use HTTPS, implement proper input validation, and use parameterized queries to prevent SQL injection. Use CSRF tokens and implement proper session management.',
                'author': users[0],
                'upvotes': 10,
                'downvotes': 0
            },
            {
                'question': questions[7],
                'description': 'Follow the OWASP Top 10 guidelines. Use security headers like CSP, HSTS, and X-Frame-Options. Implement rate limiting and use prepared statements for database queries.',
                'author': users[5],
                'upvotes': 8,
                'downvotes': 0
            },
            {
                'question': questions[8],  # TypeScript
                'description': 'TypeScript is definitely worth it for large projects. It catches errors at compile time, provides better IDE support, and makes refactoring much safer. Start with strict mode enabled.',
                'author': users[5],
                'upvotes': 9,
                'downvotes': 1
            },
            {
                'question': questions[8],
                'description': 'The learning curve is manageable if you already know JavaScript. Use gradual migration - you can add TypeScript to existing JS projects incrementally.',
                'author': users[6],
                'upvotes': 6,
                'downvotes': 0
            },
            {
                'question': questions[9],  # Microservices
                'description': 'Start with a monolith unless you have a clear need for microservices. They add complexity in networking, data consistency, and deployment. Only split when you have multiple teams or different scaling needs.',
                'author': users[6],
                'upvotes': 7,
                'downvotes': 0
            },
            {
                'question': questions[10],  # Data visualization
                'description': 'D3.js is the most powerful but has a steep learning curve. Chart.js is great for simple charts. Plotly is excellent for scientific/statistical visualizations. Choose based on your specific needs.',
                'author': users[7],
                'upvotes': 5,
                'downvotes': 0
            },
            {
                'question': questions[11],  # CI/CD
                'description': 'Use parallel jobs, implement caching for dependencies, and use Docker layers effectively. Consider using GitHub Actions or GitLab CI for easier setup. Cache node_modules, pip packages, and Docker layers.',
                'author': users[8],
                'upvotes': 8,
                'downvotes': 0
            },
            {
                'question': questions[12],  # NLP
                'description': 'spaCy is great for production NLP tasks, NLTK is good for research, and transformers (Hugging Face) are best for modern language models. Start with spaCy for most practical applications.',
                'author': users[9],
                'upvotes': 6,
                'downvotes': 0
            },
            {
                'question': questions[13],  # API design
                'description': 'Use RESTful conventions, implement proper HTTP status codes, and provide comprehensive error messages. Use OpenAPI/Swagger for documentation. Implement rate limiting and authentication.',
                'author': users[6],
                'upvotes': 10,
                'downvotes': 0
            },
            {
                'question': questions[14],  # React Native
                'description': 'React Native is great for cross-platform development but has limitations with native features. Use Expo for easier development or bare React Native for more control. Performance is generally good but not as good as native.',
                'author': users[5],
                'upvotes': 7,
                'downvotes': 1
            }
        ]
        
        # Create answers
        answers = []
        for a_data in answers_data:
            answer = Answer.objects.create(  # type: ignore
                question=a_data['question'],
                description=a_data['description'],
                author=a_data['author']
            )
            answers.append(answer)
            self.stdout.write(f'Created answer for: {a_data["question"].title}')
        
        # Create votes for questions
        for question in questions:
            # Get the target vote counts from the data
            target_upvotes = next(q['upvotes'] for q in questions_data if q['title'] == question.title)
            target_downvotes = next(q['downvotes'] for q in questions_data if q['title'] == question.title)
            
            # Create upvotes
            for i in range(target_upvotes):
                voter = random.choice(users)
                Vote.objects.get_or_create(  # type: ignore
                    user=voter,
                    question=question,
                    vote_type='question',
                    value=1
                )
            
            # Create downvotes
            for i in range(target_downvotes):
                voter = random.choice(users)
                Vote.objects.get_or_create(  # type: ignore
                    user=voter,
                    question=question,
                    vote_type='question',
                    value=-1
                )
        
        # Create votes for answers
        for answer in answers:
            # Get the target vote counts from the data
            target_upvotes = next(a['upvotes'] for a in answers_data if a['description'] == answer.description)
            target_downvotes = next(a['downvotes'] for a in answers_data if a['description'] == answer.description)
            
            # Create upvotes
            for i in range(target_upvotes):
                voter = random.choice(users)
                Vote.objects.get_or_create(  # type: ignore
                    user=voter,
                    answer=answer,
                    vote_type='answer',
                    value=1
                )
            
            # Create downvotes
            for i in range(target_downvotes):
                voter = random.choice(users)
                Vote.objects.get_or_create(  # type: ignore
                    user=voter,
                    answer=answer,
                    vote_type='answer',
                    value=-1
                )
        
        self.stdout.write(
            f'Successfully created:\n'
            f'- {len(users)} users\n'
            f'- {len(questions)} questions\n'
            f'- {len(answers)} answers\n'
            f'- Multiple votes for questions and answers'
        ) 