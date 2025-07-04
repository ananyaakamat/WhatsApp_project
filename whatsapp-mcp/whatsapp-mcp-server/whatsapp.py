import sqlite3
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, List, Tuple
import os.path
import requests
import json
import audio

MESSAGES_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'whatsapp-bridge', 'store', 'messages.db')
WHATSAPP_API_BASE_URL = "http://localhost:8080/api"

@dataclass
class Message:
    timestamp: datetime
    sender: str
    content: str
    is_from_me: bool
    chat_jid: str
    id: str
    chat_name: Optional[str] = None
    media_type: Optional[str] = None

@dataclass
class Chat:
    jid: str
    name: Optional[str]
    last_message_time: Optional[datetime]
    last_message: Optional[str] = None
    last_sender: Optional[str] = None
    last_is_from_me: Optional[bool] = None

    @property
    def is_group(self) -> bool:
        """Determine if chat is a group based on JID pattern."""
        return self.jid.endswith("@g.us")

@dataclass
class Contact:
    phone_number: str
    name: Optional[str]
    jid: str

@dataclass
class MessageContext:
    message: Message
    before: List[Message]
    after: List[Message]

def get_sender_name(sender_jid: str) -> str:
    """Get the display name for a sender JID."""
    try:
        conn = sqlite3.connect(MESSAGES_DB_PATH)
        cursor = conn.cursor()

        # Try to get contact name first
        cursor.execute("""
            SELECT name FROM contacts
            WHERE jid = ? OR phone_number = ?
        """, (sender_jid, sender_jid))

        result = cursor.fetchone()
        if result and result[0]:
            return result[0]

        # If no contact name, return the JID/phone number
        return sender_jid

    except sqlite3.Error as e:
        print(f"Database error while getting sender name: {e}")
        return sender_jid
    finally:
        if 'conn' in locals():
            conn.close()

def format_message(message: Message, show_chat_info: bool = True) -> str:
    """Format a single message with consistent formatting."""
    sender_name = get_sender_name(message.sender)

    # Format timestamp
    time_str = message.timestamp.strftime("%Y-%m-%d %H:%M:%S")

    # Build message string
    msg_parts = []

    if show_chat_info and message.chat_name:
        msg_parts.append(f"[{message.chat_name}]")

    if message.is_from_me:
        msg_parts.append(f"You ({time_str})")
    else:
        msg_parts.append(f"{sender_name} ({time_str})")

    if message.media_type:
        msg_parts.append(f"[{message.media_type.upper()}]")

    msg_parts.append(f": {message.content}")

    return " ".join(msg_parts) + "\n"

def format_messages_list(messages: List[Message], show_chat_info: bool = True) -> str:
    """Format a list of messages for display."""
    output = ""
    if not messages:
        output += "No messages to display."
        return output

    for message in messages:
        output += format_message(message, show_chat_info)
    return output

def list_messages(
    after: Optional[str] = None,
    before: Optional[str] = None,
    sender_phone_number: Optional[str] = None,
    chat_jid: Optional[str] = None,
    query: Optional[str] = None,
    limit: int = 20,
    page: int = 0,
    include_context: bool = True,
    context_before: int = 1,
    context_after: int = 1
) -> List[Message]:
    """Get messages matching the specified criteria with optional context."""
    try:
        conn = sqlite3.connect(MESSAGES_DB_PATH)
        cursor = conn.cursor()

        # Build query
        query_parts = ["""
            SELECT messages.timestamp, messages.sender, chats.name as chat_name,
                   messages.content, messages.is_from_me, messages.chat_jid,
                   messages.id, messages.media_type
            FROM messages
            LEFT JOIN chats ON messages.chat_jid = chats.jid
        """]

        where_clauses = []
        params = []

        if after:
            try:
                after = datetime.fromisoformat(after)
            except ValueError:
                raise ValueError(f"Invalid date format for 'after': {after}. Please use ISO-8601 format.")

            where_clauses.append("messages.timestamp > ?")
            params.append(after)

        if before:
            try:
                before = datetime.fromisoformat(before)
            except ValueError:
                raise ValueError(f"Invalid date format for 'before': {before}. Please use ISO-8601 format.")

            where_clauses.append("messages.timestamp < ?")
            params.append(before)

        if sender_phone_number:
            where_clauses.append("messages.sender = ?")
            params.append(sender_phone_number)

        if chat_jid:
            where_clauses.append("messages.chat_jid = ?")
            params.append(chat_jid)

        if query:
            where_clauses.append("LOWER(messages.content) LIKE LOWER(?)")
            params.append(f"%{query}%")

        if where_clauses:
            query_parts.append("WHERE " + " AND ".join(where_clauses))

        # Add pagination
        offset = page * limit
        query_parts.append("ORDER BY messages.timestamp DESC")
        query_parts.append("LIMIT ? OFFSET ?")
        params.extend([limit, offset])

        cursor.execute(" ".join(query_parts), tuple(params))
        messages = cursor.fetchall()

        result = []
        for msg in messages:
            message = Message(
                timestamp=datetime.fromisoformat(msg[0]),
                sender=msg[1],
                chat_name=msg[2],
                content=msg[3],
                is_from_me=msg[4],
                chat_jid=msg[5],
                id=msg[6],
                media_type=msg[7]
            )
            result.append(message)

        if include_context and result:
            # Add context for each message
            messages_with_context = []
            for msg in result:
                context = get_message_context(msg.id, context_before, context_after)
                messages_with_context.extend(context.before)
                messages_with_context.append(context.message)
                messages_with_context.extend(context.after)

            return format_messages_list(messages_with_context, show_chat_info=True)

        # Format and display messages without context
        return format_messages_list(result, show_chat_info=True)

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        if 'conn' in locals():
            conn.close()

