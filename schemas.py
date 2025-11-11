"""
Database Schemas for Math Club

Each Pydantic model represents a MongoDB collection. The collection name is the
lowercase of the class name (e.g., Event -> "event").
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

class Event(BaseModel):
    """Events hosted by the Math Club"""
    title: str = Field(..., description="Event title")
    date: str = Field(..., description="Event date in YYYY-MM-DD format")
    time: Optional[str] = Field(None, description="Event time, e.g., 3:30 PM - 4:30 PM")
    location: Optional[str] = Field(None, description="Where the event takes place")
    description: Optional[str] = Field(None, description="Short description of the event")
    link: Optional[str] = Field(None, description="Optional registration or info link")

class Announcement(BaseModel):
    """Announcements to display on the site"""
    message: str = Field(..., description="Announcement text")
    priority: int = Field(1, ge=1, le=5, description="1=low, 5=high priority")
    visible: bool = Field(True, description="Whether to show this announcement")

class ContactMessage(BaseModel):
    """Messages submitted from the contact form"""
    name: str = Field(..., description="Sender name")
    email: EmailStr = Field(..., description="Sender email")
    subject: str = Field(..., description="Message subject")
    message: str = Field(..., description="Message body")

class Officer(BaseModel):
    """Officer profiles (optional content)"""
    name: str
    role: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

# You can add more models like Resource, CompetitionResult, etc., as needed.
