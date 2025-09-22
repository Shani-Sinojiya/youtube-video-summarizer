import { auth } from "@/auth";
import { ForgotPasswordForm } from "@/components/forgot-password-form";
import Logo from "@/components/logo";
import { WEB_APP_BASENAME } from "@/constants/web";
import { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";

export default async function LoginPage() {
  const session = await auth();
  if (session) {
    return redirect("/chat");
  }
  return (
    <div className="bg-muted flex min-h-svh flex-col items-center justify-center gap-6 p-6 md:p-10">
      <div className="flex w-full max-w-sm flex-col gap-6">
        <Link
          href="/"
          className="flex items-center gap-2 self-center font-medium"
        >
          <div className="bg-primary text-primary-foreground flex size-6 items-center justify-center rounded-md">
            <Logo className="h-4 w-4" />
          </div>
          {WEB_APP_BASENAME}
        </Link>
        <ForgotPasswordForm />
      </div>
    </div>
  );
}

export const metadata: Metadata = {
  title: "Forgot Password | " + WEB_APP_BASENAME,
  description: "Reset your password to access the application.",
};
