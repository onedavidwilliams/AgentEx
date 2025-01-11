# AgentEx ![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg) ![License](https://img.shields.io/badge/License-GPLv3-blue.svg)


**AgentEx** is an autonomous multi-agent, multi-swarm framework designed to showcase how agents and swarms of agents can coordinate, communicate, and complete tasks in an asynchronous, event-driven environment.

AgentEx has the potential to power a wide range of AI systems and workflows. Community support and feedback are essential as we continue to refine and expand this framework!

We’re starting with **Retrieval-Augmented Generation (RAG)** integrations, making AgentEx seamlessly compatible with large language models and vector databases—empowering agents to retrieve and leverage external knowledge for complex tasks. But **RAG** is just the beginning! Our long-term vision is for AgentEx to become a flexible, ever-growing platform capable of supporting advanced workflows in AI, research, automation, and beyond.


## Table of Contents

- [Key Features](#key-features)
  - [Multi-Agent Swarms](#multi-agent-swarms)
  - [Async Task Execution](#async-task-execution)
  - [Communication Model](#communication-model)
  - [Sender and Recipient Metadata](#sender-and-recipient-metadata)
  - [Flexible Group Management](#flexible-group-management)
  - [Swarm Autonomy](#swarm-autonomy)
  - [Integration-Ready](#integration-ready)
- [Project Vision](#project-vision)
  - [RAG Integration](#rag-integration)
  - [Autonomous Learning](#autonomous-learning)
  - [Expanded Communication Protocols](#expanded-communication-protocols)
  - [Domain-Specific Skins](#domain-specific-skins)
  - [Enhanced Task Workflow](#enhanced-task-workflow)
- [Getting Started](#getting-started)
  - [Clone the Repository](#clone-the-repository)
  - [Set Up a Virtual Environment (Recommended)](#set-up-a-virtual-environment-recommended)
  - [Install Dependencies](#install-dependencies)
  - [Run the Example](#run-the-example)
- [Example Flow](#example-flow)
- [Contributing](#contributing)
  - [Potential Areas for Contribution](#potential-areas-for-contribution)
- [License](#license)
- [Contact and Future Discussion](#contact-and-future-discussion)

## Key Features

### Multi-Agent Swarms
- **Swarm Composition:** Each **Swarm** can contain multiple **Agents**, potentially grouped by roles or specialties (e.g., `analytics`, `main`, etc.).
- **Automatic Registration:** Agents register themselves automatically in the swarm’s group dictionary.

### Async Task Execution
- **Task Types:** Tasks can be either synchronous or asynchronous (`AsyncAgentTask`).
- **Concurrent Processing:** Each Agent runs tasks concurrently via `asyncio`, ensuring the system handles multiple ongoing processes gracefully.

### Communication Model
- **Cross-Swarm Messaging:** Agents or entire swarms can send messages to agents or groups in other swarms using a central hub (`CentralHub`).
- **Intra-Swarm Messaging:** Agents in the same swarm broadcast or target specific groups/agents.
- **Broadcast Fallback:** If a specified group doesn’t exist, the system can default to broadcasting messages to the entire swarm.

### Sender and Recipient Metadata
- **Detailed Information:** Agents see details like:
  - **`from_groups`:** The group(s) of the sender (if the sender is also an Agent).
  - **`to_group`:** Whether the message was intended for a specific group, a single agent, or broadcast to all.

### Flexible Group Management
- **Agent-Defined Groups:** Agents define their own group memberships.
- **Automatic Routing:** Swarms automatically note which groups an agent belongs to and can route messages accordingly.

### Swarm Autonomy
- **Internal Task Queue:** Each swarm has an internal queue of tasks.
- **Automatic Distribution:** Agents become “available” upon completing a task, and the swarm distributes queued tasks automatically.

### Integration-Ready
- **LLM Integration:** The code is structured to plug in retrieval or summarization steps from LLMs to help Agents make “intelligent” decisions about tasks and data.
- **Scalable Extensions:** A stepping stone to more advanced or domain-specific expansions (e.g., financial analysis, e-commerce, data engineering, etc.).

## Project Vision

### RAG Integration

AgentEx aims to incorporate advanced **LLM-driven retrieval**. Future capabilities include:

- **Semantic Searching:** Agents query a vector store for relevant text chunks or knowledge graphs.
- **Self-Healing Agents:** If an agent encounters missing data, it can retrieve or generate the missing pieces through a knowledge API.
- **LLM-Assisted Task Analysis:** Agents use an LLM to interpret tasks, break them down, and spawn subtasks or sub-agents automatically.

### Autonomous Learning

- **Adaptive Agents:** Over time, Agents can refine their strategies based on logs, successes, or errors.
- **Self-Updating:** The swarm or an “architect agent” might retrain or finetune certain models based on new data or tasks.

### Expanded Communication Protocols

- **From-Group Identification:** Swarms themselves can have “swarm groups” (like an internal special role) to further contextualize messages.
- **Federated Swarms:** Multiple hubs in a distributed network exchanging tasks or knowledge.

### Domain-Specific Skins

- **Financial Swarms:** For automated stock analysis & trading, hooking into real-time data.
- **Enterprise Data Processing:** Agents that unify logs, monitor data ingestion, run analytics pipelines, and share results.
- **Creative Content Generation:** Agents that co-write stories, design images, or produce marketing copy in synergy.

### Enhanced Task Workflow

- **Chained Tasks:** Each result feeding into the next step or next agent automatically.
- **Dynamic Task Prioritization:** Agents negotiate who takes which tasks based on their group skills or load.

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/onedavidwilliams/AgentEx.git
cd AgentEx
```
### Set Up a Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
### Install Dependencies
```bash
pip install -r requirements.txt
```
### Run the Example
```bash
python AgentEx.py
```
This will spin up swarms, create agents, queue tasks, and show them exchanging messages.

## Example Flow

- **Swarm1** has `Agent1` and `Agent2`.
- **Swarm2** has `Agent3` and `Agent4`, each belonging to an `analytics` group.
- **Agents** can perform tasks like:
  - Fetching data (`DataFetchTask`)
  - Processing data (`DataProcessingTask`)
  - Analyzing results (`AnalysisTask`)
- **Cross-Swarm Message:** “Hello, Swarm2 team” is broadcast to all agents in Swarm2, or specifically to `analytics` if that group is recognized.

Logs will indicate how messages are routed, whether tasks are asynchronous, and how agents handle them. Agents can see which group the message was sent to and which group(s) the sender belongs to.

## Contributing

We welcome contributions, bug fixes, and ideas! To contribute:

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
### Open a Pull Request

### Potential Areas for Contribution

- **RAG Integration:** Hooking in a vector database or knowledge base.
- **LLM-Based Advanced Agent Logic.**
- **Agent Introspection:** More robust logging.
- **GUI Development:** Monitoring swarms, tasks, and agent communications in real-time.

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).

## Contact and Future Discussion

If you have ideas for advanced swarm architectures or want to see:

- **Custom Domain Expansions:** (e.g., finance, e-commerce, DevOps)
- **LLM-Driven Retrieval:** For adaptive agent knowledge.
- **Distributed Swarm Networks:** Multi-hub or federated swarms.

Then please open an issue or pull request. Let’s evolve **AgentEx** into a powerful multi-agent + LLM synergy framework!
