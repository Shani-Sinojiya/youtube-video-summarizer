# Chapter 3 – System Design

## 3.1 Use Case Diagrams

### 3.1.1 User Authentication Use Cases

```plantuml
@startuml User_Authentication_Use_Cases

actor User as U

rectangle "Authentication System" {
    usecase "Register Account" as UC1
    usecase "Login / Logout" as UC2
    usecase "Configure Preferences" as UC9
}

U --> UC1
U --> UC2
U --> UC9

UC2 --> UC1 : <<extends>>

@enduml
```

### 3.1.2 Video Processing Use Cases

```plantuml
@startuml Video_Processing_Use_Cases

actor User as U
actor "YouTube API" as YT
actor "Google AI Service" as AI

rectangle "Video Processing System" {
    usecase "Submit YouTube URL" as UC3
    usecase "Process Video" as UC4
    usecase "Extract Video Info" as UC10
    usecase "Fetch Transcripts" as UC11
    usecase "Generate Summary" as UC5
    usecase "Create Embeddings" as UC12
}

U --> UC3
UC3 --> UC4
UC4 --> UC10
UC4 --> UC11
UC4 --> UC5
UC5 --> UC12

UC10 --> YT : <<include>>
UC11 --> YT : <<include>>
UC5 --> AI : <<include>>

@enduml
```

### 3.1.3 Chat and Library Management Use Cases

```plantuml
@startuml Chat_Library_Use_Cases

actor User as U
actor "Google AI Service" as AI

rectangle "Chat and Library System" {
    usecase "Chat with Video Content" as UC6
    usecase "Generate AI Response" as UC13
    usecase "View Chat History" as UC7
    usecase "Manage Video Library" as UC8
}

U --> UC6
U --> UC7
U --> UC8
UC6 --> UC13

UC13 --> AI : <<include>>

@enduml
```

### 3.1.4 Use Case Descriptions

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

## 3.2 Sequence Diagrams

### 3.2.1 Video Processing Sequence

```plantuml
@startuml Video_Processing_Sequence

participant "User" as U
participant "Frontend" as F
participant "Auth Service" as A
participant "Video Service" as V
participant "YouTube API" as YT
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

V -> F: Video Processing Complete
F -> U: Display Processing Status

@enduml
```

### 3.2.2 AI Processing Sequence

```plantuml
@startuml AI_Processing_Sequence

participant "Video Service" as V
participant "AI Service" as AI
participant "Vector Store" as VS
participant "Database" as DB

V -> AI: Generate Summary Request
AI -> V: Return Summary

V -> AI: Create Embeddings Request
AI -> V: Return Vector Embeddings

V -> VS: Store Embeddings
VS -> V: Confirm Storage

V -> DB: Update Processing Status
DB -> V: Confirm Update

@enduml
```

### 3.2.3 Chat Interaction Sequence

```plantuml
@startuml Chat_Interaction_Sequence

participant "User" as U
participant "Frontend" as F
participant "Chat Service" as C
participant "Vector Store" as VS
participant "AI Service" as AI
participant "Database" as DB

U -> F: Ask Question about Video
F -> C: Process Chat Request
C -> VS: Search Similar Content
VS -> C: Return Relevant Chunks

C -> AI: Generate Response with Context
AI -> C: Return Answer

C -> DB: Store Chat Message
DB -> C: Confirm Storage

C -> F: Return Response
F -> U: Display Answer

@enduml
```

## 3.3 Activity Diagrams

### 3.3.1 Video Submission and Validation Activity

```plantuml
@startuml Video_Submission_Activity

start

:User submits YouTube URL;

if (URL valid?) then (yes)
    :Extract video ID;
    :Fetch video metadata;

    if (Video accessible?) then (yes)
        :Continue to processing;
    else (no)
        :Generate error message;
        :Notify user - video not accessible;
        stop
    endif
else (no)
    :Generate error message;
    :Notify user - invalid URL;
    stop
endif

stop

@enduml
```

### 3.3.2 Video Processing Activity

```plantuml
@startuml Video_Processing_Activity

start

:Retrieve available transcripts;

if (Transcripts available?) then (yes)
    :Process transcripts for each language;
    :Generate AI summary;
    :Create vector embeddings;
    :Store in database;
    :Update video status to completed;
    :Notify user of completion;
else (no)
    :Update video status to failed;
    :Generate error message;
    :Notify user - no transcripts;
endif

stop

@enduml
```

