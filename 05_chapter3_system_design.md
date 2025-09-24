# Chapter 3 – System Design

## 3.1 Use Case Diagram

```plantuml
@startuml YouTube_Video_Summarizer_Use_Cases

!define RECTANGLE class

actor User as U
actor "YouTube API" as YT
actor "Google AI Service" as AI

rectangle "YouTube Video Summarizer System" {
    usecase "Register Account" as UC1
    usecase "Login/Logout" as UC2
    usecase "Submit YouTube URL" as UC3
    usecase "Process Video" as UC4
    usecase "Generate Summary" as UC5
    usecase "Chat with Video Content" as UC6
    usecase "View Chat History" as UC7
    usecase "Manage Video Library" as UC8
    usecase "Configure Preferences" as UC9
    usecase "Extract Video Info" as UC10
    usecase "Fetch Transcripts" as UC11
    usecase "Create Embeddings" as UC12
    usecase "Generate AI Response" as UC13
}

' User interactions
U --> UC1
U --> UC2
U --> UC3
U --> UC6
U --> UC7
U --> UC8
U --> UC9

' System internal processes
UC3 --> UC4
UC4 --> UC10
UC4 --> UC11
UC4 --> UC5
UC5 --> UC12
UC6 --> UC13

' External service interactions
UC10 --> YT : <<include>>
UC11 --> YT : <<include>>
UC5 --> AI : <<include>>
UC13 --> AI : <<include>>

' Relationships
UC2 --> UC3 : <<precedes>>
UC4 --> UC5 : <<include>>
UC12 --> UC6 : <<precedes>>

@enduml
```

### 3.1.1 Use Case Descriptions

| Use Case ID | Use Case Name           | Description                                        | Actors             | Preconditions       |
| ----------- | ----------------------- | -------------------------------------------------- | ------------------ | ------------------- |
| UC1         | Register Account        | User creates a new account with email and password | User               | None                |
| UC2         | Login/Logout            | User authenticates and manages session             | User               | Account exists      |
| UC3         | Submit YouTube URL      | User provides YouTube video URL for processing     | User               | User logged in      |
| UC4         | Process Video           | System processes video information and transcripts | System             | Valid URL provided  |
| UC5         | Generate Summary        | System creates AI-powered summary of video content | System, AI Service | Video processed     |
| UC6         | Chat with Video Content | User asks questions about video content            | User, AI Service   | Summary available   |
| UC7         | View Chat History       | User accesses previous conversations               | User               | Chat history exists |
| UC8         | Manage Video Library    | User views and manages processed videos            | User               | User logged in      |
| UC9         | Configure Preferences   | User sets language and model preferences           | User               | User logged in      |

## 3.2 Sequence Diagram

```plantuml
@startuml Video_Processing_Sequence

participant "User" as U
participant "Frontend" as F
participant "Auth Service" as A
participant "Video Service" as V
participant "YouTube API" as YT
participant "AI Service" as AI
participant "Vector Store" as VS
participant "Database" as DB

U -> F: Submit YouTube URL
F -> A: Verify Authentication
A -> F: Authentication Confirmed

F -> V: Process Video Request
V -> YT: Fetch Video Information
YT -> V: Return Metadata

V -> YT: Request Transcripts
YT -> V: Return Transcript Data

V -> DB: Store Video Information
DB -> V: Confirm Storage

V -> AI: Generate Summary
AI -> V: Return Summary

V -> VS: Create Embeddings
VS -> V: Confirm Embeddings

V -> DB: Update Processing Status
DB -> V: Confirm Update

V -> F: Processing Complete
F -> U: Display Results

note right of U: User can now chat\nwith video content

U -> F: Ask Question about Video
F -> VS: Search Similar Content
VS -> F: Return Relevant Chunks

F -> AI: Generate Response
AI -> F: Return Answer

F -> DB: Store Chat Message
DB -> F: Confirm Storage

F -> U: Display Response

@enduml
```

## 3.3 Activity Diagram

```plantuml
@startuml Video_Processing_Activity

start

:User submits YouTube URL;

if (URL valid?) then (yes)
    :Extract video ID;
    :Fetch video metadata;

    if (Video accessible?) then (yes)
        :Retrieve available transcripts;

        if (Transcripts available?) then (yes)
            :Process transcripts for each language;
            :Generate AI summary;
            :Create vector embeddings;
            :Store in database;
            :Notify user of completion;
        else (no)
            :Generate error message;
            :Notify user - no transcripts;
        endif

    else (no)
        :Generate error message;
        :Notify user - video not accessible;
    endif

else (no)
    :Generate error message;
    :Notify user - invalid URL;
endif

:Update video status;

if (User wants to chat?) then (yes)
    repeat
        :User asks question;
        :Search vector store;
        :Generate AI response;
        :Display response to user;
        :Store chat message;
    repeat while (Continue chatting?)
endif

stop

@enduml
```

