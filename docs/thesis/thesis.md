# Routers for LLM: A Framework for Model Selection and Tool Invocation

## Abstract

In the current landscape of large language models, users are confronted with a plethora of models and tools each offering a unique blend of specialisation and generality. This project proposes the development of a dynamic middleware “router” designed to automatically assign user queries to the most appropriate model or tool within a multi-agent system. By using zero-shot Natural Language Inference models, the router will evaluate incoming prompts against criteria such as task specificity and computational efficiency, and *route* the prompt to the most effective model and / or allow specific tools relevant that the model could use.

The proposed framework is underpinned by three core routing mechanisms. 

- Firstly, it will direct queries to cost effective yet sufficiently capable models, a concept that builds on existing work in semantic routing [e.g Giacomo, 2023; ArXiv:2406.18665v1].

- Secondly, it incorporates a tool routing system that automatic invocation of specialised functions, thus streamlining user interaction and reducing inefficiencies currently inherent in systems like OpenAI’s and Open Web UI. Furthermore this could also reduce inefficiencies in the recent reasoning models addressing the observed dichotomy between underthinking with complex prompts and overthinking with simpler queries when reasoning is manually toggled which can be costly and could cause hallucination.

- Thirdly, while the primary focus remains on model and tool routing, this work will preliminarily explore the potential application of the routing architecture as a security mechanism. Initial investigations will examine the theoretical feasibility of leveraging the router's natural language understanding capabilities to identify adversarial prompts. This includes a preliminary assessment of detection capabilities for prompt engineering attempts, potential jailbreaking patterns, and anomalous tool usage requests. However, given the rapidly evolving nature of LLM security threats and the complexity of implementing robust safeguards, comprehensive security features remain outside the core scope of this research. This aspect represents a promising direction for future work, particularly as the field of LLM security continues to mature.

By integrating these mechanisms, the research aims to pioneer a more efficient, modular, and secure distributed AI architecture. This architecture not only optimises resource allocation but also reinforces system integrity against emerging adversarial threats, thereby contributing novel insights into the development of next-generation LLM deployment strategies.

