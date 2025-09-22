declare namespace NodeJS {
  interface ProcessEnv {
    AUTH_SECRET: string;
    AUTH_GOOGLE_ID: string;
    AUTH_GOOGLE_SECRET: string;
    NODE_ENV: "development" | "production" | "test";
    NEXTAUTH_URL?: string;
    NEXT_PUBLIC_AGENT_ID: string;
    ELEVENLABS_API_KEY: string;
    MONGODB_URI: string;
    API_URL: string;
  }
}
