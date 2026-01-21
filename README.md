# team-1-project
Project Abstract
The Rio Grande River is a vital lifeline for New Mexico, providing essential water resources for agriculture, urban development, and ecosystems across the counties it traverses. However, increasing demands from population growth, climate variability, and competing uses have strained this shared resource, leading to concerns over sustainable water management. This project aims to address the problem of limited accessible insights into historical water consumption patterns by developing an interactive online dashboard that visualizes water withdrawal and consumption data for the key counties along the Rio Grande in New Mexico—specifically Taos, Rio Arriba, Santa Fe, Bernalillo, Valencia, Socorro, Sierra, and Doña Ana—from 2000 to 2020, aggregated in 5-year increments (2000, 2005, 2010, 2015, 2020). Users will be able to explore trends at the individual county level, such as breakdowns by sector (e.g., irrigation, public supply, industrial), source (groundwater vs. surface water), and total volumes in million gallons per day, as well as aggregated views for the entire Rio Grande corridor to highlight regional dynamics. 

Our dataset, sourced from the U.S. Geological Survey (USGS) Water Use Program, offers comprehensive, county-level estimates of water use compiled every five years, making it ideal for temporal analysis and trend detection. These data are publicly available and rigorously vetted, ensuring reliability for policy-relevant visualizations. The dashboard, built using Streamlit, will feature interactive charts, maps, and filters to empower stakeholders like water managers, policymakers, and educators to identify high-consumption areas, assess conservation progress, and inform future planning. Expected outcomes include heightened awareness of water scarcity risks and data-driven recommendations for equitable allocation, potentially influencing local sustainability initiatives and contributing to broader efforts in arid-region resource stewardship. By democratizing access to this critical data, the project could foster community engagement and support New Mexico's goals for resilient water infrastructure amid ongoing drought challenges. 
Expected Contributions 

Team members will collaborate on all aspects of the project, with individual roles assigned as follows (to be updated upon team formation): 
Dataset research and justification: Agustin Rodriguez (PM) – Identify and validate USGS datasets, ensure coverage of Rio Grande counties, and document data limitations. 
Data cleaning and preprocessing: Jake Miller – Handle missing values, standardize formats across the years, and aggregate data for county-specific and regional views. 
Writing analysis code and producing visualizations: Randall McCoy– Develop Python scripts for data analysis (e.g., using Pandas and Matplotlib) and creating interactive plots for the dashboard. 
Managing GitHub workflow (branches, commits, merges): Pratik– Set up repository structure, enforce version control best practices, and coordinate code reviews. 
Building the Streamlit application: Noah Casey – Design and implement the user interface, integrate visualizations, and deploy the dashboard for public access. 
Writing documentation and project report: Agustin Rodriguez– Author the README, user guide, and final report, including methodology and findings. 
Randall McCoy– Develop Python scripts for data analysis (e.g., using Pandas and Matplotlib) and creating interactive plots for the dashboard. Managing GitHub workflow (branches, commits, merges)


Dependencies to run Streamlit site locally:
openai streamlit library. Info can be found at:https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps#build-a-chatgpt-like-app
Python 3.12
Streamlit Library (newest release)
Matplotlib (pip install matplotlib)