# MCP Server Prototypes

## Overview

This project investigates the Model Context Protocol (MCP) and demonstrates how AI assistants can interact with external data sources through MCP servers.

Four MCP server prototypes were developed:

- Excel MCP Server
- PDF MCP Server
- SQL MCP Server
- DXF MCP Server

These servers expose tools that allow AI assistants such as Claude Desktop to read, create, update, and analyze local resources through a standardized protocol.

---

## MCP Architecture

MCP follows a client-server architecture.

1. The user interacts with an AI client.
2. The AI client communicates with MCP servers using the MCP protocol.
3. MCP servers expose tools.
4. Tools perform operations on external resources.
5. Results are returned to the AI client and presented to the user.

### Architecture Diagram

```text
User
  ↓
Claude Desktop (MCP Client)
  ↓
MCP Protocol
  ↓
MCP Servers
 ├── Excel Server
 ├── PDF Server
 ├── SQL Server
 └── DXF Server
```

---

## Technical Stack

| Component | Technology |
|------------|------------|
| Language | Python 3.x |
| MCP Framework | MCP Python SDK (FastMCP) |
| Excel Processing | openpyxl |
| PDF Processing | pdfplumber |
| Database | SQLite |
| DXF Processing | ezdxf |
| Testing Client | Claude Desktop |
| Development Environment | VS Code |

---

## Project Structure

```text
mcp-prototypes/
│
├── README.md
├── requirements.txt
│
├── excel_mcp/
│   ├── server.py
│   └── sample.xlsx
│
├── pdf_mcp/
│   ├── server.py
│   ├── sample1.pdf
│   └── sample2.pdf
│
├── sql_mcp/
│   ├── server.py
│   └── database.db
│
├── dxf_mcp/
│   └── server.py
│
└── .gitignore
```

---

## Setup

### Create Virtual Environment

```bash
python3 -m venv venv
```

### Activate Environment

macOS/Linux

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

SQLite is included with Python and does not require additional installation.

---

## Claude Desktop Configuration

Example MCP configuration:

```json
{
  "mcpServers": {
    "excel-mcp": {
      "command": "/path/to/venv/bin/python",
      "args": ["/path/to/excel_mcp/server.py"]
    },
    "pdf-mcp": {
      "command": "/path/to/venv/bin/python",
      "args": ["/path/to/pdf_mcp/server.py"]
    },
    "sql-mcp": {
      "command": "/path/to/venv/bin/python",
      "args": ["/path/to/sql_mcp/server.py"]
    },
    "dxf-mcp": {
      "command": "/path/to/venv/bin/python",
      "args": ["/path/to/dxf_mcp/server.py"]
    }
  }
}
```

Restart Claude Desktop after modifying the configuration.

---

# Excel MCP Server

## Tools

| Tool | Description |
|--------|-------------|
| server_directory | Show server location |
| list_excel_files | List available Excel files |
| create_excel | Create workbook |
| read_excel | Read active sheet |
| read_range | Read cell range |
| read_sheet | Read specific sheet |
| write_row | Append row |
| update_cell | Update cell |

## Example Prompts

- List available Excel files
- Create sales.xlsx with columns Customer, Product, Quantity
- Add a new row for Alice
- Read sales.xlsx
- Update Quantity to 500
- Read Sheet2 from sample.xlsx

---

# PDF MCP Server

## Tools

| Tool | Description |
|--------|-------------|
| server_directory | Show server location |
| list_pdf_files | List available PDFs |
| read_pdf | Extract text |
| read_pdf_tables | Extract tables |
| pdf_metadata | Retrieve metadata |

## Example Prompts

- List available PDF files
- Summarize sample1.pdf
- Extract tables from sample2.pdf
- Show metadata for sample2.pdf
- What are the key findings in sample2.pdf?

---

# SQL MCP Server

## Tools

| Tool | Description |
|--------|-------------|
| server_directory | Show server location |
| list_database_files | List SQLite databases |
| list_tables | Show tables |
| describe_table | Show schema |
| run_query | Execute SELECT queries |
| run_write | Execute INSERT/UPDATE/DELETE queries |
| seed_demo_data | Create demo data |

## Example Prompts

- Create demo data
- Show all orders
- Describe the orders table
- Add a new order for Sofia
- Update Sofia's quantity to 3
- Which customer placed the most orders?

---

# DXF MCP Server

## Tools

| Tool | Description |
|--------|-------------|
| server_directory | Show server location |
| list_dxf_files | List available DXF files |
| create_dxf | Create a new DXF drawing |
| add_line | Add a line entity |
| add_circle | Add a circle entity |
| add_arc | Add an arc entity |
| list_entities | List all entities |
| update_line | Update a line |
| update_circle | Update a circle |
| update_arc | Update an arc |
| delete_entity | Delete an entity by index |

## Example Prompts

- List available DXF files
- Create a new file called floorplan.dxf
- Add a line from (0,0) to (10,0)
- Add a circle at (5,5) with radius 3
- List all entities in floorplan.dxf
- Delete the line from floorplan.dxf
- Update the circle at (5,5) to have radius 6

---

## Key Findings

Traditional AI assistants are limited to information available within the conversation context.

The Model Context Protocol extends these capabilities by allowing AI clients to discover and invoke external tools exposed by MCP servers.

In this project:

- The Excel MCP server provided access to spreadsheets.
- The PDF MCP server provided access to document contents.
- The SQL MCP server provided access to database records.
- The DXF MCP server provided access to CAD drawing geometry.

These tools enabled Claude Desktop to perform real file and database operations through a standardized protocol.

---

## Limitations

These prototypes were designed for demonstration and learning purposes.

Current limitations include:

- No authentication
- Limited error handling
- Direct SQL execution
- Files restricted to server directories
- No role-based access control
