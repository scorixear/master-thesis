## 1.4 Example
The following example will be used in many parts of this book.
Although the situations described here are realistic, all persons in this example are fictitious and do not exist.

The Russos live in a flat in a small town on the edge of the commuter belt of a large city.
Mrs. Russo, a former optometrist, is 68 years old and—following a fall in the bathroom last year with a fracture of a leg and some complications—suffers from lasting limitations of her movement capacity, affecting her ability to perform some of her activities of daily living (e.g., taking a shower, shopping, meeting with friends). She was also diagnosed with a mild case of depression along with an anxiety disorder.
Mr. Russo, a former software consultant, is 72 and, following a myocardial infarction 15 years ago, was diagnosed with heart failure 3 years ago.
The Russos’ general practitioner (GP), Dr. Andersson, has furthermore diagnosed him with hypercholesterolemia (elevated blood cholesterol) and diabetes and has put him on medication with several drugs.
Dr. Andersson also advised Mr. Russo to take up mild physical activity and lose some of his excess weight, but—following a brief episode of motivation and a Nordic walking course—he has found it impossible to follow her advice and sustain regular physical activity, in part because he increasingly needs to help his wife in performing her daily activities.

One morning, Mr. Russo wakes up early in the morning from severe shortness of breath.
Although he has experienced this symptom before in a milder form, he immediately senses that something is wrong and calls his GP.
Dr. Andersson comes for a home visit and finds him in bed with low blood pressure, elevated heart rate, and pulmonary edema.
She diagnoses him with an exacerbation of heart failure, strongly advises him to be admitted to Ploetzberg Hospital university medical center, and subsequently calls an ambulance.
The paramedics arrive and perform a resting 12-lead electrocardiogram (ECG), and the emergency physician puts Mr. Russo on oxygen.
After arrival at Ploetzberg Hospital, Mr. Russo is admitted to the cardiology ward and treated with drugs.
Blood samples are taken and an echocardiography is performed.
His condition improves over a week, but an intracardiac catheter examination (coronary angiography) shows a severe stenosis of a main coronary artery, which is treated immediately.
Two weeks later, Mr. Russo is discharged from the hospital and, following a brief stay at home, begins rehabilitation at the Kreikebohm Rehabilitation Centre.
Meanwhile, Mrs. Russo’s children have organized a home nursing service for her that comes twice a day to support her while her husband is away, along with a domestic help to assist her with the housework.

Dr. Andersson receives discharge letters from both Ploetzberg Hospital as well as the Kreikebohm Rehabilitation Centre.
She adapts his medication according to the cardiologists’ advice.
Along with his wife, Mr. Russo enrolls in a support program arranged by his health insurance company where he uses an app on his mobile phone to enter data on his physical and mental well-being and his weight.
Furthermore, he receives an activity tracker that also measures his heart rate.
Among other things, Dr. Andersson uses this data to manage the course of his disease and for adapting her treatment.
Researchers from Ploetzberg Hospital ask Mr. Russo whether he would participate in a scientific study to investigate the effect of close-knit home monitoring on rehospitalization in patients with heart failure, to which he agrees.
He can observe his monitoring data on his smartphone.

### 1.5.1 Life Situations
Consider a recent health-related situation you were involved in.
Which life situation (Sect. 1.2) does it correspond to and what was your role in this life situation (Sect. 1.3)? List some of the requirements you had in this role and in this life situation.

Answer:
My father was admitted to the hospital after suddenly showing symptoms of numbness in the left arm, confusion, and trouble seeing while at home.
We called the ambulance, and after a short examination, the ambulance team took him to the nearest hospital for further diagnosis and treatment.
This situation corresponds to an emergency life situation. I participated in this situation as a close relative.
My urgent requirements were to know which hospital my father was taken to and to obtain more information on the suspected diagnosis (here: stroke) and the next steps of diagnosis and therapy.

### 1.5.2 Requirements of Various Stakeholders
Consider the requirements of various stakeholders when it comes to health information systems supporting various life situations.
Can you imagine situations where the requirements of two stakeholder groups differ or even contradict each other? What does this imply when building health information systems?

Answer:
While a patient is being treated for an acute disease, the requirements of the treating physicians and nurses as well as of the patient and relatives may differ.
For example, patient and relatives want to be kept informed of ongoing diagnostic outcomes (e.g., lab values) as soon as possible.
However, physicians and nurses may want to discuss the findings with the patient in person to avoid causing unnecessary confusion and stress in the patient.
Therefore, the health information system must be able to provide detailed information to physicians and nurses, but it must be able to only present confirmed information to the patient (e.g., via a patient portal).

