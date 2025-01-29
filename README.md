# **AgentEx** ![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg) ![License](https://img.shields.io/badge/License-GPLv3-blue.svg)

**AgentEx** is an autonomous multi-agent, multi-swarm framework designed to showcase how agents and swarms of agents can coordinate, communicate, and complete tasks in an asynchronous, event-driven environment.

AgentEx has the potential to power a wide range of AI systems and workflows. Community support and feedback are essential as we continue to refine and expand this framework!

Our latest milestone includes **dynamic task management, RabbitMQ messaging for distributed communication**, and a flexible system for **registering and executing custom tasks.** This paves the way for scalable, distributed AI workflows.

---

## **Table of Contents**
- [Key Features](#key-features)
- [What’s New](#whats-new)
- [Project Vision](#project-vision)
- [Getting Started](#getting-started)
- [Example Flow](#example-flow)
- [Contributing](#contributing)
- [License](#license)
- [Contact and Future Discussion](#contact-and-future-discussion)

---

## **Key Features**

### **Multi-Agent Swarms**
- **Swarm Composition:** Each **Swarm** can contain multiple **Agents**, grouped by roles or capabilities (e.g., `analytics`, `task_runners`).
- **Automatic Registration:** Agents register dynamically within a swarm.

### **Dynamic Task Management**
- **Dynamic Task Registration:** Developers can register custom task types at runtime without modifying the core system.
- **Flexible Execution:** Tasks can be defined using the provided base task class and executed asynchronously.
- **Retries and Failures:** Built-in handling for retries and failure scenarios.

### **RabbitMQ-Driven Communication**
- **Distributed Messaging:** RabbitMQ powers agent-to-agent and swarm-to-swarm communication.
- **Cross-Swarm Messaging:** Send messages across swarms or to groups of agents within the same swarm.
- **Asynchronous Messaging:** Agents communicate without blocking task execution.

### **Capability-Based Task Assignment**
- **Dynamic Capabilities:** Agents advertise their capabilities, and the task manager assigns tasks accordingly.
- **Automatic Routing:** No need for hardcoded assignments—tasks are routed based on advertised roles.

### **Scalable Backend System**
- **Local Backend:** For single-machine communication.
- **RabbitMQ Backend:** For distributed environments, using AMQP for scalability.

---

## **What’s New**

### **Core Improvements:**
- **Dynamic Task Registration:** Tasks can now be defined and registered without modifying core code, making the system more extensible.
- **Capability-Based Task Assignment:** Tasks are automatically routed to agents with matching capabilities.
- **RabbitMQ Integration:** Agents communicate efficiently using RabbitMQ, making AgentEx ready for distributed, scalable deployments.
- **Modular Backend Support:** Easily switch between local and distributed backends without changing application logic.

---

## **Project Vision**

### **Long-Term Goals:**
- **LLM Integration:** Future updates will support retrieval-augmented generation (RAG) to allow agents to query external knowledge bases for task completion.
- **Self-Optimizing Agents:** Agents will learn from successes and failures, improving task execution strategies over time.
- **Expanded Protocol Support:** Add support for protocols beyond RabbitMQ, such as Kafka or Redis Streams.

---

## **Getting Started**

### **Clone the Repository**
```bash
git clone https://github.com/onedavidwilliams/AgentEx.git
cd AgentEx
```

### **Set Up a Virtual Environment (Recommended)**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### **Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Run the Example**
```bash
python src/agentex/tests/mq_test.py
```
This will demonstrate how tasks are registered, assigned, and executed using the dynamic task manager.

---

## **Example Flow**
- **Swarm:** Contains agents `Agent1`, `Agent2`, and `Agent3`.
- **Task Assignment:** Tasks are registered dynamically and assigned to agents based on their capabilities.
- **Example Task:** Reading and processing data from `sample.txt` using the `CustomDataTask`.
- **Cross-Swarm Communication:** Agents send messages or task requests across swarms as needed.

Logs will show how tasks are queued, executed, and completed, including retry handling if applicable.

---

## **Contributing**

We welcome contributions, bug fixes, and feature enhancements! To contribute:

1. **Fork the Repository**
2. **Create a Feature Branch**
    ```bash
    git checkout -b feature/YourFeature
    ```
3. **Commit Your Changes**
    ```bash
    git commit -m "Add some feature"
    ```
4. **Push to the Branch**
    ```bash
    git push origin feature/YourFeature
    ```

### **Open a Pull Request**

---

## **License**
This project is licensed under the [GNU General Public License v3.0](LICENSE).

---

## **Contact and Future Discussion**
If you have ideas for expanding AgentEx or want to contribute to future milestones, please open an issue or pull request. We’re excited to collaborate with the community to build something amazing!
