# Understanding MCP

    - Standard for connecting AI applications to external systems
        - What kind of AI Applications?
            - Claude/ChatGPT/Gemini
        - What kind of external systems?
            - local files/databases. tools (search engine)/calculators, workflows (specialized prompts)
        - Why?
            - So that they access key information and perform tasks

    - Useful Mnemonic
        - USB C for AI applications: Standard way to connect AI applications to external systems

    - Why MCP?
        - Models can connect with other tools so that a problem can be solved in a personalized way
        - MCP reduces dev time and complexity when building/integrating with an AI application
        - MCP enhance the capabilities of AI tool

## Components of MCP

    - MCP follows client/server architecture
        - Server
            - where the data sources and tool live
        - Client
            - applications that connect to MCP servers

## Building an MCP client

    - Client can be anything
        - Can be own clients
        - Can be tools such as Claude desktop, ChatGPT or Gemini CLI etc, VS code etc.

### Core MCP Concepts

    - Servers can offer 3 types of capabilities
        - Resources: Data (In the form of Database, API connections, file contents)
        - Tools: Functions that can be called by the client
        - Prompt: Specialized prompts

    -  Logging in MCP Servers
        - What is Logging?
            - There are various streams of information flowing in between client and the server
                - Actual information that client is accessing and server is helping client get, or commands/instructions from client that the server needs to make use of. This information is transferred over stdout. Reference: print() statements in python or console.log statement in js output to stdout
                - There are also server errors/debugging messages and server record information that server produces. This information is called as logging
                    - These different streams of information should be kept separate
                    - So error or similar type of messages should be transferred using stderr or using logging module provided by python std lib.