## 2.15 Example
For this example, we merge many of the small examples of Sect. 2.14 into one 3LGM^2 model showing a section of the information system of a fictional hospital.

Four subfunctions of patient admission (appointment scheduling, patient identification and checking for readmitted patients, administrative admission, and visitor and information services) are supported by the patient administration system, which is a part of the ERPS.
Medical admission and nursing admission are supported by the MDMS.
Obtaining consent for processing of patient-related data is supported by the non-computer-based application component for patient data privacy forms.
This application component is based on paper forms which are scanned by a clerk (see physical tool layer) and then stored in the MDMS.

The patient administration system, which is the master application system (Sect. 3.​9.​1) for the entity type “patient,” sends the administrative patient data as a message to the MDMS.
The MDMS can thus store this information about the entity type “patient” in its own database; administrative patient data that is needed to support medical admission and nursing admission as functions therefore do not have to be reentered in the MDMS.
The entity type “patient” is both stored in the database systems of the ERPS and the MDMS what is represented by dashed lines between the domain layer and the logical tool layer.

Both the patient administration system and the MDMS are run on servers at a virtualized server farm (see relationships between logical and physical tool layer). The application systems can be accessed by different end devices (patient terminal, PC, tablet PC).

It therefore simplifies some aspects which might be relevant in other contexts.
Another visualization of relationships between 3LGM^2 model elements is the matrix view.
The patient administration system supports three different functions, the MDMS supports two functions, and one function is supported by the paper-based patient data privacy form system.
The matrix view also helps to identify incomplete parts of models.
We can see that there are no functions modeled that are supported by the financial accounting system, the human resources management system, and the material management system, which are parts of the ERPS.

The matrix view is an alternative representation of configuration lines between functions at the domain layer and application components at the logical tool layer. Matrix views are also available for visualizing relations between other pairs of connected 3LGM^2 classes.

### 2.16.1 Data, Information, and Knowledge
Imagine that a physician is given the following information about his patient, Mr. Russo: “Diagnosis: hypertension.
Last blood pressure measurement: 160/100 mmHg.” Use this example to discuss the difference between “data,” “information,” and “knowledge”!

Answer:
“160,” “100,” “hypertension,” and “blood pressure” represent data that cannot be interpreted without knowledge about the context.
The information is that Mr. Russo has been diagnosed with hypertension and that his last blood pressure is 160/100 mmHg.
The medical knowledge embedded in this example is that a blood pressure of 160/100 mmHg indicates hypertension that should be treated.

### 2.16.2 Systems and Subsystems
Look up some information on the nervous system of the human body.
Then try to identify subsystems of the nervous system.
In the same way, can you also describe subsystems of the system “hospital”?

Answer:
The nervous system comprises two main categories of cells: neurons and glial cells.
Neurons communicate with each other via synapses and thus form their own subsystem.
Glial cells form another subsystem that provides support and nutrition to the neurons.

The hospital can be understood as a system comprising at least two subsystems: the subsystem where clinical care takes place and the subsystem where management takes place.
The clinical subsystem can again be split into several subsystems, such as inpatient area, outpatient area, and specialized diagnostic or therapeutic areas.
The inpatient area itself can be divided into various subsystems, each represented by one ward.
The way I define the subsystems of a hospital depends on the questions or intentions I have.

### 2.16.3 Information Logistics
Imagine a situation in which a physician speaks with Mr. Russo at the patient’s bedside.
The physician looks up Mr. Russo’s recent blood pressure measurement and ongoing medication, decides to increase the level of one medication, and explains this to Mr. Russo.
Use this example to discuss the meaning of “information and knowledge logistics.” What in this example indicates the right information, the right place, the right people, the right form, and the right decision? What could happen if an information system does not support high-quality information and knowledge logistics?

Answer:
The physician wants to have access to the right information (the most recent blood pressure) at the right time (when talking to Mr. Russo) at the right place (at the patient’s bedside) in the right form (hopefully the blood pressure is provided in an easy-to-grasp, visual way) so that he can make the right decision (here: to decide on the level of a certain medication).
If the information system does not support this, the physician may obtain an incorrect or outdated blood pressure measurement, or he may misinterpret it, thereby coming to a decision that is suboptimal for the patient.