## 3.4 Class Diagram

```plantuml
@startuml YouTube_Summarizer_Classes

class User {
    +id: str
    +email: str
    +password_hash: str
    +preferred_language: str
    +preferred_model: str
    +created_at: datetime
    +last_login: datetime
    +total_videos: int
    +account_type: str
    +is_verified: bool
    --
    +authenticate(password): bool
    +update_preferences(prefs): void
    +get_chat_history(): List[Chat]
}

class Video {
    +id: str
    +youtube_id: str
    +title: str
    +thumbnail_url: str
    +transcripts: Dict[str, List]
    +default_language: str
    +available_languages: List[str]
    +status: str
    +vector_ids: Dict[str, List[str]]
    +created_at: datetime
    +duration_seconds: int
    +uploader: str
    --
    +extract_metadata(): void
    +fetch_transcripts(): void
    +generate_summary(): str
    +create_embeddings(): void
}

class Chat {
    +id: str
    +user_id: str
    +video_id: str
    +messages: List[Message]
    +created_at: datetime
    +updated_at: datetime
    +is_active: bool
    --
    +add_message(message): void
    +get_context(): str
    +archive_chat(): void
}

class Message {
    +id: str
    +chat_id: str
    +content: str
    +sender: str
    +timestamp: datetime
    +message_type: str
    --
    +format_content(): str
    +validate_content(): bool
}

class VideoService {
    +embedding_store: VideoEmbeddingStore
    --
    +process_video(url): Video
    +extract_video_info(youtube_id): Dict
    +fetch_transcripts(youtube_id): Dict
    +generate_summary(video): str
}

class RAGService {
    +llm: ChatGoogleGenerativeAI
    +temperature: float
    --
    +build_chain(retriever, history): Chain
    +generate_response(query, context): str
    +process_chat(video_id, question, history): str
}

class AuthService {
    +secret_key: str
    +algorithm: str
    --
    +create_user(email, password): User
    +authenticate_user(email, password): User
    +create_token(user): str
    +verify_token(token): User
}

class VideoEmbeddingStore {
    +embedding_model: GoogleGenerativeAIEmbeddings
    +vs: Chroma
    --
    +add_video_embeddings(video_data): List[str]
    +search_similar(query, video_id): List[Document]
    +delete_embeddings(video_id): bool
}

class YouTubeInfoExtractor {
    --
    +extract_info(url): Dict
    +get_video_id(url): str
    +validate_url(url): bool
}

class YouTubeTranscriber {
    --
    +get_transcript(video_id, languages): Dict
    +get_available_languages(video_id): List[str]
    +translate_transcript(transcript, target_lang): List
}

' Relationships
User ||--o{ Chat : "has many"
Video ||--o{ Chat : "referenced in"
Chat ||--o{ Message : "contains"
User }o--|| AuthService : "authenticated by"
Video }o--|| VideoService : "processed by"
Chat }o--|| RAGService : "responses generated by"
VideoService *-- VideoEmbeddingStore : "uses"
VideoService *-- YouTubeInfoExtractor : "uses"
VideoService *-- YouTubeTranscriber : "uses"
VideoEmbeddingStore *-- "Chroma" : "stores in"

@enduml
```

## 3.5 Database Schema

### 3.5.1 MongoDB Collections

#### Users Collection

```javascript
{
  "_id": ObjectId,
  "email": String, // Unique index
  "password_hash": String,
  "preferred_language": String, // Default: "en"
  "preferred_model": String, // Default: "gemini-2.0-flash"
  "profile": {
    "display_name": String,
    "bio": String,
    "avatar_url": String,
    "timezone": String,
    "notification_settings": Object
  },
  "created_at": ISODate,
  "last_login": ISODate,
  "total_videos": Number, // Default: 0
  "account_type": String, // Default: "free"
  "is_verified": Boolean // Default: false
}
```

#### Videos Collection

```javascript
{
  "_id": ObjectId,
  "youtube_id": String, // Unique index
  "title": String,
  "description": String,
  "thumbnail_url": String,
  "duration_seconds": Number,
  "view_count": Number,
  "uploader": String,
  "channel_url": String,
  "transcripts": {
    "en": [
      {
        "text": String,
        "start": Number,
        "duration": Number
      }
    ],
    "es": [...],
    // More languages
  },
  "default_language": String,
  "available_languages": [String],
  "status": String, // "pending", "processing", "completed", "failed"
  "processing_error": String,
  "vector_ids": {
    "en": [String], // ChromaDB document IDs
    "es": [String],
    // More languages
  },
  "created_at": ISODate,
  "updated_at": ISODate,
  "processed_at": ISODate
}
```

