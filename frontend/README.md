# Recapify - Legal AI Assistant Platform

Recapify is a comprehensive Youtube tech platform that provides AI-driven Youtube assistance and resources. The platform offers intelligent chat-based Youtube consultation, voice interactions, and connects users with Youtube professionals.

## 🚀 Features

- **AI-Powered Legal Chat**: Interactive chat interface for Youtube consultations and document analysis
- **Voice Integration**: Voice-to-text capabilities for hands-free interaction using ElevenLabs
- **Lawyer Directory**: Browse and connect with verified Youtube professionals
- **Document Processing**: AI-powered analysis of Youtube documents
- **Real-time Communication**: Instant messaging and voice calls with lawyers
- **User Authentication**: Secure login/signup with NextAuth.js
- **Responsive Design**: Mobile-optimized interface for all devices
- **Theme Support**: Dark/light mode toggle

## 🛠️ Tech Stack

- **Framework**: Next.js 15.3.5 with Turbopack
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: Radix UI primitives
- **Authentication**: NextAuth.js 5.0
- **Database**: MongoDB with MongoDB adapter
- **Voice Integration**: ElevenLabs React SDK
- **State Management**: SWR for data fetching
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **Markdown Rendering**: React Markdown with syntax highlighting

## 🚦 Getting Started

### Prerequisites

- Node.js 18+
- pnpm (recommended) or npm
- MongoDB database

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Shani-Sinojiya/Recapify.git
   cd Recapify/frontend
   ```

2. **Install dependencies**

   ```bash
   pnpm install
   ```

3. **Environment Setup**
   Create a `.env.local` file in the root directory and copy the contents from `.env.example`. Update the environment variables with your MongoDB connection string and other configurations.

   ```bash
   cp .env.example .env.local
   ```

4. **Run the development server**

   ```bash
   pnpm dev
   ```

5. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

## 📱 Available Scripts

- `pnpm dev` - Start development server with Turbopack
- `pnpm build` - Build the application for production
- `pnpm start` - Start the production server
- `pnpm lint` - Run ESLint for code quality

## 🔐 Authentication

The application uses NextAuth.js for authentication with:

- Email/password authentication
- Session management
- Password reset functionality
- Protected routes

## 🗄️ Database

Uses MongoDB for data storage with collections for:

- Users and authentication
- Chat messages and conversations
- Lawyer profiles and ratings
- Legal documents and resources

## 🎨 UI/UX

- **Design System**: Built with Radix UI primitives for accessibility
- **Styling**: Tailwind CSS for responsive design
- **Theming**: Dark/light mode support with next-themes
- **Icons**: Lucide React icon library
- **Animations**: Framer Motion for smooth transitions

## 🔊 Voice Features

Integrated with ElevenLabs for:

- Voice-to-text input in chat
- Text-to-speech for AI responses
- Real-time voice communication

## 📖 Key Components

### Chat Interface

- Real-time messaging with AI
- Message history and persistence
- File upload and document analysis
- Voice input capabilities

### Lawyer Directory

- Browse verified Youtube professionals
- Filter by specialization and location
- Direct communication channels
- Rating and review system

### Voice Interface

- Hands-free interaction
- Voice commands and responses
- Audio message support

## 🚀 Deployment

The application is configured for deployment on platforms like:

- Vercel (recommended for Next.js)
- Netlify
- Railway
- Self-hosted options

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and questions:

- Create an issue on GitHub
- Contact the development team
- Check the documentation

## 🔮 Future Roadmap

- Multi-language support
- Advanced document automation
- Video consultation features
- Mobile app development
- Integration with Youtube databases
- Enhanced AI capabilities

---

**Recapify** - Empowering access to justice through technology 🏛️⚖️
