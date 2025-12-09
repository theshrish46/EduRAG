from langchain_text_splitters import RecursiveCharacterTextSplitter
import json

json_object = {
    "subject_name": "Big Data Analytics",
    "course_code": "MMCA3I11A",
    "modules": [
        {
            "module_number": "Module-1",
            "module_name": "Big Data Fundamentals",
            "syllabus_content": "Introduction to Big Data: Classification of digital data: Structured Data, Sources of Structured Data, Ease of working with structured Data, Semi-Structured Data, Sources of Semi-Structured Data, Unstructured Data, Sources of Unstructured Data, Dealing with Unstructured data; Definition of Big Data; Characteristics of Big Data (Volume, Velocity, Variety, Veracity, Value); Why Big Data; Traditional BI versus Big Data;\n\nBig Data Analytics Concepts: Example Applications; Basic Nomenclature; Analytics; Analytical Model Requirements; Analysis Process Model; Job profiles involved;\n\nData Collection, Sampling, and Preprocessing: Sampling; Types of data elements; Visual Data Explorations & Exploratory Statistical Analysis; Missing values; Outlier Detection and Treatment; Standardizing Data; Categorization;",
        },
        {
            "module_number": "Module-2",
            "module_name": "Technologies in Big Data Analytics",
            "syllabus_content": "Big Data Technology: Hadoop’s parallel world — critical components of Hadoop; Old versus New approaches; Data Discovery: Work the way people’s minds work; Open-Source Technology for Big Data Analytics; The Cloud and Big data, - Difference between Cloud & Big Data; Predictive Analytics Moves into the Limelight; Software as a Service BI; Mobile business intelligence and big data — Ease of Mobile Application Deployment; Crowdsourcing Analytics, Inter-and Trans-Firewall Analytics; Big Data Analytics combined with Descriptive, Predictive and Prescriptive Analytics; Holistic View of Analytics",
        },
        {
            "module_number": "Module-3",
            "module_name": "Modern Data Management and Analytics Systems",
            "syllabus_content": "NoSQL — Where it is Used, What is it, Types of NoSQL Databases, Why NoSQL, Advantages of NoSQL, What we miss with NoSQL, Use of NoSQL in industry, NoSQL vendors, SQL versus NoSQL, NewSQL, Comparison of SQL, NoSQL, and NewSQL;\n\nMeet Hadoop: Data; data storage and analysis; Comparison with other systems: RDBMS, Grid Computing, Volunteer computing; A brief history of Hadoop, Hadoop at Yahoo; Apache Hadoop and Hadoop Ecosystem.",
        },
        {
            "module_number": "Module-4",
            "module_name": "HDFS - Design, Concepts, and Operations",
            "syllabus_content": "Hadoop Distributed File System: The design of HDFS, HDFS concepts — Blocks, Name nodes and Datanodes, HDFS Federation, HDFS High-Availability, Basic file system operations, Hadoop file systems, The java interface- Reading data from Hadoop URL, Reading data using the file system API, Writing data, Directories, Querying the file system, deleting data, Data flow - Anatomy of a file read, Anatomy of a file write, Coherency Model, Parallel copying with distcp, Keeping an HDFS cluster balanced, Hadoop Archives",
        },
        {
            "module_number": "Module-5",
            "module_name": "MapReduce Framework - Data Analysis, Application Development, and Execution in Hadoop",
            "syllabus_content": "Map Reduce: A weather dataset — data format; Analyzing the data with Unix Tools; Analyzing the Data with Hadoop - Map and Reduce, - Java MapReduce; Scaling out, Data Flow, - Combiner Functions; Hadoop streaming — Ruby, Python; Hadoop Pipes Compiling and Running;\n\nDeveloping a Map Reduce Application: The Configuration API - Combining Resources, - Variable Expansion; Writing a Unit Test - Mapper, - Reducer; Running Locally on Test Data - Running a Job in a Local Job Runner, Testing the Driver; Running on a Cluster - Packaging, - Launching a Job, - The MapReduce Web UI, Retrieving the Results, - Debugging a Job, - Hadoop Logs, - Remote Debugging.",
        },
    ],
    "course_outcomes": [
        {
            "description": "Demonstrate the classification of digital data, analyze Big Data characteristics and analytics concepts, and apply preprocessing techniques to prepare data for effective analysis and decision-making.",
            "blooms_level": "L2, L3",
        },
        {
            "description": "Analyze Big Data technologies and Apply integrated analytics approaches to create effective business intelligence solutions.",
            "blooms_level": "L3, L4",
        },
        {
            "description": "Develop skills to apply NoSQL databases and Hadoop ecosystem components for big data solutions.",
            "blooms_level": "L3, L4",
        },
        {
            "description": "Analyze the design, concepts, and data flow of HDFS to evaluate its role in reliable and scalable big data storage.",
            "blooms_level": "L3, L4",
        },
        {
            "description": "Develop and execute MapReduce applications on Hadoop for large-scale data analysis and processing.",
            "blooms_level": "L3, L4",
        },
    ],
    "program_outcomes": {
        "PO1": {"CO1": 3, "CO2": 3, "CO3": 3, "CO4": 3, "CO5": 3},
        "PO2": {"CO1": 3, "CO2": 3, "CO3": 3, "CO4": 3, "CO5": 3},
        "PO3": {"CO1": 2, "CO3": 3, "CO4": 3, "CO5": 3},
    },
}

meta_data = []
chunk = []


def get_chunks(json_object):
    for module in json_object["modules"]:
        chunk_text = f"Subject Name {json_object["subject_name"] } ({json_object["course_code"]})\n Module ({module['module_number']}) ({module['module_name']}) ({module['syllabus_content']})"
        chunk.append(chunk_text)

        meta_data.append(
            {
                "subject_name": json_object.get("subject_name"),
                "course_code": json_object.get("course_code"),
                "course_outcomes": json.dumps(json_object.get("course_outcomes")),
                "program_outcomes": json.dumps(json_object.get("program_outcomes")),
            }
        )
    return chunk, meta_data
