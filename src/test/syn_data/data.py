agents = {
    "Adam": "Developer – Software engineer specializing in backend development, API design, and system architecture. Proficient in programming languages like Python and JavaScript. Responsible for writing code, debugging, and implementing features.",
    
    "Eve": "UI/UX Designer – Specialist in user interface and user experience design. Creates wireframes, prototypes, and visual designs using tools like Figma. Focuses on usability, accessibility, and aesthetics to enhance user interactions with products.",
    
    "Alex": "Marketer – Professional in digital marketing, campaign strategy, market analysis, and advertising. Analyzes metrics, develops promotional strategies, manages campaigns, creates content, tracks conversion rates, optimizes funnels, and grows user engagement.",
    
    "Sophia": "Support – Customer service specialist focused on resolving user issues, answering questions, and improving customer experience through various communication channels. Handles tickets, responds to complaints, documents solutions, and provides assistance.",
    
    "Charlie": "Researcher – Data analyst skilled in extracting insights, creating reports, and conducting market research. Compiles and interprets complex information, visualizes data, identifies patterns, generates statistics, and delivers analytical findings.",
    
    "Grace": "Scheduler – Specialist in time management, appointment coordination, and event planning. Organizes calendars, schedules meetings, coordinates logistics, sends invitations, and ensures efficient allocation of time and resources.",
    
    "Liam": "Researcher – Information gathering expert who finds, evaluates, and synthesizes information from online sources for various projects and decisions. Conducts web research, compares options, documents findings, and generates comprehensive reports.",

    "Oliver": "Project Manager – Professional in project planning, task management, and team coordination. Oversees project timelines, assigns tasks, tracks progress, manages resources, communicates with stakeholders, and ensures project goals are met.",
    
    "Max": "Cybersecurity Specialist – Expert in protecting systems, networks, and data from cyber threats. Conducts security audits, implements security measures, monitors for vulnerabilities, responds to incidents, and ensures compliance with security standards.",
    
    "Luna": "Content Writer – Skilled in creating written content for various platforms, including blogs, articles, and documentation. Researches topics, writes clear and engaging content, edits for clarity, and ensures accuracy in information presented.",
    
    "Mia": "QA Tester – Quality assurance professional who identifies bugs, verifies functionality, and ensures products meet standards through systematic testing procedures. Creates test cases, validates features, reports issues, and ensures quality standards.",
    
    "Noah": "Database Administrator – Expert in database design, optimization, maintenance, and data management. Ensures efficient storage and retrieval of information, creates schemas, optimizes queries, and manages data migrations."
}

tools = {
    "IDE": "IDE or Code development environment for writing and debugging software. Used for programming in Python, JavaScript, and other languages to build applications and features. Essential for coding, syntax highlighting, auto-completion, and running tests.",
    
    "Figma": "Figma is a Visual design platform for creating user interfaces, wireframes, prototypes, and graphic designs for websites and applications. Used for layout design, mockups, UI components, and collaborative design workflows.",
    
    "Analytics": "Data analysis platform for tracking metrics, generating reports on user behavior, and providing insights from marketing campaigns and website interactions. Displays dashboards, measures performance, and helps data-driven decisions.",
    
    "Excel": "Excel is a Spreadsheet application for data organization, financial calculations, statistical analysis, and creating charts to visualize information. Handles numerical data, formulas, pivots, and data visualization needs.",
    
    "Calendar": "Use Calendar to schedule managing appointments, organizing meetings, setting reminders, and coordinating events across teams. Manages time, shows availability, sends notifications, and organizes schedules efficiently.",
    
    "Terminal": "Command-line interface for executing system commands, running scripts, managing servers, and performing development operations. Terminal is Used for system tasks, deployment, file operations, and automation scripts.",
    
    "Browser": "Use the Browser for accessing online resources, conducting research, reviewing websites, and testing web applications. Used for web access, information retrieval, and website testing.",
    
    "Email": "Email is for business communication, sending updates, contacting customers, and sharing information with teams. Handles correspondence, notifications, newsletters, and formal communications.",
    
    "Notebook": "Documentation application for taking notes, creating documentation, writing content, and organizing information in a structured format. Used for documenting processes, writing guides, and content creation.",
    
    "Jira": "Jira: Project tracking system for managing tasks, documenting bugs, assigning work items, and monitoring project progress. Tracks issues, organizes sprints, assigns tickets, and monitors project status.",
    
    "Slack": "Slack is a Team messaging platform for real-time communication, file sharing, and collaboration with integrated channels for different topics. Facilitates team discussions, quick updates, and informal communication.",
    
    "Docker": "Containerization platform for creating consistent development environments, deploying applications, and managing microservices. Docker Packages applications with dependencies for consistent deployment.",
    
    "Git": "Git: Version control system for tracking code changes, managing software versions, and facilitating collaborative development. Manages code history, branches, merges, and collaborative code contributions."
}