## Chapter 1: Introduction
In the past few years the landscape of large language models has expanded dramatically, with many domain specific as well as general-purpose agents emerging across domains such as healthcare (like Med-PaLM 2 and BioGPT), coding (like CodeLlama and GitHub Copilot), and research (like Claude Opus and GPT-4o). Organisations that provide inference as a service now face complex trade-offs between cost, latency, and capability: for example, GPT-4.5 can cost up to $75 per million tokens compared with just $0.15 for gemini-2.5-flash [https://sanand0.github.io/llmpricing/] [][https://artificialanalysis.ai/] . Although these models could be vastly different in terms of capability, the problem organisations face is determining *when* to deploy premium models versus more cost-effective alternatives for a given task / prompt. This suggests a need for intelligent routing systems that can analyse incoming prompts and direct them to the most appropriate model based on task complexity, required capabilities, and cost considerations. 

Inspired by lower level (transformer-embedded) "router" such as the one emploued by mistral for thier mixtral (MoE) model the goal of this was to allow for a more distributed, higher level prompt based routing between a verity of models with varing levels of cost and complexity. 

### 1.2 Problem Statement
The proliferation of large language models has created a complex ecosystem where selecting the optimal model for a given task has become increasingly challenging. 

Organisations and users face several key problems:

1. **Cost-Efficiency Trade-offs**: High-capability models like GPT-4o and Claude 3 Opus provide powerful capabilities but at significantly higher costs than simpler models. Without intelligent routing, organisations and users may unnecessarily infer to expensive models for tasks that could be adequately handled by more cost-effective alternatives.
    
2. **Selection Complexity**: With the dawn of function calling and Multi-modal Context Processing (MCP), most chat systems offer numerous specialised tools and functions, but determining which tools are appropriate for a given query often requires manual specification by users or developers. While this might seem like a minor inconvenience for users interacting through visual interfaces (web, mobile apps), it creates significant limitations for systems accessed through voice interfaces or complex automated pipelines such as interacting via email. Current implementations typically rely on toggle switches within the user interface that many users forget to activate before submitting their queries. This oversight leads to situations where tools aren't utilised when they should be, resulting in responses that are hallucinated by the LLM rather than grounded in factual data. While this may be acceptable for general knowledge questions, it becomes problematic for mathematical calculations, queries about latest news or weather conditions, or specialised information such as device status checks (e.g., whether a smart bulb is on or off). The disconnect between available tools and their appropriate activation represents a significant usability challenge that an intelligent router could potentially resolve.

3. **Computational Resource Allocation**: Indiscriminate routing of all queries to high-performance models can lead to inefficient resource allocation, increased latency, and higher operational costs for LLM providers and users.
    
### 1.3 Research Objectives
The premise of this research is to investigate whether pre-existing Natural Language Inference models such as Facebook's bart-large-mnli could be used as drop-in replacements to perform automated model selection and tool selection. Furthermore, we will examine the effectiveness of fine-tuning existing NLI models with specialised datasets designed for routing tasks.

The specific research objectives include:
- Creating a LLM Router library that can be deploy to existing systems with ease.
- Experimenting with Pretrained NLI models such as bart-large-mnli  for both tool routing and model selection.
- evaluating and Assessing the accuracy the effectiveness using a set of prompts.
- Incorporate it with an existing Chatbot UI platform such as OpenWebUI.

## Chapter 2: Literature Review

### 2.1 Large Language Models: Current Landscape

### 2.2 Multi-Agent Systems and Distributed AI Architecture

### 2.3 Semantic Routing Mechanisms

### 2.4 Tool Integration with LLMs

### 2.6 Current Approaches to LLM Routing

#### 2.6.1 Rule-Based Approaches

#### 2.6.2 Text Classifier NLI)-Based Approaches

#### 2.6.3 LLM-Based Routing Systems

### 2.7 Research Gap Analysis

## Chapter 3: Theoretical Framework

### 3.1 Conceptual Model of Middleware Routing

### 3.2 Natural Language Inference for Query Evaluation

### 3.3 Resource Allocation Optimization Theory

### 3.4 Tool Selection Paradigms

### 3.5 Security-First Design Principles

## Chapter 4: Methodology

### 4.1 Research Design

### 4.2 System Architecture

### 4.3 Development of Router Components

#### 4.3.1 Model Router Development

#### 4.3.2 Tool Invocation Router Development

#### 4.3.3 Security Guardrail Router Development

### 4.4 Data Collection and Generation

#### 4.4.1 Training Dataset Creation

#### 4.4.2 Synthetic Data Generation Process

### 4.5 Evaluation Framework

#### 4.5.1 Efficiency Metrics

#### 4.5.2 Accuracy Metrics

#### 4.5.3 Security Metrics

### 4.6 Experimental Setup

## Chapter 5: Model Router Implementation

### 5.1 Cost-Effectiveness Quantification

### 5.2 Domain Specificity Detection

### 5.3 Decision-Making Algorithms

### 5.4 Performance Analysis

### 5.5 Integration with Overall System

## Chapter 6: Tool Invocation Router Implementation

### 6.1 Tool Capability Mapping

### 6.2 Query Intent Classification

### 6.3 Automatic Tool Selection Algorithms

### 6.4 Tool Execution and Response Integration

### 6.5 Case Studies of Tool Router Efficiency

## Chapter 7: Security Guardrail Router Implementation

### 7.1 Threat Detection Mechanisms

### 7.2 Attack Pattern Recognition

### 7.3 Mitigation Strategies

### 7.4 Security Testing Results

### 7.5 Balance of Security and Usability

## Chapter 8: System Integration and Testing

### 8.1 Integration of Router Components

### 8.2 End-to-End System Architecture

### 8.3 Standardized Interfaces

### 8.4 Library Development for Chat Interfaces

### 8.5 Comprehensive System Testing

### 8.6 Benchmark Comparisons with Existing Solutions

## Chapter 9: Results and Analysis

### 9.1 Efficiency Improvements

### 9.2 Accuracy and Appropriateness of Routing Decisions

### 9.3 Security Enhancement Outcomes

### 9.4 Cost-Benefit Analysis

### 9.5 Limitations of the Current Implementation

## Chapter 10: Discussion

### 10.1 Implications for Multi-Agent LLM Systems

### 10.2 Scalability Considerations

### 10.3 Ethics and Privacy Considerations

### 10.4 Comparison with Related Work

### 10.5 Theoretical Contributions

### 10.6 Practical Applications


## Chapter 11: Conclusion

### 11.1 Summary of Findings

### 11.2 Research Contributions

### 11.3 Final Reflections

## References

## Appendices

### Appendix A: Technical Documentation

### Appendix B: Router Specifications

### Appendix C: Training Data Samples

### Appendix D: Test Suite Details

### Appendix E: Implementation Code