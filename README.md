# WhatsApp MCP Server

A Model Context Protocol (MCP) server that enables AI assistants to send and receive WhatsApp messages through a secure bridge architecture.

## 🚀 Features

- **Send WhatsApp Messages**: Send text messages to any WhatsApp number
- **Receive Messages**: Retrieve and search through WhatsApp conversations
- **Audio Support**: Send and receive audio messages
- **Media Handling**: Support for images, documents, and other media files
- **Contact Management**: Search and manage WhatsApp contacts
- **Group Support**: Interact with WhatsApp groups
- **Secure Bridge**: Go-based bridge for WhatsApp Web API communication

## 🏗️ Architecture

The project consists of two main components:

1. **WhatsApp MCP Server** (Python) - MCP server that provides the AI interface
2. **WhatsApp Bridge** (Go) - Handles WhatsApp Web API communication

```
AI Assistant (VSCode/Copilot)
        ↓ (MCP Protocol)
WhatsApp MCP Server (Python)
        ↓ (HTTP API)
WhatsApp Bridge (Go)
        ↓ (WhatsApp Web API)
WhatsApp
```

## � Installation

### Prerequisites

- Python 3.11+
- Go 1.21+
- Node.js (for MCP integration)
- uv (Python package manager)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ananyaakamat/WhatsApp_project.git
   cd WhatsApp_project
   ```

2. **Set up the Python MCP Server**:
   ```bash
   cd whatsapp-mcp/whatsapp-mcp-server
   uv venv
   uv pip install -r requirements.txt
   ```

3. **Set up the Go Bridge**:
   ```bash
   cd ../whatsapp-bridge
   go mod download
   go build -o whatsapp-bridge main.go
   ```

## 🔧 Configuration

### MCP Server Configuration

Add the WhatsApp MCP server to your VSCode settings.json:

```json
{
  "mcp": {
    "servers": {
      "whatsapp": {
        "command": "uv",
        "args": [
          "--directory",
          "/path/to/WhatsApp_project/whatsapp-mcp/whatsapp-mcp-server",
          "run",
          "main.py"
        ]
      }
    }
  }
}
```

### Bridge Configuration

The Go bridge will automatically start and handle WhatsApp Web authentication through QR code scanning.

## 🚀 Usage

### Starting the Services

1. **Start the Go Bridge**:
   ```bash
   cd whatsapp-mcp/whatsapp-bridge
   ./whatsapp-bridge
   ```

2. **Scan QR Code**: The bridge will display a QR code for WhatsApp Web authentication

3. **Use in AI Assistant**: The MCP server will automatically connect to the bridge

### Available MCP Tools

- `mcp_whatsapp_send_message` - Send text messages
- `mcp_whatsapp_send_file` - Send media files
- `mcp_whatsapp_send_audio_message` - Send audio messages
- `mcp_whatsapp_list_messages` - Retrieve message history
- `mcp_whatsapp_list_chats` - Get chat list
- `mcp_whatsapp_search_contacts` - Search contacts
- `mcp_whatsapp_get_message_context` - Get message context

### Example Usage

```python
# Send a message
await mcp_whatsapp_send_message(
    recipient="1234567890",  # Phone number with country code
    message="Hello from AI assistant!"
)

# Get recent messages
messages = await mcp_whatsapp_list_messages(
    limit=10,
    sender_phone_number="1234567890"
)

# Send a file
await mcp_whatsapp_send_file(
    recipient="1234567890",
    media_path="/path/to/file.pdf"
)
```

## 🔐 Security

- The bridge runs locally and doesn't store credentials
- All communication uses secure HTTP/HTTPS
- WhatsApp Web sessions are managed securely
- No message content is logged or stored permanently

## 🛠️ Development

### Project Structure

```
WhatsApp_project/
├── whatsapp-mcp/
│   ├── whatsapp-mcp-server/     # Python MCP server
│   │   ├── main.py              # MCP server implementation
│   │   ├── whatsapp.py          # WhatsApp client wrapper
│   │   ├── audio.py             # Audio message handling
│   │   └── requirements.txt     # Python dependencies
│   └── whatsapp-bridge/         # Go bridge
│       ├── main.go              # Bridge server
│       ├── go.mod               # Go module definition
│       └── go.sum               # Go dependencies
├── docs/                        # Documentation
├── templates/                   # Project templates
└── README.md                    # This file
```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit with conventional commits: `git commit -m "feat: add new feature"`
5. Push and create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Support

- Create an issue for bug reports or feature requests
- Check the documentation in the `docs/` folder
- Review the example implementations in `templates/`

## 🙏 Acknowledgments

- Built using the Model Context Protocol (MCP) specification
- WhatsApp Web API integration through go-whatsapp library
- Inspired by the need for AI assistant WhatsApp integration
