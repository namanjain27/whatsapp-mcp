"""
Test script for WhatsApp MCP tools.
Run this script to test all available WhatsApp MCP functions.
"""

import sys
from typing import Optional
from main import (
    search_contacts,
    list_messages,
    list_chats,
    get_chat,
    get_direct_chat_by_contact,
    get_contact_chats,
    get_last_interaction,
    get_message_context,
    send_message,
    send_file,
    send_audio_message,
    download_media
)


def test_search_contacts(query: str = "papa"):
    """Test searching for contacts."""
    print("\n" + "="*60)
    print("TEST: search_contacts")
    print("="*60)
    print(f"Query: {query}")
    try:
        result = search_contacts(query)
        print(f"Found {len(result)} contacts")
        for contact in result[:5]:  # Show first 5
            print(f"  - {contact.get('name', 'Unknown')}: {contact.get('phone_number', 'N/A')}")
        return result
    except Exception as e:
        print(f"ERROR: {e}")
        return None


def test_list_messages(
    after: Optional[str] = None,
    before: Optional[str] = None,
    sender_phone_number: Optional[str] = None,
    chat_jid: Optional[str] = None,
    query: Optional[str] = None,
    limit: int = 5,
    page: int = 0,
    include_context: bool = False,
    context_before: int = 1,
    context_after: int = 1
):
    """Test listing messages."""
    print("\n" + "="*60)
    print("TEST: list_messages")
    print("="*60)
    print(f"Filters: after={after}, before={before}, sender={sender_phone_number}, chat_jid={chat_jid}, query={query}")
    print(f"Limit: {limit}, Page: {page}, Include context: {include_context}")
    try:
        result = list_messages(
            after=after,
            before=before,
            sender_phone_number=sender_phone_number,
            chat_jid=chat_jid,
            query=query,
            limit=limit,
            page=page,
            include_context=include_context,
            context_before=context_before,
            context_after=context_after
        )
        if isinstance(result, str):
            print("Messages (formatted):")
            print(result[:500] + "..." if len(result) > 500 else result)
        else:
            print(f"Found {len(result)} messages")
            for msg in result[:3]:  # Show first 3
                print(f"  - {msg}")
        return result
    except Exception as e:
        print(f"ERROR: {e}")
        return None


def test_list_chats(
    query: Optional[str] = None,
    limit: int = 5,
    page: int = 0,
    include_last_message: bool = True,
    sort_by: str = "last_active"
):
    """Test listing chats."""
    print("\n" + "="*60)
    print("TEST: list_chats")
    print("="*60)
    print(f"Query: {query}, Limit: {limit}, Sort by: {sort_by}")
    try:
        result = list_chats(
            query=query,
            limit=limit,
            page=page,
            include_last_message=include_last_message,
            sort_by=sort_by
        )
        print(f"Found {len(result)} chats")
        for chat in result[:5]:  # Show first 5
            name = chat.get('name', 'Unknown')
            jid = chat.get('jid', 'N/A')
            last_msg = chat.get('last_message', 'No message')
            print(f"  - {name} ({jid})")
            if last_msg:
                print(f"    Last: {last_msg[:50]}...")
        return result
    except Exception as e:
        print(f"ERROR: {e}")
        return None


def test_get_chat(chat_jid: str, include_last_message: bool = True):
    """Test getting a specific chat."""
    print("\n" + "="*60)
    print("TEST: get_chat")
    print("="*60)
    print(f"Chat JID: {chat_jid}")
    try:
        result = get_chat(chat_jid, include_last_message)
        if result:
            print(f"Chat found: {result.get('name', 'Unknown')}")
            print(f"JID: {result.get('jid', 'N/A')}")
            if result.get('last_message'):
                print(f"Last message: {result.get('last_message', 'N/A')[:100]}")
        else:
            print("Chat not found")
        return result
    except Exception as e:
        print(f"ERROR: {e}")
        return None