### 2.16.4 3LGM^2 Metamodel
Look at the 3LGM^22 example in Sect. 2.15.
Use this example to explain the meaning of the following elements: functions, entity types, application systems, non-computer-based application components, physical data processing system, and inter-layer relationships.

Answer:
Administrative admission is an enterprise function that is supported by the patient administration system.
One entity type that is used and updated by this function is “patient.” The paper-based patient data privacy form system is an example of a non-computer-based application component.
The virtualized server farm is an example of a physical tool.
The inter-layer relationships of this example show which functions are supported by which application system and which physical data processing system the application systems are installed on.

### 2.16.5 Interpreting 3LGM^2 Models
Look at the 3LGM^2 sample model in Sect. 2.15 and try to answer the following questions.
(a) Find examples of specialization or decomposition at the domain layer.
(b) What is the meaning of the arrows pointing from patient identification to “patient” and from “patient” to medical admission ?
(c) What entity type that is stored in the paper-based patient data privacy form system should be added at the domain layer?
(d) Why is the function patient admission not connected with any application system?
(e) Which physical data processing systems are needed for the function “obtaining patient consent for the processing of data”?

Answer:
(a) The function “patient admission” is decomposed into five subfunctions—patient admission is only complete if all the subfunctions are completed. The entity type “patient” is decomposed into four entity types—data regarding that entity type are only complete if data about all sub-entity types is complete. There are no examples of specialization at the domain layer of Fig. 2.11.

(b) The function “patient identification” updates the entity type “patient.” The function “medical admission” uses the entity type “patient.” This indicates that identifying patient data are updated or created during patient admission and then used for medical admission.
 
(c) The entity type “privacy statement” could be added at the domain layer. It would be updated by the function “obtaining consent for processing of patient data.”
 
(d) Patient admission is decomposed into five subfunctions with each being linked to an application component by which it is supported. Therefore, it could lead to an ambiguous model if the superordinated function was linked with another application component. The corresponding modeling rule says that only the leaf functions in a function hierarchy should be linked to application components.
 
(e) The function “obtaining patient consent for the processing of data” is supported by the paper-based patient data privacy form system. For this, a paper record cabinet, a scanner, and a clerk handling these tools are the physical data processing systems needed for the function.

### 3.12.1 Domain Layer: Differences in Hospital Functions
Look at the functions presented in Sect. 3.3.2. Now imagine a small hospital (e.g., 350 beds) and a large university medical center (e.g., 1500 beds). What are the differences between these hospitals with regard to their functions? Explain your answer.

Answer:
A typical hospital needs all functions to function as expected.
The functions to be performed by health care professionals are mostly similar in all health care facilities, independent of their size.
Only some functions may differ.
For example, not all health care facilities are involved in clinical research, thus their information will not need to support the function research and education.

### 3.12.2 Domain Layer: Different Health care Professional Groups and Health care Facilities
Look at the functions listed in Sect. 3.3.2. Look at the relationships between the functions and the different health care professional groups (physicians, nurses, administrative staff, others) working in hospitals and medical offices.
Select one health care professional group and describe which functions are most important for this group.

Answer:
Physicians: Important functions are medical admission, decision-making and patient information, planning and organization of patient treatment, order entry, execution of diagnostic and therapeutic procedures, coding of diagnoses and procedures, and medical discharge and medical discharge summary writing.

Nurses: Important functions are nursing admission, decision-making and patient information, planning and organization of patient treatment, order entry, execution of nursing procedures, and nursing discharge and nursing discharge summary writing.

Administrative staff: Important functions are patient identification, administrative admission, and administrative discharge and billing.

### 3.12.3 Domain Layer: The Patient Entity Type
Look at the entity type “patient” that is interpreted and updated by various functions.
Which functions update the patient information, which functions interpret it?

Answer:
The entity type “patient” is updated by the function “patient admission.” All other functions that are related to patient care interpret it.

### 3.12.4 Logical Tool Layer: Communication Server
Imagine a hospital information system that comprises four application systems: a PAS, an MDMS, a RIS, and a PDMS.
The hospital is now considering the introduction of a communication server to improve data integration.
Discuss the short-term and long-term pros and cons of this decision.
Which syntactic and semantic standards could be used?