def get_message_context(
    message_id: str,
    before: int = 5,
    after: int = 5
) -> MessageContext:
    """Get context around a specific message."""
    try:
        conn = sqlite3.connect(MESSAGES_DB_PATH)
        cursor = conn.cursor()

        # Get the target message
        cursor.execute("""
            SELECT messages.timestamp, messages.sender, chats.name as chat_name,
                   messages.content, messages.is_from_me, messages.chat_jid,
                   messages.id, messages.media_type
            FROM messages
            LEFT JOIN chats ON messages.chat_jid = chats.jid
            WHERE messages.id = ?
        """, (message_id,))

        msg_data = cursor.fetchone()
        if not msg_data:
            raise ValueError(f"Message with ID {message_id} not found")

        target_message = Message(
            timestamp=datetime.fromisoformat(msg_data[0]),
            sender=msg_data[1],
            chat_name=msg_data[2],
            content=msg_data[3],
            is_from_me=msg_data[4],
            chat_jid=msg_data[5],
            id=msg_data[6],
            media_type=msg_data[7]
        )

        # Get messages before
        cursor.execute("""
            SELECT messages.timestamp, messages.sender, chats.name as chat_name,
                   messages.content, messages.is_from_me, messages.chat_jid,
                   messages.id, messages.media_type
            FROM messages
            LEFT JOIN chats ON messages.chat_jid = chats.jid
            WHERE messages.chat_jid = ? AND messages.timestamp < ?
            ORDER BY messages.timestamp DESC
            LIMIT ?
        """, (target_message.chat_jid, target_message.timestamp, before))

        before_messages = []
        for msg in reversed(cursor.fetchall()):  # Reverse to get chronological order
            before_messages.append(Message(
                timestamp=datetime.fromisoformat(msg[0]),
                sender=msg[1],
                chat_name=msg[2],
                content=msg[3],
                is_from_me=msg[4],
                chat_jid=msg[5],
                id=msg[6],
                media_type=msg[7]
            ))

        # Get messages after
        cursor.execute("""
            SELECT messages.timestamp, messages.sender, chats.name as chat_name,
                   messages.content, messages.is_from_me, messages.chat_jid,
                   messages.id, messages.media_type
            FROM messages
            LEFT JOIN chats ON messages.chat_jid = chats.jid
            WHERE messages.chat_jid = ? AND messages.timestamp > ?
            ORDER BY messages.timestamp ASC
            LIMIT ?
        """, (target_message.chat_jid, target_message.timestamp, after))

        after_messages = []
        for msg in cursor.fetchall():
            after_messages.append(Message(
                timestamp=datetime.fromisoformat(msg[0]),
                sender=msg[1],
                chat_name=msg[2],
                content=msg[3],
                is_from_me=msg[4],
                chat_jid=msg[5],
                id=msg[6],
                media_type=msg[7]
            ))

        return MessageContext(
            message=target_message,
            before=before_messages,
            after=after_messages
        )

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        raise
    finally:
        if 'conn' in locals():
            conn.close()

