#!/usr/bin/env python3
"""
WhatsApp MCP Server

A Model Context Protocol (MCP) server that provides WhatsApp messaging capabilities.
This server allows AI assistants to send and receive WhatsApp messages through 
the WhatsApp Web API.
"""

import asyncio
import logging
import sqlite3
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence
from datetime import datetime

import mcp.types as types
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the MCP server
mcp = FastMCP("WhatsApp MCP Server")

# Path to the WhatsApp bridge executable and database
BRIDGE_PATH = Path(__file__).parent.parent / "whatsapp-bridge"
DB_PATH = BRIDGE_PATH / "store" / "whatsapp.db"
MESSAGES_DB_PATH = BRIDGE_PATH / "store" / "messages.db"

class WhatsAppBridge:
    """Interface to communicate with the WhatsApp bridge."""
    
    def __init__(self):
        self.db_path = DB_PATH
        self.messages_db_path = MESSAGES_DB_PATH
    
    def get_connection(self) -> Optional[sqlite3.Connection]:
        """Get database connection."""
        try:
            if self.db_path.exists():
                return sqlite3.connect(str(self.db_path))
            return None
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            return None
    
    def get_contacts(self) -> List[Dict[str, Any]]:
        """Get list of WhatsApp contacts."""
        conn = self.get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM contacts LIMIT 50")
            columns = [description[0] for description in cursor.description]
            contacts = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return contacts
        except Exception as e:
            logger.error(f"Failed to get contacts: {e}")
            return []
        finally:
            conn.close()
    
    def get_recent_messages(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent messages."""
        conn = sqlite3.connect(str(self.messages_db_path)) if self.messages_db_path.exists() else None
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM messages 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (limit,))
            columns = [description[0] for description in cursor.description]
            messages = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return messages
        except Exception as e:
            logger.error(f"Failed to get messages: {e}")
            return []
        finally:
            conn.close()
    
    def send_message(self, phone_number: str, message: str) -> Dict[str, Any]:
        """Send a WhatsApp message."""
        # This would typically interact with the WhatsApp bridge executable
        # For now, we'll simulate the message sending
        logger.info(f"Sending message to {phone_number}: {message}")
        
        # In a real implementation, this would:
        # 1. Execute the WhatsApp bridge with appropriate parameters
        # 2. Return the result of the operation
        
        return {
            "success": True,
            "message": "Message sent successfully (simulated)",
            "timestamp": datetime.now().isoformat(),
            "phone_number": phone_number,
            "content": message
        }

# Initialize WhatsApp bridge
whatsapp = WhatsAppBridge()

@mcp.tool()
def get_whatsapp_contacts() -> List[Dict[str, Any]]:
    """
    Get list of WhatsApp contacts.
    
    Returns:
        List of contact dictionaries with phone numbers and names.
    """
    return whatsapp.get_contacts()

@mcp.tool()
def get_recent_whatsapp_messages(limit: int = 20) -> List[Dict[str, Any]]:
    """
    Get recent WhatsApp messages.
    
    Args:
        limit: Maximum number of messages to retrieve (default: 20, max: 100)
    
    Returns:
        List of recent messages with sender, content, and timestamp.
    """
    limit = min(max(1, limit), 100)  # Ensure limit is between 1 and 100
    return whatsapp.get_recent_messages(limit)

@mcp.tool()
def send_whatsapp_message(phone_number: str, message: str) -> Dict[str, Any]:
    """
    Send a WhatsApp message to a specific phone number.
    
    Args:
        phone_number: The recipient's phone number (include country code, e.g., +1234567890)
        message: The message content to send
    
    Returns:
        Dictionary with success status and message details.
    """
    if not phone_number or not message:
        return {
            "success": False,
            "error": "Phone number and message are required"
        }
    
    return whatsapp.send_message(phone_number, message)

@mcp.tool()
def get_whatsapp_status() -> Dict[str, Any]:
    """
    Get the current status of the WhatsApp bridge connection.
    
    Returns:
        Dictionary with connection status and bridge information.
    """
    bridge_exists = (BRIDGE_PATH / "whatsapp-bridge.exe").exists()
    db_exists = DB_PATH.exists()
    messages_db_exists = MESSAGES_DB_PATH.exists()
    
    status = {
        "bridge_executable": bridge_exists,
        "database_connected": db_exists,
        "messages_database": messages_db_exists,
        "bridge_path": str(BRIDGE_PATH),
        "status": "ready" if (bridge_exists and db_exists) else "not_ready"
    }
    
    if db_exists:
        contacts_count = len(whatsapp.get_contacts())
        status["contacts_count"] = contacts_count
    
    return status

async def main():
    """Main entry point for the MCP server."""
    logger.info("Starting WhatsApp MCP Server...")
    
    # Check if bridge components exist
    status = get_whatsapp_status()
    logger.info(f"WhatsApp Bridge Status: {status}")
    
    # Run the MCP server
    await mcp.run()

if __name__ == "__main__":
    asyncio.run(main())