Answer:
Short-term advantages: The communication server can handle the communication between all four application systems, including receiving, buffering, transforming, and multicasting of messages.
It can also be used for monitoring the communication traffic.
The communication server thus supports data integration in heterogeneous information system architectures.

Long-term advantages: In the resulting (ACn, CP1) architecture, new application components can easily be integrated, as only one communication interface to the communication server needs to be implemented.

Standards: For the exchange of administrative data, HL7 V2 or V3 could be used as syntactic or semantic standard.
For the exchange of clinical data, various communication standards can be chosen such as HL7 FHIR, DICOM for medical images, or HL7 CDA for clinical documents.

### 3.12.5 Logical Tool Layer: Integration from the User’s Point of View
During a night shift, a nurse uses the patient administration system to conduct the administrative patient admission.
The nurse then uses the NMDS to plan nursing care.
Now consider the types of integration presented in Sect. 3.8 and discuss how this nurse would recognize a high (or low) level of data integration, semantic integration, user interface integration, context integration, feature integration, and process integration.

Answer:
Data integration would be considered high when the nurse documents patient administrative data only once in the patient administration system and then can use this data in the NMDS.

Semantic integration would be considered high when the nurse documents a nursing diagnosis using a standardized terminology (such as NANDA) and when this standardized diagnosis is then understood by the NMDS that may, for example, suggest a standard nursing care plan for this patient based on this diagnosis.

User interface integration would be considered high when the user interfaces of both application systems look sufficiently similar, which reduces the risk of data entry or data interpretation errors.
For example, in both application systems, the names of the patients are always displayed at the same place, the birthdates are presented in standardized form, and colors that are used to highlight important information are used in the same way.

Context integration would be considered high when the user context and the patient context is preserved when the nurse shifts from one application system to the other.
The nurse thus would not have to repeat user login or the selection of the patient in the second application system.

Feature integration would be considered high when only the patient administration system offers the needed administrative features (such as documentation of patient address). The nurse would be able to call up these features from within the NMDS.

Process integration would be considered high if both application systems work together in a highly integrated way so that the process of patient admission and nursing care planning from the point of view of the nurse is supported in an efficient way.

### 3.12.6 CityCare
The following questions can be answered by reading the text and analyzing the 3LGM^2 figures of the CityCare Example 3.11.
(a) The EHRS and the VNA in CityCare are not linked with any function they support. Which function of the domain layer may (partly) be supported by these application systems? Which functions (as introduced in Sect. 3.3) that are supported by these application systems could be added at the domain layer?
(b) In which database systems shown in the logical tool layer should the entity type “patient” be stored?
(c) The MPI should receive messages containing PINs (entity type “patient”) from all patient administration systems. Why is there no communication link between the MPI and the patient administration system of Ernst Jokl Hospital?
(d) According to the matrix view, which functions are supported redundantly in CityCare? Discuss pros and cons of the functional redundancies in this scenario. What redundancies would you resolve and how?
(e) Which functions in which health care facility cannot be performed anymore if “Application Server 1 Ernst Jokl Hospital” fails? Suggest a change to the physical tool layer that would minimize the risk of missing function support in case a single application server fails.
(f) For the CityCare network, would it make sense to implement further profiles from IHE? Explain your decision.

Answer:
(a) EHR systems as comprehensive application systems combine the functionalities of MDMS, NDMS, and CPOE systems. The EHRS of CityCare could therefore be used for medical admission, preparation of an order, or execution of diagnostic and therapeutic procedures. However, each of the three health care facilities in CityCare has its own MDMS. Therefore, the EHRS is probably mainly used for accessing findings from the other health care facilities, for example, during medical admission. For the VNA, no suitable function is modeled at the domain layer. At the domain layer, archiving of patient information could be added which is supported by the VNA and, to some extent, also by the EHRS.
(b) The entity type “patient” represents the persons who are the subject of health care. Information about a patient includes the PIN and other administrative data about the person. Each of the application systems supporting subfunctions of patient care and having an own database system stores the entity type “patient,” for example, the patient administration system including the MPI, the MDMS, the EHRS, and the VNA.
(c) In Ernst Jokl Hospital, there is a star architecture at the logical tool layer, i.e., a communication server is used for the exchange of messages between application systems. The patient administration system of Ernst Jokl Hospital, where the PINs of Ernst Jokl Hospital are generated, sends this information in a message to the communication server. The communication server forwards the message to the MPI of the health care network. In the central MPI of the tHIS, the local patient identification numbers of the different health care facilities are linked to the unique transinstitutional patient identification number of CityCare.
(d) Administrative admission, appointment scheduling, medical admission, order entry, patient identification, and preparation of an order are each supported by at least three application systems in the scenario.
Pros (examples):
- Each of the health care facilities has a functioning information system that is independent from changes or system failures in the other health care facilities.
- The different patient administration systems and medical documentation and management systems may be better adapted to the local needs and grown structures in the single health care facilities than an application system that is used by all of them together.