### 3.3.3 Chat Interaction Activity

```plantuml
@startuml Chat_Interaction_Activity

start

if (User wants to chat?) then (yes)
    repeat
        :User asks question;
        :Search vector store for relevant content;
        :Generate AI response with context;
        :Display response to user;
        :Store chat message in database;
    repeat while (Continue chatting?)
    :End chat session;
else (no)
    :User exits;
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

Perfect 👍 To build the **Data Dictionary** from your schema, we’ll list each collection, its fields, data type, description, constraints (like _unique, default, reference_), and possible values.

Here’s a full **Data Dictionary** for your system:

---

# 3.5 📘 Data Dictionary

## 3.5.1 MongoDB Collections

---

### **3.5.1.1 Users Collection**

| Field                           | Data Type | Description                                          | Constraints / Default         |
| ------------------------------- | --------- | ---------------------------------------------------- | ----------------------------- |
| `_id`                           | ObjectId  | Unique identifier for each user                      | Auto-generated                |
| `email`                         | String    | User’s email                                         | Unique, required              |
| `password_hash`                 | String    | Hashed password                                      | Required                      |
| `preferred_language`            | String    | User’s preferred language for transcripts/chat       | Default: `"en"`               |
| `preferred_model`               | String    | Preferred AI model                                   | Default: `"gemini-2.0-flash"` |
| `profile.display_name`          | String    | User’s display name                                  | Optional                      |
| `profile.bio`                   | String    | Short bio                                            | Optional                      |
| `profile.avatar_url`            | String    | Profile picture URL                                  | Optional                      |
| `profile.timezone`              | String    | User’s timezone                                      | Optional                      |
| `profile.notification_settings` | Object    | User’s notification preferences                      | Optional                      |
| `created_at`                    | ISODate   | Account creation timestamp                           | Auto-set                      |
| `last_login`                    | ISODate   | Last login timestamp                                 | Updated per login             |
| `total_videos`                  | Number    | Number of videos processed by user                   | Default: 0                    |
| `account_type`                  | String    | Account type (`"free"`, `"premium"`, `"enterprise"`) | Default: `"free"`             |
| `is_verified`                   | Boolean   | Email verification status                            | Default: `false`              |

---

### **3.5.1.2 Videos Collection**

| Field                 | Data Type | Description                                                                      | Constraints / Default |
| --------------------- | --------- | -------------------------------------------------------------------------------- | --------------------- |
| `_id`                 | ObjectId  | Unique identifier for each video                                                 | Auto-generated        |
| `youtube_id`          | String    | YouTube video ID                                                                 | Unique, required      |
| `title`               | String    | Video title                                                                      | Required              |
| `description`         | String    | Video description                                                                | Optional              |
| `thumbnail_url`       | String    | URL of video thumbnail                                                           | Optional              |
| `duration_seconds`    | Number    | Video duration in seconds                                                        | Optional              |
| `view_count`          | Number    | YouTube view count at processing                                                 | Optional              |
| `uploader`            | String    | Uploader’s name                                                                  | Optional              |
| `channel_url`         | String    | YouTube channel URL                                                              | Optional              |
| `transcripts`         | Object    | Transcript data in multiple languages                                            | Key = language code   |
| `default_language`    | String    | Primary transcript language                                                      | Required              |
| `available_languages` | [String]  | List of supported languages                                                      | Optional              |
| `status`              | String    | Video processing status (`"pending"`, `"processing"`, `"completed"`, `"failed"`) | Default: `"pending"`  |
| `processing_error`    | String    | Error details if failed                                                          | Optional              |
| `vector_ids`          | Object    | Mapping of language → vector IDs in ChromaDB                                     | Optional              |
| `created_at`          | ISODate   | Video submission timestamp                                                       | Auto-set              |
| `updated_at`          | ISODate   | Last updated timestamp                                                           | Auto-set              |
| `processed_at`        | ISODate   | When processing finished                                                         | Optional              |

---

### **3.5.1.3 Chats Collection**

| Field                     | Data Type | Description                        | Constraints / Default |
| ------------------------- | --------- | ---------------------------------- | --------------------- |
| `_id`                     | ObjectId  | Unique chat ID                     | Auto-generated        |
| `user_id`                 | ObjectId  | Reference to **Users** collection  | Required              |
| `video_id`                | ObjectId  | Reference to **Videos** collection | Required              |
| `title`                   | String    | Chat session title                 | Optional              |
| `messages[].id`           | String    | Unique message ID                  | Required              |
| `messages[].content`      | String    | Message text                       | Required              |
| `messages[].sender`       | String    | `"user"` or `"assistant"`          | Required              |
| `messages[].timestamp`    | ISODate   | When the message was sent          | Auto-set              |
| `messages[].message_type` | String    | `"text"`, `"summary"`, `"error"`   | Required              |
| `created_at`              | ISODate   | Chat creation timestamp            | Auto-set              |
| `updated_at`              | ISODate   | Last updated timestamp             | Auto-set              |
| `is_active`               | Boolean   | Chat active/inactive               | Default: `true`       |
| `language`                | String    | Chat language                      | Default: `"en"`       |

---

### **3.5.1.4 Video User Uploads Collection**

| Field         | Data Type | Description                        | Constraints / Default |
| ------------- | --------- | ---------------------------------- | --------------------- |
| `_id`         | ObjectId  | Unique ID for upload record        | Auto-generated        |
| `user_id`     | ObjectId  | Reference to **Users** collection  | Required              |
| `video_id`    | ObjectId  | Reference to **Videos** collection | Required              |
| `uploaded_at` | ISODate   | Timestamp of upload                | Auto-set              |

---

## 3.5.2 ChromaDB Collections

---

### **3.5.2.1 Video Embeddings Collection**

| Field                   | Data Type | Description                                             | Constraints / Default |
| ----------------------- | --------- | ------------------------------------------------------- | --------------------- |
| `id`                    | String    | Unique embedding ID (`youtube_id_chunk_index_lang`)     | Unique, required      |
| `embedding`             | [Float]   | 768-dimensional vector                                  | Required              |
| `metadata.youtube_id`   | String    | Reference to YouTube video ID                           | Required              |
| `metadata.lang`         | String    | Language code (e.g., `"en"`, `"es"`)                    | Required              |
| `metadata.field`        | String    | Field type (`"title"`, `"description"`, `"transcript"`) | Required              |
| `metadata.chunk_index`  | Int       | Index of chunk                                          | Required              |
| `metadata.start_time`   | Float     | Start timestamp (for transcript chunks)                 | Optional              |
| `metadata.end_time`     | Float     | End timestamp (for transcript chunks)                   | Optional              |
| `metadata.content_type` | String    | `"metadata"` or `"transcript"`                          | Required              |
| `document`              | String    | Original text content                                   | Required              |

Got it! I’ll help you create a **well-documented and structured MongoDB index section** for your project, making it readable, maintainable, and professional. Here’s a polished version:

---

## 3.5.3 Database Indexes

Indexes are critical for improving query performance in MongoDB. Below is a detailed list of indexes for each collection, along with their purpose.

---

### **3.5.3.1 Users Collection**

| Index               | Type      | Purpose                                                                                                          |
| ------------------- | --------- | ---------------------------------------------------------------------------------------------------------------- |
| `{ email: 1 }`      | Unique    | Ensures that each user has a unique email and accelerates login/authentication queries.                          |
| `{ created_at: 1 }` | Ascending | Optimizes queries that sort or filter users based on creation date (e.g., reporting or user activity analytics). |

```javascript
db.users.createIndex({ email: 1 }, { unique: true });
db.users.createIndex({ created_at: 1 });
```

---

### **3.5.3.2 Videos Collection**

| Index               | Type      | Purpose                                                                                                         |
| ------------------- | --------- | --------------------------------------------------------------------------------------------------------------- |
| `{ youtube_id: 1 }` | Unique    | Guarantees that each YouTube video is stored only once. Speeds up video retrieval.                              |
| `{ status: 1 }`     | Ascending | Speeds up queries filtering videos by their processing status (`pending`, `processing`, `completed`, `failed`). |
| `{ created_at: 1 }` | Ascending | Optimizes queries sorting or filtering videos by upload date.                                                   |
| `{ uploader: 1 }`   | Ascending | Optimizes queries that fetch all videos uploaded by a particular user.                                          |

```javascript
db.videos.createIndex({ youtube_id: 1 }, { unique: true });
db.videos.createIndex({ status: 1 });
db.videos.createIndex({ created_at: 1 });
db.videos.createIndex({ uploader: 1 });
```

---

### **3.5.3.3 Chats Collection**

| Index                         | Type      | Purpose                                                                   |
| ----------------------------- | --------- | ------------------------------------------------------------------------- |
| `{ user_id: 1 }`              | Ascending | Optimizes queries fetching all chats by a specific user.                  |
| `{ video_id: 1 }`             | Ascending | Optimizes queries fetching all chats related to a specific video.         |
| `{ user_id: 1, video_id: 1 }` | Compound  | Speeds up queries fetching chats for a specific video by a specific user. |
| `{ created_at: 1 }`           | Ascending | Optimizes queries sorting chats chronologically.                          |

```javascript
db.chats.createIndex({ user_id: 1 });
db.chats.createIndex({ video_id: 1 });
db.chats.createIndex({ user_id: 1, video_id: 1 });
db.chats.createIndex({ created_at: 1 });
```

---

### **3.5.3.4 Video User Uploads Collection**

| Index                            | Type      | Purpose                                                                  |
| -------------------------------- | --------- | ------------------------------------------------------------------------ |
| `{ user_id: 1 }`                 | Ascending | Optimizes queries fetching all videos uploaded by a user.                |
| `{ video_id: 1 }`                | Ascending | Optimizes queries checking if a particular video was uploaded by a user. |
| `{ user_id: 1, uploaded_at: 1 }` | Compound  | Speeds up queries fetching a user’s uploads sorted by upload date.       |

```javascript
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