def list_chats(
    query: Optional[str] = None,
    limit: int = 20,
    page: int = 0,
    include_last_message: bool = True,
    sort_by: str = "last_active"
) -> List[Chat]:
    """Get chats matching the specified criteria."""
    try:
        conn = sqlite3.connect(MESSAGES_DB_PATH)
        cursor = conn.cursor()

        # Build query based on parameters
        if include_last_message:
            query_sql = """
                SELECT chats.jid, chats.name, chats.last_message_time,
                       chats.last_message, chats.last_sender, chats.last_is_from_me
                FROM chats
            """
        else:
            query_sql = """
                SELECT chats.jid, chats.name, chats.last_message_time,
                       NULL, NULL, NULL
                FROM chats
            """

        where_clauses = []
        params = []

        if query:
            where_clauses.append("LOWER(chats.name) LIKE LOWER(?)")
            params.append(f"%{query}%")

        if where_clauses:
            query_sql += " WHERE " + " AND ".join(where_clauses)

        # Add sorting
        if sort_by == "last_active":
            query_sql += " ORDER BY chats.last_message_time DESC"
        elif sort_by == "name":
            query_sql += " ORDER BY chats.name ASC"

        # Add pagination
        offset = page * limit
        query_sql += " LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        cursor.execute(query_sql, tuple(params))
        chats_data = cursor.fetchall()

        result = []
        for chat_data in chats_data:
            chat = Chat(
                jid=chat_data[0],
                name=chat_data[1],
                last_message_time=datetime.fromisoformat(chat_data[2]) if chat_data[2] else None,
                last_message=chat_data[3],
                last_sender=chat_data[4],
                last_is_from_me=chat_data[5]
            )
            result.append(chat)

        return result

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        if 'conn' in locals():
            conn.close()

def search_contacts(query: str) -> List[Contact]:
    """Search contacts by name or phone number."""
    try:
        conn = sqlite3.connect(MESSAGES_DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT phone_number, name, jid
            FROM contacts
            WHERE LOWER(name) LIKE LOWER(?) OR phone_number LIKE ?
            ORDER BY name ASC
            LIMIT 50
        """, (f"%{query}%", f"%{query}%"))

        contacts_data = cursor.fetchall()
        result = []

        for contact_data in contacts_data:
            contact = Contact(
                phone_number=contact_data[0],
                name=contact_data[1],
                jid=contact_data[2]
            )
            result.append(contact)

        return result

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        if 'conn' in locals():
            conn.close()

def get_contact_chats(jid: str, limit: int = 20, page: int = 0) -> List[Chat]:
    """Get all chats involving a specific contact."""
    try:
        conn = sqlite3.connect(MESSAGES_DB_PATH)
        cursor = conn.cursor()

        offset = page * limit

        cursor.execute("""
            SELECT DISTINCT chats.jid, chats.name, chats.last_message_time,
                            chats.last_message, chats.last_sender, chats.last_is_from_me
            FROM chats
            JOIN messages ON chats.jid = messages.chat_jid
            WHERE messages.sender = ? OR chats.jid = ?
            ORDER BY chats.last_message_time DESC
            LIMIT ? OFFSET ?
        """, (jid, jid, limit, offset))

        chats_data = cursor.fetchall()
        result = []

        for chat_data in chats_data:
            chat = Chat(
                jid=chat_data[0],
                name=chat_data[1],
                last_message_time=datetime.fromisoformat(chat_data[2]) if chat_data[2] else None,
                last_message=chat_data[3],
                last_sender=chat_data[4],
                last_is_from_me=chat_data[5]
            )
            result.append(chat)

        return result

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        if 'conn' in locals():
            conn.close()

def get_last_interaction(jid: str) -> str:
    """Get most recent message involving the contact."""
    try:
        conn = sqlite3.connect(MESSAGES_DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT messages.timestamp, messages.sender, messages.content,
                   messages.is_from_me, chats.name as chat_name
            FROM messages
            LEFT JOIN chats ON messages.chat_jid = chats.jid
            WHERE messages.sender = ? OR messages.chat_jid = ?
            ORDER BY messages.timestamp DESC
            LIMIT 1
        """, (jid, jid))

        msg_data = cursor.fetchone()
        if not msg_data:
            return f"No messages found for {jid}"

        message = Message(
            timestamp=datetime.fromisoformat(msg_data[0]),
            sender=msg_data[1],
            content=msg_data[2],
            is_from_me=msg_data[3],
            chat_name=msg_data[4],
            chat_jid=jid,
            id="",
            media_type=None
        )

        return format_message(message, show_chat_info=True)

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return f"Error getting last interaction: {e}"
    finally:
        if 'conn' in locals():
            conn.close()

def get_chat(chat_jid: str, include_last_message: bool = True) -> Optional[Chat]:
    """Get chat metadata by JID."""
    try:
        conn = sqlite3.connect(MESSAGES_DB_PATH)
        cursor = conn.cursor()

        if include_last_message:
            cursor.execute("""
                SELECT jid, name, last_message_time, last_message, last_sender, last_is_from_me
                FROM chats
                WHERE jid = ?
            """, (chat_jid,))
        else:
            cursor.execute("""
                SELECT jid, name, last_message_time, NULL, NULL, NULL
                FROM chats
                WHERE jid = ?
            """, (chat_jid,))

        chat_data = cursor.fetchone()
        if not chat_data:
            return None

        return Chat(
            jid=chat_data[0],
            name=chat_data[1],
            last_message_time=datetime.fromisoformat(chat_data[2]) if chat_data[2] else None,
            last_message=chat_data[3],
            last_sender=chat_data[4],
            last_is_from_me=chat_data[5]
        )

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if 'conn' in locals():
            conn.close()