def test_get_direct_chat_by_contact(sender_phone_number: str):
    """Test getting a direct chat by phone number."""
    print("\n" + "="*60)
    print("TEST: get_direct_chat_by_contact")
    print("="*60)
    print(f"Phone number: {sender_phone_number}")
    try:
        result = get_direct_chat_by_contact(sender_phone_number)
        if result:
            print(f"Chat found: {result.get('name', 'Unknown')}")
            print(f"JID: {result.get('jid', 'N/A')}")
        else:
            print("Chat not found")
        return result
    except Exception as e:
        print(f"ERROR: {e}")
        return None


def test_get_contact_chats(jid: str, limit: int = 5, page: int = 0):
    """Test getting all chats for a contact."""
    print("\n" + "="*60)
    print("TEST: get_contact_chats")
    print("="*60)
    print(f"Contact JID: {jid}")
    try:
        result = get_contact_chats(jid, limit, page)
        print(f"Found {len(result)} chats")
        for chat in result[:3]:  # Show first 3
            print(f"  - {chat.get('name', 'Unknown')}: {chat.get('jid', 'N/A')}")
        return result
    except Exception as e:
        print(f"ERROR: {e}")
        return None


def test_get_last_interaction(jid: str):
    """Test getting the last interaction with a contact."""
    print("\n" + "="*60)
    print("TEST: get_last_interaction")
    print("="*60)
    print(f"Contact JID: {jid}")
    try:
        result = get_last_interaction(jid)
        if result:
            print("Last interaction:")
            print(result[:300] + "..." if len(result) > 300 else result)
        else:
            print("No interaction found")
        return result
    except Exception as e:
        print(f"ERROR: {e}")
        return None


def test_get_message_context(message_id: str, before: int = 3, after: int = 3):
    """Test getting message context."""
    print("\n" + "="*60)
    print("TEST: get_message_context")
    print("="*60)
    print(f"Message ID: {message_id}")
    print(f"Context: {before} before, {after} after")
    try:
        result = get_message_context(message_id, before, after)
        if result:
            print("Message context retrieved:")
            # Handle both dict and dataclass types
            if isinstance(result, dict):
                msg = result.get('message', {})
                if isinstance(msg, dict):
                    print(f"  Target message: {msg.get('content', 'N/A')[:100]}")
                else:
                    print(f"  Target message: {getattr(msg, 'content', 'N/A')[:100]}")
                print(f"  Messages before: {len(result.get('before', []))}")
                print(f"  Messages after: {len(result.get('after', []))}")
            else:
                # Dataclass type
                print(f"  Target message: {getattr(result.message, 'content', 'N/A')[:100]}")
                print(f"  Messages before: {len(result.before)}")
                print(f"  Messages after: {len(result.after)}")
        else:
            print("Message context not found")
        return result
    except Exception as e:
        print(f"ERROR: {e}")
        return None


def test_send_message(recipient: str, message: str):
    """Test sending a message."""
    print("\n" + "="*60)
    print("TEST: send_message")
    print("="*60)
    print(f"Recipient: {recipient}")
    print(f"Message: {message}")
    try:
        result = send_message(recipient, message)
        print(f"Success: {result.get('success', False)}")
        print(f"Status: {result.get('message', 'N/A')}")
        return result
    except Exception as e:
        print(f"ERROR: {e}")
        return None


def test_send_file(recipient: str, media_path: str):
    """Test sending a file."""
    print("\n" + "="*60)
    print("TEST: send_file")
    print("="*60)
    print(f"Recipient: {recipient}")
    print(f"Media path: {media_path}")
    try:
        result = send_file(recipient, media_path)
        print(f"Success: {result.get('success', False)}")
        print(f"Status: {result.get('message', 'N/A')}")
        return result
    except Exception as e:
        print(f"ERROR: {e}")
        return None


def test_send_audio_message(recipient: str, media_path: str):
    """Test sending an audio message."""
    print("\n" + "="*60)
    print("TEST: send_audio_message")
    print("="*60)
    print(f"Recipient: {recipient}")
    print(f"Media path: {media_path}")
    try:
        result = send_audio_message(recipient, media_path)
        print(f"Success: {result.get('success', False)}")
        print(f"Status: {result.get('message', 'N/A')}")
        return result
    except Exception as e:
        print(f"ERROR: {e}")
        return None


