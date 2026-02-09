# 🚀 Simple MCP Demo

A comprehensive demonstration of a **Model Context Protocol (MCP)** server implemented in Python. This project showcases how to build a unified server that supports multiple transport mechanisms: **Standard I/O (stdio)**, **Server-Sent Events (SSE)**, and **Streamable HTTP**.

---

## 🛠️ Features

- **Multi-Transport Server**: One server, three ways to connect.
- **`add_numbers` Tool**: A functional example of a tool discovery and execution flow.
- **Reference Clients**: Dedicated Python scripts for each transport type.
- **Inspector Ready**: Fully compatible with the official MCP Inspector.

---

## 📂 Project Structure

- `server.py`: The core MCP server containing tool logic and transport routing.
- `client_stdio.py`: Client for local subprocess communication (pipes).
- `client_sse.py`: Client for web-based event streaming.
- `client_http.py`: Client for stateful session-based HTTP streaming.
- `DOCUMENTATION.md`: Detailed functional and technical specifications.
- `requirements.txt`: Project dependencies.

---

## 🚀 Getting Started

### 1. Installation
Clone the repo and install the required packages:
```bash
pip install -r requirements.txt
```

### 2. Run with MCP Inspector (Recommended)
The easiest way to test the server is using the official tool inspector:
```bash
npx @modelcontextprotocol/inspector python server.py
```

### 3. Run Reference Clients

#### Standard I/O (stdio)
```bash
python client_stdio.py
```

#### Server-Sent Events (SSE)
Terminal 1 (Start Server):
```bash
python server.py --transport sse
```
Terminal 2 (Run Client):
```bash
python client_sse.py
```

#### Streamable HTTP
Terminal 1 (Start Server):
```bash
python server.py --transport http
```
Terminal 2 (Run Client):
```bash
python client_http.py
```

---

## 📈 Protocol Flow

1. **Initialize**: Client and Server exchange capabilities.
2. **List Tools**: Client discovers the `add_numbers` tool.
3. **Call Tool**: Client sends parameters (`a`, `b`) and receives the sum.

---

## 📝 Technical Details
For a deeper dive into the architecture, flow diagrams, and transport implementation details, see [DOCUMENTATION.md](./DOCUMENTATION.md).

---

Built with ❤️ using the [Model Context Protocol](https://modelcontextprotocol.io/)