def get_direct_chat_by_contact(sender_phone_number: str) -> Optional[Chat]:
    """Get chat metadata by sender phone number."""
    try:
        conn = sqlite3.connect(MESSAGES_DB_PATH)
        cursor = conn.cursor()

        # Find the chat JID for this contact
        cursor.execute("""
            SELECT DISTINCT chat_jid
            FROM messages
            WHERE sender = ? AND chat_jid LIKE '%@s.whatsapp.net'
            LIMIT 1
        """, (sender_phone_number,))

        jid_result = cursor.fetchone()
        if not jid_result:
            return None

        chat_jid = jid_result[0]

        # Get chat metadata
        cursor.execute("""
            SELECT jid, name, last_message_time, last_message, last_sender, last_is_from_me
            FROM chats
            WHERE jid = ?
        """, (chat_jid,))

        chat_data = cursor.fetchone()
        if not chat_data:
            return None

        return Chat(
            jid=chat_data[0],
            name=chat_data[1],
            last_message_time=datetime.fromisoformat(chat_data[2]) if chat_data[2] else None,
            last_message=chat_data[3],
            last_sender=chat_data[4],
            last_is_from_me=chat_data[5]
        )

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if 'conn' in locals():
            conn.close()

def send_message(recipient: str, message: str) -> Tuple[bool, str]:
    """Send a WhatsApp message via the bridge API."""
    try:
        # Validate input
        if not recipient:
            return False, "Recipient must be provided"

        url = f"{WHATSAPP_API_BASE_URL}/send"
        payload = {
            "recipient": recipient,
            "message": message,
        }

        response = requests.post(url, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
            return result.get("success", False), result.get("message", "Unknown response")
        else:
            return False, f"Error: HTTP {response.status_code} - {response.text}"

    except requests.RequestException as e:
        return False, f"Request error: {str(e)}"
    except json.JSONDecodeError:
        return False, f"Error parsing response: {response.text}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

def send_file(recipient: str, media_path: str) -> Tuple[bool, str]:
    """Send a file via WhatsApp."""
    try:
        # Validate input
        if not recipient:
            return False, "Recipient must be provided"

        if not media_path:
            return False, "Media path must be provided"

        if not os.path.isfile(media_path):
            return False, f"Media file not found: {media_path}"

        url = f"{WHATSAPP_API_BASE_URL}/send"
        payload = {
            "recipient": recipient,
            "media_path": media_path
        }

        response = requests.post(url, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
            return result.get("success", False), result.get("message", "Unknown response")
        else:
            return False, f"Error: HTTP {response.status_code} - {response.text}"

    except requests.RequestException as e:
        return False, f"Request error: {str(e)}"
    except json.JSONDecodeError:
        return False, f"Error parsing response: {response.text}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

def send_audio_message(recipient: str, media_path: str) -> Tuple[bool, str]:
    """Send an audio message as a voice note."""
    try:
        # Validate input
        if not recipient:
            return False, "Recipient must be provided"

        if not media_path:
            return False, "Media path must be provided"

        if not os.path.isfile(media_path):
            return False, f"Media file not found: {media_path}"

        if not media_path.endswith(".ogg"):
            try:
                media_path = audio.convert_to_opus_ogg_temp(media_path)
            except Exception as e:
                return False, f"Error converting file to opus ogg. You likely need to install ffmpeg: {str(e)}"

        url = f"{WHATSAPP_API_BASE_URL}/send"
        payload = {
            "recipient": recipient,
            "media_path": media_path
        }

        response = requests.post(url, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
            return result.get("success", False), result.get("message", "Unknown response")
        else:
            return False, f"Error: HTTP {response.status_code} - {response.text}"

    except requests.RequestException as e:
        return False, f"Request error: {str(e)}"
    except json.JSONDecodeError:
        return False, f"Error parsing response: {response.text}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

def download_media(message_id: str, chat_jid: str) -> Optional[str]:
    """Download media from a WhatsApp message."""
    try:
        url = f"{WHATSAPP_API_BASE_URL}/download"
        payload = {
            "message_id": message_id,
            "chat_jid": chat_jid
        }

        response = requests.post(url, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
            if result.get("success", False):
                return result.get("path")
            else:
                print(f"Download failed: {result.get('message', 'Unknown error')}")
                return None
        else:
            print(f"Error: HTTP {response.status_code} - {response.text}")
            return None

    except requests.RequestException as e:
        print(f"Request error: {str(e)}")
        return None
    except json.JSONDecodeError:
        print(f"Error parsing response: {response.text}")
        return None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None