Cons (examples):
- Three or more different application systems that support the same function cause higher costs and higher administrative effort.
- The effort for establishing integration and interoperability are higher in functional redundant architectures which have a high number of single application systems.

Resolving these redundancies (examples):
- One patient administration system that supports patient identification and administrative admission could be used in all health care facilities instead of three patient administration system and an MPI.
- The central EHRS could be used as MDMS, NDMS as well as CPOE system in each of the facilities and would replace the existing local application systems.

(e) According to the matrix view in Fig. 3.​37, the MDMS of Ploetzberg Hospital is installed on application server 1 Ernst Jokl Hospital. Thus, if this application server 1 Ernst Jokl Hospital fails, the following functions cannot no longer be performed: appointment scheduling, medical admission, order entry, and preparation of an order (see matrix view in Fig. 3.​35).

The application systems used in CityCare should be made available by server clusters with redundant servers. If one server in a server cluster fails, another server can take over its task. Thus, there is no interruption in function support.
 
(f) Yes, it makes sense to use further integration profiles from IHE. For example, IHE XDS could be used. The CityCare network could be established as an affinity domain with several actors that interact in a standardized way (process interoperability) to share document-level or even large binary patient data, such as findings, images, or radiology reports. These documents would be registered centrally in a document registry and could be retrieved by other systems. Depending on how the central EHRS is implemented, it could either take the role of a document registry that forwards the requests to a decentral source, or it could—as in our case of a central database—act as a central document provider itself.

### 4.9.1 Activities of Managing Information Systems
In Sect. 4.2, we introduced a three-dimensional classification of activities of management of information systems.
How would you describe the scope and tasks of the following activities of managing information systems?
- Developing a strategic information management plan (e.g., this is related to strategic planning),
- Initiating projects from the strategic project portfolio,
- Collection and analysis of data from user surveys on their general satisfaction with the health information system,
- Planning a project to select and introduce a new CPOE system,
- Executing work packages within an evaluation project of a CPOE system,
- Assessment of user satisfaction with a new intensive care system,
- Planning of a user service desk for a group of clinical application components,
- Operation of a service desk for a group of clinical application components,
- Daily monitoring of network availability and network failures.

Answer:
- Developing a strategic information management plan: strategic planning.
- Initiating projects from the strategic project portfolio: strategic directing.
- Collecting and analyzing data from user surveys on their general health information system’s satisfaction: strategic monitoring.
- Planning a project to select and introduce a new CPOE system: tactical planning.
- Executing work packages within an evaluation project of a CPOE system: tactical directing.
- Assessment of user satisfaction with a new intensive care system: tactical monitoring.
- Planning of a user service desk for a group of clinical application components: operational planning.
- Operation of a service desk for a group of clinical application components: operational directing.
- Daily monitoring of network availability and network failures: operational monitoring.

### 4.9.2 Strategic Alignment of Hospital Goals and Information Management Goals
Imagine you are the CIO of a hospital in which almost no computer-based tools are used.
One of the hospital’s goals is to support health care professionals in their daily tasks by offering up-to-date patient information at their workplace.

Which main goals for management of information systems could you define based on this information? Which functions should be prioritized to be supported by new application systems? What could a strategic project portfolio and a migration plan for the next 5 years look like?

Answer:
Goals: efficient and high-quality information logistics to support patient care.

Functions: patient administration and all functions related to patient care (Sect. 3.​3.​2.​1).
Project portfolio and migration plan:
- Year 1: Introduction of a patient administration system.
- Year 2: Introduction of a CIS, an LIS and an RIS.
- Year 3: Introduction of a DAS and a PACS.
- Year 4: Introduction of an OMS and of a PDMS.
- Year 5: Introduction of a DWS and of a patient portal.

Please note: This is a simplified solution. Other solutions may be valid, too. In case the different application systems are meant to come from different vendors, an integration technology such as a communication server needs to be implemented.

