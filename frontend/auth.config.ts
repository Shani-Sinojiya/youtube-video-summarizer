import NextAuth from "next-auth";
import Credentials from "next-auth/providers/credentials";

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    Credentials({
      id: "signin",
      name: "signin",
      credentials: {
        email: { label: "Email", type: "email", placeholder: "m@example.com" },
        password: {
          label: "Password",
          type: "password",
          placeholder: "••••••••",
        },
      },
      async authorize(credentials, req) {
        if (!credentials?.email || !credentials?.password) {
          return new Error("Email and password are required");
        }
        try {
          console.log("Attempting to log in user:", credentials.email);

          const res = await fetch(`${process.env.API_URL}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              email: credentials.email,
              password: credentials.password,
            }),
          });

          if (res.ok) {
            const { data, access_token } = await res.json();

            if (!data || !data.id) {
              return new Error("Invalid credentials");
            }

            console.log(access_token);

            return {
              id: access_token,
              name: "User",
              email: data.email,
              image: access_token,
              token: access_token,
            };
          }
          const errorData = await res.json();
          console.error("Login error:", errorData);
          if (errorData.error) {
            return new Error(errorData.error);
          }
          return new Error("Failed to log in");
        } catch (error) {
          console.error("Error during login:", error);
          if (error instanceof Error) {
            return new Error(error.message);
          }
        }
        return null; // Return null if no user found
      },
    }),
  ],
  session: {
    strategy: "jwt",
    maxAge: 1 * 24 * 60 * 60,
  },
  // adapter: MongoDBAdapter(client),
  secret: process.env.AUTH_SECRET || "",
  pages: {
    signIn: "/login",
  },
  callbacks: {
    async session({ session, user }) {
      if (user) session.user.id = user.id;
      return session;
    },
    async jwt({ token, user }) {
      if (user) token.id = user.id;
      return token;
    },
  },
  // debug: true,
  cookies: {
    sessionToken: {
      name: "Recapify.session-token",
      options: {
        httpOnly: true,
        sameSite: "lax",
      },
    },
    callbackUrl: {
      name: "Recapify.callback-url",
      options: {
        httpOnly: true,
        sameSite: "lax",
      },
    },
    csrfToken: {
      name: "Recapify.csrf-token",
      options: {
        httpOnly: true,
        sameSite: "lax",
      },
    },
    pkceCodeVerifier: {
      name: "Recapify.pkce-code-verifier",
      options: {
        httpOnly: true,
        sameSite: "lax",
      },
    },
  },
});