#### Chats Collection

```javascript
{
  "_id": ObjectId,
  "user_id": ObjectId, // Reference to Users collection
  "video_id": ObjectId, // Reference to Videos collection
  "title": String,
  "messages": [
    {
      "id": String,
      "content": String,
      "sender": String, // "user" or "assistant"
      "timestamp": ISODate,
      "message_type": String // "text", "summary", "error"
    }
  ],
  "created_at": ISODate,
  "updated_at": ISODate,
  "is_active": Boolean,
  "language": String
}
```

#### Video User Uploads Collection

```javascript
{
  "_id": ObjectId,
  "user_id": ObjectId, // Reference to Users collection
  "video_id": ObjectId, // Reference to Videos collection
  "uploaded_at": ISODate
}
```

### 3.5.2 ChromaDB Collections

#### Video Embeddings Collection

```python
{
  "id": "youtube_id_chunk_index_lang", # Unique document ID
  "embedding": [float], # 768-dimensional vector
  "metadata": {
    "youtube_id": str,
    "lang": str,
    "field": str, # "title", "description", "transcript"
    "chunk_index": int,
    "start_time": float, # For transcript chunks
    "end_time": float,   # For transcript chunks
    "content_type": str  # "metadata" or "transcript"
  },
  "document": str # Original text content
}
```

### 3.5.3 Database Indexes

#### MongoDB Indexes

```javascript
// Users Collection
db.users.createIndex({ email: 1 }, { unique: true });
db.users.createIndex({ created_at: 1 });

// Videos Collection
db.videos.createIndex({ youtube_id: 1 }, { unique: true });
db.videos.createIndex({ status: 1 });
db.videos.createIndex({ created_at: 1 });
db.videos.createIndex({ uploader: 1 });

// Chats Collection
db.chats.createIndex({ user_id: 1 });
db.chats.createIndex({ video_id: 1 });
db.chats.createIndex({ user_id: 1, video_id: 1 });
db.chats.createIndex({ created_at: 1 });

// Video User Uploads Collection
db.video_user_uploads.createIndex({ user_id: 1 });
db.video_user_uploads.createIndex({ video_id: 1 });
db.video_user_uploads.createIndex({ user_id: 1, uploaded_at: 1 });
```

## 3.6 Data Flow Diagrams

### 3.6.1 DFD Level 0 (Context Diagram)

```mermaid
graph TB
    User[User]
    System[YouTube Video Summarizer System]
    YouTube[YouTube API]
    GoogleAI[Google AI Service]

    User -->|YouTube URLs, Queries| System
    System -->|Summaries, Responses| User
    System -->|Video Requests| YouTube
    YouTube -->|Video Data, Transcripts| System
    System -->|Text for Processing| GoogleAI
    GoogleAI -->|Summaries, Embeddings| System
```

### 3.6.2 DFD Level 1 (Major Processes)

```mermaid
graph TB
    User[User]

    subgraph "YouTube Video Summarizer System"
        P1[1.0 User Management]
        P2[2.0 Video Processing]
        P3[3.0 AI Analysis]
        P4[4.0 Chat Management]
        P5[5.0 Vector Storage]

        D1[(User Database)]
        D2[(Video Database)]
        D3[(Chat Database)]
        D4[(Vector Database)]
    end

    YouTube[YouTube API]
    GoogleAI[Google AI Service]

    User -->|Registration/Login| P1
    User -->|YouTube URLs| P2
    User -->|Chat Messages| P4

    P1 -->|User Data| D1
    P1 -->|Authentication| User

    P2 -->|Video Metadata| YouTube
    YouTube -->|Video Info/Transcripts| P2
    P2 -->|Video Data| D2
    P2 -->|Text Content| P3

    P3 -->|Processing Request| GoogleAI
    GoogleAI -->|Summaries/Embeddings| P3
    P3 -->|Embeddings| P5
    P3 -->|Summaries| D2

    P4 -->|Query Context| P5
    P5 -->|Relevant Content| P4
    P4 -->|AI Request| GoogleAI
    GoogleAI -->|Response| P4
    P4 -->|Chat Data| D3
    P4 -->|Responses| User

    P5 -->|Embeddings| D4
```

### 3.6.3 DFD Level 2 (Video Processing Detail)