### 4.9.3 Structure of a Strategic Information Management Plan
In Sect. 4.8.1, we presented the structure of the strategic information management plan of Ploetzberg Hospital.
Compare its structure to the general structure presented in Sect. 4.3.1.2, consisting of strategic goals, description of current state, assessment of current state, future state, and migration path.
Where can you find this general structure in Ploetzberg Hospital’s plan?

Answer:
- Strategic goals of the health care facility (business goals) and of management of information systems: are visible in Chaps. 1 and 2 of Ploetzberg Hospital’s plan.
- Description of the current state of the information system: are visible in Chap. 3 of Ploetzberg Hospital’s plan.
- Assessment of the current state of the information system: are visible in Chap. 4 of Ploetzberg Hospital’s plan.
- Future state of the information system: are visible in Chap. 5 of Ploetzberg Hospital’s plan.
- Migration path from the current to the planned state: are visible in Chap. 6 of Ploetzberg Hospital’s plan.

### 4.9.4 An Information-Processing Monitoring Report
Look at the health information system’s KPIs of Ploetzberg Hospital in Example 4.8.2. Try to figure out some of these numbers for a real hospital and compare both hospitals’ KPIs in the form of a benchmarking report.
It may help to look at the strategic information management plan of this hospital or at its website.

Answer:
- KPI | Ploetzberg Hospital | My hospital
- Number of HIS staff | 46 | 89
- Number of HIS users | 4800 | 9000
- Number of workstations | 1350 | 6200
- Number of mobile IT tools | 2500 | 2000
- HIS user per mobile IT tool | 1.9 | 4.5
- Number of IT problem tickets | 15,500 | 36,250
- Percentage of solved IT problem tickets | 96% | 92%
- Availability of the overall HIS systems | 98.5% | 96%
- Number of finalized strategic IT projects | 13 | 10
- Percentage of successful IT projects | 76% | 86%

### 4.9.5 Relevant Key Performance Indicators (KPIs)
Imagine you are the CIO and have to select the three most relevant indicators for the quality of your information system at your hospital: Which would you select? You can look at the examples in Sect. 4.8.2 to get ideas.
Explain your choice.

Answer:
Several solutions are possible here. One possible solution:
1. HIS user per mobile IT tool: Efficient information logistics everywhere (e.g., at the patient’s bedside) requires enough mobile IT tools.
2. Number of application systems: I would strive for an integrated information system and reduce the number of application systems in the long run in order to reduce integration problems.
3. HIS budget in relation to the overall hospital budget: Sufficient funding is the precondition for high-quality and well-integrated information system and the necessary competent IT staff.

### 4.9.6 Organizing User Feedback
You are asked to organize regular (e.g., every half year) quantitative user feedback on the general user satisfaction with major clinical application components of your hospital as part of health information system’s monitoring.
Which user groups would you consider? How could you gather user feedback regularly in an automatic way? Explain your choice.

Answer:
User groups: physicians, nurses, technical staff (e.g., lab, radiology), and management staff—these groups are typically large health information systems user groups. I would also organize regular survey of CIS key users, as they are experts in judging the quality of the information systems.

Organization of user feedback: (1) Health information system users are randomly invited to an automatic short and standardized survey that is displayed during CIS login.
(2) Every half year, I would organize sounding boards (a structured approach to obtain active feedback from stakeholders) with key users and with representatives from the larger user groups to discuss recent challenges with the CIS and opportunities for improvements.

### 4.9.7 Information Systems Managers as Architects
Information systems managers can be partly compared to architects.
Read the following statement and discuss similarities and differences between information system architects and building architects [8]:

“We are architects.
[…] We have designed numerous buildings, used by many people.
[…] We know what users want.
We know their complaints: buildings that get in the way of the things they want to do.
[…] We also know the users’ joy of relaxing, working, learning, buying, manufacturing, and worshipping in buildings which were designed with love and care as well as function in mind.
[…] We are committed to the belief that buildings can help people to do their jobs or may impede them and that good buildings bring joy as well as efficiency.”

Answer:
Health information managers can indeed be compared with architects.
Health information managers design information systems that are used by many different user groups.
Health information managers regularly monitor the quality of information systems to obtain feedback and to improve the information system.
Health information managers understand that information systems support many different functions for many different user groups within health care facilities.
Health information managers make sure that the application systems are user-friendly and support working processes in an efficient way.
Health information managers understand that an information system serves the overall goal of a health care facility and ultimately serves the need of the patients.