## 3.7 System Architecture Diagrams

### 3.7.1 Frontend Architecture

```mermaid
graph TB
    subgraph "Frontend Layer"
        UI[Next.js Frontend]
        Auth[Authentication UI]
        Video[Video Interface]
        Chat[Chat Interface]
        Lib[Library Management]
    end

    subgraph "Frontend Components"
        Auth --> Login[Login Component]
        Auth --> Register[Register Component]
        Video --> Upload[URL Submit Form]
        Video --> Status[Processing Status]
        Chat --> ChatBox[Chat Interface]
        Chat --> History[Chat History]
        Lib --> VideoList[Video List]
        Lib --> Search[Search Component]
    end

    UI --> Auth
    UI --> Video
    UI --> Chat
    UI --> Lib
```

### 3.7.2 Backend Service Architecture

```mermaid
graph TB
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

    Gateway --> CORS
    CORS --> Auth_MW
    Auth_MW --> Rate
    Rate --> AuthSvc
    Rate --> VideoSvc
    Rate --> ChatSvc

    ChatSvc --> RAGSvc
```

### 3.7.3 Data Layer Architecture

```mermaid
graph TB
    subgraph "Service Layer"
        AuthSvc[Authentication Service]
        VideoSvc[Video Service]
        ChatSvc[Chat Service]
        RAGSvc[RAG Service]
    end

    subgraph "Data Layer"
        MongoDB[(MongoDB Primary Database)]
        ChromaDB[(ChromaDB Vector Store)]
    end

    subgraph "Collections"
        MongoDB --> Users[Users Collection]
        MongoDB --> Videos[Videos Collection]
        MongoDB --> Chats[Chats Collection]
        MongoDB --> Uploads[Video User Uploads]

        ChromaDB --> Embeddings[Video Embeddings]
    end

    AuthSvc --> Users
    VideoSvc --> Videos
    VideoSvc --> Uploads
    ChatSvc --> Chats
    RAGSvc --> Embeddings
```