```mermaid
graph TB
    User[User]
    YouTube[YouTube API]
    GoogleAI[Google AI Service]

    subgraph "2.0 Video Processing"
        P21[2.1 URL Validation]
        P22[2.2 Info Extraction]
        P23[2.3 Transcript Fetching]
        P24[2.4 Content Processing]
        P25[2.5 Status Management]
    end

    D2[(Video Database)]
    D4[(Vector Database)]

    User -->|YouTube URL| P21
    P21 -->|Valid URL| P22
    P21 -->|Invalid URL| User

    P22 -->|Video ID| YouTube
    YouTube -->|Metadata| P22
    P22 -->|Video Info| P23
    P22 -->|Basic Data| D2

    P23 -->|Transcript Request| YouTube
    YouTube -->|Transcript Data| P23
    P23 -->|Complete Data| P24

    P24 -->|Text Content| GoogleAI
    GoogleAI -->|Summary| P24
    P24 -->|Processed Data| D2
    P24 -->|Embeddings| D4

    P25 -->|Status Updates| D2
    P25 -->|Notifications| User
```

## 3.7 System Architecture Diagram

```mermaid
graph TB
    subgraph "Frontend Layer"
        UI[Next.js Frontend]
        Auth[Authentication UI]
        Video[Video Interface]
        Chat[Chat Interface]
    end

    subgraph "API Gateway Layer"
        Gateway[FastAPI Gateway]
        CORS[CORS Middleware]
        Auth_MW[Auth Middleware]
        Rate[Rate Limiting]
    end

    subgraph "Service Layer"
        AuthSvc[Authentication Service]
        VideoSvc[Video Service]
        ChatSvc[Chat Service]
        RAGSvc[RAG Service]
    end

    subgraph "Data Layer"
        MongoDB[(MongoDB)]
        ChromaDB[(ChromaDB)]
        Redis[(Redis Cache)]
    end

    subgraph "External Services"
        YouTube_API[YouTube API]
        Google_AI[Google AI Service]
        Worker[Background Workers]
    end

    subgraph "Infrastructure"
        Docker[Docker Containers]
        Load_Balancer[Load Balancer]
        Monitor[Monitoring]
    end

    UI --> Gateway
    Gateway --> AuthSvc
    Gateway --> VideoSvc
    Gateway --> ChatSvc

    VideoSvc --> YouTube_API
    ChatSvc --> RAGSvc
    RAGSvc --> Google_AI
    VideoSvc --> Worker

    AuthSvc --> MongoDB
    VideoSvc --> MongoDB
    ChatSvc --> MongoDB
    RAGSvc --> ChromaDB

    Worker --> MongoDB
    Worker --> ChromaDB

    Gateway --> Redis

    Docker --> Load_Balancer
    Monitor --> Docker
```

## 3.8 Security Architecture

### 3.8.1 Authentication Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant AuthAPI
    participant Database
    participant JWT

    User->>Frontend: Login Request
    Frontend->>AuthAPI: POST /api/auth/login
    AuthAPI->>Database: Verify Credentials
    Database->>AuthAPI: User Data
    AuthAPI->>JWT: Generate Token
    JWT->>AuthAPI: Access Token
    AuthAPI->>Frontend: Token Response
    Frontend->>User: Login Success

    Note over Frontend: Store token securely

    User->>Frontend: API Request
    Frontend->>AuthAPI: Request with Bearer Token
    AuthAPI->>JWT: Validate Token
    JWT->>AuthAPI: Token Valid
    AuthAPI->>Frontend: API Response
```

### 3.8.2 Security Measures

| Layer            | Security Measure   | Implementation                        |
| ---------------- | ------------------ | ------------------------------------- |
| Transport        | HTTPS/TLS 1.3      | SSL certificates, secure headers      |
| Authentication   | JWT + bcrypt       | Token-based auth, password hashing    |
| Authorization    | Role-based access  | User permissions, resource protection |
| Input Validation | Pydantic models    | Request/response validation           |
| Rate Limiting    | Token bucket       | API endpoint protection               |
| Data Protection  | Encryption at rest | Database encryption, secure storage   |
| Monitoring       | Audit logging      | Security event tracking               |
| CORS             | Origin control     | Cross-origin request management       |

## 3.9 Performance Architecture

### 3.9.1 Caching Strategy

```mermaid
graph TB
    User[User Request]
    Cache[Redis Cache]
    API[API Server]
    DB[(Database)]

    User -->|Request| Cache
    Cache -->|Cache Miss| API
    API -->|Query| DB
    DB -->|Data| API
    API -->|Response| Cache
    Cache -->|Cached Response| User

    User -->|Subsequent Request| Cache
    Cache -->|Cache Hit| User
```

### 3.9.2 Scalability Design

| Component          | Scaling Strategy    | Implementation                    |
| ------------------ | ------------------- | --------------------------------- |
| API Server         | Horizontal scaling  | Load balancer, multiple instances |
| Database           | Sharding/Clustering | MongoDB replica sets              |
| Vector Store       | Distributed storage | ChromaDB clustering               |
| Background Workers | Queue-based scaling | Worker pool management            |
| Frontend           | CDN distribution    | Static asset caching              |
| AI Processing      | Batch processing    | Asynchronous task queues          |