### 5.6.1 Quality of Integration
Read the following case descriptions and discuss the integration problems using the types of integration presented in Sect. 5.3.4. Which negative effects for information logistics result from the identified integration problems?
1. A physician enters a medical diagnosis for a patient first in the medical documentation and management system (MDMS) and later, when ordering an X-ray, again in the CPOE system.
2. The position of the patient’s name and the formatting of the patient’s birthdate vary between the MDMS and the CPOE system.
3. When physicians shift from the MDMS to the CPOE system, they have to log in again and again search for the correct patient.
4. The CPOE system and the RIS use slightly different catalogs of available radiology examinations.
5. When physicians write the discharge letter for a patient in the MDMS, they also have to code the discharge diagnosis of a patient. For this coding, they have to use a feature that is only available in the patient administration system, so they have to shift to this application system.
6. While at the patient’s bedside during their ward rounds, physicians have to use several application components at the same time, such as MDMS for retrieving recent findings, the CPOE system for ordering, and the PACS for retrieving images.
     
Answer:
1. A physician enters a medical diagnosis for a patient first in the MDMS and later, when ordering an X-ray, again in the CPOE system. → No data integration, resulting in reentering of data, which is time-consuming and may lead to errors and inconsistencies in the data, which has the potential for patient harm.
 
2. The position of the patient’s name and the formatting of the patient’s birthdate vary between the MDMS and the CPOE system. → No user interface integration, resulting in increased time effort when using various application components, increased time needed for user training, and increased risk in overlooking or misinterpreting important patient information, which has the potential for patient harm.
 
3. When physicians shift from the MDMS to the CPOE system, they have to log in again and again search for the correct patient. → No context integration, leading to an increase in time needed to shift between application systems and an increased risk for selecting the wrong patient in the second application systems, which has the potential for patient harm.
 
4. The CPOE system and the RIS use slightly different catalogs of available radiology examinations. → No semantic integration, making the exchange and reuse of patient information in both application systems challenging.
 
5. When physicians write the discharge letter for a patient in the MDMS, they also have to code the discharge diagnosis of a patient. For this coding, they have to use a feature that is only available in the patient administration system, so they have to shift to this application system. → No feature integration, leading to increased time needed to shift to the patient administration system.
 
6. While being at the patient’s bedside during their ward rounds, physicians have to use several application components at the same time, such as MDMS for retrieving recent findings, the CPOE system for ordering, and the PACS for retrieving images. → No process integration; a process should be organized in a way that frequent change of application systems is avoided if possible.

### 5.6.2 Data Collection in Evaluation Studies
Read Examples 5.5.1 and 5.5.2 and determine which methods for collecting data (as described in Sects. 5.4.3 and 5.4.4) have been used.

Answer:
Study “Unintended Effects of a Computerized Physician Order Entry Nearly Hard-stop Alert”: The effectiveness of a nearly “hard-stop” alert was evaluated in a field study.
The data was collected via analysis of the prescriptions in the CPOE systems.
The overall data collection method is thus a quantitative observation of available data.

Study “Clinical Decision Support for Worker Health: A Five-Site Qualitative Needs Assessment in Primary Care Setting”: data were collected via interviews and qualitative observations.

### 5.6.3 Study Design in Evaluation Studies
Read Examples 5.5.1 and 5.5.2 and describe the chosen study design in more detail, using the description presented in Sect. 5.4.2.

Try to explain for which types of study questions the RCT is the best study design.

Answer:
Study “Unintended Effects of a Computerized Physician Order Entry Nearly Hard-Stop Alert”: This quantitative and explanatory field study was organized as an RCT: 1981 clinicians were randomly assigned to either the intervention group or the control group.
RCTs are considered the gold standard, as they provide a rigorous tool to assess cause–effect relationships between intervention and outcome.

Study “Clinical Decision Support for Worker Health: A Five-Site Qualitative Needs Assessment in Primary Care Setting”: This is a qualitative, explorative field study.

