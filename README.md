# AI-Powered Car & Insurance Information Platform
 
 ## Description  
 The **AI-Powered Car & Insurance Information Platform** allows users to search for car details, compare vehicles, and estimate insurance costs using AI. The system leverages **LLMs such as OpenAI's ChatGPT or Mistral** to generate intelligent insights, ensuring users make informed decisions.
 
 ## Features & Acceptance Criteria  
 
 ### 1. Car Search and Details  
 - Users can input queries like **"Best SUVs under $30,000"** or **"Toyota Corolla 2022 specs"** and receive AI-generated insights.  
 - AI extracts and displays specifications, pricing estimates, and features.  
 
 ### 2. Car Comparisons  
 - Users can compare two or more cars by entering queries such as **"Compare Tesla Model 3 vs. BMW i4"**.  
 - AI provides **structured pros and cons**, including performance, pricing, fuel efficiency, and key differences.  
 
 ### 3. Insurance Estimations  
 - AI estimates insurance costs based on car type, model, and general risk factors.  
 - Users receive **estimated premiums and coverage suggestions** aligned with industry trends.  
 
 ### 4. Personalized Recommendations  
 - AI suggests cars and insurance options based on user **budget, needs, and preferences**.  
 - Users can refine searches dynamically with follow-up queries.  
 
 ### 5. AI Chatbot Interaction  
 - Users can chat with an **LLM-powered AI chatbot** for car-buying advice, financing options, and insurance queries.  
 - The chatbot supports **dynamic follow-ups**, such as **"What about a hybrid alternative?"**.  
 
 ## Conditions of Satisfaction  
 
 - **AI Accuracy:** The LLM must generate relevant and informative responses.  
 - **Car Comparison Logic:** AI-generated comparisons should provide clear **advantages and disadvantages**.  
 - **Insurance Insights:** Estimates should align with **industry standards**.  
 - **Chatbot Responsiveness:** The chatbot should handle follow-ups smoothly.  
 - **User-Friendly UI:** Results should be structured and visually appealing using **Tailwind CSS and Bootstrap**.  
 
 ## Definition of Done  
 
 - Users can **input queries** for car details, comparisons, and insurance insights.  
 - The system **generates AI-powered responses** via OpenAI or Mistral API.  
 - The AI chatbot provides **follow-up recommendations and clarifications**.  
 - The UI is **responsive and easy to navigate**, displaying structured car and insurance data.  
 - The **Flask-based backend** processes API requests efficiently.  
 
 ---
 
 ## Development Tasks  
 
 ### **SC 1.1: Implement Car Search and AI Query Handling**  
 📌 **Estimated Effort:** 12–15 hours  
 
 #### **Acceptance Criteria**  
 - Users can input **car-related queries in natural language**.  
 - AI extracts details such as **model, year, and features**.  
 
 #### **Subtasks**  
 - [ ] Set up **Flask API endpoint** for car queries  
 - [ ] Integrate **OpenAI or Mistral API** for AI-generated responses  
 - [ ] Implement **query validation and handling**  
 - [ ] Write **unit tests** for query processing  
 - [ ] Conduct **QA testing and bug fixes**  
 
 ---
 
 ### **SC 1.2: Develop AI-Based Car Comparison System**  
 📌 **Estimated Effort:** 10–12 hours  
 
 #### **Acceptance Criteria**  
 - AI provides **clear pros and cons** for each car.  
 - The system highlights **performance, pricing, and key differences**.  
 
 #### **Subtasks**  
 - [ ] Implement API to handle **multiple-car queries**  
 - [ ] Improve AI prompts to return **structured comparisons**  
 - [ ] Ensure **UI formatting for easy readability**  
 - [ ] Write **unit tests** and handle edge cases  
 
 ---
 
 ### **SC 1.3: Implement AI-Based Insurance Estimations**  
 📌 **Estimated Effort:** 10–14 hours  
 
 #### **Acceptance Criteria**  
 - Users receive **estimated insurance premiums** based on car details.  
 - AI generates **coverage comparisons and recommendations**.  
 
 #### **Subtasks**  
 - [ ] Set up **Flask route** for insurance queries  
 - [ ] Integrate **OpenAI or Mistral API** for insurance insights  
 - [ ] Format AI responses for **clarity and readability**  
 - [ ] Write **unit tests** and handle edge cases  
 
 ---
 
 ### **SC 1.4: Build LLM-Powered Chatbot for Car & Insurance Queries**  
 📌 **Estimated Effort:** 14–18 hours  
 
 #### **Acceptance Criteria**  
 - The chatbot **handles follow-up queries** dynamically.  
 - AI suggests **car and insurance options** based on user preferences.  
 
 #### **Subtasks**  
 - [ ] Develop **chatbot Flask route** and integrate with UI  
 - [ ] Improve AI response formatting for **structured replies**  
 - [ ] Implement **query memory** to handle follow-ups  
 - [ ] Conduct **user testing and refinements**  
 
 ---
 
 ## **Workflow Overview**  
 
 1. **User enters a query**, such as **"Best sedans under $25,000"**.  
 2. **Flask API calls LLM**, such as ChatGPT or Mistral, and AI generates a response.  
 3. **User requests a comparison**, such as **"Compare Toyota Camry vs. Honda Accord"**.  
 4. **AI generates structured insights**, including pros and cons.  
 5. **User asks for insurance costs**, such as **"How much would insurance cost for a used Honda Accord?"**  
 6. **AI provides estimated premiums** and coverage options.  
 7. **User interacts with chatbot** for further advice, such as **"What’s a good hybrid alternative?"**  
 
 ---
 
 ## **Agents Overview**  
 
 ### **1. Car Query Handler Agent**  
 - Extracts **car details** from user queries.  
 - Interacts with LLM to generate **car specifications and pricing estimates**.  
 
 ### **2. Comparison Generator Agent**  
 - Handles **multi-car comparisons**.  
 - Structures AI responses into **easy-to-read pros and cons**.  
 
 ### **3. Insurance Insight Agent**  
 - Generates **estimated insurance premiums**.  
 - Provides **policy suggestions** based on car type and risk factors.  
 
 ### **4. Chatbot Interaction Agent**  
 - Maintains **context-aware conversations** for car and insurance advice.  
 - Handles **follow-up questions** and personalized recommendations.  
 
 ---
 
 ## **Definition of Ready**  
 
 - The system has **access to LLM APIs** such as OpenAI or Mistral.  
 - The **Flask backend** is ready to process user inputs and generate structured outputs.  
 - The **UI is designed using Tailwind CSS and Bootstrap** for easy navigation.  
 
