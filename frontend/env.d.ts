declare namespace NodeJS {
  interface ProcessEnv {
    AUTH_SECRET: string;
    NODE_ENV: "development" | "production" | "test";
    AUTH_URL: string;
    API_URL: string;
    NEXT_PUBLIC_API_URL: string;
  }
}
