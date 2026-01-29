import json
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from fastapi import HTTPException

from ..models.conversation import Conversation, Message, RoleType
from ..models.user import User
from ..services.agent_service import AgentService


class ChatService:
    def __init__(self):
        self.agent_service = AgentService()

    async def process_chat_message(
        self,
        session: Session,  # Database session parameter
        user_id: uuid.UUID,
        message: str,
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a chat message from a user and return AI response.
        """
        # Get or create conversation
        if conversation_id:
            conversation = self._get_conversation_by_id_from_session(session, conversation_id)
            if not conversation or conversation.user_id != user_id:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            conversation = self._create_new_conversation_in_session(session, user_id, message)

        # Save user message
        user_message = Message(
            conversation_id=conversation.id,
            role=RoleType.user,
            content=message,
            timestamp=datetime.utcnow()
        )
        session.add(user_message)
        session.commit()
        session.refresh(user_message)

        # Process with AI agent - pass the database session for consistency
        agent_response = await self.agent_service.process_message(
            user_message=user_message.content,
            user_id=user_id,
            conversation_id=str(conversation.id),
            db_session=session  # Pass the current session for consistency
        )

        # After agent processing, make sure to commit the session to persist any changes made by tools
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

        # Save AI response
        ai_message = Message(
            conversation_id=conversation.id,
            role=RoleType.assistant,
            content=agent_response['response'],
            timestamp=datetime.utcnow()
        )
        session.add(ai_message)
        session.commit()

        # Update conversation timestamp
        conversation.updated_at = datetime.utcnow()
        if not conversation.title:
            conversation.title = message[:50] + "..." if len(message) > 50 else message
        session.commit()

        return {
            "conversation_id": str(conversation.id),
            "message_id": str(ai_message.id),
            "response": agent_response['response'],
            "timestamp": ai_message.timestamp,
            "tool_calls": agent_response.get('tool_calls', []),
            "error": None
        }

    async def get_user_conversations(self, session: Session, user_id: uuid.UUID) -> List[Dict[str, Any]]:
        """
        Retrieve all conversations for a user.
        """
        conversations = session.query(Conversation).filter(
            Conversation.user_id == user_id
        ).order_by(Conversation.updated_at.desc()).all()

        return [
            {
                "id": str(conv.id),
                "title": conv.title,
                "created_at": conv.created_at,
                "updated_at": conv.updated_at,
            }
            for conv in conversations
        ]

    async def get_conversation_messages(
        self,
        session: Session,
        conversation_id: str,
        user_id: uuid.UUID
    ) -> Dict[str, Any]:
        """
        Retrieve all messages in a specific conversation.
        """
        # Verify conversation belongs to user
        conversation = self._get_conversation_by_id_from_session(session, conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise HTTPException(status_code=404, detail="Conversation not found")

        messages = session.query(Message).filter(
            Message.conversation_id == uuid.UUID(conversation_id)
        ).order_by(Message.timestamp.asc()).all()

        return {
            "conversation_id": conversation_id,
            "messages": [
                {
                    "id": str(msg.id),
                    "role": msg.role.value,
                    "content": msg.content,
                    "timestamp": msg.timestamp,
                    "metadata": {}
                }
                for msg in messages
            ]
        }

    async def delete_conversation(
        self,
        session: Session,
        conversation_id: str,
        user_id: uuid.UUID
    ) -> Dict[str, Any]:
        """
        Delete a conversation and all its messages.
        """
        # Verify conversation belongs to user
        conversation = self._get_conversation_by_id_from_session(session, conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise HTTPException(status_code=404, detail="Conversation not found")

        # Count messages to return in response
        messages_count = session.query(Message).filter(
            Message.conversation_id == uuid.UUID(conversation_id)
        ).count()

        # Delete messages first (due to foreign key constraint)
        session.query(Message).filter(
            Message.conversation_id == uuid.UUID(conversation_id)
        ).delete()

        # Delete conversation
        session.delete(conversation)
        session.commit()

        return {
            "success": True,
            "deleted_messages_count": messages_count
        }

    def _get_conversation_by_id_from_session(self, session: Session, conversation_id: str) -> Optional[Conversation]:
        """
        Helper method to get conversation by ID from a session.
        """
        try:
            uuid_obj = uuid.UUID(conversation_id)
            return session.query(Conversation).filter(
                Conversation.id == uuid_obj
            ).first()
        except ValueError:
            return None

    def _create_new_conversation_in_session(self, session: Session, user_id: uuid.UUID, first_message: str) -> Conversation:
        """
        Helper method to create a new conversation in a session.
        """
        conversation = Conversation(
            user_id=user_id,
            thread_id=str(uuid.uuid4()),  # Generate a new thread ID
            title=first_message[:50] + "..." if len(first_message) > 50 else first_message,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        # Add to session and commit
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

        return conversation