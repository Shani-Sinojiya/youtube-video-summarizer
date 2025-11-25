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
          // Missing credentials — return null to indicate authentication failure
          return null;
        }

        console.log("Attempting to log in user:", credentials.email);

        const res = await fetch(`${process.env.API_URL}/auth/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            email: credentials.email,
            password: credentials.password,
          }),
        });

        // Parse the response once
        let payload: any = null;
        try {
          payload = await res.json();
        } catch {
          payload = null;
        }

        if (!res.ok) {
          const detail = (payload && payload.detail) || "Invalid credentials";
          console.error("Login error:", payload);
          // Rethrow so AuthJS can pass the message to the client (signIn(..., { redirect: false }))
          throw new Error(detail);
        }

        // res.ok === true
        const { data, access_token } = payload || {};

        if (!data || !data.id) {
          // Invalid credentials or malformed response — return null
          console.error("Login error: missing user data", payload);
          return null;
        }

        return {
          id: access_token,
          name: "User",
          email: data.email,
          image: access_token,
          token: access_token,
        };
      },
    }),
  ],
  session: {
    strategy: "jwt",
    maxAge: 30 * 24 * 60 * 60, // 30 days
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
