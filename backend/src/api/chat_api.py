from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import uuid

from ..middleware.auth import get_current_user
from ..services.chat_service import ChatService
from ..models.user import User
from ..database.database import get_session
from ..schemas.chat import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Main chat endpoint for the AI chatbot.
    Handles user messages and returns AI responses.
    """
    try:
        # Initialize chat service
        chat_service = ChatService()

        # Process the chat request
        response = await chat_service.process_chat_message(
            session=db,  # Pass the session
            user_id=current_user.id,
            message=request.message,
            conversation_id=request.conversation_id
        )

        return response

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat request: {str(e)}"
        )


@router.get("/conversations")
async def get_user_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Retrieve all conversations for the authenticated user.
    """
    try:
        chat_service = ChatService()
        conversations = await chat_service.get_user_conversations(db, current_user.id)
        return conversations
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving conversations: {str(e)}"
        )


@router.get("/conversations/{conversation_id}/messages")
async def get_conversation_messages(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Retrieve all messages in a specific conversation.
    """
    try:
        # Validate conversation_id is a valid UUID
        try:
            uuid.UUID(conversation_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid conversation ID format"
            )

        chat_service = ChatService()
        messages = await chat_service.get_conversation_messages(
            session=db,
            conversation_id=conversation_id,
            user_id=current_user.id
        )
        return messages
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving messages: {str(e)}"
        )


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Delete a specific conversation and all its messages.
    """
    try:
        # Validate conversation_id is a valid UUID
        try:
            uuid.UUID(conversation_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid conversation ID format"
            )

        chat_service = ChatService()
        result = await chat_service.delete_conversation(
            session=db,
            conversation_id=conversation_id,
            user_id=current_user.id
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting conversation: {str(e)}"
        )