test_data = [
    # Development
    {"query": "Open the IDE and terminal to write and test a Python script for processing CSV files.", "expected_agent": "Adam", "expected_tools": ["IDE", "Terminal"]},
    {"query": "Build and debug a React frontend authentication component using the IDE and Browser.", "expected_agent": "Adam", "expected_tools": ["IDE", "Browser"]},
    {"query": "Use Git and Docker in the terminal to configure containers and set up a Jenkins CI pipeline.", "expected_agent": "Adam", "expected_tools": ["Git", "Docker", "Terminal"]},
    {"query": "Use the IDE and Browser to identify and fix the login bug blocking user access.", "expected_agent": "Adam", "expected_tools": ["IDE", "Browser"]},
    {"query": "Develop a REST API endpoint for user profiles, using the IDE for coding and Terminal for testing.", "expected_agent": "Adam", "expected_tools": ["IDE", "Terminal"]},

    # Design
    {"query": "Design a new logo in Figma using the updated brand colors.", "expected_agent": "Eve", "expected_tools": ["Figma"]},
    {"query": "Create wireframes for the mobile app checkout flow using Figma.", "expected_agent": "Eve", "expected_tools": ["Figma"]},
    {"query": "Redesign the navigation menu for better usability in Figma, and preview it in the Browser.", "expected_agent": "Eve", "expected_tools": ["Figma", "Browser"]},
    {"query": "Design icon sets for the new dashboard feature within Figma.", "expected_agent": "Eve", "expected_tools": ["Figma"]},
    {"query": "Use Figma to create dark mode versions of all application screens.", "expected_agent": "Eve", "expected_tools": ["Figma"]},

    # Marketing
    {"query": "Analyze email campaign click-through rates using Analytics and Excel.", "expected_agent": "Alex", "expected_tools": ["Analytics", "Excel"]},
    {"query": "Set up a drip email campaign for new leads and monitor results in Analytics.", "expected_agent": "Alex", "expected_tools": ["Email", "Analytics"]},
    {"query": "Plan the social media calendar for product launch using Excel and Calendar.", "expected_agent": "Alex", "expected_tools": ["Excel", "Calendar"]},
    {"query": "Research competitor marketing tactics online and summarize findings in the Notebook.", "expected_agent": "Alex", "expected_tools": ["Browser", "Notebook"]},
    {"query": "Generate a detailed Q2 marketing performance report with Analytics and Excel.", "expected_agent": "Alex", "expected_tools": ["Analytics", "Excel"]},

    # Support
    {"query": "Reply to a customer complaint about billing via Email and log the communication in Slack.", "expected_agent": "Sophia", "expected_tools": ["Email", "Slack"]},
    {"query": "Answer user questions about the export feature using Email and Slack.", "expected_agent": "Sophia", "expected_tools": ["Email", "Slack"]},
    {"query": "Document the most common support issues in a Notebook and track them in Jira.", "expected_agent": "Sophia", "expected_tools": ["Notebook", "Jira"]},
    {"query": "Send follow-up emails to customers with resolved tickets and update the cases in Jira.", "expected_agent": "Sophia", "expected_tools": ["Email", "Jira"]},
    {"query": "Write a knowledge base article explaining password reset, using Notebook and Browser.", "expected_agent": "Sophia", "expected_tools": ["Notebook", "Browser"]},

    # Research
    {"query": "Use Excel and Analytics to analyze user session data for funnel drop-offs.", "expected_agent": "Charlie", "expected_tools": ["Excel", "Analytics"]},
    {"query": "Create a quarterly business KPI report in Excel and document insights in Notebook.", "expected_agent": "Charlie", "expected_tools": ["Excel", "Notebook"]},
    {"query": "Research industry trends online and document findings in Notebook.", "expected_agent": "Charlie", "expected_tools": ["Browser", "Notebook"]},
    {"query": "Calculate the ROI of recent feature development using Excel and Analytics.", "expected_agent": "Charlie", "expected_tools": ["Excel", "Analytics"]},
    {"query": "Produce data visualizations for the board using Excel and complement with notes in Notebook.", "expected_agent": "Charlie", "expected_tools": ["Excel", "Notebook"]},

    # Scheduling
    {"query": "Schedule weekly team meetings for the sprint using Calendar and Email.", "expected_agent": "Grace", "expected_tools": ["Calendar", "Email"]},
    {"query": "Create a timeline for quarterly product review meetings in Calendar and track in Jira.", "expected_agent": "Grace", "expected_tools": ["Calendar", "Jira"]},
    {"query": "Set up project deadline reminders in Calendar and notify the team via Slack.", "expected_agent": "Grace", "expected_tools": ["Calendar", "Slack"]},
    {"query": "Coordinate interview schedules for candidates and team via Calendar and Email.", "expected_agent": "Grace", "expected_tools": ["Calendar", "Email"]},
    {"query": "Organize logistics for the product launch event with Calendar and planning notes in Notebook.", "expected_agent": "Grace", "expected_tools": ["Calendar", "Notebook"]},

    # Web Research
    {"query": "Find recent machine learning in healthcare papers using Browser and take notes in Notebook.", "expected_agent": "Liam", "expected_tools": ["Browser", "Notebook"]},
    {"query": "Research and compare cloud hosting providers using Browser and Excel.", "expected_agent": "Liam", "expected_tools": ["Browser", "Excel"]},
    {"query": "Find mobile app onboarding case studies online and summarize them in Notebook.", "expected_agent": "Liam", "expected_tools": ["Browser", "Notebook"]},
    {"query": "Identify EU customer data compliance requirements using Browser and document in Notebook.", "expected_agent": "Liam", "expected_tools": ["Browser", "Notebook"]},
    {"query": "Search for competitors' product launch news with Browser and log articles in Notebook.", "expected_agent": "Liam", "expected_tools": ["Browser", "Notebook"]},

    # Project Management
    {"query": "Track and update sprint tasks in Jira and communicate status in Slack.", "expected_agent": "Oliver", "expected_tools": ["Jira", "Slack"]},
    {"query": "Assign team members to workstreams and record assignments in Jira and Excel.", "expected_agent": "Oliver", "expected_tools": ["Jira", "Excel"]},
    {"query": "Build a detailed project timeline and milestones in Jira and Calendar.", "expected_agent": "Oliver", "expected_tools": ["Jira", "Calendar"]},
    {"query": "Prepare a stakeholder meeting status report using Jira for tracking and Notebook for notes.", "expected_agent": "Oliver", "expected_tools": ["Jira", "Notebook"]},
    {"query": "Plan Q3 resource allocation in Jira and document the plan in Excel.", "expected_agent": "Oliver", "expected_tools": ["Jira", "Excel"]},

    # Security
    {"query": "Conduct a security audit of database access controls using Terminal and record findings in Notebook.", "expected_agent": "Max", "expected_tools": ["Terminal", "Notebook"]},
    {"query": "Implement end-to-end encryption for sensitive fields in the IDE and verify via Terminal.", "expected_agent": "Max", "expected_tools": ["Terminal", "IDE"]},
    {"query": "Update firewall rules on production servers using Terminal and document changes in Notebook.", "expected_agent": "Max", "expected_tools": ["Terminal", "Notebook"]},
    {"query": "Investigate unusual login patterns with Terminal and analyze data in Analytics.", "expected_agent": "Max", "expected_tools": ["Terminal", "Analytics"]},
    {"query": "Perform a security-focused code review in the IDE and record vulnerabilities in Notebook.", "expected_agent": "Max", "expected_tools": ["IDE", "Notebook"]},

    # Content Writing
    {"query": "Write API endpoint documentation in Notebook and verify information using Browser.", "expected_agent": "Luna", "expected_tools": ["Notebook", "Browser"]},
    {"query": "Create a user guide for the reporting feature in Notebook and include screenshots from Browser.", "expected_agent": "Luna", "expected_tools": ["Notebook", "Browser"]},
    {"query": "Draft a blog post on recent product enhancements in Notebook and fact-check via Browser.", "expected_agent": "Luna", "expected_tools": ["Notebook", "Browser"]},
    {"query": "Write templated onboarding emails in Notebook and send them via Email.", "expected_agent": "Luna", "expected_tools": ["Notebook", "Email"]},
    {"query": "Update product descriptions for clarity in Notebook and review changes on Browser.", "expected_agent": "Luna", "expected_tools": ["Notebook", "Browser"]},

    # QA Testing
    {"query": "Test every checkout step for bugs using Browser and log issues in Jira.", "expected_agent": "Mia", "expected_tools": ["Browser", "Jira"]},
    {"query": "Run regression tests on updated features using Browser and Jira.", "expected_agent": "Mia", "expected_tools": ["Browser", "Jira"]},
    {"query": "Create detailed test cases for authentication flow in Notebook and sync them to Jira.", "expected_agent": "Mia", "expected_tools": ["Notebook", "Jira"]},
    {"query": "Verify last sprint's bug fixes using Browser and track results in Jira.", "expected_agent": "Mia", "expected_tools": ["Browser", "Jira"]},
    {"query": "Perform load testing on database queries in Terminal and report results in Jira.", "expected_agent": "Mia", "expected_tools": ["Terminal", "Jira"]},

    # Database Management
    {"query": "Optimize slow SQL queries in the IDE and test improvements in Terminal.", "expected_agent": "Noah", "expected_tools": ["IDE", "Terminal"]},
    {"query": "Set up automated database backups and document the recovery process in Notebook, using Terminal.", "expected_agent": "Noah", "expected_tools": ["Terminal", "Notebook"]},
    {"query": "Design a normalized schema for user profiles in IDE and document it in Notebook.", "expected_agent": "Noah", "expected_tools": ["IDE", "Notebook"]},
    {"query": "Execute migration scripts for updated database structure using Terminal and IDE.", "expected_agent": "Noah", "expected_tools": ["Terminal", "IDE"]},
    {"query": "Diagnose and fix intermittent database connection errors using Terminal and IDE.", "expected_agent": "Noah", "expected_tools": ["Terminal", "IDE"]},

    # Mixed/Ambiguous
    {"query": "Develop a system health monitoring dashboard in the IDE and test views in Browser.", "expected_agent": "Adam", "expected_tools": ["IDE", "Browser"]},
    {"query": "Design a UI for database query results in Figma and preview in Browser.", "expected_agent": "Eve", "expected_tools": ["Figma", "Browser"]},
    {"query": "Write a script in the IDE to analyze marketing data and export results to Excel.", "expected_agent": "Adam", "expected_tools": ["IDE", "Excel"]},
    {"query": "Set up automated UI testing for API endpoints using IDE for scripts and Jira for tracking.", "expected_agent": "Mia", "expected_tools": ["IDE", "Jira"]},
    {"query": "Create technical documentation diagrams in Figma and write supporting text in Notebook.", "expected_agent": "Eve", "expected_tools": ["Figma", "Notebook"]},
    {"query": "Research and implement caching for the API with Browser and code in IDE.", "expected_agent": "Adam", "expected_tools": ["Browser", "IDE"]},
    {"query": "Document team security protocols in Notebook and cross-check with Browser.", "expected_agent": "Luna", "expected_tools": ["Notebook", "Browser"]},
    {"query": "Analyze customer feedback data in Excel and summarize recurring issues in Notebook.", "expected_agent": "Charlie", "expected_tools": ["Excel", "Notebook"]},
    {"query": "Draft a workflow diagram for sensitive customer data handling in Jira and explain it in Notebook.", "expected_agent": "Oliver", "expected_tools": ["Jira", "Notebook"]},
    {"query": "Optimize application code for faster loading in the IDE and analyze results with Analytics.", "expected_agent": "Adam", "expected_tools": ["IDE", "Analytics"]}
]