### 3.7.4 External Services Integration

```mermaid
graph TB
    subgraph "Internal Services"
        VideoSvc[Video Service]
        RAGSvc[RAG Service]
        Worker[Background Workers]
    end

    subgraph "External Services"
        YouTube_API[YouTube API]
        Google_AI[Google AI Service]
        Translate[Google Translate]
    end

    subgraph "API Operations"
        YouTube_API --> Metadata[Video Metadata]
        YouTube_API --> Transcripts[Video Transcripts]
        Google_AI --> Summary[AI Summary]
        Google_AI --> Embeddings[Vector Embeddings]
        Translate --> Languages[Multi-language Support]
    end

    VideoSvc --> YouTube_API
    RAGSvc --> Google_AI
    VideoSvc --> Translate
    Worker --> YouTube_API
    Worker --> Google_AI
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

### 3.9.1 Data Storage and Optimization Strategy

```mermaid
graph TB
    User[User Request]
    API[API Server]
    MongoDB[(MongoDB Database)]
    ChromaDB[(ChromaDB Vector Store)]

    User -->|Request| API
    API -->|User/Video/Chat Data| MongoDB
    API -->|Vector Embeddings| ChromaDB
    MongoDB -->|Structured Data| API
    ChromaDB -->|Vector Search Results| API
    API -->|Response| User