def test_download_media(message_id: str, chat_jid: str):
    """Test downloading media from a message."""
    print("\n" + "="*60)
    print("TEST: download_media")
    print("="*60)
    print(f"Message ID: {message_id}")
    print(f"Chat JID: {chat_jid}")
    try:
        result = download_media(message_id, chat_jid)
        print(f"Success: {result.get('success', False)}")
        print(f"Status: {result.get('message', 'N/A')}")
        if result.get('file_path'):
            print(f"File path: {result.get('file_path')}")
        return result
    except Exception as e:
        print(f"ERROR: {e}")
        return None


def run_all_tests():
    """Run all tests with default/sample values."""
    print("\n" + "="*60)
    print("RUNNING ALL WHATSAPP MCP TOOL TESTS")
    print("="*60)
    
    # Test 1: Search contacts
    contacts = test_search_contacts("papa")
    if contacts and len(contacts) > 0:
        sample_contact = contacts[0]
        sample_jid = sample_contact.get('jid', '')
        sample_phone = sample_contact.get('phone_number', '')
    else:
        sample_jid = ""
        sample_phone = ""
    
    # Test 2: List chats
    chats = test_list_chats(query = "papa",limit=3)
    if chats and len(chats) > 0:
        sample_chat_jid = chats[0].get('jid', '')
    else:
        sample_chat_jid = ""
    
    # Test 3: List messages
    test_list_messages(limit=3)
    
    # Test 4: Get chat (if we have a chat JID)
    if sample_chat_jid:
        test_get_chat(sample_chat_jid)
    
    # Test 5: Get direct chat by contact (if we have a phone number)
    if sample_phone:
        test_get_direct_chat_by_contact(sample_phone)
    
    # Test 6: Get contact chats (if we have a JID)
    if sample_jid:
        test_get_contact_chats(sample_jid)
    
    # Test 7: Get last interaction (if we have a JID)
    if sample_jid:
        test_get_last_interaction(sample_jid)
    
    # Note: Tests 8-12 require specific IDs/values that should be provided by user
    print("\n" + "="*60)
    print("TESTS COMPLETE")
    print("="*60)
    print("\nNote: Some tests require specific parameters:")
    print("  - get_message_context: requires a message_id")
    print("  - send_message: requires recipient and message")
    print("  - send_file: requires recipient and media_path")
    print("  - send_audio_message: requires recipient and media_path")
    print("  - download_media: requires message_id and chat_jid")
    print("\nYou can call these functions individually with your own parameters.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Allow running specific tests from command line
        test_name = sys.argv[1]
        
        if test_name == "search_contacts":
            query = sys.argv[2] if len(sys.argv) > 2 else ""
            test_search_contacts(query)
        elif test_name == "list_messages":
            test_list_messages(limit=5)
        elif test_name == "list_chats":
            query = sys.argv[2] if len(sys.argv) > 2 else None
            test_list_chats(query=query)
        elif test_name == "get_chat" and len(sys.argv) > 2:
            test_get_chat(sys.argv[2])
        elif test_name == "get_direct_chat" and len(sys.argv) > 2:
            test_get_direct_chat_by_contact(sys.argv[2])
        elif test_name == "get_contact_chats" and len(sys.argv) > 2:
            test_get_contact_chats(sys.argv[2])
        elif test_name == "get_last_interaction" and len(sys.argv) > 2:
            test_get_last_interaction(sys.argv[2])
        elif test_name == "get_message_context" and len(sys.argv) > 3:
            test_get_message_context(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]) if len(sys.argv) > 4 else 3)
        elif test_name == "send_message" and len(sys.argv) > 3:
            test_send_message(sys.argv[2], sys.argv[3])
        elif test_name == "send_file" and len(sys.argv) > 3:
            test_send_file(sys.argv[2], sys.argv[3])
        elif test_name == "send_audio_message" and len(sys.argv) > 3:
            test_send_audio_message(sys.argv[2], sys.argv[3])
        elif test_name == "download_media" and len(sys.argv) > 3:
            test_download_media(sys.argv[2], sys.argv[3])
        else:
            print(f"Unknown test: {test_name}")
            print("Usage: python test_tools.py [test_name] [args...]")
    else:
        # Run all tests
        run_all_tests()