## 6.11 Example
To support medical research and care, the German Medical Informatics Initiative (MI-I) was launched.
Four consortia of university medical centers are establishing the so-called data integration centers (DICs) for the individual hospitals.
These DICs are facilities that extract data from the electronic patient records of the respective hospitals to make them available for research projects.
Note that in each hospital, the data from the electronic patient records is scattered around the various application systems of this hospital.
The consortium SMITH (Smart Medical Information Technology for Health care) decided to apply IHE to share data between the hospitals and the DICs as well as between the DICs of the different hospitals.
For details, see [4].
The dotted lines indicate that there are still refinements to the corresponding tasks and entity types.
Patient data (“EMR Data in UH Sources”) is taken from the electronic patient records of hospitals (“University Hospital (UH)”) and inserted into a separate storage area.
There, the data are prepared and, in particular, semantically “nourished,” i.e., enriched.
Also, certain rules and methods for processing the data are managed in this “Health Data Storage.” When the patients to whom these data belong have given their consent, the data are pseudonymized by a trustee unit and made available to research projects by the “Transfer Management.”

At each DIC’s site, application systems are needed to support the local DIC, i.e., supporting the execution of functions as well as storing and communicating the entity types.
Data and knowledge sharing between sites and between patient care and research projects (Research & Development Factory) have to be enabled.
Communication is standards-based, especially using IHE profiles, CDA, FHIR, and SNOMED to ensure syntactic, semantic, and process interoperability.
The architecture of the local information system and their communication links at each site follows the DIC reference architecture as outlined in the 3LGM^2 model. Using IHE profiles, the local sub-information systems of the entire tHIS of the SMITH network (SMItHIS) are integrated.
While applying the DIC reference architecture locally, the reference architecture allows for local peculiarities.

As mentioned before, the DICs have to ingest data from various data sources, i.e., different application systems of the local hospital information systems.
Communication between application systems is classified into three categories, A, B, and C, according to their interface type (“if-type”). Sources of Type A are designed using IHE profiles.
There are application systems that can serve HL7 and DICOM standards but do not fully implement IHE profile.
They are referred to here as Type B sources.
Type C sources are proprietary, such as data provided by comma-separated value (CSV) files.

The “Data Integration Engine” executes data transformation and load processes from sources into the health data storage (HDS). The HDS contains both a component for storing HL7 FHIR resources (Health Data Repository) and an IHE XDS document repository comprising clinical data in HL7 CDA documents.
Using the interface-type scheme (A, B, and C), data are shared beyond department borders.
Precise explanations of other details can be found in [4].

### 6.12.1 Research Architecture
A clinical researcher at Ploetzberg Hospital has won a grant to set up a register for patients who have received a knee endoprosthesis.
Disease registers are research databases for collecting data about a specific disease, aiming for full coverage of the respective patient collective.
The aim of a knee endoprosthesis registry is to collect longitudinal data to find out which type of endoprosthesis works best over time.
The researcher wants to integrate data from patient-reported outcome questionnaires, findings from inpatient or outpatient visits at the hospital, and results from laboratory examinations.
Which entity types need to be integrated and from which application components do they come? Devise a plan how you would set up a sustainable research architecture, i.e., an architecture that also could be used in other research settings and for different disease or research entities, considering Sect. 6.6.

Answer:
The following entity types have to be integrated: patient, person, diagnosis, finding, health record, medical procedure, patient record, self-gathered symptoms, material, medical device, classification, nomenclature.

Application components to be integrated depend on local settings and implementation but will likely include: patient administration system, MDMS, LIS, OMS, PDMS, and self-diagnosis systems (e.g., an app for collecting patient-reported outcome data) or patient portals.

A research architecture for setting up multiple registries might include a DWS for research that is fed via ETL processes from the above-mentioned application components and can be tapped for data in different use cases or research scenarios.
Finally, an open platform architecture would enable reuse of patient data in various research contexts.

### 6.12.2 Medical Admission
In which of the health care settings above will the function medical admission need to be supported?

Answer:
The function “medical admission” is relevant in several health care and research settings.
It comprises the provision of forms for documenting medical history, documenting diagnoses, and scanning documents from referring physician and other sources of information about the medical history.
It is obvious that this function needs to be supported in hospitals, nursing homes, ambulatory nursing organizations, and medical offices.
Yet it is often also necessary in research settings, for example, when a person is recruited for a clinical trial and their data are entered into an EDC system.
Furthermore, therapeutic offices need this function for documentation purposes, as do rehabilitation facilities and—to a limited extent—wellness or sports facilities.
For personal environments, medical admission also plays a role, especially in telecare situations or when prevention measures are conducted, respectively.