```

**Current Storage Architecture:**

- **MongoDB**: Primary database for users, videos, chats, and metadata
- **ChromaDB**: Vector database for embeddings and semantic search
- **Local File System**: Temporary storage for video processing
- **Memory**: In-application caching for frequently accessed data

**Optimization Strategies Implemented:**

- Database indexing for frequently queried fields
- Vector embeddings stored efficiently in ChromaDB
- Asynchronous processing for video analysis
- Connection pooling for database efficiency

### 3.9.2 Scalability Design

| Component          | Scaling Strategy      | Current Implementation                     |
| ------------------ | --------------------- | ------------------------------------------ |
| API Server         | Horizontal scaling    | FastAPI with async/await patterns          |
| MongoDB            | Replica sets/Sharding | Single instance with indexing optimization |
| ChromaDB           | Distributed storage   | Single instance with efficient embeddings  |
| Background Workers | Async task processing | Python asyncio for concurrent processing   |
| Frontend           | Static asset serving  | Next.js with optimized builds              |
| AI Processing      | Batch processing      | Queue-based video processing               |
| Vector Operations  | Optimized queries     | ChromaDB similarity search                 |

**Database Storage Details:**

**MongoDB Collections:**

- `users`: User accounts and preferences
- `videos`: Video metadata and processing status
- `chats`: Chat conversations and message history
- `video_user_uploads`: User-video relationship mapping

**ChromaDB Collections:**

- `video_embeddings`: Vector embeddings for video content
- Document structure: ID, embedding vector, metadata, original text
- Metadata includes: youtube_id, language, content_type, timestamps

**Storage Optimization:**

- MongoDB indexes on frequently queried fields (email, youtube_id, user_id)
- ChromaDB uses efficient vector similarity search algorithms
- Text chunking for optimal embedding size and retrieval accuracy

## 3.10 Actual Implementation Summary

### 3.10.1 Technology Stack Verification

**Backend Technologies:**

- **FastAPI**: RESTful API server with async support
- **Python 3.12**: Runtime environment
- **Motor**: Async MongoDB driver
- **PyMongo**: MongoDB operations
- **Pydantic**: Data validation and serialization

**Database Technologies:**

- **MongoDB**: Primary database for structured data
  - Collections: users, videos, chats, video_user_uploads
  - Async operations with Motor driver
  - Indexes for performance optimization
- **ChromaDB**: Vector database for embeddings
  - Stores video content embeddings
  - Supports semantic similarity search
  - Integrated with LangChain framework

**AI and ML Technologies:**

- **Google Generative AI**: Primary LLM (Gemini 2.0 Flash)
- **LangChain**: Framework for AI application development
- **LangChain-Google-GenAI**: Google AI integration
- **LangChain-Chroma**: ChromaDB integration
- **LangChain-Community**: Additional tools and utilities

**External APIs:**

- **YouTube Transcript API**: Fetching video transcripts
- **YT-DLP**: Video metadata extraction
- **Google Cloud Translate**: Multilingual support

### 3.10.2 Data Flow Implementation

**Video Processing Flow:**

1. User submits YouTube URL via FastAPI endpoint
2. YT-DLP extracts video metadata
3. YouTube Transcript API fetches transcripts
4. Video data stored in MongoDB videos collection
5. Text chunks created and embedded using Google AI
6. Vector embeddings stored in ChromaDB
7. Video processing status updated in MongoDB

**Chat Processing Flow:**

1. User sends chat message via FastAPI endpoint
2. RAG service retrieves relevant video context from ChromaDB
3. Google Gemini AI generates contextual response
4. Chat message and response stored in MongoDB chats collection
5. Real-time response sent back to frontend

**Authentication Flow:**

1. User credentials validated against MongoDB users collection
2. JWT tokens generated using python-jose library
3. Secure password hashing with passlib and bcrypt
4. Session management through HTTP-only cookies

### 3.10.3 Performance Characteristics

**Current Limitations:**

- No external caching layer (Redis not implemented)
- Single-instance deployment for both databases
- Synchronous video processing (no dedicated queue system)
- In-memory temporary storage during processing

**Optimization Opportunities:**

- Implement Redis for session and query caching
- Add background task queue (Celery/RQ) for video processing
- Database replication for improved read performance
- CDN integration for static asset delivery

---

_This system design document reflects the actual implementation as of September 2025, ensuring accuracy between documentation and deployed system architecture._
