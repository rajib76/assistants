# Assistants
Developing language assistants with LLMs in a low-code way.

## Quick Install

Install using pip:

```bash
pip install assistants
```
The framework requires a database to register the assistants. The default database used is MongoAtlas. Future versions of the framework will support additional database types. Currently, there is a MongoDB collection named assistants which registers each assistant as shown below:

```
_id : 6556db6cf114addad09420c6
assistant_name: "test_assist"
assistant_id: "asst_52TLl1OdJW6ulmLCEsDlizz8"
file_id: "file-lZUBJ3ZnxtkTfqsuE0WYMXDI"

```
## What are Assistants?
Assistants is a framework for developing language-based assistants using micro agents, akin to the microservices concept. Each micro agent, like a microservice, can be independently developed and deployed. The framework adheres to the Single Responsibility Principle (SRP), allowing these assistants to be combined to address complex business processes through workflows.

## Capabilities of the Framework
In time, the framework will include built-in assistants for immediate deployment within OpenAI environments. It will also support the development of custom assistants.

## Contribution
Contributions are welcome in any form, be it through new features or improved documentation.

## Example Usage
The repository includes various examples demonstrating framework usage.
